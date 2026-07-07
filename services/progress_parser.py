"""yt-dlp progress parsing."""

from __future__ import annotations

import re

from models.download_progress import DownloadProgress

PERCENT_PATTERN: re.Pattern[str] = re.compile(r"\[download\]\s+([0-9]+(?:\.[0-9]+)?)%")
SPEED_PATTERN: re.Pattern[str] = re.compile(r"\s+at\s+([^\s]+)")
ETA_PATTERN: re.Pattern[str] = re.compile(r"\s+ETA\s+([^\s]+)")


class ProgressParser:
    """Parses yt-dlp output lines into progress values."""

    def parse(self, line: str) -> DownloadProgress | None:
        """Parse a yt-dlp output line.

        Args:
            line: Raw yt-dlp output line.

        Returns:
            Download progress when the line contains progress data; otherwise None.
        """
        percent_match: re.Match[str] | None = PERCENT_PATTERN.search(line)
        if percent_match is None:
            return None

        speed_match: re.Match[str] | None = SPEED_PATTERN.search(line)
        eta_match: re.Match[str] | None = ETA_PATTERN.search(line)
        return DownloadProgress(
            percentage=float(percent_match.group(1)),
            speed=speed_match.group(1) if speed_match else None,
            eta=eta_match.group(1) if eta_match else None,
            raw_line=line.rstrip(),
        )
