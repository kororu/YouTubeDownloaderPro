"""Application lifecycle infrastructure."""

from __future__ import annotations

import sys
from logging import Logger
from pathlib import Path
from types import TracebackType

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from config.app_config import AppConfig
from config.settings import Settings
from config.settings_manager import SettingsManager
from core.logger import configure_logging
from resources.resource_manager import ResourceManager
from styles.theme_manager import ThemeManager
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
        self._settings_manager: SettingsManager = SettingsManager()
        self._settings: Settings = self._settings_manager.load()
        self._qt_application: QApplication = QApplication(argv or sys.argv)
        self._resource_manager: ResourceManager = ResourceManager()
        self._theme_manager: ThemeManager = ThemeManager()
        self._main_window: MainWindow | None = None
        self._configure_metadata()
        self._apply_icon()
        self._apply_theme()

    def run(self) -> int:
        """Show the main window and start the Qt event loop.

        Returns:
            The process exit code returned by Qt.
        """
        self._main_window = MainWindow(
            config=self._config,
            settings=self._settings,
            settings_manager=self._settings_manager,
        )
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

    def _apply_icon(self) -> None:
        """Apply the application icon when the asset is available."""
        icon_path: Path | None = self._resource_manager.resolve_icon("app_icon.svg")
        if icon_path is None:
            self._logger.warning("Application icon could not be found.")
            return
        self._qt_application.setWindowIcon(QIcon(str(icon_path)))
        self._logger.info("Application icon applied.")

    def _apply_theme(self) -> None:
        """Apply the configured application theme."""
        theme_applied: bool = self._theme_manager.apply_theme(
            self._qt_application,
            self._settings.theme,
        )
        if theme_applied:
            self._logger.info("Theme applied: %s.", self._settings.theme)
            return
        self._logger.warning("Theme could not be applied: %s.", self._settings.theme)

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
