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

- `app.py`: Starts the `QApplication` and owns process-level application bootstrapping.
- `config`: Stores configuration modules and constants.
- `core`: Contains core application rules, shared abstractions, and orchestration code.
- `models`: Contains typed domain and data models.
- `services`: Contains integrations and business services, such as future download, validation, metadata, and persistence services.
- `ui`: Contains main windows, screens, and presentation composition.
- `widgets`: Contains reusable PySide6 widgets.
- `dialogs`: Contains dialog windows and modal workflows.
- `resources`: Contains application assets.
- `styles`: Contains Qt style sheets and visual theme assets.
- `downloads`: Provides the default local download target folder.
- `tests`: Contains automated tests.

## Engineering Standards

- Python 3.12+ is the supported runtime.
- Public functions, methods, and modules must include type hints.
- Production code should use Google style docstrings where documentation clarifies behavior.
- UI code should remain separate from domain and service logic.
- No placeholder implementations, pseudocode, or TODO comments should be committed.
