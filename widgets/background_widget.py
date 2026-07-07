"""Application background container widget."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent, QPixmap
from PySide6.QtWidgets import QWidget


class BackgroundWidget(QWidget):
    """Paints an optional image behind the main application layout."""

    _supported_suffixes: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".webp"})

    def __init__(self, background_image_path: str = "", parent: QWidget | None = None) -> None:
        """Initialize the background widget.

        Args:
            background_image_path: Optional image path selected by the user.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._background_image_path: str = ""
        self._background_pixmap: QPixmap | None = None
        self.setObjectName("mainContentArea")
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.set_background_image_path(background_image_path)

    def set_background_image_path(self, background_image_path: str) -> None:
        """Update the optional background image.

        Args:
            background_image_path: Image path selected by the user.
        """
        normalized_path: str = background_image_path.strip()
        self._background_image_path = normalized_path
        self._background_pixmap = self._load_pixmap(normalized_path)
        self.update()

    def has_background_image(self) -> bool:
        """Return whether a valid background image is active."""
        return self._background_pixmap is not None and not self._background_pixmap.isNull()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the dark base, optional image, and readability overlay."""
        painter: QPainter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#0d1117"))

        if self._background_pixmap is not None and not self._background_pixmap.isNull():
            scaled_pixmap: QPixmap = self._background_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x_position: int = (self.width() - scaled_pixmap.width()) // 2
            y_position: int = (self.height() - scaled_pixmap.height()) // 2
            painter.setOpacity(0.58)
            painter.drawPixmap(x_position, y_position, scaled_pixmap)
            painter.setOpacity(1.0)
            painter.fillRect(self.rect(), QColor(13, 17, 23, 96))

        painter.end()

    @classmethod
    def _load_pixmap(cls, background_image_path: str) -> QPixmap | None:
        """Load a supported image path when it exists."""
        if not background_image_path:
            return None

        path: Path = Path(background_image_path).expanduser()
        if path.suffix.lower() not in cls._supported_suffixes or not path.is_file():
            return None

        pixmap: QPixmap = QPixmap(str(path))
        if pixmap.isNull():
            return None
        return pixmap
