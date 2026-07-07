"""URL validation service."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class UrlValidationResult:
    """URL validation result.

    Attributes:
        is_valid: Whether the URL is accepted.
        normalized_url: Trimmed URL when valid.
        error_message: Validation error when invalid.
    """

    is_valid: bool
    normalized_url: str | None
    error_message: str | None


class UrlValidator:
    """Validates user-provided media URLs."""

    _allowed_schemes: tuple[str, ...] = ("http", "https")

    def validate(self, source_url: str) -> UrlValidationResult:
        """Validate a source URL.

        Args:
            source_url: URL entered by the user.

        Returns:
            Validation result with a normalized URL or error message.
        """
        normalized_url: str = source_url.strip()
        if not normalized_url:
            return UrlValidationResult(False, None, "La URL no puede estar vacía.")

        parsed_url = urlparse(normalized_url)
        if parsed_url.scheme.lower() not in self._allowed_schemes:
            return UrlValidationResult(False, None, "La URL debe comenzar con http o https.")

        if not parsed_url.netloc:
            return UrlValidationResult(False, None, "La URL debe incluir un dominio válido.")

        return UrlValidationResult(True, normalized_url, None)
