"""Queue item widget."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget

from models.download_enums import DownloadStatus
from models.download_item import DownloadItem


@dataclass(frozen=True, slots=True)
class QueueItemData:
    """Display data for a queue item.

    Attributes:
        item_id: Stable queue item identifier.
        source_url: Source video or playlist URL.
        media_format: Selected output format.
        quality: Selected output quality.
        status: Current item status text.
    """

    item_id: str
    source_url: str
    media_format: str
    quality: str
    status: str
    title: str | None = None
    uploader: str | None = None
    error_message: str | None = None
    progress_percentage: float = 0.0
    playlist_index: int | None = None
    playlist_title: str | None = None
    playlist_source_url: str | None = None
    is_youtube_mix: bool = False
    video_id: str | None = None
    audio_quality: str = "best"
    download_thumbnail: bool = False
    write_metadata: bool = False
    write_subtitles: bool = False
    write_auto_subtitles: bool = False
    subtitle_languages: str = "es,en"
    filename_template: str = "%(title)s.%(ext)s"
    create_channel_folder: bool = False
    create_playlist_folder: bool = False

    @classmethod
    def from_download_item(cls, download_item: DownloadItem) -> "QueueItemData":
        """Create queue item data from a domain model.

        Args:
            download_item: Domain queue item.

        Returns:
            Queue item display data.
        """
        metadata_title: str | None = None
        metadata_uploader: str | None = None
        if download_item.metadata is not None:
            metadata_title = download_item.metadata.title
            metadata_uploader = download_item.metadata.uploader

        return cls(
            item_id=download_item.item_id,
            source_url=download_item.source_url,
            media_format=download_item.media_format.value,
            quality=download_item.quality.value,
            status=_translate_status(download_item.status),
            title=metadata_title,
            uploader=metadata_uploader,
            error_message=download_item.error_message,
            progress_percentage=download_item.progress_percentage,
            playlist_index=download_item.playlist_index,
            playlist_title=download_item.playlist_title,
            playlist_source_url=download_item.playlist_source_url,
            is_youtube_mix=download_item.is_youtube_mix,
            video_id=download_item.video_id,
            audio_quality=download_item.audio_quality.value,
            download_thumbnail=download_item.download_thumbnail,
            write_metadata=download_item.write_metadata,
            write_subtitles=download_item.write_subtitles,
            write_auto_subtitles=download_item.write_auto_subtitles,
            subtitle_languages=download_item.subtitle_languages,
            filename_template=download_item.filename_template,
            create_channel_folder=download_item.create_channel_folder,
            create_playlist_folder=download_item.create_playlist_folder,
        )


class QueueItemWidget(QFrame):
    """Visual representation of a single queue item."""

    selection_changed: Signal = Signal(str, bool)
    remove_requested: Signal = Signal(str)

    def __init__(self, item_data: QueueItemData, parent: QWidget | None = None) -> None:
        """Initialize the queue item widget.

        Args:
            item_data: Item data to render.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._item_data: QueueItemData = item_data
        self._checkbox: QCheckBox
        self._title_label: QLabel
        self._url_label: QLabel
        self._metadata_label: QLabel
        self._progress_label: QLabel
        self._progress_bar: QProgressBar
        self._error_label: QLabel
        self._layout: QHBoxLayout
        self.setObjectName("queueItemWidget")
        self.setProperty("compact", False)
        self._build_layout()

    @property
    def item_id(self) -> str:
        """Return the queue item identifier."""
        return self._item_data.item_id

    @property
    def source_url(self) -> str:
        """Return the queue item source URL."""
        return self._item_data.source_url

    @property
    def media_format(self) -> str:
        """Return the selected media format."""
        return self._item_data.media_format

    @property
    def quality(self) -> str:
        """Return the selected quality."""
        return self._item_data.quality

    def to_download_item(self) -> DownloadItem:
        """Return the current display data as a download item."""
        from models.download_enums import AudioQuality, DownloadFormat, DownloadQuality
        from models.video_metadata import VideoMetadata

        metadata: VideoMetadata | None = None
        if self._item_data.title is not None:
            metadata = VideoMetadata(
                source_url=self._item_data.source_url,
                title=self._item_data.title,
                duration_seconds=None,
                uploader=self._item_data.uploader,
                thumbnail_url=None,
                webpage_url=self._item_data.source_url,
            )

        return DownloadItem(
            item_id=self._item_data.item_id,
            source_url=self._item_data.source_url,
            media_format=DownloadFormat(self._item_data.media_format),
            quality=DownloadQuality(self._item_data.quality),
            status=_status_from_label(self._item_data.status),
            metadata=metadata,
            error_message=self._item_data.error_message,
            progress_percentage=self._item_data.progress_percentage,
            playlist_index=self._item_data.playlist_index,
            playlist_title=self._item_data.playlist_title,
            playlist_source_url=self._item_data.playlist_source_url,
            is_youtube_mix=self._item_data.is_youtube_mix,
            video_id=self._item_data.video_id,
            audio_quality=AudioQuality(self._item_data.audio_quality),
            download_thumbnail=self._item_data.download_thumbnail,
            write_metadata=self._item_data.write_metadata,
            write_subtitles=self._item_data.write_subtitles,
            write_auto_subtitles=self._item_data.write_auto_subtitles,
            subtitle_languages=self._item_data.subtitle_languages,
            filename_template=self._item_data.filename_template,
            create_channel_folder=self._item_data.create_channel_folder,
            create_playlist_folder=self._item_data.create_playlist_folder,
        )

    def is_selected(self) -> bool:
        """Return whether the item is selected."""
        return self._checkbox.isChecked()

    def set_selected(self, selected: bool) -> None:
        """Set selected state.

        Args:
            selected: Whether the item should be selected.
        """
        self._checkbox.setChecked(selected)

    def set_compact_mode(self, compact_mode: bool) -> None:
        """Apply the selected density without changing item contents."""
        self.setProperty("compact", compact_mode)
        if compact_mode:
            self._layout.setContentsMargins(10, 7, 10, 7)
        else:
            self._layout.setContentsMargins(14, 12, 14, 12)
        self._layout.setSpacing(9 if compact_mode else 14)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def matches_search(self, search_text: str) -> bool:
        """Return whether the item matches a search term.

        Args:
            search_text: Search text entered by the user.

        Returns:
            True when the item should remain visible.
        """
        normalized_search: str = search_text.strip().lower()
        if not normalized_search:
            return True
        searchable_text: str = (
            f"{self._item_data.source_url} "
            f"{self._item_data.media_format} "
            f"{self._item_data.quality} "
            f"{self._item_data.status} "
            f"{self._item_data.title or ''} "
            f"{self._item_data.uploader or ''} "
            f"{self._item_data.playlist_title or ''} "
            f"{self._item_data.playlist_index or ''}"
        ).lower()
        return normalized_search in searchable_text

    def update_item(self, item_data: QueueItemData) -> None:
        """Update the displayed item data.

        Args:
            item_data: Updated item data.
        """
        self._item_data = item_data
        self._refresh_labels()

    def _build_layout(self) -> None:
        """Build the queue item layout."""
        layout: QHBoxLayout = QHBoxLayout(self)
        self._layout = layout
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(14)

        self._checkbox = QCheckBox(self)
        self._checkbox.toggled.connect(self._emit_selection_changed)

        text_layout: QVBoxLayout = QVBoxLayout()
        text_layout.setSpacing(4)

        self._title_label = QLabel(self)
        self._title_label.setObjectName("queueItemTitle")
        self._title_label.setWordWrap(True)

        self._url_label = QLabel(self)
        self._url_label.setObjectName("queueItemUrl")
        self._url_label.setWordWrap(True)

        self._metadata_label = QLabel(self)
        self._metadata_label.setObjectName("queueItemMetadata")

        self._progress_label = QLabel(self)
        self._progress_label.setObjectName("queueItemProgress")

        self._progress_bar = QProgressBar(self)
        self._progress_bar.setObjectName("queueItemProgressBar")
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setTextVisible(True)

        self._error_label = QLabel(self)
        self._error_label.setObjectName("queueItemError")
        self._error_label.setWordWrap(True)

        text_layout.addWidget(self._title_label)
        text_layout.addWidget(self._url_label)
        text_layout.addWidget(self._metadata_label)
        text_layout.addWidget(self._progress_label)
        text_layout.addWidget(self._progress_bar)
        text_layout.addWidget(self._error_label)

        remove_button: QPushButton = QPushButton("Quitar", self)
        remove_button.setToolTip("Quita este elemento de la cola.")
        remove_button.setMinimumWidth(78)
        remove_button.clicked.connect(self._emit_remove_requested)

        layout.addWidget(self._checkbox)
        layout.addLayout(text_layout, 1)
        layout.addWidget(remove_button)
        self._refresh_labels()

    def _emit_selection_changed(self, selected: bool) -> None:
        """Emit item selection state."""
        self.selection_changed.emit(self.item_id, selected)

    def _emit_remove_requested(self) -> None:
        """Emit item removal request."""
        self.remove_requested.emit(self.item_id)

    def _refresh_labels(self) -> None:
        """Refresh displayed labels from current item data."""
        display_title: str = self._item_data.title or "Cargando metadatos..."
        self._title_label.setText(display_title)
        self._url_label.setText(self._item_data.source_url)
        metadata_parts: list[str] = [
            f"Formato: {self._item_data.media_format.upper()}",
            (
                f"Calidad audio: {self._item_data.audio_quality} kbps"
                if self._item_data.media_format == "mp3" and self._item_data.audio_quality != "best"
                else f"Calidad: {self._item_data.quality}"
            ),
            f"Estado: {self._item_data.status}",
        ]
        if self._item_data.playlist_index is not None:
            origin_label: str = "Mix" if self._item_data.is_youtube_mix else "Playlist"
            metadata_parts.append(f"{origin_label}: #{self._item_data.playlist_index}")
        if self._item_data.status == "Ya descargado":
            metadata_parts.append("Descargado")
        self._metadata_label.setText(" | ".join(metadata_parts))
        status: str = self._item_data.status
        if status == "Cargando metadatos":
            self._progress_bar.setRange(0, 0)
            self._progress_label.setText("Cargando metadata...")
        else:
            self._progress_bar.setRange(0, 100)
            percentage: int = 100 if status == "Ya descargado" else round(self._item_data.progress_percentage)
            self._progress_bar.setValue(percentage)
            self._progress_label.setText(f"Progreso: {percentage}%")
        self._progress_bar.setProperty("downloadState", status)
        self._progress_bar.style().unpolish(self._progress_bar)
        self._progress_bar.style().polish(self._progress_bar)
        error_message: str = self._item_data.error_message or ""
        self._error_label.setText(error_message)
        self._error_label.setVisible(bool(error_message))


def _translate_status(status: DownloadStatus) -> str:
    """Translate a domain status to display text."""
    status_labels: dict[DownloadStatus, str] = {
        DownloadStatus.PENDING: "Pendiente",
        DownloadStatus.LOADING_METADATA: "Cargando metadatos",
        DownloadStatus.READY: "Listo",
        DownloadStatus.QUEUED: "En cola",
        DownloadStatus.DOWNLOADING: "Descargando",
        DownloadStatus.COMPLETED: "Ya descargado",
        DownloadStatus.CANCELLED: "Cancelado",
        DownloadStatus.FAILED: "Error",
    }
    return status_labels[status]


def _status_from_label(status_label: str) -> DownloadStatus:
    """Convert display status text to a domain status."""
    status_values: dict[str, DownloadStatus] = {
        "Pendiente": DownloadStatus.PENDING,
        "Cargando metadatos": DownloadStatus.LOADING_METADATA,
        "Listo": DownloadStatus.READY,
        "En cola": DownloadStatus.QUEUED,
        "Descargando": DownloadStatus.DOWNLOADING,
        "Ya descargado": DownloadStatus.COMPLETED,
        "Completado": DownloadStatus.COMPLETED,
        "Cancelado": DownloadStatus.CANCELLED,
        "Error": DownloadStatus.FAILED,
    }
    return status_values.get(status_label, DownloadStatus.PENDING)
