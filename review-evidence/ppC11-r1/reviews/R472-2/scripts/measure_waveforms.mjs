#!/usr/bin/env node
// Measure committed waveform text against its actual SVG viewport.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const [modulePath, repo, captures] = process.argv.slice(2);
const {default: browserDriver} = await import(pathToFileURL(path.resolve(modulePath)));
const browser = await browserDriver.launch({headless: true, args: ['--no-sandbox']});
try {
  const page = await browser.newPage();
  for (const figure of ['fig-02-rxwave', 'fig-02-txwave', 'fig-02-memwave']) {
    await page.goto(pathToFileURL(path.resolve(repo, 'docs/diagrams/wavedrom', figure+'.svg')).href);
    await page.evaluate(() => document.fonts.ready);
    const measured = await page.evaluate(() => {
      const svg = document.querySelector('svg');
      const viewport = svg.getBoundingClientRect();
      return {width: viewport.width, height: viewport.height,
        overflow: [...svg.querySelectorAll('text')].map(t => {
          const r=t.getBoundingClientRect();
          return {text:t.textContent, font:getComputedStyle(t).font, left:r.left-viewport.left,
                  right:r.right-viewport.left, top:r.top-viewport.top,
                  bottom:r.bottom-viewport.top};
        }).filter(t=>t.left < -0.1 || t.right > viewport.width+0.1 || t.top < -0.1 || t.bottom > viewport.height+0.1)};
    });
    console.log(JSON.stringify({figure,...measured}));
    if (captures) {
      await fs.mkdir(captures, {recursive:true});
      const element = await page.$('svg');
      await element.screenshot({path:path.join(captures,figure+'.png')});
    }
  }
} finally { await browser.close(); }
