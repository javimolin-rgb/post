# Copy del post — "La casa empieza bajo tierra"

## Caption

La casa empieza mucho antes de que se vea.

Antes de la primera tabla hay una decisión que no se nota en ninguna foto:
sobre qué se apoya la casa. Nosotros fundamos sobre pilotes de PVC rellenos
de hormigón armado, y esto es lo que cambia.

El terreno deja de ser un problema. Los pilotes bajan hasta el suelo firme y
se adaptan a la pendiente, al relleno y a los suelos irregulares. No hay que
mover el cerro para construir sobre él.

El agua pasa por debajo. La casa queda elevada, así que la lluvia escurre en
vez de acumularse contra la estructura, y se corta la humedad que sube desde
el suelo.

Queda una cámara de aire ventilada bajo el piso. Eso separa la vivienda del
frío y la humedad del terreno: piso más cálido en invierno, menos
condensación y menos hongos.

Y el material acompaña. El PVC no se pudre, no se oxida y no es alimento de
termitas; funciona como encofrado permanente y deja el hormigón confinado y
protegido. Durabilidad sin mantención.

Construir bien empieza por el suelo.
Cotiza en neorigen.cl

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

## Guion de voz en off

Voz: **es-CL-CatalinaNeural** (mujer, español de Chile), a +12 % de velocidad.
Duración total: 44 s.

El guion **no repite** los textos en pantalla: los complementa. Frases
desarrolladas, no punteo, y el gancho abierto con una idea que se resuelve
recién en la segunda línea. La tipografía dice qué es; la voz dice por qué
importa. Por eso el video lleva subtítulos quemados propios (§9).

| Entra | Voz en off |
|---|---|
| 0:00.7 | Antes de la primera tabla, hay una decisión que no se ve… |
| 0:04.6 | …sobre qué se va a parar tu casa. |
| 0:06.8 | El tubo no se saca: queda ahí, protegiendo el hormigón. |
| 0:10.5 | ¿Por qué no madera? Bajo tierra no dura. |
| 0:13.9 | ¿Y si el terreno tiene pendiente? |
| 0:16.6 | Cada pilote baja hasta el suelo firme, y la casa queda a nivel. |
| 0:20.4 | ¿Y cuando llueve de verdad? |
| 0:22.6 | El agua pasa por debajo, sigue de largo, y no se empoza contra nada. |
| 0:27.0 | Entre el suelo y el piso circula aire. |
| 0:30.1 | Por eso se mantiene seca, y el piso no se siente frío. |
| 0:33.6 | ¿Termitas? Al PVC no le interesan. |
| 0:37.3 | Se instala una vez, y listo. |
| 0:40.1 | ¿Vas a construir? ¡Conversemos! *(sin subtítulo)* |

El cierre va **sin subtítulo**: ahí manda el lockup y el CTA en pantalla,
y una placa de texto encima sólo competiría. En `audio.py`, una línea con la
lista de subtítulo vacía (`[]`) se locuta pero no se dibuja.

**El fraseo está escrito en la puntuación.** Los puntos suspensivos sostienen
el gancho, los dos puntos arman el remate, las comas marcan dónde respira y
los signos de interrogación suben la entonación. Si se cambia una coma,
cambia la locución: es el único control de prosodia que tiene el texto plano.

Las pausas no son relleno: **0,55–1,10 s dentro de cada escena** (el respiro
después de una pregunta) y **0,55–0,85 s en los cortes**, donde cae la
transición de cámara. Los tiempos los calcula `audio.py` con la duración real
de cada locución, y avisa si se abre un hueco o algo se pisa.

## Notas de publicación

- **Audio:** el video trae **diseño sonoro propio** (lluvia, agua que escurre,
  la colocación de los pilotes, el vaciado del hormigón y el aire de la cámara
  ventilada). Está todo sintetizado desde cero en `video/audio.py`, así que es
  material propio y libre de derechos, como pide §9.
- **Música:** lleva un lecho instrumental propio (piano de fieltro y pad
  cálido) sintetizado en `video/audio.py`, así que es material nuestro, sin
  licencia que respetar ni atribución que poner. Los acordes cambian
  exactamente en cada corte de escena. Va ~8 dB por debajo del resto de la
  mezcla: acompaña, no compite.
- Si se prefiere una pista grabada, dos fuentes verificadas: la **colección
  Chopin de Musopen** en archive.org está en **CC0** (sin atribución), y
  **FreePD** es dominio público. **Incompetech** también sirve pero es CC BY:
  obliga a acreditar al autor en el caption. El balance se ajusta sin
  rehacer nada cambiando `MUS_LEVEL` en `audio.py`, o montando la pista
  nueva sobre `video/musica.wav`.
- **La voz es una maqueta.** `...-MAQUETA-VOZ.mp4` usa la voz chilena de
  Microsoft generada con `edge-tts`, que va contra el servicio de lectura en
  voz alta de Edge y **no está licenciado para publicar**. Sirve para aprobar
  guion, ritmo y tiempos. Para publicar hay que regenerarla con una clave
  propia de **Azure Speech** (capa gratuita):
  `python3 voz-azure.py` — usa la misma voz y el mismo guion, y deja todo en
  su lugar. Después: `audio.py --voice`, `render.js` y volver a encodear.
- **Subtítulos con placa propia**, en Azul Origen (el negro de la marca según
  §2), para que se lean como subtítulos y no como texto superpuesto.
- **"PVC" se escribe `pe ve ce`** en el texto hablado para que la V se lea
  "ve" y no "uve". En pantalla el subtítulo sigue diciendo PVC.
- **El archivo sin voz ya trae los subtítulos**, así que queda listo para
  montarle la locución grabada sin tocar la imagen. Si se decide no usar voz,
  se regenera sin subtítulos con `node render.js --nosubs`.
- **Niveles:** la versión con voz queda en −14 LUFS y −1,4 dBTP, como pide §9.
  La versión sin voz queda en −21,9 LUFS a propósito: es ambiente, y a −14
  la lluvia quedaría al frente de la pieza.
- **Formatos:** `neorigen-pilotes-reel-1080x1920.mp4` para Reel o historia;
  `neorigen-pilotes-feed-1080x1350.mp4` si va como post de feed.
- **Portada:** `portada-1080x1920.png`.
- **Datos:** no se incluyó ninguna cifra de empresa. Si se quiere reforzar el
  mensaje con números (vida útil en años, profundidad habitual de los
  pilotes, plazo de instalación), hay que tomarlos de las fichas técnicas
  oficiales: `[DATO A CONFIRMAR]`.
