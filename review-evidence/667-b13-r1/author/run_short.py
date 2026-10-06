"""One hundred two-second talker starts, supervised in the foreground."""
import json,sys,time
from run_b13 import OUT,RAW,Probe,caps,finish_caps,emit,ledger

def main():
 for stem in ('probe.jsonl','probe.stderr'):
  p=RAW/stem
  if p.exists():p.rename(RAW/('soak-'+stem))
 pr=None;active=[];rows=[]
 try:
  pr=Probe();ready=pr.wait(lambda r:r.get('ev')=='both_online',110)
  if not ready or not ready['ok']:raise RuntimeError('both entities not online')
  for n in range(1,101):
   tag=f'start-{n:03d}';active=caps(tag);ledger(tag,0,'RUNNING');begin=len(pr.events);t0=time.monotonic()
   pr.send(f'cycle {tag} B 0 0 2000 1200 500')
   result=pr.wait(lambda r:r.get('ev')=='cycle_end' and r.get('tag')==tag,18)
   elapsed=time.monotonic()-t0
   finish_caps(active);active=[]
   events=pr.events[begin:]
   polls=[r for r in events if r.get('ev')=='poll' and r.get('tag')==tag]
   # Listener counters reset at bind. The largest bound observation retains
   # a startup increment even when the application callback arrives later.
   post=[r for r in polls if r['phase']!='pre-bind']
   if any(not r['status'].startswith('Success') for r in polls):raise RuntimeError('counter read failed')
   early=max((r['counters'].get('EARLY',0) for r in post),default=None)
   late=max((r['counters'].get('LATE',0) for r in post),default=None)
   row={'cycle':tag,'result':result,'early':early,'late':late,'polls':polls,'formats':[r for r in events if r.get('ev') in ('formats','set_listener_format')],'bind_unbind':[r for r in events if r.get('ev') in ('bind','unbind')]}
   (OUT/(tag+'.json')).write_text(json.dumps(row,indent=2)+'\n');rows.append({'cycle':tag,'early':early,'late':late,'result':result})
   ledger(tag,elapsed,f'EARLY {early}; LATE {late}');emit(event='short_cycle',cycle=tag,early=early,late=late,result=result)
   if not result or result['result']!='OK':raise RuntimeError('short cycle failed')
 finally:
  try:
   if pr:pr.quit()
  finally:
   if active:finish_caps(active)
  (OUT/'short-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
 return 0
if __name__=='__main__':sys.exit(main())
