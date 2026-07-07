"""Application log display widget."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPlainTextEdit, QVBoxLayout, QWidget


class LogWidget(QWidget):
    """Read-only log area for application messages."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the log widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("logWidget")
        self._build_layout()

    def _build_layout(self) -> None:
        """Build the log layout."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        title_label: QLabel = QLabel("Registro", self)
        title_label.setObjectName("sectionTitle")

        log_output: QPlainTextEdit = QPlainTextEdit(self)
        log_output.setObjectName("logOutput")
        log_output.setReadOnly(True)
        log_output.setPlainText("Aplicación iniciada.")

        layout.addWidget(title_label)
        layout.addWidget(log_output, 1)
