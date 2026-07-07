"""Main window infrastructure for YouTube Downloader Pro."""

from __future__ import annotations

from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QSplitter, QVBoxLayout, QWidget

from config.app_config import AppConfig
from config.settings import Settings
from config.settings_manager import SettingsManager
from core.dependency_checker import DependencyChecker, DependencyCheckResult
from widgets.dependency_notice_widget import DependencyNoticeWidget
from widgets.footer_widget import FooterWidget
from widgets.log_widget import LogWidget
from widgets.queue_widget import QueueWidget
from widgets.status_widget import StatusWidget
from widgets.toolbar_widget import ToolbarWidget


class MainWindow(QMainWindow):
    """Primary desktop window for the application."""

    def __init__(
        self,
        config: AppConfig,
        settings: Settings,
        settings_manager: SettingsManager,
    ) -> None:
        """Initialize the main window.

        Args:
            config: Runtime application configuration.
            settings: Persisted application settings.
            settings_manager: Settings persistence manager.
        """
        super().__init__()
        self._config: AppConfig = config
        self._settings: Settings = settings
        self._settings_manager: SettingsManager = settings_manager
        self._dependency_result: DependencyCheckResult = DependencyChecker().check()
        self._configure_window()
        self._build_layout()

    def _configure_window(self) -> None:
        """Apply base window metadata and sizing."""
        self.setWindowTitle(self._config.application_name)
        self.resize(
            self._settings.window_width,
            self._settings.window_height,
        )
        self.move(self._settings.window_x, self._settings.window_y)
        self.setMinimumSize(
            self._config.window_minimum_width,
            self._config.window_minimum_height,
        )

        central_widget: QWidget = QWidget(self)
        central_widget.setObjectName("mainContentArea")
        self.setCentralWidget(central_widget)

    def _build_layout(self) -> None:
        """Build the main window layout."""
        central_widget: QWidget | None = self.centralWidget()
        if central_widget is None:
            return

        layout: QVBoxLayout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        toolbar_widget: ToolbarWidget = ToolbarWidget(central_widget)
        queue_widget: QueueWidget = QueueWidget(central_widget)
        log_widget: LogWidget = LogWidget(central_widget)
        status_widget: StatusWidget = StatusWidget(central_widget)
        footer_widget: FooterWidget = FooterWidget(central_widget)

        main_splitter: QSplitter = QSplitter(Qt.Orientation.Horizontal, central_widget)
        main_splitter.setObjectName("mainSplitter")

        content_splitter: QSplitter = QSplitter(Qt.Orientation.Vertical, main_splitter)
        content_splitter.setObjectName("mainContentSplitter")
        content_splitter.addWidget(queue_widget)
        content_splitter.addWidget(log_widget)
        content_splitter.setStretchFactor(0, 3)
        content_splitter.setStretchFactor(1, 1)

        dependency_notice_widget: DependencyNoticeWidget = DependencyNoticeWidget(
            self._dependency_result,
            main_splitter,
        )
        dependency_notice_widget.setMinimumWidth(280)
        dependency_notice_widget.setMaximumWidth(360)

        main_splitter.addWidget(content_splitter)
        main_splitter.addWidget(dependency_notice_widget)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 0)

        layout.addWidget(toolbar_widget)
        layout.addWidget(main_splitter, 1)
        layout.addWidget(status_widget)
        layout.addWidget(footer_widget)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Persist window geometry before closing.

        Args:
            event: Qt close event.
        """
        updated_settings: Settings = self._settings.with_window_geometry(
            width=self.width(),
            height=self.height(),
            x_position=self.x(),
            y_position=self.y(),
        )
        self._settings_manager.save(updated_settings)
        self._settings = updated_settings
        super().closeEvent(event)
