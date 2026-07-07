"""Application lifecycle infrastructure."""

from __future__ import annotations

import sys
from importlib import resources
from types import TracebackType

from PySide6.QtWidgets import QApplication

from config.app_config import AppConfig
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
        self._qt_application: QApplication = QApplication(argv or sys.argv)
        self._main_window: MainWindow | None = None
        self._configure_metadata()
        self._load_stylesheet()

    def run(self) -> int:
        """Show the main window and start the Qt event loop.

        Returns:
            The process exit code returned by Qt.
        """
        self._main_window = MainWindow(self._config)
        self._main_window.show()
        return self._qt_application.exec()

    def _configure_metadata(self) -> None:
        """Apply application metadata to Qt."""
        self._qt_application.setApplicationName(self._config.application_name)
        self._qt_application.setApplicationVersion(self._config.application_version)
        self._qt_application.setOrganizationName(self._config.organization_name)

    def _load_stylesheet(self) -> None:
        """Load the bundled dark theme stylesheet."""
        stylesheet_path: resources.abc.Traversable = resources.files("styles").joinpath(
            "dark_theme.qss"
        )
        stylesheet: str = stylesheet_path.read_text(encoding="utf-8")
        self._qt_application.setStyleSheet(stylesheet)

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
        self._main_window = None
