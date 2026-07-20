"""Download queue orchestration service."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from models.download_enums import DownloadStatus
from models.download_item import DownloadItem
from models.download_progress import DownloadProgress
from services.download_worker import DownloadWorker


class DownloadQueueService(QObject):
    """Coordinates queued downloads and concurrent workers."""

    item_changed: Signal = Signal(object)
    progress_changed: Signal = Signal(str, object)
    download_completed: Signal = Signal(object, str)
    log_received: Signal = Signal(str, str)
    queue_finished: Signal = Signal()

    def __init__(self, max_concurrent_downloads: int = 3) -> None:
        """Initialize the download queue service.

        Args:
            max_concurrent_downloads: Maximum simultaneous downloads.
        """
        super().__init__()
        self._max_concurrent_downloads: int = max(1, min(3, max_concurrent_downloads))
        self._items: dict[str, DownloadItem] = {}
        self._pending_item_ids: list[str] = []
        self._workers: dict[str, DownloadWorker] = {}
        self._output_folder: Path | None = None

    def add_items(self, items: tuple[DownloadItem, ...]) -> None:
        """Add items to the queue service.

        Args:
            items: Download items to track.
        """
        for item in items:
            self._items[item.item_id] = item

    def start_downloads(self, item_ids: tuple[str, ...], output_folder: Path) -> None:
        """Queue selected items and start available worker slots.

        Args:
            item_ids: Item identifiers selected for download.
            output_folder: Destination folder.
        """
        self._output_folder = output_folder
        for item_id in item_ids:
            item: DownloadItem | None = self._items.get(item_id)
            if item is None or item_id in self._pending_item_ids or item_id in self._workers:
                continue
            queued_item: DownloadItem = item.with_status(DownloadStatus.QUEUED)
            self._items[item_id] = queued_item
            self._pending_item_ids.append(item_id)
            self.item_changed.emit(queued_item)
        self._start_next_workers()

    def cancel_current(self) -> None:
        """Cancel the first active download."""
        first_worker: DownloadWorker | None = next(iter(self._workers.values()), None)
        if first_worker is not None:
            first_worker.cancel()

    def cancel_all(self) -> None:
        """Cancel active and pending downloads."""
        pending_ids: tuple[str, ...] = tuple(self._pending_item_ids)
        self._pending_item_ids.clear()
        for item_id in pending_ids:
            self._update_item_status(item_id, DownloadStatus.CANCELLED)
        for worker in tuple(self._workers.values()):
            worker.cancel()

    def update_max_concurrent_downloads(self, max_concurrent_downloads: int) -> None:
        """Update concurrency limit.

        Args:
            max_concurrent_downloads: New maximum simultaneous downloads.
        """
        self._max_concurrent_downloads = max(1, min(3, max_concurrent_downloads))
        self._start_next_workers()

    def _start_next_workers(self) -> None:
        """Start workers until the concurrency limit is reached."""
        if self._output_folder is None:
            return
        while self._pending_item_ids and len(self._workers) < self._max_concurrent_downloads:
            item_id: str = self._pending_item_ids.pop(0)
            item: DownloadItem | None = self._items.get(item_id)
            if item is None:
                continue
            downloading_item: DownloadItem = item.with_status(DownloadStatus.DOWNLOADING)
            self._items[item_id] = downloading_item
            self.item_changed.emit(downloading_item)

            worker: DownloadWorker = DownloadWorker(downloading_item, self._output_folder)
            worker.progress_changed.connect(self._handle_progress_changed)
            worker.log_received.connect(self.log_received.emit)
            worker.download_completed.connect(self._handle_download_completed)
            worker.download_failed.connect(self._handle_download_failed)
            worker.download_cancelled.connect(self._handle_download_cancelled)
            worker.finished.connect(lambda completed_id=item_id: self._remove_worker(completed_id))
            self._workers[item_id] = worker
            worker.start()

    def _handle_progress_changed(self, item_id: str, progress: object) -> None:
        """Handle worker progress."""
        if not isinstance(progress, DownloadProgress):
            return
        item: DownloadItem | None = self._items.get(item_id)
        if item is None:
            return
        updated_item: DownloadItem = item.with_progress(progress.percentage)
        self._items[item_id] = updated_item
        self.item_changed.emit(updated_item)
        self.progress_changed.emit(item_id, progress)

    def _handle_download_completed(self, item_id: str, output_path: str) -> None:
        """Handle completed download."""
        self._update_item_status(item_id, DownloadStatus.COMPLETED)
        completed_item: DownloadItem | None = self._items.get(item_id)
        if completed_item is not None:
            self.download_completed.emit(completed_item, output_path)

    def _handle_download_failed(self, item_id: str, error_message: str) -> None:
        """Handle failed download."""
        item: DownloadItem | None = self._items.get(item_id)
        if item is None:
            return
        failed_item: DownloadItem = item.with_failure(error_message)
        self._items[item_id] = failed_item
        self.item_changed.emit(failed_item)

    def _handle_download_cancelled(self, item_id: str) -> None:
        """Handle cancelled download."""
        self._update_item_status(item_id, DownloadStatus.CANCELLED)

    def _remove_worker(self, item_id: str) -> None:
        """Remove finished worker and continue the queue."""
        worker: DownloadWorker | None = self._workers.pop(item_id, None)
        if worker is not None:
            worker.deleteLater()
        self._start_next_workers()
        if not self._workers and not self._pending_item_ids:
            self.queue_finished.emit()

    def _update_item_status(self, item_id: str, status: DownloadStatus) -> None:
        """Update an item status."""
        item: DownloadItem | None = self._items.get(item_id)
        if item is None:
            return
        updated_item: DownloadItem = item.with_status(status)
        self._items[item_id] = updated_item
        self.item_changed.emit(updated_item)
