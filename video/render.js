const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const args = process.argv.slice(2);
  const get = (k, d) => { const i = args.indexOf('--' + k); return i < 0 ? d : args[i + 1]; };
  const FPS   = parseFloat(get('fps', 30));
  const OUT   = get('out', path.join(__dirname, 'frames'));
  const PROBE = get('probe', null);          // comma-separated seconds -> png probes
  const HTML  = 'file://' + path.join(__dirname, 'pilotes-reel.html');

  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
  });
  await page.goto(HTML, { waitUntil: 'load' });
  if (args.includes('--nosubs')) await page.evaluate(() => { window.SUBS_ON = false; });
  await page.evaluate(() => document.fonts.ready);
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
  console.log(`rendering ${N} frames @ ${FPS}fps (${TOTAL}s) -> ${OUT}`);
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
