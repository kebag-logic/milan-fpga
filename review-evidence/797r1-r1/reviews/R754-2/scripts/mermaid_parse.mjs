// Parse every Mermaid block of a Markdown page with the published parser. Usage: node mermaid_parse.mjs <page>
import { readFileSync } from 'fs';
import { JSDOM } from 'jsdom';
const dom = new JSDOM('<!doctype html><body></body>');
globalThis.window = dom.window; globalThis.document = dom.window.document;
const mermaid = (await import('mermaid')).default;
mermaid.initialize({ startOnLoad: false });
const t = readFileSync(process.argv[2], 'utf8');
let i = 0, bad = 0;
for (const m of t.matchAll(/```mermaid\n([\s\S]*?)```/g)) {
  i++;
  try { const r = await mermaid.parse(m[1]); console.log(`block ${i} ok ${r.diagramType}`); }
  catch (e) { bad++; console.log(`block ${i} FAIL ${String(e.message).slice(0, 300)}`); }
}
console.log(`blocks ${i} failed ${bad}`);
