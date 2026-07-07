"""Download queue item domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
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
    """

    item_id: str
    source_url: str
    media_format: DownloadFormat
    quality: DownloadQuality
    status: DownloadStatus
    metadata: VideoMetadata | None = None
    error_message: str | None = None
    progress_percentage: float = 0.0

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
        return DownloadItem(
            item_id=self.item_id,
            source_url=self.source_url,
            media_format=self.media_format,
            quality=self.quality,
            status=DownloadStatus.READY,
            metadata=metadata,
        )

    def with_failure(self, error_message: str) -> "DownloadItem":
        """Create a failed item with an error message."""
        return DownloadItem(
            item_id=self.item_id,
            source_url=self.source_url,
            media_format=self.media_format,
            quality=self.quality,
            status=DownloadStatus.FAILED,
            metadata=self.metadata,
            error_message=error_message,
            progress_percentage=self.progress_percentage,
        )

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
        )

    def with_progress(self, progress_percentage: float) -> "DownloadItem":
        """Create an item with updated progress."""
        return DownloadItem(
            item_id=self.item_id,
            source_url=self.source_url,
            media_format=self.media_format,
            quality=self.quality,
            status=DownloadStatus.DOWNLOADING,
            metadata=self.metadata,
            error_message=self.error_message,
            progress_percentage=max(0.0, min(100.0, progress_percentage)),
        )

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
