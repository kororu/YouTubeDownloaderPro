"""Application settings widget."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from config.settings import Settings


class SettingsWidget(QWidget):
    """Editable application settings panel."""

    settings_changed: Signal = Signal(Settings)

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        """Initialize the settings widget.

        Args:
            settings: Current persisted settings.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._settings: Settings = settings
        self._output_folder_input: QLineEdit
        self._background_image_input: QLineEdit
        self._format_combo_box: QComboBox
        self._quality_combo_box: QComboBox
        self._playlist_limit_combo_box: QComboBox
        self._max_downloads_spin_box: QSpinBox
        self.setObjectName("settingsWidget")
        self._build_layout()

    def update_settings(self, settings: Settings) -> None:
        """Update the widget with current settings.

        Args:
            settings: Latest persisted settings.
        """
        self._settings = settings
        self._output_folder_input.setText(settings.output_folder)
        self._background_image_input.setText(settings.background_image_path)
        self._format_combo_box.setCurrentText(settings.selected_format)
        self._quality_combo_box.setCurrentText(settings.selected_quality)
        self._playlist_limit_combo_box.setCurrentText(self._format_playlist_limit(settings.max_playlist_items))
        self._max_downloads_spin_box.setValue(settings.max_concurrent_downloads)

    def _build_layout(self) -> None:
        """Build settings controls."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title_label: QLabel = QLabel("Ajustes", self)
        title_label.setObjectName("sectionTitle")

        form_layout: QFormLayout = QFormLayout()
        form_layout.setSpacing(10)

        output_layout: QHBoxLayout = QHBoxLayout()
        self._output_folder_input = QLineEdit(self._settings.output_folder, self)
        self._output_folder_input.setObjectName("outputFolderInput")

        browse_button: QPushButton = QPushButton("Elegir", self)
        browse_button.clicked.connect(self._select_output_folder)

        output_layout.addWidget(self._output_folder_input, 1)
        output_layout.addWidget(browse_button)

        background_layout: QHBoxLayout = QHBoxLayout()
        self._background_image_input = QLineEdit(self._settings.background_image_path, self)
        self._background_image_input.setObjectName("backgroundImageInput")
        self._background_image_input.setPlaceholderText("Sin imagen de fondo")

        select_background_button: QPushButton = QPushButton("Elegir", self)
        select_background_button.clicked.connect(self._select_background_image)

        clear_background_button: QPushButton = QPushButton("Quitar", self)
        clear_background_button.clicked.connect(self._clear_background_image)

        background_layout.addWidget(self._background_image_input, 1)
        background_layout.addWidget(select_background_button)
        background_layout.addWidget(clear_background_button)

        self._format_combo_box = QComboBox(self)
        self._format_combo_box.addItems(("mp4", "mp3"))
        self._format_combo_box.setCurrentText(self._settings.selected_format)

        self._quality_combo_box = QComboBox(self)
        self._quality_combo_box.addItems(("best", "480", "720", "1080", "1440", "2160"))
        self._quality_combo_box.setCurrentText(self._settings.selected_quality)

        self._playlist_limit_combo_box = QComboBox(self)
        self._playlist_limit_combo_box.addItems(("50", "100", "200", "500", "Sin límite"))
        self._playlist_limit_combo_box.setCurrentText(self._format_playlist_limit(self._settings.max_playlist_items))

        self._max_downloads_spin_box = QSpinBox(self)
        self._max_downloads_spin_box.setRange(1, 3)
        self._max_downloads_spin_box.setValue(self._settings.max_concurrent_downloads)

        form_layout.addRow("Carpeta", output_layout)
        form_layout.addRow("Fondo", background_layout)
        form_layout.addRow("Formato", self._format_combo_box)
        form_layout.addRow("Calidad", self._quality_combo_box)
        form_layout.addRow("Límite playlist", self._playlist_limit_combo_box)
        form_layout.addRow("Descargas", self._max_downloads_spin_box)

        save_button: QPushButton = QPushButton("Guardar ajustes", self)
        save_button.clicked.connect(self._emit_settings_changed)

        layout.addWidget(title_label)
        layout.addLayout(form_layout)
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
        """Open a file picker for the optional background image."""
        selected_file, _selected_filter = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen de fondo",
            self._background_image_input.text() or self._settings.output_folder,
            "Images (*.png *.jpg *.jpeg *.webp)",
        )
        if selected_file:
            self._background_image_input.setText(selected_file)

    def _clear_background_image(self) -> None:
        """Clear the optional background image path."""
        self._background_image_input.clear()

    def _emit_settings_changed(self) -> None:
        """Emit updated settings values."""
        playlist_limit: int = self._parse_playlist_limit()
        if playlist_limit == 0 and self._settings.max_playlist_items != 0:
            confirmation: QMessageBox.StandardButton = QMessageBox.warning(
                self,
                "Confirmar playlist sin límite",
                (
                    "Procesar playlists sin límite puede ralentizar o bloquear la aplicación.\n\n"
                    "¿Desea guardar esta configuración?"
                ),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if confirmation is not QMessageBox.StandardButton.Yes:
                self._playlist_limit_combo_box.setCurrentText(
                    self._format_playlist_limit(self._settings.max_playlist_items)
                )
                return

        updated_settings: Settings = self._settings.with_preferences(
            output_folder=self._output_folder_input.text().strip() or self._settings.output_folder,
            selected_format=self._format_combo_box.currentText(),
            selected_quality=self._quality_combo_box.currentText(),
            background_image_path=self._background_image_input.text().strip(),
            max_playlist_items=playlist_limit,
            max_concurrent_downloads=self._max_downloads_spin_box.value(),
        )
        self.settings_changed.emit(updated_settings)

    def _parse_playlist_limit(self) -> int:
        """Read selected playlist limit from the combo box."""
        selected_limit: str = self._playlist_limit_combo_box.currentText()
        if selected_limit == "Sin límite":
            return 0
        return int(selected_limit)

    @staticmethod
    def _format_playlist_limit(max_playlist_items: int) -> str:
        """Format a playlist limit for display."""
        if max_playlist_items == 0:
            return "Sin límite"
        return str(max_playlist_items)
