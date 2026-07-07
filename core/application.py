"""Application lifecycle infrastructure."""

from __future__ import annotations

import sys
from types import TracebackType
from logging import Logger

from PySide6.QtWidgets import QApplication

from config.app_config import AppConfig
from core.logger import configure_logging
from styles.theme_manager import DARK_THEME, ThemeManager
from ui.main_window import MainWindow


class Application:
    """Encapsulates the Qt application lifecycle."""

    def __init__(self, argv: list[str] | None = None, config: AppConfig | None = None) -> None:
        """Initialize the application container.

        Args:
            argv: Command-line arguments passed to Qt.
            config: Runtime application configuration.
        """
        self._config: AppConfig = config or AppConfig()
        self._logger: Logger = configure_logging()
        self._logger.info("Starting application bootstrap.")
        self._qt_application: QApplication = QApplication(argv or sys.argv)
        self._theme_manager: ThemeManager = ThemeManager()
        self._main_window: MainWindow | None = None
        self._configure_metadata()
        self._apply_theme()

    def run(self) -> int:
        """Show the main window and start the Qt event loop.

        Returns:
            The process exit code returned by Qt.
        """
        self._main_window = MainWindow(self._config)
        self._main_window.show()
        self._logger.info("Main window shown.")
        return self._qt_application.exec()

    def _configure_metadata(self) -> None:
        """Apply application metadata to Qt."""
        self._qt_application.setApplicationName(self._config.application_name)
        self._qt_application.setApplicationVersion(self._config.application_version)
        self._qt_application.setOrganizationName(self._config.organization_name)
        self._logger.info(
            "Application metadata configured: name=%s version=%s organization=%s.",
            self._config.application_name,
            self._config.application_version,
            self._config.organization_name,
        )

    def _apply_theme(self) -> None:
        """Apply the configured application theme."""
        theme_applied: bool = self._theme_manager.apply_theme(self._qt_application, DARK_THEME)
        if theme_applied:
            self._logger.info("Theme applied: %s.", DARK_THEME)
            return
        self._logger.warning("Theme could not be applied: %s.", DARK_THEME)

    def __enter__(self) -> "Application":
        """Enter the application context.

        Returns:
            The current application instance.
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the application context."""
        self._logger.info("Application context closed.")
        self._main_window = None
