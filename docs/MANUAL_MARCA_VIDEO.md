# Manual de marca para video — Neorigen

> Instrucciones para Claude Code. Léelo completo antes de producir cualquier video, reel o historia de Neorigen. Todo lo que está acá es obligatorio salvo que diga "recomendado".

**Neorigen** es una constructora chilena de casas prediseñadas sustentables (neorigen.cl · @neorigen_chile). La marca habla de madera, bosque del sur de Chile, oficio y hogar. El tono visual es **sobrio, cálido y natural**: nada estridente, nada "tech", nada de efectos llamativos.

---

## 1. Reglas de oro

1. **Nunca inventar datos de la empresa.** Precios, m², distribución, plazos, promociones o servicios se toman de https://neorigen.cl o de las fichas técnicas oficiales. Si no hay fuente, se deja un marcador `[DATO A CONFIRMAR]` y se pregunta. No redondear cifras.
2. **Sin prueba social fabricada.** No inventar testimonios, citas de clientes, cifras de ventas ni "+100 familias felices".
3. **Contraste legible siempre**, también para personas con baja visión (mínimo WCAG AA 4,5:1 para texto normal; apuntar a 7:1 en texto sobre video).
4. **Texto grande.** En Neorigen sienten que las piezas se ven chicas. Si dudas entre dos tamaños, usa el mayor.
5. **Español neutro** en todo texto en pantalla y caption. Nada de voseo ("tenés", "mirá").
6. Promoción del Kit Starlink: **vencida** (1 mar – 30 abr 2026). No usarla como oferta activa.

---

## 2. Color

### Paleta

| Nombre | Rol | HEX | RGB |
| --- | --- | --- | --- |
| **Azul Origen** | Color oficial, fondos, texto oscuro | `#011E2F` | 1, 30, 47 |
| **Niebla** | Claro principal (Azul Origen al 6 %) | `#F1F4F3` | 241, 244, 243 |
| **Verde Pino** | Complementario, interiores, naturaleza | `#3C4A3E` | 60, 74, 62 |
| **Madera** | Acento cálido, detalles, líneas | `#A9764A` | 169, 118, 74 |
| **Amarillo** | Solo acento en RRSS (badges, subrayados). Nunca fondo, nunca color de marca | `#FFEDA0` | 255, 237, 160 |

Proporción recomendada en un video: ~60 % Azul Origen o imagen, ~25 % Niebla, ~10 % Verde Pino, ≤5 % Madera/Amarillo.

### Escala de tinta del Azul Origen

Los claros de la marca **son tintas del azul**, no colores nuevos. Para grises, overlays y fondos suaves usa esta escala (Azul Origen sobre blanco):

| Tinta | HEX |
| --- | --- |
| 100 % | `#011E2F` |
| 85 % | `#27404E` |
| 70 % | `#4D626D` |
| 50 % | `#808E97` |
| 30 % | `#B3BCC1` |
| 25 % | `#C0C7CB` |
| 20 % | `#CCD2D5` |
| 15 % | `#D9DDE0` |
| 6 % | `#F0F2F3` (≈ Niebla) |

No uses grises neutros (`#888`, `#ccc`, negro puro `#000`). Para "negro" usa Azul Origen.

### Combinaciones de texto aprobadas

| Texto | Fondo | Uso |
| --- | --- | --- |
| Niebla `#F1F4F3` | Azul Origen `#011E2F` | La principal |
| Azul Origen | Niebla | Placas claras |
| Niebla | Verde Pino `#3C4A3E` | Secciones de interior/naturaleza |
| Azul Origen | Amarillo `#FFEDA0` | Badges cortos |
| Niebla | Video + scrim (ver §6) | Texto sobre imagen |

Prohibido: Madera como color de texto pequeño sobre azul o verde (contraste insuficiente), Amarillo sobre Niebla, blanco sobre tintas claras.

---

## 3. Tipografía

| Familia | Uso | Pesos |
| --- | --- | --- |
| **Fraunces** | Titulares, frases protagonistas | Light 300, opsz 144, SOFT 20, WONK 1 |
| **Work Sans** | Texto de apoyo, subtítulos, párrafos | 400 / 500 |
| **IBM Plex Mono** | Datos y rótulos: m², nombre de modelo, número de paso, etiquetas | 400 / 500, en MAYÚSCULAS con tracking +8 % |

- Las tres son SIL OFL. Descargarlas del repo oficial de Google Fonts (`github.com/google/fonts`) y **embeberlas localmente**; no depender de fuentes del sistema.
- Si el render pasa por Chromium/Puppeteer/Playwright: usar Fraunces **instanciada estática** con esos ejes (`fontTools.varLib.instancer` → `FrauncesDisplay.ttf`). No usar `font-variation-settings` en vivo.
- Cursiva de Fraunces: `transform: skewX(-11deg)`, nunca `font-style: italic` sintético.
- No usar negritas que la fuente no tenga (síntesis de bold).
- **El wordmark "Neorigen" es lettering a medida.** Nunca escribir "Neorigen" con una fuente para reemplazar el logo.

### Tamaños mínimos (lienzo 1080 × 1920)

| Elemento | Tamaño |
| --- | --- |
| Titular (Fraunces) | 96–140 px, interlineado 1.1–1.22 |
| Subtítulo / apoyo (Work Sans) | 44–56 px |
| Subtítulos de voz (Work Sans 500) | 48 px mínimo |
| Rótulo / dato (IBM Plex Mono) | 32–40 px |
| Nada por debajo de | **32 px** |

Máximo ~8 palabras por placa de texto. Máximo 2 líneas de titular.

---

## 4. Logotipo

Variantes: isologo cuadrado, lockup horizontal, monocromático azul, monocromático blanco. Pídele a Javi los archivos si no están en el repo; no recrearlos.

- Sobre fondo oscuro o video: usar los recortes **con transparencia real** (`logo_icon_white_transparent.png`, `logo04_white.png`). Los PNG con fondo horneado dejan un cuadrado visible.
- El isologo va en **la esquina opuesta al bloque de texto**, nunca en la misma ni superpuesto.
- Tamaño: isologo en esquina ~120–160 px de ancho; en el cierre, lockup centrado ~50–60 % del ancho.

**No hacer:** recolorear el isotipo, estirarlo, ponerle sombra o glow, separar isotipo y wordmark, animarlo deformándolo (rebotes, squash & stretch, giros 3D), usar el logo blanco sobre fondo claro.

Animación permitida del logo: fade + leve desplazamiento vertical (≤20 px), o revelado con máscara horizontal. Duración 0,6–1 s.

---

## 5. Formatos y zonas seguras

| Formato | Tamaño | FPS | Duración recomendada |
| --- | --- | --- | --- |
| Reel / historia | 1080 × 1920 (9:16) | 30 | Reel 15–45 s · historia ≤15 s por clip |
| Feed vertical | 1080 × 1350 (4:5) | 30 | 15–30 s |
| Cuadrado (si se pide) | 1080 × 1080 | 30 | — |

**Zonas seguras 9:16** (Instagram tapa con su interfaz):
- Superior: 250 px libres.
- Inferior: 420 px libres (caption, botones).
- Derecha: 130 px libres (íconos de like/compartir).
- Texto y logo siempre dentro de ese recuadro.

**Exportación:** MP4, H.264, `yuv420p`, 30 fps, perfil High, audio AAC 48 kHz 192 kbps, `-movflags +faststart`. Calidad CRF 18–20 con `-preset veryfast` salvo que se pida máxima calidad.

---

## 6. Imagen y texto sobre video

- Material fuente: fotos, renders y fichas en el Drive oficial: https://drive.google.com/drive/folders/1bFHxl3ufFlmR0LkJDLgBzWYlzJzzk7do (si no hay acceso, pedírselas a Javi; no usar fotos de stock genéricas de casas).
- Cuando el fondo compromete el contraste, usar **scrim**: degradado de Azul Origen de 0 % a 70–85 % de opacidad detrás del texto, nunca una caja negra.
- Tratamiento de color recomendado: tonos naturales, ligeramente cálidos en la madera, sombras hacia el azul. Sin filtros saturados, sin LUTs "cinemáticos" teal & orange exagerados.
- Atenuar el aspecto de render 3D cuando se pueda (leve grano 2–3 %, viñeta muy suave), sin falsear la arquitectura.
- Nunca deformar proporciones de una casa (no estirar para llenar el cuadro: recortar).

---

## 7. Movimiento

El ritmo de Neorigen es **pausado y con oficio**, como la construcción en madera. El movimiento acompaña; no compite con la casa.

**Sí:**
- Curvas de easing suaves: `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out) para entradas; `cubic-bezier(0.65, 0, 0.35, 1)` para transiciones.
- Entradas de texto: fade + subida de 20–40 px, o revelado por línea/palabra con máscara. 0,5–0,8 s.
- Movimientos de cámara lentos sobre fotos (Ken Burns ≤ 8 % de zoom en todo el plano).
- Transiciones: corte limpio, fundido cruzado (0,3–0,5 s) o barrido con una placa de color de marca.
- Líneas finas en Madera o Niebla (2–4 px) que se dibujan, como trazo de plano.
- Cada texto en pantalla queda visible al menos **2 s** (o 0,3 s por palabra, lo que sea mayor).

**No:**
- Glitch, zoom punch, shake, flashes, rebotes elásticos, giros 3D, partículas, brillos, texto tipo máquina de escribir rápida, emojis animados.
- Más de dos animaciones distintas compitiendo en el mismo momento.
- Cambiar de plano más rápido que cada 1,2 s (salvo un montaje de proceso pedido explícitamente).

---

## 8. Estructura y contenido

Lo que mejor funciona en la cuenta (datos ene–ago 2026): **contenido narrativo de proceso constructivo**, sin colaboraciones. El reel de mayor rendimiento fue de proceso ("Todo gran hogar comienza mucho antes de su entrega"). El contenido tipo "tip educativo" rinde bajo.

Estructura recomendada para reel:
1. **Gancho (0–2 s):** imagen fuerte de la casa o del proceso + frase corta en Fraunces. Nunca abrir con el logo ni con una placa vacía.
2. **Desarrollo:** 3–6 planos con un dato o idea cada uno (rótulos en IBM Plex Mono).
3. **Cierre (2–3 s):** lockup del logo sobre Azul Origen + llamada a la acción sobria ("Cotiza en neorigen.cl" / "Escríbenos por DM").

Público: mayoritariamente 35–54 años, 78 % en Chile, núcleo en Santiago. Hablar claro, cálido, sin jerga de influencer.

Modelos (para nombres; los datos se verifican en neorigen.cl): Lingue, Huingán, Peumo, Boldo, Huingán Familiar, Roble, Maitén, Coihue. Siempre se escribe "Casa Lingue", "Casa Boldo", etc. Para series de modelos, respetar el orden en que aparecen en neorigen.cl.

---

## 9. Audio

- Música instrumental tranquila: acústica, piano, ambient orgánico. Sin EDM ni trap.
- Sonido ambiente real de obra (madera, herramientas) a bajo volumen suma oficio.
- Voz en off: pausada, cercana; siempre con subtítulos quemados (mucha gente ve sin sonido).
- Pico de audio ≤ −1 dBTP, loudness ~ −14 LUFS.
- Solo música con licencia libre o con derechos claros. Si no hay, entregar sin música y avisar.

---

## 10. Entregables por video

1. `.mp4` final según §5.
2. Un **frame de portada** en PNG (1080 × 1920) con imagen, no placa de texto sola.
3. El archivo fuente editable (HTML/composición/script) para poder ajustar textos sin rehacer todo.
4. Caption en español neutro con hashtags (5–10, mezcla de marca + rubro + lugar, p. ej. `#Neorigen #CasasPrediseñadas #CasasDeMadera #ConstrucciónSustentable #Chile`).
5. Si va en ZIP: subcarpeta nombrada con el título del video, no `imagenes/` ni `output/`.

Cada video con layout propio: no repetir la misma plantilla de placa en piezas consecutivas del feed.

---

## 11. Checklist antes de entregar

- [ ] Ningún dato de empresa sin fuente; ninguno redondeado.
- [ ] Solo colores de la paleta y la escala de tinta.
- [ ] Solo Fraunces / Work Sans / IBM Plex Mono, embebidas.
- [ ] Ningún texto bajo 32 px; contraste ≥ 4,5:1 (idealmente 7:1).
- [ ] Texto y logo dentro de las zonas seguras.
- [ ] Logo sin deformar, en esquina opuesta al texto, con transparencia real.
- [ ] Gancho en los primeros 2 s; cierre con logo.
- [ ] Cada texto visible ≥ 2 s.
- [ ] Revisar el MP4 final abriéndolo (extraer 4–5 frames y mirarlos), no solo confiar en que el render terminó sin error.
- [ ] Portada PNG, editable y caption entregados.
