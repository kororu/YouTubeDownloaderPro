"""Download queue item domain model."""

from __future__ import annotations

from dataclasses import dataclass
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
    """

    item_id: str
    source_url: str
    media_format: DownloadFormat
    quality: DownloadQuality
    status: DownloadStatus
    metadata: VideoMetadata | None = None
    error_message: str | None = None

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
        )
