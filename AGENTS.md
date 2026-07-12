# AGENTS.md

# YouTube Downloader Pro — Agent Instructions

## Project Identity

Project name: YouTube Downloader Pro
Author: Ariel Ponce
Visible version: v0.5.0
Target platform: Windows
Final distribution: PyInstaller executable
Main technology stack: Python, PySide6, QThread, subprocess.Popen, yt-dlp, ffmpeg, JSON, QSS

This project is a professional desktop frontend for `yt-dlp` and `ffmpeg`.

The application must behave like a polished open-source desktop project.

---

## Language Rules

The assistant must respond to the user in Spanish.

Source code must remain in English:

* File names
* Folder names
* Class names
* Function names
* Method names
* Variable names
* Constants
* Commit messages
* Technical identifiers
* Logs
* Internal exceptions

User-facing UI text may be in Spanish unless a technical label is clearer in English.

---

## Core Development Rules

Always follow these rules:

* Use Python 3.12+.
* Use PySide6.
* Use Clean Architecture.
* Use modular architecture.
* Use type hints everywhere.
* Use Google style docstrings.
* Never write pseudocode.
* Never write temporary code.
* Never write fake implementations.
* Never leave placeholder logic.
* Never add unused files.
* Never break compatibility with previous commits.
* Never modify unrelated files.
* Keep the application runnable after every commit.
* Prefer small, focused commits.
* Prefer readable production code over clever code.
* Use descriptive names.
* Keep UI code separated from business logic.
* Keep services independent from widgets.
* Keep models free from UI dependencies.
* Keep infrastructure isolated.

---

## Project Structure

The project root must follow this structure:

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

Every Python package must contain:

```text
__init__.py
```

---

## Architecture Rules

Use a clean modular architecture.

Recommended responsibilities:

```text
config/
    Application settings and JSON persistence.

core/
    Application lifecycle, constants, paths, environment, dependency checks, logging.

models/
    Domain models and enums.

services/
    yt-dlp, ffmpeg, queue, playlist and download services.

ui/
    Main windows and high-level UI composition.

widgets/
    Reusable custom PySide6 widgets.

dialogs/
    Modal dialogs.

resources/
    Resource loading helpers.

styles/
    QSS themes and theme management.

downloads/
    Default download output folder.

tests/
    Unit tests.
```

Do not put download logic directly inside widgets.

Do not put subprocess logic directly inside UI components.

Do not put persistent configuration logic directly inside UI components.

---

## UI Rules

The interface must use a professional dark theme inspired by Visual Studio Code.

Do not use `QTreeWidget` as the main queue component.

The main queue must use:

```text
QScrollArea + custom QueueItemWidget
```

The main application must eventually include:

```text
ToolbarWidget
QueueWidget
QueueItemWidget
LogWidget
SettingsWidget
FooterWidget
StatusWidget
PlaylistDialog
AboutDialog
```

The footer must visibly show:

```text
Autor: Ariel Ponce
Versión: v0.5.0
```

Initial main window:

```text
Title: YouTube Downloader Pro
Initial size: 1400x900
Minimum size: 1100x700
```

---

## yt-dlp and ffmpeg Rules

Do not install `yt-dlp` automatically.

Do not install `ffmpeg` automatically.

Only verify whether both are available in the system PATH.

If one or both dependencies are missing, the UI must show a small side panel with:

```text
Si yt-dlp o ffmpeg no están instalados, copie y ejecute estos comandos en PowerShell

winget install yt-dlp

winget install ffmpeg
```

The panel must include a copy button.

---

## Baseline Product Capabilities

The final application must support:

* Add single video URL.
* Add playlist URL.
* Select playlist videos.
* Remove videos from queue.
* Remove multiple queue items.
* Select all.
* Deselect all.
* Search queue.
* Sort queue.
* Download MP4.
* Download MP3.
* Select quality:

  * 480
  * 720
  * 1080
  * 1440
  * 2160
  * Best available
* Select output folder.
* Cancel current download.
* Cancel entire queue.
* Run up to 3 simultaneous downloads.
* Persist settings.
* Persist queue.
* Show logs.
* Show status.

---

## Roadmap oficial hasta v1.0.0

La versión visible permanece en `v0.5.0`. Cada entrada del roadmap debe identificarse como implementada, en progreso, planificada o sugerida. Nunca se debe presentar una función planificada como implementada.

### Estado actual — v0.5.0

Implementado en el working tree, pero pendiente de validación manual completa y release:

* Ejecución silenciosa de procesos `yt-dlp` y `ffmpeg` en Windows.
* Inicio centralizado de subprocess con `CREATE_NO_WINDOW`.
* Carga por rangos de playlists y YouTube Mix.
* Rangos como `1-200`, `201-400` y `401-600`.
* `Cargar siguientes` con progreso por URL.
* Prevención de duplicados por identificador de video o URL.
* Mejoras de cancelación y logs de progreso de playlists.
* Preparación del paquete portable.
* Audio MP3, M4A, OPUS, FLAC, WAV y audio original/best audio.
* Bitrates MP3, miniaturas, metadata, subtítulos y plantillas de nombre.
* Carpetas opcionales por canal y playlist con persistencia compatible.

Todavía se requiere validación manual de descargas MP4/MP3 reales, playlists y Mix grandes, ejecución silenciosa desde el `.exe` y uso del portable en otro PC Windows.

### Releases planificadas

* `v0.4.0 — Queue and playlist advanced management`: orden, prioridades, pausa/reanudación, reintentos, limpieza, progreso por playlist, detección de archivos descargados, importación/exportación de cola e historial básico.
* `v0.5.0 — Audio and format improvements`: implementado en el working tree con MP3, M4A, OPUS, FLAC, WAV, best audio, bitrates MP3, miniaturas, metadata, subtítulos, plantillas de nombres y carpetas por canal o playlist; pendiente de pruebas manuales con medios reales.
* `v0.6.0 — Visual polish and UX`: toolbar agrupada o en dos filas, correcciones de espaciado y recorte, controles mejorados, fondo adaptable, opacidad, modo compacto, miniaturas, iconos, pantallas vacías, tooltips y atajos.
* `v0.7.0 — Download history and duplicate control`: historial buscable, control de duplicados, acciones sobre archivos, reintentos, favoritos e importación/exportación.
* `v0.8.0 — Advanced settings and diagnostics`: ancho de banda cuando sea compatible, concurrencia, cookies opcionales con advertencias, proxy, diagnóstico, dependencias, reset e importación/exportación de ajustes.
* `v0.9.0 — Installer and release candidate`: instalador opcional, ZIP portable, accesos directos, icono y metadata finales, documentación, pruebas en un PC limpio y correcciones finales.
* `v1.0.0 — Stable Windows release`: ejecutable y portable estables, documentación completa, errores robustos, descargas silenciosas, playlists por rango y YouTube Mix estables, audio avanzado con WAV, historial e interfaz clara.

### Versiones futuras después de v1.0

* `v1.1 — Multi-source downloads`: evaluar Facebook, X/Twitter, TikTok, Vimeo, Instagram, SoundCloud, clips/VOD de Twitch y otras fuentes compatibles con `yt-dlp`; detectar el origen y advertir sobre cookies o sesión. No se debe prometer soporte absoluto porque los sitios y `yt-dlp` cambian.
* `v1.2 — Site profiles`: opciones por plataforma, cookies opcionales, errores específicos y ayuda por fuente.
* `v1.3 — Scheduler and automation`: descargas programadas, apagado al finalizar, inicio opcional con Windows y modo de bajo consumo.
* `v1.4 — Remote companion`: evaluar una app Android que controle por WiFi/5G la cola de Windows mientras el PC ejecuta `yt-dlp` y `ffmpeg`.
* `v2.0 — Android evaluation`: evaluar una aplicación Kotlin, Java o Flutter separada, con avisos de datos móviles, modo solo WiFi, gestión de cambios de red, almacenamiento y descargas en segundo plano permitidas. No reutilizar PySide6/PyInstaller en Android.

### Guía sobre WAV

WAV está disponible desde `v0.5.0` mediante `yt-dlp` y FFmpeg. Genera archivos grandes sin compresión, pero no restaura calidad ya perdida en una fuente comprimida. Es útil para edición porque evita otra compresión con pérdida. Para uso normal, MP3, M4A u OPUS suelen ser más prácticos; se debe elegir best audio, FLAC o WAV según la necesidad real.

### Uso responsable

La aplicación es un frontend para `yt-dlp` y `ffmpeg`. Los usuarios deben respetar derechos de autor, términos de servicio y legislación aplicable. El proyecto debe priorizar contenido propio, libre, educativo o autorizado y no debe promover descargas no autorizadas de contenido protegido.

El detalle se mantiene en `PROJECT.md`, el progreso en `PROJECT_STATUS.md` y las tareas en `TODO.md`.

---

## Plan histórico de commits

El siguiente plan de Sprints 1–7 registra el camino original hasta la primera aplicación empaquetada. Es una referencia histórica, no el roadmap vigente. No se debe seleccionar un commit antiguo de esta sección como próxima tarea; se debe usar el roadmap oficial y la solicitud explícita del usuario.

---

## Sprint 1 — Infrastructure (historical)

Sprint goal:

Build the application infrastructure, configuration system, dependency verification and base UI shell.

The application must remain runnable after every commit.

---

### Commit 002 — Application Infrastructure

Status: may already exist.

Create or verify:

```text
core/application.py
core/constants.py
config/app_config.py
ui/main_window.py
styles/dark_theme.qss
```

Modify:

```text
app.py
requirements.txt
README.md
```

Requirements:

* `Application` class encapsulates `QApplication`.
* `MainWindow` inherits `QMainWindow`.
* Load dark theme automatically.
* Set app name.
* Set app version.
* Set organization metadata.
* Main window opens correctly.
* No download logic yet.

---

### Commit 003 — Project Agent Instructions

Create:

```text
AGENTS.md
```

Requirements:

* Add permanent project rules.
* Add architecture rules.
* Add sprint rules.
* Add Codex behavior rules.
* Do not implement code beyond this file.
* Keep the project runnable.

---

### Commit 004 — Settings System

Create:

```text
config/settings.py
config/settings_manager.py
```

Requirements:

* Use JSON persistence.
* Store settings in a safe user config path.
* Provide a typed `Settings` dataclass.
* Provide a `SettingsManager`.
* Automatically create settings file if missing.
* Recover safely from invalid JSON.
* Support:

  * output folder
  * selected format
  * selected quality
  * theme
  * window width
  * window height
  * window x position
  * window y position
  * max concurrent downloads
* Use sensible defaults.
* No UI implementation in this commit.

---

### Commit 005 — Paths and Dependency Checker

Create:

```text
core/paths.py
core/environment.py
core/dependency_checker.py
```

Requirements:

* Detect operating system.
* Detect whether running as frozen PyInstaller executable.
* Resolve project root.
* Resolve resources directory.
* Resolve styles directory.
* Resolve downloads directory.
* Resolve logs directory.
* Verify `yt-dlp` exists using `shutil.which`.
* Verify `ffmpeg` exists using `shutil.which`.
* Return typed dependency check results.
* Do not install anything.
* No UI implementation in this commit.

---

### Commit 006 — Theme Manager

Create:

```text
styles/theme_manager.py
```

Modify:

```text
styles/dark_theme.qss
core/application.py
```

Requirements:

* Theme manager loads QSS files.
* Apply dark theme to `QApplication`.
* Fail gracefully if QSS file is missing.
* Keep dark theme as the permanent application theme.
* Keep styles centralized.
* Keep app runnable.

---

### Commit 007 — Logger

Create:

```text
core/logger.py
```

Requirements:

* Use Python `logging`.
* Use `RotatingFileHandler`.
* Store logs in `logs/`.
* Support:

  * DEBUG
  * INFO
  * WARNING
  * ERROR
* Console logging for development.
* File logging for diagnostics.
* Avoid duplicate handlers.
* Add startup logging in application bootstrap.
* Keep app runnable.

---

### Commit 008 — Resource Manager

Create:

```text
resources/resource_manager.py
```

Requirements:

* Resolve icons.
* Resolve images.
* Resolve QSS style files.
* Resolve fonts.
* Return safe paths.
* Do not crash when optional resources are missing.
* Prepare for future icons and images.
* Keep app runnable.

---

### Commit 009 — MainWindow Layout Skeleton

Modify:

```text
ui/main_window.py
```

Create if needed:

```text
widgets/toolbar_widget.py
widgets/queue_widget.py
widgets/log_widget.py
widgets/status_widget.py
widgets/footer_widget.py
```

Requirements:

* Build a professional main layout.
* Use dark theme.
* Include placeholder-free real widgets.
* Toolbar area.
* Search/filter area.
* Queue area.
* Log area.
* Status area.
* Footer area.
* Footer must show:

  * Autor: Ariel Ponce
  * Versión: v0.5.0
* Do not implement download logic yet.
* Do not use QTreeWidget.
* QueueWidget must be based on QScrollArea.
* Keep app runnable.

---

### Commit 010 — Dependency Warning Panel

Create:

```text
widgets/dependency_notice_widget.py
```

Modify:

```text
ui/main_window.py
```

Requirements:

* Show dependency status for:

  * yt-dlp
  * ffmpeg
* If dependencies are missing, show install instructions.
* Include copy button.
* Copy this exact text to clipboard:

```text
winget install yt-dlp
winget install ffmpeg
```

* Do not install dependencies automatically.
* Use dependency checker from core.
* Keep app runnable.

---

### Commit 011 — Window and Settings Persistence

Modify:

```text
ui/main_window.py
core/application.py
config/settings.py
config/settings_manager.py
```

Requirements:

* Restore window size on startup.
* Restore window position on startup.
* Save window size on close.
* Save window position on close.
* Use SettingsManager.
* Keep default values safe.
* Keep app runnable.

---

### Commit 012 — Sprint 1 Stabilization

Modify as needed:

```text
README.md
CHANGELOG.md
PROJECT.md
TODO.md
requirements.txt
```

Requirements:

* Review all Sprint 1 code.
* Fix imports.
* Remove unused code.
* Remove dead code.
* Ensure app starts with:

```text
python app.py
```

* Update README with:

  * project description
  * requirements
  * winget instructions
  * development setup
  * run command
* Update CHANGELOG.
* Update PROJECT architecture documentation.
* Update TODO.
* Ensure no fake implementations remain.
* Keep app runnable.

---

## Sprint 2 — Interface

Sprint goal:

Build the professional user interface components before implementing download logic.

Planned commits:

```text
Commit 013 - ToolbarWidget
Commit 014 - QueueItemWidget
Commit 015 - QueueWidget interactions
Commit 016 - Search and filtering UI
Commit 017 - Format and quality controls
Commit 018 - SettingsWidget
Commit 019 - LogWidget improvements
Commit 020 - StatusWidget improvements
Commit 021 - AboutDialog
Commit 022 - Sprint 2 stabilization
```

---

## Sprint 3 — yt-dlp Engine

Sprint goal:

Implement metadata extraction and command generation without full queue execution.

Planned commits:

```text
Commit 023 - Download models and enums
Commit 024 - yt-dlp command builder
Commit 025 - Video metadata service
Commit 026 - Subprocess runner foundation
Commit 027 - Worker thread infrastructure
Commit 028 - Metadata loading integration
Commit 029 - Error handling and validation
Commit 030 - Sprint 3 stabilization
```

---

## Sprint 4 — Playlists

Sprint goal:

Support playlist analysis and video selection.

Planned commits:

```text
Commit 031 - Playlist models
Commit 032 - Playlist metadata service
Commit 033 - PlaylistDialog layout
Commit 034 - Playlist selection logic
Commit 035 - Add selected videos to queue
Commit 036 - Playlist error handling
Commit 037 - Sprint 4 stabilization
```

---

## Sprint 5 — Downloads

Sprint goal:

Implement real queue download execution.

Planned commits:

```text
Commit 038 - Download queue service
Commit 039 - Download worker
Commit 040 - Progress parsing
Commit 041 - MP4 download
Commit 042 - MP3 download
Commit 043 - Quality selection
Commit 044 - Output folder selection
Commit 045 - Cancel current download
Commit 046 - Cancel all downloads
Commit 047 - Up to 3 simultaneous downloads
Commit 048 - Sprint 5 stabilization
```

---

## Sprint 6 — Polish

Sprint goal:

Improve UX, resilience, visual consistency and queue persistence.

Planned commits:

```text
Commit 049 - Queue persistence
Commit 050 - Settings persistence improvements
Commit 051 - Better error messages
Commit 052 - Better empty states
Commit 053 - Keyboard shortcuts
Commit 054 - UI polish pass
Commit 055 - Log export
Commit 056 - Sprint 6 stabilization
```

---

## Sprint 7 — Release

Sprint goal:

Package as Windows executable.

Planned commits:

```text
Commit 057 - PyInstaller spec
Commit 058 - Build script
Commit 059 - Version metadata
Commit 060 - App icon support
Commit 061 - Release README
Commit 062 - Final validation
Commit 063 - v0.1.0 release
```

---

## Git Rules

Use small commits.

Each commit must have a clear message in English.

Suggested format:

```text
Commit 002 - Application infrastructure
Commit 003 - Add project agent instructions
Commit 004 - Settings system
```

Before committing:

```powershell
python app.py
git status
git diff
```

After validating:

```powershell
git add .
git commit -m "Commit XXX - Short description"
git push
```

---

## Codex Workflow Rules

When asked to continue:

1. Read `AGENTS.md`.
2. Read `PROJECT_STATUS.md` and identify the requested current roadmap item.
3. Modify only files required for that item.
4. Keep the project runnable.
5. Validate imports.
6. Summarize:

   * roadmap version or requested scope
   * description
   * created files
   * modified files
   * validation result
7. Stop after completing the requested item unless explicitly asked to continue.

Do not continue into the next roadmap item without instruction.

---

## Validation Rules

At minimum, after implementation, verify:

```powershell
python app.py
```

If tests exist:

```powershell
python -m pytest
```

If formatting tools exist:

```powershell
python -m black .
python -m ruff check .
```

Do not add new formatting tools unless requested.

---

## Dependency Rules

Allowed runtime dependencies:

```text
PySide6
yt-dlp
```

Do not bundle `ffmpeg`.

Do not auto-install `yt-dlp`.

Do not auto-install `ffmpeg`.

The user installs them manually with:

```powershell
winget install yt-dlp
winget install ffmpeg
```

---

## Final Goal

The final application must be a Windows desktop executable created with PyInstaller.

The final product must feel like a polished desktop application, not a script.

The user must be able to:

1. Open the app.
2. Add video or playlist URLs.
3. Select videos.
4. Select MP4 or MP3.
5. Select quality.
6. Select output folder.
7. Start downloads.
8. Monitor progress.
9. Cancel downloads.
10. Preserve settings and queue between sessions.
