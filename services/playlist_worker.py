"""QThread worker for playlist metadata loading."""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from models.playlist_metadata import PlaylistMetadata
from services.playlist_metadata_service import PlaylistMetadataService


class PlaylistWorker(QThread):
    """Loads playlist metadata outside the UI thread."""

    playlist_loaded: Signal = Signal(str, object)
    playlist_failed: Signal = Signal(str, str)

    def __init__(
        self,
        request_id: str,
        source_url: str,
        playlist_service: PlaylistMetadataService | None = None,
    ) -> None:
        """Initialize the playlist worker.

        Args:
            request_id: Stable request identifier.
            source_url: Source playlist URL.
            playlist_service: Playlist metadata service instance.
        """
        super().__init__()
        self._request_id: str = request_id
        self._source_url: str = source_url
        self._playlist_service: PlaylistMetadataService = playlist_service or PlaylistMetadataService()

    def run(self) -> None:
        """Load playlist metadata and emit success or failure."""
        try:
            playlist: PlaylistMetadata = self._playlist_service.load_playlist(self._source_url)
        except Exception as exc:
            self.playlist_failed.emit(self._request_id, str(exc))
            return
        self.playlist_loaded.emit(self._request_id, playlist)
