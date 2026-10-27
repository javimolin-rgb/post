#!/usr/bin/env python3
"""Genera muestras de voz para elegir locutor. python3 muestras.py"""
import subprocess, sys, wave, pathlib
import numpy as np

SR_OUT = 24000
HERE = pathlib.Path(__file__).resolve().parent
OUT  = HERE / 'muestras'
TMP  = HERE / '_mu'; TMP.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)

def say(model, text, speaker=None, ls='0.88'):
    f = TMP / 'x.wav'
    cmd = [sys.executable, '-m', 'piper', '-m', str(HERE/'voice'/model),
           '-f', str(f), '--length-scale', ls]
    if speaker is not None: cmd += ['-s', str(speaker)]
    subprocess.run(cmd, input=text.encode('utf-8'), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(str(f)) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)/32768
        if w.getnchannels() == 2: a = a.reshape(-1,2).mean(1)
    if sr != SR_OUT:
        a = np.interp(np.arange(int(len(a)*SR_OUT/sr))*sr/SR_OUT, np.arange(len(a)), a)
    return a

def sil(s): return np.zeros(int(s*SR_OUT))

def write(path, a):
    a = a / max(np.max(np.abs(a)), 1e-9) * 0.89
    pcm = (np.clip(a,-1,1)*32767).astype('<i2')
    wv = path.with_suffix('.wav')
    with wave.open(str(wv),'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR_OUT)
        w.writeframes(pcm.tobytes())
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(wv),
                    '-c:a','libmp3lame','-b:a','128k',str(path)], check=True)
    wv.unlink()
    print('  ', path.name)

FRASE = ("Lo que sostiene una casa casi nunca se ve. "
         "A las termitas no les interesa el pe ve ce. "
         "Si estás por construir, hablemos primero del terreno.")

VOCES = [
 ('A', 'es_MX-ald-medium',      None, 'hombre, español de México. La voz actual'),
 ('B', 'es_ES-davefx-medium',   None, 'hombre, español de España'),
 ('C', 'es_ES-sharvard-medium', 0,    'hombre, español de España, segunda opción'),
 ('D', 'es_MX-claude-high',     None, 'mujer, español de México'),
 ('E', 'es_AR-daniela-high',    None, 'mujer, español de Argentina'),
 ('F', 'es_ES-sharvard-medium', 1,    'mujer, español de España'),
]

print('muestras individuales:')
combo = [sil(0.4)]
for letra, modelo, spk, desc in VOCES:
    pres = f"Opción {letra}. {desc}."
    a = np.concatenate([say(modelo, pres, spk), sil(0.35), say(modelo, FRASE, spk)])
    reg = 'hombre' if 'hombre' in desc else 'mujer'
    pais = 'mexico' if 'México' in desc else ('argentina' if 'Argentina' in desc else 'espana')
    write(OUT / f'voz-{letra}-{reg}-{pais}.mp3', a)
    combo += [a, sil(0.9)]
write(OUT / 'comparacion-de-voces.mp3', np.concatenate(combo))

# --- cómo escribir PVC y el dominio para que no los lea mal
print('prueba de pronunciación:')
M = 'es_MX-ald-medium'
PRUEBAS = [("Así está escrito hoy.", "A las termitas no les interesa el PVC."),
           ("Escrito con puntos.",   "A las termitas no les interesa el P.V.C."),
           ("Escrito fonético.",     "A las termitas no les interesa el pe ve ce."),
           ("El dominio, tal cual.", "Cotiza en neorigen.cl"),
           ("El dominio, fonético.", "Cotiza en neorigen punto ce ele.")]
seq=[sil(0.4)]
for intro, txt in PRUEBAS:
    seq += [say(M, intro), sil(0.25), say(M, txt), sil(0.8)]
write(OUT / 'prueba-pronunciacion.mp3', np.concatenate(seq))
