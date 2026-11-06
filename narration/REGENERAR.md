# Regeneración de la película narrada

Requisitos: Python 3.11, Manim 0.21.0 y sus dependencias nativas, LaTeX con dvisvgm, FFmpeg y FFprobe en PATH, conexión a Internet y `edge-tts` 7.3.1 o posterior. Instala Manim con `pip install -r requirements.txt` y la voz con `pip install "edge-tts>=7.3.1"`. La versión 7.2.8 instalada inicialmente recibió HTTP 403; la 7.3.1 se comprobó en este entorno.

En PowerShell desde la raíz, con el entorno apropiado activo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/render_narrated.ps1
```

`cues.json` contiene el texto exacto y el identificador de cada señal. El primer paso genera MP3 independientes en `assets/audio/narration/`. `prepare_narrated_scene.py` deriva una escena de la película original, inserta señales en eventos visuales concretos y sustituye las esperas antiguas por pausas breves. Cada señal espera la duración real de su archivo más 0,3 segundos. La escena conserva las llamadas originales a `run_tarjan` y `validate_trace`. La película generada y el resultado original son independientes.

La mezcla crea `assets/audio/ambient_original.flac`, una textura ambiental original mediante cuatro ondas senoidales, con entrada y salida gradual, compresión lateral controlada por la voz, normalización de voz y limitador. No utiliza música de terceros. FFprobe verifica códecs, duración y coincidencia entre pistas y guarda su informe en `output/validacion_ffprobe.json`. El resultado se escribe en `output/Proyecto_AED_Articulaciones_Final.mp4`. El render usa la resolución original 1280 × 720 a 30 FPS.
