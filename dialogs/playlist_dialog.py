"""Playlist video selection dialog."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models.playlist_metadata import PlaylistMetadata, PlaylistVideo

VIDEO_ROLE: int = int(Qt.ItemDataRole.UserRole)


class PlaylistDialog(QDialog):
    """Dialog for selecting videos from a playlist."""

    def __init__(self, playlist: PlaylistMetadata, parent: QWidget | None = None) -> None:
        """Initialize the playlist dialog.

        Args:
            playlist: Playlist metadata to display.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._playlist: PlaylistMetadata = playlist
        self._search_input: QLineEdit
        self._video_list_widget: QListWidget
        self._selection_label: QLabel
        self.setObjectName("playlistDialog")
        self.setWindowTitle("Seleccionar videos de playlist")
        self.setModal(True)
        self.resize(900, 640)
        self.setMinimumSize(760, 520)
        self._build_layout()
        self._populate_videos()
        self._update_selection_label()

    def selected_videos(self) -> tuple[PlaylistVideo, ...]:
        """Return selected playlist videos.

        Returns:
            Tuple of selected playlist videos.
        """
        selected_videos: list[PlaylistVideo] = []
        for index in range(self._video_list_widget.count()):
            item: QListWidgetItem = self._video_list_widget.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                video: object = item.data(VIDEO_ROLE)
                if isinstance(video, PlaylistVideo):
                    selected_videos.append(video)
        return tuple(selected_videos)

    def _build_layout(self) -> None:
        """Build dialog layout."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title_label: QLabel = QLabel(self._playlist.title, self)
        title_label.setObjectName("playlistTitle")
        title_label.setWordWrap(True)

        metadata_label: QLabel = QLabel(
            f"Videos disponibles: {len(self._playlist.videos)}",
            self,
        )
        metadata_label.setObjectName("playlistMetadata")

        toolbar_layout: QHBoxLayout = QHBoxLayout()
        self._search_input = QLineEdit(self)
        self._search_input.setClearButtonEnabled(True)
        self._search_input.setToolTip("Buscar videos en la playlist")
        self._search_input.textChanged.connect(self._filter_videos)

        select_all_button: QPushButton = QPushButton("Seleccionar todo", self)
        select_all_button.clicked.connect(self._select_all_visible)

        deselect_all_button: QPushButton = QPushButton("Deseleccionar", self)
        deselect_all_button.clicked.connect(self._deselect_all)

        toolbar_layout.addWidget(self._search_input, 1)
        toolbar_layout.addWidget(select_all_button)
        toolbar_layout.addWidget(deselect_all_button)

        self._video_list_widget = QListWidget(self)
        self._video_list_widget.setObjectName("playlistVideoList")
        self._video_list_widget.itemChanged.connect(self._update_selection_label)

        footer_layout: QHBoxLayout = QHBoxLayout()
        self._selection_label = QLabel(self)

        add_button: QPushButton = QPushButton("Agregar seleccionados", self)
        add_button.clicked.connect(self.accept)

        cancel_button: QPushButton = QPushButton("Cancelar", self)
        cancel_button.clicked.connect(self.reject)

        footer_layout.addWidget(self._selection_label)
        footer_layout.addStretch(1)
        footer_layout.addWidget(cancel_button)
        footer_layout.addWidget(add_button)

        layout.addWidget(title_label)
        layout.addWidget(metadata_label)
        layout.addLayout(toolbar_layout)
        layout.addWidget(self._video_list_widget, 1)
        layout.addLayout(footer_layout)

    def _populate_videos(self) -> None:
        """Populate the list with playlist videos."""
        for video in self._playlist.videos:
            item: QListWidgetItem = QListWidgetItem(self._format_video_label(video))
            item.setData(VIDEO_ROLE, video)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self._video_list_widget.addItem(item)

    def _filter_videos(self, search_text: str) -> None:
        """Filter videos by search text."""
        normalized_search: str = search_text.strip().lower()
        for index in range(self._video_list_widget.count()):
            item: QListWidgetItem = self._video_list_widget.item(index)
            video: object = item.data(VIDEO_ROLE)
            if not isinstance(video, PlaylistVideo):
                item.setHidden(True)
                continue
            searchable_text: str = f"{video.title} {video.uploader or ''} {video.source_url}".lower()
            item.setHidden(bool(normalized_search) and normalized_search not in searchable_text)

    def _select_all_visible(self) -> None:
        """Select all currently visible videos."""
        for index in range(self._video_list_widget.count()):
            item: QListWidgetItem = self._video_list_widget.item(index)
            if not item.isHidden():
                item.setCheckState(Qt.CheckState.Checked)
        self._update_selection_label()

    def _deselect_all(self) -> None:
        """Deselect all videos."""
        for index in range(self._video_list_widget.count()):
            item: QListWidgetItem = self._video_list_widget.item(index)
            item.setCheckState(Qt.CheckState.Unchecked)
        self._update_selection_label()

    def _update_selection_label(self) -> None:
        """Update selected video count."""
        selected_count: int = len(self.selected_videos())
        total_count: int = self._video_list_widget.count()
        self._selection_label.setText(f"Seleccionados: {selected_count} de {total_count}")

    @staticmethod
    def _format_video_label(video: PlaylistVideo) -> str:
        """Format playlist video list text."""
        duration_text: str = _format_duration(video.duration_seconds)
        uploader_text: str = f" | {video.uploader}" if video.uploader else ""
        return f"{video.index}. {video.title}{uploader_text} | {duration_text}"


def _format_duration(duration_seconds: int | None) -> str:
    """Format optional duration in H:MM:SS or M:SS."""
    if duration_seconds is None:
        return "Duración no disponible"
    hours, remainder = divmod(duration_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"
