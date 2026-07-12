"""Tests for playlist range values."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from models.playlist_range import PlaylistRange
from services.playlist_range_history_service import PlaylistRangeHistoryService


class PlaylistRangeTestCase(unittest.TestCase):
    """Validate playlist range behavior."""

    def test_from_start_and_limit_builds_inclusive_range(self) -> None:
        """Start and limit produce an inclusive end index."""
        playlist_range: PlaylistRange = PlaylistRange.from_start_and_limit(201, 200)

        self.assertEqual(playlist_range.start_index, 201)
        self.assertEqual(playlist_range.end_index, 400)
        self.assertEqual(playlist_range.item_count, 200)

    def test_next_range_continues_after_end(self) -> None:
        """Next range begins after the current end index."""
        playlist_range: PlaylistRange = PlaylistRange(1, 200).next_range(200)

        self.assertEqual(playlist_range, PlaylistRange(201, 400))

    def test_invalid_empty_range_raises(self) -> None:
        """An end index before start is invalid."""
        with self.assertRaises(ValueError):
            PlaylistRange(400, 201)

    def test_history_continues_after_last_completed_index(self) -> None:
        """Persisted history advances to the next adjacent block per URL."""
        with TemporaryDirectory() as temporary_directory:
            service: PlaylistRangeHistoryService = PlaylistRangeHistoryService(
                Path(temporary_directory) / "playlist_ranges.json"
            )
            source_url: str = "https://www.youtube.com/playlist?list=example"

            self.assertEqual(service.next_range(source_url, 200), PlaylistRange(1, 200))
            service.save_completed_range(source_url, PlaylistRange(1, 200))
            self.assertEqual(service.next_range(source_url, 200), PlaylistRange(201, 400))


if __name__ == "__main__":
    unittest.main()
