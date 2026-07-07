"""External dependency availability checks."""

from __future__ import annotations

import shutil
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DependencyStatus:
    """Availability status for an external command-line dependency.

    Attributes:
        name: Dependency command name.
        executable_path: Resolved executable path when available.
        is_available: Whether the dependency exists in PATH.
    """

    name: str
    executable_path: str | None
    is_available: bool


@dataclass(frozen=True, slots=True)
class DependencyCheckResult:
    """Combined dependency check result.

    Attributes:
        yt_dlp: Availability status for yt-dlp.
        ffmpeg: Availability status for ffmpeg.
    """

    yt_dlp: DependencyStatus
    ffmpeg: DependencyStatus

    @property
    def all_available(self) -> bool:
        """Return whether all required dependencies are available."""
        return self.yt_dlp.is_available and self.ffmpeg.is_available


class DependencyChecker:
    """Checks required command-line tools without installing them."""

    def check(self) -> DependencyCheckResult:
        """Check all required external dependencies.

        Returns:
            Typed dependency availability result.
        """
        return DependencyCheckResult(
            yt_dlp=self._check_command("yt-dlp"),
            ffmpeg=self._check_command("ffmpeg"),
        )

    @staticmethod
    def _check_command(command_name: str) -> DependencyStatus:
        """Check whether a command exists in PATH."""
        executable_path: str | None = shutil.which(command_name)
        return DependencyStatus(
            name=command_name,
            executable_path=executable_path,
            is_available=executable_path is not None,
        )
