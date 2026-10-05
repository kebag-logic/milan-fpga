#!/usr/bin/env python3
"""Measure text ink and logical bounds through the installed SVG render library."""
import argparse
import ctypes as C
import ctypes.util
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('packet',type=Path);a=ap.parse_args()
lib=C.CDLL(ctypes.util.find_library('rsvg-2')); gobj=C.CDLL(ctypes.util.find_library('gobject-2.0'))
class Rect(C.Structure): _fields_=[(n,C.c_double) for n in ('x','y','width','height')]
lib.rsvg_handle_new_from_data.argtypes=[C.c_char_p,C.c_size_t,C.c_void_p];lib.rsvg_handle_new_from_data.restype=C.c_void_p
lib.rsvg_handle_set_dpi.argtypes=[C.c_void_p,C.c_double]
lib.rsvg_handle_get_geometry_for_layer.argtypes=[C.c_void_p,C.c_char_p,C.POINTER(Rect),C.POINTER(Rect),C.POINTER(Rect),C.c_void_p]
lib.rsvg_handle_get_geometry_for_layer.restype=C.c_int
gobj.g_object_unref.argtypes=[C.c_void_p]
results=[]
for revision in ('HEAD','80588cdc43ca5605a1d3748d13dd8ed7f22f7000'):
 for name in ('txwave','memwave'):
  rel=f'docs/diagrams/wavedrom/fig-02-{name}.svg'
  original=subprocess.check_output(['git','-C',str(a.root),'show',revision+':'+rel],text=True)
  for font in ('default','Adwaita Sans','Adwaita Mono'):
   tree=ET.fromstring(original); texts=list(tree.iter('{http://www.w3.org/2000/svg}text'))
   # Preserve default namespaces and CSS selectors exactly. Only add text IDs.
   ids=iter(range(len(texts)))
   source=re.sub(r'<text\b([^>]*)>',lambda m:'<text id="review-text-'+str(next(ids))+'"'+re.sub(r'\s+id="[^"]*"','',m[1])+'>',original)
   if font!='default': source=source.replace('font-family:Helvetica',f'font-family:"{font}"')
   data=source.encode()
   handle=lib.rsvg_handle_new_from_data(data,len(data),None);assert handle
   lib.rsvg_handle_set_dpi(handle,96.0)
   width,height=float(tree.get('width')),float(tree.get('height'))
   viewport=Rect(0,0,width,height);rows=[]
   for i,el in enumerate(texts):
    ink,logical=Rect(),Rect()
    ok=lib.rsvg_handle_get_geometry_for_layer(handle,f'#review-text-{i}'.encode(),C.byref(viewport),C.byref(ink),C.byref(logical),None)
    assert ok
    row={'text':''.join(el.itertext())}
    for key,r in [('ink',ink),('logical',logical)]: row[key]={'left':r.x,'top':r.y,'right':r.x+r.width,'bottom':r.y+r.height}
    rows.append(row)
   outside=[r for r in rows if any(v['left']<-.05 or v['top']<-.05 or v['right']>width+.05 or v['bottom']>height+.05 for v in (r['ink'],r['logical']))]
   gobj.g_object_unref(handle)
   results.append(dict(revision=revision,name=name,font=font,width=width,height=height,rows=rows,outside=outside))
   print(revision[:8],name,font,'left',min(r['logical']['left'] for r in rows),'outside',json.dumps(outside))
   if font=='default':
    tag='head' if revision=='HEAD' else 'old'
    subprocess.run(['rsvg-convert','--background-color=white','-o',str(a.packet/f'receipts/native-{tag}-{name}.png')],input=original,text=True,check=True)
(a.packet/'receipts/native-bounds.json').write_text(json.dumps(results,indent=2)+'\n')
assert not any(r['outside'] for r in results if r['revision']=='HEAD')
assert all(any(r['outside'] for r in results if r['name']==n and r['revision']!='HEAD') for n in ('txwave','memwave'))
