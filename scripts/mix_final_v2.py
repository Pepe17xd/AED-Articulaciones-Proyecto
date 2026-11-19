"""Mezcla una película narrada con el ambiente original en una salida nueva."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'output/final_v2/Articulaciones_v2.mp4')
    parser.add_argument('--music', type=Path, default=ROOT / 'assets/audio/ambient_original.flac')
    parser.add_argument('--music-gain', type=float, default=0.12)
    args = parser.parse_args()
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(args.video)], check=True, capture_output=True, text=True)
    info = json.loads(result.stdout)
    duration = float(info['format']['duration'])
    streams = {stream['codec_type']: stream for stream in info['streams']}
    video_duration = float(streams['video']['duration'])
    voice_duration = float(streams['audio']['duration'])
    if abs(video_duration - voice_duration) > 0.15:
        raise ValueError(f'Video y voz tienen duraciones distintas: {video_duration:.2f} / {voice_duration:.2f} s')
    if duration >= 300:
        raise ValueError(f'La película supera el límite: {duration:.2f} s')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if not args.music.exists():
        if args.music != ROOT / 'assets/audio/ambient_original.flac':
            raise FileNotFoundError(args.music)
        args.music.parent.mkdir(parents=True, exist_ok=True)
        sound = (f'aevalsrc=0.14*sin(2*PI*110*t)+0.08*sin(2*PI*164.81*t)'
                 f'+0.06*sin(2*PI*220*t)+0.04*sin(2*PI*329.63*t):s=48000:d={duration}')
        subprocess.run(['ffmpeg', '-y', '-f', 'lavfi', '-i', sound, '-af', 'volume=0.16',
                        '-c:a', 'flac', str(args.music)], check=True)
    fade = max(0, duration - 3)
    # Gain stays configurable so the legacy v2 mix remains unchanged; v3 uses
    # a more audible bed before sidechain ducking keeps it under the voice.
    filters = (f'[1:a]volume={args.music_gain},afade=t=in:st=0:d=3,afade=t=out:st={fade}:d=3[bed];'
               '[0:a]loudnorm=I=-16:TP=-2:LRA=11,asplit=2[voice][key];'
               '[bed][key]sidechaincompress=threshold=0.015:ratio=8:attack=30:release=500[duck];'
               '[voice][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]')
    subprocess.run(['ffmpeg', '-y', '-i', str(args.video), '-stream_loop', '-1', '-i', str(args.music),
                    '-filter_complex', filters, '-map', '0:v:0', '-map', '[a]', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(args.output)], check=True)
    subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,duration', '-of', 'json', str(args.output)], check=True)

if __name__ == '__main__':
    main()
