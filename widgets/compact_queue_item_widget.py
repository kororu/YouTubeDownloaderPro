"""Compact list row renderer for download queue items."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton, QWidget

from widgets.queue_item_widget import QueueItemData


class CompactQueueItemWidget(QFrame):
    """One compact queue row rendered from shared queue item data."""

    selection_changed: Signal = Signal(str, bool)
    remove_requested: Signal = Signal(str)

    def __init__(self, item_data: QueueItemData, parent: QWidget | None = None) -> None:
        """Initialize a compact row.

        Args:
            item_data: Shared queue item display data.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._item_data = item_data
        self._checkbox: QCheckBox
        self._title_label: QLabel
        self._format_label: QLabel
        self._quality_label: QLabel
        self._status_label: QLabel
        self._progress_bar: QProgressBar
        self._percentage_label: QLabel
        self.setObjectName("compactQueueItemWidget")
        self._build_layout()

    @property
    def item_id(self) -> str:
        """Return the stable queue item identifier."""
        return self._item_data.item_id

    def set_selected(self, selected: bool) -> None:
        """Synchronize the row selection state."""
        self._checkbox.setChecked(selected)

    def update_item(self, item_data: QueueItemData) -> None:
        """Update row contents from the shared queue data."""
        self._item_data = item_data
        self._refresh()

    def _build_layout(self) -> None:
        """Build the compact row columns."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        self._checkbox = QCheckBox(self)
        self._checkbox.setFixedWidth(24)
        self._checkbox.toggled.connect(self._emit_selection_changed)

        self._title_label = QLabel(self)
        self._title_label.setObjectName("compactQueueTitle")
        self._title_label.setMinimumWidth(220)

        self._format_label = QLabel(self)
        self._format_label.setFixedWidth(62)
        self._quality_label = QLabel(self)
        self._quality_label.setFixedWidth(66)
        self._status_label = QLabel(self)
        self._status_label.setFixedWidth(132)

        self._progress_bar = QProgressBar(self)
        self._progress_bar.setObjectName("compactQueueProgressBar")
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setMinimumWidth(120)

        self._percentage_label = QLabel(self)
        self._percentage_label.setFixedWidth(42)

        remove_button = QPushButton("Quitar", self)
        remove_button.setObjectName("compactQueueRemoveButton")
        remove_button.setFixedWidth(62)
        remove_button.clicked.connect(lambda: self.remove_requested.emit(self.item_id))

        layout.addWidget(self._checkbox)
        layout.addWidget(self._title_label, 1)
        layout.addWidget(self._format_label)
        layout.addWidget(self._quality_label)
        layout.addWidget(self._status_label)
        layout.addWidget(self._progress_bar, 1)
        layout.addWidget(self._percentage_label)
        layout.addWidget(remove_button)
        self._refresh()

    def _refresh(self) -> None:
        """Refresh row labels, progress, and tooltips."""
        title = self._item_data.title or "Cargando metadatos..."
        self._title_label.setText(title)
        self._title_label.setToolTip(self._item_data.source_url)
        self._format_label.setText(self._item_data.media_format.upper())
        self._quality_label.setText(self._item_data.quality)
        self._status_label.setText(self._item_data.status)
        self._status_label.setToolTip(self._item_data.error_message or self._item_data.status)
        percentage = 100 if self._item_data.status == "Ya descargado" else round(self._item_data.progress_percentage)
        if self._item_data.status == "Cargando metadatos":
            self._progress_bar.setRange(0, 0)
            self._percentage_label.setText("...")
        else:
            self._progress_bar.setRange(0, 100)
            self._progress_bar.setValue(percentage)
            self._percentage_label.setText(f"{percentage}%")
        self._progress_bar.setProperty("downloadState", self._item_data.status)
        self._progress_bar.style().unpolish(self._progress_bar)
        self._progress_bar.style().polish(self._progress_bar)

    def _emit_selection_changed(self, selected: bool) -> None:
        """Emit selection updates for synchronization with the card renderer."""
        self.selection_changed.emit(self.item_id, selected)
