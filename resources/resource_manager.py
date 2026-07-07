"""Resource path resolution helpers."""

from __future__ import annotations

from pathlib import Path

from core.paths import AppPaths, get_app_paths


class ResourceManager:
    """Resolves optional application resource paths safely."""

    def __init__(self, app_paths: AppPaths | None = None) -> None:
        """Initialize the resource manager.

        Args:
            app_paths: Optional resolved application paths.
        """
        self._app_paths: AppPaths = app_paths or get_app_paths()

    def resolve_icon(self, file_name: str) -> Path | None:
        """Resolve an icon path.

        Args:
            file_name: Icon file name.

        Returns:
            Existing icon path, or None when the file is unavailable.
        """
        return self._resolve_optional_path(self._app_paths.resources_dir / "icons" / file_name)

    def resolve_image(self, file_name: str) -> Path | None:
        """Resolve an image path.

        Args:
            file_name: Image file name.

        Returns:
            Existing image path, or None when the file is unavailable.
        """
        return self._resolve_optional_path(self._app_paths.resources_dir / "images" / file_name)

    def resolve_style(self, file_name: str) -> Path | None:
        """Resolve a QSS stylesheet path.

        Args:
            file_name: Stylesheet file name.

        Returns:
            Existing stylesheet path, or None when the file is unavailable.
        """
        return self._resolve_optional_path(self._app_paths.styles_dir / file_name)

    def resolve_font(self, file_name: str) -> Path | None:
        """Resolve a font path.

        Args:
            file_name: Font file name.

        Returns:
            Existing font path, or None when the file is unavailable.
        """
        return self._resolve_optional_path(self._app_paths.resources_dir / "fonts" / file_name)

    @staticmethod
    def _resolve_optional_path(path: Path) -> Path | None:
        """Resolve a path only when it exists as a file."""
        if path.is_file():
            return path.resolve()
        return None
