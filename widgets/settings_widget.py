"""Application settings widget."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from config.settings import Settings

FORMAT_OPTIONS: tuple[tuple[str, str], ...] = (
    ("Video MP4", "mp4"),
    ("Audio MP3", "mp3"),
    ("Audio M4A", "m4a"),
    ("Audio OPUS", "opus"),
    ("Audio FLAC", "flac"),
    ("Audio WAV", "wav"),
    ("Audio original / best audio", "best_audio"),
)
FILENAME_TEMPLATES: tuple[tuple[str, str], ...] = (
    ("Título", "%(title)s.%(ext)s"),
    ("Canal - título", "%(channel)s - %(title)s.%(ext)s"),
    ("Índice playlist - título", "%(playlist_index)s - %(title)s.%(ext)s"),
    ("Fecha - título", "%(upload_date)s - %(title)s.%(ext)s"),
)


class SettingsWidget(QWidget):
    """Editable application settings panel."""

    settings_changed: Signal = Signal(Settings)
    settings_warning: Signal = Signal(str)

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        """Initialize the settings widget.

        Args:
            settings: Current persisted settings.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._settings: Settings = settings
        self.setObjectName("settingsWidget")
        self._build_layout()
        self.update_settings(settings)

    def update_settings(self, settings: Settings) -> None:
        """Update all controls with current settings."""
        self._settings = settings
        self._output_folder_input.setText(settings.output_folder)
        self._background_image_input.setText(settings.background_image_path)
        self._set_combo_data(self._format_combo_box, settings.selected_format)
        self._set_combo_data(self._video_quality_combo_box, settings.selected_quality)
        self._set_combo_data(self._audio_quality_combo_box, settings.selected_audio_quality)
        self._download_thumbnail_checkbox.setChecked(settings.download_thumbnail)
        self._write_metadata_checkbox.setChecked(settings.write_metadata)
        self._write_subtitles_checkbox.setChecked(settings.write_subtitles)
        self._write_auto_subtitles_checkbox.setChecked(settings.write_auto_subtitles)
        self._subtitle_languages_input.setText(settings.subtitle_languages)
        self._set_filename_template(settings.filename_template)
        self._create_channel_folder_checkbox.setChecked(settings.create_channel_folder)
        self._create_playlist_folder_checkbox.setChecked(settings.create_playlist_folder)
        self._playlist_limit_combo_box.setCurrentText(str(settings.max_playlist_items))
        self._playlist_start_spin_box.setValue(settings.playlist_start_index)
        self._playlist_end_spin_box.setValue(settings.playlist_end_index)
        self._max_downloads_spin_box.setValue(settings.max_concurrent_downloads)
        self._update_format_controls()
        self._update_subtitle_controls()

    def _build_layout(self) -> None:
        """Build scrollable settings controls."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        title_label: QLabel = QLabel("Ajustes", self)
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)

        scroll_area: QScrollArea = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        content: QWidget = QWidget(scroll_area)
        form_layout: QFormLayout = QFormLayout(content)
        form_layout.setSpacing(9)

        self._output_folder_input = QLineEdit(content)
        output_layout: QHBoxLayout = QHBoxLayout()
        output_layout.addWidget(self._output_folder_input, 1)
        output_button: QPushButton = QPushButton("Elegir", content)
        output_button.clicked.connect(self._select_output_folder)
        output_layout.addWidget(output_button)

        self._background_image_input = QLineEdit(content)
        self._background_image_input.setPlaceholderText("Sin imagen de fondo")
        background_layout: QHBoxLayout = QHBoxLayout()
        background_layout.addWidget(self._background_image_input, 1)
        background_button: QPushButton = QPushButton("Elegir", content)
        background_button.clicked.connect(self._select_background_image)
        background_layout.addWidget(background_button)
        clear_background_button: QPushButton = QPushButton("Quitar", content)
        clear_background_button.clicked.connect(self._background_image_input.clear)
        background_layout.addWidget(clear_background_button)

        self._format_combo_box = QComboBox(content)
        for label, value in FORMAT_OPTIONS:
            self._format_combo_box.addItem(label, value)
        self._format_combo_box.currentIndexChanged.connect(self._update_format_controls)

        self._video_quality_combo_box = QComboBox(content)
        for label, value in (
            ("Best available", "best"),
            ("480p", "480"),
            ("720p", "720"),
            ("1080p", "1080"),
            ("1440p", "1440"),
            ("2160p", "2160"),
        ):
            self._video_quality_combo_box.addItem(label, value)

        self._audio_quality_combo_box = QComboBox(content)
        for label, value in (
            ("Best / Original", "best"),
            ("128 kbps", "128"),
            ("192 kbps", "192"),
            ("256 kbps", "256"),
            ("320 kbps", "320"),
        ):
            self._audio_quality_combo_box.addItem(label, value)
        self._audio_quality_combo_box.setToolTip("El bitrate solo se aplica a MP3")

        self._download_thumbnail_checkbox = QCheckBox("Descargar miniatura", content)
        self._write_metadata_checkbox = QCheckBox("Guardar metadata", content)
        self._write_subtitles_checkbox = QCheckBox("Descargar subtítulos", content)
        self._write_auto_subtitles_checkbox = QCheckBox("Subtítulos automáticos", content)
        self._write_subtitles_checkbox.toggled.connect(self._update_subtitle_controls)
        self._write_auto_subtitles_checkbox.toggled.connect(self._update_subtitle_controls)
        self._subtitle_languages_input = QLineEdit(content)
        self._subtitle_languages_input.setPlaceholderText("es,en")

        self._filename_template_combo_box = QComboBox(content)
        for label, template in FILENAME_TEMPLATES:
            self._filename_template_combo_box.addItem(label, template)
        self._filename_template_combo_box.addItem("Personalizada", "custom")
        self._filename_template_combo_box.currentIndexChanged.connect(self._update_custom_template_state)
        self._custom_filename_template_input = QLineEdit(content)
        self._custom_filename_template_input.setPlaceholderText("%(title)s.%(ext)s")

        self._create_channel_folder_checkbox = QCheckBox("Crear carpeta por canal", content)
        self._create_playlist_folder_checkbox = QCheckBox("Crear carpeta por playlist", content)

        self._playlist_limit_combo_box = QComboBox(content)
        self._playlist_limit_combo_box.addItems(("50", "100", "200", "500"))
        self._playlist_start_spin_box = QSpinBox(content)
        self._playlist_start_spin_box.setRange(1, 100000)
        self._playlist_end_spin_box = QSpinBox(content)
        self._playlist_end_spin_box.setRange(0, 100000)
        self._playlist_end_spin_box.setSpecialValueText("Auto")
        self._max_downloads_spin_box = QSpinBox(content)
        self._max_downloads_spin_box.setRange(1, 3)

        form_layout.addRow("Carpeta", output_layout)
        form_layout.addRow("Fondo", background_layout)
        form_layout.addRow("Formato", self._format_combo_box)
        form_layout.addRow("Calidad video", self._video_quality_combo_box)
        form_layout.addRow("Calidad MP3", self._audio_quality_combo_box)
        form_layout.addRow("Archivos extra", self._download_thumbnail_checkbox)
        form_layout.addRow("", self._write_metadata_checkbox)
        form_layout.addRow("Subtítulos", self._write_subtitles_checkbox)
        form_layout.addRow("", self._write_auto_subtitles_checkbox)
        form_layout.addRow("Idiomas", self._subtitle_languages_input)
        form_layout.addRow("Nombre", self._filename_template_combo_box)
        form_layout.addRow("Plantilla custom", self._custom_filename_template_input)
        form_layout.addRow("Organización", self._create_channel_folder_checkbox)
        form_layout.addRow("", self._create_playlist_folder_checkbox)
        form_layout.addRow("Límite playlist", self._playlist_limit_combo_box)
        form_layout.addRow("Inicio playlist", self._playlist_start_spin_box)
        form_layout.addRow("Fin playlist", self._playlist_end_spin_box)
        form_layout.addRow("Descargas", self._max_downloads_spin_box)
        scroll_area.setWidget(content)
        layout.addWidget(scroll_area, 1)

        save_button: QPushButton = QPushButton("Guardar ajustes", self)
        save_button.clicked.connect(self._emit_settings_changed)
        layout.addWidget(save_button)

    def _select_output_folder(self) -> None:
        """Open a folder picker for the output folder."""
        selected_folder: str = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta de salida",
            self._output_folder_input.text(),
        )
        if selected_folder:
            self._output_folder_input.setText(selected_folder)

    def _select_background_image(self) -> None:
        """Open a picker for the optional background image."""
        selected_file, _selected_filter = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen de fondo",
            self._background_image_input.text() or self._settings.output_folder,
            "Images (*.png *.jpg *.jpeg *.webp)",
        )
        if selected_file:
            self._background_image_input.setText(selected_file)

    def _emit_settings_changed(self) -> None:
        """Validate and emit updated settings values."""
        start_index: int = self._playlist_start_spin_box.value()
        end_index: int = self._playlist_end_spin_box.value()
        if 0 < end_index < start_index:
            self.settings_warning.emit("El fin de playlist debe ser mayor o igual al inicio.")
            return
        if end_index > 0 and end_index - start_index + 1 > 500:
            self.settings_warning.emit("El rango de playlist no puede superar 500 videos.")
            return

        filename_template: str = self._selected_filename_template()
        if not filename_template:
            self.settings_warning.emit("La plantilla de nombre personalizada no puede estar vacía.")
            return
        if "/" in filename_template or "\\" in filename_template or ".." in filename_template:
            self.settings_warning.emit("La plantilla de nombre no puede contener rutas ni '..'.")
            return

        updated_settings: Settings = self._settings.with_preferences(
            output_folder=self._output_folder_input.text().strip() or self._settings.output_folder,
            selected_format=str(self._format_combo_box.currentData()),
            selected_quality=str(self._video_quality_combo_box.currentData()),
            selected_audio_quality=str(self._audio_quality_combo_box.currentData()),
            background_image_path=self._background_image_input.text().strip(),
            download_thumbnail=self._download_thumbnail_checkbox.isChecked(),
            write_metadata=self._write_metadata_checkbox.isChecked(),
            write_subtitles=self._write_subtitles_checkbox.isChecked(),
            write_auto_subtitles=self._write_auto_subtitles_checkbox.isChecked(),
            subtitle_languages=self._subtitle_languages_input.text(),
            filename_template=filename_template,
            create_channel_folder=self._create_channel_folder_checkbox.isChecked(),
            create_playlist_folder=self._create_playlist_folder_checkbox.isChecked(),
            max_playlist_items=int(self._playlist_limit_combo_box.currentText()),
            playlist_start_index=start_index,
            playlist_end_index=end_index,
            max_concurrent_downloads=self._max_downloads_spin_box.value(),
        )
        self.settings_changed.emit(updated_settings)
        self._emit_option_warnings(updated_settings)

    def _emit_option_warnings(self, settings: Settings) -> None:
        """Emit non-blocking warnings for options that create extra files."""
        if settings.selected_format == "wav":
            self.settings_warning.emit(
                "WAV genera archivos grandes y no recupera calidad perdida en la fuente."
            )
        if settings.selected_format == "best_audio":
            self.settings_warning.emit("Audio original puede conservar una extensión distinta según la fuente.")
        if settings.download_thumbnail:
            self.settings_warning.emit("Miniatura habilitada: se generará un archivo adicional.")
        if settings.write_metadata:
            self.settings_warning.emit("Metadata habilitada: se generará un archivo JSON adicional.")
        if settings.write_auto_subtitles:
            self.settings_warning.emit("Los subtítulos automáticos pueden no estar disponibles.")

    def _update_format_controls(self) -> None:
        """Enable only the quality control relevant to the selected format."""
        selected_format: str = str(self._format_combo_box.currentData())
        self._video_quality_combo_box.setEnabled(selected_format == "mp4")
        self._audio_quality_combo_box.setEnabled(selected_format == "mp3")

    def _update_subtitle_controls(self) -> None:
        """Enable language selection when subtitle output is requested."""
        subtitles_enabled: bool = (
            self._write_subtitles_checkbox.isChecked()
            or self._write_auto_subtitles_checkbox.isChecked()
        )
        self._subtitle_languages_input.setEnabled(subtitles_enabled)

    def _update_custom_template_state(self) -> None:
        """Enable the custom template field only for the custom preset."""
        self._custom_filename_template_input.setEnabled(
            self._filename_template_combo_box.currentData() == "custom"
        )

    def _selected_filename_template(self) -> str:
        """Return the selected preset or custom filename template."""
        selected_template: str = str(self._filename_template_combo_box.currentData())
        if selected_template == "custom":
            return self._custom_filename_template_input.text().strip()
        return selected_template

    def _set_filename_template(self, filename_template: str) -> None:
        """Select a known template or configure the custom field."""
        for index in range(self._filename_template_combo_box.count()):
            if self._filename_template_combo_box.itemData(index) == filename_template:
                self._filename_template_combo_box.setCurrentIndex(index)
                self._custom_filename_template_input.clear()
                self._update_custom_template_state()
                return
        self._set_combo_data(self._filename_template_combo_box, "custom")
        self._custom_filename_template_input.setText(filename_template)
        self._update_custom_template_state()

    @staticmethod
    def _set_combo_data(combo_box: QComboBox, value: str) -> None:
        """Select a combo item by user data."""
        index: int = combo_box.findData(value)
        if index >= 0:
            combo_box.setCurrentIndex(index)
