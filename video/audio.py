#!/usr/bin/env python3
"""
Diseño sonoro de "La casa empieza bajo tierra".

Todo el audio se sintetiza acá (ruido filtrado y osciladores), así que no
depende de ninguna biblioteca con licencia: es material propio y libre de
derechos, como pide §9 del manual de marca.

  python3 audio.py            -> out/sfx.wav     (ambiente y efectos)
  python3 audio.py --voice    -> ademas voz.wav y mezcla-voz.wav (maqueta)
"""
import sys, wave, subprocess, pathlib
import numpy as np

SR   = 48000
DUR  = 43.0
N    = int(SR * DUR)
T    = np.arange(N) / SR
HERE = pathlib.Path(__file__).resolve().parent
rng  = np.random.default_rng(20261027)       # determinista

# ---------------------------------------------------------------- utilidades
def noise(n=N):
    return rng.standard_normal(n).astype(np.float64)

def band(x, lo=None, hi=None, slope=4):
    """Filtro en el dominio de la frecuencia: simple, estable y vectorizado."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    H = np.ones_like(f)
    if lo:  H *= 1.0 / np.sqrt(1.0 + (lo / np.maximum(f, 1e-6)) ** slope)
    if hi:  H *= 1.0 / np.sqrt(1.0 + (f / hi) ** slope)
    return np.fft.irfft(X * H, n=len(x))

def env(points):
    """Envolvente lineal a partir de pares (segundo, valor)."""
    ts = np.array([p[0] for p in points], dtype=float)
    vs = np.array([p[1] for p in points], dtype=float)
    return np.interp(T, ts, vs, left=vs[0], right=vs[-1])

def at(buf, t0, sig, gain=1.0):
    """Suma `sig` en el instante t0."""
    i = int(t0 * SR)
    if i >= N: return
    k = min(len(sig), N - i)
    buf[i:i + k] += sig[:k] * gain

def thud(f0=105, f1=52, dur=0.55, tau=0.17, click=0.35):
    """Golpe de colocación: seno que cae de tono + transitorio de tierra."""
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / tau)
    tr   = band(noise(n), 60, 1800) * np.exp(-t / 0.035) * click
    return body * 0.9 + tr

def swipe(dur=0.30, tau=0.09):
    n = int(dur * SR); t = np.arange(n) / SR
    s = band(noise(n), 1400, 6500) * np.exp(-t / tau)
    s += band(noise(n), 90, 400) * np.exp(-t / 0.05) * 0.5
    return s

def whoosh(dur=0.75, lo=180, hi=1600):
    """Aire de transición: vende el movimiento de cámara entre escenas."""
    n = int(dur * SR); t = np.arange(n) / SR
    e = np.sin(np.pi * t / dur) ** 2
    return band(noise(n), lo, hi) * e

def lfo(freq, depth=0.5, phase=0.0):
    return 1.0 - depth + depth * (0.5 + 0.5 * np.sin(2 * np.pi * freq * T + phase))

# ---------------------------------------------------------------- capas
mix = np.zeros(N)

# 1 · peso de la tierra: un zumbido grave constante
drone  = band(noise(), None, 95, slope=6) * 1.0
drone += np.sin(2 * np.pi * 47.0 * T) * 0.25
drone += np.sin(2 * np.pi * 70.5 * T) * 0.12
mix += drone * env([(0,0),(2.2,1),(37.0,1),(41.6,.85),(43,0)]) * lfo(.045,.28) * 0.055

# 2 · aire: colchón muy bajo, sube en la escena de ventilación
air = band(noise(), 240, 1900)
mix += air * env([(0,.20),(24.6,.22),(26.3,.75),(31.4,.55),(37.6,.25),(43,0)]) * lfo(.07,.45) * 0.030

# 3 · lluvia: aparece en la pendiente y crece en la escena de lluvias
rain = band(noise(), 750, 7500) * 0.8 + band(noise(), 200, 750) * 0.35
mix += rain * env([(0,0),(14.3,0),(15.6,.34),(17.8,.40),(19.0,1.0),
                   (24.2,1.0),(25.6,.12),(26.6,0),(43,0)]) * 0.075

# 4 · el agua que escurre: en la pendiente y bajo la casa
flow = band(noise(), 380, 3200) * lfo(.55,.55) * lfo(.23,.35,1.2)
mix += flow * env([(0,0),(14.8,0),(16.0,.55),(18.2,.45),(19.8,.85),
                   (24.4,.75),(25.8,0),(43,0)]) * 0.055

# 5 · la casa se asienta sobre los pilotes (gancho)
at(mix, 1.62, thud(95, 44, .9, .26, .25), 0.24)

# 6 · colocación de los cinco pilotes en la pendiente
for i, t0 in enumerate([12.65, 12.87, 13.09, 13.31, 13.53]):
    at(mix, t0, thud(108 - i * 5, 54, .6, .16, .40), 0.40)
at(mix, 14.05, thud(70, 38, .9, .30, .15), 0.22)          # la plataforma apoya

# 7 · vaciado del hormigón dentro del tubo (5,70 → 7,90)
pn = int(2.6 * SR); pt = np.arange(pn) / SR
pour = band(noise(pn), 140, 2600) * (0.25 + 0.75 * np.sin(np.pi * np.clip(pt/2.2,0,1))**1.5)
pour += band(noise(pn), 60, 260) * np.clip(pt/2.2, 0, 1) * 0.8
at(mix, 5.70, pour, 0.085)
at(mix, 7.95, thud(85, 40, .7, .22, .20), 0.20)           # queda lleno

# 8 · los tres descartes (no se pudre / termitas / corrosión)
for t0 in (33.05, 33.60, 34.15):
    at(mix, t0, swipe(), 0.085)

# 9 · transiciones de cámara
for t0, lo, hi, g in [(4.00,220,1700,.085),(10.80,160,1200,.075),
                      (17.60,220,1700,.080),(24.40,260,2000,.085),
                      (31.20,200,1500,.080),(37.40,140,1000,.070)]:
    at(mix, t0, whoosh(.85, lo, hi), g)

# 10 · cierre
at(mix, 38.0, whoosh(2.4, 60, 420), 0.055)

# ---------------------------------------------------------------- música
# Lecho instrumental propio: piano de fieltro sintetizado y pad cálido.
# Los acordes cambian exactamente en los cortes de escena, así la música
# acompaña el montaje en vez de correr por debajo sin relación.
NOTE = {'F2':87.31,'A2':110.00,'C3':130.81,'D3':146.83,'E3':164.81,'F3':174.61,
        'G3':196.00,'A3':220.00,'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,
        'G4':392.00,'A4':440.00,'C5':523.25,'D5':587.33,'E5':659.25}

def pad(f, dur, atk=1.5, rel=2.8, seed=0):
    n = int((dur + rel) * SR); t = np.arange(n) / SR
    g = np.random.default_rng(int(f * 10) + seed)
    y = np.zeros(n)
    for k, amp, det in ((1, 1.0, 0), (2, .28, 2.5), (3, .11, -3), (4, .045, 4)):
        y += amp * np.sin(2 * np.pi * f * k * 2 ** (det / 1200) * t + g.random() * 6.283)
    e = np.ones(n)
    a = int(atk * SR); e[:a] = np.linspace(0, 1, a) ** 1.7
    d = int(rel * SR); e[-d:] *= np.linspace(1, 0, d) ** 1.8
    e *= .86 + .14 * np.sin(2 * np.pi * .085 * t + seed)
    return band(y * e, None, 1250)

def pluck(f, dur=3.4):
    """Nota de piano de fieltro: parciales que decaen + golpe de martillo."""
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for k, amp, dec in ((1, 1.0, 2.8), (2, .40, 1.7), (3, .17, 1.0),
                        (4, .085, .70), (6, .035, .45)):
        y += amp * np.sin(2 * np.pi * f * k * t) * np.exp(-t / dec)
    y += band(noise(n), 900, 4200) * np.exp(-t / .012) * .16
    a = int(.006 * SR); y[:a] *= np.linspace(0, 1, a)
    return band(y, None, 2700)

mus = np.zeros(N)
# (inicio, acorde, bajo) — los inicios son los de las escenas
CHORDS = [(0.0, ['A3','C4','E4'], 'A2'), (4.2, ['F3','A3','C4'], 'F2'),
          (11.0,['C4','E4','G4'], 'C3'), (17.8,['D4','F4','A4'], 'D3'),
          (24.6,['F3','A3','C4'], 'F2'), (31.4,['A3','C4','E4'], 'A2'),
          (37.6,['C4','E4','G4'], 'C3')]
for i, (t0, tones, bass) in enumerate(CHORDS):
    t1 = CHORDS[i + 1][0] if i + 1 < len(CHORDS) else DUR
    d = t1 - t0
    at(mus, t0, pad(NOTE[bass], d, 1.8, 3.0, seed=i), 0.50)
    for j, nm in enumerate(tones):
        at(mus, t0 + j * .10, pad(NOTE[nm], d, 1.6, 2.8, seed=i * 7 + j), 0.34)

MEL = [(1.60,'E5'),(3.10,'C5'),
       (5.40,'A4'),(7.70,'C5'),(9.70,'F4'),
       (12.10,'G4'),(14.30,'E5'),(16.20,'C5'),
       (18.70,'D5'),(21.00,'A4'),(23.10,'F4'),
       (25.50,'C5'),(27.70,'A4'),(29.90,'F4'),
       (32.30,'E5'),(34.50,'C5'),(36.30,'A4'),
       (38.60,'E5'),(40.40,'C5'),(41.80,'A4')]
for t0, nm in MEL:
    at(mus, t0, pluck(NOTE[nm]), 0.30)

mp = np.max(np.abs(mus))
if mp > 0: mus = mus / mp
mus *= env([(0,0),(2.6,1),(40.4,1),(43,0)])
MUS_LEVEL = 0.115          # va bajo: acompaña, no compite
mix += mus * MUS_LEVEL

# ---------------------------------------------------------------- estéreo
# la lluvia y el aire se abren; los golpes quedan al centro
wide  = band(noise(), 600, 7000) * env([(0,0),(15.6,.25),(19.0,.6),(24.2,.6),(25.8,0),(43,0)]) * 0.030
L = mix + wide
R = mix - wide
st = np.stack([L, R], axis=1)

peak = np.max(np.abs(st))
if peak > 0: st = st / peak * 0.72

def write_wav(path, data):
    d = np.clip(data, -1, 1)
    pcm = (d * 32767).astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print('escrito', path)

OUT = HERE.parent / 'out'
OUT.mkdir(exist_ok=True)
write_wav(HERE / 'sfx.wav', st)
write_wav(HERE / 'musica.wav', np.stack([mus, mus], axis=1))   # para ajustar el balance aparte

# ---------------------------------------------------------------- voz (maqueta)
if '--voice' in sys.argv:
    MODEL = HERE / 'voice' / 'es_MX-ald-medium.onnx'      # voz masculina, es-MX
    # (inicio, locución, subtítulo, fin de la escena)
    # El guion NO repite los textos en pantalla: los complementa.
    LINES = [
        (0.85,  "Lo que sostiene una casa casi nunca se ve.",
                ["Lo que sostiene una casa", "casi nunca se ve."], 4.60),
        (4.85,  "El tubo queda ahí, protegiendo el hormigón.",
                ["El tubo queda ahí,", "protegiendo el hormigón."], 11.40),
        (7.95,  "La madera, bajo tierra, no dura.",
                ["La madera, bajo tierra,", "no dura."], 11.40),
        (11.75, "Cada uno baja lo que necesita.",
                ["Cada uno baja", "lo que necesita."], 18.20),
        (14.75, "La casa queda a nivel sin mover tierra.",
                ["La casa queda a nivel", "sin mover tierra."], 18.20),
        (18.60, "En invierno se nota: el agua sigue de largo.",
                ["En invierno se nota:", "el agua sigue de largo."], 25.00),
        (22.20, "Nada se empoza contra la estructura.",
                ["Nada se empoza", "contra la estructura."], 25.00),
        (25.45, "Entre el suelo y el piso circula aire.",
                ["Entre el suelo y el piso", "circula aire."], 31.80),
        (28.55, "Eso es lo que mantiene la casa seca.",
                ["Eso es lo que mantiene", "la casa seca."], 31.80),
        (32.25, "A las termitas no les interesa el PVC.",
                ["A las termitas", "no les interesa el PVC."], 38.00),
        (35.70, "Se instala y se olvida.",
                ["Se instala", "y se olvida."], 38.00),
        (38.55, "Si estás por construir, hablemos primero del terreno.",
                ["Si estás por construir,", "hablemos primero del terreno."], 43.00),
    ]
    voz = np.zeros(N)
    tmp = HERE / '_vo'; tmp.mkdir(exist_ok=True)
    spans = []
    for i, (t0, text, sub, tend) in enumerate(LINES):
        f = tmp / f'l{i:02d}.wav'
        subprocess.run([sys.executable, '-m', 'piper', '-m', str(MODEL),
                        '-f', str(f), '--length-scale', '0.88',
                        '--noise-w-scale', '0.85'],
                       input=text.encode('utf-8'), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with wave.open(str(f), 'rb') as w:
            sr0 = w.getframerate()
            a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64) / 32768
            if w.getnchannels() == 2: a = a.reshape(-1, 2).mean(axis=1)
        if sr0 != SR:                                    # remuestreo lineal a 48 k
            a = np.interp(np.arange(int(len(a) * SR / sr0)) * sr0 / SR,
                          np.arange(len(a)), a)
        a = band(a, 90, 12000)                           # limpia graves de sala
        f_in = int(0.015 * SR)
        a[:f_in] *= np.linspace(0, 1, f_in); a[-f_in:] *= np.linspace(1, 0, f_in)
        at(voz, t0, a, 1.0)
        d = len(a) / SR
        spans.append((t0, t0 + d, tend, text, sub))
        print(f'  {t0:6.2f} → {t0+d:6.2f}s   {text}')
    bad = False
    for j in range(len(spans)):
        s0, s1, send, tx = spans[j][:4]
        if s1 > send:
            print(f'  ! se pasa de la escena por {s1-send:.2f}s: {tx}'); bad = True
        if j + 1 < len(spans) and s1 > spans[j+1][0]:
            print(f'  ! se pisa con la siguiente por {s1-spans[j+1][0]:.2f}s: {tx}'); bad = True
    print('  locuciones: ' + ('REVISAR' if bad else 'sin choques ni desbordes'))
    # escribe los subtítulos, con sus tiempos reales, dentro del HTML
    rows = ',\n  '.join(
        '{a:%.2f,b:%.2f,l:[%s]}' % (s0, s1, ','.join(repr(x) for x in sub))
        for s0, s1, _send, _tx, sub in spans)
    html = HERE / 'pilotes-reel.html'
    src = html.read_text(encoding='utf-8')
    k0 = src.index('/* SUBS:INICIO */'); k1 = src.index('/* SUBS:FIN */')
    src = src[:k0] + '/* SUBS:INICIO */\nlet SUBS=[\n  ' + rows + '\n];\n' + src[k1:]
    html.write_text(src, encoding='utf-8')
    print('  subtitulos escritos en pilotes-reel.html')
    p = np.max(np.abs(voz))
    if p > 0: voz = voz / p * 0.85
    write_wav(HERE / 'voz.wav', np.stack([voz, voz], axis=1))
    duck = 1.0 - 0.55 * np.clip(np.convolve(np.abs(voz),
            np.ones(int(.12 * SR)) / (.12 * SR), mode='same') * 6, 0, 1)
    m2 = np.stack([L * duck + voz * .95, R * duck + voz * .95], axis=1)
    p = np.max(np.abs(m2))
    if p > 0: m2 = m2 / p * 0.9
    write_wav(HERE / 'mezcla-voz.wav', m2)
