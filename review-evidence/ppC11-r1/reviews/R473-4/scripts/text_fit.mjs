#!/usr/bin/env node
// Check every SVG text rectangle under explicit font substitution.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';

const [source, scratch, receipt, cliPackage, ...extraAnchors] = process.argv.slice(2);
if (!cliPackage) throw new Error('source scratch receipt mermaid-cli/package.json required');
const require = createRequire(cliPackage);
const puppeteer = require('puppeteer');
const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox', '--disable-gpu']});
const page = await browser.newPage();
await page.setViewport({width: 1100, height: 420, deviceScaleFactor: 1});
const fonts = ['sans-serif', 'serif', 'monospace', 'Adwaita Sans', 'Adwaita Mono'];
const result = [];
let failures = 0;
try {
  for (const anchor of ['fig-02-txwave', 'fig-02-memwave', ...extraAnchors]) {
    const rel = `docs/diagrams/wavedrom/${anchor}.svg`;
    for (const version of extraAnchors.includes(anchor) ? ['current'] : ['current', 'old-control']) {
      const src = version === 'current' ? fs.readFileSync(path.join(source, rel), 'utf8') :
        execFileSync('git', ['-C', source, 'show', `80588cdc43ca5605a1d3748d13dd8ed7f22f7000:${rel}`], {encoding: 'utf8'});
      for (const font of fonts) {
        await page.setContent(`<html><body style="margin:0">${src}</body></html>`);
        const row = await page.evaluate(async (font) => {
          const style = document.createElement('style');
          style.textContent = `svg text, svg tspan {font-family: '${font}' !important;}`;
          document.head.append(style);
          await document.fonts.ready;
          const svg = document.querySelector('svg');
          const viewport = svg.getBoundingClientRect();
          const texts = [...svg.querySelectorAll('text')].filter(e => !e.closest('defs')).map(e => {
            const box = e.getBoundingClientRect();
            return {text: e.textContent, left: box.left - viewport.left,
              right: viewport.right - box.right, top: box.top - viewport.top,
              bottom: viewport.bottom - box.bottom};
          });
          const clipped = texts.filter(t => Math.min(t.left, t.right, t.top, t.bottom) < -0.1);
          return {font, width: viewport.width, height: viewport.height, texts, clipped,
            minHorizontalMargin: Math.min(...texts.flatMap(t => [t.left, t.right]))};
        }, font);
        result.push({anchor, version, ...row});
        if (version === 'current' && row.clipped.length) failures++;
        console.log(JSON.stringify({anchor, version, font, margin: row.minHorizontalMargin, clipped: row.clipped}));
        if (version === 'current' && ['Adwaita Sans', 'Adwaita Mono'].includes(font)) {
          await page.screenshot({path: path.join(scratch, `${anchor}-${font.replaceAll(' ', '-')}.png`)});
        }
      }
    }
    if (!extraAnchors.includes(anchor) && !result.some(r => r.anchor === anchor && r.version === 'old-control' && r.clipped.length)) failures++;
  }
} finally {
  await browser.close();
}
fs.writeFileSync(receipt, JSON.stringify({fonts, failures, result}, null, 2) + '\n');
console.log(`Text-fit failures: ${failures}; prior exports must expose clipping`);
process.exitCode = failures ? 1 : 0;
