# Animación — "La casa empieza bajo tierra"

Pieza generada por código: una página HTML con línea de tiempo determinista,
capturada fotograma a fotograma con Chromium y codificada con ffmpeg.
Sigue `../docs/MANUAL_MARCA_VIDEO.md`.

## Archivos

| Archivo | Descripción |
|---|---|
| `pilotes-reel.html` | La animación. `window.renderFrame(t)` dibuja el estado exacto del segundo `t`. |
| `render.js` | Captura de fotogramas con Playwright. |
| `fonts/` | Fraunces Display (instancia estática), Work Sans 400/500, IBM Plex Mono 400/500. |
| `brand/logo-04.png` | Lockup blanco, transparencia real — para fondo oscuro o video. |
| `brand/logo-05.png` | Lockup Azul Origen — para fondo claro. |
| `../out/neorigen-pilotes-reel-1080x1920.mp4` | 9:16, 30 fps, 43 s — Reel / historia. |
| `../out/neorigen-pilotes-feed-1080x1350.mp4` | 4:5 — post de feed. |
| `../out/portada-1080x1920.png` | Frame de portada. |

## Guion (7 escenas, 43 s)

| Desde | Escena | Titular |
|---|---|---|
| 0,0 s | Gancho | La casa empieza bajo tierra. |
| 4,2 s | 01 · El pilote | Un tubo de PVC lleno de hormigón. |
| 11,0 s | 02 · El terreno | Se adapta a la pendiente. |
| 17,8 s | 03 · Las lluvias | El agua pasa por debajo. |
| 24,6 s | 04 · La temperatura | Una cámara de aire ventilada. |
| 31,4 s | 05 · El tiempo | No se pudre. No se oxida. |
| 37,6 s | Cierre | Lockup + "Cotiza en neorigen.cl" |

## Re-generar

```bash
cd video
node render.js --fps 30 --out frames

ffmpeg -y -framerate 30 -i frames/f%05d.jpg \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 -shortest \
  -c:v libx264 -profile:v high -level 4.0 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
  ../out/neorigen-pilotes-reel-1080x1920.mp4

ffmpeg -y -framerate 30 -i frames/f%05d.jpg \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
  -vf "crop=1080:1350:0:198" -shortest \
  -c:v libx264 -profile:v high -level 4.0 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
  ../out/neorigen-pilotes-feed-1080x1350.mp4
```

Fotogramas sueltos para revisar sin renderizar todo:

```bash
node render.js --probe 3.2,14.5,21.5 --out /tmp/probes
```

## Re-generar las tipografías

Fraunces va **instanciada estática** (manual §3): nada de ejes variables en vivo.

```bash
pip install fonttools brotli
python3 - <<'PY'
from fontTools.varLib import instancer
from fontTools import ttLib
import urllib.request
B='https://raw.githubusercontent.com/google/fonts/main'
urllib.request.urlretrieve(B+'/ofl/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf','/tmp/F.ttf')
f=ttLib.TTFont('/tmp/F.ttf')
inst=instancer.instantiateVariableFont(f,{'opsz':144,'wght':300,'SOFT':20,'WONK':1},
                                       inplace=False,updateFontNames=False)
inst.save('fonts/FrauncesDisplay.ttf')
PY
```

## Personalizar

- **Textos y tiempos:** cada escena es un `<div class="scene">` en el HTML.
  Los elementos con clase `rv` entran con fade + subida; `data-d` es el
  retardo en segundos dentro de la escena. El array `SCENES` define
  `start` y `dur`.
- **Color:** bloque `:root` y el objeto `C` en el script. Son los valores
  exactos del manual.
- **Zonas seguras:** la columna de texto es `.col` (left 80, width 870, es
  decir hasta x=950). No sacar texto ni logo de ahí.

## Audio

`audio.py` sintetiza toda la banda sonora con numpy — ruido filtrado en el
dominio de la frecuencia y osciladores. No usa ninguna biblioteca de samples,
así que es material propio y libre de derechos (§9 del manual).

```bash
python3 audio.py            # sfx.wav — ambiente y efectos
python3 audio.py --voice    # ademas voz.wav y mezcla-voz.wav (maqueta)
```

Las capas siguen a la animación: el peso de la tierra, el aire, la lluvia que
entra en la escena 02 y crece en la 03, el agua que escurre, el golpe de cada
pilote al colocarse, el vaciado del hormigón, los tres descartes de la escena
05 y un soplo suave en cada transición de cámara.

### Música

El lecho musical también se sintetiza en `audio.py`: piano de fieltro
(parciales que decaen + golpe de martillo) sobre un pad cálido. La progresión
es Am – F – C – Dm – F – Am – C y **cada acorde cambia en el corte de escena**,
por eso la música sigue el montaje. Son unas 20 notas en 43 s: calmo por
construcción, como pide §9.

- `MUS_LEVEL` controla cuánto entra en la mezcla (por defecto 0.115, que deja
  la música ~8 dB bajo el conjunto).
- `musica.wav` se escribe aparte, por si se quiere rebalancear o reemplazar.

Alternativas verificadas si se prefiere una pista grabada:

| Fuente | Licencia | Atribución |
|---|---|---|
| [Musopen — Complete Chopin Collection](https://archive.org/details/musopen-chopin) | CC0 | No |
| FreePD | Dominio público | No |
| Incompetech (Kevin MacLeod) | CC BY 4.0 | **Sí**, en el caption |

### Voz

La voz es una **maqueta** (TTS, masculina es-MX). Necesita el modelo, que no
está en el repo por peso:

```bash
mkdir -p voice && cd voice
B=https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/ald/medium
curl -sSfLO $B/es_MX-ald-medium.onnx
curl -sSfLO $B/es_MX-ald-medium.onnx.json
pip install piper-tts
```

`audio.py --voice` hace tres cosas además de sintetizar: verifica que ninguna
locución se pise con la siguiente ni se salga de su escena, y **escribe los
subtítulos con sus tiempos reales dentro de `pilotes-reel.html`** (bloque
`SUBS:INICIO` / `SUBS:FIN`). Por eso el orden es: `audio.py --voice` primero,
`render.js` después. Si se cambia una locución, hay que volver a renderizar.

`node render.js --nosubs` genera los fotogramas sin la capa de subtítulos.

**El acento no se puede arreglar acá:** piper no tiene voz chilena. Las únicas
opciones en español son es-MX (la que usamos), es-AR y es-ES; cualquiera va a
sonar extranjera en Chile. Para la locución definitiva conviene un servicio:

| Servicio | Por qué |
|---|---|
| **Azure Speech** | Es el único con voces **nativas de Chile**: `es-CL-LorenzoNeural` (hombre) y `es-CL-CatalinaNeural` (mujer). Confirmar los identificadores en la documentación de Azure antes de integrarlo. |
| **ElevenLabs** | La más citada por naturalidad en español y permite clonar una voz propia, que sería lo ideal para la marca. Su español neutro tiende a sonar peninsular, así que hay que elegir bien la voz. |
| **Google Cloud TTS / Amazon Polly** | Alternativas con voces latinas, sin opción chilena nativa. |

Lo más fiel a la marca sería clonar la voz de alguien del equipo y usarla
siempre: queda chilena de verdad y no depende del catálogo de nadie.

### Muestras para elegir locutor

```bash
python3 muestras.py     # -> muestras/
```

Genera un MP3 por voz (cada una se presenta sola, así se sabe cuál es cuál),
uno con las seis seguidas para comparar, y `prueba-pronunciacion.mp3`.

### Pronunciación

El TTS lee mal las siglas y los dominios. Por eso en `audio.py` cada línea
tiene **el texto hablado separado del subtítulo**: se escribe fonético para
que suene bien y en pantalla se lee como corresponde.

| Se escribe para la voz | Aparece en pantalla |
|---|---|
| `pe ve ce` | PVC |
| `neorigen punto ce ele` | neorigen.cl |

Al cambiar de voz hay que volver a correr `audio.py --voice` y después
`render.js`: los tiempos de los subtítulos salen de la duración real de cada
locución.

## Cámara

`CAM` (en el script del HTML) encadena las escenas: cada una entra con el
encuadre donde terminó la anterior y sale empujando o retrocediendo hacia la
siguiente, de modo que el corte se lee como un movimiento continuo. Del tubo
se sale hacia el terreno, de la casa se entra bajo el piso, y de ahí a un
pilote. La cámara sólo mueve la ilustración: el texto se queda quieto.

Por eso el terreno se dibuja de `x=-700` a `x=1780` y hasta `y=1800`: al
alejarse la cámara, el borde del suelo no puede entrar en cuadro.

## Sistema de ilustración

Las piezas no son trazo plano: tienen volumen, dentro de la paleta del manual.

- **Pilote** (`pile()`): cilindro con degradado `#pvc` (borde oscuro → brillo →
  caída), collar superior y, con `{cut:[y1,y2]}`, ventana de corte que muestra
  el hormigón (`#core`), los áridos y la armadura en Madera.
- **Casa** (`house()`): volumen con `#wall` y `#roof`, entablado horizontal en
  Madera y vanos en Madera con contorno Niebla.
- **Terreno**: `groundBase()` dibuja el suelo vegetal, el estrato firme y los
  áridos; `groundFade()` va **después** de los pilotes y es lo que entierra de
  verdad lo que está bajo la línea de tierra (cara frontal de suelo + velo de
  profundidad). Su parámetro `cover` gradúa cuánto se transparenta: bajo en las
  escenas que son un corte (01, 02, 05), alto en las que no (gancho, 03, 04).

Los degradados y tramas viven en un `<svg id="gdefs">` **fuera de las escenas**:
un paint server dentro de un subárbol `display:none` no se resuelve en Chromium
y los rellenos salen vacíos.

## Notas

- Las animaciones son funciones puras del tiempo (sin CSS animations ni
  `requestAnimationFrame`): cada render produce exactamente los mismos
  fotogramas.
- El easing es el del manual: `cubic-bezier(0.22, 1, 0.36, 1)` para entradas
  y `cubic-bezier(0.65, 0, 0.35, 1)` para transiciones, resueltos por Newton
  en el script.
- Sin música: ver `../CAPTION.md`.
