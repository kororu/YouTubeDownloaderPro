"""Focused controls for the application's simple interface mode."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class SimpleModeWidget(QWidget):
    """Expose essential video and queue actions without advanced controls."""

    add_video_requested: Signal = Signal(str, str)
    add_playlist_requested: Signal = Signal(str, str)
    change_folder_requested: Signal = Signal()
    download_all_requested: Signal = Signal()
    download_selected_requested: Signal = Signal()
    select_all_requested: Signal = Signal()
    deselect_all_requested: Signal = Signal()
    remove_selected_requested: Signal = Signal()
    cancel_requested: Signal = Signal()

    def __init__(self, output_folder: str, parent: QWidget | None = None) -> None:
        """Initialize simple controls.

        Args:
            output_folder: Current download destination.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("simpleModeWidget")
        self._url_input: QLineEdit
        self._format_combo_box: QComboBox
        self._destination_label: QLabel
        self._add_video_button: QPushButton
        self._add_playlist_button: QPushButton
        self._build_layout(output_folder)

    def focus_url_input(self) -> None:
        """Focus the URL input for the global keyboard shortcut."""
        self._url_input.setFocus()

    def set_output_folder(self, output_folder: str) -> None:
        """Show the current output folder.

        Args:
            output_folder: Current download destination.
        """
        self._destination_label.setText(output_folder)
        self._destination_label.setToolTip(output_folder)

    def _build_layout(self, output_folder: str) -> None:
        """Build the reduced control layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)

        input_frame = QFrame(self)
        input_frame.setObjectName("simpleModeInputFrame")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 8, 10, 8)
        input_layout.setSpacing(8)

        self._url_input = QLineEdit(self)
        self._url_input.setObjectName("simpleUrlInput")
        self._url_input.setPlaceholderText("Pega una URL de video o playlist")
        self._url_input.setClearButtonEnabled(True)
        self._url_input.textChanged.connect(self._update_action_state)

        self._format_combo_box = QComboBox(self)
        self._format_combo_box.addItem("MP4", "mp4")
        self._format_combo_box.addItem("MP3", "mp3")
        self._format_combo_box.setToolTip("Mejor calidad automática")

        self._add_video_button = QPushButton("Agregar video", self)
        self._add_video_button.setEnabled(False)
        self._add_video_button.clicked.connect(self._emit_add_video)
        self._add_playlist_button = QPushButton("Agregar playlist", self)
        self._add_playlist_button.setEnabled(False)
        self._add_playlist_button.clicked.connect(self._emit_add_playlist)

        input_layout.addWidget(self._url_input, 1)
        input_layout.addWidget(self._format_combo_box)
        quality_label = QLabel("Mejor calidad automática", self)
        quality_label.setObjectName("simpleModeQualityLabel")
        input_layout.addWidget(quality_label)
        input_layout.addWidget(self._add_video_button)
        input_layout.addWidget(self._add_playlist_button)

        destination_row = QHBoxLayout()
        destination_row.addWidget(QLabel("Destino:", self))
        self._destination_label = QLabel(self)
        self._destination_label.setObjectName("simpleModeDestination")
        destination_row.addWidget(self._destination_label, 1)
        change_folder_button = QPushButton("Cambiar carpeta", self)
        change_folder_button.clicked.connect(self.change_folder_requested.emit)
        destination_row.addWidget(change_folder_button)

        actions_row = QHBoxLayout()
        actions = (
            ("Descargar todo", self.download_all_requested),
            ("Descargar seleccionados", self.download_selected_requested),
            ("Seleccionar todo", self.select_all_requested),
            ("Deseleccionar", self.deselect_all_requested),
            ("Quitar seleccionados", self.remove_selected_requested),
            ("Cancelar", self.cancel_requested),
        )
        for label, signal in actions:
            button = QPushButton(label, self)
            button.clicked.connect(signal.emit)
            actions_row.addWidget(button)
        actions_row.addStretch(1)

        layout.addWidget(input_frame)
        layout.addLayout(destination_row)
        layout.addLayout(actions_row)
        self.set_output_folder(output_folder)

    def _update_action_state(self) -> None:
        """Enable URL actions only when text is available."""
        enabled = bool(self._url_input.text().strip())
        self._add_video_button.setEnabled(enabled)
        self._add_playlist_button.setEnabled(enabled)

    def _emit_add_video(self) -> None:
        """Emit a best-quality single-video request."""
        self.add_video_requested.emit(self._url_input.text().strip(), self._format_combo_box.currentData())

    def _emit_add_playlist(self) -> None:
        """Emit a best-quality playlist request."""
        self.add_playlist_requested.emit(self._url_input.text().strip(), self._format_combo_box.currentData())
