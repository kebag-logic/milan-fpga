// Usage: node measure-browser.cjs SOURCE PACKET PUPPETEER_MODULE
const fs=require('fs'), path=require('path'), cp=require('child_process');
const [source,packet,modulePath]=process.argv.slice(2);
const browserAPI=require(modulePath);
(async()=>{
 const browser=await browserAPI.launch({headless:true,args:['--no-sandbox','--disable-gpu']});
 const page=await browser.newPage();
 await page.setViewport({width:1500,height:700,deviceScaleFactor:1});
 const rows=[];
 const fonts=['default','sans-serif','serif','monospace','Adwaita Sans','Adwaita Mono'];
 for(const name of ['fig-02-txwave','fig-02-memwave']) {
  const rel='docs/diagrams/wavedrom/'+name+'.svg';
  for(const rev of ['HEAD','80588cdc']) {
   const svg=cp.execFileSync('git',['-C',source,'show',rev+':'+rel],{encoding:'utf8'});
   for(const font of fonts) {
    await page.setContent('<!doctype html><style>body{margin:0}</style>'+svg);
    if(font!=='default') await page.addStyleTag({content:'text,tspan {font-family:'+JSON.stringify(font)+' !important}'});
    await page.evaluate(()=>document.fonts.ready);
    const bounds=await page.evaluate(()=>{
     const root=document.querySelector('svg'),view=root.getBoundingClientRect();
     const texts=[...root.querySelectorAll('text')].map(t=>{
      const r=t.getBoundingClientRect();
      return {text:t.textContent,font:getComputedStyle(t).fontFamily,
       left:r.left-view.left,right:r.right-view.left,top:r.top-view.top,bottom:r.bottom-view.top};
     });
     return {width:view.width,height:view.height,viewBox:root.getAttribute('viewBox'),texts,
      overflow:texts.filter(t=>t.left < -0.05 || t.right>view.width+0.05 || t.top < -0.05 || t.bottom>view.height+0.05)};
    });
    rows.push({name,rev,font,...bounds});
    if(rev==='HEAD' && bounds.overflow.length) throw Error(JSON.stringify(rows.at(-1)));
    if(font==='default' && rev==='HEAD') await (await page.$('svg')).screenshot({path:path.join(packet,'receipts',name+'-browser.png')});
   }
  }
 }
 const controls=rows.filter(x=>x.rev==='80588cdc' && x.font==='default');
 if(controls.some(x=>!x.overflow.length)) throw Error('Original figure did not fail control');
 fs.writeFileSync(path.join(packet,'receipts/browser-bounds.json'),JSON.stringify({version:await browser.version(),rows},null,2)+'\n');
 for(const x of rows) console.log(x.name,x.rev,x.font,'text',x.texts.length,'overflows',x.overflow.length,
   'left',Math.min(...x.texts.map(t=>t.left)).toFixed(3),'right',Math.max(...x.texts.map(t=>t.right)).toFixed(3),'width',x.width);
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
