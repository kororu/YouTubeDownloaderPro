# YouTube Downloader Pro

YouTube Downloader Pro is a Windows desktop frontend for `yt-dlp` and `ffmpeg`, built with Python 3.12 and PySide6.

Version `0.2.0` contains infrastructure, interface, metadata loading, progressive playlist and YouTube Mix loading, download execution, queue persistence, permanent dark mode, optional background image support, polish improvements, and Windows release packaging with PyInstaller.

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

If available in your checkout, run the helper script:

```powershell
.\install_dependencies.bat
```

The application verifies dependencies internally and reports missing tools in the log/status area without showing a permanent dependency panel.

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

## Playlist and YouTube Mix Loading

Use the playlist action with a standard playlist URL or a YouTube Mix URL, including URLs with `list=RD` or `start_radio=1`. Videos are added to the queue progressively while progress is shown in the log.

The default playlist and YouTube Mix limit is `200` videos to keep the interface responsive with large lists. Change `Límite playlist` in Settings to `50`, `100`, `200`, `500`, or `Sin límite`. Avoid `Sin límite` for very large mixes unless you explicitly accept the performance risk.

## Appearance

The application always runs in dark mode. A custom background image can be selected from settings using `png`, `jpg`, `jpeg`, or `webp`; only the selected path is saved. Main panels use subtle transparency when a background image is active while controls remain readable.

## Build

Create the Windows release build:

```powershell
.\scripts\build_windows.ps1 -Clean
```

Release build details are documented in `RELEASE.md`.

## Project Status

Version `0.2.0` improves the first release with permanent dark mode, PyInstaller-safe style/resource loading, optional background images, and incremental playlist and YouTube Mix loading for large lists.
