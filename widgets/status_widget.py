"""Application status display widget."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class StatusWidget(QWidget):
    """Compact status area for current application state."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the status widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("statusWidget")
        self._build_layout()

    def _build_layout(self) -> None:
        """Build the status layout."""
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)

        status_label: QLabel = QLabel("Estado: listo", self)
        status_label.setObjectName("statusLabel")
        layout.addWidget(status_label)
        layout.addStretch(1)
