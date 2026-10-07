// Usage: NODE_PATH=<existing browser library directory> node inspect_graphs.cjs PACKET
// Screenshots and sampled geometric evidence supplement human visual inspection.
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {
  const packet = path.resolve(process.argv[2]);
  const out = path.join(packet, 'graphs');
  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox'], userDataDir: path.join(packet,'scratch','inspection-profile')});
  const page = await browser.newPage();
  const results = [];
  for (const file of fs.readdirSync(out).filter(f => f.endsWith('.svg')).sort()) {
    const svg = fs.readFileSync(path.join(out, file), 'utf8');
    await page.setViewport({width: 1800, height: 1600, deviceScaleFactor: 1});
    await page.setContent('<style>body{margin:0;background:white}svg{display:block;max-width:none!important}</style>' + svg);
    await page.evaluate(() => document.fonts.ready);
    const size = await page.evaluate(() => {
      const svg = document.querySelector('svg'), box = svg.viewBox.baseVal;
      const width = Math.ceil(box.width), height = Math.ceil(box.height);
      svg.style.width = width + 'px'; svg.style.height = height + 'px';
      return {width, height};
    });
    await page.setViewport({width: Math.max(size.width, 800), height: Math.max(size.height, 800), deviceScaleFactor: 1});
    const geometry = await page.evaluate(() => {
      const boxOf = el => {
        const r = el.getBoundingClientRect();
        return {id: el.id, label: el.textContent.trim(), x:r.x,y:r.y,w:r.width,h:r.height};
      };
      const nodes = [...document.querySelectorAll('g.node')].map(boxOf);
      // In sequence graphs actor and note rectangles are the visible boxes.
      if (!nodes.length) {
        for (const el of document.querySelectorAll('rect.actor, rect.note')) nodes.push(boxOf(el));
      }
      const paths = [...document.querySelectorAll('path[data-edge="true"], path.messageLine0, line.messageLine0, line.messageLine1')];
      const inside = (p,n,margin=1) => p.x>n.x+margin && p.x<n.x+n.w-margin && p.y>n.y+margin && p.y<n.y+n.h-margin;
      const crossings = [];
      for (const edge of paths) {
        const length=edge.getTotalLength(), transform=edge.getScreenCTM();
        const at = distance => {
          const point=edge.getPointAtLength(distance);
          return new DOMPoint(point.x,point.y).matrixTransform(transform);
        };
        const start=at(0), end=at(length);
        for (const node of nodes) {
          if (inside(start,node,-8) || inside(end,node,-8)) continue;
          for (let distance=0;distance<=length;distance+=0.5) {
            if (inside(at(distance),node)) {
              crossings.push({edge:edge.id||edge.dataset.id,node:node.id||node.label});break;
            }
          }
        }
      }
      return {nodes, edgeCount: paths.length, crossings};
    });
    await page.screenshot({path:path.join(out,file.replace('.svg','-native.png')),clip:{x:0,y:0,width:size.width,height:size.height}});
    const width=Math.min(760,size.width), height=Math.ceil(size.height*width/size.width);
    await page.evaluate(({width,height})=>{
      const svg=document.querySelector('svg');svg.style.width=width+'px';svg.style.height=height+'px';
    },{width,height});
    await page.screenshot({path:path.join(out,file.replace('.svg','-page.png')),clip:{x:0,y:0,width,height}});
    results.push({file,...size,pageWidth:width,pageHeight:height,...geometry});
    console.log(file, `${size.width}x${size.height}`, `page=${width}x${height}`, `crossings=${geometry.crossings.length}`);
  }
  fs.writeFileSync(path.join(packet,'receipts/graph-geometry.json'),JSON.stringify(results,null,2)+'\n');
  await browser.close();
})();
