"""Download queue item domain model."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

from models.download_enums import DownloadFormat, DownloadQuality, DownloadStatus
from models.video_metadata import VideoMetadata


@dataclass(frozen=True, slots=True)
class DownloadItem:
    """Domain model for a queue item.

    Attributes:
        item_id: Stable queue item identifier.
        source_url: Source media URL.
        media_format: Selected output format.
        quality: Selected output quality.
        status: Current item status.
        metadata: Extracted video metadata when available.
        error_message: Error message when the item failed.
        progress_percentage: Download progress percentage.
        playlist_index: One-based playlist index when the item comes from a playlist.
        playlist_title: Playlist title when known.
        playlist_source_url: Playlist or YouTube Mix source URL when known.
        is_youtube_mix: Whether the item comes from a YouTube Mix.
        video_id: Stable video identifier when known.
    """

    item_id: str
    source_url: str
    media_format: DownloadFormat
    quality: DownloadQuality
    status: DownloadStatus
    metadata: VideoMetadata | None = None
    error_message: str | None = None
    progress_percentage: float = 0.0
    playlist_index: int | None = None
    playlist_title: str | None = None
    playlist_source_url: str | None = None
    is_youtube_mix: bool = False
    video_id: str | None = None

    @classmethod
    def create(
        cls,
        source_url: str,
        media_format: DownloadFormat,
        quality: DownloadQuality,
    ) -> "DownloadItem":
        """Create a new queue item.

        Args:
            source_url: Source media URL.
            media_format: Selected output format.
            quality: Selected output quality.

        Returns:
            Queue item in metadata loading state.
        """
        return cls(
            item_id=str(uuid4()),
            source_url=source_url,
            media_format=media_format,
            quality=quality,
            status=DownloadStatus.LOADING_METADATA,
        )

    def with_metadata(self, metadata: VideoMetadata) -> "DownloadItem":
        """Create a ready item with extracted metadata."""
        return replace(self, status=DownloadStatus.READY, metadata=metadata, error_message=None)

    def with_failure(self, error_message: str) -> "DownloadItem":
        """Create a failed item with an error message."""
        return replace(self, status=DownloadStatus.FAILED, error_message=error_message)

    def with_status(self, status: DownloadStatus) -> "DownloadItem":
        """Create an item with updated status."""
        progress_percentage: float = self.progress_percentage
        if status is DownloadStatus.COMPLETED:
            progress_percentage = 100.0
        return DownloadItem(
            item_id=self.item_id,
            source_url=self.source_url,
            media_format=self.media_format,
            quality=self.quality,
            status=status,
            metadata=self.metadata,
            error_message=self.error_message,
            progress_percentage=progress_percentage,
            playlist_index=self.playlist_index,
            playlist_title=self.playlist_title,
            playlist_source_url=self.playlist_source_url,
            is_youtube_mix=self.is_youtube_mix,
            video_id=self.video_id,
        )

    def with_progress(self, progress_percentage: float) -> "DownloadItem":
        """Create an item with updated progress."""
        return replace(
            self,
            status=DownloadStatus.DOWNLOADING,
            progress_percentage=max(0.0, min(100.0, progress_percentage)),
        )

    def duplicate_key(self) -> str:
        """Return a stable key used to avoid duplicate queue entries."""
        if self.video_id:
            return f"video:{self.video_id}"
        video_id: str | None = _read_video_id_from_url(self.source_url)
        if video_id is not None:
            return f"video:{video_id}"
        return f"url:{self.source_url.strip().lower()}"

    def to_dict(self) -> dict[str, Any]:
        """Convert the item to JSON-serializable data.

        Returns:
            Dictionary representation of the download item.
        """
        metadata_data: dict[str, Any] | None = None
        if self.metadata is not None:
            metadata_data = {
                "source_url": self.metadata.source_url,
                "title": self.metadata.title,
                "duration_seconds": self.metadata.duration_seconds,
                "uploader": self.metadata.uploader,
                "thumbnail_url": self.metadata.thumbnail_url,
                "webpage_url": self.metadata.webpage_url,
            }

        return {
            "item_id": self.item_id,
            "source_url": self.source_url,
            "media_format": self.media_format.value,
            "quality": self.quality.value,
            "status": self.status.value,
            "metadata": metadata_data,
            "error_message": self.error_message,
            "progress_percentage": self.progress_percentage,
            "playlist_index": self.playlist_index,
            "playlist_title": self.playlist_title,
            "playlist_source_url": self.playlist_source_url,
            "is_youtube_mix": self.is_youtube_mix,
            "video_id": self.video_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DownloadItem":
        """Create a download item from JSON data.

        Args:
            data: Raw dictionary data.

        Returns:
            Parsed download item.

        Raises:
            ValueError: If required values are invalid.
        """
        metadata: VideoMetadata | None = None
        raw_metadata: Any = data.get("metadata")
        if isinstance(raw_metadata, dict):
            metadata = VideoMetadata(
                source_url=_read_string(raw_metadata, "source_url", _read_string(data, "source_url", "")),
                title=_read_string(raw_metadata, "title", _read_string(data, "source_url", "")),
                duration_seconds=_read_optional_int(raw_metadata, "duration_seconds"),
                uploader=_read_optional_string(raw_metadata, "uploader"),
                thumbnail_url=_read_optional_string(raw_metadata, "thumbnail_url"),
                webpage_url=_read_optional_string(raw_metadata, "webpage_url"),
            )

        status: DownloadStatus = DownloadStatus(_read_string(data, "status", DownloadStatus.READY.value))
        if status in {DownloadStatus.QUEUED, DownloadStatus.DOWNLOADING}:
            status = DownloadStatus.READY

        return cls(
            item_id=_read_string(data, "item_id", str(uuid4())),
            source_url=_read_string(data, "source_url", ""),
            media_format=DownloadFormat(_read_string(data, "media_format", DownloadFormat.MP4.value)),
            quality=DownloadQuality(_read_string(data, "quality", DownloadQuality.BEST.value)),
            status=status,
            metadata=metadata,
            error_message=_read_optional_string(data, "error_message"),
            progress_percentage=_read_float(data, "progress_percentage", 0.0),
            playlist_index=_read_optional_int(data, "playlist_index"),
            playlist_title=_read_optional_string(data, "playlist_title"),
            playlist_source_url=_read_optional_string(data, "playlist_source_url"),
            is_youtube_mix=_read_bool(data, "is_youtube_mix", False),
            video_id=_read_optional_string(data, "video_id"),
        )


def _read_string(data: dict[str, Any], key: str, default: str) -> str:
    """Read a string from dictionary data."""
    value: Any = data.get(key)
    if isinstance(value, str):
        return value
    return default


def _read_optional_string(data: dict[str, Any], key: str) -> str | None:
    """Read an optional string from dictionary data."""
    value: Any = data.get(key)
    if isinstance(value, str) and value:
        return value
    return None


def _read_optional_int(data: dict[str, Any], key: str) -> int | None:
    """Read an optional integer from dictionary data."""
    value: Any = data.get(key)
    if isinstance(value, int):
        return value
    return None


def _read_float(data: dict[str, Any], key: str, default: float) -> float:
    """Read a float from dictionary data."""
    value: Any = data.get(key)
    if isinstance(value, int | float):
        return float(value)
    return default


def _read_bool(data: dict[str, Any], key: str, default: bool) -> bool:
    """Read a boolean from dictionary data."""
    value: Any = data.get(key)
    if isinstance(value, bool):
        return value
    return default


def _read_video_id_from_url(source_url: str) -> str | None:
    """Read a YouTube video identifier from a URL when present."""
    parsed_url = urlparse(source_url)
    host: str = parsed_url.netloc.lower()
    if "youtu.be" in host:
        video_id: str = parsed_url.path.strip("/")
        return video_id or None
    if "youtube.com" in host:
        query_values: dict[str, list[str]] = parse_qs(parsed_url.query)
        video_values: list[str] = query_values.get("v", [])
        if video_values and video_values[0].strip():
            return video_values[0].strip()
    return None
