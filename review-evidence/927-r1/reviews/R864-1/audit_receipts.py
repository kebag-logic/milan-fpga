#!/usr/bin/env python3
"""Audit public receipt hashes, carried RTL, route summaries, and budget inputs."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('repo',type=Path);p.add_argument('archive',type=Path);a=p.parse_args()
def git(*args):return subprocess.check_output(['git','--no-replace-objects',*args],cwd=a.repo,text=True)
print('HEAD',git('rev-parse','HEAD').strip());print('TREE',git('rev-parse','HEAD^{tree}').strip())
manifest=json.loads((a.archive/'MANIFEST.json').read_text());count=0
for e in manifest:
 f=a.archive/e['file']
 if f.is_file():
  assert hashlib.sha256(f.read_bytes()).hexdigest()==e['published_sha256'],str(f)
  count+=1
print('Public archive manifest hashes verified:',count,'receipt files; unextracted narratives not read')
def tokens(s):return re.sub(r'\s+','',re.sub(r'//[^\n]*|/\*.*?\*/','',s,flags=re.S))
for head in ['5d098172','338ece89']:
 paths=git('diff','--name-only',head,'HEAD','--','hdl').splitlines()
 for path in paths:
  if path.endswith(('.sv','.v')):assert tokens(git('show',head+':'+path))==tokens(git('show','HEAD:'+path)),path
 print('Carried HDL from',head,':',paths,'; changed HDL executable tokens equal')
p=a.archive/'author-r2/receipts'
print('ROUTES: published per-corner summaries, not rerouted')
for f in sorted((p/'route').glob('*/signoff.txt')):
 rows=re.findall(r'(Slow_85C|Slow_0C|Fast_85C|Fast_0C): WNS ([+\-\d.]+) ns \((\d+) failing\), WHS ([+\-\d.]+) ns \((\d+) failing\)',f.read_text())
 assert len(rows)==4
 for corner,wns,fail1,whs,fail2 in rows:assert float(wns)>=.030 and float(whs)>=0 and int(fail1)==int(fail2)==0
 status=(f.parent/'alinx_ax7101_route_status.rpt').read_text()
 def n(label):return int(re.search(re.escape(label)+r'\.+\s*:\s*(\d+)',status)[1])
 assert n('# of routable nets')==n('# of fully routed nets') and n('# of nets with routing errors')==0
 print(f.parent.name,'WNS',min(float(x[1]) for x in rows),'WHS',min(float(x[3]) for x in rows),'PASS all 4 corners; fully routed, zero errors')
print('BUDGET: public source-head evidence only')
for shape in ['1x1','8x8-1if']:
 o=json.loads((p/'budget'/shape/'build.json').read_text());b=json.loads((p/'budget'/('base-'+shape)/'build.json').read_text())
 ins={k.removeprefix('checkout:'):v for k,v in o['inputs'].items() if k.startswith('checkout:')}
 for f,h in ins.items():assert hashlib.sha256((a.repo/f).read_bytes()).hexdigest()==h,f
 print(shape,len(ins),'checkout inputs match reviewed head; changed vs base:',[k for k in o['inputs'] if k.startswith('checkout:') and o['inputs'][k]!=b['inputs'].get(k)])
 assert o['inputs']['build:image/ctrl_app.elf']==b['inputs']['build:image/ctrl_app.elf']
 print(shape,'control firmware ELF hash identical to base')
 head=(p/'budget/units'/f'regrade-{shape}.log').read_text()
 base='\n'.join(f.read_text() for f in (p/'budget/units').glob(f'base-{shape}*.log'))
 for kind in ['BUDGET','STATED']:
  lines=[l for l in head.splitlines() if l.startswith(kind)]
  absent=[l for l in lines if l not in base]
  print(shape,kind,'lines',len(lines),'not present verbatim in published base sample',len(absent))
  for line in absent:print('UNPAIRED BASE SAMPLE:',line)
 print('\n'.join(l for l in head.splitlines() if 'groups graded' in l))
print('NATIVE SOURCE SWEEP: published exact-head summaries')
for f in sorted((p/'sweep').glob('*-spec.json')):assert json.loads(f.read_text())['head']==git('rev-parse','HEAD').strip()
for f in sorted((p/'sweep').glob('*-summary.log')):
 print(f.name);print(f.read_text())
print('PUBLIC RECEIPT AUDIT COMPLETE')
