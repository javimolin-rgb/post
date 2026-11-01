# Copy del post — "La casa empieza bajo tierra"

Versión aprobada: **sin voz y sin subtítulos, solo música**. La gráfica se
explica sola.

## Caption

La casa empieza bajo tierra.

Antes de la primera tabla hay una decisión que después ya no se ve: sobre qué
se para la casa.

Fundamos sobre pilotes de PVC rellenos de hormigón armado. Cada uno baja hasta
el suelo firme, así que la casa queda a nivel sin mover tierra. El agua de
lluvia pasa por debajo en vez de empozarse, y entre el suelo y el piso queda
una cámara de aire que mantiene la casa seca.

El PVC no se degrada, no se oxida y a las termitas no les interesa. Se instala
una vez, y listo.

¿Vas a construir? Conversemos.

#Neorigen #ViveLoNatural #CasasPrediseñadas #CasasDeMadera
#ConstrucciónSustentable #Fundaciones #Pilotes #Chile

## Versión corta (historia)

La casa empieza bajo tierra.
Pilotes de PVC rellenos de hormigón: se adaptan a la pendiente, el agua pasa
por debajo y el piso queda más cálido.
neorigen.cl

## Primer comentario sugerido

¿En qué terreno estás pensando construir? Cuéntanos y te decimos cómo se
resuelve la fundación en ese caso.

## Archivos

| Archivo | Para qué |
|---|---|
| `neorigen-pilotes-reel-1080x1920.mp4` | **Opción 1.** Sin los sonidos de cambio de escena ni nota al final. |
| `opcion-sonidos-bajos-1080x1920.mp4` | **Opción 2.** Los mismos sonidos, 10 dB más abajo. A elegir entre esta y la 1. |
| `neorigen-pilotes-feed-1080x1350.mp4` | 4:5 para feed, con el audio de la opción 1. Se rehace con el de la 2 si se elige esa. |
| `alternativa-musica-y-ambiente-1080x1920.mp4` | Por si quieren oír la lluvia, el agua y los pilotes al colocarse. |
| `portada-1080x1920.png` | Portada. |

### Con la música nueva (`musica-v1`)

Sobre el corte que mandó el equipo, con su música:

| Archivo | Qué suena |
|---|---|
| `musica-v1-sin-efectos-1080x1920.mp4` | Solo la música. |
| `musica-v1-con-efectos-1080x1920.mp4` | La música + el diseño sonoro (lluvia, agua, pilotes, vaciado, aire y las transiciones), 12 dB por debajo. |

> **Ojo con los textos.** El video que mandó el equipo es **la versión
> vigente** y trae **los seis bloques de texto reescritos** respecto de
> `video/pilotes-reel.html` (sólo el cierre coincide). Los dos archivos de
> arriba usan ese video tal cual, copiado sin recomprimir, así que conservan
> la copy buena — pero **el HTML del repo todavía tiene la vieja**, así que
> cualquier re-render la haría retroceder. Hay que pasar los textos nuevos al
> HTML antes de volver a tocar la animación.

Las dos opciones tienen **el mismo video** y el **mismo nivel** (−13,6 LUFS):
lo único que cambia es si los sonidos están o no, así que se comparan parejo.
Cuando decidan, el 4:5 se rehace con ese audio en un comando.

## Notas de publicación

- **Música propia.** Piano de fieltro y pad cálido sintetizados en
  `video/audio.py`, con los acordes cambiando en cada corte de escena. Es
  material nuestro: sin licencia que respetar ni atribución que poner. Queda
  a −13,6 LUFS y −3,3 dBTP, dentro de lo que pide §9.
- **Los sonidos de cambio de escena y la nota del final**, que el equipo pidió
  sacar o bajar mucho, van en dos versiones para elegir:

  **Opción 1 — sin ellos.** Los soplos de transición apagados; la nota de
  piano sin el chasquido de martillo que la hacía sonar a "tin", más oscura
  (−16 dB de brillo sobre 1800 Hz) y casi 7 dB más abajo; la primera nota de
  cada escena corrida un segundo después del corte; el cierre sin ninguna
  nota.

  **Opción 2 — con ellos, abajo.** Los mismos sonidos de siempre, sin
  cambiarles el timbre, sólo el volumen: la melodía con su "tin" 10 dB más
  abajo y el soplo de cada cambio de escena 15 dB bajo la música. En el
  cierre, la nota queda 9,5 dB bajo lo que era.

  En las dos, el resto de la música es el mismo y el nivel general no cambió.
- **Sin voz ni subtítulos**, por decisión del equipo. El guion locutado y el
  script para generarlo con Azure siguen en el repo (`video/voz-azure.py` y
  el historial de este archivo) por si se retoma.
- **Datos:** no se incluye ninguna cifra de empresa. Si se quiere reforzar
  con números (vida útil, profundidad de los pilotes, plazo de instalación),
  hay que tomarlos de las fichas técnicas oficiales: `[DATO A CONFIRMAR]`.
