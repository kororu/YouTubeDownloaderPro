"""JSON persistence for the download queue."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config.settings_manager import SettingsManager
from models.download_item import DownloadItem


class QueuePersistenceService:
    """Persists queue items next to application settings."""

    def __init__(self, queue_file: Path | None = None) -> None:
        """Initialize the queue persistence service.

        Args:
            queue_file: Optional explicit queue file path.
        """
        self._queue_file: Path = queue_file or self.default_queue_file()

    @property
    def queue_file(self) -> Path:
        """Return the active queue file path."""
        return self._queue_file

    @staticmethod
    def default_queue_file() -> Path:
        """Resolve the default queue file path.

        Returns:
            Queue JSON path beside the settings file.
        """
        return SettingsManager.default_settings_file().with_name("queue.json")

    def load(self) -> tuple[DownloadItem, ...]:
        """Load persisted queue items.

        Returns:
            Valid persisted queue items.
        """
        if not self._queue_file.exists():
            return ()

        try:
            raw_data: Any = json.loads(self._queue_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return ()

        if not isinstance(raw_data, list):
            return ()

        items: list[DownloadItem] = []
        for raw_item in raw_data:
            if not isinstance(raw_item, dict):
                continue
            try:
                item: DownloadItem = DownloadItem.from_dict(raw_item)
            except ValueError:
                continue
            if item.source_url:
                items.append(item)
        return tuple(items)

    def save(self, items: tuple[DownloadItem, ...]) -> None:
        """Persist queue items.

        Args:
            items: Queue items to persist.
        """
        serialized_data: str = json.dumps(
            [item.to_dict() for item in items],
            indent=4,
            sort_keys=True,
        )
        self._write_text(f"{serialized_data}\n")

    def _write_text(self, text: str) -> None:
        """Write queue JSON, falling back to the system temp path if needed."""
        try:
            self._queue_file.parent.mkdir(parents=True, exist_ok=True)
            self._queue_file.write_text(text, encoding="utf-8")
        except OSError:
            fallback_settings_file: Path = SettingsManager._fallback_settings_file()
            self._queue_file = fallback_settings_file.with_name("queue.json")
            self._queue_file.parent.mkdir(parents=True, exist_ok=True)
            self._queue_file.write_text(text, encoding="utf-8")
