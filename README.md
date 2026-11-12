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
