"""Queue display widget."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from widgets.queue_item_widget import QueueItemData, QueueItemWidget


class QueueWidget(QWidget):
    """Scrollable queue area based on QScrollArea."""

    queue_changed: Signal = Signal(int, int)

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the queue widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("queueWidget")
        self._items_container: QWidget = QWidget(self)
        self._items_layout: QVBoxLayout = QVBoxLayout(self._items_container)
        self._items: list[QueueItemWidget] = []
        self._item_order: dict[str, int] = {}
        self._empty_state: QLabel
        self._search_input: QLineEdit
        self._sort_combo_box: QComboBox
        self._build_layout()

    def add_item(self, source_url: str, media_format: str, quality: str) -> None:
        """Add a URL to the visible queue.

        Args:
            source_url: Source video or playlist URL.
            media_format: Selected output format.
            quality: Selected output quality.
        """
        item_data: QueueItemData = QueueItemData.create(source_url, media_format, quality)
        item_widget: QueueItemWidget = QueueItemWidget(item_data, self._items_container)
        item_widget.selection_changed.connect(self._emit_queue_changed)
        item_widget.remove_requested.connect(self.remove_item)

        insert_index: int = max(0, self._items_layout.count() - 1)
        self._items.append(item_widget)
        self._item_order[item_widget.item_id] = len(self._item_order)
        self._items_layout.insertWidget(insert_index, item_widget)
        self._apply_sorting()
        self._apply_filter()
        self._emit_queue_changed()

    def remove_item(self, item_id: str) -> None:
        """Remove an item by identifier.

        Args:
            item_id: Queue item identifier.
        """
        item_widget: QueueItemWidget | None = self._find_item(item_id)
        if item_widget is None:
            return

        self._items.remove(item_widget)
        self._item_order.pop(item_widget.item_id, None)
        self._items_layout.removeWidget(item_widget)
        item_widget.deleteLater()
        self._apply_filter()
        self._emit_queue_changed()

    def remove_selected_items(self) -> None:
        """Remove every selected queue item."""
        selected_items: list[QueueItemWidget] = [item for item in self._items if item.is_selected()]
        for item_widget in selected_items:
            self.remove_item(item_widget.item_id)

    def select_all_items(self) -> None:
        """Select all queue items."""
        for item_widget in self._items:
            item_widget.set_selected(True)
        self._emit_queue_changed()

    def deselect_all_items(self) -> None:
        """Deselect all queue items."""
        for item_widget in self._items:
            item_widget.set_selected(False)
        self._emit_queue_changed()

    def item_count(self) -> int:
        """Return total queue item count."""
        return len(self._items)

    def selected_count(self) -> int:
        """Return selected queue item count."""
        return sum(1 for item in self._items if item.is_selected())

    def _build_layout(self) -> None:
        """Build the queue layout."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header_layout: QHBoxLayout = QHBoxLayout()
        title_label: QLabel = QLabel("Cola de descargas", self)
        title_label.setObjectName("sectionTitle")

        select_all_button: QPushButton = QPushButton("Seleccionar todo", self)
        select_all_button.clicked.connect(self.select_all_items)

        deselect_all_button: QPushButton = QPushButton("Deseleccionar", self)
        deselect_all_button.clicked.connect(self.deselect_all_items)

        remove_selected_button: QPushButton = QPushButton("Quitar seleccionados", self)
        remove_selected_button.clicked.connect(self.remove_selected_items)

        self._sort_combo_box = QComboBox(self)
        self._sort_combo_box.setObjectName("queueSortComboBox")
        self._sort_combo_box.addItems(("Orden de ingreso", "URL A-Z", "URL Z-A"))
        self._sort_combo_box.currentIndexChanged.connect(self._apply_sorting)

        self._search_input = QLineEdit(self)
        self._search_input.setObjectName("queueSearchInput")
        self._search_input.setClearButtonEnabled(True)
        self._search_input.setFixedWidth(320)
        self._search_input.setToolTip("Buscar en la cola")
        self._search_input.textChanged.connect(self._apply_filter)

        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(select_all_button)
        header_layout.addWidget(deselect_all_button)
        header_layout.addWidget(remove_selected_button)
        header_layout.addWidget(self._sort_combo_box)
        header_layout.addWidget(self._search_input)

        scroll_area: QScrollArea = QScrollArea(self)
        scroll_area.setObjectName("queueScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self._items_container.setObjectName("queueItemsContainer")
        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(8)

        self._empty_state = QLabel("No hay elementos en cola.", self._items_container)
        self._empty_state.setObjectName("emptyQueueLabel")
        self._empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_state.setMinimumHeight(220)
        self._items_layout.addWidget(self._empty_state)
        self._items_layout.addStretch(1)

        scroll_area.setWidget(self._items_container)

        layout.addLayout(header_layout)
        layout.addWidget(scroll_area, 1)

    def _find_item(self, item_id: str) -> QueueItemWidget | None:
        """Find a queue item by identifier."""
        for item_widget in self._items:
            if item_widget.item_id == item_id:
                return item_widget
        return None

    def _apply_filter(self) -> None:
        """Filter queue items by search text."""
        search_text: str = self._search_input.text()
        visible_count: int = 0
        for item_widget in self._items:
            is_visible: bool = item_widget.matches_search(search_text)
            item_widget.setVisible(is_visible)
            if is_visible:
                visible_count += 1
        self._empty_state.setVisible(visible_count == 0)

    def _apply_sorting(self) -> None:
        """Apply selected visual sort order."""
        sort_mode: str = self._sort_combo_box.currentText()
        if sort_mode == "Orden de ingreso":
            self._items.sort(key=lambda item: self._item_order[item.item_id])
        elif sort_mode == "URL A-Z":
            self._items.sort(key=lambda item: item.source_url.lower())
        elif sort_mode == "URL Z-A":
            self._items.sort(key=lambda item: item.source_url.lower(), reverse=True)

        for item_widget in self._items:
            self._items_layout.removeWidget(item_widget)

        for index, item_widget in enumerate(self._items):
            self._items_layout.insertWidget(index, item_widget)

        self._apply_filter()

    def _emit_queue_changed(self) -> None:
        """Emit current queue counts."""
        self.queue_changed.emit(self.item_count(), self.selected_count())
