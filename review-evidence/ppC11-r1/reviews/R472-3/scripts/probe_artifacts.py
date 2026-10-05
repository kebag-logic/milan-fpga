#!/usr/bin/env python3
"""Artifact provenance, source geometry and gate controls in disposable copies."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('packet',type=Path);a=ap.parse_args()
root,packet=a.root.resolve(),a.packet.resolve();out=[]
def record(name,ok,**kw):
 out.append(dict(name=name,ok=ok,**kw));print(name,'PASS' if ok else 'FAIL',kw)
def git(*args):return subprocess.check_output(['git','-C',str(root),*args],text=True)
base=git('show','c050d971:docs/architecture/02_interfaces.md')
hist=(root/'docs/history/02-class-a-word-stream.md').read_text()
paragraph=hist[hist.index('Word-oriented stream,'):hist.index('\n## Its two waveforms')]
record('history-prose-table',paragraph.strip() in base)
oldwaves=re.findall(r'```wavedrom\n(.*?)\n```',base,re.S)[:2]
historywaves=re.findall(r'```json\n(.*?)\n```',hist,re.S)
record('history-waveform-bytes',oldwaves==historywaves)
def strip_comments(s):return re.findall(r'\S+',re.sub(r'/\*.*?\*/|//[^\n]*','',s,flags=re.S))
for f in git('diff','--name-only','ead80360..HEAD','--','hdl','tb').splitlines():
 if f.endswith(('.sv','.cpp')):record('executable-unchanged:'+f,strip_comments(git('show','ead80360:'+f))==strip_comments((root/f).read_text()))
top=(root/'hdl/top/protocol_processor_top.sv').read_text()
ports=set(re.findall(r'\b(?:input|output)\s+(?:wire|logic)\s+(?:\[[^\]]+\]\s*)?(\w+)',top))
names=set(re.findall(r'\b[a-zA-Z]\w*_[io]\b',(root/'docs/architecture/02_interfaces.md').read_text()))
record('02-port-names',not (names-ports),count=len(names),missing=sorted(names-ports))
record('top-no-rx-ready-error',not any(n in ports for n in ['rx_ready_o','rx_err_i','rx_sof_i']))
spec=importlib.util.spec_from_file_location('renderer',root/'scripts/render-wavedrom.py');render=importlib.util.module_from_spec(spec);spec.loader.exec_module(render)
blocks={anchor:json.loads(src) for _,anchor,src in render.collect_blocks()}
for name in ('fig-02-txwave','fig-02-memwave'):
 obj=blocks[name]; obj['config']['svg_margin']=0
 old=ET.fromstring(render.render_svg(json.dumps(obj)))
 x,y,w,h=map(float,old.get('viewBox').replace(',',' ').split())
 for margin in (0,1,40,80):
  obj['config']['svg_margin']=margin; new=ET.fromstring(render.render_svg(json.dumps(obj)))
  box=list(map(float,new.get('viewBox').replace(',',' ').split()))
  same=list(map(ET.tostring,old))==list(map(ET.tostring,new))
  record(f'{name}-margin-{margin}',box==[x-margin,y,w+2*margin,h] and same and float(new.get('width'))==w+2*margin,viewBox=box,children_identical=same)
 for bad in (-1,1.5,'40',True,None):
  obj['config']['svg_margin']=bad
  try: render.render_svg(json.dumps(obj));ok=False
  except ValueError as e:ok='config.svg_margin' in str(e)
  record(name+'-invalid-'+repr(bad),ok)

tree=packet/'scratch/artifact-tree'
if not tree.exists():
 subprocess.run(['git','clone','--quiet','--shared','--no-checkout',str(root),str(tree)],check=True)
 subprocess.run(['git','-C',str(tree),'checkout','--quiet','--detach','5123548eb4de35f24d43eb088c12dab70b06d01d'],check=True)
page=tree/'docs/architecture/02_interfaces.md';orig=page.read_bytes()
for name,body,expected in [('margin-removed',orig.replace(b' "config": {"svg_margin": 40},\n',b''),['WAVEDROM STALE:','fig-02-txwave','fig-02-memwave']),('negative-margin',orig.replace(b'"svg_margin": 40',b'"svg_margin": -1',1),['fig-02-txwave','config.svg_margin'])]:
 try:
  page.write_bytes(body)
  p=subprocess.run([sys.executable,str(tree/'scripts/render-wavedrom.py'),'--check'],capture_output=True,text=True)
  record(name,p.returncode==1 and all(t in p.stdout+p.stderr for t in expected),rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
 finally:page.write_bytes(orig)
f=tree/'tb/reviewer_probe.md'
for name,body,token in [('composition','T-ADP-\n// DELAY(-STRT)','T-ADP-DELAY-STRT'),('minus-one','P-REVIEWER-MISSING-1','P-REVIEWER-MISSING-1')]:
 try:
  f.write_text(body)
  p=subprocess.run(['make','-j16','ids'],cwd=tree,capture_output=True,text=True)
  record('make-ids-'+name,p.returncode==2 and token in p.stdout,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
 finally:f.unlink()
src=(root/'scripts/check-figures.py').read_text()
mutations={
 'foreignObject':src.replace('("image", "feImage", "foreignObject")','("image", "feImage")'),
 'root-namespace':src.replace('if svg.tag != f"{SVG_NS}svg":','if False:'),
 'empty-inventory':src.replace('if not names:\n        raise ValueError','if False:\n        raise ValueError'),
}
for name,body in mutations.items():
 assert body!=src
 f=packet/'scratch'/('figure-'+name+'.py');f.write_text(body)
 p=subprocess.run([sys.executable,str(f),'--selftest'],capture_output=True,text=True)
 record('figure-mutant-'+name,p.returncode==1 and 'SELFTEST FAIL:' in p.stdout,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
record('probe-copy-restored',not subprocess.check_output(['git','-C',str(tree),'status','--porcelain']))
(packet/'receipts/artifact-probes.json').write_text(json.dumps(out,indent=2)+'\n')
assert all(r['ok'] for r in out)
