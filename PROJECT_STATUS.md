# Estado del proyecto

## Estado general

- Nombre del proyecto: YouTube Downloader Pro.
- Autor: Ariel Ponce.
- Versión actual visible: v0.3.0.
- Plataforma objetivo: Windows.
- Estado del ejecutable: generado en `dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe`; pendiente de verificación manual completa.
- Distribución final: PyInstaller en modo `onedir`.
- Stack técnico:
  - Python 3.12+.
  - PySide6.
  - QThread.
  - subprocess / yt-dlp / ffmpeg.
  - JSON para persistencia.
  - QSS para estilos.
  - PyInstaller para empaquetado.

## Estado del árbol de trabajo

- El working tree actual contiene cambios sin commit.
- La versión visible ya aparece como `v0.3.0`.
- Existe build generado con PyInstaller.
- Las pruebas manuales con URLs reales de YouTube, playlists, YouTube Mix, MP4 y MP3 están pendientes de verificar.

## Funcionalidades implementadas

- Aplicación Windows con PySide6.
- MainWindow basado en `QMainWindow`.
- Tema dark permanente.
- Opción de imagen de fondo personalizada.
- Escalado de imagen de fondo tipo cover, pendiente de verificación visual manual en el `.exe`.
- Cola de descargas basada en `QScrollArea` y widgets propios.
- `QueueItemWidget` para elementos de cola.
- `LogWidget` visible con exportación de logs.
- `SettingsWidget` para ajustes.
- `FooterWidget` con autor y versión.
- `AboutDialog`.
- Selector de formato:
  - MP4.
  - MP3.
- Selector de calidad:
  - Best available.
  - 480.
  - 720.
  - 1080.
  - 1440.
  - 2160.
- Límite de playlist/mix:
  - 50.
  - 100.
  - 200.
  - 500.
- Límite predeterminado de playlist/mix: 200 videos.
- Persistencia de settings en JSON.
- Persistencia de cola en JSON.
- Descargas con `yt-dlp`.
- Uso de `ffmpeg` para flujos que lo requieren, como MP3.
- Verificación de dependencias `yt-dlp` y `ffmpeg` en PATH.
- `install_dependencies.bat` como ayuda manual para instalar dependencias externas.
- PyInstaller configurado con `YouTubeDownloaderPro.spec`.
- Script de build Windows: `scripts\build_windows.ps1`.
- Soporte de video individual.
- Soporte de playlist y YouTube Mix.
- Soporte de carga incremental de playlist/mix.
- Soporte de carga por rango en el working tree actual, pendiente de prueba manual con URLs reales.
- Soporte de `Cargar siguientes` en el working tree actual, pendiente de prueba manual con URLs reales.
- Prevención de duplicados por `video_id` o URL en el working tree actual, pendiente de prueba manual con playlists reales.
- Ejecución silenciosa de procesos externos en Windows mediante configuración centralizada, pendiente de prueba manual con descargas reales.

## Problemas detectados y pendientes de verificar

- Ventanas emergentes de `yt-dlp.exe` o `ffmpeg.exe` durante descargas largas:
  - Estado actual: tratado en código con `CREATE_NO_WINDOW` y `STARTUPINFO`.
  - Pendiente de verificar: descarga real MP4 y MP3 desde el `.exe`.
- Necesidad de ocultar procesos externos:
  - Estado actual: existe `core/process.py` para centralizar la configuración de subprocess.
  - Pendiente de verificar: que no aparezcan ventanas externas durante metadata, playlist, Mix, MP4, MP3 y conversión con ffmpeg.
- Playlists o mixes muy grandes pueden colapsar si se procesan demasiados videos:
  - Estado actual: se mantiene límite predeterminado de 200 y procesamiento por rangos.
  - Pendiente de verificar: playlists reales de 400, 1000 o más videos.
- Necesidad de cargar playlists por rangos:
  - Estado actual: implementado en working tree con inicio, fin y límite.
  - Pendiente de verificar: rangos `1-200`, `201-400`, `401-600`.
- Necesidad de opción para cargar siguientes:
  - Estado actual: implementado como `Cargar siguientes`.
  - Pendiente de verificar: persistencia por URL entre sesiones.
- Posibles detalles visuales pendientes:
  - Verificar que el `.exe` mantenga dark mode.
  - Verificar contraste de desplegables.
  - Verificar escalado de imagen de fondo.
  - Verificar que paneles transparentes no reduzcan legibilidad.
- Validación manual pendiente:
  - Descargar 1 video MP4.
  - Descargar 1 video MP3.
  - Cargar playlist `1-200`.
  - Cargar playlist `201-400`.
  - Cargar YouTube Mix `1-200`.
  - Cargar YouTube Mix `201-400`.
  - Confirmar que no se dupliquen videos.
  - Confirmar que el log muestre progreso claro.
  - Confirmar que la UI no se congele.

## Decisiones técnicas tomadas

- No instalar `yt-dlp` automáticamente desde la app.
- No instalar `ffmpeg` automáticamente desde la app.
- No empaquetar `yt-dlp` dentro del `.exe`.
- No empaquetar `ffmpeg` dentro del `.exe`.
- Usar `install_dependencies.bat` como herramienta auxiliar manual.
- Mantener dark mode permanente.
- Eliminar la opción light.
- Mantener límite predeterminado de 200 videos por playlist/mix.
- Preferir procesamiento incremental por bloques.
- Preferir carga de playlist/mix por rangos para listas grandes.
- Usar PyInstaller en modo `onedir`.
- Mantener Clean Architecture:
  - UI en `ui/` y `widgets/`.
  - Modelos en `models/`.
  - Servicios en `services/`.
  - Infraestructura en `core/`.
  - Configuración en `config/`.

## Próxima versión planificada

### v0.3.0 - Silent downloads and playlist range loading

Estado actual: esta versión aparece implementada en el working tree actual, pero requiere verificación manual completa y commit.

Alcance documentado:

- Ocultar ventanas emergentes de `yt-dlp` y `ffmpeg`.
- Centralizar ejecución de subprocess.
- Agregar soporte para rangos de playlist.
- Agregar opción para cargar siguientes 200.
- Evitar duplicados en cola.
- Mejorar logs de progreso.
- Mejorar cancelación de análisis de playlist.
- Actualizar versión visible.

## Comandos útiles

Ejecutar la app:

```powershell
python app.py
```

Compilar módulos:

```powershell
python -m compileall .
```

Generar el `.exe`:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

Ejecutar el `.exe` generado:

```powershell
.\dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe
```

Revisar estado Git:

```powershell
git status
```

Revisar resumen de cambios:

```powershell
git diff --stat
```

## Flujo recomendado para continuar

Antes de modificar el proyecto, Codex debe leer:

- `AGENTS.md`
- `PROJECT_STATUS.md`

Luego debe implementar solo la próxima versión o commit solicitado.

## Notas para futuras sesiones

- No hacer `git commit` automáticamente salvo pedido explícito.
- No instalar dependencias externas automáticamente.
- No modificar archivos no relacionados.
- Si una funcionalidad no está confirmada con pruebas manuales, mantenerla marcada como pendiente de verificar.
