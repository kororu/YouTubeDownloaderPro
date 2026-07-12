# Visión y arquitectura del proyecto

YouTube Downloader Pro es un frontend de escritorio para `yt-dlp` y `ffmpeg`. Su objetivo es ofrecer una experiencia Windows profesional, modular y distribuible mediante PyInstaller, sin ocultar que la compatibilidad con fuentes externas depende de las herramientas y sitios subyacentes.

Versión visible actual: `v0.3.0`.

## Arquitectura

```text
YouTubeDownloaderPro/
    app.py
    config/
    core/
    models/
    services/
    ui/
    widgets/
    dialogs/
    resources/
    styles/
    downloads/
    scripts/
    tests/
```

- `config`: configuración tipada y persistencia JSON.
- `core`: ciclo de vida, constantes, paths, entorno, dependencias, procesos y logging.
- `models`: modelos y enums del dominio sin dependencias de UI.
- `services`: metadata, playlists, cola, descarga, persistencia e integración con procesos externos.
- `ui`, `widgets` y `dialogs`: composición y presentación PySide6.
- `resources` y `styles`: assets, resolución segura de recursos y QSS.
- `scripts`: build y empaquetado portable de Windows.
- `tests`: validaciones automatizadas.

La UI no debe contener lógica directa de descarga, persistencia o `subprocess`. Los servicios deben permanecer independientes de widgets y la infraestructura externa debe estar centralizada.

## Estado funcional

### Implementado

- Shell PySide6, tema dark, fondo opcional, cola personalizada, logs, estado y ajustes.
- Descargas MP4/MP3 con selector de calidad y carpeta de salida.
- Persistencia de ajustes y cola.
- Videos individuales, playlists y YouTube Mix con carga incremental.
- Build PyInstaller `onedir` y flujo de paquete portable.

### En progreso

El working tree de `v0.3.0` contiene ejecución silenciosa, rangos de playlist, `Cargar siguientes`, historial por URL y deduplicación. Se requiere validación manual de descargas reales, listas grandes y portable antes de declarar la versión estable.

### Problemas recientes que guían el roadmap

- Ventanas emergentes de `yt-dlp`/FFmpeg y necesidad de ejecución silenciosa.
- Listas grandes que requieren rangos, bloques y cancelación segura.
- Logs de progreso que deben ser claros y acotados.
- Layout superior congestionado, controles cortados y mejoras visuales pendientes.
- Empaquetado portable que debe validarse fuera del equipo de desarrollo.

## Roadmap oficial hasta v1.0.0

### v0.3.0 - Silent downloads and playlist ranges

Objetivo: estabilizar la ejecución silenciosa y el procesamiento incremental de listas grandes.

- Ocultar ventanas emergentes de `yt-dlp` y FFmpeg.
- Centralizar procesos con `CREATE_NO_WINDOW` en Windows.
- Cargar rangos `1-200`, `201-400`, `401-600` y otros rangos válidos.
- Incorporar `Cargar siguientes` e historial por URL.
- Evitar duplicados en la cola.
- Mejorar cancelación, logs y soporte de YouTube Mix grandes.

Estado: implementado en el working tree; pendiente de validación manual completa y release.

### v0.4.0 - Queue and playlist advanced management

Objetivo: convertir la cola en una herramienta de gestión recuperable.

- Reordenar videos y establecer prioridades.
- Pausar/reanudar la cola y reintentar fallidos.
- Limpiar completados o errores.
- Guardar progreso por playlist y detectar archivos ya descargados.
- Exportar/importar cola.
- Introducir historial básico.

Estado: planificado.

### v0.5.0 - Audio and format improvements

Objetivo: ampliar formatos y control de salida.

- MP3, M4A, OPUS, FLAC y WAV.
- `Audio original / best audio` cuando la fuente lo permita.
- Perfiles original/best, 128, 192, 256 y 320 kbps.
- Miniaturas, metadata y subtítulos disponibles.
- Plantillas de nombres y carpetas opcionales por canal o playlist.

WAV será una opción orientada principalmente a edición: es audio sin compresión, ocupa mucho espacio y no restaura calidad ya perdida en una fuente comprimida. Puede evitar una segunda compresión, pero no constituye una mejora mágica. Para uso común, MP3/M4A/OPUS suelen ser preferibles; `best audio`, FLAC o WAV deben elegirse según el objetivo.

Estado: planificado.

### v0.6.0 - Visual polish and UX

Objetivo: hacer la interfaz más ordenada, adaptable y legible.

- Barra superior en dos filas o grupos y mejor separación de acciones.
- Corrección de textos cortados, combos y desplegables.
- Fondo con escalado automático y opacidad configurable.
- Modo compacto y vista de cola mejorada.
- Miniaturas en `QueueItemWidget`, iconos por estado, pantalla vacía, tooltips y atajos.

Estado: planificado.

### v0.7.0 - Download history and duplicate control

Objetivo: ofrecer trazabilidad completa de descargas.

- Historial buscable y prevención de duplicados.
- Abrir carpeta, copiar ruta y reintentar desde historial.
- Favoritos e importación/exportación del historial.

Estado: planificado.

### v0.8.0 - Advanced settings and diagnostics

Objetivo: cubrir escenarios avanzados sin degradar la experiencia básica.

- Límite de ancho de banda si `yt-dlp` lo admite.
- Concurrencia configurable.
- Cookies opcionales del navegador con advertencias y proxy personalizado.
- Logs exportables, modo diagnóstico y verificación avanzada de dependencias.
- Reset e importación/exportación de configuración.

Estado: planificado.

### v0.9.0 - Installer and release candidate

Objetivo: validar una distribución candidata a estable.

- Evaluar un instalador real y mantener un ZIP portable.
- Accesos directos, icono y metadata definitivos.
- Documentación de usuario final.
- Pruebas en otro PC y del `.exe` sin VS Code.
- Corrección final de defectos.

Estado: planificado.

### v1.0.0 - Stable Windows release

Objetivo: entregar una aplicación Windows estable y lista para compartir.

- Ejecutable y portable estables.
- Documentación y changelog completos.
- Manejo robusto de errores y descargas silenciosas.
- Playlists por rango y YouTube Mix estables.
- Audio avanzado, incluido WAV.
- Historial y control de duplicados.
- Interfaz ordenada y legible.

Estado: planificado; no representa la funcionalidad actual.

## Futuras versiones después de v1.0

### v1.1 - Multi-source downloads

Evaluar URLs de Facebook, X/Twitter, TikTok, Vimeo, Instagram, SoundCloud, clips/VOD de Twitch y otras fuentes compatibles con `yt-dlp`. La aplicación debería detectar el origen y avisar si se necesitan cookies o sesión. No se promete soporte absoluto: depende de `yt-dlp`, las condiciones de cada plataforma y sus cambios técnicos.

### v1.2 - Site profiles

Perfiles y opciones por plataforma, cookies opcionales, detección de errores y mensajes de ayuda específicos por fuente.

### v1.3 - Scheduler and automation

Programación horaria, apagado al finalizar, inicio opcional de cola con Windows y modo de bajo consumo.

### v1.4 - Remote companion

Evaluar una aplicación Android complementaria que controle por WiFi/5G el programa Windows. En una primera etapa, `yt-dlp` y FFmpeg continuarían ejecutándose en el PC.

### v2.0 - Android evaluation

Evaluar una aplicación Android separada, sin reutilizar PySide6/PyInstaller, con Kotlin, Java o Flutter. Considerar WiFi/5G, avisos y restricciones de datos móviles, modo solo WiFi, cambios de red, almacenamiento y ejecución en segundo plano permitida por Android.

Todas las versiones post-`v1.0` son sugerencias sujetas a investigación técnica, legal y de mantenimiento.

## Distribución y dependencias

- PyInstaller `onedir` es el formato actual.
- `yt-dlp` y FFmpeg permanecen como dependencias externas en `PATH`.
- La aplicación no debe instalarlos automáticamente ni empaquetarlos sin una decisión explícita futura.
- El portable debe verificarse en un sistema Windows independiente antes de publicarse.

## Uso responsable

YouTube Downloader Pro es un frontend para `yt-dlp` y `ffmpeg`. El usuario es responsable de respetar derechos de autor, términos de servicio y legislación aplicable. El uso recomendado se limita a contenido propio, libre, educativo o descargado con autorización.

## Estándares de ingeniería

- Python 3.12+, PySide6, type hints y docstrings Google cuando aporten claridad.
- Clean Architecture y módulos con responsabilidades definidas.
- Sin pseudocódigo, placeholders ni instalaciones automáticas.
- Cambios pequeños, verificables y compatibles con el historial.
- Ninguna función se marca como estable sin pruebas confirmadas.
