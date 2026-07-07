"""Application footer widget."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from core.constants import APPLICATION_AUTHOR, APPLICATION_VERSION


class FooterWidget(QWidget):
    """Footer displaying project metadata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the footer widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("footerWidget")
        self._build_layout()

    def _build_layout(self) -> None:
        """Build footer metadata labels."""
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(16)

        author_label: QLabel = QLabel(f"Autor: {APPLICATION_AUTHOR}", self)
        version_label: QLabel = QLabel(f"Versión: v{APPLICATION_VERSION}", self)

        layout.addWidget(author_label)
        layout.addStretch(1)
        layout.addWidget(version_label)
