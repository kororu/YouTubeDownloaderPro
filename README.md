# YouTube Downloader Pro

YouTube Downloader Pro es una aplicación de escritorio para Windows creada con Python 3.12+, PySide6 y PyInstaller. Actúa como interfaz gráfica para `yt-dlp` y `ffmpeg`, con cola de descargas, ajustes persistentes, logs y soporte para videos, playlists y YouTube Mix.

Versión visible actual: `v0.3.0`.

## Estado actual

### Implementado

- Aplicación Windows con PySide6 y tema dark permanente.
- Empaquetado `onedir` con PyInstaller y preparación de paquete portable.
- Descargas mediante `yt-dlp` y procesamiento con `ffmpeg` cuando corresponde.
- Formatos MP4 y MP3, selector de calidad y carpeta de salida configurable.
- Cola de descargas basada en `QScrollArea` y widgets propios.
- Persistencia JSON de ajustes y cola.
- `LogWidget`, exportación de logs, estado, ajustes y diálogo Acerca de.
- Imagen de fondo opcional con escalado tipo cover.
- `install_dependencies.bat` para verificar e instalar manualmente `yt-dlp` y FFmpeg.
- Carga incremental de playlists y YouTube Mix.
- En el working tree de `v0.3.0`: ejecución silenciosa de procesos, rangos de playlist, `Cargar siguientes` y prevención de duplicados.

### En progreso y pendiente de validación

- Confirmar que `yt-dlp` y `ffmpeg` no abran ventanas emergentes desde el `.exe`.
- Probar rangos `1-200`, `201-400` y `401-600` con playlists y Mix reales grandes.
- Verificar cancelación del análisis, logs de progreso y continuidad de `Cargar siguientes`.
- Mejorar la distribución del layout superior y revisar textos o combos cortados.
- Validar tema, fondo y legibilidad en el ejecutable.
- Probar el paquete portable completo en otro PC Windows sin VS Code.

Lo anterior no se considera estable hasta completar las pruebas manuales indicadas en [PROJECT_STATUS.md](PROJECT_STATUS.md).

## Requisitos

- Windows.
- Python 3.12+ para desarrollo.
- PySide6.
- `yt-dlp` disponible en `PATH`.
- FFmpeg disponible en `PATH`.

Instalación manual de herramientas externas:

```powershell
winget install --id yt-dlp.yt-dlp --exact
winget install --id Gyan.FFmpeg --exact
```

También puede ejecutar:

```powershell
.\install_dependencies.bat
```

La aplicación no instala dependencias automáticamente ni incluye `yt-dlp` o FFmpeg en el ejecutable.

## Desarrollo y ejecución

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Playlists y YouTube Mix

El límite predeterminado es de 200 videos para proteger la capacidad de respuesta de la interfaz. La carga por rangos permite procesar bloques como `1-200`, `201-400` y `401-600`; `Cargar siguientes` continúa desde el último bloque registrado para la misma URL. Estas mejoras de `v0.3.0` están implementadas en el working tree y requieren validación manual con fuentes reales antes de considerarse estables.

## Empaquetado

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\package_portable.ps1
.\dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe
```

El paquete portable se prepara en `release\YouTubeDownloaderPro_Portable\`. Consulte [RELEASE.md](RELEASE.md) y `README_INSTALL.txt` antes de distribuirlo.

## Roadmap hacia v1.0.0

- `v0.3.0`: descargas silenciosas, rangos de playlist, `Cargar siguientes`, deduplicación y mejoras para YouTube Mix.
- `v0.4.0`: gestión avanzada de cola y playlists, pausa, reintentos, prioridades, historial básico e importación/exportación.
- `v0.5.0`: audio avanzado (MP3, M4A, OPUS, FLAC y WAV), best audio, metadata, miniaturas, subtítulos y plantillas de nombres.
- `v0.6.0`: rediseño visual, layout superior, miniaturas en cola, modo compacto, fondo configurable, tooltips y atajos.
- `v0.7.0`: historial completo y control de duplicados.
- `v0.8.0`: ajustes avanzados, cookies opcionales, proxy, diagnóstico y configuración importable/exportable.
- `v0.9.0`: release candidate, portable validado, posible instalador, documentación final y pruebas en otros equipos.
- `v1.0.0`: release estable para Windows, silenciosa, robusta, documentada y lista para compartir.

El alcance detallado está en [PROJECT.md](PROJECT.md) y [TODO.md](TODO.md).

## WAV y audio sin compresión

WAV es técnicamente posible mediante `yt-dlp` y FFmpeg y está planificado para `v0.5.0`. Produce archivos grandes y no recupera calidad perdida cuando la fuente original ya está comprimida. Su ventaja es evitar una segunda compresión cuando el archivo se usará para edición. Para uso cotidiano, MP3, M4A u OPUS suelen ofrecer una mejor relación entre calidad y tamaño; para máxima calidad práctica se recomienda conservar `best audio` o elegir FLAC/WAV según la necesidad.

## Futuras versiones después de v1.0

Se evaluará soporte para Facebook, X/Twitter, TikTok, Vimeo, Instagram, SoundCloud, clips/VOD de Twitch y otras fuentes compatibles con `yt-dlp`. El soporte dependerá de `yt-dlp`, de los cambios de cada sitio y, en algunos casos, de cookies o sesión; no se garantiza compatibilidad absoluta. También se estudiarán perfiles por plataforma, programación de descargas, control remoto desde Android y una posible aplicación Android separada.

## Uso responsable

Esta herramienta es un frontend para `yt-dlp` y `ffmpeg`. Cada usuario debe respetar los derechos de autor, los términos de servicio de las plataformas y la legislación aplicable. Utilícela prioritariamente con contenido propio, libre, educativo o para el cual tenga autorización; el proyecto no promueve la descarga no autorizada de contenido protegido.

## Comandos útiles

```powershell
python app.py
python -m compileall .
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\package_portable.ps1
.\dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe
git status
git diff --stat
```
