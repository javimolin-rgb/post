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

El guion **no repite** los textos en pantalla: los complementa y usa preguntas
para enganchar. La tipografía dice qué es; la voz dice por qué importa. Por eso
el video lleva subtítulos quemados propios (§9).

| Entra | Voz en off |
|---|---|
| 0:00.6 | ¿Sabes sobre qué se apoya tu casa? |
| 0:03.3 | Casi nunca se ve. |
| 0:05.1 | El tubo queda protegiendo el hormigón. |
| 0:08.0 | ¿Por qué no madera? Bajo tierra no dura. |
| 0:11.6 | ¿Y si el terreno está en pendiente? |
| 0:13.7 | Cada pilote baja lo que necesita. |
| 0:15.7 | La casa queda a nivel, sin mover tierra. |
| 0:18.4 | ¿Y cuando llueve fuerte? |
| 0:20.2 | El agua sigue de largo, sin empozarse. |
| 0:23.0 | Tampoco sube humedad del suelo. |
| 0:25.2 | Entre el suelo y el piso circula aire. |
| 0:27.8 | Eso mantiene la casa seca. |
| 0:29.7 | Por eso el piso no se siente frío. |
| 0:32.2 | ¿Termitas? No les interesa el PVC. |
| 0:36.4 | Se instala y listo. |
| 0:38.7 | ¿Vas a construir? Hablemos primero del terreno. |

Las pausas no son relleno: **0,40–1,15 s dentro de cada escena** (el respiro
después de una pregunta) y **0,47–1,24 s en los cortes**, donde cae la
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
