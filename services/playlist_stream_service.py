"""Incremental playlist extraction service."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from core.dependency_checker import DependencyChecker
from core.exceptions import CommandExecutionError, DependencyUnavailableError, MetadataExtractionError
from core.process import create_text_process, request_process_termination, wait_for_process
from models.playlist_metadata import PlaylistVideo
from models.playlist_range import PlaylistRange
from services.yt_dlp_command_builder import YtDlpCommandBuilder


PlaylistBatchCallback = Callable[[tuple[PlaylistVideo, ...], int, int | None], None]
PlaylistTotalCallback = Callable[[int], None]
PlaylistLimitCallback = Callable[[int, int], None]
PlaylistFallbackCallback = Callable[[], None]
MAX_DIAGNOSTIC_LINES: int = 20


@dataclass(frozen=True, slots=True)
class PlaylistStreamResult:
    """Result of an incremental playlist stream.

    Attributes:
        processed_count: Number of selectable videos emitted.
        cancelled: Whether the user cancelled the process.
        limit_reached: Whether processing stopped at the configured limit.
    """

    processed_count: int
    cancelled: bool
    limit_reached: bool


class PlaylistStreamService:
    """Streams playlist and YouTube Mix entries through yt-dlp."""

    def __init__(
        self,
        dependency_checker: DependencyChecker | None = None,
        command_builder: YtDlpCommandBuilder | None = None,
    ) -> None:
        """Initialize the playlist stream service.

        Args:
            dependency_checker: Dependency checker instance.
            command_builder: yt-dlp command builder.
        """
        self._dependency_checker: DependencyChecker = dependency_checker or DependencyChecker()
        self._command_builder: YtDlpCommandBuilder = command_builder or YtDlpCommandBuilder()
        self._process: subprocess.Popen[str] | None = None
        self._cancel_requested: bool = False

    def stream_playlist(
        self,
        source_url: str,
        playlist_range: PlaylistRange,
        batch_size: int,
        batch_loaded: PlaylistBatchCallback,
        total_detected: PlaylistTotalCallback,
        limit_reached: PlaylistLimitCallback,
        fallback_used: PlaylistFallbackCallback,
    ) -> PlaylistStreamResult:
        """Stream playlist videos incrementally.

        Args:
            source_url: Source playlist or YouTube Mix URL.
            playlist_range: One-based inclusive range to emit.
            batch_size: Number of videos emitted per batch.
            batch_loaded: Callback called for each batch of selectable videos.
            total_detected: Callback called when yt-dlp exposes a total count.
            limit_reached: Callback retained for compatibility with older callers.
            fallback_used: Callback called before safe incremental fallback scanning.

        Returns:
            Streaming result.

        Raises:
            DependencyUnavailableError: If yt-dlp is unavailable.
            MetadataExtractionError: If no selectable videos are found.
            CommandExecutionError: If yt-dlp fails.
        """
        self._cancel_requested = False
        dependency_result = self._dependency_checker.check()
        if not dependency_result.yt_dlp.is_available:
            raise DependencyUnavailableError("yt-dlp is not available in PATH.")

        try:
            return self._stream_playlist_once(
                source_url=source_url,
                playlist_range=playlist_range,
                batch_size=batch_size,
                batch_loaded=batch_loaded,
                total_detected=total_detected,
                use_ytdlp_range=True,
            )
        except (CommandExecutionError, MetadataExtractionError):
            if self._cancel_requested:
                raise
            fallback_used()
            return self._stream_playlist_once(
                source_url=source_url,
                playlist_range=playlist_range,
                batch_size=batch_size,
                batch_loaded=batch_loaded,
                total_detected=total_detected,
                use_ytdlp_range=False,
            )

    def _stream_playlist_once(
        self,
        source_url: str,
        playlist_range: PlaylistRange,
        batch_size: int,
        batch_loaded: PlaylistBatchCallback,
        total_detected: PlaylistTotalCallback,
        use_ytdlp_range: bool,
    ) -> PlaylistStreamResult:
        """Stream a playlist once, optionally using yt-dlp range options."""
        command: list[str] = self._command_builder.build_playlist_stream_command(
            source_url,
            playlist_range if use_ytdlp_range else None,
        )
        processed_count: int = 0
        scanned_count: int = 0
        detected_total: int | None = None
        stopped_at_range_end: bool = False
        pending_batch: list[PlaylistVideo] = []
        diagnostic_lines: list[str] = []

        try:
            self._process = create_text_process(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
            )
        except FileNotFoundError as exc:
            raise CommandExecutionError(f"Command not found: {command[0]}") from exc

        if self._process.stdout is None:
            self.cancel()
            raise CommandExecutionError("yt-dlp did not provide playlist output.")

        try:
            for line in self._process.stdout:
                if self._cancel_requested:
                    self.cancel()
                    break

                entry: dict[str, Any] | None = self._parse_json_line(line)
                if entry is None:
                    self._append_diagnostic_line(diagnostic_lines, line)
                    continue

                new_total: int | None = self._read_playlist_total(entry)
                if new_total is not None and new_total != detected_total:
                    detected_total = new_total
                    total_detected(new_total)
                    if new_total > playlist_range.item_count:
                        limit_reached(new_total, playlist_range.item_count)

                scanned_count += 1
                entry_index: int = self._read_playlist_index(
                    entry,
                    scanned_count,
                    playlist_range.start_index,
                    use_ytdlp_range,
                )

                if entry_index < playlist_range.start_index:
                    continue
                if entry_index > playlist_range.end_index:
                    stopped_at_range_end = True
                    if self._process is not None:
                        request_process_termination(self._process)
                    break

                video: PlaylistVideo | None = PlaylistVideo.from_entry(entry_index, entry)
                if video is None:
                    continue

                processed_count += 1
                pending_batch.append(video)
                if len(pending_batch) >= max(1, batch_size):
                    batch_loaded(tuple(pending_batch), processed_count, detected_total)
                    pending_batch.clear()
        finally:
            if self._process.stdout is not None:
                self._process.stdout.close()

        if pending_batch:
            batch_loaded(tuple(pending_batch), processed_count, detected_total)

        return_code: int = self._wait_for_process()
        self._process = None

        if self._cancel_requested:
            return PlaylistStreamResult(
                processed_count=processed_count,
                cancelled=True,
                limit_reached=False,
            )
        if return_code != 0 and not stopped_at_range_end:
            message: str = "\n".join(diagnostic_lines[-MAX_DIAGNOSTIC_LINES:]).strip()
            if not message:
                message = "yt-dlp playlist streaming failed."
            raise CommandExecutionError(message)
        if processed_count == 0:
            raise MetadataExtractionError("No selectable videos were found in the playlist.")
        return PlaylistStreamResult(
            processed_count=processed_count,
            cancelled=False,
            limit_reached=False,
        )

    def cancel(self) -> None:
        """Request cancellation and stop the active yt-dlp process."""
        self._cancel_requested = True
        if self._process is not None and self._process.poll() is None:
            request_process_termination(self._process)

    def _wait_for_process(self) -> int:
        """Wait for the active process and force termination when needed."""
        if self._process is None:
            return 0
        return wait_for_process(self._process)

    @staticmethod
    def _parse_json_line(line: str) -> dict[str, Any] | None:
        """Parse a single yt-dlp JSON line."""
        stripped_line: str = line.strip()
        if not stripped_line:
            return None
        try:
            data: Any = json.loads(stripped_line)
        except json.JSONDecodeError:
            return None
        if isinstance(data, dict):
            return data
        return None

    @staticmethod
    def _append_diagnostic_line(diagnostic_lines: list[str], line: str) -> None:
        """Keep a bounded set of non-JSON diagnostic output lines."""
        stripped_line: str = line.strip()
        if not stripped_line:
            return
        diagnostic_lines.append(stripped_line)
        if len(diagnostic_lines) > MAX_DIAGNOSTIC_LINES:
            del diagnostic_lines[0]

    @staticmethod
    def _read_playlist_total(entry: dict[str, Any]) -> int | None:
        """Read a total playlist count when yt-dlp exposes one."""
        for key in ("playlist_count", "n_entries"):
            value: Any = entry.get(key)
            if isinstance(value, int) and value > 0:
                return value
        return None

    @staticmethod
    def _read_playlist_index(
        entry: dict[str, Any],
        scanned_count: int,
        requested_start_index: int,
        use_ytdlp_range: bool,
    ) -> int:
        """Read the absolute playlist index for a streamed entry."""
        value: Any = entry.get("playlist_index")
        if isinstance(value, int) and value > 0:
            return value
        if use_ytdlp_range:
            return requested_start_index + scanned_count - 1
        return scanned_count
