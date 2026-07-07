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

## Engineering Standards

- Python 3.12+ is the supported runtime.
- Public functions, methods, and modules must include type hints.
- Production code should use Google style docstrings where documentation clarifies behavior.
- UI code should remain separate from domain and service logic.
- No placeholder implementations, pseudocode, or TODO comments should be committed.
