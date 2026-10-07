#!/usr/bin/env python3
"""Collect linked text contribution by object and compute historical deltas."""
import json,re
from pathlib import Path
p=Path(__file__).resolve().parents[1];out=[]
for n in (1,2):
 row={}
 for mode in ('round5','head'):
  lines=(p/f'scratch/sizes/1x1_tdm8-if{n}-{mode}/ctrl_app.map').read_text().split('Linker script and memory map',1)[1].splitlines()
  objects={};section=''
  for line in lines:
   m=re.match(r' (\.[\w.]+)',line)
   if m:section=m.group(1)
   m=re.search(r'0x[\da-f]+\s+0x([\da-f]+)\s+\S+/\d+-([\w_]+)\.o$',line)
   if m and section.startswith('.text'):
    name=m.group(2);objects[name]=objects.get(name,0)+int(m.group(1),16)
  row[mode]=objects
 diff={k:row['head'].get(k,0)-row['round5'].get(k,0) for k in row['head'].keys()|row['round5'].keys()}
 out.append({'interfaces':n,'text_by_object':row,'text_delta':dict(sorted(diff.items()))})
(p/'receipts/size-attribution.json').write_text(json.dumps(out,indent=2)+'\n')
