"""Application status display widget."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget


class StatusWidget(QWidget):
    """Compact status area for current application state."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the status widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("statusWidget")
        self._status_label: QLabel
        self._queue_label: QLabel
        self._dependency_label: QLabel
        self._progress_bar: QProgressBar
        self._build_layout()

    def update_queue_status(self, total_items: int, selected_items: int) -> None:
        """Update queue counters.

        Args:
            total_items: Total queue items.
            selected_items: Selected queue items.
        """
        self._queue_label.setText(f"Cola: {total_items} | Seleccionados: {selected_items}")

    def update_dependency_status(self, all_available: bool) -> None:
        """Update dependency status.

        Args:
            all_available: Whether all external dependencies are available.
        """
        status_text: str = "Dependencias: listas" if all_available else "Dependencias: revisar"
        self._dependency_label.setText(status_text)

    def set_status_message(self, message: str) -> None:
        """Update the main status message.

        Args:
            message: Status message.
        """
        self._status_label.setText(f"Estado: {message}")

    def set_progress(self, percentage: float) -> None:
        """Update the status progress bar.

        Args:
            percentage: Progress percentage.
        """
        self._progress_bar.setValue(round(max(0.0, min(100.0, percentage))))

    def _build_layout(self) -> None:
        """Build the status layout."""
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        self._status_label = QLabel("Estado: listo", self)
        self._status_label.setObjectName("statusLabel")

        self._queue_label = QLabel("Cola: 0 | Seleccionados: 0", self)
        self._queue_label.setObjectName("queueStatusLabel")

        self._dependency_label = QLabel("Dependencias: verificando", self)
        self._dependency_label.setObjectName("dependencyStatusLabel")

        self._progress_bar = QProgressBar(self)
        self._progress_bar.setObjectName("statusProgressBar")
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setFixedWidth(180)

        layout.addWidget(self._status_label)
        layout.addWidget(self._queue_label)
        layout.addWidget(self._dependency_label)
        layout.addStretch(1)
        layout.addWidget(self._progress_bar)
