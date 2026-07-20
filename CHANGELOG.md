# Changelog

## v1.1.0 - Simple mode and compact queue

- Añadido selector persistente de Modo Simple y Modo Avanzado; el modo inicial es Simple.
- Añadido flujo simple con URL, MP4/MP3, mejor calidad automática, destino visible y acciones esenciales de cola.
- Reutilizada la misma cola y servicios de descarga para que cambiar de modo no reinicie elementos ni descargas activas.

## v1.0.4 - Dual queue view

- Añadida una vista de lista compacta para seleccionar y gestionar playlists o colas grandes.
- Mantenida la vista detallada de tarjetas y sincronizada la selección, el estado y el progreso entre ambas vistas.
- Persistida la preferencia `Tarjetas` o `Lista` entre sesiones.

## v1.0.3 - Download history validation before metadata loading

- La cola consulta el historial local por ID de YouTube y URL antes de iniciar `yt-dlp`.
- Los archivos existentes se muestran como `Ya descargado` sin cargar metadata ni mostrar un bot-check.
- Las rutas ausentes o incompletas permiten redescarga y las descargas nuevas guardan la ruta final reportada por `yt-dlp`.

## v1.0.2 - History file validation and YouTube bot-check fixes

- La prevención de redescargas ahora exige que el archivo registrado aún exista.
- Mejorado el mensaje para el desafío anti-bot de YouTube y protegidas rutas de cookies locales.

## v1.0.1 - Progress bar and YouTube cookie handling

- Añadida barra de progreso visual por elemento y mensaje amigable ante el control anti-bot de YouTube.

## v1.0.0 - Stable Windows release

- Finalizado el ciclo de estabilización, build PyInstaller onedir y paquete portable para Windows.
- Consolidada la documentación de instalación, dependencias, diagnóstico y pruebas de release.

## v0.9.0 - 2026-07-20

- Preparado build onedir, portable limpio, documentación de usuario y checklist de release candidate.

## v0.7.0 - 2026-07-20

- Añadido historial JSON local de descargas completadas y fallidas, con búsqueda, copiado, apertura de carpeta y reintento.
- Añadidos ajustes persistentes para duplicados en cola, avisos de descargados y redescarga.

## v0.6.0 - 2026-07-20

- Reorganizada la toolbar en grupos visuales y reforzada la legibilidad de controles y desplegables dark.
- Añadidos fondo adaptable con opacidad persistente, paneles semitransparentes y modo compacto.
- Mejoradas cola, estados vacíos, tooltips, contadores de estado y acciones para copiar o limpiar el registro.
- Añadidos atajos: Ctrl+L, Ctrl+D, Ctrl+Shift+C, Ctrl+O, Ctrl+,, F1, Ctrl+A y Delete según el contexto.

Todos los cambios relevantes del proyecto se documentan en este archivo.

## Upcoming

### Documentación

- Implementado `v1.1.0 - Simple mode and compact queue` en el working tree; requiere las pruebas manuales normales antes de una release.
- Reordenado el roadmap posterior a `v1.0.x`: modo simple primero, luego cola avanzada de playlists, flujo de playlists, perfiles, fuentes múltiples y automatización.

- Documentado el estado real de `v0.3.0`, incluidas las mejoras presentes en el working tree y sus validaciones pendientes.
- Incorporado el roadmap oficial desde `v0.3.0` hasta la versión estable `v1.0.0`.
- Añadidas propuestas post-`v1.0` para fuentes adicionales compatibles con `yt-dlp`, perfiles por sitio, automatización, control remoto y evaluación de Android.
- Añadida una explicación sobre WAV, audio sin compresión y sus limitaciones de calidad y tamaño.
- Añadida una nota de uso responsable y cumplimiento de derechos de autor, términos de servicio y legislación aplicable.

Esta sección no cambia la versión visible ni representa nuevas funcionalidades implementadas.

## v0.5.0 - 2026-07-12

- Actualizada la versión visible y metadata de Windows a `v0.5.0`.
- Añadidos M4A, OPUS, FLAC, WAV y audio original/best audio sin romper MP4/MP3.
- Añadidos bitrates MP3 best/original, 128, 192, 256 y 320 kbps.
- Añadidas opciones de miniatura, metadata JSON, subtítulos publicados y automáticos e idiomas configurables.
- Añadidas plantillas de nombre predefinidas y personalizadas con validación segura.
- Añadidas carpetas opcionales por canal y playlist.
- Extendida la persistencia de settings y cola con defaults compatibles con JSON antiguo.
- Mejorados los errores de FFmpeg y los logs de opciones activas y subtítulos no disponibles.
- Mantenida la ejecución silenciosa de procesos externos en Windows.
- Añadidas pruebas para formatos, comandos, persistencia y plantillas de salida.
- Verificados 35 tests, compilación, arranque, build PyInstaller, ejecutable y portable `v0.5.0`.

> Estado: implementado en el working tree; pendiente de pruebas manuales con descargas reales y validación final del portable.

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
