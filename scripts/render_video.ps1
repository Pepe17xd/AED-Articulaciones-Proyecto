$ErrorActionPreference = 'Stop'

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$sceneFile = Join-Path $projectRoot 'src\animation\articulation_film.py'
$mediaDirectory = Join-Path $projectRoot 'media\final'
$manim = Get-Command manim -ErrorAction Stop

Push-Location $projectRoot
try {
    & $manim.Source render -qm --disable_caching --progress_bar none `
        --media_dir $mediaDirectory $sceneFile ArticulationFilm
    if ($LASTEXITCODE -ne 0) {
        throw "Manim render failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
