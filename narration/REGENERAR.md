# Regeneración de la película narrada

Requisitos: Python 3.11, Manim 0.21.0 y sus dependencias nativas, LaTeX con dvisvgm, FFmpeg y FFprobe en PATH y conexión a Internet. Instala las dependencias Python con `python -m pip install -r requirements-film-narration.txt`. La versión 7.2.8 de `edge-tts` recibió HTTP 403; se requiere 7.3.1 o posterior. El archivo local `requirements-narration.txt` corresponde a otro prototipo y no es necesario para esta película.

En PowerShell desde la raíz, con el entorno apropiado activo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/render_narrated.ps1
```

`cues.json` contiene el texto exacto y el identificador de cada señal. El primer paso genera MP3 independientes en `assets/audio/narration/`. `prepare_narrated_scene.py` deriva una escena de la película original, inserta señales en eventos visuales concretos y sustituye las esperas antiguas por pausas breves. Cada señal espera la duración real de su archivo más 0,3 segundos. La escena conserva las llamadas originales a `run_tarjan` y `validate_trace`. La película generada y el resultado original son independientes.

La mezcla crea `assets/audio/ambient_original.flac`, una textura ambiental original mediante cuatro ondas senoidales, con entrada y salida gradual, compresión lateral controlada por la voz, normalización de voz y limitador. No utiliza música de terceros. FFprobe verifica códecs, duración y coincidencia entre pistas y guarda su informe en `output/validacion_ffprobe.json`. El resultado se escribe en `output/Proyecto_AED_Articulaciones_Final.mp4`. El render usa la resolución original 1280 × 720 a 30 FPS.

## Edición v2

La edición nueva reutiliza los MP3 ya generados y crea su escena a partir de `articulation_film.py` con `python scripts/prepare_narrated_v2.py`. Las señales no bloquean la animación al comenzar: la siguiente señal espera solo el tiempo que falte para que termine la anterior. La última señal se completa antes de finalizar la película. Esta edición está en revisión: los puntos visuales y el equilibrio de la mezcla deben verificarse en el MP4 renderizado.

Consulta el README para los comandos de vista previa, 1080p30 y mezcla. `scripts/mix_final_v2.py` utiliza `assets/audio/ambient_original.flac`, creado por el sintetizador del proyecto, sin descargar música de terceros. También admite `--music` para una pista autorizada. El resultado usa una ruta distinta de la película anterior.


## Guion actualizado v3

La pelicula compartida `src/animation/film_v3.py` usa las senales de `narration/cues.json`; cada MP3 se genera en `assets/audio/narration_v3_guion/` y se reproduce durante la accion visual correspondiente. Esta carpeta es separada de `assets/audio/narration/`, donde se conservan los 19 archivos anteriores. Requiere conectividad con Edge TTS.

En PowerShell desde la raiz, con `.venv` y FFmpeg/FFprobe disponibles:

```powershell
.\.venv\Scripts\python.exe scripts/generate_film_narration.py --script narration/cues.json --output-dir assets/audio/narration_v3_guion --voice es-MX-JorgeNeural --rate '+40%' --overwrite
$env:AED_NARRATION = '1'
$env:AED_NARRATION_DIR = 'assets/audio/narration_v3_guion'
.\.venv\Scripts\python.exe -m manim render -qh --fps 30 --disable_caching --progress_bar none --media_dir media/v3_guion_final src/animation/film_v3.py ArticulationFilmV3
.\.venv\Scripts\python.exe scripts/mix_final_v2.py media/v3_guion_final/videos/film_v3/1080p30/ArticulationFilmV3.mp4 --output output/final_v3/Articulaciones_v3.mp4 --music-gain 0.8
```

Antes de reemplazar una entrega existente, respaldala con `Copy-Item output/final_v3/Articulaciones_v3.mp4 output/final_v3/Articulaciones_v3_pre_guion.mp4`. La musica es la textura ambiental original `assets/audio/ambient_original.flac`; el mezclador la mantiene por debajo de la voz mediante ducking, y aplica fundidos y limitacion.

## Guion editorial v3

`narration/cues.json` contiene 680 palabras en 27 senales. Los MP3 van a `assets/audio/narration_v3_editorial/`, separados de las versiones previas. A +15% los audios suman 248.71 s; la vista previa con animacion mide 254.7 s. Usa los comandos de la seccion "Edicion editorial optimizada" del README para generar la salida Full HD nueva.
