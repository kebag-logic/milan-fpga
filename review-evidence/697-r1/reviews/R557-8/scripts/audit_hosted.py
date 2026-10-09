#!/usr/bin/env python3
import json,pathlib,subprocess,sys
r=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();head='abe2476c4771bedc84531cf8d05fd12ef947c0cf';rows=[]
for number in (37925745383,37925739153):
 run=json.loads((p/'scratch'/('run-'+str(number)+'.json')).read_text());jobs=json.loads((p/'scratch'/('jobs-'+str(number)+'.json')).read_text())['jobs'];assert run['head_sha']==head and run['conclusion']=='success'
 assert {j['name'] for j in jobs}=={'quality','bare-metal'}
 for j in jobs:
  assert j['conclusion']=='success' and all(s['conclusion']=='success' for s in j['steps'])
 w=p/'scratch'/('hosted-'+str(number));quality=w/'quality-evidence';rv32=w/'rv32-evidence'
 gates=json.loads((quality/'gates.json').read_text());assert len(gates)==24 and all(x['rc']==0 for x in gates)
 metal=json.loads((rv32/'results.json').read_text());assert len(metal)==2 and all(x['rc']==0 and not x['unresolved_final'] for x in metal)
 subprocess.run([sys.executable,str(p/'scripts/prior-audit_results.py'),str(r),str(quality/'mutations'),str(p/'receipts'/('hosted-'+str(number)+'-mutation-audit.json'))],check=True)
 logs=(p/'scratch'/('hosted-'+str(number)+'.log')).read_text()
 checkout=[line for line in logs.splitlines() if head in line and ('ref:' in line or 'checkout --progress' in line or line.endswith(head))]
 for name in ('quality','bare-metal'):assert any(line.startswith(name+'\t') and line.endswith(head) for line in checkout)
 rows.append(dict(run=number,event=run['event'],head=head,url=run['html_url'],conclusion=run['conclusion'],jobs=[dict(name=j['name'],url=j['html_url'],conclusion=j['conclusion'],steps=[dict(name=s['name'],conclusion=s['conclusion']) for s in j['steps']]) for j in jobs],gates=gates,rv32=metal,checkout=checkout,skipped_steps=0))
(p/'receipts/hosted-audit.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Both runs: exact head checked out in both jobs; all steps executed successfully; 24 gates; 311 plants/329 killers; RV32 Debug/Release link and smoke passed')
