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
        theme: Active visual theme name, forced to dark for compatibility.
        background_image_path: Optional custom application background image path.
        max_playlist_items: Maximum playlist or YouTube Mix videos processed per request.
        window_width: Main window width in pixels.
        window_height: Main window height in pixels.
        window_x: Main window horizontal screen position.
        window_y: Main window vertical screen position.
        max_concurrent_downloads: Maximum simultaneous downloads.
    """

    output_folder: str
    selected_format: str
    selected_quality: str
    theme: str
    background_image_path: str
    max_playlist_items: int
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
            theme="dark",
            background_image_path="",
            max_playlist_items=200,
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
        return cls(
            output_folder=_read_string(data, "output_folder", defaults.output_folder),
            selected_format=_read_choice(
                data,
                "selected_format",
                defaults.selected_format,
                ("mp4", "mp3"),
            ),
            selected_quality=_read_choice(
                data,
                "selected_quality",
                defaults.selected_quality,
                ("480", "720", "1080", "1440", "2160", "best"),
            ),
            theme="dark",
            background_image_path=_read_background_image_path(data, defaults.background_image_path),
            max_playlist_items=_read_playlist_limit(data, defaults.max_playlist_items),
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
        background_image_path: str,
        max_playlist_items: int,
        max_concurrent_downloads: int,
    ) -> Self:
        """Create settings with updated user preferences.

        Args:
            output_folder: Preferred output folder.
            selected_format: Preferred media format.
            selected_quality: Preferred media quality.
            background_image_path: Optional custom application background image path.
            max_playlist_items: Maximum playlist or YouTube Mix videos processed per request.
            max_concurrent_downloads: Maximum simultaneous downloads.

        Returns:
            Updated settings instance.
        """
        normalized_output_folder: str = str(Path(output_folder.strip()).expanduser())
        normalized_background_image_path: str = _normalize_background_image_path(background_image_path)
        return replace(
            self,
            output_folder=normalized_output_folder,
            selected_format=selected_format,
            selected_quality=selected_quality,
            theme="dark",
            background_image_path=normalized_background_image_path,
            max_playlist_items=_normalize_playlist_limit(max_playlist_items),
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
    if value in {0, 50, 100, 200, 500}:
        return value
    return 200


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
