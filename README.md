# YouTube Downloader Pro

YouTube Downloader Pro is a Windows desktop frontend for `yt-dlp` and `ffmpeg`, built with Python 3.12 and PySide6.

The current version contains the Sprint 1 infrastructure: application bootstrap, typed settings, safe paths, dependency checks, centralized theme loading, rotating logs, resource resolution, and the base main window shell. Download functionality is not implemented yet.

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

## Run

Start the application:

```powershell
python app.py
```

## Project Status

Version `0.1.0` establishes the repository structure, application infrastructure, settings persistence, dependency verification, resource resolution, logging, theme management, and a base UI shell. Download workflows will be added in later milestones.
