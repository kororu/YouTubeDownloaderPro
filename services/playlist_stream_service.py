"""Incremental playlist extraction service."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from core.dependency_checker import DependencyChecker
from core.exceptions import CommandExecutionError, DependencyUnavailableError, MetadataExtractionError
from models.playlist_metadata import PlaylistVideo
from services.yt_dlp_command_builder import YtDlpCommandBuilder


PlaylistBatchCallback = Callable[[tuple[PlaylistVideo, ...], int, int | None], None]
PlaylistTotalCallback = Callable[[int], None]
PlaylistLimitCallback = Callable[[int, int], None]


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
        max_items: int,
        batch_size: int,
        batch_loaded: PlaylistBatchCallback,
        total_detected: PlaylistTotalCallback,
        limit_reached: PlaylistLimitCallback,
    ) -> PlaylistStreamResult:
        """Stream playlist videos incrementally.

        Args:
            source_url: Source playlist or YouTube Mix URL.
            max_items: Maximum videos to emit, or 0 for no configured limit.
            batch_size: Number of videos emitted per batch.
            batch_loaded: Callback called for each batch of selectable videos.
            total_detected: Callback called when yt-dlp exposes a total count.
            limit_reached: Callback called when the configured limit is reached.

        Returns:
            Streaming result.

        Raises:
            DependencyUnavailableError: If yt-dlp is unavailable.
            MetadataExtractionError: If no selectable videos are found.
            CommandExecutionError: If yt-dlp fails.
        """
        dependency_result = self._dependency_checker.check()
        if not dependency_result.yt_dlp.is_available:
            raise DependencyUnavailableError("yt-dlp is not available in PATH.")

        command: list[str] = self._command_builder.build_playlist_stream_command(source_url)
        processed_count: int = 0
        detected_total: int | None = None
        emitted_limit_warning: bool = False
        stopped_at_limit: bool = False
        pending_batch: list[PlaylistVideo] = []
        stderr_text: str = ""

        try:
            self._process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
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
                    continue

                new_total: int | None = self._read_playlist_total(entry)
                if new_total is not None and new_total != detected_total:
                    detected_total = new_total
                    total_detected(new_total)
                    if max_items > 0 and new_total > max_items and not emitted_limit_warning:
                        emitted_limit_warning = True
                        limit_reached(new_total, max_items)

                if max_items > 0 and processed_count >= max_items:
                    stopped_at_limit = True
                    self.cancel()
                    break

                video: PlaylistVideo | None = PlaylistVideo.from_entry(processed_count + 1, entry)
                if video is None:
                    continue

                processed_count += 1
                pending_batch.append(video)
                if len(pending_batch) >= max(1, batch_size):
                    batch_loaded(tuple(pending_batch), processed_count, detected_total)
                    pending_batch.clear()

                if max_items > 0 and processed_count >= max_items:
                    stopped_at_limit = True
                    self.cancel()
                    break
        finally:
            if self._process.stdout is not None:
                self._process.stdout.close()

        if pending_batch:
            batch_loaded(tuple(pending_batch), processed_count, detected_total)

        if self._process.stderr is not None:
            stderr_text = self._process.stderr.read()
            self._process.stderr.close()

        return_code: int | None = self._process.wait()
        self._process = None

        if self._cancel_requested:
            return PlaylistStreamResult(
                processed_count=processed_count,
                cancelled=not stopped_at_limit,
                limit_reached=stopped_at_limit,
            )
        if return_code != 0:
            message: str = stderr_text.strip() or "yt-dlp playlist streaming failed."
            raise CommandExecutionError(message)
        if processed_count == 0:
            raise MetadataExtractionError("No selectable videos were found in the playlist.")
        return PlaylistStreamResult(
            processed_count=processed_count,
            cancelled=False,
            limit_reached=stopped_at_limit,
        )

    def cancel(self) -> None:
        """Request cancellation and stop the active yt-dlp process."""
        self._cancel_requested = True
        if self._process is not None and self._process.poll() is None:
            self._process.terminate()

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
    def _read_playlist_total(entry: dict[str, Any]) -> int | None:
        """Read a total playlist count when yt-dlp exposes one."""
        for key in ("playlist_count", "n_entries"):
            value: Any = entry.get(key)
            if isinstance(value, int) and value > 0:
                return value
        return None
