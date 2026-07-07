"""About dialog for YouTube Downloader Pro."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QWidget

from core.constants import APPLICATION_AUTHOR, APPLICATION_NAME, APPLICATION_VERSION


class AboutDialog(QDialog):
    """Application information dialog."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the about dialog.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("aboutDialog")
        self.setWindowTitle(f"Acerca de {APPLICATION_NAME}")
        self.setModal(True)
        self.setMinimumWidth(420)
        self._build_layout()

    def _build_layout(self) -> None:
        """Build dialog content."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title_label: QLabel = QLabel(APPLICATION_NAME, self)
        title_label.setObjectName("aboutTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version_label: QLabel = QLabel(f"Versión: v{APPLICATION_VERSION}", self)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        author_label: QLabel = QLabel(f"Autor: {APPLICATION_AUTHOR}", self)
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        description_label: QLabel = QLabel(
            "Frontend de escritorio para yt-dlp y ffmpeg construido con Python y PySide6.",
            self,
        )
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        close_button: QPushButton = QPushButton("Cerrar", self)
        close_button.clicked.connect(self.accept)

        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addWidget(author_label)
        layout.addWidget(description_label)
        layout.addSpacing(8)
        layout.addWidget(close_button)
