"""Tests for download item queue behavior."""

from __future__ import annotations

import unittest

from models.download_enums import AudioQuality, DownloadFormat, DownloadQuality, DownloadStatus
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

    def test_duplicate_key_normalizes_generic_url(self) -> None:
        """Generic URLs ignore host case, query order, trailing slash, and fragments."""
        first_item: DownloadItem = DownloadItem(
            item_id="first",
            source_url="HTTPS://Example.com/video/?b=2&a=1#section",
            media_format=DownloadFormat.MP4,
            quality=DownloadQuality.BEST,
            status=DownloadStatus.READY,
        )
        second_item: DownloadItem = DownloadItem(
            item_id="second",
            source_url="https://example.com/video?a=1&b=2",
            media_format=DownloadFormat.MP4,
            quality=DownloadQuality.BEST,
            status=DownloadStatus.READY,
        )

        self.assertEqual(first_item.duplicate_key(), second_item.duplicate_key())

    def test_advanced_audio_options_round_trip(self) -> None:
        """Queue JSON preserves v0.5.0 download options."""
        item: DownloadItem = DownloadItem(
            item_id="audio",
            source_url="https://example.com/audio",
            media_format=DownloadFormat.FLAC,
            quality=DownloadQuality.BEST,
            status=DownloadStatus.READY,
            audio_quality=AudioQuality.K320,
            download_thumbnail=True,
            write_metadata=True,
            write_subtitles=True,
            write_auto_subtitles=True,
            subtitle_languages="es,en",
            filename_template="%(channel)s - %(title)s.%(ext)s",
            create_channel_folder=True,
            create_playlist_folder=True,
        )

        restored_item: DownloadItem = DownloadItem.from_dict(item.to_dict())

        self.assertEqual(restored_item, item)
        self.assertEqual(item.to_dict()["output_format"], "audio")
        self.assertEqual(item.to_dict()["audio_format"], "flac")

    def test_legacy_queue_item_uses_advanced_defaults(self) -> None:
        """Queue entries from older versions remain loadable."""
        restored_item: DownloadItem = DownloadItem.from_dict(
            {
                "item_id": "legacy",
                "source_url": "https://example.com/video",
                "media_format": "mp3",
                "quality": "best",
                "status": "ready",
            }
        )

        self.assertEqual(restored_item.media_format, DownloadFormat.MP3)
        self.assertEqual(restored_item.audio_quality, AudioQuality.BEST)
        self.assertFalse(restored_item.download_thumbnail)


if __name__ == "__main__":
    unittest.main()
