# Changelog

All notable changes to this project will be documented in this file.

## v0.1.0 - 2026-07-07

- Created the initial project scaffold.
- Added the PySide6 application entry point.
- Added project documentation and architecture notes.
- Added Python, VS Code, and PyInstaller ignore rules.
- Added application infrastructure, metadata, and dark theme loading.
- Added JSON settings persistence with safe defaults and invalid JSON recovery.
- Added path, environment, dependency, resource, theme, and logging infrastructure.
- Added a base main window shell with toolbar, queue, log, status, footer, and dependency notice areas.
- Added window size and position persistence.
- Added toolbar controls for URL entry, format selection, quality selection, settings, and about actions.
- Added queue item widgets, queue selection, removal, search, and sorting interactions.
- Added settings, log, status, and about interface components.
- Stabilized Sprint 2 documentation and UI integration.
- Added download domain enums and queue item domain models.
- Added yt-dlp command generation for metadata and future download commands.
- Added subprocess runner foundation.
- Added video metadata extraction service using yt-dlp JSON output.
- Added QThread metadata worker infrastructure.
- Added URL validation, error handling, and metadata loading integration.
- Stabilized Sprint 3 documentation and imports.
- Added playlist metadata models and playlist video selection models.
- Added playlist metadata extraction using yt-dlp JSON output.
- Added PlaylistDialog for selecting playlist videos.
- Added playlist selection integration that adds selected videos to the queue.
- Added playlist error handling and Sprint 4 documentation.
