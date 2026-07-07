"""Application configuration values."""

from __future__ import annotations

from dataclasses import dataclass

from core.constants import (
    APPLICATION_AUTHOR,
    APPLICATION_NAME,
    APPLICATION_VERSION,
    ORGANIZATION_NAME,
    PLANNED_WIDGET_CLASSES,
    WINDOW_INITIAL_HEIGHT,
    WINDOW_INITIAL_WIDTH,
    WINDOW_MINIMUM_HEIGHT,
    WINDOW_MINIMUM_WIDTH,
)


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Immutable runtime configuration for the desktop application.

    Attributes:
        application_name: Human-readable application name.
        application_version: Semantic application version.
        author: Application author.
        organization_name: Qt organization name.
        window_initial_width: Initial main window width in pixels.
        window_initial_height: Initial main window height in pixels.
        window_minimum_width: Minimum main window width in pixels.
        window_minimum_height: Minimum main window height in pixels.
        planned_widget_classes: Future widget class names reserved by the UI layer.
    """

    application_name: str = APPLICATION_NAME
    application_version: str = APPLICATION_VERSION
    author: str = APPLICATION_AUTHOR
    organization_name: str = ORGANIZATION_NAME
    window_initial_width: int = WINDOW_INITIAL_WIDTH
    window_initial_height: int = WINDOW_INITIAL_HEIGHT
    window_minimum_width: int = WINDOW_MINIMUM_WIDTH
    window_minimum_height: int = WINDOW_MINIMUM_HEIGHT
    planned_widget_classes: tuple[str, ...] = PLANNED_WIDGET_CLASSES
