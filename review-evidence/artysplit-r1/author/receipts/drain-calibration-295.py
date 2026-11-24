"""Close admission to the known stale-cost attempt, preserving its active native runs."""
import datetime,json,os,signal,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4'); parent=2799895
proc=Path('/proc')/str(parent)
argv=proc.joinpath('cmdline').read_bytes().split(b'\0')
assert b'$VALIDATION_STORAGE/artysplit-a829/r4/run-final-census.py' in argv
assert not (r/'calibration-drain.json').exists()
os.kill(parent,signal.SIGSTOP)
children=[]
for p in Path('/proc').glob('[0-9]*/stat'):
 try:
  fields=p.read_text().rsplit(') ',1)[1].split()
  if int(fields[1])!=parent:continue
  command=[x.decode() for x in p.with_name('cmdline').read_bytes().split(b'\0') if x]
  assert command and command[0].startswith(str(r/'final-census')) and command[0].endswith('/native/Vsim'),command
  children.append(dict(pid=int(p.parent.name),command=command,script=command[1],state=fields[0]))
 except FileNotFoundError:continue
assert 1<=len(children)<=4,children
record=dict(status='DRAINING CALIBRATION',parent=parent,children=children,
            time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            reason='Measured SRP margin rounds to 300 us; installed 295 us requires a firmware correction. No owner bound failed.',
            admission='Only this supervisor is SIGSTOPped. Its existing foreground native children continue normally; a just-finished group may be awaiting Python grading.')
(r/'calibration-drain.json').write_text(json.dumps(record,indent=2)+'\n')
(r/'final-progress/stop-watch').write_text(record['reason']+'\n')
while True:
 for child in children:
  if 'returncode' in child:continue
  stat=Path('/proc')/str(child['pid'])/'stat'
  fields=stat.read_text().rsplit(') ',1)[1].split()
  child['state']=fields[0]
  if fields[0]=='Z':
   assert len(fields)>=50,fields
   child['wait_status']=int(fields[49])
   child['returncode']=os.waitstatus_to_exitcode(child['wait_status'])
   Path(child['script']).with_suffix('.status').write_text(str(child['returncode'])+'\n')
 record['updated']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 (r/'calibration-drain.json').write_text(json.dumps(record,indent=2)+'\n')
 print('DRAIN',sum('returncode' in c for c in children),'of',len(children),
       [(Path(c['script']).stem,c['state']) for c in children],flush=True)
 if all('returncode' in c for c in children):break
 time.sleep(55)
# All children have exited and their exact wait statuses are recorded. Killing
# the stopped supervisor prevents any queued work from being admitted on resume.
os.kill(parent,signal.SIGKILL)
record['status']='NATIVE DRAIN COMPLETE; CALIBRATION REGRADING REQUIRED'
record['supervisor_exit']='intentional SIGKILL after all native children exited'
(r/'calibration-drain.json').write_text(json.dumps(record,indent=2)+'\n')
assert all(c['returncode']==0 for c in children),record
print(record['status'],flush=True)
