"""Measure both full MRPDUs in the labelled admission fixture, after destination slots are released."""
import hashlib,json,os,sys,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');root=Path.cwd()
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build,run,scenario

def natives():
 found=[]
 for p in Path('/proc').glob('[0-9]*/cmdline'):
  try:a=p.read_bytes().split(b'\0')
  except OSError:continue
  if a and a[0].startswith(str(r).encode()) and a[0].endswith(b'/native/Vsim'):found.append(a[0].decode())
 return found

def complete(name):
 p=r/'arm-valid/results'/(name+'.log')
 if not p.exists():return False
 with p.open('rb') as f:f.seek(max(0,p.stat().st_size-4000));return b'RESULT: PASS' in f.read()
while True:
 if any((r/name).exists() for name in ('watch-finding.json','remaining-finding.json')):raise SystemExit('refused: a measured finding needs resolution')
 active=natives()
 if all(complete(n) for n in ('srp-talker-loss','srp-talker-held')) and str(r/'arm-valid/native/Vsim') not in active:break
 time.sleep(5)
assert len(active)<=2 and all(n==str(r/'arm-later/native/Vsim') for n in active),active
arm=r/'arm-two';spec=build.reused(arm);assert spec['mutation']=='arty-measure-two-mrpdus'
g=next(g for g in run.all_groups(scenario.point('arty-1x1',spec),spec) if g.name=='srp-talker-held')
out=arm/'held-results';out.mkdir(exist_ok=False)
log=run.run_group(arm,out,g,'-')
results,refusals,misses=run.graded([g],[log],spec,out)
shares=run.share_misses(results);late=run.save_misses(results)+run.burst_misses(results)+run.notice_misses(results,1)
record=run.summary('arty-1x1',spec['executable_sha256'],results,refusals,misses,shares)
record.update(trace_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),measurement_fixture='Full licensed Talker and registered Listener declarations; provisional admission fixture, not final image qualification',late=late)
(out/'results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(refusals=refusals,misses=misses,share=shares,late=late)),flush=True)
raise SystemExit(bool(refusals or misses or shares or late))
