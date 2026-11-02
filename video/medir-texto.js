const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1080,height:1920}, deviceScaleFactor:1 });
  await p.goto('file://' + path.join('/home/user/post/video', process.argv[2]), {waitUntil:'load'});
  await p.evaluate(async () => {
    const want = ['300 120px "Fraunces Display"','400 48px "Work Sans N"','500 48px "Work Sans N"',
                  '400 34px "Plex Mono N"','500 34px "Plex Mono N"'];
    await Promise.all(want.map(f => document.fonts.load(f, 'Agj0')));
    await document.fonts.ready;
  });
  const rows = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.scene').forEach(sc => {
      sc.style.display='block';
      sc.querySelectorAll('.title,.support,.eyebrow').forEach(n => {
        const r = document.createRange(); r.selectNodeContents(n);
        const rects = [...r.getClientRects()];
        const w = Math.round(Math.max(...rects.map(x=>x.right)) - Math.min(...rects.map(x=>x.left)));
        // cajas de línea distintas = líneas reales
        const tops = new Set(rects.map(x=>Math.round(x.top)));
        out.push({sc:sc.id, cls:n.className.replace(/\brv\b/,'').trim(),
                  txt:n.textContent.trim(), w, lines:tops.size,
                  bottom:Math.round(n.getBoundingClientRect().bottom)});
      });
      sc.style.display='none';
    });
    return out;
  });
  for (const r of rows) {
    const bad = r.w > 870 || r.lines > 1;
    console.log(`${bad?'!!':'  '} ${r.sc} ${r.cls.padEnd(11)} ancho=${String(r.w).padStart(4)}/870 lineas=${r.lines} fondo=${r.bottom}  "${r.txt}"`);
  }
  await b.close();
})();
