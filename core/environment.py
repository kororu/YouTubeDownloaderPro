"""Runtime environment detection."""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class EnvironmentInfo:
    """Information about the current runtime environment.

    Attributes:
        operating_system: Operating system name.
        is_windows: Whether the app is running on Windows.
        is_frozen: Whether the app is running as a PyInstaller executable.
        executable_path: Current Python or frozen executable path.
    """

    operating_system: str
    is_windows: bool
    is_frozen: bool
    executable_path: Path


def get_environment_info() -> EnvironmentInfo:
    """Detect runtime environment details.

    Returns:
        Current environment information.
    """
    operating_system: str = platform.system()
    executable_path: Path = Path(sys.executable).resolve()
    is_frozen: bool = bool(getattr(sys, "frozen", False))
    return EnvironmentInfo(
        operating_system=operating_system,
        is_windows=operating_system == "Windows",
        is_frozen=is_frozen,
        executable_path=executable_path,
    )
