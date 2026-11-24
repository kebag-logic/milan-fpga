"""Grade each completed native trace once; no process launching or simulation slots."""
import hashlib,json,shutil,sys,time
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tb/verilator/ctrl_service_budget'))
import run,scenario,egress_ledger
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4')
arms=('arm-fast',)
seen={};records=[]
while not (r/'stop-watch').exists():
 for name in arms:
  d=r/name
  if not (d/'build.json').exists():continue
  spec=json.loads((d/'build.json').read_text())
  groups=run.all_groups(scenario.point('arty-1x1',spec),spec)
  out=d/'watch-extra';out.mkdir(exist_ok=True)
  for g in groups:
   path=d/'extra-results'/(g.name+'.log');key=name+'/'+g.name
   if key in seen or not path.exists():continue
   with path.open('rb') as f:
    f.seek(max(0,path.stat().st_size-4000));tail=f.read()
   if b'RESULT: PASS' not in tail:continue
   j=path.with_suffix('.journal')
   if j.exists():shutil.copyfile(j,out/j.name)
   results,refusals,misses=run.graded([g],[path],spec,out)
   share=run.share_misses(results)
   late=run.save_misses(results)+run.burst_misses(results)+run.notice_misses(results,spec['interfaces'])
   forbidden=[]
   for result in results:
    for p in result['probes']:
     if p.get('within_budget',True):continue
     entry={**p,'group':g.name,'exact':True}
     ledger=egress_ledger.LEDGER['arty-1x1']
     if not egress_ledger.is_row(entry,ledger) or egress_ledger.over(entry,ledger[p['probe']]):
      forbidden.append(p)
   row=dict(arm=name,group=g.name,trace_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            refusals=refusals,misses=misses,share=share,late=late,forbidden=forbidden,
            worst_pass_cycles=max([x['passes']['worst']['cycles'] for x in results] or [0]))
   records.append(row);seen[key]=True
   (r/'watch-extra.json').write_text(json.dumps(records,indent=2)+'\n')
   print(json.dumps(row),flush=True)
   if refusals or share or late or forbidden:
    (r/'watch-extra-finding.json').write_text(json.dumps(row,indent=2)+'\n')
    raise SystemExit(2)
 time.sleep(10)
