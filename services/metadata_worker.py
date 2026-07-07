"""QThread worker for metadata loading."""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from models.video_metadata import VideoMetadata
from services.video_metadata_service import VideoMetadataService


class MetadataWorker(QThread):
    """Loads video metadata outside the UI thread."""

    metadata_loaded: Signal = Signal(str, object)
    metadata_failed: Signal = Signal(str, str)

    def __init__(
        self,
        item_id: str,
        source_url: str,
        metadata_service: VideoMetadataService | None = None,
    ) -> None:
        """Initialize the metadata worker.

        Args:
            item_id: Queue item identifier.
            source_url: Source video URL.
            metadata_service: Metadata service instance.
        """
        super().__init__()
        self._item_id: str = item_id
        self._source_url: str = source_url
        self._metadata_service: VideoMetadataService = metadata_service or VideoMetadataService()

    def run(self) -> None:
        """Load metadata and emit success or failure."""
        try:
            metadata: VideoMetadata = self._metadata_service.load_metadata(self._source_url)
        except Exception as exc:
            self.metadata_failed.emit(self._item_id, str(exc))
            return
        self.metadata_loaded.emit(self._item_id, metadata)
