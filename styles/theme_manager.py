"""QSS theme loading and application."""

from __future__ import annotations

from pathlib import Path
from typing import Final

from PySide6.QtWidgets import QApplication

from core.paths import AppPaths, get_app_paths

DARK_THEME: Final[str] = "dark"
LIGHT_THEME: Final[str] = "light"


class ThemeManager:
    """Loads and applies application themes."""

    _theme_files: dict[str, str] = {
        DARK_THEME: "dark_theme.qss",
        LIGHT_THEME: "light_theme.qss",
    }

    def __init__(self, app_paths: AppPaths | None = None) -> None:
        """Initialize the theme manager.

        Args:
            app_paths: Optional resolved application paths.
        """
        self._app_paths: AppPaths = app_paths or get_app_paths()

    def apply_theme(self, application: QApplication, theme_name: str = DARK_THEME) -> bool:
        """Apply a theme to a Qt application.

        Args:
            application: Qt application instance.
            theme_name: Theme name to apply.

        Returns:
            True when the theme was loaded and applied; otherwise False.
        """
        stylesheet: str | None = self.load_stylesheet(theme_name)
        if stylesheet is None:
            application.setStyleSheet("")
            return False

        application.setStyleSheet(stylesheet)
        return True

    def load_stylesheet(self, theme_name: str = DARK_THEME) -> str | None:
        """Load stylesheet text for a theme.

        Args:
            theme_name: Theme name to load.

        Returns:
            QSS text when the file exists; otherwise None.
        """
        theme_file_name: str | None = self._theme_files.get(theme_name)
        if theme_file_name is None:
            return None

        theme_path: Path = self._app_paths.styles_dir / theme_file_name
        if not theme_path.is_file():
            return None

        try:
            return theme_path.read_text(encoding="utf-8")
        except OSError:
            return None
