"""JSON-backed download history persistence and duplicate lookup."""

from __future__ import annotations

import json
from pathlib import Path

from models.download_history_item import DownloadHistoryItem


class DownloadHistoryService:
    """Persist download records without UI dependencies."""

    def __init__(self, history_path: Path | None = None) -> None:
        """Initialize service with an optional history path."""
        self._history_path = history_path or Path.home() / ".youtube_downloader_pro" / "download_history.json"

    def load(self) -> tuple[DownloadHistoryItem, ...]:
        """Load valid records, recovering safely from corrupt JSON."""
        try:
            raw = json.loads(self._history_path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                return ()
            return tuple(DownloadHistoryItem.from_dict(item) for item in raw if isinstance(item, dict))
        except (OSError, ValueError, json.JSONDecodeError, TypeError):
            return ()

    def save(self, items: tuple[DownloadHistoryItem, ...]) -> None:
        """Persist records atomically enough for local application settings."""
        self._history_path.parent.mkdir(parents=True, exist_ok=True)
        self._history_path.write_text(json.dumps([item.to_dict() for item in items], ensure_ascii=False, indent=2), encoding="utf-8")

    def record(self, item: DownloadHistoryItem) -> tuple[DownloadHistoryItem, ...]:
        """Upsert a history record and return the updated collection."""
        records = tuple(existing for existing in self.load() if existing.history_id != item.history_id)
        updated = (item, *records)
        self.save(updated)
        return updated

    def is_completed(self, duplicate_key: str) -> bool:
        """Return whether the same video or normalized URL completed before."""
        return any(item.normalized_url == duplicate_key and item.status == "completed" for item in self.load())

    def clear(self) -> None:
        """Clear all persisted history records."""
        self.save(())

    def export_to(self, destination: Path) -> None:
        """Export the current history JSON to a user-selected file."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps([item.to_dict() for item in self.load()], ensure_ascii=False, indent=2), encoding="utf-8")

    def import_from(self, source: Path) -> tuple[DownloadHistoryItem, ...]:
        """Import valid records, merging them by history identifier."""
        raw = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("History import must be a JSON list")
        imported = tuple(DownloadHistoryItem.from_dict(item) for item in raw if isinstance(item, dict))
        merged = {item.history_id: item for item in self.load()}
        merged.update({item.history_id: item for item in imported})
        result = tuple(sorted(merged.values(), key=lambda item: item.downloaded_at, reverse=True))
        self.save(result)
        return result
