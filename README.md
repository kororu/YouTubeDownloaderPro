# YouTube Downloader Pro

YouTube Downloader Pro is a Windows desktop frontend for `yt-dlp` and `ffmpeg`, built with Python 3.12 and PySide6.

Version `0.1.0` contains infrastructure, interface, metadata loading, playlist support, download execution, queue persistence, polish improvements, and Windows release packaging with PyInstaller.

## Requirements

- Python 3.12
- PySide6
- yt-dlp
- FFmpeg

## External Tools

Install external tools on Windows:

```powershell
winget install --id yt-dlp.yt-dlp --exact
winget install --id Gyan.FFmpeg --exact
```

## Development Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Install PyInstaller in the active environment when building the Windows executable:

```powershell
pip install pyinstaller
```

## Run

Start the application:

```powershell
python app.py
```

## Build

Create the Windows release build:

```powershell
.\scripts\build_windows.ps1 -Clean
```

Release build details are documented in `RELEASE.md`.

## Project Status

Version `0.1.0` establishes the complete first release: repository structure, application infrastructure, settings persistence, queue persistence, dependency verification, resource resolution, logging, theme management, polished UI foundation, playlist selection, download execution flow, and Windows packaging assets.
