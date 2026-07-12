"""Tests for incremental playlist range fallback behavior."""

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from core.dependency_checker import DependencyCheckResult, DependencyStatus
from core.exceptions import MetadataExtractionError
from models.playlist_range import PlaylistRange
from services.playlist_stream_service import PlaylistStreamResult, PlaylistStreamService


class PlaylistStreamServiceTestCase(unittest.TestCase):
    """Validate safe ranged playlist extraction behavior."""

    def test_empty_ranged_result_uses_incremental_fallback(self) -> None:
        """A range rejected by a Mix triggers one safe fallback scan."""
        dependency_checker: Mock = Mock()
        dependency_checker.check.return_value = DependencyCheckResult(
            yt_dlp=DependencyStatus("yt-dlp", "yt-dlp", True),
            ffmpeg=DependencyStatus("ffmpeg", "ffmpeg", True),
        )
        service: PlaylistStreamService = PlaylistStreamService(dependency_checker=dependency_checker)
        expected_result: PlaylistStreamResult = PlaylistStreamResult(200, False, False)
        fallback_events: list[bool] = []

        with patch.object(
            service,
            "_stream_playlist_once",
            side_effect=(MetadataExtractionError("empty range"), expected_result),
        ) as stream_once:
            result: PlaylistStreamResult = service.stream_playlist(
                source_url="https://www.youtube.com/watch?v=example&list=RDexample",
                playlist_range=PlaylistRange(201, 400),
                batch_size=25,
                batch_loaded=lambda _videos, _processed, _total: None,
                total_detected=lambda _total: None,
                limit_reached=lambda _total, _limit: None,
                fallback_used=lambda: fallback_events.append(True),
            )

        self.assertEqual(result, expected_result)
        self.assertEqual(stream_once.call_count, 2)
        self.assertEqual(fallback_events, [True])


if __name__ == "__main__":
    unittest.main()
