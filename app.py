"""Application entry point for YouTube Downloader Pro."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication


def main() -> int:
    """Start the Qt application.

    Returns:
        The process exit code returned by the Qt event loop.
    """
    app: QApplication = QApplication(sys.argv)
    app.setApplicationName("YouTube Downloader Pro")
    app.setOrganizationName("YouTube Downloader Pro")
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
