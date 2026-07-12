# Guía de release

## Estado de versión

- Producto: YouTube Downloader Pro.
- Versión visible actual: `0.3.0`.
- Plataforma: Windows.
- Formato: ejecutable PyInstaller `onedir` y paquete portable.
- Estado: mejoras de `v0.3.0` presentes en el working tree; release pendiente de validación manual completa.

Este documento no cambia el número de versión ni implica que `v0.3.0` esté publicada.

## Requisitos de build

- Python 3.12+.
- Dependencias de `requirements.txt`.
- PyInstaller en el entorno activo.
- `yt-dlp` y FFmpeg instalados por el usuario para probar descargas reales.

```powershell
winget install --id yt-dlp.yt-dlp --exact
winget install --id Gyan.FFmpeg --exact
```

## Build y portable

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\package_portable.ps1
```

Salidas esperadas:

```text
dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe
release\YouTubeDownloaderPro_Portable\
```

## Validación obligatoria para v0.3.0

```powershell
python app.py
python -m compileall .
.\dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe
git status
git diff --stat
```

Comprobar manualmente:

- Inicio, cierre, tema dark, ajustes y persistencia de cola.
- Fondo opcional, escalado, contraste y legibilidad.
- Descarga individual MP4 y MP3 sin consolas emergentes.
- Rangos de playlist `1-200`, `201-400` y `401-600`.
- `Cargar siguientes`, historial por URL y omisión de duplicados.
- Cancelación de un análisis activo y logs de progreso.
- YouTube Mix grande sin bloqueo de la interfaz.
- Paquete portable completo en otro PC Windows sin VS Code.
- Dependencias faltantes y ejecución de `install_dependencies.bat`.

## Criterios de publicación

- No publicar si una descarga abre consolas externas inesperadas.
- No publicar si un rango repite o pierde videos sin una explicación visible.
- No marcar el portable como validado hasta probarlo en otro equipo.
- Registrar defectos conocidos y cambios finales en `CHANGELOG.md`.
- Mantener `PROJECT_STATUS.md` alineado con los resultados reales.

## Alcance futuro

El roadmap hacia `v1.0.0` está en `PROJECT.md` y `TODO.md`. Formatos como WAV, historial completo, configuración avanzada y fuentes adicionales son planificados o sugeridos; no forman parte de la funcionalidad estable actual.

## Uso responsable

La distribución es un frontend para `yt-dlp` y `ffmpeg`. La publicación y el uso deben respetar licencias, derechos de autor, términos de servicio y legislación aplicable. No debe presentarse como una herramienta para descargar contenido protegido sin autorización.
