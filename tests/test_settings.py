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


if __name__ == "__main__":
    unittest.main()
