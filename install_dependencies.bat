@echo off
setlocal EnableExtensions

title YouTube Downloader Pro Dependencies

echo YouTube Downloader Pro dependency installer
echo.
echo This script checks and installs external tools required by the application:
echo - yt-dlp
echo - FFmpeg
echo.
echo The application does not bundle these tools and never installs them automatically.
echo.

where winget >nul 2>nul
if errorlevel 1 (
    echo ERROR: winget is not available on this system.
    echo Install App Installer from Microsoft Store and run this script again.
    echo.
    pause
    exit /b 1
)

set "NEEDS_YTDLP=0"
set "NEEDS_FFMPEG=0"

where yt-dlp >nul 2>nul
if errorlevel 1 (
    set "NEEDS_YTDLP=1"
    echo yt-dlp: missing
) else (
    echo yt-dlp: detected
    yt-dlp --version
)

where ffmpeg >nul 2>nul
if errorlevel 1 (
    set "NEEDS_FFMPEG=1"
    echo FFmpeg: missing
) else (
    echo FFmpeg: detected
    ffmpeg -version 2^>nul | findstr /B /C:"ffmpeg version"
)

if "%NEEDS_YTDLP%"=="0" if "%NEEDS_FFMPEG%"=="0" (
    echo.
    echo All external dependencies are already available.
    echo.
    pause
    exit /b 0
)

echo.
choice /C YN /M "Install missing dependencies with winget now"
if errorlevel 2 (
    echo.
    echo Installation cancelled by user.
    pause
    exit /b 1
)

if "%NEEDS_YTDLP%"=="1" (
    echo.
    echo Installing yt-dlp...
    winget install --id yt-dlp.yt-dlp --exact --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo ERROR: Failed to install yt-dlp.
        pause
        exit /b 1
    )
)

if "%NEEDS_FFMPEG%"=="1" (
    echo.
    echo Installing FFmpeg...
    winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo ERROR: Failed to install FFmpeg.
        pause
        exit /b 1
    )
)

echo.
echo Final verification:

where yt-dlp >nul 2>nul
if errorlevel 1 (
    echo yt-dlp: not detected after installation.
    set "VERIFY_FAILED=1"
) else (
    echo yt-dlp: detected
)

where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo FFmpeg: not detected after installation.
    set "VERIFY_FAILED=1"
) else (
    echo FFmpeg: detected
)

echo.
if defined VERIFY_FAILED (
    echo If a tool was just installed but is still not detected, close this window,
    echo open a new terminal, and run this script again so PATH can refresh.
    pause
    exit /b 1
)

echo Dependencies are ready. Restart YouTube Downloader Pro before downloading.
echo If a new terminal was required, open YouTube Downloader Pro after PATH refreshes.
pause
exit /b 0
