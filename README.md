# YouTube Downloader Pro

YouTube Downloader Pro is a Windows desktop frontend for `yt-dlp` and `ffmpeg`, built with Python 3.12 and PySide6.

The current version contains infrastructure, interface, metadata loading, playlist support, download execution, and Sprint 6 polish: queue persistence, settings resilience, clearer error messages, improved empty states, keyboard shortcuts, visual refinements, and log export.

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

Version `0.1.0` establishes the repository structure, application infrastructure, settings persistence, queue persistence, dependency verification, resource resolution, logging, theme management, polished UI foundation, playlist selection, and download execution flow.
