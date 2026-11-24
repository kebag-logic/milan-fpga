from pathlib import Path
import argparse,datetime,json,sys,time
ROOT=Path('/data-2/milan/lanes/opt-hart2');sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import run,scenario
base=Path('/data-2/milan/tmp/opt-a837/scale');done=set();deadline=time.monotonic()+18000
wanted={'srp','backlog-owed','backlog-adp-refill','control','adp-link','acmp-noresp','maap','aecp','acmp-notk'}
args=argparse.Namespace(cpu_regions='cover',mutation='none',record_budget_findings=True,record_share_findings=True)
while len(done)<18 and time.monotonic()<deadline:
 for arm in ('32-d0','32-d8'):
  d=base/arm;spec=json.loads((d/'build.json').read_text());point=scenario.point('32x32',spec)
  groups={g.name:g for g in run.all_groups(point,spec) if g.name in wanted}
  for name in sorted(wanted):
   if (arm,name) in done:continue
   p=d/'results'/f'{name}.log'
   if not p.exists():continue
   with p.open('rb') as f:f.seek(max(0,p.stat().st_size-8000));tail=f.read().decode(errors='replace')
   if 'RESULT:' not in tail:continue
   out=d/'group-grades';out.mkdir(exist_ok=True);group=groups[name]
   results,refusals,misses=run.graded([group],[p],spec,out);shares=run.share_misses(results)
   late=run.save_misses(results)+run.burst_misses(results)+run.notice_misses(results,2)+run.stated_misses(results)
   rc=run.verdict(args,[group],refusals,misses,shares,late)
   timings=[]
   for g in results:
    h1=g.get('hart1',{});h0=g['passes'];sh=h0.get('share',{})
    timings.append(dict(hart0_cycles=max((h0.get('worst') or {}).get('cycles',0),sh.get('idle_longest',0)),
                       hart1_cycles=max((h1.get('worst') or {}).get('cycles',0),h1.get('idle_max',0))))
   r=dict(arm=arm,group=name,at=datetime.datetime.now(datetime.timezone.utc).isoformat(),grader_rc=rc,
          flags='record-budget-findings and record-share-findings; rc is not a waiver of those findings',
          refusals=refusals,budget_misses=misses,share_misses=shares,other_findings=late,timings=timings,
          native_verdict='PASS' if 'RESULT: PASS' in tail else 'FAIL')
   (out/f'{name}-verdict.json').write_text(json.dumps(r,indent=2)+'\n')
   print(json.dumps({k:r[k] for k in ('arm','group','grader_rc','native_verdict','timings')}),flush=True)
   done.add((arm,name))
 if len(done)<18:time.sleep(15)
if len(done)<18:raise SystemExit('timed out awaiting completed groups')
print('All 18 individual record-mode grader receipts written.')
