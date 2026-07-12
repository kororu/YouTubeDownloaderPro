"""Download output template construction."""

from __future__ import annotations

import re
from pathlib import Path

from models.download_item import DownloadItem

INVALID_WINDOWS_PATH_CHARACTERS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


class OutputTemplateBuilder:
    """Build yt-dlp output templates from queue item preferences."""

    def build(self, output_folder: Path, download_item: DownloadItem) -> str:
        """Build an output template inside the selected base folder.

        Args:
            output_folder: User-selected base output folder.
            download_item: Queue item containing naming preferences.

        Returns:
            Complete yt-dlp output template path.
        """
        path: Path = output_folder
        if download_item.create_channel_folder:
            path /= "%(channel,uploader)s"
        if download_item.create_playlist_folder and download_item.playlist_title:
            playlist_folder: str = self._sanitize_path_segment(download_item.playlist_title)
            if playlist_folder:
                path /= playlist_folder
        return str(path / download_item.filename_template)

    @staticmethod
    def _sanitize_path_segment(value: str) -> str:
        """Sanitize a known metadata value for use as a Windows folder name."""
        sanitized_value: str = INVALID_WINDOWS_PATH_CHARACTERS.sub("_", value).strip().rstrip(".")
        return sanitized_value[:120]
