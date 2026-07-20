"""System diagnostics dialog."""

from __future__ import annotations

import platform
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QDialog, QHBoxLayout, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from core.constants import APPLICATION_VERSION
from core.dependency_checker import DependencyChecker


class DiagnosticsDialog(QDialog):
    """Display non-sensitive runtime and dependency diagnostics."""

    def __init__(self, settings_path: Path, history_path: Path, queue_count: int, history_count: int, parent: QWidget | None = None) -> None:
        """Initialize the diagnostics dialog."""
        super().__init__(parent)
        self.setWindowTitle("Diagnóstico")
        self.resize(720, 480)
        result = DependencyChecker().check()
        report = "\n".join((f"Versión app: {APPLICATION_VERSION}", f"Sistema: {platform.platform()}", f"Python: {sys.version.split()[0]}", f"PyInstaller: {'Sí' if getattr(sys, 'frozen', False) else 'No'}", f"yt-dlp: {result.yt_dlp.executable_path or 'No disponible'}", f"ffmpeg: {result.ffmpeg.executable_path or 'No disponible'}", f"Settings: {settings_path}", f"Historial: {history_path}", f"Cola: {queue_count}", f"Entradas historial: {history_count}", "Tema: dark"))
        layout = QVBoxLayout(self)
        output = QPlainTextEdit(report, self); output.setReadOnly(True); layout.addWidget(output)
        actions = QHBoxLayout(); copy = QPushButton("Copiar diagnóstico", self); copy.clicked.connect(lambda: QGuiApplication.clipboard().setText(report)); close = QPushButton("Cerrar", self); close.clicked.connect(self.accept); actions.addWidget(copy); actions.addStretch(1); actions.addWidget(close); layout.addLayout(actions)
