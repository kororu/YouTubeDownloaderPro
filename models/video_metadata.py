"""Video metadata domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True, slots=True)
class VideoMetadata:
    """Metadata extracted from yt-dlp.

    Attributes:
        source_url: Original video URL.
        title: Video title.
        duration_seconds: Duration in seconds when available.
        uploader: Uploader name when available.
        thumbnail_url: Thumbnail URL when available.
        webpage_url: Canonical webpage URL when available.
    """

    source_url: str
    title: str
    duration_seconds: int | None
    uploader: str | None
    thumbnail_url: str | None
    webpage_url: str | None

    @classmethod
    def from_yt_dlp_json(cls, source_url: str, data: dict[str, Any]) -> Self:
        """Create metadata from yt-dlp JSON output.

        Args:
            source_url: Original URL requested by the user.
            data: Parsed yt-dlp JSON object.

        Returns:
            Typed video metadata.
        """
        title: str = _read_non_empty_string(data, "title", source_url)
        duration_seconds: int | None = _read_optional_int(data, "duration")
        uploader: str | None = _read_optional_string(data, "uploader")
        thumbnail_url: str | None = _read_optional_string(data, "thumbnail")
        webpage_url: str | None = _read_optional_string(data, "webpage_url")
        return cls(
            source_url=source_url,
            title=title,
            duration_seconds=duration_seconds,
            uploader=uploader,
            thumbnail_url=thumbnail_url,
            webpage_url=webpage_url,
        )


def _read_non_empty_string(data: dict[str, Any], key: str, default: str) -> str:
    """Read a non-empty string from JSON data."""
    value: Any = data.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return default


def _read_optional_string(data: dict[str, Any], key: str) -> str | None:
    """Read an optional string from JSON data."""
    value: Any = data.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _read_optional_int(data: dict[str, Any], key: str) -> int | None:
    """Read an optional integer from JSON data."""
    value: Any = data.get(key)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return None
