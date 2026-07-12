@echo off
setlocal EnableExtensions

set "APP_DIR=%~dp0YouTubeDownloaderPro"
set "APP_EXE=%APP_DIR%\YouTubeDownloaderPro.exe"

if not exist "%APP_EXE%" (
    echo ERROR: YouTubeDownloaderPro.exe was not found.
    echo Expected path:
    echo "%APP_EXE%"
    echo.
    echo Keep run_app.bat next to the YouTubeDownloaderPro folder.
    pause
    exit /b 1
)

start "" /D "%APP_DIR%" "%APP_EXE%"
if errorlevel 1 (
    echo ERROR: The application could not be started.
    echo Executable path:
    echo "%APP_EXE%"
    pause
    exit /b 1
)

exit /b 0
