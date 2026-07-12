"""Main window infrastructure for YouTube Downloader Pro."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import QFileDialog, QMainWindow, QSplitter, QVBoxLayout, QWidget

from config.app_config import AppConfig
from config.settings import Settings
from config.settings_manager import SettingsManager
from core.dependency_checker import DependencyChecker, DependencyCheckResult
from dialogs.about_dialog import AboutDialog
from models.download_enums import DownloadFormat, DownloadQuality, DownloadStatus
from models.download_item import DownloadItem
from models.download_progress import DownloadProgress
from models.playlist_metadata import PlaylistVideo
from models.playlist_range import PlaylistRange
from models.video_metadata import VideoMetadata
from services.download_queue_service import DownloadQueueService
from services.metadata_worker import MetadataWorker
from services.playlist_range_history_service import PlaylistRangeHistoryService
from services.playlist_worker import PlaylistWorker
from services.queue_persistence_service import QueuePersistenceService
from services.url_validator import UrlValidationResult, UrlValidator
from widgets.background_widget import BackgroundWidget
from widgets.footer_widget import FooterWidget
from widgets.log_widget import LogWidget
from widgets.queue_widget import QueueWidget
from widgets.settings_widget import SettingsWidget
from widgets.status_widget import StatusWidget
from widgets.toolbar_widget import ToolbarWidget


@dataclass(frozen=True, slots=True)
class PlaylistLoadRequest:
    """Playlist load request state."""

    source_url: str
    media_format: DownloadFormat
    quality: DownloadQuality
    playlist_range: PlaylistRange
    is_youtube_mix: bool


@dataclass(slots=True)
class PlaylistLoadStats:
    """Mutable playlist load counters."""

    processed_count: int = 0
    added_count: int = 0
    duplicate_count: int = 0


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
        self._playlist_workers: dict[str, PlaylistWorker] = {}
        self._playlist_requests: dict[str, PlaylistLoadRequest] = {}
        self._playlist_stats: dict[str, PlaylistLoadStats] = {}
        self._playlist_totals: dict[str, int] = {}
        self._active_playlist_loads: int = 0
        self._download_queue_service: DownloadQueueService = DownloadQueueService(
            self._settings.max_concurrent_downloads
        )
        self._queue_persistence_service: QueuePersistenceService = QueuePersistenceService()
        self._playlist_range_history_service: PlaylistRangeHistoryService = PlaylistRangeHistoryService()
        self._toolbar_widget: ToolbarWidget
        self._queue_widget: QueueWidget
        self._log_widget: LogWidget
        self._status_widget: StatusWidget
        self._settings_widget: SettingsWidget
        self._background_widget: BackgroundWidget
        self._side_panel: QWidget
        self._configure_window()
        self._build_menu()
        self._build_layout()
        self._connect_signals()
        self._restore_persisted_queue()

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

        central_widget: BackgroundWidget = BackgroundWidget(self._settings.background_image_path, self)
        self.setCentralWidget(central_widget)
        self._background_widget = central_widget

    def _build_menu(self) -> None:
        """Build the application menu."""
        queue_menu = self.menuBar().addMenu("Cola")

        start_action: QAction = QAction("Descargar seleccionados", self)
        start_action.setShortcut("Ctrl+D")
        start_action.triggered.connect(self._start_selected_downloads)

        cancel_current_action: QAction = QAction("Cancelar actual", self)
        cancel_current_action.setShortcut("Ctrl+K")
        cancel_current_action.triggered.connect(self._cancel_current_download)

        cancel_all_action: QAction = QAction("Cancelar todo", self)
        cancel_all_action.setShortcut("Ctrl+Shift+K")
        cancel_all_action.triggered.connect(self._cancel_all_downloads)

        select_all_action: QAction = QAction("Seleccionar todo", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self._select_all_queue_items)

        deselect_all_action: QAction = QAction("Deseleccionar", self)
        deselect_all_action.setShortcut("Ctrl+Shift+A")
        deselect_all_action.triggered.connect(self._deselect_all_queue_items)

        queue_menu.addAction(start_action)
        queue_menu.addAction(cancel_current_action)
        queue_menu.addAction(cancel_all_action)
        queue_menu.addSeparator()
        queue_menu.addAction(select_all_action)
        queue_menu.addAction(deselect_all_action)

        log_menu = self.menuBar().addMenu("Registro")
        export_logs_action: QAction = QAction("Exportar registro", self)
        export_logs_action.setShortcut("Ctrl+L")
        export_logs_action.triggered.connect(self._export_logs)
        log_menu.addAction(export_logs_action)

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
            playlist_start_index=self._settings.playlist_start_index,
            playlist_end_index=self._settings.playlist_end_index,
            playlist_limit=self._settings.max_playlist_items,
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
        self._side_panel = side_panel
        side_panel_layout: QVBoxLayout = QVBoxLayout(side_panel)
        side_panel_layout.setContentsMargins(0, 0, 0, 0)
        side_panel_layout.setSpacing(0)

        side_panel_layout.addWidget(self._settings_widget)
        side_panel_layout.addStretch(1)
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
        self._apply_background_state()

    def _connect_signals(self) -> None:
        """Connect main window widget signals."""
        self._toolbar_widget.add_video_requested.connect(self._add_video_to_queue)
        self._toolbar_widget.add_playlist_requested.connect(self._add_playlist_to_queue)
        self._toolbar_widget.add_next_playlist_range_requested.connect(self._add_next_playlist_range_to_queue)
        self._toolbar_widget.start_downloads_requested.connect(self._start_selected_downloads)
        self._toolbar_widget.cancel_current_requested.connect(self._cancel_current_download)
        self._toolbar_widget.cancel_all_requested.connect(self._cancel_all_downloads)
        self._toolbar_widget.settings_requested.connect(self._focus_settings_panel)
        self._toolbar_widget.about_requested.connect(self._show_about_dialog)
        self._toolbar_widget.queue_search_changed.connect(self._queue_widget.set_search_text)
        self._toolbar_widget.queue_sort_changed.connect(self._queue_widget.set_sort_mode)
        self._queue_widget.queue_changed.connect(self._handle_queue_changed)
        self._settings_widget.settings_changed.connect(self._save_settings)
        self._log_widget.export_requested.connect(self._export_logs)
        self._queue_widget.item_removed.connect(self._remove_item_from_services)
        self._report_dependency_status()
        self._download_queue_service.item_changed.connect(self._handle_download_item_changed)
        self._download_queue_service.progress_changed.connect(self._handle_download_progress)
        self._download_queue_service.log_received.connect(self._handle_download_log)
        self._download_queue_service.queue_finished.connect(self._handle_download_queue_finished)

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
        self._download_queue_service.add_items((download_item,))
        self._log_widget.append_info(f"Cargando metadatos: {download_item.source_url}")
        self._status_widget.set_status_message("cargando metadatos")
        self._start_metadata_worker(download_item)

    def _add_playlist_to_queue(
        self,
        source_url: str,
        media_format: str,
        quality: str,
        playlist_range_data: object,
    ) -> None:
        """Validate a playlist URL and load a selected range."""
        if not isinstance(playlist_range_data, PlaylistRange):
            self._show_input_error("Rango de playlist inválido.")
            return
        self._queue_playlist_range(source_url, media_format, quality, playlist_range_data)

    def _add_next_playlist_range_to_queue(self, source_url: str, media_format: str, quality: str) -> None:
        """Validate a playlist URL and load the next persisted range."""
        validation_result: UrlValidationResult = self._url_validator.validate(source_url)
        if not validation_result.is_valid or validation_result.normalized_url is None:
            self._show_input_error(validation_result.error_message or "URL inválida.")
            return
        playlist_range: PlaylistRange = self._playlist_range_history_service.next_range(
            validation_result.normalized_url,
            self._settings.max_playlist_items,
            self._settings.playlist_start_index,
        )
        self._queue_playlist_range(validation_result.normalized_url, media_format, quality, playlist_range)

    def _queue_playlist_range(
        self,
        source_url: str,
        media_format: str,
        quality: str,
        playlist_range: PlaylistRange,
    ) -> None:
        """Validate a playlist request and start range loading."""
        validation_result: UrlValidationResult = self._url_validator.validate(source_url)
        if not validation_result.is_valid or validation_result.normalized_url is None:
            self._show_input_error(validation_result.error_message or "URL inválida.")
            return
        try:
            selected_format: DownloadFormat = DownloadFormat(media_format)
            selected_quality: DownloadQuality = DownloadQuality(quality)
        except ValueError:
            self._show_input_error("Formato o calidad no válidos.")
            return

        if playlist_range.item_count > 500:
            self._log_widget.append_warning(
                f"Advertencia: el rango solicitado contiene {playlist_range.item_count} videos."
            )

        normalized_url: str = validation_result.normalized_url
        is_youtube_mix: bool = self._url_validator.is_youtube_mix_url(normalized_url)
        request_id: str = str(uuid4())
        self._playlist_requests[request_id] = PlaylistLoadRequest(
            source_url=normalized_url,
            media_format=selected_format,
            quality=selected_quality,
            playlist_range=playlist_range,
            is_youtube_mix=is_youtube_mix,
        )
        self._playlist_stats[request_id] = PlaylistLoadStats()
        self._start_playlist_worker(request_id, normalized_url, playlist_range)
        if is_youtube_mix:
            self._log_widget.append_info("YouTube Mix detectado.")
        self._log_widget.append_info(f"Rango solicitado: {playlist_range.label()}")
        self._log_widget.append_info(f"Cargando playlist: {normalized_url}")
        self._status_widget.set_status_message("cargando playlist")

    def _handle_queue_changed(self, total_items: int, selected_items: int) -> None:
        """Update status when queue selection changes."""
        self._status_widget.update_queue_status(total_items, selected_items)
        if self._active_playlist_loads == 0:
            self._persist_queue()

    def _restore_persisted_queue(self) -> None:
        """Restore queue items persisted from a previous session."""
        persisted_items: tuple[DownloadItem, ...] = self._queue_persistence_service.load()
        if not persisted_items:
            return
        for item in persisted_items:
            self._queue_widget.add_download_item(item)
        self._download_queue_service.add_items(persisted_items)
        self._log_widget.append_info(f"Cola restaurada: {len(persisted_items)} elementos.")
        self._status_widget.set_status_message("cola restaurada")

    def _persist_queue(self) -> None:
        """Persist current queue items."""
        self._queue_persistence_service.save(self._queue_widget.all_download_items())

    def _remove_item_from_services(self, item_id: str) -> None:
        """Persist queue after an item is removed."""
        self._persist_queue()

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
        self._download_queue_service.add_items(self._queue_widget.all_download_items())
        self._persist_queue()
        self._log_widget.append_info(f"Metadatos cargados: {metadata.title}")
        self._status_widget.set_status_message("metadatos cargados")

    def _handle_metadata_failed(self, item_id: str, error_message: str) -> None:
        """Handle metadata loading failure."""
        friendly_message: str = self._friendly_error_message(error_message)
        self._queue_widget.mark_item_failed(item_id, friendly_message)
        self._persist_queue()
        self._log_widget.append_error(friendly_message)
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

    def _start_playlist_worker(self, request_id: str, source_url: str, playlist_range: PlaylistRange) -> None:
        """Start asynchronous incremental playlist loading."""
        worker: PlaylistWorker = PlaylistWorker(request_id, source_url, playlist_range)
        worker.playlist_started.connect(self._handle_playlist_started)
        worker.playlist_total_detected.connect(self._handle_playlist_total_detected)
        worker.playlist_limit_reached.connect(self._handle_playlist_limit_reached)
        worker.playlist_batch_loaded.connect(self._handle_playlist_batch_loaded)
        worker.playlist_finished.connect(self._handle_playlist_finished)
        worker.playlist_cancelled.connect(self._handle_playlist_cancelled)
        worker.playlist_failed.connect(self._handle_playlist_failed)
        worker.finished.connect(lambda completed_id=request_id: self._remove_playlist_worker(completed_id))
        self._playlist_workers[request_id] = worker
        self._active_playlist_loads += 1
        worker.start()

    def _handle_playlist_started(self, request_id: str, source_url: str, playlist_range_data: object) -> None:
        """Handle playlist streaming startup."""
        self._log_widget.append_info("Cargando playlist...")
        self._log_widget.append_info(f"Origen: {source_url}")
        if isinstance(playlist_range_data, PlaylistRange):
            self._log_widget.append_info(f"Procesando rango {playlist_range_data.label()}")
        self._status_widget.set_status_message("cargando playlist")

    def _handle_playlist_total_detected(self, request_id: str, total_count: int) -> None:
        """Handle detected playlist total count."""
        self._playlist_totals[request_id] = total_count
        self._log_widget.append_info(f"Playlist detectada: {total_count} videos")
        request: PlaylistLoadRequest | None = self._playlist_requests.get(request_id)
        if request is not None and request.playlist_range.start_index > total_count:
            self._log_widget.append_warning("El inicio solicitado supera el total detectado.")

    def _handle_playlist_limit_reached(self, request_id: str, total_count: int, max_items: int) -> None:
        """Handle active playlist limit notification."""
        self._log_widget.append_warning(f"Límite activo: se procesarán {max_items} videos")
        self._status_widget.set_status_message("límite de playlist activo")

    def _handle_playlist_batch_loaded(
        self,
        request_id: str,
        videos: object,
        processed_count: int,
        total_count: object,
    ) -> None:
        """Handle a playlist batch loaded incrementally."""
        if not isinstance(videos, tuple):
            return
        playlist_videos: tuple[PlaylistVideo, ...] = tuple(video for video in videos if isinstance(video, PlaylistVideo))
        if not playlist_videos:
            return

        request: PlaylistLoadRequest | None = self._playlist_requests.get(request_id)
        stats: PlaylistLoadStats | None = self._playlist_stats.get(request_id)
        if request is None or stats is None:
            return

        detected_total: int | None = total_count if isinstance(total_count, int) else None
        if detected_total is not None:
            self._playlist_totals[request_id] = detected_total

        previous_processed_count: int = stats.processed_count
        download_items: list[DownloadItem] = []
        existing_duplicate_keys: set[str] = self._queue_duplicate_keys()
        for video in playlist_videos:
            download_item: DownloadItem = DownloadItem(
                item_id=str(uuid4()),
                source_url=video.source_url,
                media_format=request.media_format,
                quality=request.quality,
                status=DownloadStatus.READY,
                metadata=video.to_video_metadata(),
                playlist_index=video.index,
                playlist_title=video.playlist_title or request.source_url,
                playlist_source_url=request.source_url,
                is_youtube_mix=request.is_youtube_mix,
                video_id=video.video_id,
            )
            duplicate_key: str = download_item.duplicate_key()
            if duplicate_key in existing_duplicate_keys:
                stats.duplicate_count += 1
                self._log_widget.append_warning(f"Video omitido por duplicado: {video.title}")
                continue
            existing_duplicate_keys.add(duplicate_key)
            stats.added_count += 1
            download_items.append(download_item)
        playlist_items: tuple[DownloadItem, ...] = tuple(download_items)
        self._queue_widget.add_download_items(playlist_items)
        self._download_queue_service.add_items(playlist_items)

        stats.processed_count = processed_count
        requested_count: int = request.playlist_range.item_count
        percentage: int = min(100, round((processed_count / requested_count) * 100))
        self._status_widget.set_progress(float(percentage))
        last_video: PlaylistVideo = playlist_videos[-1]
        progress_message: str = (
            f"Procesando video {last_video.index} de {request.playlist_range.end_index} ({percentage}%)"
        )

        block_number: int = max(1, (processed_count - 1) // 25 + 1)
        self._log_widget.append_info(f"Procesando bloque {block_number}...")
        if previous_processed_count == 0:
            self._log_widget.append_info(
                f"Procesando video {playlist_videos[0].index} de {request.playlist_range.end_index}"
            )
        if self._should_log_playlist_progress(processed_count, requested_count):
            self._log_widget.append_info(progress_message)
        if playlist_items and self._should_log_playlist_item(processed_count, requested_count):
            self._log_widget.append_info(f"Agregado {last_video.index}/{request.playlist_range.end_index}: {last_video.title}")
            self._log_widget.append_info(f"Agregado a la cola: {last_video.title}")

    def _handle_playlist_finished(self, request_id: str, processed_count: int, limit_reached: bool) -> None:
        """Handle completed playlist streaming."""
        request: PlaylistLoadRequest | None = self._playlist_requests.pop(request_id, None)
        stats: PlaylistLoadStats = self._playlist_stats.pop(request_id, PlaylistLoadStats())
        self._playlist_totals.pop(request_id, None)
        self._active_playlist_loads = max(0, self._active_playlist_loads - 1)
        self._persist_queue()
        if request is not None and processed_count > 0:
            completed_end_index: int = min(
                request.playlist_range.end_index,
                request.playlist_range.start_index + processed_count - 1,
            )
            self._playlist_range_history_service.save_completed_range(
                request.source_url,
                PlaylistRange(request.playlist_range.start_index, completed_end_index),
            )
            next_range: PlaylistRange = request.playlist_range.next_range(self._settings.max_playlist_items)
            self._log_widget.append_info(f"Próximo rango sugerido: {next_range.label()}")
        if limit_reached:
            self._log_widget.append_warning("Carga detenida al alcanzar el límite configurado")
        self._log_widget.append_info(f"Videos agregados: {stats.added_count}")
        self._log_widget.append_info(f"Duplicados omitidos: {stats.duplicate_count}")
        self._log_widget.append_info(f"Carga finalizada: {stats.added_count} videos agregados")
        self._status_widget.set_status_message("playlist agregada")

    def _handle_playlist_cancelled(self, request_id: str, processed_count: int) -> None:
        """Handle playlist streaming cancellation."""
        self._playlist_requests.pop(request_id, None)
        stats: PlaylistLoadStats = self._playlist_stats.pop(request_id, PlaylistLoadStats())
        self._playlist_totals.pop(request_id, None)
        self._active_playlist_loads = max(0, self._active_playlist_loads - 1)
        self._persist_queue()
        self._log_widget.append_warning("Carga de playlist cancelada por el usuario")
        self._log_widget.append_info(f"Videos agregados: {stats.added_count}")
        self._log_widget.append_info(f"Duplicados omitidos: {stats.duplicate_count}")
        self._log_widget.append_info(f"Carga finalizada: {processed_count} videos procesados")
        self._status_widget.set_status_message("playlist cancelada")

    def _start_selected_downloads(self) -> None:
        """Start downloads for selected queue items."""
        selected_items: tuple[DownloadItem, ...] = self._queue_widget.selected_download_items()
        if not selected_items:
            self._show_input_error("Seleccione uno o más elementos de la cola.")
            return

        ready_items: tuple[DownloadItem, ...] = tuple(
            item for item in selected_items if item.status in {DownloadStatus.READY, DownloadStatus.FAILED}
        )
        if not ready_items:
            self._show_input_error("No hay elementos listos para descargar.")
            return

        self._download_queue_service.add_items(ready_items)
        self._download_queue_service.start_downloads(
            tuple(item.item_id for item in ready_items),
            Path(self._settings.output_folder),
        )
        self._log_widget.append_info(f"Descargas iniciadas: {len(ready_items)}")
        self._status_widget.set_status_message("descargando")

    def _cancel_current_download(self) -> None:
        """Cancel the current active download."""
        self._download_queue_service.cancel_current()
        self._log_widget.append_warning("Cancelación solicitada para la descarga actual.")

    def _cancel_all_downloads(self) -> None:
        """Cancel all active and pending downloads."""
        self._download_queue_service.cancel_all()
        for worker in self._playlist_workers.values():
            worker.cancel()
        self._log_widget.append_warning("Cancelación solicitada para toda la cola.")

    def _handle_download_item_changed(self, item: object) -> None:
        """Update UI when a download item changes."""
        if not isinstance(item, DownloadItem):
            return
        self._queue_widget.update_download_item(item)
        self._persist_queue()
        if item.status is DownloadStatus.FAILED and item.error_message:
            self._log_widget.append_error(self._friendly_error_message(item.error_message))

    def _handle_download_progress(self, item_id: str, progress: object) -> None:
        """Update UI progress from worker output."""
        if not isinstance(progress, DownloadProgress):
            return
        self._status_widget.set_progress(progress.percentage)

    def _handle_download_log(self, item_id: str, message: str) -> None:
        """Display download worker log lines."""
        self._log_widget.append_info(message)

    def _handle_download_queue_finished(self) -> None:
        """Handle queue completion."""
        self._status_widget.set_status_message("cola finalizada")
        self._status_widget.set_progress(100.0)
        self._log_widget.append_info("Cola de descargas finalizada.")

    def _select_all_queue_items(self) -> None:
        """Select all queue items."""
        self._queue_widget.select_all_items()

    def _deselect_all_queue_items(self) -> None:
        """Deselect all queue items."""
        self._queue_widget.deselect_all_items()

    def _export_logs(self) -> None:
        """Export visible logs to a text file."""
        selected_path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exportar registro",
            str(Path(self._settings.output_folder) / "youtube_downloader_pro.log"),
            "Text files (*.txt *.log);;All files (*)",
        )
        if not selected_path:
            return
        try:
            self._log_widget.export_to_file(Path(selected_path))
        except OSError as exc:
            self._log_widget.append_error(f"No se pudo exportar el registro: {exc}")
            self._status_widget.set_status_message("error al exportar registro")
            return
        self._log_widget.append_info(f"Registro exportado: {selected_path}")
        self._status_widget.set_status_message("registro exportado")

    def _handle_playlist_failed(self, request_id: str, error_message: str) -> None:
        """Handle playlist metadata loading failure."""
        self._playlist_requests.pop(request_id, None)
        self._playlist_stats.pop(request_id, None)
        self._playlist_totals.pop(request_id, None)
        self._active_playlist_loads = max(0, self._active_playlist_loads - 1)
        self._log_widget.append_error(self._friendly_error_message(error_message))
        self._status_widget.set_status_message("error de playlist")

    def _remove_playlist_worker(self, request_id: str) -> None:
        """Remove a finished playlist worker."""
        worker: PlaylistWorker | None = self._playlist_workers.pop(request_id, None)
        if worker is not None:
            worker.deleteLater()

    @staticmethod
    def _friendly_error_message(error_message: str) -> str:
        """Convert technical errors into clearer user-facing messages."""
        normalized_message: str = error_message.lower()
        if "yt-dlp is not available" in normalized_message or "command not found" in normalized_message:
            return "yt-dlp no está disponible en PATH. Instálelo con winget y reinicie la aplicación."
        if "ffmpeg is required" in normalized_message:
            return "ffmpeg es requerido para descargas MP3. Instálelo con winget y reinicie la aplicación."
        if "invalid json" in normalized_message:
            return "yt-dlp devolvió una respuesta inválida. Verifique la URL e inténtelo nuevamente."
        if "no selectable videos" in normalized_message:
            return "No se encontraron videos seleccionables en la playlist."
        if "timed out" in normalized_message:
            return "La operación tardó demasiado. Verifique la conexión e inténtelo nuevamente."
        return error_message

    def _save_settings(self, settings: Settings) -> None:
        """Persist settings changed from the settings panel."""
        self._settings_manager.save(settings)
        self._settings = settings
        self._download_queue_service.update_max_concurrent_downloads(settings.max_concurrent_downloads)
        self._settings_widget.update_settings(settings)
        self._background_widget.set_background_image_path(settings.background_image_path)
        self._apply_background_state()
        self._toolbar_widget.set_download_preferences(
            settings.selected_format,
            settings.selected_quality,
        )
        self._toolbar_widget.set_playlist_preferences(
            settings.playlist_start_index,
            settings.playlist_end_index,
            settings.max_playlist_items,
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
        self._download_queue_service.cancel_all()
        for worker in self._playlist_workers.values():
            worker.cancel()
        updated_settings: Settings = self._settings.with_window_geometry(
            width=self.width(),
            height=self.height(),
            x_position=self.x(),
            y_position=self.y(),
        )
        self._settings_manager.save(updated_settings)
        self._persist_queue()
        self._settings = updated_settings
        super().closeEvent(event)

    @staticmethod
    def _should_log_playlist_progress(processed_count: int, total_count: int | None) -> bool:
        """Return whether playlist progress should be logged."""
        if processed_count <= 5:
            return True
        if total_count is not None and processed_count == total_count:
            return True
        return processed_count % 10 == 0

    @staticmethod
    def _should_log_playlist_item(processed_count: int, total_count: int | None) -> bool:
        """Return whether an added playlist item should be logged."""
        if processed_count <= 5:
            return True
        if total_count is not None and processed_count == total_count:
            return True
        return processed_count % 25 == 0

    def _effective_playlist_total(self, detected_total: int | None) -> int | None:
        """Return the total used for user-visible playlist progress."""
        if self._settings.max_playlist_items > 0:
            if detected_total is None:
                return self._settings.max_playlist_items
            return min(detected_total, self._settings.max_playlist_items)
        return detected_total

    def _queue_duplicate_keys(self) -> set[str]:
        """Return duplicate keys for current queue items."""
        return {item.duplicate_key() for item in self._queue_widget.all_download_items()}

    def _report_dependency_status(self) -> None:
        """Report dependency status without a permanent visual panel."""
        self._status_widget.update_dependency_status(self._dependency_result.all_available)
        if self._dependency_result.all_available:
            return
        missing_dependencies: list[str] = []
        if not self._dependency_result.yt_dlp.is_available:
            missing_dependencies.append("yt-dlp")
        if not self._dependency_result.ffmpeg.is_available:
            missing_dependencies.append("ffmpeg")
        self._log_widget.append_warning(
            (
                "Dependencias faltantes: "
                f"{', '.join(missing_dependencies)}. "
                "Ejecute install_dependencies.bat o instálelas manualmente con winget."
            )
        )

    def _apply_background_state(self) -> None:
        """Apply background-dependent panel styling."""
        background_active: bool = self._background_widget.has_background_image()
        for widget in (self._queue_widget, self._log_widget, self._settings_widget, self._side_panel):
            widget.setProperty("backgroundActive", background_active)
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()
