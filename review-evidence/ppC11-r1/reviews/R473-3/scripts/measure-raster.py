#!/usr/bin/env python3
"""Measure text-only ink on a padded canvas, then render the unmodified SVGs.
Usage: python3 measure-raster.py SOURCE PACKET. Requires pillow and rsvg-convert.
"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
from PIL import Image,ImageChops

source,packet=map(Path,sys.argv[1:3]); rows=[]
ns='{http://www.w3.org/2000/svg}'
for name in ('fig-02-txwave','fig-02-memwave'):
 for rev in ('HEAD','80588cdc'):
  data=subprocess.check_output(['git','-C',str(source),'show',rev+':docs/diagrams/wavedrom/'+name+'.svg'])
  for font in ('default','sans-serif','serif','monospace','Adwaita Sans','Adwaita Mono'):
   root=ET.fromstring(data if font=='default' else data.replace(b'font-family:Helvetica',('font-family:"'+font+'"').encode()))
   x,y,w,h=map(float,root.attrib['viewBox'].replace(',',' ').split())
   pad=400
   root.set('viewBox',f'{x-pad} {y-pad} {w+2*pad} {h+2*pad}')
   root.set('width',str(w+2*pad));root.set('height',str(h+2*pad))
   style=ET.SubElement(root,ns+'style')
   style.text='path,rect,use,polygon,polyline,line,circle,ellipse {visibility:hidden !important} text,tspan {visibility:visible !important;fill:#000 !important;stroke:none !important;}'
   svg=packet/'scratch'/f'{name}-{rev}-{font}.svg';svg.write_bytes(ET.tostring(root))
   png=svg.with_suffix('.png')
   subprocess.run(['rsvg-convert','-b','white','-o',str(png),str(svg)],check=True)
   image=Image.open(png).convert('RGB')
   box=ImageChops.difference(image,Image.new('RGB',image.size,'white')).getbbox()
   assert box
   l,t,r,b=(v-pad for v in box)
   ok=l>=0 and t>=0 and r<=w and b<=h
   rows.append(dict(name=name,rev=rev,font=font,width=w,height=h,bounds=[l,t,r,b],fits=ok))
   if rev=='HEAD': assert ok,rows[-1]
  if rev=='HEAD':
   subprocess.run(['rsvg-convert','-b','white','-o',str(packet/'receipts'/(name+'-raster.png')),
                   str(source/'docs/diagrams/wavedrom'/(name+'.svg'))],check=True)
for name in ('fig-02-txwave','fig-02-memwave'):
 assert any(r['name']==name and r['rev']=='80588cdc' and not r['fits'] for r in rows)
(packet/'receipts/raster-bounds.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows:print(row)
