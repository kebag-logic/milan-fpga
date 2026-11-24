from pathlib import Path
import json,sys,time
ROOT=Path('/data-2/milan/lanes/opt-hart2')
sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import run,scenario
base=Path('/data-2/milan/tmp/opt-a837/scale');pending={'32-d0','32-d8'};deadline=time.monotonic()+3600;bad=False
while pending and time.monotonic()<deadline:
 for arm in sorted(pending):
  d=base/arm;p=d/'results/srp.log'
  with p.open('rb') as f:f.seek(max(0,p.stat().st_size-8000));tail=f.read().decode(errors='replace')
  if 'RESULT:' not in tail:continue
  spec=json.loads((d/'build.json').read_text());point=scenario.point('32x32',spec)
  group=next(g for g in run.all_groups(point,spec) if g.name=='srp')
  out=d/'early-srp';out.mkdir(exist_ok=True)
  results,refusals,misses=run.graded([group],[p],spec,out)
  shares=run.share_misses(results);stated=run.stated_misses(results)
  code=int(bool(refusals or misses or shares or stated));bad=bad or code
  record=dict(arm=arm,scope='EARLY single-group grade; full nine-group run still pending',rc=code,
              refusals=refusals,misses=misses,shares=shares,stated=stated,
              harts=[dict(hart0=g['passes'].get('worst'),hart1=g.get('hart1')) for g in results])
  (out/'grade.json').write_text(json.dumps(record,indent=2)+'\n')
  print(json.dumps(record,indent=2),flush=True);pending.remove(arm)
 if pending:time.sleep(10)
if pending:raise SystemExit('no completed SRP log within the early-grade window')
raise SystemExit(int(bad))
