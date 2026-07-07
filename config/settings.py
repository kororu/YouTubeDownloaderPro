"""Persistent application settings model."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Self


@dataclass(frozen=True, slots=True)
class Settings:
    """User-configurable application settings.

    Attributes:
        output_folder: Default folder used for downloaded files.
        selected_format: Preferred media format.
        selected_quality: Preferred video quality.
        theme: Active visual theme name.
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
            theme=_read_choice(data, "theme", defaults.theme, ("dark", "light")),
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
