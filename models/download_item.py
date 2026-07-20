"""Download queue item domain model."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import Any, TypeVar
from uuid import uuid4

from core.url_identity import extract_youtube_video_id, normalize_url_for_comparison
from models.download_enums import AudioQuality, DownloadFormat, DownloadQuality, DownloadStatus
from models.video_metadata import VideoMetadata

EnumValue = TypeVar("EnumValue", bound=StrEnum)


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
        audio_quality: Selected MP3 bitrate or best/original audio quality.
        download_thumbnail: Whether yt-dlp writes the source thumbnail.
        write_metadata: Whether yt-dlp writes an info JSON file.
        write_subtitles: Whether published subtitles are requested.
        write_auto_subtitles: Whether automatic subtitles are requested.
        subtitle_languages: yt-dlp subtitle language selector.
        filename_template: Safe yt-dlp filename template.
        create_channel_folder: Whether output is grouped by channel.
        create_playlist_folder: Whether playlist output uses its own folder.
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
    audio_quality: AudioQuality = AudioQuality.BEST
    download_thumbnail: bool = False
    write_metadata: bool = False
    write_subtitles: bool = False
    write_auto_subtitles: bool = False
    subtitle_languages: str = "es,en"
    filename_template: str = "%(title)s.%(ext)s"
    create_channel_folder: bool = False
    create_playlist_folder: bool = False

    @classmethod
    def create(
        cls,
        source_url: str,
        media_format: DownloadFormat,
        quality: DownloadQuality,
        audio_quality: AudioQuality = AudioQuality.BEST,
        download_thumbnail: bool = False,
        write_metadata: bool = False,
        write_subtitles: bool = False,
        write_auto_subtitles: bool = False,
        subtitle_languages: str = "es,en",
        filename_template: str = "%(title)s.%(ext)s",
        create_channel_folder: bool = False,
        create_playlist_folder: bool = False,
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
            audio_quality=audio_quality,
            download_thumbnail=download_thumbnail,
            write_metadata=write_metadata,
            write_subtitles=write_subtitles,
            write_auto_subtitles=write_auto_subtitles,
            subtitle_languages=subtitle_languages,
            filename_template=filename_template,
            create_channel_folder=create_channel_folder,
            create_playlist_folder=create_playlist_folder,
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
        return replace(self, status=status, progress_percentage=progress_percentage)

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
        video_id: str | None = extract_youtube_video_id(self.source_url)
        if video_id is not None:
            return f"video:{video_id}"
        return f"url:{normalize_url_for_comparison(self.source_url)}"

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
            "output_format": "audio" if self.media_format.is_audio else "video",
            "audio_format": self.media_format.value if self.media_format.is_audio else None,
            "quality": self.quality.value,
            "audio_quality": self.audio_quality.value,
            "status": self.status.value,
            "metadata": metadata_data,
            "error_message": self.error_message,
            "progress_percentage": self.progress_percentage,
            "playlist_index": self.playlist_index,
            "playlist_title": self.playlist_title,
            "playlist_source_url": self.playlist_source_url,
            "is_youtube_mix": self.is_youtube_mix,
            "video_id": self.video_id,
            "thumbnail_enabled": self.download_thumbnail,
            "metadata_enabled": self.write_metadata,
            "subtitles_enabled": self.write_subtitles,
            "auto_subtitles_enabled": self.write_auto_subtitles,
            "subtitle_languages": self.subtitle_languages,
            "filename_template": self.filename_template,
            "channel_folder_enabled": self.create_channel_folder,
            "playlist_folder_enabled": self.create_playlist_folder,
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

        media_format: DownloadFormat = _read_download_format(data)
        return cls(
            item_id=_read_string(data, "item_id", str(uuid4())),
            source_url=_read_string(data, "source_url", ""),
            media_format=media_format,
            quality=_read_enum(
                DownloadQuality,
                _read_string(data, "quality", DownloadQuality.BEST.value),
                DownloadQuality.BEST,
            ),
            status=status,
            metadata=metadata,
            error_message=_read_optional_string(data, "error_message"),
            progress_percentage=_read_float(data, "progress_percentage", 0.0),
            playlist_index=_read_optional_int(data, "playlist_index"),
            playlist_title=_read_optional_string(data, "playlist_title"),
            playlist_source_url=_read_optional_string(data, "playlist_source_url"),
            is_youtube_mix=_read_bool(data, "is_youtube_mix", False),
            video_id=_read_optional_string(data, "video_id"),
            audio_quality=_read_enum(
                AudioQuality,
                _read_string(data, "audio_quality", AudioQuality.BEST.value),
                AudioQuality.BEST,
            ),
            download_thumbnail=_read_bool(data, "thumbnail_enabled", False),
            write_metadata=_read_bool(data, "metadata_enabled", False),
            write_subtitles=_read_bool(data, "subtitles_enabled", False),
            write_auto_subtitles=_read_bool(data, "auto_subtitles_enabled", False),
            subtitle_languages=_read_string(data, "subtitle_languages", "es,en"),
            filename_template=_read_string(data, "filename_template", "%(title)s.%(ext)s"),
            create_channel_folder=_read_bool(data, "channel_folder_enabled", False),
            create_playlist_folder=_read_bool(data, "playlist_folder_enabled", False),
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


def _read_download_format(data: dict[str, Any]) -> DownloadFormat:
    """Read new or legacy output format fields safely."""
    media_format_value: str = _read_string(data, "media_format", "")
    if not media_format_value:
        media_format_value = _read_string(data, "audio_format", "")
    if not media_format_value and _read_string(data, "output_format", "") == "video":
        media_format_value = DownloadFormat.MP4.value
    return _read_enum(DownloadFormat, media_format_value, DownloadFormat.MP4)


def _read_enum(
    enum_type: type[EnumValue],
    value: str,
    default: EnumValue,
) -> EnumValue:
    """Read a string enum value with a backward-compatible default."""
    try:
        return enum_type(value)
    except ValueError:
        return default
