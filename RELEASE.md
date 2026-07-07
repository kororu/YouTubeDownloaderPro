# Release Guide

## Version

- Product: YouTube Downloader Pro
- Version: 0.1.0
- Platform: Windows
- Package target: PyInstaller executable

## Build Requirements

- Python 3.12
- Project runtime dependencies from `requirements.txt`
- PyInstaller available in the active environment
- yt-dlp and FFmpeg installed by the user when running downloads

## External Tools

```powershell
winget install --id yt-dlp.yt-dlp --exact
winget install --id Gyan.FFmpeg --exact
```

## Build

```powershell
.\scripts\build_windows.ps1 -Clean
```

The executable is produced at:

```text
dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe
```

## Validation

Before publishing a build, run:

```powershell
python app.py
python -m compileall app.py config core models services resources ui widgets dialogs styles tests
git status --short
```

Confirm that the application starts, dependency warnings are visible when tools are missing, settings persist, queue persistence works, and downloads use user-installed `yt-dlp` and `ffmpeg`.
