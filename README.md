# YouTube Downloader Pro

YouTube Downloader Pro is a desktop application foundation for a professional video download manager built with Python 3.12 and PySide6.

This repository currently contains the application infrastructure, clean architecture modules, Qt application lifecycle, main window shell, and dark theme loading. Download functionality is not implemented yet.

## Requirements

- Python 3.12
- PySide6
- yt-dlp
- FFmpeg

## Setup

Install external tools on Windows:

```powershell
winget install --id yt-dlp.yt-dlp --exact
winget install --id Gyan.FFmpeg --exact
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the application entry point:

```powershell
python app.py
```

## Project Status

Version `0.1.0` establishes the repository structure, dependency baseline, application container, main window infrastructure, and bundled dark theme. Download workflows and feature widgets will be added in later milestones.
