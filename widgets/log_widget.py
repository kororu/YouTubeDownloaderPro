"""Application log display widget."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

MAX_VISIBLE_LOG_LINES: int = 1200


class LogWidget(QWidget):
    """Read-only log area for application messages."""

    export_requested: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the log widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("logWidget")
        self._log_output: QPlainTextEdit
        self._build_layout()

    def append_info(self, message: str) -> None:
        """Append an informational message.

        Args:
            message: Message text.
        """
        self.append_log("INFO", message)

    def append_warning(self, message: str) -> None:
        """Append a warning message.

        Args:
            message: Message text.
        """
        self.append_log("WARNING", message)

    def append_error(self, message: str) -> None:
        """Append an error message.

        Args:
            message: Message text.
        """
        self.append_log("ERROR", message)

    def append_log(self, level: str, message: str) -> None:
        """Append a timestamped log message to the visible log.

        Args:
            level: Log level label.
            message: Message text.
        """
        timestamp: str = datetime.now().strftime("%H:%M:%S")
        self._log_output.appendPlainText(f"{timestamp} | {level} | {message}")

    def _build_layout(self) -> None:
        """Build the log layout."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        header_layout: QHBoxLayout = QHBoxLayout()
        title_label: QLabel = QLabel("Registro", self)
        title_label.setObjectName("sectionTitle")

        clear_button: QPushButton = QPushButton("Limpiar", self)
        clear_button.clicked.connect(self._clear_log)

        export_button: QPushButton = QPushButton("Exportar", self)
        export_button.clicked.connect(self.export_requested.emit)

        copy_button: QPushButton = QPushButton("Copiar", self)
        copy_button.setToolTip("Copia el registro visible al portapapeles.")
        copy_button.clicked.connect(self._copy_log)

        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(export_button)
        header_layout.addWidget(copy_button)
        header_layout.addWidget(clear_button)

        self._log_output = QPlainTextEdit(self)
        self._log_output.setObjectName("logOutput")
        self._log_output.setReadOnly(True)
        self._log_output.document().setMaximumBlockCount(MAX_VISIBLE_LOG_LINES)

        layout.addLayout(header_layout)
        layout.addWidget(self._log_output, 1)
        self.append_info("Aplicación iniciada.")

    def _clear_log(self) -> None:
        """Clear the visible log output."""
        self._log_output.clear()
        self.append_info("Registro limpiado.")

    def _copy_log(self) -> None:
        """Copy the visible log to the system clipboard."""
        QGuiApplication.clipboard().setText(self._log_output.toPlainText())
        self.append_info("Registro copiado al portapapeles.")

    def export_to_file(self, destination_path: Path) -> None:
        """Export visible logs to a text file.

        Args:
            destination_path: Destination text file path.
        """
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        destination_path.write_text(self._log_output.toPlainText(), encoding="utf-8")
