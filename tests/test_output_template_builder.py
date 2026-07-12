"""Tests for download output template construction."""

from __future__ import annotations

import unittest
from pathlib import Path

from models.download_enums import DownloadFormat, DownloadQuality, DownloadStatus
from models.download_item import DownloadItem
from services.output_template_builder import OutputTemplateBuilder


class OutputTemplateBuilderTestCase(unittest.TestCase):
    """Validate output organization and safe playlist folder names."""

    def test_channel_and_playlist_folders_are_composed(self) -> None:
        """Known playlist metadata and channel placeholders organize output."""
        item: DownloadItem = DownloadItem(
            item_id="item",
            source_url="https://example.com/video",
            media_format=DownloadFormat.MP4,
            quality=DownloadQuality.BEST,
            status=DownloadStatus.READY,
            playlist_title='Playlist: Test/One',
            filename_template="%(playlist_index)s - %(title)s.%(ext)s",
            create_channel_folder=True,
            create_playlist_folder=True,
        )

        output_template: str = OutputTemplateBuilder().build(Path("downloads"), item)

        self.assertIn("%(channel,uploader)s", output_template)
        self.assertIn("Playlist_ Test_One", output_template)
        self.assertTrue(output_template.endswith("%(playlist_index)s - %(title)s.%(ext)s"))

    def test_missing_playlist_title_uses_base_folder(self) -> None:
        """Playlist folder output safely falls back when metadata is absent."""
        item: DownloadItem = DownloadItem(
            item_id="item",
            source_url="https://example.com/video",
            media_format=DownloadFormat.MP3,
            quality=DownloadQuality.BEST,
            status=DownloadStatus.READY,
            create_playlist_folder=True,
        )

        self.assertEqual(
            OutputTemplateBuilder().build(Path("downloads"), item),
            str(Path("downloads") / "%(title)s.%(ext)s"),
        )


if __name__ == "__main__":
    unittest.main()
