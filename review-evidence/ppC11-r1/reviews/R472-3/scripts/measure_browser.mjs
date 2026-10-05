// Usage: node measure_browser.mjs REPO PACKET PUPPETEER_PACKAGE_DIRECTORY
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {execFileSync} from 'node:child_process';
const [repo, packet, moduleDir] = process.argv.slice(2);
const require = createRequire(path.join(moduleDir,'package.json'));
const puppeteer = require(moduleDir);
const browser = await puppeteer.launch({headless:true,args:['--no-sandbox','--disable-gpu']});
const results=[];
try {
 const page=await browser.newPage();
 await page.setViewport({width:1100,height:500,deviceScaleFactor:1});
 for (const revision of ['HEAD','80588cdc43ca5605a1d3748d13dd8ed7f22f7000']) {
  for (const name of ['txwave','memwave']) {
   const rel=`docs/diagrams/wavedrom/fig-02-${name}.svg`;
   const source=execFileSync('git',['-C',repo,'show',`${revision}:${rel}`],{encoding:'utf8'});
   for (const font of ['default','sans-serif','monospace','Arial','Adwaita Sans','Adwaita Mono']) {
    const override=font==='default'?'':`<style>text,tspan{font-family:"${font}"!important}</style>`;
    await page.setContent(`<html><style>body{margin:0}</style><body>${source.replace('</svg>',override+'</svg>')}</body></html>`);
    await page.evaluate(()=>document.fonts.ready);
    const measured=await page.evaluate(()=>{
     const svg=document.querySelector('svg'),box=svg.getBoundingClientRect();
     const rows=[...svg.querySelectorAll('text')].map(e=>{
      const r=e.getBoundingClientRect();
      return {text:e.textContent,font:getComputedStyle(e).fontFamily,left:r.left-box.left,top:r.top-box.top,right:r.right-box.left,bottom:r.bottom-box.top};
     });
     const outside=rows.filter(r=>r.left<-.05||r.top<-.05||r.right>box.width+.05||r.bottom>box.height+.05);
     return {width:box.width,height:box.height,rows,outside};
    });
    results.push({revision,name,font,...measured});
    if (font==='default') await (await page.$('svg')).screenshot({path:path.join(packet,'receipts',`browser-${revision==='HEAD'?'head':'old'}-${name}.png`)});
   }
  }
 }
 const output={version:await browser.version(),results};
 fs.writeFileSync(path.join(packet,'receipts/browser-bounds.json'),JSON.stringify(output,null,2)+'\n');
 for (const r of results) console.log(r.revision.slice(0,8),r.name,r.font,'left',Math.min(...r.rows.map(x=>x.left)),'outside',JSON.stringify(r.outside));
 if(results.some(r=>r.revision==='HEAD'&&r.outside.length)) process.exitCode=1;
 for(const name of ['txwave','memwave']) if(!results.some(r=>r.revision!=='HEAD'&&r.name===name&&r.outside.length)) process.exitCode=1;
} finally {await browser.close();}
