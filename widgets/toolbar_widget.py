"""Top toolbar widget for primary user inputs."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class ToolbarWidget(QWidget):
    """Toolbar area for URL input and main commands."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the toolbar widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("toolbarWidget")
        self._build_layout()

    def _build_layout(self) -> None:
        """Build toolbar controls."""
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        url_label: QLabel = QLabel("URL", self)
        url_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        url_input: QLineEdit = QLineEdit(self)
        url_input.setObjectName("urlInput")
        url_input.setClearButtonEnabled(True)
        url_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        add_video_button: QPushButton = QPushButton("Agregar video", self)
        add_video_button.setEnabled(False)

        add_playlist_button: QPushButton = QPushButton("Agregar playlist", self)
        add_playlist_button.setEnabled(False)

        layout.addWidget(url_label)
        layout.addWidget(url_input, 1)
        layout.addWidget(add_video_button)
        layout.addWidget(add_playlist_button)
