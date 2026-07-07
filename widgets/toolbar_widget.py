"""Top toolbar widget for primary user inputs."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class ToolbarWidget(QWidget):
    """Toolbar area for URL input and main commands."""

    add_video_requested: Signal = Signal(str, str, str)
    add_playlist_requested: Signal = Signal(str, str, str)
    start_downloads_requested: Signal = Signal()
    cancel_current_requested: Signal = Signal()
    cancel_all_requested: Signal = Signal()
    settings_requested: Signal = Signal()
    about_requested: Signal = Signal()

    def __init__(
        self,
        selected_format: str = "mp4",
        selected_quality: str = "best",
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the toolbar widget.

        Args:
            selected_format: Initial selected media format.
            selected_quality: Initial selected media quality.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("toolbarWidget")
        self._initial_format: str = selected_format
        self._initial_quality: str = selected_quality
        self._url_input: QLineEdit
        self._format_combo_box: QComboBox
        self._quality_combo_box: QComboBox
        self._add_video_button: QPushButton
        self._add_playlist_button: QPushButton
        self._build_layout()

    def _build_layout(self) -> None:
        """Build toolbar controls."""
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        url_label: QLabel = QLabel("URL", self)
        url_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._url_input = QLineEdit(self)
        self._url_input.setObjectName("urlInput")
        self._url_input.setClearButtonEnabled(True)
        self._url_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._url_input.setToolTip("Ingrese una URL de video o playlist")
        self._url_input.textChanged.connect(self._update_action_state)

        self._format_combo_box = QComboBox(self)
        self._format_combo_box.setObjectName("formatComboBox")
        self._format_combo_box.addItems(("MP4", "MP3"))
        self._format_combo_box.setCurrentText(self._initial_format.upper())

        self._quality_combo_box = QComboBox(self)
        self._quality_combo_box.setObjectName("qualityComboBox")
        self._quality_combo_box.addItems(("Best available", "480", "720", "1080", "1440", "2160"))
        self._quality_combo_box.setCurrentText(
            "Best available" if self._initial_quality == "best" else self._initial_quality
        )

        self._add_video_button = QPushButton("Agregar video", self)
        self._add_video_button.setEnabled(False)
        self._add_video_button.clicked.connect(self._emit_add_video_requested)

        self._add_playlist_button = QPushButton("Agregar playlist", self)
        self._add_playlist_button.setEnabled(False)
        self._add_playlist_button.clicked.connect(self._emit_add_playlist_requested)

        settings_button: QPushButton = QPushButton("Ajustes", self)
        settings_button.clicked.connect(self.settings_requested.emit)

        about_button: QPushButton = QPushButton("Acerca de", self)
        about_button.clicked.connect(self.about_requested.emit)

        start_button: QPushButton = QPushButton("Descargar seleccionados", self)
        start_button.clicked.connect(self.start_downloads_requested.emit)

        cancel_current_button: QPushButton = QPushButton("Cancelar actual", self)
        cancel_current_button.clicked.connect(self.cancel_current_requested.emit)

        cancel_all_button: QPushButton = QPushButton("Cancelar todo", self)
        cancel_all_button.clicked.connect(self.cancel_all_requested.emit)

        layout.addWidget(url_label)
        layout.addWidget(self._url_input, 1)
        layout.addWidget(self._format_combo_box)
        layout.addWidget(self._quality_combo_box)
        layout.addWidget(self._add_video_button)
        layout.addWidget(self._add_playlist_button)
        layout.addWidget(start_button)
        layout.addWidget(cancel_current_button)
        layout.addWidget(cancel_all_button)
        layout.addWidget(settings_button)
        layout.addWidget(about_button)

    def selected_format(self) -> str:
        """Return the selected media format."""
        return self._format_combo_box.currentText().lower()

    def selected_quality(self) -> str:
        """Return the selected media quality."""
        quality: str = self._quality_combo_box.currentText()
        if quality == "Best available":
            return "best"
        return quality

    def set_download_preferences(self, selected_format: str, selected_quality: str) -> None:
        """Update selected format and quality controls.

        Args:
            selected_format: Selected media format.
            selected_quality: Selected media quality.
        """
        self._format_combo_box.setCurrentText(selected_format.upper())
        self._quality_combo_box.setCurrentText(
            "Best available" if selected_quality == "best" else selected_quality
        )

    def _update_action_state(self, text: str) -> None:
        """Enable URL actions when text is available."""
        has_url: bool = bool(text.strip())
        self._add_video_button.setEnabled(has_url)
        self._add_playlist_button.setEnabled(has_url)

    def _emit_add_video_requested(self) -> None:
        """Emit the add video request."""
        self.add_video_requested.emit(
            self._url_input.text().strip(),
            self.selected_format(),
            self.selected_quality(),
        )
        self._url_input.clear()

    def _emit_add_playlist_requested(self) -> None:
        """Emit the add playlist request."""
        self.add_playlist_requested.emit(
            self._url_input.text().strip(),
            self.selected_format(),
            self.selected_quality(),
        )
        self._url_input.clear()
