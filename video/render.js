const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const args = process.argv.slice(2);
  const get = (k, d) => { const i = args.indexOf('--' + k); return i < 0 ? d : args[i + 1]; };
  const FPS   = parseFloat(get('fps', 30));
  const OUT   = get('out', path.join(__dirname, 'frames'));
  const PROBE = get('probe', null);          // comma-separated seconds -> png probes
  // --html elige la pieza; por defecto, la primera (pilotes)
  const PAGE  = get('html', 'pilotes-reel.html');
  const HTML  = 'file://' + path.join(__dirname, PAGE);

  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
  });
  await page.goto(HTML, { waitUntil: 'load' });
  if (args.includes('--nosubs')) await page.evaluate(() => { window.SUBS_ON = false; });
  // document.fonts.ready sólo espera las fuentes YA en uso. En el segundo 0 no
  // hay texto en Work Sans, así que sin esto el primer frame de una escena que
  // la estrena sale con la fuente de reemplazo (más ancha: parte las líneas).
  await page.evaluate(async () => {
    const want = ['300 120px "Fraunces Display"',
                  '400 48px "Work Sans N"', '500 48px "Work Sans N"',
                  '400 34px "Plex Mono N"', '500 34px "Plex Mono N"'];
    await Promise.all(want.map(f => document.fonts.load(f, 'Ágj0123')));
    await document.fonts.ready;
  });
  const TOTAL = await page.evaluate(() => window.TOTAL);

  if (PROBE) {
    for (const sec of PROBE.split(',')) {
      const t = parseFloat(sec);
      await page.evaluate(t => window.renderFrame(t), t);
      const f = path.join(OUT, 'probe-' + sec.replace('.', '_') + 's.png');
      await page.screenshot({ path: f });
      console.log('probe', t + 's ->', f);
    }
    await browser.close();
    return;
  }

  const N = Math.round(TOTAL * FPS);
  console.log(`rendering ${PAGE}: ${N} frames @ ${FPS}fps (${TOTAL}s) -> ${OUT}`);
  const t0 = Date.now();
  for (let i = 0; i < N; i++) {
    await page.evaluate(t => window.renderFrame(t), i / FPS);
    await page.screenshot({
      path: path.join(OUT, 'f' + String(i).padStart(5, '0') + '.jpg'),
      type: 'jpeg', quality: 94,
    });
    if (i % 100 === 0 || i === N - 1) {
      const el = (Date.now() - t0) / 1000;
      console.log(`  ${i + 1}/${N}  ${el.toFixed(0)}s elapsed  eta ${(el / (i + 1) * (N - i - 1)).toFixed(0)}s`);
    }
  }
  await browser.close();
  console.log('done in', ((Date.now() - t0) / 1000).toFixed(0) + 's');
})().catch(e => { console.error(e); process.exit(1); });
