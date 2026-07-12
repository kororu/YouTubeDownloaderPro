"""Tests for playlist range values."""

from __future__ import annotations

import unittest

from models.playlist_range import PlaylistRange


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


if __name__ == "__main__":
    unittest.main()
