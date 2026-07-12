"""Tests for download item queue behavior."""

from __future__ import annotations

import unittest

from models.download_enums import DownloadFormat, DownloadQuality, DownloadStatus
from models.download_item import DownloadItem


class DownloadItemTestCase(unittest.TestCase):
    """Validate download item helpers."""

    def test_duplicate_key_prefers_video_id(self) -> None:
        """Known video identifiers drive deduplication."""
        item: DownloadItem = DownloadItem(
            item_id="item",
            source_url="https://www.youtube.com/watch?v=abc123&list=PL123",
            media_format=DownloadFormat.MP4,
            quality=DownloadQuality.BEST,
            status=DownloadStatus.READY,
            video_id="abc123",
        )

        self.assertEqual(item.duplicate_key(), "video:abc123")

    def test_duplicate_key_reads_youtube_video_id_from_url(self) -> None:
        """YouTube URLs deduplicate by video id when possible."""
        item: DownloadItem = DownloadItem(
            item_id="item",
            source_url="https://www.youtube.com/watch?v=abc123&list=PL123",
            media_format=DownloadFormat.MP4,
            quality=DownloadQuality.BEST,
            status=DownloadStatus.READY,
        )

        self.assertEqual(item.duplicate_key(), "video:abc123")


if __name__ == "__main__":
    unittest.main()
