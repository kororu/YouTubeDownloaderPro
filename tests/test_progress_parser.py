"""Tests for yt-dlp progress parsing."""

from __future__ import annotations

import unittest

from models.download_progress import DownloadProgress
from services.progress_parser import ProgressParser


class ProgressParserTestCase(unittest.TestCase):
    """Validate parsing of yt-dlp progress lines."""

    def setUp(self) -> None:
        """Create a parser for each test."""
        self.parser: ProgressParser = ProgressParser()

    def test_progress_line_extracts_percentage_speed_and_eta(self) -> None:
        """Download progress lines expose percentage, speed, and ETA."""
        progress: DownloadProgress | None = self.parser.parse(
            "[download]  42.5% of 10.00MiB at 1.25MiB/s ETA 00:05"
        )

        self.assertIsNotNone(progress)
        self.assertEqual(progress.percentage, 42.5)
        self.assertEqual(progress.speed, "1.25MiB/s")
        self.assertEqual(progress.eta, "00:05")

    def test_non_progress_line_returns_none(self) -> None:
        """Unrelated output lines are ignored."""
        progress: DownloadProgress | None = self.parser.parse("[info] Downloading webpage")

        self.assertIsNone(progress)


if __name__ == "__main__":
    unittest.main()
