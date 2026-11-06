"""Generate one Edge TTS audio file per section of the Spanish script."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "narration" / "cues.json"
DEST = ROOT / "assets" / "audio" / "narration"


async def main() -> None:
    sections = json.loads(SCRIPT.read_text(encoding="utf-8"))
    DEST.mkdir(parents=True, exist_ok=True)
    for section in sections:
        if len(sys.argv) > 1 and section["id"] not in sys.argv[1:]:
            continue
        output = DEST / f"{section['id']}.mp3"
        await edge_tts.Communicate(section["text"], "es-MX-JorgeNeural", rate="-5%").save(str(output))
        if output.stat().st_size == 0:
            raise RuntimeError(f"Audio vacío: {output}")
        print(output)


if __name__ == "__main__":
    asyncio.run(main())
