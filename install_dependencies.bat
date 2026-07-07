@echo off
setlocal

echo YouTube Downloader Pro dependency installer
echo.
echo This script installs external tools using winget:
echo - yt-dlp
echo - FFmpeg
echo.
echo The application does not bundle these tools. They remain system dependencies.
echo.

where winget >nul 2>nul
if errorlevel 1 (
    echo winget is not available on this system.
    echo Install App Installer from Microsoft Store and run this script again.
    exit /b 1
)

winget install --id yt-dlp.yt-dlp --exact
if errorlevel 1 (
    echo Failed to install yt-dlp.
    exit /b 1
)

winget install --id Gyan.FFmpeg --exact
if errorlevel 1 (
    echo Failed to install FFmpeg.
    exit /b 1
)

echo.
echo Dependencies installed. Restart YouTube Downloader Pro before downloading.
exit /b 0
