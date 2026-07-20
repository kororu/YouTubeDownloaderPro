"""yt-dlp command generation."""

from __future__ import annotations

from dataclasses import dataclass

from models.download_enums import AudioQuality, DownloadFormat, DownloadQuality
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
        audio_quality: AudioQuality = AudioQuality.BEST,
        download_thumbnail: bool = False,
        write_metadata: bool = False,
        write_subtitles: bool = False,
        write_auto_subtitles: bool = False,
        subtitle_languages: str = "es,en",
        download_rate_limit: int = 0,
        retries: int = 3,
        fragment_retries: int = 3,
        socket_timeout: int = 30,
        sleep_interval: int = 0,
        prefer_ipv4: bool = False,
        prefer_ipv6: bool = False,
        continue_downloads: bool = True,
        no_overwrites: bool = False,
        use_browser_cookies: bool = False,
        browser_cookies_source: str = "none",
        cookies_file_path: str = "",
        proxy_url: str = "",
    ) -> list[str]:
        """Build a future download command without executing it.

        Args:
            source_url: Source media URL.
            output_template: yt-dlp output template.
            media_format: Desired media format.
            quality: Desired quality.
            audio_quality: MP3 bitrate or best/original selection.
            download_thumbnail: Whether to write the source thumbnail.
            write_metadata: Whether to write an info JSON file.
            write_subtitles: Whether to write published subtitles.
            write_auto_subtitles: Whether to write automatic subtitles.
            subtitle_languages: Comma-separated yt-dlp language selector.

        Returns:
            Command arguments ready for future download execution.
        """
        command: list[str] = [
            self.executable_name,
            "--newline",
            "--print",
            "after_move:__OUTPUT_PATH__%(filepath)s",
            "--windows-filenames",
            "-o",
            output_template,
        ]
        if download_rate_limit > 0: command.extend(["--limit-rate", str(download_rate_limit)])
        command.extend(["--retries", str(max(0, retries)), "--fragment-retries", str(max(0, fragment_retries)), "--socket-timeout", str(max(0, socket_timeout))])
        if sleep_interval > 0: command.extend(["--sleep-interval", str(sleep_interval)])
        if prefer_ipv4: command.append("--force-ipv4")
        elif prefer_ipv6: command.append("--force-ipv6")
        if continue_downloads: command.append("--continue")
        if no_overwrites: command.append("--no-overwrites")
        if cookies_file_path.strip():
            command.extend(["--cookies", cookies_file_path.strip()])
        elif use_browser_cookies and browser_cookies_source in {"chrome", "edge", "firefox", "brave", "opera"}:
            command.extend(["--cookies-from-browser", browser_cookies_source])
        if proxy_url.strip(): command.extend(["--proxy", proxy_url.strip()])
        if media_format is DownloadFormat.MP4:
            command.extend(["--merge-output-format", "mp4", "-f", self._video_format_selector(quality)])
        else:
            command.extend(["-f", self._audio_format_selector(media_format)])
            if media_format is not DownloadFormat.BEST_AUDIO:
                command.extend(["-x", "--audio-format", media_format.value])
            if media_format is DownloadFormat.MP3 and audio_quality is not AudioQuality.BEST:
                command.extend(["--audio-quality", f"{audio_quality.value}K"])
        if download_thumbnail:
            command.append("--write-thumbnail")
        if write_metadata:
            command.append("--write-info-json")
        if write_subtitles:
            command.append("--write-subs")
        if write_auto_subtitles:
            command.append("--write-auto-subs")
        if write_subtitles or write_auto_subtitles:
            command.extend(["--sub-langs", subtitle_languages])
        command.append(source_url)
        return command

    @staticmethod
    def _audio_format_selector(media_format: DownloadFormat) -> str:
        """Build a best-audio selector that prefers matching source codecs."""
        if media_format is DownloadFormat.M4A:
            return "bestaudio[ext=m4a]/bestaudio/best"
        if media_format is DownloadFormat.OPUS:
            return "bestaudio[acodec^=opus]/bestaudio/best"
        return "bestaudio/best"

    @staticmethod
    def _video_format_selector(quality: DownloadQuality) -> str:
        """Build a yt-dlp format selector for video quality."""
        if quality is DownloadQuality.BEST:
            return "bestvideo+bestaudio/best"
        return f"bestvideo[height<={quality.value}]+bestaudio/best[height<={quality.value}]"
