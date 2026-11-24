"""Redistribute the remaining destination and notice phases across four slots.

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
def completed(path):
 if not path.exists():return False
 with path.open('rb') as f:f.seek(max(0,path.stat().st_size-4000));return b'RESULT: PASS' in f.read()
while True:
 all_declaring=all(completed(r/'arm-declaring/results'/(n+'.log')) for n in ('aecp','aecp-fanout','aecp-largest-notice','aecp-reboot','aecp-outputs'))
 if completed(r/'arm-valid/results/srp-talker.log') and all_declaring and region_done():break
 if (r/'watch-finding.json').exists():raise SystemExit('A measured owner or non-ledger finding needs reporting')
 time.sleep(5)
# Stop the queue itself first, so it cannot launch a later arm while its
# child runners are being collected. Only our exact queue/script paths match.
queues=[pid for pid,a in processes().items() if a[0].endswith('python3') and str(r/'queue-missing.py') in a]
assert len(queues)==1,queues
os.kill(queues[0],signal.SIGTERM)
for _ in range(100):
 if not running(queues[0]):break
 time.sleep(.05)
assert not running(queues[0])
serial=[pid for pid,a in processes().items() if 'tb/verilator/ctrl_service_budget/run.py' in a
        and '--build-dir' in a and any(str(r/name) in a for name in ('arm-valid','arm-later','arm-declaring'))]
for pid in serial:os.kill(pid,signal.SIGTERM)
for _ in range(100):
 if not any(running(pid) for pid in serial):break
 time.sleep(.05)
assert not any(running(pid) for pid in serial)
children=[pid for pid,a in processes().items() if a[0] in [str(r/name/'native/Vsim') for name in ('arm-valid','arm-later','arm-declaring')]]
for pid in children:os.kill(pid,signal.SIGTERM)
for _ in range(100):
 if not any(running(pid) for pid in children):break
 time.sleep(.05)
assert not any(running(pid) for pid in children)
remaining_native=[a for a in processes().values() if a[0].startswith(str(r)) and a[0].endswith('/native/Vsim')]
assert not remaining_native,remaining_native
kept=[];pending=[];saved=[];groups_by_arm={};specs={}
for name in ('arm-valid','arm-later','arm-declaring'):
 arm=r/name
 spec=json.loads((arm/'build.json').read_text());specs[name]=spec
 groups=run.all_groups(scenario.point('arty-1x1',spec),spec);groups_by_arm[name]=groups
 backup=arm/'interrupted-serial';backup.mkdir(exist_ok=False)
 for g in groups:
  log=arm/'results'/(g.name+'.log');script=log.with_suffix('.txt')
  if completed(log) and script.read_text()==g.script():kept.append([name,g.name]);continue
  pending.append((name,g))
  for suffix in ('.txt','.log','.json','.journal'):
   p=log.with_suffix(suffix)
   if p.exists():
    saved.append(dict(arm=name,file=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    p.rename(backup/p.name)
record=dict(status='RESCHEDULED; incomplete serial traces excluded',workers=4,kept=kept,
            pending=[[n,g.name] for n,g in pending],interrupted=saved)
(r/'remaining-reschedule.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
import concurrent.futures
pending.sort(key=lambda item:item[1].sim_ms,reverse=True)
def one(item):
 name,g=item;arm=r/name
 print('START',name,g.name,flush=True)
 path=run.run_group(arm,arm/'results',g,specs[name].get('flash_image') or '-')
 results,refusals,misses=run.graded([g],[path],specs[name],arm/'results')
 shares=run.share_misses(results)
 late=run.save_misses(results)+run.burst_misses(results)+run.notice_misses(results,1)
 if refusals or shares or misses or late:
  for pid,args in processes().items():
   if args[0] in [str(r/n/'native/Vsim') for n in groups_by_arm]:os.kill(pid,signal.SIGTERM)
  (r/'remaining-finding.json').write_text(json.dumps(dict(arm=name,group=g.name,refusals=refusals,misses=misses,share=shares,late=late),indent=2)+'\n')
 print('DONE',name,g.name,len(refusals),len(misses),len(shares),len(late),flush=True)
 return [name,g.name]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:record['completed']=list(pool.map(one,pending))
for name in groups_by_arm:
 argv=[sys.executable,'-B','tb/verilator/ctrl_service_budget/run.py','--point','arty-1x1','--build-dir',str(r/name),
       '--reuse-build','--variant',specs[name]['variant'],'--regrade','--record-budget-findings','--record-share-findings']
 with (r/(name+'-combined.log')).open('w') as log:
  p=subprocess.run(argv,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=10800)
 record[name+'_regrade_returncode']=p.returncode
record['status']='MEASUREMENTS FINISHED; bootstrap cost statements still unqualified'
(r/'remaining-reschedule.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
