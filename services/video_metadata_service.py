"""Video metadata extraction service."""

from __future__ import annotations

import json
from typing import Any

from core.dependency_checker import DependencyChecker
from core.exceptions import DependencyUnavailableError, MetadataExtractionError
from models.video_metadata import VideoMetadata
from services.subprocess_runner import CommandResult, SubprocessRunner
from services.yt_dlp_command_builder import YtDlpCommandBuilder


class VideoMetadataService:
    """Extracts video metadata through yt-dlp."""

    def __init__(
        self,
        dependency_checker: DependencyChecker | None = None,
        command_builder: YtDlpCommandBuilder | None = None,
        subprocess_runner: SubprocessRunner | None = None,
    ) -> None:
        """Initialize the metadata service.

        Args:
            dependency_checker: Dependency checker instance.
            command_builder: yt-dlp command builder.
            subprocess_runner: Subprocess runner instance.
        """
        self._dependency_checker: DependencyChecker = dependency_checker or DependencyChecker()
        self._command_builder: YtDlpCommandBuilder = command_builder or YtDlpCommandBuilder()
        self._subprocess_runner: SubprocessRunner = subprocess_runner or SubprocessRunner()

    def load_metadata(self, source_url: str) -> VideoMetadata:
        """Load metadata for a single video URL.

        Args:
            source_url: Source video URL.

        Returns:
            Extracted video metadata.

        Raises:
            DependencyUnavailableError: If yt-dlp is unavailable.
            MetadataExtractionError: If yt-dlp returns invalid metadata.
        """
        dependency_result = self._dependency_checker.check()
        if not dependency_result.yt_dlp.is_available:
            raise DependencyUnavailableError("yt-dlp is not available in PATH.")

        command: list[str] = self._command_builder.build_metadata_command(source_url)
        result: CommandResult = self._subprocess_runner.run(command)
        try:
            data: Any = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise MetadataExtractionError("yt-dlp returned invalid JSON metadata.") from exc

        if not isinstance(data, dict):
            raise MetadataExtractionError("yt-dlp metadata response is not an object.")

        return VideoMetadata.from_yt_dlp_json(source_url, data)
