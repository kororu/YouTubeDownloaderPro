"""Desktop application entry point."""

from __future__ import annotations

import sys

from core.application import Application


def main() -> int:
    """Start YouTube Downloader Pro.

    Returns:
        The process exit code returned by the Qt event loop.
    """
    with Application(sys.argv) as application:
        return application.run()


if __name__ == "__main__":
    raise SystemExit(main())
