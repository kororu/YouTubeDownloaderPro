"""Queue display widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class QueueWidget(QWidget):
    """Scrollable queue area based on QScrollArea."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the queue widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("queueWidget")
        self._items_container: QWidget = QWidget(self)
        self._items_layout: QVBoxLayout = QVBoxLayout(self._items_container)
        self._build_layout()

    def _build_layout(self) -> None:
        """Build the queue layout."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header_layout: QHBoxLayout = QHBoxLayout()
        title_label: QLabel = QLabel("Cola de descargas", self)
        title_label.setObjectName("sectionTitle")

        search_input: QLineEdit = QLineEdit(self)
        search_input.setObjectName("queueSearchInput")
        search_input.setClearButtonEnabled(True)
        search_input.setFixedWidth(320)

        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(search_input)

        scroll_area: QScrollArea = QScrollArea(self)
        scroll_area.setObjectName("queueScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self._items_container.setObjectName("queueItemsContainer")
        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(8)

        empty_state: QLabel = QLabel("No hay elementos en cola.", self._items_container)
        empty_state.setObjectName("emptyQueueLabel")
        empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_state.setMinimumHeight(220)
        self._items_layout.addWidget(empty_state)
        self._items_layout.addStretch(1)

        scroll_area.setWidget(self._items_container)

        layout.addLayout(header_layout)
        layout.addWidget(scroll_area, 1)
