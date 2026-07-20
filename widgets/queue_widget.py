"""Queue display widget."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from models.download_enums import DownloadFormat, DownloadQuality, DownloadStatus
from widgets.queue_item_widget import QueueItemData, QueueItemWidget
from widgets.compact_queue_item_widget import CompactQueueItemWidget
from models.download_item import DownloadItem
from models.video_metadata import VideoMetadata


class QueueWidget(QWidget):
    """Scrollable queue area based on QScrollArea."""

    queue_changed: Signal = Signal(int, int)
    item_removed: Signal = Signal(str)
    view_mode_changed: Signal = Signal(str)

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
        self._compact_items: dict[str, CompactQueueItemWidget] = {}
        self._item_order: dict[str, int] = {}
        self._empty_state: QLabel
        self._search_text: str = ""
        self._sort_mode: str = "Orden de ingreso"
        self._compact_mode: bool = False
        self._view_mode: str = "cards"
        self._list_container: QWidget = QWidget(self)
        self._list_layout: QVBoxLayout = QVBoxLayout(self._list_container)
        self._view_stack: QStackedWidget
        self._cards_view_button: QPushButton
        self._list_view_button: QPushButton
        self._build_layout()

    def add_download_item(self, download_item: DownloadItem) -> None:
        """Add a domain item to the visible queue.

        Args:
            download_item: Domain queue item.
        """
        self.add_download_items((download_item,))

    def add_download_items(self, download_items: tuple[DownloadItem, ...]) -> None:
        """Add domain items to the visible queue in a single UI update.

        Args:
            download_items: Domain queue items.
        """
        if not download_items:
            return

        self.setUpdatesEnabled(False)
        try:
            for download_item in download_items:
                item_widget: QueueItemWidget = self._create_item_widget(download_item)
                insert_index: int = max(0, self._items_layout.count() - 1)
                self._items.append(item_widget)
                self._item_order[item_widget.item_id] = len(self._item_order)
                self._items_layout.insertWidget(insert_index, item_widget)
                self._add_compact_item(item_widget)
            self._apply_sorting()
            self._apply_filter()
        finally:
            self.setUpdatesEnabled(True)
        self._emit_queue_changed()

    def _create_item_widget(self, download_item: DownloadItem) -> QueueItemWidget:
        """Create a configured queue item widget."""
        item_data: QueueItemData = QueueItemData.from_download_item(download_item)
        item_widget: QueueItemWidget = QueueItemWidget(item_data, self._items_container)
        item_widget.selection_changed.connect(self._handle_card_selection)
        item_widget.remove_requested.connect(self.remove_item)
        item_widget.set_compact_mode(self._compact_mode)
        return item_widget

    def _add_compact_item(self, item_widget: QueueItemWidget) -> None:
        """Create the compact renderer for one canonical card item."""
        compact_item = CompactQueueItemWidget(
            QueueItemData.from_download_item(item_widget.to_download_item()),
            self._list_container,
        )
        compact_item.selection_changed.connect(self._sync_compact_selection)
        compact_item.remove_requested.connect(self.remove_item)
        self._compact_items[item_widget.item_id] = compact_item
        self._list_layout.insertWidget(max(1, self._list_layout.count() - 1), compact_item)

    def add_item(self, source_url: str, media_format: str, quality: str) -> None:
        """Add a URL to the visible queue.

        Args:
            source_url: Source video or playlist URL.
            media_format: Selected output format.
            quality: Selected output quality.
        """
        download_item: DownloadItem = DownloadItem.create(
            source_url=source_url,
            media_format=DownloadFormat(media_format),
            quality=DownloadQuality(quality),
        )
        self.add_download_item(download_item)

    def update_item_metadata(self, item_id: str, metadata: VideoMetadata) -> None:
        """Update queue item metadata.

        Args:
            item_id: Queue item identifier.
            metadata: Loaded video metadata.
        """
        item_widget: QueueItemWidget | None = self._find_item(item_id)
        if item_widget is None:
            return

        updated_item: DownloadItem = item_widget.to_download_item().with_metadata(metadata)
        item_widget.update_item(QueueItemData.from_download_item(updated_item))
        self._update_compact_item(item_widget)
        self._apply_filter()

    def update_download_item(self, download_item: DownloadItem) -> None:
        """Update a queue item from a domain item.

        Args:
            download_item: Updated domain item.
        """
        item_widget: QueueItemWidget | None = self._find_item(download_item.item_id)
        if item_widget is None:
            return
        item_widget.update_item(QueueItemData.from_download_item(download_item))
        self._update_compact_item(item_widget)
        self._apply_filter()

    def mark_item_failed(self, item_id: str, error_message: str) -> None:
        """Mark a queue item as failed.

        Args:
            item_id: Queue item identifier.
            error_message: Failure message.
        """
        item_widget: QueueItemWidget | None = self._find_item(item_id)
        if item_widget is None:
            return

        failed_item: DownloadItem = item_widget.to_download_item().with_failure(error_message)
        item_widget.update_item(QueueItemData.from_download_item(failed_item))
        self._update_compact_item(item_widget)
        self._apply_filter()

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
        compact_item = self._compact_items.pop(item_id, None)
        if compact_item is not None:
            self._list_layout.removeWidget(compact_item)
            compact_item.deleteLater()
        item_widget.deleteLater()
        self._apply_filter()
        self._emit_queue_changed()
        self.item_removed.emit(item_id)

    def remove_selected_items(self) -> None:
        """Remove every selected queue item."""
        selected_items: list[QueueItemWidget] = [item for item in self._items if item.is_selected()]
        for item_widget in selected_items:
            self.remove_item(item_widget.item_id)

    def select_all_items(self) -> None:
        """Select all queue items."""
        for item_widget in self._items:
            item_widget.set_selected(True)
        self._sync_compact_selections()
        self._emit_queue_changed()

    def deselect_all_items(self) -> None:
        """Deselect all queue items."""
        for item_widget in self._items:
            item_widget.set_selected(False)
        self._sync_compact_selections()
        self._emit_queue_changed()

    def item_count(self) -> int:
        """Return total queue item count."""
        return len(self._items)

    def selected_count(self) -> int:
        """Return selected queue item count."""
        return sum(1 for item in self._items if item.is_selected())

    def selected_download_items(self) -> tuple[DownloadItem, ...]:
        """Return selected queue item domain values."""
        return tuple(item.to_download_item() for item in self._items if item.is_selected())

    def all_download_items(self) -> tuple[DownloadItem, ...]:
        """Return all queue item domain values."""
        return tuple(item.to_download_item() for item in self._items)

    def set_search_text(self, search_text: str) -> None:
        """Apply a queue search filter.

        Args:
            search_text: Search text entered by the user.
        """
        self._search_text = search_text
        self._apply_filter()

    def set_sort_mode(self, sort_mode: str) -> None:
        """Apply the selected queue sort mode.

        Args:
            sort_mode: Sort mode selected by the user.
        """
        self._sort_mode = sort_mode
        self._apply_sorting()

    def set_compact_mode(self, compact_mode: bool) -> None:
        """Apply the selected queue density immediately."""
        self._compact_mode = compact_mode
        self._items_layout.setSpacing(4 if compact_mode else 10)
        for item_widget in self._items:
            item_widget.set_compact_mode(compact_mode)

    def set_view_mode(self, view_mode: str) -> None:
        """Switch immediately between card and compact list renderers."""
        self._view_mode = "list" if view_mode == "list" else "cards"
        self._view_stack.setCurrentIndex(1 if self._view_mode == "list" else 0)
        self._cards_view_button.setChecked(self._view_mode == "cards")
        self._list_view_button.setChecked(self._view_mode == "list")

    def _set_cards_view(self) -> None:
        """Activate the detailed card view."""
        self.set_view_mode("cards")
        self.view_mode_changed.emit("cards")

    def _set_list_view(self) -> None:
        """Activate the compact list view."""
        self.set_view_mode("list")
        self.view_mode_changed.emit("list")

    def _build_layout(self) -> None:
        """Build the queue layout."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header_layout: QHBoxLayout = QHBoxLayout()
        title_label: QLabel = QLabel("Cola de descargas", self)
        title_label.setObjectName("sectionTitle")

        self._cards_view_button = QPushButton("Tarjetas", self)
        self._cards_view_button.setObjectName("queueViewButton")
        self._cards_view_button.setCheckable(True)
        self._cards_view_button.clicked.connect(self._set_cards_view)
        self._list_view_button = QPushButton("Lista", self)
        self._list_view_button.setObjectName("queueViewButton")
        self._list_view_button.setCheckable(True)
        self._list_view_button.clicked.connect(self._set_list_view)

        select_all_button: QPushButton = QPushButton("Seleccionar todo", self)
        select_all_button.clicked.connect(self.select_all_items)

        deselect_all_button: QPushButton = QPushButton("Deseleccionar", self)
        deselect_all_button.clicked.connect(self.deselect_all_items)

        remove_selected_button: QPushButton = QPushButton("Quitar seleccionados", self)
        remove_selected_button.clicked.connect(self.remove_selected_items)

        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self._cards_view_button)
        header_layout.addWidget(self._list_view_button)
        header_layout.addWidget(select_all_button)
        header_layout.addWidget(deselect_all_button)
        header_layout.addWidget(remove_selected_button)

        cards_scroll_area: QScrollArea = self._create_scroll_area(self._items_container)

        self._items_container.setObjectName("queueItemsContainer")
        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(8)

        self._empty_state = QLabel(
            "La cola está vacía\nAgrega una URL de video o playlist para comenzar.",
            self._items_container,
        )
        self._empty_state.setObjectName("emptyQueueLabel")
        self._empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_state.setMinimumHeight(220)
        self._items_layout.addWidget(self._empty_state)
        self._items_layout.addStretch(1)

        cards_scroll_area.setWidget(self._items_container)

        list_scroll_area: QScrollArea = self._create_scroll_area(self._list_container)
        self._list_container.setObjectName("compactQueueItemsContainer")
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(2)
        self._list_layout.addWidget(self._build_list_header())
        self._list_layout.addStretch(1)
        list_scroll_area.setWidget(self._list_container)

        self._view_stack = QStackedWidget(self)
        self._view_stack.addWidget(cards_scroll_area)
        self._view_stack.addWidget(list_scroll_area)

        layout.addLayout(header_layout)
        layout.addWidget(self._view_stack, 1)
        self.set_view_mode("cards")

    def _create_scroll_area(self, container: QWidget) -> QScrollArea:
        """Create a transparent scroll area for a queue renderer."""
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName("queueScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        return scroll_area

    def _build_list_header(self) -> QWidget:
        """Build fixed column labels for the compact list renderer."""
        header = QFrame(self._list_container)
        header.setObjectName("compactQueueHeader")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        labels = (("", 24), ("Título", 220), ("Formato", 62), ("Calidad", 66), ("Estado", 132))
        for text, width in labels:
            label = QLabel(text, header)
            if width:
                label.setFixedWidth(width)
            layout.addWidget(label, 1 if text == "Título" else 0)
        progress_label = QLabel("Progreso", header)
        progress_label.setMinimumWidth(120)
        layout.addWidget(progress_label, 1)
        percentage_label = QLabel("%", header)
        percentage_label.setFixedWidth(42)
        layout.addWidget(percentage_label)
        action_label = QLabel("Acción", header)
        action_label.setFixedWidth(62)
        layout.addWidget(action_label)
        return header

    def _find_item(self, item_id: str) -> QueueItemWidget | None:
        """Find a queue item by identifier."""
        for item_widget in self._items:
            if item_widget.item_id == item_id:
                return item_widget
        return None

    def _apply_filter(self) -> None:
        """Filter queue items by search text."""
        visible_count: int = 0
        for item_widget in self._items:
            is_visible: bool = item_widget.matches_search(self._search_text)
            item_widget.setVisible(is_visible)
            compact_item = self._compact_items.get(item_widget.item_id)
            if compact_item is not None:
                compact_item.setVisible(is_visible)
            if is_visible:
                visible_count += 1
        self._empty_state.setVisible(visible_count == 0)

    def _apply_sorting(self) -> None:
        """Apply selected visual sort order."""
        if self._sort_mode == "Orden de ingreso":
            self._items.sort(key=lambda item: self._item_order[item.item_id])
        elif self._sort_mode == "URL A-Z":
            self._items.sort(key=lambda item: item.source_url.lower())
        elif self._sort_mode == "URL Z-A":
            self._items.sort(key=lambda item: item.source_url.lower(), reverse=True)

        for item_widget in self._items:
            self._items_layout.removeWidget(item_widget)
            compact_item = self._compact_items.get(item_widget.item_id)
            if compact_item is not None:
                self._list_layout.removeWidget(compact_item)

        for index, item_widget in enumerate(self._items):
            self._items_layout.insertWidget(index, item_widget)
            compact_item = self._compact_items.get(item_widget.item_id)
            if compact_item is not None:
                self._list_layout.insertWidget(index + 1, compact_item)

        self._apply_filter()

    def _emit_queue_changed(self) -> None:
        """Emit current queue counts."""
        self.queue_changed.emit(self.item_count(), self.selected_count())

    def _update_compact_item(self, item_widget: QueueItemWidget) -> None:
        """Reflect card data changes in the compact renderer."""
        compact_item = self._compact_items.get(item_widget.item_id)
        if compact_item is not None:
            compact_item.update_item(QueueItemData.from_download_item(item_widget.to_download_item()))

    def _sync_compact_selection(self, item_id: str, selected: bool) -> None:
        """Apply a compact-row selection change to the canonical card item."""
        item_widget = self._find_item(item_id)
        if item_widget is not None:
            item_widget.set_selected(selected)
        self._emit_queue_changed()

    def _handle_card_selection(self, item_id: str, selected: bool) -> None:
        """Reflect card selection changes in the compact list renderer."""
        compact_item = self._compact_items.get(item_id)
        if compact_item is not None:
            compact_item.set_selected(selected)
        self._emit_queue_changed()

    def _sync_compact_selections(self) -> None:
        """Reflect all canonical card selections in compact rows."""
        for item_widget in self._items:
            compact_item = self._compact_items.get(item_widget.item_id)
            if compact_item is not None:
                compact_item.set_selected(item_widget.is_selected())
