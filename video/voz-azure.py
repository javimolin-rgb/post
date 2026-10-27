#!/usr/bin/env python3
"""
Genera la locución definitiva con Azure Speech — licenciada para uso comercial.

  export AZURE_SPEECH_KEY=...        # clave de un recurso Speech
  export AZURE_SPEECH_REGION=eastus  # la región del recurso
  python3 voz-azure.py --voz es-CL-LorenzoNeural

Escribe voz-azure.wav a 48 kHz. Después:
  1. en audio.py, apuntar la mezcla a ese archivo en vez de la maqueta
  2. python3 audio.py --voice   (reescribe los subtítulos con los tiempos reales)
  3. node render.js && volver a encodear

La capa gratuita de Azure Speech cubre de sobra estas 12 líneas.
"""
import argparse, os, sys, wave, pathlib
import urllib.request
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ap = argparse.ArgumentParser()
ap.add_argument('--voz', default='es-CL-LorenzoNeural')
ap.add_argument('--rate', default='+0%', help='velocidad, p.ej. -5% si suena apurada')
ap.add_argument('--out', default=str(HERE / 'voz-azure.wav'))
a = ap.parse_args()

KEY = os.environ.get('AZURE_SPEECH_KEY')
REG = os.environ.get('AZURE_SPEECH_REGION')
if not KEY or not REG:
    sys.exit('Falta AZURE_SPEECH_KEY o AZURE_SPEECH_REGION')

# mismas líneas y tiempos que audio.py
from audio import SR, N, DUR, at, band          # reutiliza las utilidades
import audio as A

LINES = [
    (0.85,  "Lo que sostiene una casa casi nunca se ve."),
    (4.85,  "El tubo queda ahí, protegiendo el hormigón."),
    (7.95,  "La madera, bajo tierra, no dura."),
    (11.75, "Cada uno baja lo que necesita."),
    (14.75, "La casa queda a nivel sin mover tierra."),
    (18.60, "En invierno se nota: el agua sigue de largo."),
    (22.20, "Nada se empoza contra la estructura."),
    (25.45, "Entre el suelo y el piso circula aire."),
    (28.55, "Eso es lo que mantiene la casa seca."),
    (32.25, "A las termitas no les interesa el PVC."),
    (35.70, "Se instala y se olvida."),
    (38.55, "Si estás por construir, hablemos primero del terreno."),
]

URL = f'https://{REG}.tts.speech.microsoft.com/cognitiveservices/v1'
HDR = {'Ocp-Apim-Subscription-Key': KEY,
       'Content-Type': 'application/ssml+xml',
       'X-Microsoft-OutputFormat': 'riff-48khz-16bit-mono-pcm',
       'User-Agent': 'neorigen-reel'}

def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

voz = np.zeros(N)
for t0, text in LINES:
    ssml = (f'<speak version="1.0" xml:lang="es-CL">'
            f'<voice name="{a.voz}"><prosody rate="{a.rate}">{esc(text)}</prosody>'
            f'</voice></speak>')
    req = urllib.request.Request(URL, data=ssml.encode('utf-8'), headers=HDR)
    raw = urllib.request.urlopen(req, timeout=60).read()
    tmp = HERE / '_az_line.wav'; tmp.write_bytes(raw)
    with wave.open(str(tmp)) as w:
        sr0 = w.getframerate()
        s = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)/32768
    if sr0 != SR:
        s = np.interp(np.arange(int(len(s)*SR/sr0))*sr0/SR, np.arange(len(s)), s)
    f = int(0.015*SR); s[:f] *= np.linspace(0,1,f); s[-f:] *= np.linspace(1,0,f)
    at(voz, t0, s, 1.0)
    print(f'  {t0:6.2f} → {t0+len(s)/SR:6.2f}s   {text}')
    tmp.unlink()

p = np.max(np.abs(voz))
if p > 0: voz = voz/p*0.85
pcm = (np.clip(np.stack([voz,voz],axis=1),-1,1)*32767).astype('<i2')
with wave.open(a.out,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('escrito', a.out)
