# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

PROJECT_ROOT = Path(SPECPATH)
APP_NAME = "YouTubeDownloaderPro"
EXCLUDED_DATA_PARTS = {"__pycache__"}
EXCLUDED_DATA_SUFFIXES = {".log", ".py", ".pyc", ".pyo", ".tmp"}


def collect_data_files(source_directory: Path, target_directory: str) -> list[tuple[str, str]]:
    """Collect distributable data files for PyInstaller."""
    collected_files: list[tuple[str, str]] = []
    for file_path in source_directory.rglob("*"):
        if not file_path.is_file():
            continue
        if any(part in EXCLUDED_DATA_PARTS for part in file_path.parts):
            continue
        if file_path.suffix.lower() in EXCLUDED_DATA_SUFFIXES:
            continue

        relative_parent = file_path.parent.relative_to(source_directory)
        collected_files.append((str(file_path), str(Path(target_directory) / relative_parent)))
    return collected_files


datas = collect_data_files(PROJECT_ROOT / "resources", "resources")
datas += collect_data_files(PROJECT_ROOT / "styles", "styles")

analysis = Analysis(
    ["app.py"],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "PySide6.QtSvg",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(analysis.pure)

exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=str(PROJECT_ROOT / "resources" / "version_info.txt"),
)

coll = COLLECT(
    exe,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
