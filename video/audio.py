#!/usr/bin/env python3
"""
Diseño sonoro de "La casa empieza bajo tierra".

Todo el audio se sintetiza acá (ruido filtrado y osciladores), así que no
depende de ninguna biblioteca con licencia: es material propio y libre de
derechos, como pide §9 del manual de marca.

  python3 audio.py            -> out/sfx.wav     (ambiente y efectos)
  python3 audio.py --voice    -> ademas voz.wav y mezcla-voz.wav (maqueta)
"""
import os, sys, wave, subprocess, pathlib
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
# ---------------------------------------------------------------- voz
# Guion locutado. No repite los textos en pantalla: los complementa, y usa
# preguntas para enganchar. "pe ve ce" va escrito fonético para que la V se
# lea "ve" y no "uve"; el subtítulo sigue diciendo PVC.
#
# Cada escena define su retardo de entrada y la pausa después de cada línea,
# y los tiempos se calculan con la duración real de cada locución. Así las
# pausas quedan donde se quieren (después de una pregunta) y no aparecen
# huecos por descuadre.
VOZ = 'es-CL-CatalinaNeural'      # mujer, español de Chile
RATE = '+12%'

VO_SCENES = [
 # (inicio, fin, retardo, [(hablado, subtítulo, pausa después), ...])
 (0.0, 4.6, 0.55, [
   ("¿Sabes sobre qué se apoya tu casa?",
    ["¿Sabes sobre qué", "se apoya tu casa?"], 0.45),
   ("Casi nunca se ve.",
    ["Casi nunca se ve."], 0.0)]),
 (4.2, 11.4, 0.60, [
   ("El tubo queda protegiendo el hormigón.",
    ["El tubo queda", "protegiendo el hormigón."], 0.50),
   ("¿Por qué no madera? Bajo tierra no dura.",
    ["¿Por qué no madera?", "Bajo tierra no dura."], 0.0)]),
 (11.0, 18.2, 0.60, [
   ("¿Y si el terreno está en pendiente?",
    ["¿Y si el terreno", "está en pendiente?"], 0.45),
   ("Cada pilote baja lo que necesita.",
    ["Cada pilote baja", "lo que necesita."], 0.40),
   ("La casa queda a nivel, sin mover tierra.",
    ["La casa queda a nivel,", "sin mover tierra."], 0.0)]),
 (17.8, 25.0, 0.60, [
   ("¿Y cuando llueve fuerte?",
    ["¿Y cuando llueve fuerte?"], 0.45),
   ("El agua sigue de largo, sin empozarse.",
    ["El agua sigue de largo,", "sin empozarse."], 0.45),
   ("Tampoco sube humedad del suelo.",
    ["Tampoco sube humedad", "del suelo."], 0.0)]),
 (24.6, 31.8, 0.60, [
   ("Entre el suelo y el piso circula aire.",
    ["Entre el suelo y el piso", "circula aire."], 0.50),
   ("Eso mantiene la casa seca.",
    ["Eso mantiene la casa seca."], 0.45),
   ("Por eso el piso no se siente frío.",
    ["Por eso el piso", "no se siente frío."], 0.0)]),
 (31.4, 38.0, 0.60, [
   ("¿Termitas? No les interesa el pe ve ce.",
    ["¿Termitas?", "No les interesa el PVC."], 0.45),
   ("Se instala y listo.",
    ["Se instala y listo."], 0.0)]),
 (37.6, 43.0, 0.60, [
   ("¿Vas a construir? Hablemos primero del terreno.",
    ["¿Vas a construir?", "Hablemos primero del terreno."], 0.0)]),
]

if '--voice' in sys.argv:
    import asyncio, edge_tts
    PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    tmp = HERE / '_vo'; tmp.mkdir(exist_ok=True)

    async def una(text, f):
        # el servicio falla de vez en cuando: se reintenta con espera creciente
        for intento in range(5):
            try:
                await edge_tts.Communicate(text, VOZ, rate=RATE, proxy=PROXY).save(str(f))
                if f.exists() and f.stat().st_size > 1000:
                    return
            except Exception as e:
                if intento == 4: raise
            await asyncio.sleep(1.5 * (intento + 1))
        raise RuntimeError(f'sin audio para: {text}')

    async def grab():
        out = []
        for si, (s0, s1, lead, lines) in enumerate(VO_SCENES):
            for li, (text, sub, gap) in enumerate(lines):
                import hashlib
                h = hashlib.sha1(f'{VOZ}|{RATE}|{text}'.encode()).hexdigest()[:12]
                f = tmp / f'{h}.mp3'
                if not (f.exists() and f.stat().st_size > 1000):
                    await una(text, f)
                    await asyncio.sleep(0.4)
                out.append((si, li, f, text, sub, gap, s0, s1, lead))
        return out
    takes = asyncio.run(grab())

    def load(mp3):
        wv = mp3.with_suffix('.conv.wav')
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(mp3),
                        '-ar',str(SR),'-ac','1',str(wv)], check=True)
        with wave.open(str(wv)) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64)/32768
        wv.unlink()
        a = band(a, 85, 13000)
        # edge-tts entrega silencio de relleno en los bordes: se recorta, si no
        # aparecen huecos que no están en el guion
        e = np.convolve(np.abs(a), np.ones(int(.02*SR))/int(.02*SR), mode='same')
        viva = np.where(e > 10 ** (-46/20))[0]
        if len(viva):
            i0 = max(0, viva[0] - int(.05*SR)); i1 = min(len(a), viva[-1] + int(.07*SR))
            a = a[i0:i1]
        f = int(0.012*SR); a[:f] *= np.linspace(0,1,f); a[-f:] *= np.linspace(1,0,f)
        return a

    # Se reparte el tiempo que sobra en la escena entre sus pausas, en vez de
    # dejarlo todo al final. Así las pausas quedan donde dicen algo (después
    # de una pregunta) y no se abre un hueco antes del corte.
    TAIL = 0.35
    por_escena = {}
    for tk in takes: por_escena.setdefault(tk[0], []).append(tk)

    voz = np.zeros(N); spans = []
    for si in sorted(por_escena):
        grupo = por_escena[si]
        audios = [load(f) for _si, _li, f, *_ in grupo]
        _, _, _, _, _, _, s0, s1, lead = grupo[0]
        base = [g for *_r, g, _a, _b, _c in
                [(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]) for x in grupo]]
        base = [x[5] for x in grupo]
        dur = [len(a)/SR for a in audios]
        avail = (s1 - TAIL) - (s0 + lead)
        sobra = avail - sum(dur) - sum(base[:-1])
        n = len(grupo)
        extra = min(max(sobra, 0) / (n - 1), 0.65) if n > 1 else 0.0
        resto = max(sobra, 0) - extra * (n - 1)
        t = s0 + lead + min(resto * 0.5, 0.5)
        for k, (tk, a) in enumerate(zip(grupo, audios)):
            at(voz, t, a, 1.0)
            spans.append((t, t + dur[k], s1, tk[3], tk[4]))
            print(f'  {t:6.2f} → {t+dur[k]:6.2f}s   {tk[3]}')
            t += dur[k] + (base[k] + extra if k < n - 1 else 0.0)

    bad = False
    for j, (a0, a1, send, tx, _s) in enumerate(spans):
        if a1 > send - 0.10:
            print(f'  ! se pasa de la escena por {a1-(send-0.10):.2f}s: {tx}'); bad = True
        if j+1 < len(spans):
            hueco = spans[j+1][0] - a1
            misma = spans[j+1][1] <= send + 0.01     # ¿siguen en la misma escena?
            if hueco < 0:
                print(f'  ! se pisa con la siguiente: {tx}'); bad = True
            elif misma and hueco > 1.25:
                print(f'  ! silencio largo ({hueco:.2f}s) dentro de escena tras: {tx}'); bad = True
    dentro = [spans[j+1][0]-spans[j][1] for j in range(len(spans)-1)
              if spans[j+1][1] <= spans[j][2] + 0.01]
    corte  = [spans[j+1][0]-spans[j][1] for j in range(len(spans)-1)
              if spans[j+1][1] > spans[j][2] + 0.01]
    print(f'  pausas dentro de escena: {min(dentro):.2f}–{max(dentro):.2f}s')
    print(f'  pausas en los cortes:    {min(corte):.2f}–{max(corte):.2f}s')
    print('  locuciones: ' + ('REVISAR' if bad else 'sin choques, desbordes ni silencios largos'))

    p = np.max(np.abs(voz))
    if p > 0: voz = voz / p * 0.85
    write_wav(HERE / 'voz.wav', np.stack([voz, voz], axis=1))
    duck = 1.0 - 0.55 * np.clip(np.convolve(np.abs(voz),
            np.ones(int(.12 * SR)) / (.12 * SR), mode='same') * 6, 0, 1)
    m2 = np.stack([L * duck + voz * .95, R * duck + voz * .95], axis=1)
    p = np.max(np.abs(m2))
    if p > 0: m2 = m2 / p * 0.9
    write_wav(HERE / 'mezcla-voz.wav', m2)

    rows = ',\n  '.join(
        '{a:%.2f,b:%.2f,l:[%s]}' % (a0, a1, ','.join(repr(x) for x in sub))
        for a0, a1, _s, _t, sub in spans)
    html = HERE / 'pilotes-reel.html'
    src = html.read_text(encoding='utf-8')
    k0 = src.index('/* SUBS:INICIO */'); k1 = src.index('/* SUBS:FIN */')
    html.write_text(src[:k0] + '/* SUBS:INICIO */\nlet SUBS=[\n  ' + rows + '\n];\n' + src[k1:],
                    encoding='utf-8')
    print('  subtitulos escritos en pilotes-reel.html')
