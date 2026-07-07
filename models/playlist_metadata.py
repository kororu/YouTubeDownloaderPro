"""Playlist metadata domain models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from models.video_metadata import VideoMetadata


@dataclass(frozen=True, slots=True)
class PlaylistVideo:
    """A selectable video inside a playlist.

    Attributes:
        index: One-based position inside the playlist.
        source_url: Video URL.
        title: Video title.
        duration_seconds: Duration in seconds when available.
        uploader: Uploader name when available.
        thumbnail_url: Thumbnail URL when available.
    """

    index: int
    source_url: str
    title: str
    duration_seconds: int | None
    uploader: str | None
    thumbnail_url: str | None

    @classmethod
    def from_entry(cls, index: int, entry: dict[str, Any]) -> Self | None:
        """Create a playlist video from a yt-dlp entry.

        Args:
            index: One-based playlist position.
            entry: Raw yt-dlp entry.

        Returns:
            Playlist video when the entry contains a usable URL; otherwise None.
        """
        source_url: str | None = _read_entry_url(entry)
        if source_url is None:
            return None

        title: str = _read_non_empty_string(entry, "title", source_url)
        return cls(
            index=index,
            source_url=source_url,
            title=title,
            duration_seconds=_read_optional_int(entry, "duration"),
            uploader=_read_optional_string(entry, "uploader"),
            thumbnail_url=_read_optional_string(entry, "thumbnail"),
        )

    def to_video_metadata(self) -> VideoMetadata:
        """Convert playlist video data to video metadata.

        Returns:
            Video metadata for queue display.
        """
        return VideoMetadata(
            source_url=self.source_url,
            title=self.title,
            duration_seconds=self.duration_seconds,
            uploader=self.uploader,
            thumbnail_url=self.thumbnail_url,
            webpage_url=self.source_url,
        )


@dataclass(frozen=True, slots=True)
class PlaylistMetadata:
    """Metadata extracted from a playlist.

    Attributes:
        source_url: Original playlist URL.
        title: Playlist title.
        uploader: Playlist uploader when available.
        videos: Selectable playlist videos.
    """

    source_url: str
    title: str
    uploader: str | None
    videos: tuple[PlaylistVideo, ...]

    @classmethod
    def from_yt_dlp_json(cls, source_url: str, data: dict[str, Any]) -> Self:
        """Create playlist metadata from yt-dlp JSON output.

        Args:
            source_url: Original playlist URL.
            data: Parsed yt-dlp JSON object.

        Returns:
            Typed playlist metadata.
        """
        title: str = _read_non_empty_string(data, "title", source_url)
        uploader: str | None = _read_optional_string(data, "uploader")
        entries: Any = data.get("entries")
        videos: list[PlaylistVideo] = []
        if isinstance(entries, list):
            for index, entry in enumerate(entries, start=1):
                if isinstance(entry, dict):
                    video: PlaylistVideo | None = PlaylistVideo.from_entry(index, entry)
                    if video is not None:
                        videos.append(video)

        return cls(
            source_url=source_url,
            title=title,
            uploader=uploader,
            videos=tuple(videos),
        )


def _read_entry_url(entry: dict[str, Any]) -> str | None:
    """Read the best available video URL from a playlist entry."""
    for key in ("webpage_url", "url"):
        value: Any = entry.get(key)
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return value.strip()
        if isinstance(value, str) and value.startswith("/watch?"):
            return f"https://www.youtube.com{value.strip()}"

    video_id: Any = entry.get("id")
    if isinstance(video_id, str) and video_id.strip():
        return f"https://www.youtube.com/watch?v={video_id.strip()}"
    return None


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
