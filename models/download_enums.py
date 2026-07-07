"""Download domain enumerations."""

from __future__ import annotations

from enum import StrEnum


class DownloadFormat(StrEnum):
    """Supported output media formats."""

    MP4 = "mp4"
    MP3 = "mp3"


class DownloadQuality(StrEnum):
    """Supported video quality selections."""

    BEST = "best"
    P480 = "480"
    P720 = "720"
    P1080 = "1080"
    P1440 = "1440"
    P2160 = "2160"


class DownloadStatus(StrEnum):
    """Download item lifecycle status."""

    PENDING = "pending"
    LOADING_METADATA = "loading_metadata"
    READY = "ready"
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
