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
- `[x]` Validar tests, compilación, arranque, build PyInstaller y generación portable.
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

- `[x]` Añadir MP3, M4A, OPUS, FLAC y WAV.
- `[x]` Añadir `Audio original / best audio` sin conversión innecesaria.
- `[x]` Añadir calidades original/best, 128, 192, 256 y 320 kbps para MP3.
- `[x]` Añadir opciones de miniatura y metadata.
- `[x]` Añadir subtítulos publicados, automáticos e idiomas configurables.
- `[x]` Añadir plantillas de nombre predefinidas y personalizadas seguras.
- `[x]` Crear carpetas opcionales por canal y playlist.
- `[x]` Mantener compatibilidad con settings y cola JSON antiguos.
- `[x]` Explicar que WAV no recupera calidad perdida y ocupa más espacio.
- `[x]` Validar tests, compilación, arranque, build PyInstaller y portable `v0.5.0`.
- `[ ]` Validar todos los formatos y opciones con descargas reales.

## v0.6.0 - Visual polish and UX

- `[x]` Rediseñar la barra superior en grupos y mejorar separación de botones.
- `[x]` Mejorar combos y desplegables dark.
- `[x]` Mejorar escalado del fondo y añadir opacidad configurable.
- `[x]` Añadir modo compacto persistente.
- `[x]` Mejorar la vista de cola, progreso, origen y estado descargado.
- `[x]` Mejorar estados vacíos, tooltips y atajos de teclado.
- `[ ]` Validar visualmente todas las resoluciones de pantalla y el `.exe` en Windows.

## v0.7.0 - Download history and duplicate control

- `[x]` Historial JSON persistente, búsqueda, acciones y reintento desde historial.
- `[x]` Aviso de videos ya descargados y ajustes de duplicados/redescarga.

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

- `[x]` Preparar build onedir, portable limpio y documentación de instalación.
- `[x]` Añadir checklist de validación para release candidate.

- `[ ]` Decidir si se publicará un instalador real para Windows.
- `[ ]` Preparar ZIP portable final, accesos directos e icono definitivo.
- `[ ]` Verificar metadata de versión.
- `[ ]` Completar documentación de usuario final.
- `[ ]` Probar en otro PC y sin VS Code.
- `[ ]` Validar el `.exe` y corregir errores finales.

## v1.0.0 - Stable Windows release

- `[x]` Preparar ejecutable onedir y paquete portable para Windows.
- `[x]` Consolidar documentación y checklist de release estable.
- `[ ]` Ejecutar matriz manual de descargas reales y PC limpio antes de distribución pública.

- `[ ]` Publicar ejecutable y portable estables.
- `[ ]` Completar documentación y changelog.
- `[ ]` Confirmar manejo robusto de errores y descargas silenciosas.
- `[ ]` Confirmar playlists por rango y YouTube Mix estable.
- `[ ]` Incluir audio avanzado, incluido WAV.
- `[ ]` Incluir historial y control de duplicados.
- `[ ]` Confirmar interfaz ordenada, legible y lista para compartir.

## Backlog aprobado después de v1.0

### v1.0.x - Stability and bugfixes

- `[~]` Consolidar historial, redescarga, archivo movido/no encontrado, progreso, cookies, portable y defectos visuales menores.
- `[ ]` Completar pruebas manuales de `v1.1.0` antes de su release.

### v1.1.0 - Simple mode and compact queue

- `[x]` Crear Modo Simple y conservar Modo Avanzado.
- `[x]` Mostrar URL, MP4/MP3, mejor calidad automática, carpeta destino y acciones principales de cola.
- `[x]` Ocultar calidad manual, rangos, opciones técnicas, cookies avanzadas, diagnóstico, log grande y archivos auxiliares.
- `[x]` Implementar cola minimalista: selección, nombre, formato, estado, porcentaje, barra compacta y quitar.
- `[x]` Mantener la vista avanzada para control por rango, historial, diagnósticos, formatos adicionales y configuraciones especiales.
- `[ ]` Ejecutar pruebas manuales de cambio de modo durante descargas y playlist.

### v1.2.0 - Advanced playlist queue view

- `[ ]` Extender tarjetas/lista, filtros por estado, orden por progreso/estado/nombre y selección masiva para playlists grandes.

### v1.3.0 - Playlist workflow improvements

- `[ ]` Mejorar bloques, reanudación, cola persistente, rangos automáticos y recuperación de descargas interrumpidas.

### v1.4.0 - Download profiles

- `[ ]` Añadir perfiles Música MP3, Video MP4, Playlist, Máxima calidad, Liviano y personalizados.

### v1.5.0 - Multi-source downloads

- `[?]` Evaluar fuentes externas compatibles con `yt-dlp`, detección de plataforma y mensajes de cookies o incompatibilidad.

### v1.6.0 - Automation and scheduler

- `[?]` Evaluar programación, inicio diferido, apagado al finalizar, cola persistente y tareas automáticas.

## Ideas posteriores a v1.6.0

### Multi-source research

- `[?]` Evaluar Facebook, X/Twitter, TikTok, Vimeo, Instagram, SoundCloud, clips/VOD de Twitch y otras fuentes compatibles con `yt-dlp`.
- `[?]` Detectar el origen de la URL.
- `[?]` Advertir cuando un sitio requiera cookies o sesión.
- `[?]` Documentar que el soporte depende de `yt-dlp` y puede cambiar.

### Site-profile research

- `[?]` Crear perfiles y opciones por plataforma.
- `[?]` Añadir cookies opcionales, errores específicos y ayuda por fuente.

### Remote and Android research

- `[?]` Programar horarios de descarga.
- `[?]` Apagar el PC al finalizar.
- `[?]` Ejecutar la cola al iniciar Windows de forma opcional.
- `[?]` Añadir modo de bajo consumo.

### Remote companion research

- `[?]` Evaluar una app Android para controlar por WiFi/5G la cola ejecutada en el PC.
- `[?]` Mantener inicialmente `yt-dlp` y FFmpeg en Windows, no dentro del teléfono.

### v2.0 - Android evaluation

- `[?]` Evaluar una aplicación Android separada con Kotlin, Java o Flutter.
- `[?]` No reutilizar PySide6/PyInstaller para Android.
- `[?]` Considerar WiFi/5G, avisos de datos móviles, modo solo WiFi, pausa al cambiar de red, almacenamiento y ejecución en segundo plano permitida por Android.
