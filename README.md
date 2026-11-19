# Proyecto AED: puntos de articulación en grafos

Implementación original del algoritmo DFS de Tarjan para detectar puntos de articulación en grafos no dirigidos. El proyecto registra y valida los eventos de la ejecución, y Manim Community los convierte en una animación educativa.

**Integrantes:** Antony Yonel Rosales Esteban, Itta Zhair Saavedra Clavijo y Jeseph Imanol Burgos Ochoa.

## Qué calcula

Un vértice es un punto de articulación si al eliminarlo aumenta el número de componentes conexas del grafo. Tarjan resuelve el problema con una búsqueda en profundidad (DFS): `tin[u]` registra cuándo se descubre `u`, y `low[u]` el instante más antiguo al que se puede volver desde el subárbol DFS de `u` usando aristas del árbol y, como máximo, una arista de retorno.

Al terminar de visitar un hijo `v` de un vértice no raíz `u`, la condición `low[v] >= tin[u]` identifica una articulación. La raíz DFS usa una regla distinta: es articulación cuando tiene más de un hijo en el bosque DFS. El algoritmo procesa grafos conexos y desconectados en tiempo `O(V + E)`. La implementación acepta grafos simples con etiquetas de texto y rechaza lazos y aristas paralelas.

La animación no programa a mano el recorrido: llama a `run_tarjan`, valida su traza y reproduce sus eventos.

## Herramientas y requisitos

- Python 3.11.
- Manim Community 0.21.0, fijado en `requirements.txt`.
- LaTeX y `dvisvgm` para las fórmulas `MathTex` de la película.
- Git para clonar el repositorio.

La dependencia Python se instala con pip en un entorno virtual. Manim también necesita componentes nativos según el sistema: en Windows puede requerirse Microsoft C++ Build Tools si pip debe compilar una dependencia; en macOS, Cairo y `pkg-config`; en Linux, compilador C, headers de Python, Cairo y Pango. Consulta la [guía oficial de instalación de Manim Community](https://docs.manim.community/en/stable/installation.html) y su guía [para Windows, macOS y Linux](https://docs.manim.community/en/stable/installation.html#installing-manim-locally).

Para las fórmulas, instala una distribución TeX: MiKTeX o TeX Live en Windows, MacTeX en macOS y TeX Live en Linux. Comprueba que `latex`, `dvisvgm` y `xelatex` estén disponibles en `PATH` si también compilarás el informe.

El proyecto se comprobó en Windows 11 con Python 3.11.9, Manim Community 0.21.0 y PyAV. Las instrucciones de Linux y macOS reflejan los requisitos generales de Manim, pero no se ejecutaron en esos sistemas.

## Clonar e instalar

### Windows PowerShell

```powershell
git clone https://github.com/Pepe17xd/AED-Articulaciones-Proyecto.git
Set-Location AED-Articulaciones-Proyecto
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno, usa `python` desde su ruta completa, por ejemplo `& .\.venv\Scripts\python.exe -m pip install -r requirements.txt`, y antepone `& .\.venv\Scripts\manim.exe` a los comandos Manim.

### Linux y macOS

```bash
git clone https://github.com/Pepe17xd/AED-Articulaciones-Proyecto.git
cd AED-Articulaciones-Proyecto
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecutar Tarjan sin Manim

Desde la raíz del repositorio, este ejemplo ejecuta la implementación y muestra las articulaciones, `tin` y `low` del grafo ilustrativo. En Windows PowerShell:

```powershell
python .\scripts\run_example.py
```

En Linux y macOS:

```bash
python scripts/run_example.py
```

Resultado esperado: articulaciones `('A', 'B', 'D', 'E')`. El orden de vecinos es lexicográfico para que el recorrido y la traza sean deterministas.

## Animaciones y video

La edición narrada se configura mediante [`narration/cues.json`](narration/cues.json), y sus instrucciones de regeneración están en [`narration/REGENERAR.md`](narration/REGENERAR.md). Las señales se insertan en momentos visuales de una escena derivada de la película original. El resultado se guarda en `output/Proyecto_AED_Articulaciones_Final.mp4`.

Para la versión narrada, instala también `python -m pip install -r requirements-film-narration.txt`; requiere FFmpeg, FFprobe e Internet. Los audios son generados localmente. El MP4 narrado es una salida distinta y su publicación queda pendiente de decidir.

Renderiza primero la escena corta de traza a baja calidad. Escribe bajo `media/previews/` y conserva intacto el video final:

```powershell
manim render -ql --disable_caching --progress_bar none --media_dir .\media\previews .\src\animation\trace_preview.py TracePreview -o TracePreview
```

El resultado es `media/previews/videos/trace_preview/480p15/TracePreview.mp4`.

Para generar la película final a 720p30 en Windows, ejecuta:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\render_video.ps1
```

O, con el entorno virtual activo, en cualquier terminal:

```bash
manim render -qm --disable_caching --progress_bar none --media_dir media/final src/animation/articulation_film.py ArticulationFilm
```

El comando final escribe `media/final/videos/articulation_film/720p30/ArticulationFilm.mp4` y reemplaza ese archivo si ya existe. Para una renderización rápida de toda la película, cambia `-qm` por `-ql` y `media/final` por `media/previews`; no uses la carpeta final para pruebas.

## Archivos de entrega

- Video final 720p30: [`media/final/videos/articulation_film/720p30/ArticulationFilm.mp4`](media/final/videos/articulation_film/720p30/ArticulationFilm.mp4).

El MP4 incluido es un render anterior a la corrección del ejemplo de raíz. Hay que regenerarlo y revisarlo antes de publicar una versión corregida. Los tests y el informe son materiales locales.

## Organización del código

- `src/articulations/`: grafo, algoritmo Tarjan, eventos y validación de la traza.
- `src/animation/trace_preview.py`: escena breve conducida por eventos reales.
- `src/animation/articulation_film.py`: película de siete secuencias.
- `src/animation/intro_graph.py`: definición compartida del grafo introductorio.
- `scripts/render_video.ps1`: render de producción en Windows.
- `media/final/`: MP4 final incluido en la entrega.
- `requirements-film-narration.txt`: dependencias Python adicionales para la versión narrada.

## Edición narrada v2 (en desarrollo)

La película base sigue usando `run_tarjan` y `validate_trace`; `src/animation/graph_view.py` reúne los elementos visuales compartidos. La escena narrada se regenera a partir de la película actual con `scripts/prepare_narrated_v2.py`; reutiliza los MP3 existentes de `assets/audio/narration/`. Las señales se reproducen durante la animación y la siguiente señal espera a que termine la anterior. La mezcla v2 usa la textura original sintetizada del proyecto, atenuación lateral por la voz y fundidos; escribe en `output/final_v2/`, sin modificar el MP4 anterior.

Con Python y las dependencias de `requirements-film-narration.txt`, FFmpeg, FFprobe, LaTeX y dvisvgm disponibles en PATH, desde PowerShell:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_narrated_v2.py
.\.venv\Scripts\python.exe -m manim render -ql --disable_caching --progress_bar none --media_dir media/v2_preview src/animation/narrated_articulation_film_v2.py NarratedArticulationFilmV2
.\.venv\Scripts\python.exe -m manim render -qh --fps 30 --disable_caching --progress_bar none --media_dir media/v2_final src/animation/narrated_articulation_film_v2.py NarratedArticulationFilmV2
.\.venv\Scripts\python.exe scripts/mix_final_v2.py media/v2_final/videos/narrated_articulation_film_v2/1080p30/NarratedArticulationFilmV2.mp4
```

Si los ejecutables locales descargados están en `tmp/ffmpeg-download`, antepón `$env:PATH = "$(Resolve-Path 'tmp/ffmpeg-download');$env:PATH"` durante esa sesión. La carpeta temporal y los audios generados no forman parte del repositorio; para regenerar los MP3 consulta `narration/REGENERAR.md`. La version v2 se conserva como salida anterior en `output/final_v2/`; la producción v3 se documenta a continuación.

## Producción v3 final

Antes de reemplazar la película de esta carpeta, conserva la anterior como `output/final_v3/Articulaciones_v3_pre_guion.mp4`. La mezcla nueva mantiene la versión v2 intacta.

La película compartida vive en `src/animation/film_v3.py`. La misma clase `ArticulationFilmV3` admite voz o modo silencioso con `AED_NARRATION=1` / `0`; `src/animation/narrated_film_v3.py` importa esa escena. `narration/cues.json` contiene 27 señales del guion actualizado. Sus voces se guardan aparte en `assets/audio/narration_v3_guion/`; los 19 MP3 previos de `assets/audio/narration/` permanecen intactos. El algoritmo y las animaciones de la ejecución usan `run_tarjan` y `validate_trace`.

En PowerShell, desde la raíz del repositorio, con `.venv`, Manim Community, PyAV, LaTeX/dvisvgm y FFmpeg/FFprobe disponibles:

```powershell
$env:PATH = "$(Resolve-Path 'tmp/ffmpeg-download');$env:PATH"
if (-not (Test-Path 'output/final_v3/Articulaciones_v3_pre_guion.mp4')) { Copy-Item -LiteralPath 'output/final_v3/Articulaciones_v3.mp4' -Destination 'output/final_v3/Articulaciones_v3_pre_guion.mp4' }
$env:AED_NARRATION = '1'
$env:AED_NARRATION_DIR = 'assets/audio/narration_v3_guion'
.\.venv\Scripts\python.exe scripts/generate_film_narration.py --script narration/cues.json --output-dir assets/audio/narration_v3_guion --voice es-MX-JorgeNeural --rate '+40%' --overwrite
.\.venv\Scripts\python.exe -m manim render -qh --fps 30 --disable_caching --progress_bar none --media_dir media/v3_guion_final src/animation/film_v3.py ArticulationFilmV3
.\.venv\Scripts\python.exe scripts/mix_final_v2.py media/v3_guion_final/videos/film_v3/1080p30/ArticulationFilmV3.mp4 --output output/final_v3/Articulaciones_v3.mp4 --music-gain 0.8
```

El mezclador conserva la voz y `assets/audio/ambient_original.flac`, aplica ducking, limitador y fundidos. Para renderizar sin voz, establece `$env:AED_NARRATION = '0'` y renderiza la misma escena con Manim; no invoques el mezclador de narración. Ejecuta las pruebas con `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.

Video de entrega v3 (Full HD 1080p30, 4:51.7): [output/final_v3/Articulaciones_v3.mp4](output/final_v3/Articulaciones_v3.mp4). La v3 anterior se conserva en `output/final_v3/Articulaciones_v3_pre_guion.mp4`; v2 permanece en `output/final_v2/`.

## Edición editorial optimizada

El guion de `narration/cues.json` conserva los siete bloques y queda en 680 palabras. Las 27 voces a +15% suman 248.71 s. La edición final narrada y mezclada dura 254.8 s (4:14.8), en Full HD 1080p30; la mezcla conserva la música ambiental y el ducking. Archivo: `output/final_v3_optimizada/Articulaciones_v3_optimizada.mp4`. No sobrescribe los MP4 anteriores.

En PowerShell desde la raiz del repositorio:

```powershell
$env:PATH = (Resolve-Path 'tmp\ffmpeg-download').Path + ';' + $env:PATH
$env:AED_NARRATION = '1'
$env:AED_NARRATION_DIR = 'assets/audio/narration_v3_editorial'
.\.venv\Scripts\python.exe scripts/generate_film_narration.py --script narration/cues.json --output-dir assets/audio/narration_v3_editorial --voice es-MX-JorgeNeural --rate '+15%' --overwrite
.\.venv\Scripts\python.exe -m manim render -qh --fps 30 --disable_caching --progress_bar none --media_dir media/v3_editorial_final src/animation/film_v3.py ArticulationFilmV3
.\.venv\Scripts\python.exe scripts/mix_final_v2.py media/v3_editorial_final/videos/film_v3/1080p30/ArticulationFilmV3.mp4 --output output/final_v3_optimizada/Articulaciones_v3_optimizada.mp4 --music-gain 0.8
```

Las pruebas se ejecutan con ` .\.venv\Scripts\python.exe -m unittest discover -s tests -v`.
