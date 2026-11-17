#!/usr/bin/env python3
"""Collect finished round-4 legs. Refuse a missing exit record; omit large raw files by identity."""
from pathlib import Path
import hashlib,json,sys
scratch,out=map(Path,sys.argv[1:3])
seeds=['10092','10592','11102','11602','12102','12602','13102','13602','14602','15032']
legs=[('s'+n,scratch/f'seeds/b4-sync-{n}') for n in seeds]+[(n,scratch/'r4'/b) for n,b in [('p81','b81'),('v1','b1x1-V'),('v81','b81-V')]]
manifest=[]
for tag,build in legs:
 logtag='p81-required' if tag=='p81' else tag
 resultdir=build/('required-results' if tag=='p81' else 'results')
 rc=scratch/f'r4/logs/{logtag}.log.rc'
 assert rc.is_file(),f'{tag}: no recorded rc'
 dest=out/'budget/legs'/tag;dest.mkdir(parents=True,exist_ok=True)
 paths=[scratch/f'r4/logs/{logtag}.log',rc,build/'build.json',*resultdir.glob('*.json'),*resultdir.glob('*.txt'),*resultdir.glob('*.log')]
 for p in paths:
  data=p.read_bytes();large=len(data)>200000
  manifest.append(dict(leg=tag,file=str(p.relative_to(scratch)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),copied=not large,stored_file=None if large else str((dest/p.name).relative_to(out))))
  if not large:(dest/p.name).write_bytes(data)
  elif p.suffix=='.log':
   text=data.decode(errors='replace');lines=text.splitlines()
   selected=[x for x in lines if x.startswith('PARTICIPANT ') or (x.startswith('ENTRY ') and ' on_la_timer ' in x) or x.startswith('RESULT:') or x.startswith('== ctrl_service_budget:')]
   (dest/(p.stem+'.owner-extract.txt')).write_text('Exact selected lines from raw log; all PARTICIPANT bindings and LeaveAll expiry entries, plus final verdict. Full raw log omitted: over 200 KB.\nRaw bytes: '+str(len(data))+'\nRaw sha256: '+hashlib.sha256(data).hexdigest()+'\n\n'+'\n'.join(selected)+'\n')
(out/'budget/raw-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(len(legs),'finished legs collected;',len(manifest),'raw artifact identities')
