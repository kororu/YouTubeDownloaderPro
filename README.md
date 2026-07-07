# YouTube Downloader Pro

YouTube Downloader Pro is a Windows desktop frontend for `yt-dlp` and `ffmpeg`, built with Python 3.12 and PySide6.

The current version contains the Sprint 1 infrastructure, Sprint 2 interface foundation, Sprint 3 metadata engine foundation, Sprint 4 playlist support, and Sprint 5 download execution: application bootstrap, typed settings, safe paths, dependency checks, centralized theme loading, rotating logs, resource resolution, a professional main window shell, queue interactions, settings panel, status area, log panel, about dialog, yt-dlp command generation, subprocess execution, URL validation, asynchronous metadata loading, playlist analysis, playlist video selection, MP4 and MP3 downloads, progress parsing, output folder selection, cancellation, and up to three simultaneous downloads.

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

Version `0.1.0` establishes the repository structure, application infrastructure, settings persistence, dependency verification, resource resolution, logging, theme management, Sprint 2 UI foundation, Sprint 3 metadata foundation, Sprint 4 playlist selection flow, and Sprint 5 download execution flow.
