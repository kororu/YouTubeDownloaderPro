"""Download domain enumerations."""

from __future__ import annotations

from enum import StrEnum


class DownloadFormat(StrEnum):
    """Supported output media formats."""

    MP4 = "mp4"
    MP3 = "mp3"
    M4A = "m4a"
    OPUS = "opus"
    FLAC = "flac"
    WAV = "wav"
    BEST_AUDIO = "best_audio"

    @property
    def is_audio(self) -> bool:
        """Return whether the format contains audio only."""
        return self is not DownloadFormat.MP4

    @property
    def requires_ffmpeg(self) -> bool:
        """Return whether the requested output requires FFmpeg conversion."""
        return self in {
            DownloadFormat.MP3,
            DownloadFormat.M4A,
            DownloadFormat.OPUS,
            DownloadFormat.FLAC,
            DownloadFormat.WAV,
        }


class DownloadQuality(StrEnum):
    """Supported video quality selections."""

    BEST = "best"
    P480 = "480"
    P720 = "720"
    P1080 = "1080"
    P1440 = "1440"
    P2160 = "2160"


class AudioQuality(StrEnum):
    """Supported audio quality selections."""

    BEST = "best"
    K128 = "128"
    K192 = "192"
    K256 = "256"
    K320 = "320"


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
