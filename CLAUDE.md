# Repositorio de piezas audiovisuales — Neorigen

**Antes de producir o modificar cualquier video, reel o historia, leer
`docs/MANUAL_MARCA_VIDEO.md` completo.** Todo lo que dice ahí es obligatorio
salvo que esté marcado como "recomendado".

Resumen operativo (el manual manda sobre este resumen):

- **Paleta:** Azul Origen `#011E2F`, Niebla `#F1F4F3`, Verde Pino `#3C4A3E`,
  Madera `#A9764A`, Amarillo `#FFEDA0` (solo acento). Los grises salen de la
  escala de tinta del azul, nunca grises neutros ni negro puro.
  Madera nunca como color de texto chico sobre azul o verde.
- **Tipografías:** Fraunces (titulares), Work Sans (apoyo), IBM Plex Mono
  (rótulos y datos). Embebidas en `video/fonts/`, no del sistema.
  Fraunces va instanciada estática (`FrauncesDisplay.ttf`), sin
  `font-variation-settings`.
- **Logo:** `video/brand/logo-04.png` (lockup blanco, fondo oscuro) y
  `video/brand/logo-05.png` (lockup Azul Origen, fondo claro). No recrearlo,
  no recolorearlo, no separar isotipo y wordmark, no escribir "Neorigen" con
  una fuente para reemplazarlo.
- **Zonas seguras 9:16:** 250 px arriba, 420 px abajo, 130 px a la derecha.
- **Mínimos de texto:** nada bajo 32 px; cada texto visible ≥ 2 s.
- **Movimiento:** pausado. Easing `cubic-bezier(0.22, 1, 0.36, 1)`. Sin glitch,
  shake, rebotes ni partículas.
- **Datos de empresa:** nunca inventarlos. Si no hay fuente, dejar
  `[DATO A CONFIRMAR]` y preguntar.

Flujo de trabajo: todo cambio va directo a `main`.
