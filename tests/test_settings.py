"""Tests for persistent settings validation."""

from __future__ import annotations

import unittest

from config.settings import Settings


class SettingsTestCase(unittest.TestCase):
    """Validate settings normalization rules."""

    def test_invalid_theme_is_forced_to_dark(self) -> None:
        """Settings always use the permanent dark theme."""
        settings: Settings = Settings.from_dict({"theme": "light"})

        self.assertEqual(settings.theme, "dark")

    def test_invalid_playlist_limit_uses_safe_default(self) -> None:
        """Unsupported playlist limits fall back to the safe default."""
        settings: Settings = Settings.from_dict({"max_playlist_items": 999})

        self.assertEqual(settings.max_playlist_items, 200)

    def test_unlimited_playlist_limit_uses_safe_default(self) -> None:
        """The old unlimited playlist option falls back to the safe default."""
        settings: Settings = Settings.from_dict({"max_playlist_items": 0})

        self.assertEqual(settings.max_playlist_items, 200)

    def test_playlist_range_defaults_are_loaded(self) -> None:
        """Playlist range settings use safe defaults."""
        settings: Settings = Settings.from_dict({})

        self.assertEqual(settings.playlist_start_index, 1)
        self.assertEqual(settings.playlist_end_index, 0)

    def test_unsupported_background_suffix_is_removed(self) -> None:
        """Unsupported background image formats are ignored."""
        settings: Settings = Settings.from_dict({"background_image_path": "image.bmp"})

        self.assertEqual(settings.background_image_path, "")

    def test_audio_options_use_safe_defaults_for_legacy_settings(self) -> None:
        """Settings created before v0.5.0 receive non-invasive defaults."""
        settings: Settings = Settings.from_dict({"selected_format": "mp3"})

        self.assertEqual(settings.selected_audio_quality, "best")
        self.assertFalse(settings.download_thumbnail)
        self.assertFalse(settings.write_metadata)
        self.assertFalse(settings.write_subtitles)
        self.assertFalse(settings.write_auto_subtitles)
        self.assertEqual(settings.subtitle_languages, "es,en")
        self.assertEqual(settings.filename_template, "%(title)s.%(ext)s")

    def test_advanced_audio_settings_are_loaded(self) -> None:
        """Advanced audio and auxiliary output settings persist."""
        settings: Settings = Settings.from_dict(
            {
                "selected_format": "wav",
                "selected_audio_quality": "320",
                "download_thumbnail": True,
                "write_metadata": True,
                "write_subtitles": True,
                "write_auto_subtitles": True,
                "subtitle_languages": " es, en ",
                "filename_template": "%(channel)s - %(title)s.%(ext)s",
                "create_channel_folder": True,
                "create_playlist_folder": True,
            }
        )

        self.assertEqual(settings.selected_format, "wav")
        self.assertEqual(settings.selected_audio_quality, "320")
        self.assertTrue(settings.download_thumbnail)
        self.assertEqual(settings.subtitle_languages, "es,en")
        self.assertTrue(settings.create_playlist_folder)

    def test_unsafe_filename_template_uses_safe_default(self) -> None:
        """Persisted templates cannot escape the selected output folder."""
        settings: Settings = Settings.from_dict({"filename_template": "..\\outside"})

        self.assertEqual(settings.filename_template, "%(title)s.%(ext)s")


if __name__ == "__main__":
    unittest.main()
