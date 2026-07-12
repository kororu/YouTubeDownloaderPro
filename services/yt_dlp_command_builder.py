"""yt-dlp command generation."""

from __future__ import annotations

from dataclasses import dataclass

from models.download_enums import DownloadFormat, DownloadQuality
from models.playlist_range import PlaylistRange


@dataclass(frozen=True, slots=True)
class YtDlpCommandBuilder:
    """Builds yt-dlp commands without executing them."""

    executable_name: str = "yt-dlp"

    def build_metadata_command(self, source_url: str) -> list[str]:
        """Build a command that extracts single-video metadata as JSON.

        Args:
            source_url: Source video URL.

        Returns:
            Command arguments ready for subprocess execution.
        """
        return [
            self.executable_name,
            "--dump-single-json",
            "--no-playlist",
            "--no-warnings",
            source_url,
        ]

    def build_playlist_metadata_command(self, source_url: str) -> list[str]:
        """Build a command that extracts playlist metadata as JSON.

        Args:
            source_url: Source playlist URL.

        Returns:
            Command arguments ready for subprocess execution.
        """
        return [
            self.executable_name,
            "--dump-single-json",
            "--yes-playlist",
            "--no-warnings",
            source_url,
        ]

    def build_playlist_stream_command(
        self,
        source_url: str,
        playlist_range: PlaylistRange | None = None,
    ) -> list[str]:
        """Build a command that streams flat playlist entries as JSON lines.

        Args:
            source_url: Source playlist or YouTube Mix URL.
            playlist_range: Optional one-based inclusive playlist range.

        Returns:
            Command arguments ready for subprocess execution.
        """
        command: list[str] = [
            self.executable_name,
            "--dump-json",
            "--flat-playlist",
            "--yes-playlist",
            "--no-warnings",
        ]
        if playlist_range is not None:
            command.extend(
                [
                    "--playlist-start",
                    str(playlist_range.start_index),
                    "--playlist-end",
                    str(playlist_range.end_index),
                ]
            )
        command.append(source_url)
        return command

    def build_download_command(
        self,
        source_url: str,
        output_template: str,
        media_format: DownloadFormat,
        quality: DownloadQuality,
    ) -> list[str]:
        """Build a future download command without executing it.

        Args:
            source_url: Source media URL.
            output_template: yt-dlp output template.
            media_format: Desired media format.
            quality: Desired quality.

        Returns:
            Command arguments ready for future download execution.
        """
        command: list[str] = [self.executable_name, "--newline", "-o", output_template]
        if media_format is DownloadFormat.MP3:
            command.extend(["-x", "--audio-format", "mp3"])
        else:
            command.extend(["--merge-output-format", "mp4", "-f", self._video_format_selector(quality)])
        command.append(source_url)
        return command

    @staticmethod
    def _video_format_selector(quality: DownloadQuality) -> str:
        """Build a yt-dlp format selector for video quality."""
        if quality is DownloadQuality.BEST:
            return "bestvideo+bestaudio/best"
        return f"bestvideo[height<={quality.value}]+bestaudio/best[height<={quality.value}]"
