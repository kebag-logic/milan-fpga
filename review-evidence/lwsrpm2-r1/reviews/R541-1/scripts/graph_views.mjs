// SPDX-License-Identifier: Apache-2.0
// Usage: node graph_views.mjs GRAPH_DIRECTORY PUPPETEER_MODULE
import fs from "node:fs/promises";
import path from "node:path";
import {pathToFileURL} from "node:url";
const [dir,modulePath]=process.argv.slice(2);
const {default:puppeteer}=await import(pathToFileURL(path.resolve(modulePath)));
const browser=await puppeteer.launch({headless:true,args:["--no-sandbox"]});
const page=await browser.newPage();
const files=(await fs.readdir(dir)).filter(x=>x.endsWith(".svg")).sort();
const items=[];
for(const file of files){
 const svg=await fs.readFile(path.join(dir,file),"utf8");
 const size=/viewBox="([^"]+)"/.exec(svg)?.[1].split(" ").map(Number);
 await page.setViewport({width:Math.ceil(size?.[2]||1200)+20,height:Math.ceil(size?.[3]||1200)+20});
 await page.setContent(`<style>body{margin:0;background:white}</style>${svg}`);
 await (await page.$("svg")).screenshot({path:path.join(dir,file+".png")});
 items.push({file,svg});
}
await page.setViewport({width:1600,height:1750});
for(let k=0;k<items.length;k+=4){
 const html=items.slice(k,k+4).map(x=>`<section><h3>${x.file}</h3><div>${x.svg}</div></section>`).join("");
 await page.setContent(`<style>body{margin:0;background:white;font:18px sans-serif;display:grid;grid-template-columns:800px 800px}section{height:870px;border:1px solid #999;box-sizing:border-box;padding:15px}h3{font-size:18px;margin:5px}section div{height:800px;display:flex;align-items:center;justify-content:center}section svg{max-width:765px;max-height:800px;width:100%;height:100%}</style>${html}`);
 await page.screenshot({path:path.join(dir,`sheet-${k/4+1}.png`)});
}
await browser.close();console.log(`Native views=${files.length}; page-width sheets=${Math.ceil(files.length/4)}`);
