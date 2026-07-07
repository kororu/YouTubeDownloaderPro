# Project Architecture

YouTube Downloader Pro follows a modular clean architecture style. The project separates application startup, domain concepts, services, presentation code, styling, resources, and tests so each area can evolve independently.

## Structure

```text
YouTubeDownloaderPro/
    app.py
    requirements.txt
    README.md
    CHANGELOG.md
    PROJECT.md
    TODO.md
    AGENTS.md
    .gitignore
    config/
    core/
    models/
    services/
    ui/
    widgets/
    dialogs/
    resources/
    styles/
    downloads/
    tests/
```

## Layers

- `app.py`: Delegates process startup to the application container.
- `config`: Stores typed application configuration and JSON-backed user settings.
- `core`: Contains application lifecycle, constants, paths, environment detection, dependency checks, and logging.
- `models`: Contains typed domain and data models.
- `services`: Contains integrations and business services, such as future download, validation, metadata, and persistence services.
- `ui`: Contains main windows, screens, and presentation composition.
- `widgets`: Contains reusable PySide6 widgets for the main shell.
- `dialogs`: Contains dialog windows and modal workflows.
- `resources`: Contains application assets and safe resource resolution helpers.
- `styles`: Contains Qt style sheets and centralized theme management.
- `downloads`: Provides the default local download target folder.
- `tests`: Contains automated tests.

## Sprint 1 Infrastructure

- `Application` encapsulates `QApplication`, metadata, theme application, settings loading, logging, and main window startup.
- `SettingsManager` persists user settings as JSON in the user configuration directory.
- `DependencyChecker` verifies `yt-dlp` and `ffmpeg` availability through the system `PATH`.
- `ThemeManager` centralizes QSS loading and applies the configured theme safely.
- `ResourceManager` resolves optional icons, images, styles, and fonts without crashing when files are absent.
- `MainWindow` provides the base shell and persists window geometry on close.

## Sprint 2 Interface

- `ToolbarWidget` provides URL entry, format and quality controls, and high-level actions.
- `QueueWidget` uses `QScrollArea` with `QueueItemWidget` instances for queue display.
- Queue interactions support add, remove, select all, deselect all, search, and sort operations without download execution.
- `SettingsWidget` edits persisted user preferences through the configuration layer.
- `LogWidget` and `StatusWidget` provide visible application feedback.
- `AboutDialog` displays application metadata without coupling to download services.

## Sprint 3 Metadata Engine

- `models` contains download enums, queue item state, and extracted video metadata.
- `YtDlpCommandBuilder` builds command arguments without executing them.
- `SubprocessRunner` centralizes external command execution and output capture.
- `VideoMetadataService` extracts single-video metadata through `yt-dlp --dump-single-json`.
- `MetadataWorker` loads metadata on a `QThread` so the UI remains responsive.
- `UrlValidator` validates user-entered URLs before service execution.
- UI integration adds metadata-backed queue entries and reports dependency or extraction errors without starting downloads.

## Sprint 4 Playlists

- `PlaylistMetadata` and `PlaylistVideo` model playlist analysis results.
- `PlaylistMetadataService` extracts playlist data through `yt-dlp --dump-single-json`.
- `PlaylistWorker` runs playlist analysis on a `QThread`.
- `PlaylistDialog` lets the user search, select, deselect, and confirm playlist videos.
- Selected playlist videos are added to the queue as ready metadata-backed items.
- Playlist dependency and extraction errors are reported through the existing log and status widgets.

## Engineering Standards

- Python 3.12+ is the supported runtime.
- Public functions, methods, and modules must include type hints.
- Production code should use Google style docstrings where documentation clarifies behavior.
- UI code should remain separate from domain and service logic.
- No placeholder implementations, pseudocode, or TODO comments should be committed.
