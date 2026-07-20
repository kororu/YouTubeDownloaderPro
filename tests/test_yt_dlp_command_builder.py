"""Tests for yt-dlp command generation."""

from __future__ import annotations

import unittest

from models.download_enums import AudioQuality, DownloadFormat, DownloadQuality
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

    def test_download_command_reports_final_output_path(self) -> None:
        """Downloads request the final path used for local history validation."""
        command: list[str] = self.builder.build_download_command(
            "https://example.com/video",
            "%(title)s.%(ext)s",
            DownloadFormat.MP4,
            DownloadQuality.BEST,
        )

        self.assertIn("--print", command)
        self.assertIn("after_move:__OUTPUT_PATH__%(filepath)s", command)

    def test_mp3_command_applies_selected_bitrate(self) -> None:
        """MP3 conversion passes the requested bitrate to yt-dlp."""
        command: list[str] = self.builder.build_download_command(
            "https://example.com/video",
            "%(title)s.%(ext)s",
            DownloadFormat.MP3,
            DownloadQuality.BEST,
            audio_quality=AudioQuality.K320,
        )

        self.assertIn("--audio-quality", command)
        self.assertIn("320K", command)

    def test_lossless_audio_commands_do_not_apply_bitrate(self) -> None:
        """WAV and FLAC conversion never claim bitrate quality improvements."""
        for media_format in (DownloadFormat.WAV, DownloadFormat.FLAC):
            with self.subTest(media_format=media_format):
                command: list[str] = self.builder.build_download_command(
                    "https://example.com/video",
                    "%(title)s.%(ext)s",
                    media_format,
                    DownloadQuality.BEST,
                    audio_quality=AudioQuality.K320,
                )
                self.assertIn("--audio-format", command)
                self.assertIn(media_format.value, command)
                self.assertNotIn("--audio-quality", command)

    def test_best_audio_avoids_conversion(self) -> None:
        """Original audio keeps the source container when practical."""
        command: list[str] = self.builder.build_download_command(
            "https://example.com/video",
            "%(title)s.%(ext)s",
            DownloadFormat.BEST_AUDIO,
            DownloadQuality.BEST,
        )

        self.assertIn("bestaudio/best", command)
        self.assertNotIn("-x", command)
        self.assertNotIn("--audio-format", command)

    def test_auxiliary_file_options_are_included(self) -> None:
        """Thumbnail, metadata, and subtitle settings map to yt-dlp flags."""
        command: list[str] = self.builder.build_download_command(
            "https://example.com/video",
            "%(title)s.%(ext)s",
            DownloadFormat.M4A,
            DownloadQuality.BEST,
            download_thumbnail=True,
            write_metadata=True,
            write_subtitles=True,
            write_auto_subtitles=True,
            subtitle_languages="es,en",
        )

        self.assertIn("--write-thumbnail", command)
        self.assertIn("--write-info-json", command)
        self.assertIn("--write-subs", command)
        self.assertIn("--write-auto-subs", command)
        self.assertIn("--sub-langs", command)
        self.assertIn("es,en", command)


if __name__ == "__main__":
    unittest.main()
