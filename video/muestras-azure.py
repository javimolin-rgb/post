#!/usr/bin/env python3
"""
Muestras de las voces neuronales de Microsoft (las mismas de Azure Speech),
para ELEGIR locutor. Se generan vía edge-tts, que usa el servicio de lectura
en voz alta de Edge.

  OJO: este audio es SOLO para evaluar. Para publicar hay que generarlo con
  una clave propia de Azure Speech (tiene capa gratuita), que es donde estas
  mismas voces están licenciadas para uso comercial.

  python3 muestras-azure.py
"""
import asyncio, os, pathlib, subprocess, wave
import numpy as np
import edge_tts

HERE = pathlib.Path(__file__).resolve().parent
OUT  = HERE / 'muestras'; OUT.mkdir(exist_ok=True)
TMP  = HERE / '_az'; TMP.mkdir(exist_ok=True)
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
SR = 24000

FRASE = ("Lo que sostiene una casa casi nunca se ve. "
         "A las termitas no les interesa el PVC. "
         "Si estás por construir, hablemos primero del terreno.")

VOCES = [
 ('1', 'es-CL-LorenzoNeural',  'hombre',  'chile',     'hombre, español de Chile'),
 ('2', 'es-CL-CatalinaNeural', 'mujer',   'chile',     'mujer, español de Chile'),
 ('3', 'es-US-AlonsoNeural',   'hombre',  'eeuu',      'hombre, español de Estados Unidos'),
 ('4', 'es-US-PalomaNeural',   'mujer',   'eeuu',      'mujer, español de Estados Unidos'),
 ('5', 'es-CO-GonzaloNeural',  'hombre',  'colombia',  'hombre, español de Colombia'),
 ('6', 'es-PE-AlexNeural',     'hombre',  'peru',      'hombre, español de Perú'),
]

async def tts(voice, text, path):
    c = edge_tts.Communicate(text, voice, proxy=PROXY)
    await c.save(str(path))

def load(mp3):
    wv = mp3.with_suffix('.tmp.wav')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(mp3),
                    '-ar',str(SR),'-ac','1',str(wv)], check=True)
    with wave.open(str(wv)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)/32768
    wv.unlink(); return a

def save(path, a):
    a = a/max(np.max(np.abs(a)),1e-9)*0.89
    wv = path.with_suffix('.tmp.wav')
    with wave.open(str(wv),'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(wv),
                    '-c:a','libmp3lame','-b:a','128k',str(path)], check=True)
    wv.unlink(); print('  ', path.name)

async def main():
    sil = lambda s: np.zeros(int(s*SR))
    combo = [sil(0.4)]
    for num, voz, sexo, pais, desc in VOCES:
        p1, p2 = TMP/f'{num}a.mp3', TMP/f'{num}b.mp3'
        await tts(voz, f"Opción {num}. {desc}.", p1)
        await tts(voz, FRASE, p2)
        a = np.concatenate([load(p1), sil(0.35), load(p2)])
        save(OUT/f'azure-{num}-{sexo}-{pais}.mp3', a)
        combo += [a, sil(0.9)]
    save(OUT/'comparacion-azure.mp3', np.concatenate(combo))

asyncio.run(main())
