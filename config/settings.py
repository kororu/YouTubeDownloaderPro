"""Persistent application settings model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Self


@dataclass(frozen=True, slots=True)
class Settings:
    """User-configurable application settings.

    Attributes:
        output_folder: Default folder used for downloaded files.
        selected_format: Preferred media format.
        selected_quality: Preferred video quality.
        selected_audio_quality: Preferred MP3 bitrate or best/original audio.
        theme: Active visual theme name, forced to dark for compatibility.
        background_image_path: Optional custom application background image path.
        background_opacity: Image visibility behind the dark readability overlay.
        compact_mode: Whether the interface uses reduced visual spacing.
        download_thumbnail: Whether downloads include a thumbnail file.
        write_metadata: Whether downloads include an info JSON file.
        write_subtitles: Whether published subtitles are requested.
        write_auto_subtitles: Whether automatic subtitles are requested.
        subtitle_languages: Comma-separated yt-dlp subtitle languages.
        filename_template: Safe yt-dlp filename template.
        create_channel_folder: Whether output is grouped by channel.
        create_playlist_folder: Whether playlist output uses its own folder.
        max_playlist_items: Maximum playlist or YouTube Mix videos processed per request.
        playlist_start_index: Default one-based playlist start index.
        playlist_end_index: Optional default playlist end index, or 0 for automatic limit.
        window_width: Main window width in pixels.
        window_height: Main window height in pixels.
        window_x: Main window horizontal screen position.
        window_y: Main window vertical screen position.
        max_concurrent_downloads: Maximum simultaneous downloads.
    """

    output_folder: str
    selected_format: str
    selected_quality: str
    selected_audio_quality: str
    theme: str
    background_image_path: str
    background_opacity: float
    compact_mode: bool
    prevent_queue_duplicates: bool
    warn_already_downloaded: bool
    allow_redownload_completed: bool
    download_rate_limit: int
    retries: int
    fragment_retries: int
    socket_timeout: int
    sleep_interval: int
    prefer_ipv4: bool
    prefer_ipv6: bool
    continue_downloads: bool
    no_overwrites: bool
    use_browser_cookies: bool
    browser_cookies_source: str
    proxy_enabled: bool
    proxy_url: str
    diagnostic_mode: bool
    download_thumbnail: bool
    write_metadata: bool
    write_subtitles: bool
    write_auto_subtitles: bool
    subtitle_languages: str
    filename_template: str
    create_channel_folder: bool
    create_playlist_folder: bool
    max_playlist_items: int
    playlist_start_index: int
    playlist_end_index: int
    window_width: int
    window_height: int
    window_x: int
    window_y: int
    max_concurrent_downloads: int

    @classmethod
    def defaults(cls) -> Self:
        """Create default settings.

        Returns:
            A settings instance with safe default values.
        """
        return cls(
            output_folder=str(Path.home() / "Downloads" / "YouTubeDownloaderPro"),
            selected_format="mp4",
            selected_quality="best",
            selected_audio_quality="best",
            theme="dark",
            background_image_path="",
            background_opacity=0.28,
            compact_mode=False,
            prevent_queue_duplicates=True,
            warn_already_downloaded=True,
            allow_redownload_completed=False,
            download_rate_limit=0, retries=3, fragment_retries=3, socket_timeout=30, sleep_interval=0,
            prefer_ipv4=False, prefer_ipv6=False, continue_downloads=True, no_overwrites=False,
            use_browser_cookies=False, browser_cookies_source="none", proxy_enabled=False, proxy_url="", diagnostic_mode=False,
            download_thumbnail=False,
            write_metadata=False,
            write_subtitles=False,
            write_auto_subtitles=False,
            subtitle_languages="es,en",
            filename_template="%(title)s.%(ext)s",
            create_channel_folder=False,
            create_playlist_folder=False,
            max_playlist_items=200,
            playlist_start_index=1,
            playlist_end_index=0,
            window_width=1400,
            window_height=900,
            window_x=100,
            window_y=100,
            max_concurrent_downloads=3,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create settings from dictionary data.

        Args:
            data: Raw settings dictionary loaded from JSON.

        Returns:
            A validated settings instance.
        """
        defaults: Settings = cls.defaults()
        playlist_start_index: int = _read_int(
            data,
            "playlist_start_index",
            defaults.playlist_start_index,
            1,
            100000,
        )
        return cls(
            output_folder=_read_string(data, "output_folder", defaults.output_folder),
            selected_format=_read_choice(
                data,
                "selected_format",
                defaults.selected_format,
                ("mp4", "mp3", "m4a", "opus", "flac", "wav", "best_audio"),
            ),
            selected_quality=_read_choice(
                data,
                "selected_quality",
                defaults.selected_quality,
                ("480", "720", "1080", "1440", "2160", "best"),
            ),
            selected_audio_quality=_read_choice(
                data,
                "selected_audio_quality",
                defaults.selected_audio_quality,
                ("best", "128", "192", "256", "320"),
            ),
            theme="dark",
            background_image_path=_read_background_image_path(data, defaults.background_image_path),
            background_opacity=_read_float(data, "background_opacity", defaults.background_opacity, 0.10, 0.55),
            compact_mode=_read_bool(data, "compact_mode", defaults.compact_mode),
            prevent_queue_duplicates=_read_bool(data, "prevent_queue_duplicates", defaults.prevent_queue_duplicates),
            warn_already_downloaded=_read_bool(data, "warn_already_downloaded", defaults.warn_already_downloaded),
            allow_redownload_completed=_read_bool(data, "allow_redownload_completed", defaults.allow_redownload_completed),
            download_rate_limit=_read_int(data, "download_rate_limit", 0, 0, 1000000000),
            retries=_read_int(data, "retries", 3, 0, 100), fragment_retries=_read_int(data, "fragment_retries", 3, 0, 100),
            socket_timeout=_read_int(data, "socket_timeout", 30, 0, 600), sleep_interval=_read_int(data, "sleep_interval", 0, 0, 600),
            prefer_ipv4=_read_bool(data, "prefer_ipv4", False), prefer_ipv6=_read_bool(data, "prefer_ipv6", False), continue_downloads=_read_bool(data, "continue_downloads", True), no_overwrites=_read_bool(data, "no_overwrites", False),
            use_browser_cookies=_read_bool(data, "use_browser_cookies", False), browser_cookies_source=_read_choice(data, "browser_cookies_source", "none", ("none", "chrome", "edge", "firefox", "brave")),
            proxy_enabled=_read_bool(data, "proxy_enabled", False), proxy_url=_read_string(data, "proxy_url", ""), diagnostic_mode=_read_bool(data, "diagnostic_mode", False),
            download_thumbnail=_read_bool(data, "download_thumbnail", defaults.download_thumbnail),
            write_metadata=_read_bool(data, "write_metadata", defaults.write_metadata),
            write_subtitles=_read_bool(data, "write_subtitles", defaults.write_subtitles),
            write_auto_subtitles=_read_bool(data, "write_auto_subtitles", defaults.write_auto_subtitles),
            subtitle_languages=_normalize_subtitle_languages(
                _read_string(data, "subtitle_languages", defaults.subtitle_languages)
            ),
            filename_template=_normalize_filename_template(
                _read_string(data, "filename_template", defaults.filename_template)
            ),
            create_channel_folder=_read_bool(
                data,
                "create_channel_folder",
                defaults.create_channel_folder,
            ),
            create_playlist_folder=_read_bool(
                data,
                "create_playlist_folder",
                defaults.create_playlist_folder,
            ),
            max_playlist_items=_read_playlist_limit(data, defaults.max_playlist_items),
            playlist_start_index=playlist_start_index,
            playlist_end_index=_read_playlist_end_index(
                data,
                defaults.playlist_end_index,
                playlist_start_index,
            ),
            window_width=_read_int(data, "window_width", defaults.window_width, 1100, 10000),
            window_height=_read_int(data, "window_height", defaults.window_height, 700, 10000),
            window_x=_read_int(data, "window_x", defaults.window_x, -10000, 10000),
            window_y=_read_int(data, "window_y", defaults.window_y, -10000, 10000),
            max_concurrent_downloads=_read_int(
                data,
                "max_concurrent_downloads",
                defaults.max_concurrent_downloads,
                1,
                3,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert settings to JSON-serializable data.

        Returns:
            Dictionary representation of the settings.
        """
        return asdict(self)

    def with_window_geometry(self, width: int, height: int, x_position: int, y_position: int) -> Self:
        """Create settings with updated window geometry.

        Args:
            width: Window width in pixels.
            height: Window height in pixels.
            x_position: Window horizontal screen position.
            y_position: Window vertical screen position.

        Returns:
            Updated settings instance.
        """
        return replace(
            self,
            window_width=max(1100, width),
            window_height=max(700, height),
            window_x=x_position,
            window_y=y_position,
        )

    def with_preferences(
        self,
        output_folder: str,
        selected_format: str,
        selected_quality: str,
        selected_audio_quality: str,
        background_image_path: str,
        background_opacity: float,
        compact_mode: bool,
        prevent_queue_duplicates: bool,
        warn_already_downloaded: bool,
        allow_redownload_completed: bool,
        download_thumbnail: bool,
        write_metadata: bool,
        write_subtitles: bool,
        write_auto_subtitles: bool,
        subtitle_languages: str,
        filename_template: str,
        create_channel_folder: bool,
        create_playlist_folder: bool,
        max_playlist_items: int,
        playlist_start_index: int,
        playlist_end_index: int,
        max_concurrent_downloads: int,
    ) -> Self:
        """Create settings with updated user preferences.

        Args:
            output_folder: Preferred output folder.
            selected_format: Preferred media format.
            selected_quality: Preferred media quality.
            background_image_path: Optional custom application background image path.
            max_playlist_items: Maximum playlist or YouTube Mix videos processed per request.
            playlist_start_index: Default one-based playlist start index.
            playlist_end_index: Optional playlist end index, or 0 for automatic limit.
            max_concurrent_downloads: Maximum simultaneous downloads.

        Returns:
            Updated settings instance.
        """
        normalized_output_folder: str = str(Path(output_folder.strip()).expanduser())
        normalized_background_image_path: str = _normalize_background_image_path(background_image_path)
        return replace(
            self,
            output_folder=normalized_output_folder,
            selected_format=_normalize_choice(
                selected_format,
                self.selected_format,
                ("mp4", "mp3", "m4a", "opus", "flac", "wav", "best_audio"),
            ),
            selected_quality=_normalize_choice(
                selected_quality,
                self.selected_quality,
                ("480", "720", "1080", "1440", "2160", "best"),
            ),
            selected_audio_quality=_normalize_choice(
                selected_audio_quality,
                self.selected_audio_quality,
                ("best", "128", "192", "256", "320"),
            ),
            theme="dark",
            background_image_path=normalized_background_image_path,
            background_opacity=max(0.10, min(0.55, background_opacity)),
            compact_mode=compact_mode,
            prevent_queue_duplicates=prevent_queue_duplicates,
            warn_already_downloaded=warn_already_downloaded,
            allow_redownload_completed=allow_redownload_completed,
            download_thumbnail=download_thumbnail,
            write_metadata=write_metadata,
            write_subtitles=write_subtitles,
            write_auto_subtitles=write_auto_subtitles,
            subtitle_languages=_normalize_subtitle_languages(subtitle_languages),
            filename_template=_normalize_filename_template(filename_template),
            create_channel_folder=create_channel_folder,
            create_playlist_folder=create_playlist_folder,
            max_playlist_items=_normalize_playlist_limit(max_playlist_items),
            playlist_start_index=max(1, playlist_start_index),
            playlist_end_index=_normalize_playlist_end_index(playlist_end_index, playlist_start_index),
            max_concurrent_downloads=max(1, min(3, max_concurrent_downloads)),
        )


def _read_string(data: dict[str, Any], key: str, default: str) -> str:
    """Read a non-empty string from dictionary data."""
    value: Any = data.get(key)
    if isinstance(value, str) and value.strip():
        return value
    return default


def _read_choice(
    data: dict[str, Any],
    key: str,
    default: str,
    allowed_values: tuple[str, ...],
) -> str:
    """Read a string constrained to allowed values."""
    value: str = _read_string(data, key, default)
    if value in allowed_values:
        return value
    return default


def _normalize_choice(value: str, default: str, allowed_values: tuple[str, ...]) -> str:
    """Normalize a direct preference value to an allowed string."""
    if value in allowed_values:
        return value
    return default


def _read_bool(data: dict[str, Any], key: str, default: bool) -> bool:
    """Read a boolean setting."""
    value: Any = data.get(key)
    if isinstance(value, bool):
        return value
    return default


def _read_float(data: dict[str, Any], key: str, default: float, minimum: float, maximum: float) -> float:
    """Read a numeric setting constrained to a closed range."""
    value: Any = data.get(key)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return max(minimum, min(maximum, float(value)))
    return default


def _normalize_subtitle_languages(value: str) -> str:
    """Normalize a comma-separated yt-dlp subtitle language selector."""
    languages: list[str] = [language.strip() for language in value.split(",") if language.strip()]
    return ",".join(languages) or "es,en"


def _normalize_filename_template(value: str) -> str:
    """Return a non-empty yt-dlp filename template with an extension token."""
    normalized_value: str = value.strip()
    if (
        not normalized_value
        or "/" in normalized_value
        or "\\" in normalized_value
        or ".." in normalized_value
    ):
        return "%(title)s.%(ext)s"
    if "%(ext)s" not in normalized_value:
        return f"{normalized_value}.%(ext)s"
    return normalized_value


def _read_background_image_path(data: dict[str, Any], default: str) -> str:
    """Read a valid optional background image path."""
    value: str = _read_string(data, "background_image_path", default)
    return _normalize_background_image_path(value)


def _normalize_background_image_path(value: str) -> str:
    """Normalize a background image path when it uses a supported image format."""
    normalized_value: str = value.strip()
    if not normalized_value:
        return ""

    path: Path = Path(normalized_value).expanduser()
    if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        return ""
    return str(path)


def _read_playlist_limit(data: dict[str, Any], default: int) -> int:
    """Read a safe playlist item limit."""
    value: Any = data.get("max_playlist_items")
    if isinstance(value, int):
        return _normalize_playlist_limit(value)
    return default


def _normalize_playlist_limit(value: int) -> int:
    """Normalize playlist limits to supported values."""
    if value in {50, 100, 200, 500}:
        return value
    return 200


def _read_playlist_end_index(data: dict[str, Any], default: int, start_index: int) -> int:
    """Read an optional playlist end index."""
    value: Any = data.get("playlist_end_index")
    if isinstance(value, int):
        return _normalize_playlist_end_index(value, start_index)
    return default


def _normalize_playlist_end_index(value: int, start_index: int) -> int:
    """Normalize an optional playlist end index."""
    if value == 0:
        return 0
    if value >= start_index:
        return min(value, 100000)
    return 0


def _read_int(
    data: dict[str, Any],
    key: str,
    default: int,
    minimum: int,
    maximum: int,
) -> int:
    """Read an integer constrained to a closed range."""
    value: Any = data.get(key)
    if isinstance(value, int) and minimum <= value <= maximum:
        return value
    return default
