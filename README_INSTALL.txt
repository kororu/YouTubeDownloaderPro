YouTube Downloader Pro - Guia de instalacion portable
======================================================

Contenido de la carpeta portable:

- YouTubeDownloaderPro\
- install_dependencies.bat
- run_app.bat
- README_INSTALL.txt
- VERSION.txt

Como usar en otro PC Windows
----------------------------

1. Copie la carpeta completa YouTubeDownloaderPro_Portable al otro PC.
2. Ejecute install_dependencies.bat como administrador.
3. Cuando termine, ejecute run_app.bat.

Tambien puede abrir directamente:

YouTubeDownloaderPro\YouTubeDownloaderPro.exe

Dependencias externas
---------------------

La aplicacion no incluye yt-dlp ni ffmpeg por decision tecnica.
Estos programas deben instalarse en Windows con winget:

winget install yt-dlp
winget install ffmpeg

El archivo install_dependencies.bat revisa si faltan yt-dlp o ffmpeg,
pregunta antes de instalar y usa winget solo para las dependencias faltantes.

Si yt-dlp o ffmpeg no son detectados
------------------------------------

1. Cierre la ventana actual.
2. Abra una nueva terminal o reinicie Windows.
3. Ejecute install_dependencies.bat nuevamente.
4. Abra YouTube Downloader Pro otra vez.

Esto puede ser necesario porque Windows a veces no actualiza PATH en
terminales ya abiertas.

Advertencia de seguridad de Windows
-----------------------------------

Windows puede mostrar una advertencia al abrir un ejecutable nuevo descargado
o copiado desde otro equipo. Si usted confia en esta copia, seleccione
"Mas informacion" y luego "Ejecutar de todas formas".

Descargas
---------

Las descargas se guardan en la carpeta configurada desde la aplicacion.
Puede cambiar esa carpeta desde Ajustes.

Estado de esta version
----------------------

La version visible es v0.5.0. Antes de distribuir este paquete, se recomienda
probar descargas MP4 y MP3, playlists por rangos, YouTube Mix, la opcion
"Cargar siguientes" y la ausencia de ventanas emergentes de yt-dlp/ffmpeg.
Tambien se deben probar MP3, M4A, OPUS, FLAC, WAV, audio original,
miniaturas, metadata, subtitulos y plantillas de nombre.

Uso responsable
---------------

YouTube Downloader Pro es una interfaz para yt-dlp y ffmpeg. El usuario debe
respetar los derechos de autor, los terminos de servicio y la legislacion
aplicable. Utilice la herramienta con contenido propio, libre, educativo o
para el cual tenga autorizacion.

Compatibilidad con sitios
-------------------------

La version actual se centra en YouTube. El soporte futuro para otras fuentes
es solo una propuesta y dependera de yt-dlp y de los cambios de cada sitio.
