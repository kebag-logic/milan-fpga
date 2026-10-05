// Measure every <text> bounding box of each SVG against its viewBox under several
// font selections, in headless Chromium. Usage: NODE_PATH=<mermaid-cli node_modules> node text_fit.js a.svg ...
const fs = require('fs'); const path = require('path');
const puppeteer = require('puppeteer');
const FONTS = [null, 'Adwaita Sans', 'Adwaita Mono', 'serif', 'sans-serif', 'monospace', 'DejaVu Sans', 'Liberation Serif'];
(async () => {
  const browser = await puppeteer.launch({headless: 'shell', args: ['--no-sandbox']});
  const page = await browser.newPage();
  let worst = 0;
  for (const file of process.argv.slice(2)) {
    const svg = fs.readFileSync(file, 'utf8');
    for (const font of FONTS) {
      const css = font ? `svg text, svg tspan { font-family: "${font}" !important; }` : '';
      await page.setContent(`<!doctype html><html><head><style>body{margin:0} ${css}</style></head><body>${svg}</body></html>`);
      await page.evaluate(() => document.fonts.ready);
      const r = await page.evaluate(() => {
        const s = document.querySelector('svg');
        const vb = s.viewBox.baseVal; const sr = s.getBoundingClientRect();
        const kx = vb.width / sr.width, ky = vb.height / sr.height;
        const out = [];
        for (const t of s.querySelectorAll('text')) {
          if (!t.textContent.trim()) continue;
          const b = t.getBoundingClientRect();
          const x0 = vb.x + (b.left - sr.left) * kx, x1 = vb.x + (b.right - sr.left) * kx;
          const y0 = vb.y + (b.top - sr.top) * ky, y1 = vb.y + (b.bottom - sr.top) * ky;
          out.push({text: t.textContent.trim(), x0, x1, y0, y1,
                    left: x0 - vb.x, right: vb.x + vb.width - x1, top: y0 - vb.y, bottom: vb.y + vb.height - y1,
                    family: getComputedStyle(t).fontFamily});
        }
        return {vb: [vb.x, vb.y, vb.width, vb.height], out};
      });
      const minL = Math.min(...r.out.map(o => o.left)), minR = Math.min(...r.out.map(o => o.right));
      const minT = Math.min(...r.out.map(o => o.top)), minB = Math.min(...r.out.map(o => o.bottom));
      const bad = r.out.filter(o => o.left < 0 || o.right < 0 || o.top < 0 || o.bottom < 0);
      if (bad.length) worst = 1;
      console.log(`${path.basename(file)} font=${font || '(as authored)'} viewBox=${r.vb.join(',')} texts=${r.out.length} ` +
        `minLeft=${minL.toFixed(2)} minRight=${minR.toFixed(2)} minTop=${minT.toFixed(2)} minBottom=${minB.toFixed(2)} ` +
        `${bad.length ? 'CLIPPED: ' + bad.map(o => JSON.stringify(o.text) + ` [${o.x0.toFixed(1)},${o.x1.toFixed(1)}]`).join('; ') : 'FIT'}`);
    }
  }
  await browser.close();
  process.exit(worst);
})().catch(e => { console.error(e); process.exit(2); });
