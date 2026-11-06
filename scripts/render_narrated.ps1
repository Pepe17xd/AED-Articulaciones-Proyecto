$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python scripts/generate_film_narration.py
    if ($LASTEXITCODE -ne 0) { throw 'Falló la generación de voz.' }
    python scripts/prepare_narrated_scene.py
    if ($LASTEXITCODE -ne 0) { throw 'Falló la preparación de la escena.' }
    python scripts/check_narration.py
    if ($LASTEXITCODE -ne 0) { throw 'Falló la verificación de la narración.' }
    python -m manim render -qm --disable_caching --progress_bar none --media_dir media/narrated src/animation/narrated_articulation_film.py NarratedArticulationFilm
    if ($LASTEXITCODE -ne 0) { throw 'Falló el render de Manim.' }
    python scripts/mix_final.py
    if ($LASTEXITCODE -ne 0) { throw 'Falló la mezcla o su validación.' }
} finally { Pop-Location }
