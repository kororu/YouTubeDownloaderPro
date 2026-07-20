"""Persistent download history domain model."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from models.download_item import DownloadItem


@dataclass(frozen=True, slots=True)
class DownloadHistoryItem:
    """Immutable record of a completed or failed download."""

    history_id: str
    video_id: str | None
    title: str
    url: str
    normalized_url: str
    source_url: str
    playlist_title: str | None
    playlist_index: int | None
    output_path: str | None
    output_folder: str
    output_format: str
    audio_format: str | None
    quality: str
    status: str
    file_size: int | None
    downloaded_at: str
    duration: int | None
    channel: str | None
    extractor: str | None
    error_message: str | None

    @classmethod
    def from_download_item(cls, item: DownloadItem, output_folder: str, output_path: str | None = None) -> "DownloadHistoryItem":
        """Create a history record from a queue item."""
        metadata = item.metadata
        return cls(
            history_id=item.item_id,
            video_id=item.video_id,
            title=metadata.title if metadata else item.source_url,
            url=item.source_url,
            normalized_url=item.duplicate_key(),
            source_url=item.source_url,
            playlist_title=item.playlist_title,
            playlist_index=item.playlist_index,
            output_path=output_path,
            output_folder=output_folder,
            output_format="audio" if item.media_format.is_audio else "video",
            audio_format=item.media_format.value if item.media_format.is_audio else None,
            quality=item.audio_quality.value if item.media_format.value == "mp3" else item.quality.value,
            status=item.status.value,
            file_size=None,
            downloaded_at=datetime.now(timezone.utc).isoformat(),
            duration=metadata.duration_seconds if metadata else None,
            channel=metadata.uploader if metadata else None,
            extractor=None,
            error_message=item.error_message,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize this history record."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DownloadHistoryItem":
        """Deserialize a validated history record."""
        required = ("history_id", "title", "url", "normalized_url", "source_url", "output_folder", "output_format", "quality", "status", "downloaded_at")
        if not all(isinstance(data.get(key), str) and data[key] for key in required):
            raise ValueError("Invalid history record")
        return cls(**{field: data.get(field) for field in cls.__dataclass_fields__})
