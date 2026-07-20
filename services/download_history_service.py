"""JSON-backed download history persistence and duplicate lookup."""

from __future__ import annotations

import json
from pathlib import Path

from core.url_identity import extract_youtube_video_id, normalize_url_for_comparison
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

    def remove(self, history_id: str) -> bool:
        """Remove one history record without touching its output file.

        Args:
            history_id: Identifier of the persisted history record.

        Returns:
            True when a record was removed.
        """
        records = self.load()
        updated = tuple(item for item in records if item.history_id != history_id)
        if len(updated) == len(records):
            return False
        self.save(updated)
        return True

    def completed_entries_without_available_file(self) -> tuple[DownloadHistoryItem, ...]:
        """Return completed history records whose output file cannot be found."""
        return tuple(
            item
            for item in self.load()
            if item.status == "completed" and not self.is_completed_download_available(item)
        )

    def remove_completed_entries_without_available_file(self) -> int:
        """Remove completed records whose output file cannot be found.

        Returns:
            Number of history records removed. Files on disk are never removed.
        """
        records = self.load()
        missing_ids = {
            item.history_id
            for item in records
            if item.status == "completed" and not self.is_completed_download_available(item)
        }
        if not missing_ids:
            return 0
        self.save(tuple(item for item in records if item.history_id not in missing_ids))
        return len(missing_ids)

    def is_completed(self, duplicate_key: str) -> bool:
        """Return whether the same video or normalized URL completed before."""
        return any(item.normalized_url == duplicate_key and item.status == "completed" for item in self.load())

    def find_by_video_id(self, video_id: str) -> DownloadHistoryItem | None:
        """Find the most recent completed record for a YouTube video identifier."""
        normalized_video_id = video_id.strip()
        if not normalized_video_id:
            return None
        for item in self.load():
            if item.status != "completed":
                continue
            if item.video_id == normalized_video_id or item.normalized_url == f"video:{normalized_video_id}":
                return item
            if extract_youtube_video_id(item.source_url) == normalized_video_id:
                return item
        return None

    def find_by_normalized_url(self, source_url: str) -> DownloadHistoryItem | None:
        """Find the most recent completed record whose URL matches locally."""
        normalized_url = normalize_url_for_comparison(source_url)
        expected_key = f"url:{normalized_url}"
        for item in self.load():
            if item.status != "completed":
                continue
            if item.normalized_url in {expected_key, normalized_url}:
                return item
            if any(
                normalize_url_for_comparison(candidate) == normalized_url
                for candidate in (item.source_url, item.url)
                if candidate
            ):
                return item
        return None

    def find_by_original_url(self, source_url: str) -> DownloadHistoryItem | None:
        """Find a completed record whose stored source or original URL matches exactly."""
        original_url = source_url.strip()
        return next(
            (
                item
                for item in self.load()
                if item.status == "completed" and original_url in {item.source_url, item.url}
            ),
            None,
        )

    def is_completed_download_available(self, entry: DownloadHistoryItem) -> bool:
        """Return whether a completed history record points to an existing file."""
        if entry.status != "completed" or not entry.output_path:
            return False
        try:
            return Path(entry.output_path).is_file()
        except OSError:
            return False

    def get_completed_entry_for_url(self, source_url: str) -> DownloadHistoryItem | None:
        """Find a completed record by YouTube ID, normalized URL, or original URL."""
        video_id = extract_youtube_video_id(source_url)
        if video_id is not None:
            entry = self.find_by_video_id(video_id)
            if entry is not None:
                return entry
        entry = self.find_by_normalized_url(source_url)
        if entry is not None:
            return entry
        return self.find_by_original_url(source_url)

    def is_completed_file_available(self, duplicate_key: str) -> bool:
        """Return whether a matching completed record still has its output file."""
        for item in self.load():
            if item.normalized_url != duplicate_key or item.status != "completed" or not item.output_path:
                continue
            if self.is_completed_download_available(item):
                return True
        return False

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
