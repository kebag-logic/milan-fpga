#!/usr/bin/env python3
"""Compare current verdicts with immutable public round-2 receipts."""
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);raw=p/'scratch/raw';pub=p/'public-inputs/reviews'
def rows(path):
 d=json.loads(path.read_text());return d.get('results',d.get('rows'))
pairs=[('r316-'+m,pub/'R316-2/receipts'/('r2set-head-'+m+'.json'),'id') for m in ('sdk','absent')]
for c in ('r2','r2b','r2c','r2d','r2e'):
 for m in ('sdk','absent'):
  old=pub/'R317-2/receipts/probes-r2'/(c+'-head-'+m+'.json')
  if old.exists():pairs.append(('public-cases_544_'+c+'-'+m,old,'label'))
changes={}
for name,old,key in pairs:
 current=raw/(name+'.json')
 if not current.exists():continue
 previous={r[key]:r for r in rows(old)};now={r[key]:r for r in rows(current)}
 assert previous.keys()==now.keys(),name
 changed=[dict(case=k,before=r['verdict'],after=now[k]['verdict'],reason=now[k].get('reason')) for k,r in previous.items() if r['verdict']!=now[k]['verdict']]
 if name.endswith('absent'):assert not changed,name
 else:
  for r in changed:assert r['before']=='ACCEPTED' and r['after']=='REFUSED' and r['reason'].startswith('boot-unit asm allowlist rule'),(name,r)
 changes[name]=dict(rows=len(now),changes=changed)
summary=dict(compared_configurations=len(changes),comparisons=changes)
(raw/'probe-delta.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
