from pathlib import Path
import argparse, hashlib, json, sys
ROOT=Path('/data-2/milan/lanes/opt-hart2')
sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import run, scenario
base=Path('/data-2/milan/tmp/opt-a837/scale')
rows=[]
args=argparse.Namespace(cpu_regions='cover',mutation='none',record_budget_findings=False,record_share_findings=False)
for arm in ('32-d0','32-d8'):
 b=base/arm; spec=json.loads((b/'build.json').read_text())
 group=next(g for g in run.all_groups(scenario.point('32x32',spec),spec) if g.name=='srp')
 original=b/'results/srp.log'; text=original.read_text()
 out=base/'trace-controls'/arm;out.mkdir(parents=True,exist_ok=True)
 for plant,body in [('clean',text),('removed-hart1-observations','\n'.join(line for line in text.splitlines() if not line.startswith('H1'))+'\n')]:
  log=out/(plant+'.log');log.write_text(body)
  results,refusals,misses=run.graded([group],[log],spec,out)
  shares=run.share_misses(results)
  late=run.save_misses(results)+run.burst_misses(results)+run.notice_misses(results,2)+run.stated_misses(results)
  rc=run.verdict(args,[group],refusals,misses,shares,late)
  expected=0 if plant=='clean' else 1
  ok=rc==expected and (plant=='clean' or any('no executing hart 1' in x for x in refusals))
  rows.append(dict(arm=arm,plant=plant,grader_rc=rc,expected_rc=expected,passed=ok,refusals=refusals,
                   source_sha256=hashlib.sha256(text.encode()).hexdigest(),plant_sha256=hashlib.sha256(body.encode()).hexdigest()))
  log.unlink()
result=dict(scope='Actual completed 32x32 SRP traces; observation-deletion plant, not a rebuilt physical core removal',checks=rows,failures=sum(not r['passed'] for r in rows))
(base/'trace-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));raise SystemExit(bool(result['failures']))
