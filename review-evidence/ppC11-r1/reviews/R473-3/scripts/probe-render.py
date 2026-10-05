#!/usr/bin/env python3
"""Exercise margin geometry, invalid inputs, and the actual freshness gate.
Run with an interpreter providing wavedrom==2.0.3.post3; SOURCE PACKET arguments.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

source,packet=map(Path,sys.argv[1:3]);sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('render',source/'scripts/render-wavedrom.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
out=[]
for _,anchor,src in mod.collect_blocks():
 if anchor not in ('fig-02-txwave','fig-02-memwave'): continue
 data=json.loads(src);data['config'].pop('svg_margin')
 original=mod.render_svg(json.dumps(data)); orig=ET.fromstring(original)
 x,y,w,h=map(float,orig.attrib['viewBox'].replace(',',' ').split())
 for margin in (0,1,40,80):
  data['config']['svg_margin']=margin
  actual=mod.render_svg(json.dumps(data));root=ET.fromstring(actual)
  assert list(map(float,root.attrib['viewBox'].replace(',',' ').split()))==[x-margin,y,w+2*margin,h]
  assert float(root.attrib['width'])==w+2*margin
  assert root.attrib['height']==orig.attrib['height']
  assert [ET.tostring(a) for a in root]==[ET.tostring(a) for a in orig]
  if margin==0:assert actual==original
  out.append({'anchor':anchor,'margin':margin,'geometry':'PASS','children':'identical'})
 for bad in (-1,0.5,'40',True,None):
  data['config']['svg_margin']=bad
  try:mod.render_svg(json.dumps(data))
  except ValueError as e:
   assert 'non-negative integer' in str(e)
   out.append({'anchor':anchor,'invalid_margin':bad,'rejected':str(e)})
  else:raise AssertionError(bad)

copy=packet/'scratch/suites';path=copy/'docs/architecture/02_interfaces.md'
original=path.read_bytes()
env=os.environ.copy();env['TMPDIR']=str(packet/'scratch')
try:
 for label,replacement in [('removed-margin',b'"svg_margin": 0'),('invalid-margin',b'"svg_margin": -1')]:
  assert original.count(b'"svg_margin": 40')==2
  path.write_bytes(original.replace(b'"svg_margin": 40',replacement))
  cp=subprocess.run([sys.executable,'scripts/render-wavedrom.py','--check'],cwd=copy,env=env,text=True,capture_output=True)
  (packet/'receipts'/(label+'.log')).write_text(cp.stdout+cp.stderr)
  (packet/'receipts'/(label+'.rc')).write_text(str(cp.returncode)+'\n')
  assert cp.returncode==1
  assert ('fig-02-txwave' in cp.stdout and 'fig-02-memwave' in cp.stdout) if label=='removed-margin' else 'non-negative integer' in cp.stderr
finally:path.write_bytes(original)
cp=subprocess.run([sys.executable,'scripts/render-wavedrom.py','--check'],cwd=copy,env=env,text=True,capture_output=True)
assert cp.returncode==0
out.append({'restored_freshness_rc':cp.returncode,'stdout':cp.stdout})
(packet/'receipts/render-probes.json').write_text(json.dumps(out,indent=2)+'\n')
print('18 geometry/input checks PASS; both freshness faults caught; restored copy fresh')
