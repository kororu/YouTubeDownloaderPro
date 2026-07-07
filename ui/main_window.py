"""Main window infrastructure for YouTube Downloader Pro."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import QMainWindow, QSplitter, QVBoxLayout, QWidget

from config.app_config import AppConfig
from config.settings import Settings
from config.settings_manager import SettingsManager
from core.dependency_checker import DependencyChecker, DependencyCheckResult
from dialogs.about_dialog import AboutDialog
from models.download_enums import DownloadFormat, DownloadQuality
from models.download_item import DownloadItem
from models.video_metadata import VideoMetadata
from services.metadata_worker import MetadataWorker
from services.url_validator import UrlValidationResult, UrlValidator
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
        self._url_validator: UrlValidator = UrlValidator()
        self._metadata_workers: dict[str, MetadataWorker] = {}
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
        """Validate a video URL and load metadata."""
        validation_result: UrlValidationResult = self._url_validator.validate(source_url)
        if not validation_result.is_valid or validation_result.normalized_url is None:
            self._show_input_error(validation_result.error_message or "URL inválida.")
            return

        download_item: DownloadItem | None = self._create_download_item(
            validation_result.normalized_url,
            media_format,
            quality,
        )
        if download_item is None:
            return

        self._queue_widget.add_download_item(download_item)
        self._log_widget.append_info(f"Cargando metadatos: {download_item.source_url}")
        self._status_widget.set_status_message("cargando metadatos")
        self._start_metadata_worker(download_item)

    def _add_playlist_to_queue(self, source_url: str, media_format: str, quality: str) -> None:
        """Validate playlist URL and report current support boundary."""
        validation_result: UrlValidationResult = self._url_validator.validate(source_url)
        if not validation_result.is_valid:
            self._show_input_error(validation_result.error_message or "URL inválida.")
            return
        self._log_widget.append_warning("La selección de playlist se implementará en Sprint 4.")
        self._status_widget.set_status_message("playlist pendiente de Sprint 4")

    def _handle_queue_changed(self, total_items: int, selected_items: int) -> None:
        """Update status when queue selection changes."""
        self._status_widget.update_queue_status(total_items, selected_items)

    def _create_download_item(
        self,
        source_url: str,
        media_format: str,
        quality: str,
    ) -> DownloadItem | None:
        """Create a validated domain download item."""
        try:
            return DownloadItem.create(
                source_url=source_url,
                media_format=DownloadFormat(media_format),
                quality=DownloadQuality(quality),
            )
        except ValueError:
            self._show_input_error("Formato o calidad no válidos.")
            return None

    def _start_metadata_worker(self, download_item: DownloadItem) -> None:
        """Start asynchronous metadata loading for a queue item."""
        worker: MetadataWorker = MetadataWorker(download_item.item_id, download_item.source_url)
        worker.metadata_loaded.connect(self._handle_metadata_loaded)
        worker.metadata_failed.connect(self._handle_metadata_failed)
        worker.finished.connect(lambda item_id=download_item.item_id: self._remove_metadata_worker(item_id))
        self._metadata_workers[download_item.item_id] = worker
        worker.start()

    def _handle_metadata_loaded(self, item_id: str, metadata: object) -> None:
        """Handle successful metadata loading."""
        if not isinstance(metadata, VideoMetadata):
            self._handle_metadata_failed(item_id, "Respuesta de metadatos inválida.")
            return
        self._queue_widget.update_item_metadata(item_id, metadata)
        self._log_widget.append_info(f"Metadatos cargados: {metadata.title}")
        self._status_widget.set_status_message("metadatos cargados")

    def _handle_metadata_failed(self, item_id: str, error_message: str) -> None:
        """Handle metadata loading failure."""
        self._queue_widget.mark_item_failed(item_id, error_message)
        self._log_widget.append_error(error_message)
        self._status_widget.set_status_message("error de metadatos")

    def _remove_metadata_worker(self, item_id: str) -> None:
        """Remove a finished metadata worker."""
        worker: MetadataWorker | None = self._metadata_workers.pop(item_id, None)
        if worker is not None:
            worker.deleteLater()

    def _show_input_error(self, message: str) -> None:
        """Show validation feedback to the user."""
        self._log_widget.append_error(message)
        self._status_widget.set_status_message("entrada inválida")

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
