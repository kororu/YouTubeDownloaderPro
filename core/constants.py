"""Project-wide constants for YouTube Downloader Pro."""

from __future__ import annotations

APPLICATION_NAME: str = "YouTube Downloader Pro"
APPLICATION_VERSION: str = "0.5.0"
APPLICATION_AUTHOR: str = "Ariel Ponce"
ORGANIZATION_NAME: str = "YouTube Downloader Pro"

WINDOW_INITIAL_WIDTH: int = 1400
WINDOW_INITIAL_HEIGHT: int = 900
WINDOW_MINIMUM_WIDTH: int = 1100
WINDOW_MINIMUM_HEIGHT: int = 700

PLANNED_WIDGET_CLASSES: tuple[str, ...] = (
    "ToolbarWidget",
    "QueueWidget",
    "FooterWidget",
    "StatusWidget",
    "LogWidget",
)
