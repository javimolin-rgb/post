#!/usr/bin/env python3
"""
Diseño sonoro de "Lo que pasa en seis meses".

Igual que en la primera pieza, todo se sintetiza acá (osciladores y ruido
filtrado): es material propio, sin licencia que respetar ni atribución que
poner, como pide §9 del manual de marca.

  python3 audio-seis-meses.py
    -> seis-meses-musica.wav           la que va: sólo música
    -> seis-meses-mus-ambiente.wav     alternativa con sonido de obra
  y escribe la tabla de escenas dentro de seis-meses-reel.html.
"""
import sys, wave, pathlib
import numpy as np

SR = 48000
# Tabla de escenas: manda sobre todo lo demás. Este script la escribe también
# dentro del HTML, así imagen y audio no pueden desalinearse.
ESCENAS = [(0.00, 5.20), (4.80, 5.60), (10.00, 5.60), (15.20, 5.60),
           (20.40, 5.80), (25.80, 5.80), (31.20, 5.20), (36.00, 4.60)]
ini = lambda i: ESCENAS[i][0]
fin = lambda i: ESCENAS[i][0] + ESCENAS[i][1]

DUR  = round(fin(len(ESCENAS) - 1), 2)
N    = int(SR * DUR)
T    = np.arange(N) / SR
HERE = pathlib.Path(__file__).resolve().parent
rng  = np.random.default_rng(20261102)          # determinista

# ---------------------------------------------------------------- utilidades
def noise(n=N):
    return rng.standard_normal(n).astype(np.float64)

def band(x, lo=None, hi=None, slope=4):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    H = np.ones_like(f)
    if lo:  H *= 1.0 / np.sqrt(1.0 + (lo / np.maximum(f, 1e-6)) ** slope)
    if hi:  H *= 1.0 / np.sqrt(1.0 + (f / hi) ** slope)
    return np.fft.irfft(X * H, n=len(x))

def env(points):
    ts = np.array([p[0] for p in points], dtype=float)
    vs = np.array([p[1] for p in points], dtype=float)
    return np.interp(T, ts, vs, left=vs[0], right=vs[-1])

def at(buf, t0, sig, gain=1.0):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    k = min(len(sig), N - i)
    buf[i:i + k] += sig[:k] * gain

def lfo(freq, depth=0.5, phase=0.0):
    return 1.0 - depth + depth * (0.5 + 0.5 * np.sin(2 * np.pi * freq * T + phase))

# ---------------------------------------------------------------- música
NOTE = {'E2':82.41,'F2':87.31,'G2':98.00,'A2':110.00,'C3':130.81,'D3':146.83,
        'E3':164.81,'F3':174.61,'G3':196.00,'A3':220.00,'B3':246.94,
        'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392.00,'A4':440.00,
        'B4':493.88,'C5':523.25,'D5':587.33,'E5':659.25,'G5':783.99}

def pad(f, dur, atk=1.6, rel=2.8, seed=0):
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
    """Piano de fieltro: parciales que decaen + golpe de martillo."""
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for k, amp, dec in ((1, 1.0, 2.8), (2, .40, 1.7), (3, .17, 1.0),
                        (4, .085, .70), (6, .035, .45)):
        y += amp * np.sin(2 * np.pi * f * k * t) * np.exp(-t / dec)
    y += band(noise(n), 900, 4200) * np.exp(-t / .012) * .16
    a = int(.006 * SR); y[:a] *= np.linspace(0, 1, a)
    return band(y, None, 2700)

mus = np.zeros(N)
# Una escena, un acorde. La progresión sube y recién cierra en la entrega:
# Am · F · C · G · Dm · F · G · C — el reposo llega con la casa terminada.
ACORDES = [(['A3','C4','E4'],'A2'), (['F3','A3','C4'],'F2'), (['C4','E4','G4'],'C3'),
           (['G3','B3','D4'],'G2'), (['D4','F4','A4'],'D3'), (['F3','A3','C4'],'F2'),
           (['G3','B3','D4'],'G2'), (['C4','E4','G4'],'C3')]
CHORDS = [(ini(i), t, b) for i, (t, b) in enumerate(ACORDES)]
for i, (t0, tones, bass) in enumerate(CHORDS):
    t1 = CHORDS[i + 1][0] if i + 1 < len(CHORDS) else DUR
    d = t1 - t0
    at(mus, t0, pad(NOTE[bass], d, 1.8, 3.0, seed=i), 0.50)
    for j, nm in enumerate(tones):
        at(mus, t0 + j * .10, pad(NOTE[nm], d, 1.6, 2.8, seed=i * 7 + j), 0.34)

# Dos o tres notas por escena. La melodía gana una nota más alta a medida que
# la casa sube, y se asienta en el cierre.
MEL_REL = [[(1.5,'E5'),(3.2,'C5'),(4.4,'A4')],      # gancho
           [(1.2,'A4'),(3.0,'C5'),(4.6,'F4')],      # diseño
           [(1.2,'G4'),(2.9,'C5'),(4.5,'E5')],      # fundación
           [(1.2,'B4'),(3.0,'D5'),(4.6,'G4')],      # estructura
           [(1.2,'A4'),(3.0,'D5'),(4.7,'F4')],      # envolvente
           [(1.2,'C5'),(3.0,'A4'),(4.7,'F4')],      # terminaciones
           [(1.1,'D5'),(2.8,'G5'),(4.2,'B4')],      # entrega
           [(0.9,'E5'),(2.4,'C5'),(3.6,'G4')]]      # cierre
for i, grupo in enumerate(MEL_REL):
    for dt, nm in grupo:
        at(mus, ini(i) + dt, pluck(NOTE[nm]), 0.30)

mp = np.max(np.abs(mus))
if mp > 0: mus = mus / mp
mus *= env([(0, 0), (2.2, 1), (DUR - 2.6, 1), (DUR, 0)])

# ---------------------------------------------------------------- obra
# Sonido de obra a bajo volumen: el manual lo pide como oficio, no como efecto.
def thud(f0=105, f1=52, dur=0.55, tau=0.17, click=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / tau)
    tr   = band(noise(n), 60, 1800) * np.exp(-t / 0.035) * click
    return body * 0.9 + tr

def tap(f0=620, dur=0.26, tau=0.045):
    """Martillo sobre madera: cuerpo corto y mate, nada metálico."""
    n = int(dur * SR); t = np.arange(n) / SR
    y  = np.sin(2 * np.pi * f0 * t) * np.exp(-t / tau) * .5
    y += np.sin(2 * np.pi * f0 * 1.47 * t) * np.exp(-t / (tau * .7)) * .25
    y += band(noise(n), 300, 3400) * np.exp(-t / .018)
    return band(y, 120, 5200)

obra = np.zeros(N)
# peso de la tierra
drone  = band(noise(), None, 92, slope=6)
drone += np.sin(2 * np.pi * 46.0 * T) * 0.25 + np.sin(2 * np.pi * 69.0 * T) * 0.12
obra += drone * env([(0,0),(2.0,1),(ini(7)-1.4,1),(DUR-2.0,.8),(DUR,0)]) * lfo(.045,.28) * 0.050
# aire
air = band(noise(), 240, 1900)
obra += air * env([(0,.18),(ini(1),.22),(ini(4),.34),(ini(6),.22),(DUR,0)]) * lfo(.07,.45) * 0.026
# los cinco pilotes bajan (etapa 02), con los tiempos de la animación
for i in range(5):
    at(obra, ini(2) + 0.45 + i * 0.24, thud(108 - i * 5, 54, .6, .16, .40), 0.38)
at(obra, ini(2) + 2.05, thud(70, 38, .9, .30, .15), 0.22)       # apoya la plataforma
# el marco se arma (etapa 03): clavado pausado, no una ráfaga
for dt in (0.55, 0.82, 1.06, 1.62, 1.88, 2.12, 2.74, 3.00, 3.62, 3.88):
    at(obra, ini(3) + dt, tap(600 + (int(dt * 97) % 90)), 0.055)
# la envolvente cierra el volumen: un roce sordo y largo
n5 = int(2.4 * SR); t5 = np.arange(n5) / SR
cierre = band(noise(n5), 120, 2200) * np.sin(np.pi * np.clip(t5 / 2.2, 0, 1)) ** 1.4
at(obra, ini(4) + 0.45, cierre, 0.055)
# terminaciones: unos pocos golpes finos
for dt in (0.70, 1.15, 2.05, 2.60):
    at(obra, ini(5) + dt, tap(760 + (int(dt * 131) % 70), .18, .032), 0.040)
# la casa se entrega: un swell cálido y bajo
n6 = int(3.0 * SR); t6 = np.arange(n6) / SR
swell = band(noise(n6), 60, 520) * np.sin(np.pi * t6 / 3.0) ** 2
at(obra, ini(6) + 0.20, swell, 0.055)

# ---------------------------------------------------------------- mezcla
def reverb(x, dur=2.6, pre=0.035, damp=3400, seed=0):
    n = int(dur * SR); t = np.arange(n) / SR
    g = np.random.default_rng(1000 + seed)
    ir = g.standard_normal(n) * np.exp(-t * (6.2 / dur))
    ir = band(ir, 130, damp)
    ir[:int(pre * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum()) or 1.0
    M = 1 << (len(x) + n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, M) * np.fft.rfft(ir, M), M)[:len(x)]

WET = 0.30
musL = mus * (1 - WET) + reverb(mus, seed=1) * WET
musR = mus * (1 - WET) + reverb(mus, seed=2) * WET

# §9 pide ~-14 LUFS y pico <= -1 dBTP. Con este material (música sostenida,
# rango dinámico chico) 0.75 de pico deja -14,2 LUFS y -2,5 dBTP: medido, no
# estimado — ver el bloque de verificación al final del README.
def norm(st, peak=0.75):
    p = np.max(np.abs(st))
    return st / p * peak if p > 0 else st

sola = norm(np.stack([musL, musR], axis=1))

# alternativa: la misma música con la obra por debajo
OBRA_LEVEL = 0.85
wide = band(noise(), 600, 7000) * env([(0,0),(ini(3),.35),(ini(5),.30),(DUR,0)]) * 0.022
conObra = norm(np.stack([musL * .82 + (obra + wide) * OBRA_LEVEL,
                         musR * .82 + (obra - wide) * OBRA_LEVEL], axis=1))

def write_wav(path, data):
    d = np.clip(data, -1, 1)
    pcm = (d * 32767).astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print('escrito', path)

write_wav(HERE / 'seis-meses-musica.wav', sola)
write_wav(HERE / 'seis-meses-mus-ambiente.wav', conObra)

# ---------------------------------------------------------------- HTML
_html = HERE / 'seis-meses-reel.html'
_src = _html.read_text(encoding='utf-8')
_filas = ',\n  '.join("{id:'s%d',start:%.2f,dur:%.2f}" % (k + 1, a, b)
                      for k, (a, b) in enumerate(ESCENAS))
_k0 = _src.index('/* SCENES:INICIO */'); _k1 = _src.index('/* SCENES:FIN */')
_html.write_text(_src[:_k0] + '/* SCENES:INICIO */\nconst SCENES=[\n  ' + _filas
                 + '\n];\nconst TOTAL=%.2f;\n' % DUR + _src[_k1:], encoding='utf-8')
print(f'  escenas escritas en el HTML (total {DUR:.2f}s)')
