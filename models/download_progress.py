"""Download progress domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DownloadProgress:
    """Progress emitted by yt-dlp.

    Attributes:
        percentage: Completion percentage from 0 to 100.
        speed: Human-readable speed when available.
        eta: Human-readable estimated time remaining when available.
        raw_line: Original yt-dlp output line.
    """

    percentage: float
    speed: str | None
    eta: str | None
    raw_line: str
