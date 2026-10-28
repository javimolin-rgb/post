#!/usr/bin/env python3
"""
Muestras de Kokoro (Apache-2.0), el único motor libre de los que trae
VoiceStudio que corre rápido en CPU y acá sí se puede instalar.

  pip install kokoro-onnx soundfile
  B=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
  curl -LO $B/kokoro-v1.0.onnx && curl -LO $B/voices-v1.0.bin
  python3 muestras-kokoro.py

Sus tres voces en español (ef_dora, em_alex, em_santa) suenan peninsulares.
No hay voz chilena en ningún modelo libre: para eso hay que clonar una.
"""
import pathlib, subprocess, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'muestras'; OUT.mkdir(exist_ok=True)
MOD = sys.argv[1] if len(sys.argv) > 1 else '.'

FRASE = ("Antes de la primera tabla, hay una decisión que no se ve… "
         "sobre qué se va a parar tu casa. "
         "¿Termitas? Al pe ve ce no le interesan.")

k = Kokoro(f'{MOD}/kokoro-v1.0.onnx', f'{MOD}/voices-v1.0.bin')
for v in ('em_alex', 'em_santa', 'ef_dora'):
    s, sr = k.create(FRASE, voice=v, speed=1.05, lang='es')
    wav = OUT / f'kokoro-{v}.wav'
    sf.write(wav, s, sr)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(wav),
                    '-c:a', 'libmp3lame', '-b:a', '128k',
                    str(OUT / f'kokoro-{v}.mp3')], check=True)
    wav.unlink()
    print(f'  kokoro-{v}.mp3  {len(s)/sr:.2f}s')
