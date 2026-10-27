# Video animado — Pilotes de PVC + hormigón (Neorigen)

Animación 100% generada por código: una página HTML con una línea de tiempo
determinista, capturada fotograma a fotograma con Chromium y codificada con ffmpeg.

## Archivos

| Archivo | Descripción |
|---|---|
| `pilotes-reel.html` | La animación. `window.renderFrame(t)` dibuja el estado exacto en el segundo `t`. |
| `render.js` | Captura los fotogramas con Playwright. |
| `../out/neorigen-pilotes-reel-9x16.mp4` | 1080×1920, 30 fps, 39,5 s — Reels / Stories. |
| `../out/neorigen-pilotes-feed-4x5.mp4` | 1080×1350 — post de feed (recorte central, no pierde contenido). |
| `../out/portada-reel.jpg` | Fotograma de portada. |
| `../CAPTION.md` | Copy, hashtags y notas de publicación. |

## Guion (8 escenas, 39,5 s)

1. **0,0 s — Hook.** "Tu casa no debería tocar el suelo."
2. **3,6 s — El elemento.** Tubo de PVC + hormigón armado (relleno animado).
3. **9,1 s — El terreno.** Pendiente, suelo firme, plataforma nivelada.
4. **14,8 s — Las lluvias.** Comparación: radier anegado vs. agua que escurre bajo los pilotes.
5. **20,5 s — La temperatura.** Cámara de aire ventilada y termómetro.
6. **26,1 s — La durabilidad.** Pudrición / termitas / corrosión / mantención.
7. **30,8 s — La obra.** Barras comparativas pilotes vs. excavación + radier.
8. **34,7 s — Cierre.** Marca, tagline y CTA.

## Re-generar el video

```bash
cd video
npm ls playwright || true          # Chromium ya viene instalado en el entorno
node render.js --fps 30 --out frames

ffmpeg -y -framerate 30 -i frames/f%05d.jpg \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -shortest \
  -c:v libx264 -profile:v high -level 4.0 -preset slow -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart ../out/neorigen-pilotes-reel-9x16.mp4

# versión 4:5 para feed
ffmpeg -y -i ../out/neorigen-pilotes-reel-9x16.mp4 -vf "crop=1080:1350:0:285" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a copy \
  -movflags +faststart ../out/neorigen-pilotes-feed-4x5.mp4
```

Fotogramas sueltos para revisar sin renderizar todo:

```bash
node render.js --probe 2.6,11.5,17.8 --out /tmp/probes
```

## Personalizar

- **Colores de marca:** bloque `:root` al inicio del HTML (`--or` es el naranja
  de acento, `--bg0/--bg1` los fondos, `--tl` el verde de los ✔).
- **Textos:** cada escena es un `<div class="scene">` en el HTML. Los elementos
  con clase `rv` aparecen con fade+subida; `data-d` es el retardo en segundos
  dentro de la escena.
- **Duración / ritmo:** array `SCENES` en el script (`start` y `dur` por escena).
- **Logo:** el wordmark `#brand` es texto. Para usar el logotipo real, reemplaza
  ese bloque por un `<img>` y publica el archivo junto al HTML.

## Notas

- El contenido crítico vive entre `y=300` y `y=1620`, por eso el recorte 4:5 es
  seguro y la UI de Reels no tapa nada.
- Las animaciones son funciones puras del tiempo (sin CSS animations ni
  `requestAnimationFrame`), por eso cada render produce exactamente los mismos
  fotogramas.
- Tipografía: Inter / Inter Display (instaladas en el sistema, sin red).
