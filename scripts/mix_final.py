"""Mix the rendered voice with an original, synthesized ambient background."""
from pathlib import Path
import json
import subprocess
import av

ROOT = Path(__file__).resolve().parents[1]
video = ROOT / "media/narrated/videos/narrated_articulation_film/720p30/NarratedArticulationFilm.mp4"
output = ROOT / "output/Proyecto_AED_Articulaciones_Final.mp4"
music = ROOT / "assets/audio/ambient_original.flac"
with av.open(str(video)) as container:
    duration = container.duration / 1_000_000 + 3
if duration > 300:
    raise RuntimeError(f"La película excede cinco minutos: {duration:.2f} s")
output.parent.mkdir(parents=True, exist_ok=True)
music.parent.mkdir(parents=True, exist_ok=True)
# Four quiet, sustained sine components form an original ambient texture.
# Sidechain compression lowers it further whenever speech is present.
fade_out = max(0, duration - 3)
filters = (
    f"[0:v]tpad=stop_mode=clone:stop_duration=3,fade=t=out:st={duration - 1.2}:d=1.2[v];"
    "[1:a]anull[bed];"
    f"[0:a]apad,atrim=duration={duration},loudnorm=I=-16:TP=-2:LRA=11,asplit=2[voice][key];"
    "[bed][key]sidechaincompress=threshold=0.015:ratio=8:attack=30:release=500[duck];"
    "[voice][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]"
)
sound = (f"aevalsrc=0.14*sin(2*PI*110*t)+0.08*sin(2*PI*164.81*t)"
         f"+0.06*sin(2*PI*220*t)+0.04*sin(2*PI*329.63*t):s=48000:d={duration}")
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", sound, "-af",
                f"volume=0.16,afade=t=in:st=0:d=3,afade=t=out:st={fade_out}:d=3",
                "-c:a", "flac", str(music)], check=True)
subprocess.run(["ffmpeg", "-y", "-i", str(video), "-i", str(music),
                "-filter_complex", filters, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output)], check=True)
result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(output)], check=True, capture_output=True, text=True)
report = json.loads(result.stdout)
streams = {stream["codec_type"]: stream for stream in report["streams"]}
assert streams["video"]["codec_name"] == "h264"
assert streams["audio"]["codec_name"] == "aac"
assert abs(float(streams["video"]["duration"]) - float(streams["audio"]["duration"])) < 0.1
assert float(report["format"]["duration"]) <= 300
(ROOT / "output/validacion_ffprobe.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(f"Video verificado: {output} ({duration:.2f} s)")
