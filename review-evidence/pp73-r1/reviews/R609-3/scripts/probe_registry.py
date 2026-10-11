#!/usr/bin/env python3
"""Independent boundary probes for record steps and exhaustive registry errors."""
import argparse,copy,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();sys.dont_write_bytecode=True;sys.path.insert(0,str(a.root/'scripts'))
from aecp_gate.inputs import load,DOC
from aecp_gate.gate import check
from aecp_gate.doc import regenerated
base=load(a.root);assert not check(base);count=0
for name in ['ADD_AUDIO_MAPPINGS','REMOVE_AUDIO_MAPPINGS']:
 for side in ['command','response']:
  for step in [0,None,-1,True,1.5]:
   i=copy.deepcopy(base);c=next(x for x in i.table['commands'] if x['name']==name);c[side]['per']=step
   got=check(i);named=[x for x in got if name in x and side+' per must' in x]
   assert named,(name,side,step,got);count+=1;print(name,side,'per',repr(step),'REFUSED',named[0])
 for step in [1,2,4,16]:
  i=copy.deepcopy(base);c=next(x for x in i.table['commands'] if x['name']==name)
  c['command']['per']=c['response']['per']=step;i.texts[DOC]=regenerated(i.table,i.texts[DOC]);got=check(i)
  assert any(name in x and 'gcd' in x for x in got),(name,step,got)
  count+=1;print(name,'echo step',step,'REFUSED by exact gcd')
i=copy.deepcopy(base);i.table['commands'][0]['command']['review_extra']=1;got=check(i)
assert any('commands[].command.review_extra: table field missing from registry' in x for x in got);print('Unknown nested table leaf: REFUSED by path');count+=1
i=copy.deepcopy(base);i.registry.append(dict(path='commands[].review_absent',status='held to nothing',reason='probe'));got=check(i)
assert any('commands[].review_absent: registry entry has no such table field' in x for x in got);print('Absent registry leaf: REFUSED by path');count+=1
print('PASS',count,'independent registry/step probes')
