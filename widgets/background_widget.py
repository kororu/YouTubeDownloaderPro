"""Application background container widget."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent, QPixmap, QResizeEvent
from PySide6.QtWidgets import QWidget


class BackgroundWidget(QWidget):
    """Paints an optional image behind the main application layout."""

    _supported_suffixes: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".webp"})

    def __init__(
        self,
        background_image_path: str = "",
        background_opacity: float = 0.28,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the background widget.

        Args:
            background_image_path: Optional image path selected by the user.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._background_image_path: str = ""
        self._background_opacity: float = 0.28
        self._background_pixmap: QPixmap | None = None
        self._scaled_background_pixmap: QPixmap | None = None
        self._scaled_background_size: QSize = QSize()
        self.setObjectName("mainContentArea")
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.set_background_opacity(background_opacity)
        self.set_background_image_path(background_image_path)

    def set_background_opacity(self, opacity: float) -> None:
        """Set the visible image opacity while preserving readable content."""
        self._background_opacity = max(0.10, min(0.55, opacity))
        self.update()

    def set_background_image_path(self, background_image_path: str) -> None:
        """Update the optional background image.

        Args:
            background_image_path: Image path selected by the user.
        """
        normalized_path: str = background_image_path.strip()
        self._background_image_path = normalized_path
        self._background_pixmap = self._load_pixmap(normalized_path)
        self._refresh_scaled_background_pixmap()
        self.update()

    def has_background_image(self) -> bool:
        """Return whether a valid background image is active."""
        return self._background_pixmap is not None and not self._background_pixmap.isNull()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the dark base, optional image, and readability overlay."""
        painter: QPainter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#0d1117"))

        if self._background_pixmap is not None and self._scaled_background_size != self.size():
            self._refresh_scaled_background_pixmap()

        if self._scaled_background_pixmap is not None and not self._scaled_background_pixmap.isNull():
            x_position: int = (self.width() - self._scaled_background_pixmap.width()) // 2
            y_position: int = (self.height() - self._scaled_background_pixmap.height()) // 2
            painter.setOpacity(self._background_opacity)
            painter.drawPixmap(x_position, y_position, self._scaled_background_pixmap)
            painter.setOpacity(1.0)
            painter.fillRect(self.rect(), QColor(13, 17, 23, 142))

        painter.end()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Refresh the cover-scaled background when the widget changes size."""
        super().resizeEvent(event)
        self._refresh_scaled_background_pixmap()

    def _refresh_scaled_background_pixmap(self) -> None:
        """Scale the background image to cover the current widget size."""
        if (
            self._background_pixmap is None
            or self._background_pixmap.isNull()
            or self.width() <= 0
            or self.height() <= 0
        ):
            self._scaled_background_pixmap = None
            self._scaled_background_size = QSize()
            return

        self._scaled_background_pixmap = self._background_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._scaled_background_size = QSize(self.size())

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
