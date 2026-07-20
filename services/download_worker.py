"""QThread worker for real download execution."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from core.dependency_checker import DependencyChecker
from core.process import create_text_process, request_process_termination, wait_for_process
from models.download_item import DownloadItem
from models.download_progress import DownloadProgress
from services.progress_parser import ProgressParser
from services.output_template_builder import OutputTemplateBuilder
from services.yt_dlp_command_builder import YtDlpCommandBuilder


class DownloadWorker(QThread):
    """Runs a single yt-dlp download outside the UI thread."""

    progress_changed: Signal = Signal(str, object)
    log_received: Signal = Signal(str, str)
    download_completed: Signal = Signal(str, str)
    download_failed: Signal = Signal(str, str)
    download_cancelled: Signal = Signal(str)

    def __init__(
        self,
        download_item: DownloadItem,
        output_folder: Path,
        command_builder: YtDlpCommandBuilder | None = None,
        dependency_checker: DependencyChecker | None = None,
        progress_parser: ProgressParser | None = None,
        output_template_builder: OutputTemplateBuilder | None = None,
    ) -> None:
        """Initialize the download worker.

        Args:
            download_item: Download item to execute.
            output_folder: Destination folder.
            command_builder: yt-dlp command builder.
            dependency_checker: Dependency checker.
            progress_parser: yt-dlp progress parser.
        """
        super().__init__()
        self._download_item: DownloadItem = download_item
        self._output_folder: Path = output_folder
        self._command_builder: YtDlpCommandBuilder = command_builder or YtDlpCommandBuilder()
        self._dependency_checker: DependencyChecker = dependency_checker or DependencyChecker()
        self._progress_parser: ProgressParser = progress_parser or ProgressParser()
        self._output_template_builder: OutputTemplateBuilder = output_template_builder or OutputTemplateBuilder()
        self._process: subprocess.Popen[str] | None = None
        self._cancel_requested: bool = False
        self._output_path: str = ""

    @property
    def item_id(self) -> str:
        """Return the download item identifier."""
        return self._download_item.item_id

    def cancel(self) -> None:
        """Cancel the running process."""
        self._cancel_requested = True
        if self._process is not None and self._process.poll() is None:
            request_process_termination(self._process)

    def run(self) -> None:
        """Execute the download command."""
        dependency_result = self._dependency_checker.check()
        if not dependency_result.yt_dlp.is_available:
            self.download_failed.emit(self.item_id, "yt-dlp is not available in PATH.")
            return
        if self._download_item.media_format.requires_ffmpeg and not dependency_result.ffmpeg.is_available:
            self.download_failed.emit(
                self.item_id,
                f"ffmpeg is required for {self._download_item.media_format.value.upper()} downloads.",
            )
            return

        self._output_folder.mkdir(parents=True, exist_ok=True)
        output_template: str = self._output_template_builder.build(self._output_folder, self._download_item)
        command: list[str] = self._command_builder.build_download_command(
            source_url=self._download_item.source_url,
            output_template=output_template,
            media_format=self._download_item.media_format,
            quality=self._download_item.quality,
            audio_quality=self._download_item.audio_quality,
            download_thumbnail=self._download_item.download_thumbnail,
            write_metadata=self._download_item.write_metadata,
            write_subtitles=self._download_item.write_subtitles,
            write_auto_subtitles=self._download_item.write_auto_subtitles,
            subtitle_languages=self._download_item.subtitle_languages,
        )

        try:
            self._process = create_text_process(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except OSError as exc:
            self.download_failed.emit(self.item_id, str(exc))
            return

        if self._process.stdout is not None:
            for line in self._process.stdout:
                if self._cancel_requested:
                    break
                stripped_line: str = line.rstrip()
                if stripped_line:
                    if self._read_output_path(stripped_line):
                        continue
                    self.log_received.emit(self.item_id, stripped_line)
                    if self._subtitles_unavailable(stripped_line):
                        self.log_received.emit(self.item_id, "Subtitles not available")
                progress: DownloadProgress | None = self._progress_parser.parse(line)
                if progress is not None:
                    self.progress_changed.emit(self.item_id, progress)

        return_code: int = wait_for_process(self._process)
        if self._cancel_requested:
            self.download_cancelled.emit(self.item_id)
            return
        if return_code == 0:
            self.download_completed.emit(self.item_id, self._output_path)
            return
        self.download_failed.emit(self.item_id, f"yt-dlp exited with code {return_code}.")

    @staticmethod
    def _subtitles_unavailable(log_line: str) -> bool:
        """Return whether yt-dlp reports that subtitles are unavailable."""
        normalized_line: str = log_line.lower()
        return "no subtitles" in normalized_line or "does not have subtitles" in normalized_line

    def _read_output_path(self, log_line: str) -> bool:
        """Capture the final yt-dlp output path without displaying the marker."""
        marker = "__OUTPUT_PATH__"
        if not log_line.startswith(marker):
            return False
        self._output_path = log_line.removeprefix(marker).strip()
        return True
