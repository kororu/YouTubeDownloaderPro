# Estado del proyecto

## Resumen general

- Proyecto: YouTube Downloader Pro.
- Autor: Ariel Ponce.
- Versión visible actual: `v0.3.0`.
- Plataforma objetivo: Windows.
- Stack: Python 3.12+, PySide6, QThread, `subprocess`, `yt-dlp`, `ffmpeg`, JSON, QSS y PyInstaller.
- Distribución: ejecutable PyInstaller `onedir` y paquete portable.
- Estado Git: el working tree contiene cambios sin commit; esta documentación no los considera una release publicada.

## Implementado

- Aplicación Windows con `QMainWindow` y tema dark permanente.
- Imagen de fondo opcional con escalado tipo cover.
- Cola basada en `QScrollArea` y `QueueItemWidget`.
- `LogWidget` con exportación, `StatusWidget`, `SettingsWidget`, footer y `AboutDialog`.
- Formatos MP4 y MP3, selector de calidad y carpeta de salida.
- Persistencia JSON de ajustes y cola.
- Descargas mediante `yt-dlp` y uso de FFmpeg para conversión/procesamiento.
- Verificación de `yt-dlp` y `ffmpeg` en `PATH`.
- Ayudante manual `install_dependencies.bat`.
- Soporte de video individual, playlist y YouTube Mix.
- Carga incremental y límites configurables para playlists/Mix.
- PyInstaller configurado mediante `YouTubeDownloaderPro.spec`.
- Scripts `scripts\build_windows.ps1` y `scripts\package_portable.ps1`.
- Launcher `run_app.bat` y guía `README_INSTALL.txt` para el portable.

## En progreso en v0.3.0

Las siguientes mejoras están implementadas en el working tree, pero siguen pendientes de validación manual completa y de su proceso normal de commit/release:

- Ejecución silenciosa centralizada con `CREATE_NO_WINDOW` y `STARTUPINFO` en Windows.
- Carga de playlist/Mix por rangos de inicio y fin.
- Acción `Cargar siguientes` con historial por URL.
- Prevención de duplicados por `video_id` o URL.
- Mejoras de cancelación y logs del análisis de playlists.
- Preparación automatizada del paquete portable.

## Pendiente de verificación

- Ejecutar descargas MP4 y MP3 reales desde el `.exe` sin ventanas emergentes de `yt-dlp` o `ffmpeg`.
- Probar rangos `1-200`, `201-400` y `401-600` con playlists reales.
- Probar YouTube Mix de 400, 1000 o más entradas sin bloquear la interfaz.
- Confirmar `Cargar siguientes`, deduplicación y persistencia por URL entre sesiones.
- Confirmar cancelación durante el análisis y claridad de los logs de progreso.
- Revisar layout superior, separación de controles, textos cortados y desplegables.
- Validar tema dark, imagen de fondo, escalado y contraste en el `.exe`.
- Generar y probar el paquete portable en otro PC Windows sin VS Code.
- Mejorar, si las pruebas lo requieren, el contenido y robustez del empaquetado portable.

## Planificado

- `v0.4.0`: gestión avanzada de cola y playlists.
- `v0.5.0`: formatos de audio avanzados, incluido WAV, y opciones de metadata.
- `v0.6.0`: mejora visual y de experiencia de usuario.
- `v0.7.0`: historial completo y control de duplicados.
- `v0.8.0`: configuración avanzada y diagnóstico.
- `v0.9.0`: instalador/portable y release candidate.
- `v1.0.0`: release estable de Windows.

El detalle vinculante del roadmap se mantiene en `PROJECT.md` y las tareas en `TODO.md`.

## Sugerido para después de v1.0

- `v1.1`: evaluar múltiples fuentes compatibles con `yt-dlp`.
- `v1.2`: perfiles y ayuda específica por plataforma.
- `v1.3`: programación y automatización.
- `v1.4`: aplicación Android complementaria como control remoto.
- `v2.0`: evaluar una aplicación Android separada.

Estas ideas no están implementadas ni garantizan compatibilidad con sitios concretos.

## Decisiones técnicas vigentes

- No instalar automáticamente `yt-dlp` ni FFmpeg desde la aplicación.
- No incluir `yt-dlp` ni FFmpeg dentro del ejecutable.
- Usar `install_dependencies.bat` únicamente como ayuda manual.
- Mantener el tema dark como único tema.
- Mantener 200 videos como límite predeterminado de playlist/Mix.
- Preferir procesamiento incremental y carga por bloques/rangos.
- Mantener PyInstaller en modo `onedir` y un paquete portable externo.
- Preservar la separación entre UI, modelos, servicios, infraestructura y configuración.

## Empaquetado portable

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package_portable.ps1
```

Resultado esperado:

```text
release\YouTubeDownloaderPro_Portable\
```

Contenido esperado:

- `YouTubeDownloaderPro\YouTubeDownloaderPro.exe`.
- `install_dependencies.bat`.
- `run_app.bat`.
- `README_INSTALL.txt`.
- `VERSION.txt`.

## WAV y calidad de audio

WAV se planifica para `v0.5.0`. Es posible mediante `yt-dlp` y FFmpeg, pero genera archivos grandes y no recupera información perdida si la fuente ya está comprimida. Resulta útil para edición porque evita una segunda compresión. Para uso normal convienen MP3, M4A u OPUS; para máxima calidad práctica se debe evaluar `best audio`, FLAC o WAV según el flujo de trabajo.

## Uso responsable

El proyecto es un frontend para `yt-dlp` y `ffmpeg`. El usuario debe cumplir derechos de autor, términos de servicio y legislación aplicable, y priorizar contenido propio, libre, educativo o autorizado.

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

## Próximo paso recomendado

Completar la matriz de pruebas manuales de `v0.3.0` con videos, MP4, MP3, playlists grandes, YouTube Mix, rangos consecutivos y el paquete portable en otro PC. Corregir solo los defectos confirmados antes de etiquetar o publicar la versión.

## Reglas para futuras sesiones

- Leer `AGENTS.md` y este archivo antes de modificar el proyecto.
- No marcar una función como estable sin evidencia de prueba.
- No hacer commit automáticamente salvo pedido explícito.
- No instalar dependencias externas automáticamente.
- No modificar archivos ajenos al alcance solicitado.
