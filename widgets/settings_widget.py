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
        self._format_combo_box: QComboBox
        self._quality_combo_box: QComboBox
        self._theme_combo_box: QComboBox
        self._max_downloads_spin_box: QSpinBox
        self.setObjectName("settingsWidget")
        self._build_layout()

    def update_settings(self, settings: Settings) -> None:
        """Update the widget with current settings.

        Args:
            settings: Latest persisted settings.
        """
        self._settings = settings

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

        self._format_combo_box = QComboBox(self)
        self._format_combo_box.addItems(("mp4", "mp3"))
        self._format_combo_box.setCurrentText(self._settings.selected_format)

        self._quality_combo_box = QComboBox(self)
        self._quality_combo_box.addItems(("best", "480", "720", "1080", "1440", "2160"))
        self._quality_combo_box.setCurrentText(self._settings.selected_quality)

        self._theme_combo_box = QComboBox(self)
        self._theme_combo_box.addItems(("dark", "light"))
        self._theme_combo_box.setCurrentText(self._settings.theme)

        self._max_downloads_spin_box = QSpinBox(self)
        self._max_downloads_spin_box.setRange(1, 3)
        self._max_downloads_spin_box.setValue(self._settings.max_concurrent_downloads)

        form_layout.addRow("Carpeta", output_layout)
        form_layout.addRow("Formato", self._format_combo_box)
        form_layout.addRow("Calidad", self._quality_combo_box)
        form_layout.addRow("Tema", self._theme_combo_box)
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

    def _emit_settings_changed(self) -> None:
        """Emit updated settings values."""
        updated_settings: Settings = self._settings.with_preferences(
            output_folder=self._output_folder_input.text().strip() or self._settings.output_folder,
            selected_format=self._format_combo_box.currentText(),
            selected_quality=self._quality_combo_box.currentText(),
            theme=self._theme_combo_box.currentText(),
            max_concurrent_downloads=self._max_downloads_spin_box.value(),
        )
        self.settings_changed.emit(updated_settings)
