"""Persistence for playlist range progress."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config.settings_manager import SettingsManager
from models.playlist_range import PlaylistRange


class PlaylistRangeHistoryService:
    """Stores the last processed playlist index for each source URL."""

    def __init__(self, history_file: Path | None = None) -> None:
        """Initialize the history service.

        Args:
            history_file: Optional explicit JSON path.
        """
        self._history_file: Path = history_file or self.default_history_file()

    @property
    def history_file(self) -> Path:
        """Return the active history file."""
        return self._history_file

    @staticmethod
    def default_history_file() -> Path:
        """Resolve the default playlist range history path."""
        return SettingsManager.default_settings_file().with_name("playlist_ranges.json")

    def next_range(self, source_url: str, max_items: int, default_start_index: int = 1) -> PlaylistRange:
        """Return the next range for a source URL.

        Args:
            source_url: Playlist or YouTube Mix URL.
            max_items: Number of items to include in the next range.
            default_start_index: Start index used when there is no history.

        Returns:
            Next playlist range.
        """
        history: dict[str, int] = self._load_history()
        last_end_index: int | None = history.get(source_url)
        start_index: int = (last_end_index + 1) if last_end_index is not None else default_start_index
        return PlaylistRange.from_start_and_limit(start_index, max_items)

    def save_completed_range(self, source_url: str, playlist_range: PlaylistRange) -> None:
        """Persist a completed range for a source URL.

        Args:
            source_url: Playlist or YouTube Mix URL.
            playlist_range: Completed playlist range.
        """
        history: dict[str, int] = self._load_history()
        history[source_url] = max(history.get(source_url, 0), playlist_range.end_index)
        self._save_history(history)

    def _load_history(self) -> dict[str, int]:
        """Load valid persisted playlist history."""
        if not self._history_file.exists():
            return {}
        try:
            raw_data: Any = json.loads(self._history_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        if not isinstance(raw_data, dict):
            return {}

        history: dict[str, int] = {}
        for key, value in raw_data.items():
            if isinstance(key, str) and isinstance(value, int) and value >= 1:
                history[key] = value
        return history

    def _save_history(self, history: dict[str, int]) -> None:
        """Persist playlist history."""
        serialized_data: str = json.dumps(history, indent=4, sort_keys=True)
        try:
            self._history_file.parent.mkdir(parents=True, exist_ok=True)
            self._history_file.write_text(f"{serialized_data}\n", encoding="utf-8")
        except OSError:
            fallback_settings_file: Path = SettingsManager._fallback_settings_file()
            self._history_file = fallback_settings_file.with_name("playlist_ranges.json")
            self._history_file.parent.mkdir(parents=True, exist_ok=True)
            self._history_file.write_text(f"{serialized_data}\n", encoding="utf-8")
