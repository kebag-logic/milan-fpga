// Parse every Mermaid block with the library's own parser. Usage: node mermaid_parse.mjs <mm-dir> <blocks-dir>
import { createRequire } from 'module'; import fs from 'fs'; import path from 'path';
const [mm, dir] = process.argv.slice(2);
const req = createRequire(path.join(path.resolve(mm), 'x.js'));
const { JSDOM } = req('jsdom');
const dom = new JSDOM('<!doctype html><body></body>'); globalThis.window = dom.window; globalThis.document = dom.window.document;
const mermaid = (await import(path.resolve(mm, 'node_modules/mermaid/dist/mermaid.core.mjs'))).default;
mermaid.initialize({ startOnLoad: false });
let bad = 0;
for (const f of fs.readdirSync(dir).sort()) {
  const src = fs.readFileSync(path.join(dir, f), 'utf8');
  try { const r = await mermaid.parse(src); console.log('ok ', f, r.diagramType); }
  catch (e) { bad++; console.log('BAD', f, String(e.message).split('\n').slice(0, 4).join(' | ')); }
}
console.log('blocks', fs.readdirSync(dir).length, 'bad', bad);
