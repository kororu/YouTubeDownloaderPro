# TODO y roadmap oficial

Convenciones:

- `[x]` implementado.
- `[~]` implementado o en progreso, pendiente de validación.
- `[ ]` planificado; todavía no implementado.
- `[?]` sugerencia futura sujeta a evaluación.

## v0.3.0 - Silent downloads and playlist ranges

- `[~]` Ocultar ventanas emergentes de `yt-dlp` y `ffmpeg`.
- `[~]` Centralizar `subprocess` con `CREATE_NO_WINDOW` en Windows.
- `[~]` Cargar playlists por rango.
- `[~]` Validar rangos `1-200`, `201-400` y `401-600`.
- `[~]` Añadir `Cargar siguientes`.
- `[~]` Evitar duplicados en cola.
- `[~]` Mejorar cancelación del análisis de playlist.
- `[~]` Mejorar logs de progreso.
- `[~]` Mejorar soporte para YouTube Mix grandes.
- `[ ]` Validar MP4 y MP3 reales desde el `.exe`.
- `[ ]` Validar el portable en otro PC Windows.

## v0.4.0 - Queue and playlist advanced management

- `[ ]` Reordenar videos y asignar prioridad.
- `[ ]` Pausar y reanudar la cola.
- `[ ]` Reintentar elementos fallidos.
- `[ ]` Limpiar completados y errores.
- `[ ]` Guardar progreso por playlist.
- `[ ]` Detectar videos ya descargados.
- `[ ]` Exportar e importar la cola.
- `[ ]` Añadir historial básico de descargas.

## v0.5.0 - Audio and format improvements

- `[ ]` Añadir MP3, M4A, OPUS, FLAC y WAV.
- `[ ]` Añadir `Audio original / best audio` cuando sea posible.
- `[ ]` Añadir calidades original/best, 128, 192, 256 y 320 kbps.
- `[ ]` Extraer miniatura y metadata.
- `[ ]` Descargar subtítulos disponibles.
- `[ ]` Añadir plantillas de nombre de archivo.
- `[ ]` Crear carpetas opcionales por canal y playlist.
- `[ ]` Explicar en la UI/documentación que WAV no recupera calidad perdida y ocupa más espacio.

## v0.6.0 - Visual polish and UX

- `[ ]` Rediseñar la barra superior en dos filas o grupos.
- `[ ]` Mejorar separación de botones y corregir textos cortados.
- `[ ]` Mejorar combos y desplegables.
- `[ ]` Mejorar escalado del fondo y añadir opacidad configurable.
- `[ ]` Añadir modo compacto.
- `[ ]` Mejorar la vista de cola.
- `[ ]` Añadir miniaturas a `QueueItemWidget` e iconos por estado.
- `[ ]` Mejorar pantalla vacía, tooltips y atajos de teclado.

## v0.7.0 - Download history and duplicate control

- `[ ]` Crear historial completo y buscable.
- `[ ]` Evitar descargas duplicadas mediante historial.
- `[ ]` Abrir carpeta y copiar ruta del archivo.
- `[ ]` Reintentar desde historial.
- `[ ]` Marcar favoritos.
- `[ ]` Exportar e importar historial.

## v0.8.0 - Advanced settings and diagnostics

- `[ ]` Añadir configuración avanzada.
- `[ ]` Evaluar límite de ancho de banda admitido por `yt-dlp`.
- `[ ]` Configurar descargas simultáneas.
- `[ ]` Añadir cookies opcionales del navegador con advertencias.
- `[ ]` Añadir proxy personalizado.
- `[ ]` Exportar logs y añadir modo diagnóstico.
- `[ ]` Mejorar verificación de dependencias.
- `[ ]` Restablecer, exportar e importar configuración.

## v0.9.0 - Installer and release candidate

- `[ ]` Decidir si se publicará un instalador real para Windows.
- `[ ]` Preparar ZIP portable final, accesos directos e icono definitivo.
- `[ ]` Verificar metadata de versión.
- `[ ]` Completar documentación de usuario final.
- `[ ]` Probar en otro PC y sin VS Code.
- `[ ]` Validar el `.exe` y corregir errores finales.

## v1.0.0 - Stable Windows release

- `[ ]` Publicar ejecutable y portable estables.
- `[ ]` Completar documentación y changelog.
- `[ ]` Confirmar manejo robusto de errores y descargas silenciosas.
- `[ ]` Confirmar playlists por rango y YouTube Mix estable.
- `[ ]` Incluir audio avanzado, incluido WAV.
- `[ ]` Incluir historial y control de duplicados.
- `[ ]` Confirmar interfaz ordenada, legible y lista para compartir.

## Futuras versiones después de v1.0

### v1.1 - Multi-source downloads

- `[?]` Evaluar Facebook, X/Twitter, TikTok, Vimeo, Instagram, SoundCloud, clips/VOD de Twitch y otras fuentes compatibles con `yt-dlp`.
- `[?]` Detectar el origen de la URL.
- `[?]` Advertir cuando un sitio requiera cookies o sesión.
- `[?]` Documentar que el soporte depende de `yt-dlp` y puede cambiar.

### v1.2 - Site profiles

- `[?]` Crear perfiles y opciones por plataforma.
- `[?]` Añadir cookies opcionales, errores específicos y ayuda por fuente.

### v1.3 - Scheduler and automation

- `[?]` Programar horarios de descarga.
- `[?]` Apagar el PC al finalizar.
- `[?]` Ejecutar la cola al iniciar Windows de forma opcional.
- `[?]` Añadir modo de bajo consumo.

### v1.4 - Remote companion

- `[?]` Evaluar una app Android para controlar por WiFi/5G la cola ejecutada en el PC.
- `[?]` Mantener inicialmente `yt-dlp` y FFmpeg en Windows, no dentro del teléfono.

### v2.0 - Android evaluation

- `[?]` Evaluar una aplicación Android separada con Kotlin, Java o Flutter.
- `[?]` No reutilizar PySide6/PyInstaller para Android.
- `[?]` Considerar WiFi/5G, avisos de datos móviles, modo solo WiFi, pausa al cambiar de red, almacenamiento y ejecución en segundo plano permitida por Android.
