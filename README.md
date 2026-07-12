# YouTube Downloader Pro

YouTube Downloader Pro es una aplicación de escritorio para Windows creada con Python 3.12+, PySide6 y PyInstaller. Actúa como interfaz gráfica para `yt-dlp` y `ffmpeg`, con cola de descargas, ajustes persistentes, logs y soporte para videos, playlists y YouTube Mix.

Versión visible actual: `v0.5.0`.

## Estado actual

### Implementado

- Aplicación Windows con PySide6 y tema dark permanente.
- Empaquetado `onedir` con PyInstaller y preparación de paquete portable.
- Descargas mediante `yt-dlp` y procesamiento con `ffmpeg` cuando corresponde.
- Video MP4 y audio MP3, M4A, OPUS, FLAC, WAV y audio original/best audio.
- Bitrates MP3 de 128, 192, 256 y 320 kbps, además de best/original.
- Opciones para miniatura, metadata JSON, subtítulos normales y automáticos.
- Plantillas de nombre y carpetas opcionales por canal o playlist.
- Cola de descargas basada en `QScrollArea` y widgets propios.
- Persistencia JSON de ajustes y cola.
- `LogWidget`, exportación de logs, estado, ajustes y diálogo Acerca de.
- Imagen de fondo opcional con escalado tipo cover.
- `install_dependencies.bat` para verificar e instalar manualmente `yt-dlp` y FFmpeg.
- Carga incremental de playlists y YouTube Mix.
- Ejecución silenciosa de procesos, rangos de playlist, `Cargar siguientes` y prevención de duplicados desde `v0.3.0`.
- Fallback incremental seguro para Mixes que no respeten las opciones de rango de `yt-dlp`.
- Cancelación del análisis de playlist desde `Cancelar actual` y `Cancelar todo`.

### En progreso y pendiente de validación

- Probar con medios reales MP3 en 192/320 kbps, M4A, OPUS, FLAC, WAV y audio original.
- Confirmar miniaturas, metadata, subtítulos, plantillas y carpetas organizadas con distintas fuentes.
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

Los rangos manuales no pueden estar vacíos ni superar 500 videos. Si un YouTube Mix no respeta `--playlist-start` y `--playlist-end`, la aplicación informa el problema y usa un recorrido incremental acotado como fallback. Las preferencias de audio, archivos auxiliares y organización se guardan en cada elemento agregado a la cola.

## Audio avanzado y archivos auxiliares

- `MP3`: convierte mediante FFmpeg y permite best/original, 128, 192, 256 o 320 kbps.
- `M4A` y `OPUS`: prefieren una fuente del mismo tipo cuando está disponible y convierten mediante FFmpeg cuando es necesario.
- `FLAC` y `WAV`: conversión sin pérdida adicional mediante FFmpeg; requieren más espacio.
- `Audio original / best audio`: descarga el mejor audio disponible sin conversión innecesaria y puede conservar una extensión variable.
- `Descargar miniatura`: añade `--write-thumbnail`.
- `Guardar metadata`: añade `--write-info-json` y genera un archivo adicional.
- Subtítulos: admite subtítulos publicados, automáticos e idiomas como `es,en`; su disponibilidad depende del video.
- Nombres: título, canal-título, índice de playlist-título, fecha-título o plantilla personalizada segura.
- Organización: carpetas opcionales por canal y por playlist.

MP3, M4A, OPUS, FLAC y WAV requieren FFmpeg. La aplicación muestra un error útil si falta; no instala ni empaqueta la dependencia.

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
- `v0.5.0` (actual): audio avanzado, best audio, metadata, miniaturas, subtítulos, plantillas y carpetas organizadas.
- `v0.6.0`: rediseño visual, layout superior, miniaturas en cola, modo compacto, fondo configurable, tooltips y atajos.
- `v0.7.0`: historial completo y control de duplicados.
- `v0.8.0`: ajustes avanzados, cookies opcionales, proxy, diagnóstico y configuración importable/exportable.
- `v0.9.0`: release candidate, portable validado, posible instalador, documentación final y pruebas en otros equipos.
- `v1.0.0`: release estable para Windows, silenciosa, robusta, documentada y lista para compartir.

El alcance detallado está en [PROJECT.md](PROJECT.md) y [TODO.md](TODO.md).

## WAV y audio sin compresión

WAV está disponible mediante `yt-dlp` y FFmpeg desde `v0.5.0`. Produce archivos grandes y no recupera calidad perdida cuando la fuente original ya está comprimida. Solo evita una compresión adicional y resulta útil para edición. Para uso cotidiano, MP3, M4A u OPUS suelen ofrecer una mejor relación entre calidad y tamaño; para máxima calidad práctica se recomienda conservar `best audio` o elegir FLAC/WAV según la necesidad.

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
