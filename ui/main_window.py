"""Main window infrastructure for YouTube Downloader Pro."""

from __future__ import annotations

from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QSplitter, QVBoxLayout, QWidget

from config.app_config import AppConfig
from config.settings import Settings
from config.settings_manager import SettingsManager
from core.dependency_checker import DependencyChecker, DependencyCheckResult
from dialogs.about_dialog import AboutDialog
from widgets.dependency_notice_widget import DependencyNoticeWidget
from widgets.footer_widget import FooterWidget
from widgets.log_widget import LogWidget
from widgets.queue_widget import QueueWidget
from widgets.settings_widget import SettingsWidget
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
        self._toolbar_widget: ToolbarWidget
        self._queue_widget: QueueWidget
        self._log_widget: LogWidget
        self._status_widget: StatusWidget
        self._settings_widget: SettingsWidget
        self._configure_window()
        self._build_menu()
        self._build_layout()
        self._connect_signals()

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

    def _build_menu(self) -> None:
        """Build the application menu."""
        about_action: QAction = QAction("Acerca de", self)
        about_action.triggered.connect(self._show_about_dialog)
        self.menuBar().addMenu("Ayuda").addAction(about_action)

    def _build_layout(self) -> None:
        """Build the main window layout."""
        central_widget: QWidget | None = self.centralWidget()
        if central_widget is None:
            return

        layout: QVBoxLayout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._toolbar_widget = ToolbarWidget(
            selected_format=self._settings.selected_format,
            selected_quality=self._settings.selected_quality,
            parent=central_widget,
        )
        self._queue_widget = QueueWidget(central_widget)
        self._log_widget = LogWidget(central_widget)
        self._status_widget = StatusWidget(central_widget)
        self._settings_widget = SettingsWidget(self._settings, central_widget)
        footer_widget: FooterWidget = FooterWidget(central_widget)

        main_splitter: QSplitter = QSplitter(Qt.Orientation.Horizontal, central_widget)
        main_splitter.setObjectName("mainSplitter")

        content_splitter: QSplitter = QSplitter(Qt.Orientation.Vertical, main_splitter)
        content_splitter.setObjectName("mainContentSplitter")
        content_splitter.addWidget(self._queue_widget)
        content_splitter.addWidget(self._log_widget)
        content_splitter.setStretchFactor(0, 3)
        content_splitter.setStretchFactor(1, 1)

        side_panel: QWidget = QWidget(main_splitter)
        side_panel.setObjectName("sidePanel")
        side_panel_layout: QVBoxLayout = QVBoxLayout(side_panel)
        side_panel_layout.setContentsMargins(0, 0, 0, 0)
        side_panel_layout.setSpacing(0)

        dependency_notice_widget: DependencyNoticeWidget = DependencyNoticeWidget(
            self._dependency_result,
            side_panel,
        )

        side_panel_layout.addWidget(self._settings_widget)
        side_panel_layout.addWidget(dependency_notice_widget, 1)
        side_panel.setMinimumWidth(300)
        side_panel.setMaximumWidth(380)

        main_splitter.addWidget(content_splitter)
        main_splitter.addWidget(side_panel)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 0)

        layout.addWidget(self._toolbar_widget)
        layout.addWidget(main_splitter, 1)
        layout.addWidget(self._status_widget)
        layout.addWidget(footer_widget)

    def _connect_signals(self) -> None:
        """Connect main window widget signals."""
        self._toolbar_widget.add_video_requested.connect(self._add_video_to_queue)
        self._toolbar_widget.add_playlist_requested.connect(self._add_playlist_to_queue)
        self._toolbar_widget.settings_requested.connect(self._focus_settings_panel)
        self._toolbar_widget.about_requested.connect(self._show_about_dialog)
        self._queue_widget.queue_changed.connect(self._handle_queue_changed)
        self._settings_widget.settings_changed.connect(self._save_settings)
        self._status_widget.update_dependency_status(self._dependency_result.all_available)

    def _add_video_to_queue(self, source_url: str, media_format: str, quality: str) -> None:
        """Add a video URL to the queue view."""
        self._queue_widget.add_item(source_url, media_format, quality)
        self._log_widget.append_info(f"Video agregado a la cola: {source_url}")
        self._status_widget.set_status_message("video agregado")

    def _add_playlist_to_queue(self, source_url: str, media_format: str, quality: str) -> None:
        """Add a playlist URL to the queue view."""
        self._queue_widget.add_item(source_url, media_format, quality)
        self._log_widget.append_info(f"Playlist agregada a la cola: {source_url}")
        self._status_widget.set_status_message("playlist agregada")

    def _handle_queue_changed(self, total_items: int, selected_items: int) -> None:
        """Update status when queue selection changes."""
        self._status_widget.update_queue_status(total_items, selected_items)

    def _save_settings(self, settings: Settings) -> None:
        """Persist settings changed from the settings panel."""
        self._settings_manager.save(settings)
        self._settings = settings
        self._settings_widget.update_settings(settings)
        self._toolbar_widget.set_download_preferences(
            settings.selected_format,
            settings.selected_quality,
        )
        self._log_widget.append_info("Ajustes guardados.")
        self._status_widget.set_status_message("ajustes guardados")

    def _focus_settings_panel(self) -> None:
        """Move focus to the settings panel."""
        self._settings_widget.setFocus(Qt.FocusReason.ShortcutFocusReason)
        self._status_widget.set_status_message("ajustes visibles")

    def _show_about_dialog(self) -> None:
        """Open the about dialog."""
        dialog: AboutDialog = AboutDialog(self)
        dialog.exec()

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
