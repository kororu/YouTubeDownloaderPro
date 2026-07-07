"""Dependency status and installation guidance widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import QApplication, QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from core.dependency_checker import DependencyCheckResult, DependencyStatus

INSTALL_COMMANDS: str = "winget install yt-dlp\nwinget install ffmpeg"


class DependencyNoticeWidget(QFrame):
    """Panel showing external dependency availability."""

    def __init__(self, dependency_result: DependencyCheckResult, parent: QWidget | None = None) -> None:
        """Initialize the dependency notice widget.

        Args:
            dependency_result: Current dependency check result.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._dependency_result: DependencyCheckResult = dependency_result
        self.setObjectName("dependencyNoticeWidget")
        self._build_layout()

    def _build_layout(self) -> None:
        """Build dependency status content."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title_label: QLabel = QLabel("Dependencias", self)
        title_label.setObjectName("sectionTitle")

        yt_dlp_label: QLabel = QLabel(self._format_dependency(self._dependency_result.yt_dlp), self)
        ffmpeg_label: QLabel = QLabel(self._format_dependency(self._dependency_result.ffmpeg), self)

        layout.addWidget(title_label)
        layout.addWidget(yt_dlp_label)
        layout.addWidget(ffmpeg_label)

        if not self._dependency_result.all_available:
            instructions_label: QLabel = QLabel(
                "Si yt-dlp o ffmpeg no están instalados, copie y ejecute estos comandos en PowerShell",
                self,
            )
            instructions_label.setWordWrap(True)

            commands_label: QLabel = QLabel(INSTALL_COMMANDS, self)
            commands_label.setObjectName("commandLabel")
            commands_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            copy_button: QPushButton = QPushButton("Copiar comandos", self)
            copy_button.clicked.connect(self._copy_install_commands)

            layout.addSpacing(8)
            layout.addWidget(instructions_label)
            layout.addWidget(commands_label)
            layout.addWidget(copy_button)

        layout.addStretch(1)

    @staticmethod
    def _format_dependency(status: DependencyStatus) -> str:
        """Format dependency status for display."""
        state: str = "disponible" if status.is_available else "no encontrado"
        return f"{status.name}: {state}"

    def _copy_install_commands(self) -> None:
        """Copy install commands to the system clipboard."""
        clipboard: QClipboard = QApplication.clipboard()
        clipboard.setText(INSTALL_COMMANDS)
