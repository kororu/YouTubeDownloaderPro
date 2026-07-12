"""Tests for URL validation helpers."""

from __future__ import annotations

import unittest

from services.url_validator import UrlValidator


class UrlValidatorTestCase(unittest.TestCase):
    """Validate source URL handling."""

    def setUp(self) -> None:
        """Create a validator for each test."""
        self.validator: UrlValidator = UrlValidator()

    def test_valid_http_url_is_accepted(self) -> None:
        """HTTP and HTTPS URLs are accepted."""
        result = self.validator.validate("https://www.youtube.com/watch?v=abc123")

        self.assertTrue(result.is_valid)
        self.assertEqual(result.normalized_url, "https://www.youtube.com/watch?v=abc123")

    def test_invalid_scheme_is_rejected(self) -> None:
        """Non HTTP schemes are rejected."""
        result = self.validator.validate("ftp://example.com/video")

        self.assertFalse(result.is_valid)

    def test_radio_list_is_detected_as_youtube_mix(self) -> None:
        """YouTube radio playlists are treated as Mix URLs."""
        self.assertTrue(
            self.validator.is_youtube_mix_url("https://www.youtube.com/watch?v=abc123&list=RDabc123")
        )

    def test_start_radio_parameter_is_detected_as_youtube_mix(self) -> None:
        """The start_radio query parameter is treated as a Mix signal."""
        self.assertTrue(
            self.validator.is_youtube_mix_url("https://www.youtube.com/watch?v=abc123&start_radio=1")
        )

    def test_standard_playlist_is_not_youtube_mix(self) -> None:
        """Regular playlist IDs are not treated as YouTube Mix URLs."""
        self.assertFalse(
            self.validator.is_youtube_mix_url("https://www.youtube.com/playlist?list=PLabc123")
        )


if __name__ == "__main__":
    unittest.main()
