"""Filesystem path resolution for the application."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AppPaths:
    """Resolved application paths.

    Attributes:
        project_root: Root directory for the source or frozen application.
        resources_dir: Directory containing application resources.
        styles_dir: Directory containing QSS stylesheets.
        downloads_dir: Default local downloads directory.
        logs_dir: Directory used for diagnostic logs.
    """

    project_root: Path
    resources_dir: Path
    styles_dir: Path
    downloads_dir: Path
    logs_dir: Path


def resolve_project_root() -> Path:
    """Resolve the application root directory.

    Returns:
        Project root for source execution or PyInstaller runtime root.
    """
    if bool(getattr(sys, "frozen", False)):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def get_app_paths() -> AppPaths:
    """Resolve standard application directories.

    Returns:
        Immutable path collection for application infrastructure.
    """
    project_root: Path = resolve_project_root()
    return AppPaths(
        project_root=project_root,
        resources_dir=project_root / "resources",
        styles_dir=project_root / "styles",
        downloads_dir=project_root / "downloads",
        logs_dir=project_root / "logs",
    )
