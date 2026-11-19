"""Generate one Edge TTS audio file per section of the Spanish script."""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCRIPT = ROOT / "narration" / "cues.json"
DEFAULT_DEST = ROOT / "assets" / "audio" / "narration_v3_guion"


def project_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


async def main() -> None:
    parser = argparse.ArgumentParser(description="Genera un MP3 por señal de narración.")
    parser.add_argument("--script", type=Path, default=DEFAULT_SCRIPT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DEST)
    parser.add_argument("--voice", default="es-MX-JorgeNeural")
    parser.add_argument("--rate", default="+15%", help="Velocidad Edge TTS; por ejemplo +15%%")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    sections = json.loads(project_path(args.script).read_text(encoding="utf-8"))
    destination = project_path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    for section in sections:
        output = destination / f"{section['id']}.mp3"
        if output.exists() and not args.overwrite:
            raise FileExistsError(f"{output} ya existe; elige otra carpeta o pasa --overwrite")
        await edge_tts.Communicate(section["text"], args.voice, rate=args.rate).save(str(output))
        if output.stat().st_size == 0:
            raise RuntimeError(f"Audio vacío: {output}")
        print(output)


if __name__ == "__main__":
    asyncio.run(main())
