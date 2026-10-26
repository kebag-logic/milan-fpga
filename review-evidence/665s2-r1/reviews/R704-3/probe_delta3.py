#!/usr/bin/env python3
"""Independent populations, capacity, omission, composition and shutdown checks."""
import hashlib,json,os,sys
from pathlib import Path
from unittest.mock import patch
root=Path(os.environ['REVIEW_ROOT']);p=Path(os.environ['REVIEW_PACKET'])
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import scenario,grade,selftest,run
out={'populations':{},'mutants':{},'capacity':{},'shutdown':{},'builds':{}}
want={'adp':8,'acmp':12,'aecp':16,'maap':7,'srp':32,'GM':15}
for label,point in [('A1','1x1'),('A8','8x8')]:
 spec=json.loads((p/'scratch'/label/'build.json').read_text());pt=scenario.point(point,spec)
 for g in scenario.backlog_groups(pt):
  expected=dict(want)
  if g.name=='backlog':expected['LINK']=1
  if g.name=='backlog-adp-refill':expected['adp']=11
  # Decode transmitted bytes directly rather than accepting Group.load.
  actual={};inside=False
  for line in g.steps:
   if line=='mark composed':inside=True
   if line=='mark composed_end':inside=False
   if not inside:continue
   w=line.split();name=None
   if w[0]=='frame':
    f=bytes.fromhex(w[2]);et=int.from_bytes(f[12:14],'big')
    name='srp' if et in (0x22ea,0x88f5) else {0xfa:'adp',0xfb:'aecp',0xfc:'acmp',0xfe:'maap'}[f[14]]
   if w[0]=='reply':name=[c.name for c in scenario.CONTRACT.channels][int(w[2])]
   if w[0] in ('gm','link'):name=w[0].upper()
   if name:actual[name]=actual.get(name,0)+1
  assert actual==expected,(label,g.name,actual)
  out['populations'][label+'/'+g.name]=actual
 g=scenario.aecp_fanout_groups(pt,spec)[0]
 out['capacity'][label]=[{'probe':r.name,'recipients':len(r.recipients)} for r in g.probes]
 assert all(len(r.recipients)==16*pt.interfaces for r in g.probes)
 groups=scenario.shutdown_groups(pt);keys=[r.path_key() for g in groups for r in g.probes]
 out['shutdown'][label]={'paths':len(set(keys)),'instances':len(keys)}
 assert (len(set(keys)),len(keys))==((1,2) if label=='A1' else (2,3))
 published=json.loads((p/'scratch/public/author-r3/receipts/builds'/f'{label}.build.json').read_text())
 matching={};different={}
 for key,value in spec['inputs'].items():
  old=published['inputs'].get(key)
  if old is None and key.startswith('build:python/'):
   old=next((v for k,v in published['inputs'].items() if k.endswith('/'+key.split('/')[-1])),None)
  if old is not None:(matching if old==value else different)[key]=value
 out['builds'][label]={'matching_inputs':matching,'different_inputs':different,'netlist':spec['netlist'],
  'configuration_equal':all(spec[k]==published[k] for k in ('sys_hz','cpu_hz','vexii_args','vexii_soc_args','cpu_memory_regions','memory_regions'))}
 assert spec['inputs']['build:image/ctrl_app.elf']==published['inputs']['build:image/ctrl_app.elf']
 assert out['builds'][label]['configuration_equal']
original=scenario.Group.offer
for ch in ('srp','maap','acmp'):
 def omitted(self,channel,step,frame):
  if self.name.startswith('backlog') and channel==ch and (ch!='acmp' or 'mark backlog.owed.if0' in self.steps):return
  return original(self,channel,step,frame)
 with patch.object(scenario.Group,'offer',omitted):
  failed=[n for n,ok,_ in selftest.checks() if not ok]
 assert "every composed window's stimulus is its defined load" in failed
 out['mutants']['omit-'+ch]=failed
original_max=grade.composed
def halved(*args):
 result=original_max(*args)
 if result is not None:result=dict(result,cycles=result['cycles']//2,ms=result['ms']/2)
 return result
with patch.object(grade,'composed',halved):
 failed=[n for n,ok,_ in selftest.checks() if not ok]
assert 'fixture passes: worst pass and composed maximum' in failed
out['mutants']['halve-composed-maximum']=failed
(p/'delta3-probes.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: independent populations, every capacity recipient, three omissions, halved maximum, shutdown counts and build identity')
