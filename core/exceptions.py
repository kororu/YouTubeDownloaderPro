"""Application-specific exceptions."""

from __future__ import annotations


class ApplicationError(Exception):
    """Base exception for recoverable application errors."""


class ValidationError(ApplicationError):
    """Raised when user input fails validation."""


class DependencyUnavailableError(ApplicationError):
    """Raised when an external dependency is unavailable."""


class CommandExecutionError(ApplicationError):
    """Raised when an external command fails."""


class MetadataExtractionError(ApplicationError):
    """Raised when metadata extraction fails."""
