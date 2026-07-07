"""JSON-backed settings persistence."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from config.settings import Settings
from core.constants import APPLICATION_NAME


class SettingsManager:
    """Loads and saves application settings in the user config directory."""

    def __init__(self, settings_file: Path | None = None) -> None:
        """Initialize the settings manager.

        Args:
            settings_file: Optional explicit settings file path.
        """
        self._settings_file: Path = settings_file or self.default_settings_file()

    @property
    def settings_file(self) -> Path:
        """Return the active settings file path."""
        return self._settings_file

    @staticmethod
    def default_settings_file() -> Path:
        """Resolve the default settings file path.

        Returns:
            A path inside the current user's config directory.
        """
        app_data: str | None = os.environ.get("APPDATA")
        base_path: Path = Path(app_data) if app_data else Path.home() / ".config"
        return base_path / APPLICATION_NAME.replace(" ", "") / "settings.json"

    def load(self) -> Settings:
        """Load settings from disk.

        Returns:
            Current settings, creating or repairing the file when needed.
        """
        if not self._settings_file.exists():
            settings: Settings = Settings.defaults()
            self.save(settings)
            return settings

        try:
            raw_data: Any = json.loads(self._settings_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            settings = Settings.defaults()
            self.save(settings)
            return settings

        if not isinstance(raw_data, dict):
            settings = Settings.defaults()
            self.save(settings)
            return settings

        settings = Settings.from_dict(raw_data)
        self.save(settings)
        return settings

    def save(self, settings: Settings) -> None:
        """Persist settings to disk.

        Args:
            settings: Settings instance to write.
        """
        self._settings_file.parent.mkdir(parents=True, exist_ok=True)
        serialized_settings: str = json.dumps(settings.to_dict(), indent=4, sort_keys=True)
        self._settings_file.write_text(f"{serialized_settings}\n", encoding="utf-8")
