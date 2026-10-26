#!/usr/bin/env python3
"""Regrade byte-identical prior public stimulus and raw traces with the current head."""
import hashlib,json,os,sys
from pathlib import Path
p=Path(os.environ['REVIEW_PACKET']);root=Path(os.environ['REVIEW_ROOT'])
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import scenario,grade
out={}
for label,point in [('A1','1x1'),('A8','8x8')]:
 spec=json.loads((p/'scratch'/label/'build.json').read_text())
 groups={g.name:g for g in scenario.all_groups(scenario.point(point,spec),spec)}
 for name in ('backlog','backlog-adp','backlog-adp-refill','aecp'):
  folder=p/'scratch/public/reviews/R704-2/measurements'/label
  old=(folder/(name+'.txt')).read_bytes();assert old==groups[name].script().encode(),(label,name)
  raw=(folder/(name+'.log')).read_bytes()
  got=grade.grade(raw.decode(),groups[name],100000000,50000000)
  expected=json.loads((p/'scratch/public/author-r3/receipts/runs'/label/(name+'.json')).read_text())
  assert got==expected,(label,name)
  out[label+'/'+name]=dict(script_sha256=hashlib.sha256(old).hexdigest(),log_sha256=hashlib.sha256(raw).hexdigest(),exact_match=True,
   composed=got['passes']['composed'],srp=[r for r in got['probes'] if '.service.srp.' in r['probe']])
(p/'unchanged-regrade.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:',len(out),'unchanged public scripts/traces reproduce current results exactly')
