#!/usr/bin/env python3
"""Read-only scope, port, history and prior-control reconciliation."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

source,packet=map(Path,sys.argv[1:3]);out={}
def git(*args):return subprocess.check_output(['git','-C',str(source),*args],text=True)
def tokens(s):
 s=re.sub(r'("(?:\\.|[^"\\])*")|//[^\n]*|/\*[\s\S]*?\*/',lambda m:m.group(1) or '',s)
 return re.findall(r'"(?:\\.|[^"\\])*"|\w+|[^\s]',s)
changed=git('diff','--name-only','ead80360..HEAD','--','hdl','tb').splitlines()
out['c11_compiled_identity']=[]
for path in changed:
 if Path(path).suffix not in ('.sv','.cpp'):continue
 a=tokens(git('show','ead80360:'+path));b=tokens((source/path).read_text())
 assert a==b,path
 out['c11_compiled_identity'].append({'path':path,'tokens':len(a),'equal':True})
assert len(out['c11_compiled_identity'])==4
out['round3_changed']=git('diff','--name-only','80588cdc..HEAD').splitlines()
assert len(out['round3_changed'])==7 and not any(x.startswith(('hdl/','tb/')) for x in out['round3_changed'])
top=(source/'hdl/top/protocol_processor_top.sv').read_text()
ports=set(re.findall(r'\b(?:input|output|inout)\s+(?:wire|logic)\s*(?:\[[^\]]+\]\s*)?(\w+)',top))
iface=(source/'docs/architecture/02_interfaces.md').read_text()
names=set(re.findall(r'(?<![A-Za-z0-9_*])([A-Za-z][A-Za-z0-9_]*_[io])\b',iface))
assert not names-ports,sorted(names-ports)
out['interface_ports']={'named':len(names),'all_top_ports':True,'names':sorted(names)}
old=git('show','c050d971:docs/architecture/02_interfaces.md')
hist=(source/'docs/history/02-class-a-word-stream.md').read_text()
paragraph=hist.split('## The word stream as specified\n\n')[1].split('\n## Its two waveforms')[0].strip()
assert paragraph in old
waves=re.findall(r'```json\n(.*?)\n```',hist,re.S)
assert len(waves)==2 and all(w in old for w in waves)
out['history']={'paragraph_and_table_verbatim':True,'wave_sources_verbatim':2}
pngs=[s for s in git('ls-files','docs/diagrams').splitlines() if s.endswith('.png')]
assert not pngs;out['tracked_pngs']=pngs
checker=source/'scripts/check-figures.py';body=checker.read_text()
changes={
 'figure-skip-foreignObject':('for tag in ("image", "feImage", "foreignObject"):', 'for tag in ("image", "feImage"):'),
 'figure-skip-namespace':('if svg.tag != f"{SVG_NS}svg":', 'if svg.tag.rsplit("}", 1)[-1] != "svg":'),
 'figure-skip-root':('if svg.tag != f"{SVG_NS}svg":', 'if False:'),
 'figure-skip-empty-inventory':('if not names:', 'if False and not names:'),
}
env=os.environ.copy();env['TMPDIR']=str(packet/'scratch')
out['figure_mutants']=[]
for name,(a,b) in changes.items():
 assert body.count(a)==1
 p=packet/'scratch'/(name+'.py');p.write_text(body.replace(a,b))
 cp=subprocess.run([sys.executable,str(p),'--selftest'],env=env,text=True,capture_output=True)
 assert cp.returncode==1 and 'SELFTEST FAIL' in cp.stdout
 (packet/'receipts'/(name+'.log')).write_text(cp.stdout+cp.stderr)
 (packet/'receipts'/(name+'.rc')).write_text(str(cp.returncode)+'\n')
 out['figure_mutants'].append({'name':name,'rc':cp.returncode})

# The exact F3 composition and F4 negatives must fail through make as well.
copy=packet/'scratch/suites';plant=copy/'tb/review-id-plant.md'
forms=[('composition','T-ADP-\n// DELAY(-STRT)','T-ADP-DELAY-STRT'),
       ('optional-break','T-ADP-DELAY(-\n// STRT)','T-ADP-DELAY-STRT'),
       ('minus-one','P-REVIEWER-MISSING-1','P-REVIEWER-MISSING-1'),
       ('valid-composition','T-ADP-\n// DELAY(-START)',None)]
out['make_ids_plants']=[]
try:
 for name,text,token in forms:
  plant.write_text(text)
  cp=subprocess.run(['make','-j16','ids'],cwd=copy,env=env,text=True,capture_output=True)
  assert cp.returncode==(2 if token else 0)
  assert token is None or token in cp.stdout
  (packet/'receipts'/('make-ids-'+name+'.log')).write_text(cp.stdout+cp.stderr)
  (packet/'receipts'/('make-ids-'+name+'.rc')).write_text(str(cp.returncode)+'\n')
  out['make_ids_plants'].append({'name':name,'rc':cp.returncode,'token':token})
finally:plant.unlink(missing_ok=True)
(packet/'receipts/artifacts.json').write_text(json.dumps(out,indent=2)+'\n')
print('Scope, history and ports PASS; four figure mutants killed; four complete ids target plants PASS')
