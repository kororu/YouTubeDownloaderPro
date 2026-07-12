"""Tests for yt-dlp command generation."""

from __future__ import annotations

import unittest

from models.download_enums import DownloadFormat, DownloadQuality
from models.playlist_range import PlaylistRange
from services.yt_dlp_command_builder import YtDlpCommandBuilder


class YtDlpCommandBuilderTestCase(unittest.TestCase):
    """Validate generated yt-dlp commands."""

    def setUp(self) -> None:
        """Create a command builder for each test."""
        self.builder: YtDlpCommandBuilder = YtDlpCommandBuilder()

    def test_metadata_command_uses_no_playlist(self) -> None:
        """Single-video metadata commands disable playlist expansion."""
        command: list[str] = self.builder.build_metadata_command("https://example.com/video")

        self.assertIn("--dump-single-json", command)
        self.assertIn("--no-playlist", command)
        self.assertEqual(command[-1], "https://example.com/video")

    def test_playlist_stream_command_streams_flat_json(self) -> None:
        """Playlist streaming commands emit flat JSON entries."""
        command: list[str] = self.builder.build_playlist_stream_command("https://example.com/playlist")

        self.assertIn("--dump-json", command)
        self.assertIn("--flat-playlist", command)
        self.assertIn("--yes-playlist", command)
        self.assertEqual(command[-1], "https://example.com/playlist")

    def test_playlist_stream_command_supports_range(self) -> None:
        """Playlist streaming commands can request a specific range."""
        command: list[str] = self.builder.build_playlist_stream_command(
            "https://example.com/playlist",
            PlaylistRange(201, 400),
        )

        self.assertIn("--playlist-start", command)
        self.assertIn("201", command)
        self.assertIn("--playlist-end", command)
        self.assertIn("400", command)

    def test_mp3_download_command_extracts_audio(self) -> None:
        """MP3 commands enable audio extraction."""
        command: list[str] = self.builder.build_download_command(
            "https://example.com/video",
            "%(title)s.%(ext)s",
            DownloadFormat.MP3,
            DownloadQuality.BEST,
        )

        self.assertIn("-x", command)
        self.assertIn("--audio-format", command)
        self.assertIn("mp3", command)


if __name__ == "__main__":
    unittest.main()
