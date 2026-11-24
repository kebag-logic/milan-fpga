"""Reuse two released test slots for the eight remaining notice phases.

The existing queue owns one later-arm slot. Only after both the extra-cost and
RTL/region slots finish does this replace that serial arm with three workers.
The destination arm keeps the fourth slot. Interrupted traces are retained and
excluded, and a finished native phase is reused only with its identical script.
"""
import hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4'); arm=r/'arm-later'; root=Path.cwd()
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import run,scenario
def processes():
 result={}
 for p in Path('/proc').glob('[0-9]*/cmdline'):
  try:args=[a.decode() for a in p.read_bytes().split(b'\0') if a]
  except (OSError,UnicodeDecodeError):continue
  if args:result[int(p.parent.name)]=args
 return result
def running(pid):
 try:return Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()[0]!='Z'
 except OSError:return False
def region_done():
 try:x=json.loads((r/'region-placement-results.json').read_text())
 except (OSError,ValueError):return False
 return len(x)==2 and all(row['returncode']==0 for row in x)
while True:
 procs=processes()
 extra=any('--out' in a and str(r/'arm-fast/extra-results') in a for a in procs.values())
 done=(r/'arm-fast/extra-results/results.json').exists() and not extra
 serial=[pid for pid,a in procs.items() if 'tb/verilator/ctrl_service_budget/run.py' in a
         and '--build-dir' in a and str(arm) in a]
 if done and region_done() and serial:break
 if (r/'arm-later-queued.json').exists() and not serial:
  print('Serial later arm already finished; no reschedule',flush=True);raise SystemExit(0)
 time.sleep(5)
assert len(serial)==1,serial
pid=serial[0]
ppid=int(Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()[1])
assert any(a.endswith('/queue-missing.py') for a in processes().get(ppid,[])),(pid,ppid)
os.kill(pid,signal.SIGTERM)
for _ in range(100):
 if not running(pid):break
 time.sleep(.05)
assert not running(pid),'serial caller did not terminate'
children=[pid for pid,a in processes().items() if a[0]==str(arm/'native/Vsim')]
for pid in children:os.kill(pid,signal.SIGTERM)
for _ in range(100):
 if not any(running(pid) for pid in children):break
 time.sleep(.05)
assert not any(running(pid) for pid in children)
remaining_native=[a for a in processes().values() if a[0].startswith(str(r)) and a[0].endswith('/native/Vsim')]
assert len(remaining_native)<=1 and all(a[0]==str(r/'arm-valid/native/Vsim') for a in remaining_native),remaining_native
spec=json.loads((arm/'build.json').read_text());groups=run.all_groups(scenario.point('arty-1x1',spec),spec)
kept=[];pending=[];saved=[];backup=arm/'interrupted-serial';backup.mkdir(exist_ok=False)
for g in groups:
 log=arm/'results'/(g.name+'.log');script=log.with_suffix('.txt')
 if log.exists():
  with log.open('rb') as f:f.seek(max(0,log.stat().st_size-4000));complete=b'RESULT: PASS' in f.read()
 else:complete=False
 if complete and script.read_text()==g.script():kept.append(g.name);continue
 pending.append(g.name)
 for suffix in ('.txt','.log','.json','.journal'):
  p=log.with_suffix(suffix)
  if p.exists():
   saved.append(dict(file=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
   p.rename(backup/p.name)
record=dict(status='RESCHEDULED; incomplete serial traces excluded',workers=3,kept=kept,pending=pending,
            interrupted=saved,remaining_reserved_slot='valid-destinations')
(r/'later-reschedule.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
argv=[sys.executable,'-B','tb/verilator/ctrl_service_budget/run.py','--point','arty-1x1','--build-dir',str(arm),
      '--reuse-build','--variant','answering-later','--jobs','3','--record-budget-findings','--record-share-findings']
env=dict(os.environ,PYTHONHASHSEED='0',COURSIER_MODE='offline',SBT_OPTS='-Dsbt.offline=true')
if pending:
 with (r/'arm-later-parallel.log').open('w') as log:
  p=subprocess.run([*argv,'--groups',','.join(pending)],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=43200)
 record['measurement_returncode']=p.returncode
with (r/'arm-later-combined.log').open('w') as log:
 p=subprocess.run([*argv,'--regrade'],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=10800)
record.update(status='MEASUREMENTS FINISHED; bootstrap cost statements still unqualified',regrade_returncode=p.returncode)
(r/'later-reschedule.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
