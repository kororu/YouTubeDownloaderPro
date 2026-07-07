"""QThread worker for incremental playlist loading."""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from models.playlist_metadata import PlaylistVideo
from services.playlist_stream_service import PlaylistStreamResult, PlaylistStreamService

PLAYLIST_BATCH_SIZE: int = 25


class PlaylistWorker(QThread):
    """Loads playlist and YouTube Mix entries outside the UI thread."""

    playlist_started: Signal = Signal(str, str)
    playlist_total_detected: Signal = Signal(str, int)
    playlist_limit_reached: Signal = Signal(str, int, int)
    playlist_batch_loaded: Signal = Signal(str, object, int, object)
    playlist_finished: Signal = Signal(str, int, bool)
    playlist_cancelled: Signal = Signal(str, int)
    playlist_failed: Signal = Signal(str, str)

    def __init__(
        self,
        request_id: str,
        source_url: str,
        max_items: int,
        playlist_service: PlaylistStreamService | None = None,
    ) -> None:
        """Initialize the playlist worker.

        Args:
            request_id: Stable request identifier.
            source_url: Source playlist URL.
            max_items: Maximum videos to process, or 0 for no configured limit.
            playlist_service: Playlist stream service instance.
        """
        super().__init__()
        self._request_id: str = request_id
        self._source_url: str = source_url
        self._max_items: int = max_items
        self._playlist_service: PlaylistStreamService = playlist_service or PlaylistStreamService()

    def run(self) -> None:
        """Load playlist entries incrementally and emit progress."""
        self.playlist_started.emit(self._request_id, self._source_url)
        try:
            result: PlaylistStreamResult = self._playlist_service.stream_playlist(
                self._source_url,
                self._max_items,
                PLAYLIST_BATCH_SIZE,
                self._emit_batch_loaded,
                self._emit_total_detected,
                self._emit_limit_reached,
            )
        except Exception as exc:
            self.playlist_failed.emit(self._request_id, str(exc))
            return
        if result.cancelled:
            self.playlist_cancelled.emit(self._request_id, result.processed_count)
            return
        self.playlist_finished.emit(self._request_id, result.processed_count, result.limit_reached)

    def cancel(self) -> None:
        """Cancel playlist loading."""
        self._playlist_service.cancel()

    def _emit_batch_loaded(
        self,
        videos: tuple[PlaylistVideo, ...],
        processed_count: int,
        total_count: int | None,
    ) -> None:
        """Emit a loaded playlist batch."""
        self.playlist_batch_loaded.emit(self._request_id, videos, processed_count, total_count)

    def _emit_total_detected(self, total_count: int) -> None:
        """Emit detected playlist total count."""
        self.playlist_total_detected.emit(self._request_id, total_count)

    def _emit_limit_reached(self, total_count: int, max_items: int) -> None:
        """Emit active playlist limit information."""
        self.playlist_limit_reached.emit(self._request_id, total_count, max_items)
