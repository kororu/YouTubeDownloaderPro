"""Tests for local completed-download lookup."""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from models.download_history_item import DownloadHistoryItem
from services.download_history_service import DownloadHistoryService


class DownloadHistoryServiceTestCase(unittest.TestCase):
    """Validate completed history lookup without network access."""

    def _entry(self, output_path: str | None) -> DownloadHistoryItem:
        """Create a completed entry compatible with legacy history files."""
        return DownloadHistoryItem(
            history_id="history-item",
            video_id="video123",
            title="Stored video",
            url="https://youtu.be/video123?si=tracking",
            normalized_url="video:video123",
            source_url="https://youtu.be/video123?si=tracking",
            playlist_title=None,
            playlist_index=None,
            output_path=output_path,
            output_folder="C:/Downloads",
            output_format="video",
            audio_format=None,
            quality="best",
            status="completed",
            file_size=None,
            downloaded_at=datetime.now(timezone.utc).isoformat(),
            duration=None,
            channel=None,
            extractor=None,
            error_message=None,
        )

    def test_finds_completed_entry_by_shorts_video_id(self) -> None:
        """Shorts URLs use their ID before metadata extraction."""
        with tempfile.TemporaryDirectory() as directory:
            service = DownloadHistoryService(Path(directory) / "history.json")
            entry = self._entry(None)
            service.save((entry,))

            found = service.get_completed_entry_for_url("https://youtube.com/shorts/video123?t=5")

        self.assertEqual(found, entry)

    def test_load_recovers_video_id_from_legacy_youtube_url(self) -> None:
        """Legacy records without video_id gain an in-memory lookup identity."""
        with tempfile.TemporaryDirectory() as directory:
            service = DownloadHistoryService(Path(directory) / "history.json")
            entry = self._entry(None)
            service.save((entry,))

            loaded_entry = service.load()[0]

        self.assertEqual(loaded_entry.video_id, "video123")

    def test_existing_output_file_is_available(self) -> None:
        """A completed entry is only protected when its output still exists."""
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "Stored video.mp4"
            output_path.touch()
            service = DownloadHistoryService(Path(directory) / "history.json")
            entry = self._entry(str(output_path))

            self.assertTrue(service.is_completed_download_available(entry))

            output_path.unlink()
            self.assertFalse(service.is_completed_download_available(entry))

    def test_remove_only_deletes_the_selected_history_entry(self) -> None:
        """Removing history records leaves unrelated records available."""
        with tempfile.TemporaryDirectory() as directory:
            service = DownloadHistoryService(Path(directory) / "history.json")
            first_entry = self._entry(None)
            second_entry = DownloadHistoryItem(
                **{**first_entry.to_dict(), "history_id": "second-history-item"}
            )
            service.save((first_entry, second_entry))

            removed = service.remove(first_entry.history_id)

            self.assertTrue(removed)
            self.assertEqual(service.load(), (second_entry,))

    def test_clear_missing_completed_entries_keeps_available_files(self) -> None:
        """Cleanup removes only completed records whose output cannot be found."""
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "Stored video.mp4"
            output_path.touch()
            service = DownloadHistoryService(Path(directory) / "history.json")
            available_entry = self._entry(str(output_path))
            missing_entry = DownloadHistoryItem(
                **{**available_entry.to_dict(), "history_id": "missing-history-item", "output_path": None}
            )
            service.save((available_entry, missing_entry))

            removed_count = service.remove_completed_entries_without_available_file()

            self.assertEqual(removed_count, 1)
            self.assertEqual(service.load(), (available_entry,))


if __name__ == "__main__":
    unittest.main()
