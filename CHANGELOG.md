# Changelog

Todos los cambios relevantes del proyecto se documentan en este archivo.

## Upcoming

### Documentación

- Documentado el estado real de `v0.3.0`, incluidas las mejoras presentes en el working tree y sus validaciones pendientes.
- Incorporado el roadmap oficial desde `v0.3.0` hasta la versión estable `v1.0.0`.
- Añadidas propuestas post-`v1.0` para fuentes adicionales compatibles con `yt-dlp`, perfiles por sitio, automatización, control remoto y evaluación de Android.
- Añadida una explicación sobre WAV, audio sin compresión y sus limitaciones de calidad y tamaño.
- Añadida una nota de uso responsable y cumplimiento de derechos de autor, términos de servicio y legislación aplicable.

Esta sección no cambia la versión visible ni representa nuevas funcionalidades implementadas.

## v0.3.0 - 2026-07-07

- Actualizada la versión visible y la metadata de release a v0.3.0.
- Añadida configuración oculta de procesos de Windows para flujos de `yt-dlp` y `ffmpeg`.
- Centralizado el inicio de procesos externos en `core/process.py`.
- Añadida carga por rangos de playlists y YouTube Mix mediante `--playlist-start` y `--playlist-end`.
- Añadidos controles de inicio, fin y `Cargar siguientes`.
- Añadido historial persistente de rangos por URL.
- Añadida detección de duplicados por identificador de video o URL.
- Normalizada la URL de respaldo para comparar duplicados sin depender de mayúsculas, fragmentos ni orden de query parameters.
- Persistidos índice, URL de origen, título de playlist, indicador de Mix e identificador del video.
- Mejorados los logs de cancelación del análisis de playlists.
- `Cancelar actual` detiene primero un análisis de playlist activo.
- Añadido fallback incremental con aviso visible cuando un Mix no respeta el rango solicitado.
- Rechazados rangos vacíos y bloques manuales superiores a 500 videos.
- Mejorado el avance de `Cargar siguientes` usando el último índice real procesado.
- Añadidas pruebas de rangos y claves de duplicados.
- Añadida automatización del paquete portable y guía de instalación.
- Mejorado `install_dependencies.bat` para comprobar `winget` e instalar solo dependencias faltantes con confirmación.
- Verificados tests, compilación, arranque de la aplicación, build PyInstaller, arranque del `.exe` y generación portable.

> Estado: implementado en el working tree; pendiente de validación manual completa y commit/release.

## v0.2.0 - 2026-07-07

- Establecido el tema dark permanente y retirada la selección de tema light.
- Corregida la resolución de estilos y recursos en PyInstaller.
- Añadido fondo opcional persistente con capa de legibilidad.
- Añadida carga incremental de playlists y YouTube Mix.
- Añadidos progreso, inserción por lotes, cancelación segura y límites configurables.
- Acotado el log visible y reforzado el streaming para listas grandes.
- Retirado el panel permanente de dependencias de la barra lateral.
- Añadidas pruebas unitarias para ajustes, URLs, comandos y progreso.

## v0.1.0 - 2026-07-07

- Creada la base del proyecto, arquitectura modular y aplicación PySide6.
- Añadidos ajustes y cola persistentes, infraestructura, tema, logging y recursos.
- Añadidos toolbar, cola personalizada, logs, estado, ajustes y diálogos.
- Añadidos modelos, extracción de metadata, playlists y workers con QThread.
- Añadida ejecución de descargas MP4/MP3, progreso y cancelación.
- Añadidos controles de cola, mensajes de error, atajos y exportación de logs.
- Añadidos especificación PyInstaller, script de build, metadata e icono.
