"""Main window infrastructure for YouTube Downloader Pro."""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QWidget

from config.app_config import AppConfig


class MainWindow(QMainWindow):
    """Primary desktop window for the application."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize the main window.

        Args:
            config: Runtime application configuration.
        """
        super().__init__()
        self._config: AppConfig = config
        self._configure_window()

    def _configure_window(self) -> None:
        """Apply base window metadata and sizing."""
        self.setWindowTitle(self._config.application_name)
        self.resize(
            self._config.window_initial_width,
            self._config.window_initial_height,
        )
        self.setMinimumSize(
            self._config.window_minimum_width,
            self._config.window_minimum_height,
        )

        central_widget: QWidget = QWidget(self)
        central_widget.setObjectName("mainContentArea")
        self.setCentralWidget(central_widget)
