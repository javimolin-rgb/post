#!/usr/bin/env python3
"""
Genera la locución definitiva con Azure Speech — licenciada para publicar.

  export AZURE_SPEECH_KEY=...        # clave de un recurso Speech
  export AZURE_SPEECH_REGION=eastus  # la región del recurso
  python3 voz-azure.py                       # usa la voz y el guion de audio.py
  python3 voz-azure.py --rate "+6%"          # si hace falta apurarla o soltarla

Escribe voz-azure.wav con las locuciones ya colocadas en el mismo lugar del
montaje. Después:
  1. en audio.py, cargar ese wav en vez de sintetizar la maqueta
  2. python3 audio.py --voice   (reescribe los subtítulos con los tiempos reales)
  3. node render.js && volver a encodear

El guion se lee directamente de audio.py, así no se pueden desincronizar.
La capa gratuita de Azure Speech cubre de sobra estas líneas.
"""
import argparse, ast, os, pathlib, sys, wave
import urllib.request
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
SR = 48000
DUR = 43.0
N = int(SR * DUR)

def del_audio(nombre):
    """Lee una constante de audio.py sin ejecutar todo el módulo."""
    arbol = ast.parse((HERE / 'audio.py').read_text(encoding='utf-8'))
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and getattr(nodo.targets[0], 'id', None) == nombre:
            return ast.literal_eval(nodo.value)
    raise SystemExit(f'no encontré {nombre} en audio.py')

VO_SCENES = del_audio('VO_SCENES')
VOZ_DEF   = del_audio('VOZ')
RATE_DEF  = del_audio('RATE')

ap = argparse.ArgumentParser()
ap.add_argument('--voz',  default=VOZ_DEF)
ap.add_argument('--rate', default=RATE_DEF)
ap.add_argument('--out',  default=str(HERE / 'voz-azure.wav'))
a = ap.parse_args()

KEY = os.environ.get('AZURE_SPEECH_KEY')
REG = os.environ.get('AZURE_SPEECH_REGION')
if not KEY or not REG:
    sys.exit('Falta AZURE_SPEECH_KEY o AZURE_SPEECH_REGION')

URL = f'https://{REG}.tts.speech.microsoft.com/cognitiveservices/v1'
HDR = {'Ocp-Apim-Subscription-Key': KEY,
       'Content-Type': 'application/ssml+xml',
       'X-Microsoft-OutputFormat': 'riff-48khz-16bit-mono-pcm',
       'User-Agent': 'neorigen-reel'}
esc = lambda t: t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def decir(texto):
    ssml = (f'<speak version="1.0" xml:lang="es-CL"><voice name="{a.voz}">'
            f'<prosody rate="{a.rate}">{esc(texto)}</prosody></voice></speak>')
    raw = urllib.request.urlopen(
        urllib.request.Request(URL, data=ssml.encode('utf-8'), headers=HDR), timeout=60).read()
    tmp = HERE / '_az_line.wav'; tmp.write_bytes(raw)
    with wave.open(str(tmp)) as w:
        sr0 = w.getframerate()
        s = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64)/32768
    tmp.unlink()
    if sr0 != SR:
        s = np.interp(np.arange(int(len(s)*SR/sr0))*sr0/SR, np.arange(len(s)), s)
    # mismo recorte de silencio que la maqueta, para que los tiempos calcen
    e = np.convolve(np.abs(s), np.ones(int(.02*SR))/int(.02*SR), mode='same')
    viva = np.where(e > 10 ** (-46/20))[0]
    if len(viva):
        s = s[max(0, viva[0]-int(.05*SR)) : min(len(s), viva[-1]+int(.07*SR))]
    f = int(.012*SR); s[:f] *= np.linspace(0,1,f); s[-f:] *= np.linspace(1,0,f)
    return s

TAIL = 0.35
voz = np.zeros(N)
for s0, s1, lead, lineas in VO_SCENES:
    audios = [decir(t) for t, _sub, _g in lineas]
    dur = [len(x)/SR for x in audios]
    base = [g for _t, _sub, g in lineas]
    n = len(lineas)
    sobra = ((s1 - TAIL) - (s0 + lead)) - sum(dur) - sum(base[:-1])
    extra = min(max(sobra,0)/(n-1), 0.65) if n > 1 else 0.0
    t = s0 + lead + min(max(sobra,0) - extra*(n-1), 1.0) * 0.5
    for k, x in enumerate(audios):
        i = int(t*SR); m = min(len(x), N-i)
        if m > 0: voz[i:i+m] += x[:m]
        print(f'  {t:6.2f} → {t+dur[k]:6.2f}s   {lineas[k][0]}')
        t += dur[k] + (base[k] + extra if k < n-1 else 0.0)

p = np.max(np.abs(voz))
if p > 0: voz = voz/p*0.85
with wave.open(a.out,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(np.stack([voz,voz],axis=1),-1,1)*32767).astype('<i2').tobytes())
print('escrito', a.out, f'(voz {a.voz}, rate {a.rate})')
