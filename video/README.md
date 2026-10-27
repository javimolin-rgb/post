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

## Notas

- Las animaciones son funciones puras del tiempo (sin CSS animations ni
  `requestAnimationFrame`): cada render produce exactamente los mismos
  fotogramas.
- El easing es el del manual: `cubic-bezier(0.22, 1, 0.36, 1)` para entradas
  y `cubic-bezier(0.65, 0, 0.35, 1)` para transiciones, resueltos por Newton
  en el script.
- Sin música: ver `../CAPTION.md`.
