"""Check that every requested cue exists and contains decoded audio."""
from pathlib import Path
import json
import av
import numpy as np

root = Path(__file__).resolve().parents[1]
cues = json.loads((root / "narration/cues.json").read_text(encoding="utf-8"))
scene = (root / "src/animation/narrated_articulation_film.py").read_text(encoding="utf-8")
measurements = []
for cue in cues:
    cue_id = cue["id"]
    if scene.count(f'self.narrate("{cue_id}")') != 1:
        raise RuntimeError(f"La señal no aparece exactamente una vez en la escena: {cue_id}")
    path = root / "assets/audio/narration" / (cue_id + ".mp3")
    with av.open(str(path)) as audio:
        duration = audio.duration / 1_000_000
        frames = [frame.to_ndarray().astype(np.float64).ravel() for frame in audio.decode(audio=0)]
    if not frames:
        raise RuntimeError(f"La señal está vacía: {cue_id}")
    samples = np.concatenate(frames)
    rms = float(np.sqrt(np.mean(samples * samples)))
    if duration <= 0 or rms < 0.001:
        raise RuntimeError(f"La señal no contiene voz audible: {cue_id}")
    measurements.append({"id": cue_id, "duration_seconds": duration, "rms": rms})
report = root / "output/validacion_narracion.json"
report.parent.mkdir(parents=True, exist_ok=True)
report.write_text(json.dumps(measurements, indent=2), encoding="utf-8")
print(f"{len(measurements)} señales verificadas: {report}")
