#!/usr/bin/env python3
"""Instrument disposable recipes while preserving the submitted make graph."""
import argparse,json,os,pathlib,re,subprocess,sys
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args()
root=a.packet/"scratch/schedule-probes";root.mkdir(exist_ok=True)
original=(a.source/"tb/verilator/follow_ring/Makefile").read_text()
pattern=r"^((build|b8|pullin|small-pullin|settle-control):[^\n]*\n)(?:\t[^\n]*\n)+"
modified,n=re.subn(pattern,lambda m:m[1]+"\tpython3 action.py "+m[2]+"\n",original,flags=re.M)
assert n==5
(root/"Makefile").write_text(modified)
(root/"action.py").write_text("""import fcntl,json,os,sys,time
name=sys.argv[1]
def emit(event):
 with open('events.jsonl','a') as f:
  fcntl.flock(f,fcntl.LOCK_EX);f.write(json.dumps(dict(target=name,event=event,time=time.monotonic()))+'\\n');f.flush()
emit('start');time.sleep(.1);emit('end');raise SystemExit(1 if os.environ.get('PROBE_FAIL')==name else 0)
""")
results=[]
for parallel in (False,True):
 for fault in ("", "build","b8","pullin","small-pullin","settle-control"):
  name=("parallel" if parallel else "serial")+"-"+(fault or "positive")
  events=root/"events.jsonl";events.unlink(missing_ok=True)
  env=os.environ.copy();env.pop("MAKEFLAGS",None);env["PROBE_FAIL"]=fault
  cmd=["make"]+(["-j16"] if parallel else [])
  r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True)
  out=a.packet/"receipts/schedule";out.mkdir(exist_ok=True)
  (out/(name+".log")).write_text(r.stdout+r.stderr)
  records=[json.loads(s) for s in events.read_text().splitlines()]
  (out/(name+".events.json")).write_text(json.dumps(records,indent=2)+"\n")
  starts=[e['target'] for e in records if e['event']=='start']
  assert starts.count('build')==1,(name,starts)
  assert (r.returncode==0)==(not fault),(name,r.returncode)
  if not fault:assert set(starts)=={'build','b8','pullin','small-pullin','settle-control'}
  active=maximum=0
  for e in sorted(records,key=lambda e:e['time']):
   if e['target']=='build':continue
   active+=1 if e['event']=='start' else -1;maximum=max(maximum,active)
  assert maximum<=4
  row=dict(case=name,rc=r.returncode,shared_builds=starts.count('build'),maximum_leg_actions=maximum);results.append(row);print(json.dumps(row))
(a.packet/"receipts/schedule/results.json").write_text(json.dumps(results,indent=2)+"\n")
print('PASS: graph retains one shared build, bounded leg dispatch and all failure statuses')
