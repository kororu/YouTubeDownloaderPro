"""Download history management dialog."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget

from models.download_history_item import DownloadHistoryItem


class HistoryDialog(QDialog):
    """Searchable history dialog with local file actions."""

    retry_requested: Signal = Signal(object)

    def __init__(self, items: tuple[DownloadHistoryItem, ...], parent: QWidget | None = None) -> None:
        """Initialize dialog with current history records."""
        super().__init__(parent)
        self.setWindowTitle("Historial de descargas")
        self.resize(850, 520)
        self._items = items
        self._search = QLineEdit(self)
        self._search.setPlaceholderText("Buscar por título, canal o URL")
        self._list = QListWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self._search)
        layout.addWidget(self._list, 1)
        actions = QHBoxLayout()
        for text, handler in (("Reintentar", self._retry), ("Abrir carpeta", self._open_folder), ("Copiar ruta", self._copy_path), ("Copiar URL", self._copy_url)):
            button = QPushButton(text, self)
            button.clicked.connect(handler)
            actions.addWidget(button)
        actions.addStretch(1)
        close_button = QPushButton("Cerrar", self)
        close_button.clicked.connect(self.accept)
        actions.addWidget(close_button)
        layout.addLayout(actions)
        self._search.textChanged.connect(self._refresh)
        self._refresh()

    def _refresh(self) -> None:
        """Apply search filtering to visible history records."""
        query = self._search.text().strip().lower()
        self._list.clear()
        for item in self._items:
            text = f"{item.title} {item.channel or ''} {item.url}".lower()
            if query and query not in text:
                continue
            row = QListWidgetItem(f"[{item.status}] {item.title}\n{item.output_format.upper()} · {item.quality} · {item.downloaded_at}")
            row.setData(256, item)
            self._list.addItem(row)

    def _selected(self) -> DownloadHistoryItem | None:
        """Return the selected record."""
        row = self._list.currentItem()
        return row.data(256) if row is not None else None

    def _retry(self) -> None:
        """Request a retry for the selected record."""
        item = self._selected()
        if item is not None:
            self.retry_requested.emit(item)

    def _open_folder(self) -> None:
        """Open the output folder when it still exists."""
        item = self._selected()
        if item is not None:
            folder = Path(item.output_folder)
            if folder.is_dir():
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def _copy_path(self) -> None:
        """Copy output path to clipboard."""
        item = self._selected()
        if item is not None:
            QGuiApplication.clipboard().setText(item.output_path or item.output_folder)

    def _copy_url(self) -> None:
        """Copy source URL to clipboard."""
        item = self._selected()
        if item is not None:
            QGuiApplication.clipboard().setText(item.url)
