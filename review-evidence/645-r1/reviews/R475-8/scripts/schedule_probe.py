#!/usr/bin/env python3
"""Exercise the unchanged Makefile with disposable instrumented workers."""
import argparse,json,os,pathlib,subprocess,sys
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args()
root=a.packet/"receipts/schedule";root.mkdir(parents=True,exist_ok=True)
scratch=a.packet/"scratch/schedule";scratch.mkdir(exist_ok=True)
worker=scratch/"worker.py"
worker.write_text(r'''#!/usr/bin/python3
import fcntl,json,os,pathlib,sys,time
args=sys.argv[1:];base=pathlib.Path(os.environ['PROBE_ROOT'])
def mark(kind,name):
 with (base/'events.jsonl').open('a') as f:
  fcntl.flock(f,fcntl.LOCK_EX);f.write(json.dumps({'kind':kind,'name':name,'time':time.monotonic(),'pid':os.getpid()})+'\n')
if '-Mdir' in args:
 dest=pathlib.Path(args[args.index('-Mdir')+1]);dest.mkdir(exist_ok=True,parents=True)
 name='fine-build' if str(dest).endswith('_fine') else 'shared-build'
 mark('start',name);time.sleep(.05)
 binary=dest/'Vfollow_ring';binary.write_text('#!/bin/sh\nexec /usr/bin/python3 "'+__file__+'" "$@"\n');binary.chmod(0o755)
 mark('end',name)
elif args[0]=='dp_glue.py':
 pathlib.Path(args[2]).write_text('fixture')
else:
 if args[0]=='small_pulls.py':name='small-pullin'
 elif args[0]=='settle_control.py':name='settle-control'
 else:name=args[args.index('--case')+1]
 mark('start',name);time.sleep(.4);mark('end',name)
 if os.environ.get('PROBE_FAIL')==name:raise SystemExit(19)
''')
worker.chmod(0o755);bindir=scratch/'bin';bindir.mkdir(exist_ok=True);(bindir/'python3').symlink_to(worker)
results=[]
for parallel in [False,True]:
 for failure in ['', 'b8','pullin','small-pullin','settle-control']:
  name=('outer-j16' if parallel else 'serial')+'-'+(failure or 'clean');work=scratch/name;work.mkdir()
  (work/'Makefile').write_bytes((a.source/'tb/verilator/follow_ring/Makefile').read_bytes())
  env={**os.environ,'PATH':str(bindir)+':'+os.environ['PATH'],'VERILATOR':str(worker),'PROBE_ROOT':str(work),'PROBE_FAIL':failure};env.pop('MAKEFLAGS',None);env.pop('MFLAGS',None)
  cmd=['timeout','10','make']+(['-j16'] if parallel else [])+['-C',str(work)]
  r=subprocess.run(cmd,env=env,text=True,capture_output=True)
  events=[json.loads(line) for line in (work/'events.jsonl').read_text().splitlines()]
  starts=[x['name'] for x in events if x['kind']=='start'];active=0;peak=0
  for e in sorted(events,key=lambda e:e['time']):
   if e['name'] in ['b8','pullin','small-pullin','settle-control']:
    active+=1 if e['kind']=='start' else -1;peak=max(peak,active)
  shared_end=next(e['time'] for e in events if e['name']=='shared-build' and e['kind']=='end')
  consumers_after=all(e['time']>shared_end for e in events if e['name'] in ['b8','pullin'] and e['kind']=='start')
  good=(r.returncode!=0 if failure else r.returncode==0) and starts.count('shared-build')==1 and starts.count('fine-build')==1 and set(starts)=={'shared-build','fine-build','b8','pullin','small-pullin','settle-control'} and peak==4 and active==0 and consumers_after
  result={'name':name,'rc':r.returncode,'peak_legs':peak,'shared_builds':starts.count('shared-build'),'fine_builds':starts.count('fine-build'),'consumers_after_build':consumers_after,'pass':good}
  results.append(result);print(json.dumps(result),flush=True)
  (root/(name+'.log')).write_text(r.stdout+r.stderr);(root/(name+'.events.json')).write_text(json.dumps(events,indent=2)+'\n');(root/(name+'.command.json')).write_text(json.dumps(cmd)+'\n')
(root/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(int(not all(r['pass'] for r in results)))
