"""Top toolbar widget for primary user inputs."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from models.playlist_range import PlaylistRange

FORMAT_OPTIONS: tuple[tuple[str, str], ...] = (
    ("MP4", "mp4"),
    ("MP3", "mp3"),
    ("M4A", "m4a"),
    ("OPUS", "opus"),
    ("FLAC", "flac"),
    ("WAV", "wav"),
    ("Audio original", "best_audio"),
)


class ToolbarWidget(QWidget):
    """Toolbar area for URL input and main commands."""

    add_video_requested: Signal = Signal(str, str, str)
    add_playlist_requested: Signal = Signal(str, str, str, object)
    add_next_playlist_range_requested: Signal = Signal(str, str, str)
    playlist_range_error: Signal = Signal(str)
    start_downloads_requested: Signal = Signal()
    cancel_current_requested: Signal = Signal()
    cancel_all_requested: Signal = Signal()
    settings_requested: Signal = Signal()
    about_requested: Signal = Signal()
    queue_search_changed: Signal = Signal(str)
    queue_sort_changed: Signal = Signal(str)

    def __init__(
        self,
        selected_format: str = "mp4",
        selected_quality: str = "best",
        selected_audio_quality: str = "best",
        playlist_start_index: int = 1,
        playlist_end_index: int = 0,
        playlist_limit: int = 200,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the toolbar widget.

        Args:
            selected_format: Initial selected media format.
            selected_quality: Initial selected media quality.
            playlist_start_index: Initial playlist start index.
            playlist_end_index: Initial playlist end index, or 0 for automatic.
            playlist_limit: Playlist item count used when end is automatic.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setObjectName("toolbarWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._initial_format: str = selected_format
        self._initial_quality: str = selected_quality
        self._initial_audio_quality: str = selected_audio_quality
        self._initial_playlist_start_index: int = playlist_start_index
        self._initial_playlist_end_index: int = playlist_end_index
        self._playlist_limit: int = playlist_limit
        self._url_input: QLineEdit
        self._format_combo_box: QComboBox
        self._quality_combo_box: QComboBox
        self._playlist_start_spin_box: QSpinBox
        self._playlist_end_spin_box: QSpinBox
        self._queue_sort_combo_box: QComboBox
        self._queue_search_input: QLineEdit
        self._add_video_button: QPushButton
        self._add_playlist_button: QPushButton
        self._load_range_button: QPushButton
        self._add_next_playlist_range_button: QPushButton
        self._build_layout()

    def _build_layout(self) -> None:
        """Build toolbar controls."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)

        input_row: QHBoxLayout = self._create_row(spacing=10)
        playlist_row: QHBoxLayout = self._create_row(spacing=14)
        action_row: QHBoxLayout = self._create_row(spacing=10)

        input_group: QFrame = self._create_group()
        input_group_layout: QHBoxLayout = self._create_group_layout(input_group)

        playlist_group: QFrame = self._create_group()
        playlist_group_layout: QHBoxLayout = self._create_group_layout(playlist_group)

        queue_group: QFrame = self._create_group()
        queue_group_layout: QHBoxLayout = self._create_group_layout(queue_group)

        download_group: QFrame = self._create_group()
        download_group_layout: QHBoxLayout = self._create_group_layout(download_group)

        app_group: QFrame = self._create_group()
        app_group_layout: QHBoxLayout = self._create_group_layout(app_group)

        self._url_input = QLineEdit(self)
        self._url_input.setObjectName("urlInput")
        self._url_input.setClearButtonEnabled(True)
        self._url_input.setMinimumWidth(340)
        self._url_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._url_input.setToolTip("Ingrese una URL de video o playlist")
        self._url_input.textChanged.connect(self._update_action_state)

        self._format_combo_box = QComboBox(self)
        self._format_combo_box.setObjectName("formatComboBox")
        for label, value in FORMAT_OPTIONS:
            self._format_combo_box.addItem(label, value)
        self._set_combo_data(self._format_combo_box, self._initial_format)
        self._format_combo_box.setMinimumWidth(145)
        self._format_combo_box.setToolTip("Elige video MP4 o el formato de audio de salida.")
        self._format_combo_box.currentIndexChanged.connect(self._populate_quality_combo_box)

        self._quality_combo_box = QComboBox(self)
        self._quality_combo_box.setObjectName("qualityComboBox")
        self._quality_combo_box.setMinimumWidth(150)
        self._quality_combo_box.setToolTip("Elige la resolución de video o bitrate de MP3.")
        self._populate_quality_combo_box()
        self._quality_combo_box.currentIndexChanged.connect(self._remember_selected_quality)

        self._playlist_start_spin_box = QSpinBox(self)
        self._playlist_start_spin_box.setObjectName("playlistStartSpinBox")
        self._playlist_start_spin_box.setRange(1, 100000)
        self._playlist_start_spin_box.setValue(max(1, self._initial_playlist_start_index))
        self._playlist_start_spin_box.setMinimumWidth(82)
        self._playlist_start_spin_box.setToolTip("Primer video de la playlist o Mix")

        self._playlist_end_spin_box = QSpinBox(self)
        self._playlist_end_spin_box.setObjectName("playlistEndSpinBox")
        self._playlist_end_spin_box.setRange(0, 100000)
        self._playlist_end_spin_box.setSpecialValueText("Auto")
        self._playlist_end_spin_box.setValue(max(0, self._initial_playlist_end_index))
        self._playlist_end_spin_box.setMinimumWidth(82)
        self._playlist_end_spin_box.setToolTip("Ultimo video de la playlist o Mix; Auto usa el limite")

        self._queue_sort_combo_box = QComboBox(self)
        self._queue_sort_combo_box.setObjectName("queueSortComboBox")
        self._queue_sort_combo_box.addItems(("Orden de ingreso", "URL A-Z", "URL Z-A"))
        self._queue_sort_combo_box.setMinimumWidth(145)
        self._queue_sort_combo_box.currentTextChanged.connect(self.queue_sort_changed.emit)

        self._queue_search_input = QLineEdit(self)
        self._queue_search_input.setObjectName("queueSearchInput")
        self._queue_search_input.setClearButtonEnabled(True)
        self._queue_search_input.setPlaceholderText("Buscar en cola")
        self._queue_search_input.setMinimumWidth(200)
        self._queue_search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._queue_search_input.textChanged.connect(self.queue_search_changed.emit)

        self._add_video_button = self._create_button("Agregar video", 128)
        self._add_video_button.setToolTip("Agrega un video individual y carga sus metadatos.")
        self._add_video_button.setEnabled(False)
        self._add_video_button.clicked.connect(self._emit_add_video_requested)

        self._add_playlist_button = self._create_button("Agregar playlist", 142)
        self._add_playlist_button.setToolTip("Carga el bloque predeterminado de una playlist o Mix.")
        self._add_playlist_button.setEnabled(False)
        self._add_playlist_button.clicked.connect(self._emit_add_default_playlist_requested)

        self._load_range_button = self._create_button("Cargar rango", 126)
        self._load_range_button.setToolTip("Carga el rango de posiciones indicado para la playlist o Mix.")
        self._load_range_button.setEnabled(False)
        self._load_range_button.clicked.connect(self._emit_add_playlist_requested)

        self._add_next_playlist_range_button = self._create_button("Cargar siguientes", 156)
        self._add_next_playlist_range_button.setToolTip("Carga el siguiente rango pendiente de esta URL.")
        self._add_next_playlist_range_button.setEnabled(False)
        self._add_next_playlist_range_button.clicked.connect(self._emit_add_next_playlist_range_requested)

        start_button: QPushButton = self._create_button("Descargar seleccionados", 198)
        start_button.setToolTip("Inicia las descargas de los elementos seleccionados.")
        start_button.clicked.connect(self.start_downloads_requested.emit)

        cancel_current_button: QPushButton = self._create_button("Cancelar actual", 138)
        cancel_current_button.setToolTip("Cancela el análisis de playlist o descarga actualmente activa.")
        cancel_current_button.clicked.connect(self.cancel_current_requested.emit)

        cancel_all_button: QPushButton = self._create_button("Cancelar todo", 126)
        cancel_all_button.setToolTip("Solicita cancelar todas las descargas y análisis activos.")
        cancel_all_button.clicked.connect(self.cancel_all_requested.emit)

        settings_button: QPushButton = self._create_button("Ajustes", 96)
        settings_button.clicked.connect(self.settings_requested.emit)

        about_button: QPushButton = self._create_button("Acerca de", 104)
        about_button.clicked.connect(self.about_requested.emit)

        input_group_layout.addWidget(self._create_label("URL"))
        input_group_layout.addWidget(self._url_input, 1)
        input_group_layout.addWidget(self._create_label("Formato"))
        input_group_layout.addWidget(self._format_combo_box)
        input_group_layout.addWidget(self._create_label("Calidad"))
        input_group_layout.addWidget(self._quality_combo_box)
        input_group_layout.addWidget(self._add_video_button)
        input_group_layout.addWidget(self._add_playlist_button)

        playlist_group_layout.addWidget(self._create_label("Inicio"))
        playlist_group_layout.addWidget(self._playlist_start_spin_box)
        playlist_group_layout.addWidget(self._create_label("Fin"))
        playlist_group_layout.addWidget(self._playlist_end_spin_box)
        playlist_group_layout.addWidget(self._load_range_button)
        playlist_group_layout.addWidget(self._add_next_playlist_range_button)

        queue_group_layout.addWidget(self._create_label("Orden"))
        queue_group_layout.addWidget(self._queue_sort_combo_box)
        queue_group_layout.addWidget(self._create_label("Buscar"))
        queue_group_layout.addWidget(self._queue_search_input, 1)

        download_group_layout.addWidget(start_button)
        download_group_layout.addWidget(cancel_current_button)
        download_group_layout.addWidget(cancel_all_button)

        app_group_layout.addWidget(settings_button)
        app_group_layout.addWidget(about_button)

        input_row.addWidget(input_group, 1)
        playlist_row.addWidget(playlist_group, 0)
        playlist_row.addWidget(queue_group, 1)
        action_row.addWidget(download_group, 0)
        action_row.addStretch(1)
        action_row.addWidget(app_group, 0)

        layout.addLayout(input_row)
        layout.addLayout(playlist_row)
        layout.addLayout(action_row)

    def _create_row(self, spacing: int) -> QHBoxLayout:
        """Create a toolbar row layout.

        Args:
            spacing: Row spacing in pixels.

        Returns:
            Configured horizontal layout.
        """
        row: QHBoxLayout = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(spacing)
        return row

    def _create_group(self) -> QFrame:
        """Create a transparent control group container.

        Returns:
            Configured frame.
        """
        group: QFrame = QFrame(self)
        group.setObjectName("toolbarGroup")
        group.setFrameShape(QFrame.Shape.NoFrame)
        group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        return group

    def _create_group_layout(self, group: QFrame) -> QHBoxLayout:
        """Create a compact layout for a toolbar group.

        Args:
            group: Toolbar group frame.

        Returns:
            Configured group layout.
        """
        group_layout: QHBoxLayout = QHBoxLayout(group)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(8)
        return group_layout

    def _create_label(self, text: str) -> QLabel:
        """Create a compact toolbar label.

        Args:
            text: Label text.

        Returns:
            Configured label.
        """
        label: QLabel = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        return label

    def _create_button(self, text: str, minimum_width: int) -> QPushButton:
        """Create a toolbar button with stable sizing.

        Args:
            text: Button text.
            minimum_width: Minimum button width in pixels.

        Returns:
            Configured push button.
        """
        button: QPushButton = QPushButton(text, self)
        button.setMinimumWidth(minimum_width)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        return button

    def selected_format(self) -> str:
        """Return the selected media format."""
        return str(self._format_combo_box.currentData())

    def focus_url_input(self) -> None:
        """Focus the URL input without changing its current contents."""
        self._url_input.setFocus(Qt.FocusReason.ShortcutFocusReason)

    def is_url_input_focused(self) -> bool:
        """Return whether the URL input currently owns keyboard focus."""
        return self._url_input.hasFocus()

    def selected_quality(self) -> str:
        """Return the selected media quality."""
        return str(self._quality_combo_box.currentData())

    def set_download_preferences(
        self,
        selected_format: str,
        selected_quality: str,
        selected_audio_quality: str,
    ) -> None:
        """Update selected format and quality controls.

        Args:
            selected_format: Selected media format.
            selected_quality: Selected media quality.
        """
        self._initial_quality = selected_quality
        self._initial_audio_quality = selected_audio_quality
        self._set_combo_data(self._format_combo_box, selected_format)
        self._populate_quality_combo_box()

    def _populate_quality_combo_box(self) -> None:
        """Show video resolutions or audio quality values for the active format."""
        selected_format: str = self.selected_format()
        selected_value: str = (
            self._initial_quality if selected_format == "mp4" else self._initial_audio_quality
        )
        self._quality_combo_box.blockSignals(True)
        self._quality_combo_box.clear()
        if selected_format == "mp4":
            options: tuple[tuple[str, str], ...] = (
                ("Best available", "best"),
                ("480p", "480"),
                ("720p", "720"),
                ("1080p", "1080"),
                ("1440p", "1440"),
                ("2160p", "2160"),
            )
        elif selected_format == "mp3":
            options = (
                ("Best / Original", "best"),
                ("128 kbps", "128"),
                ("192 kbps", "192"),
                ("256 kbps", "256"),
                ("320 kbps", "320"),
            )
        else:
            options = (("Best / Original", "best"),)
        for label, value in options:
            self._quality_combo_box.addItem(label, value)
        self._set_combo_data(self._quality_combo_box, selected_value)
        self._quality_combo_box.blockSignals(False)

    def _remember_selected_quality(self) -> None:
        """Remember contextual quality when the user switches output formats."""
        selected_value: str = self.selected_quality()
        if self.selected_format() == "mp4":
            self._initial_quality = selected_value
        else:
            self._initial_audio_quality = selected_value

    @staticmethod
    def _set_combo_data(combo_box: QComboBox, value: str) -> None:
        """Select a combo item by user data."""
        index: int = combo_box.findData(value)
        if index >= 0:
            combo_box.setCurrentIndex(index)

    def set_playlist_preferences(
        self,
        playlist_start_index: int,
        playlist_end_index: int,
        playlist_limit: int,
    ) -> None:
        """Update playlist range controls.

        Args:
            playlist_start_index: Default one-based playlist start index.
            playlist_end_index: Optional playlist end index, or 0 for automatic.
            playlist_limit: Playlist item count used when end is automatic.
        """
        self._playlist_limit = playlist_limit
        self._playlist_start_spin_box.setValue(max(1, playlist_start_index))
        self._playlist_end_spin_box.setValue(max(0, playlist_end_index))

    def _update_action_state(self, text: str) -> None:
        """Enable URL actions when text is available."""
        has_url: bool = bool(text.strip())
        self._add_video_button.setEnabled(has_url)
        self._add_playlist_button.setEnabled(has_url)
        self._load_range_button.setEnabled(has_url)
        self._add_next_playlist_range_button.setEnabled(has_url)

    def _emit_add_video_requested(self) -> None:
        """Emit the add video request."""
        self.add_video_requested.emit(
            self._url_input.text().strip(),
            self.selected_format(),
            self.selected_quality(),
        )
        self._url_input.clear()

    def _emit_add_default_playlist_requested(self) -> None:
        """Emit a playlist request using the default configured range."""
        self.add_playlist_requested.emit(
            self._url_input.text().strip(),
            self.selected_format(),
            self.selected_quality(),
            PlaylistRange.from_optional_end(1, None, self._playlist_limit),
        )
        self._url_input.clear()

    def _emit_add_playlist_requested(self) -> None:
        """Emit the add playlist request."""
        try:
            playlist_range: PlaylistRange = self._selected_playlist_range()
        except ValueError:
            self.playlist_range_error.emit("El fin de playlist debe ser igual o mayor que el inicio.")
            return
        self.add_playlist_requested.emit(
            self._url_input.text().strip(),
            self.selected_format(),
            self.selected_quality(),
            playlist_range,
        )
        self._url_input.clear()

    def _emit_add_next_playlist_range_requested(self) -> None:
        """Emit the add next playlist range request."""
        self.add_next_playlist_range_requested.emit(
            self._url_input.text().strip(),
            self.selected_format(),
            self.selected_quality(),
        )
        self._url_input.clear()

    def _selected_playlist_range(self) -> PlaylistRange:
        """Return the selected playlist range."""
        end_index: int | None = self._playlist_end_spin_box.value()
        if end_index == 0:
            end_index = None
        return PlaylistRange.from_optional_end(
            self._playlist_start_spin_box.value(),
            end_index,
            self._playlist_limit,
        )
