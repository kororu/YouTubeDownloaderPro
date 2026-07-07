"""Queue item widget."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


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

    @classmethod
    def create(cls, source_url: str, media_format: str, quality: str) -> "QueueItemData":
        """Create queue item data for a submitted URL.

        Args:
            source_url: Source video or playlist URL.
            media_format: Selected output format.
            quality: Selected output quality.

        Returns:
            Queue item data with a stable generated identifier.
        """
        return cls(
            item_id=str(uuid4()),
            source_url=source_url,
            media_format=media_format,
            quality=quality,
            status="Pendiente",
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
        self.setObjectName("queueItemWidget")
        self._build_layout()

    @property
    def item_id(self) -> str:
        """Return the queue item identifier."""
        return self._item_data.item_id

    @property
    def source_url(self) -> str:
        """Return the queue item source URL."""
        return self._item_data.source_url

    def is_selected(self) -> bool:
        """Return whether the item is selected."""
        return self._checkbox.isChecked()

    def set_selected(self, selected: bool) -> None:
        """Set selected state.

        Args:
            selected: Whether the item should be selected.
        """
        self._checkbox.setChecked(selected)

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
            f"{self._item_data.status}"
        ).lower()
        return normalized_search in searchable_text

    def _build_layout(self) -> None:
        """Build the queue item layout."""
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        self._checkbox = QCheckBox(self)
        self._checkbox.toggled.connect(self._emit_selection_changed)

        text_layout: QVBoxLayout = QVBoxLayout()
        text_layout.setSpacing(4)

        url_label: QLabel = QLabel(self._item_data.source_url, self)
        url_label.setObjectName("queueItemUrl")
        url_label.setWordWrap(True)

        metadata_label: QLabel = QLabel(
            (
                f"Formato: {self._item_data.media_format.upper()} | "
                f"Calidad: {self._item_data.quality} | "
                f"Estado: {self._item_data.status}"
            ),
            self,
        )
        metadata_label.setObjectName("queueItemMetadata")

        text_layout.addWidget(url_label)
        text_layout.addWidget(metadata_label)

        remove_button: QPushButton = QPushButton("Quitar", self)
        remove_button.clicked.connect(self._emit_remove_requested)

        layout.addWidget(self._checkbox)
        layout.addLayout(text_layout, 1)
        layout.addWidget(remove_button)

    def _emit_selection_changed(self, selected: bool) -> None:
        """Emit item selection state."""
        self.selection_changed.emit(self.item_id, selected)

    def _emit_remove_requested(self) -> None:
        """Emit item removal request."""
        self.remove_requested.emit(self.item_id)
