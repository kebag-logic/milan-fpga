"""Small read-only status view; no waits and no native processes started."""
import datetime,fcntl,json
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4')
print(datetime.datetime.now(datetime.timezone.utc).isoformat())
for p in sorted((r/'final-slots').glob('*.lock')):
 with p.open() as handle:
  try:fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:
   row=json.loads(p.read_text());print('ACTIVE',row['slot'],row['label'],row['started'])
for name in ('final-census-command','final-firmware-0','final-firmware-1','final-firmware-2',
             'final-firmware-3','final-boot','final-boot-controls','final-service-selftest'):
 p=r/(name+'.json')
 if p.exists():
  row=json.loads(p.read_text());print('COMPLETE',name,'rc',row.get('returncode'))
 p=r/(name+'.log')
 if p.exists() and p.stat().st_size:
  if name.startswith('final-firmware-'):
   text=p.read_text();markers=[line for line in text.splitlines() if line.startswith(('[ok]','[FAIL]','RESULT:','ESCAPED'))]
   print('FIRMWARE',name,'passed arms' if name.endswith('-0') else 'caught markers',text.count('[ok]'),'failure markers',text.count('[FAIL]'),
         'last',markers[-1] if markers else 'verdict pending')
   continue
  if name=='final-service-selftest':
   text=p.read_text();markers=[line for line in text.splitlines() if line.startswith(('MUTANT ','FAIL ','RESULT:'))]
   print('GRADER','caught',text.count('MUTANT caught:'),'escaped',text.count('MUTANT ESCAPED:'),
         'last',markers[-1] if markers else 'verdict pending')
   continue
  with p.open('rb') as handle:handle.seek(max(0,p.stat().st_size-800));tail=handle.read().decode(errors='replace')
  lines=[line for line in tail.splitlines() if line.strip()]
  print('TAIL',name,p.stat().st_size,'bytes',lines[-1] if lines else '')
p=r/'final-census/completed.json'
if p.exists():
 rows=json.loads(p.read_text());print('SERVICE',len(rows),'completed; worst',max(x['worst_pass_cycles'] for x in rows),'cycles')
for p in (r/'final-census/stop-finding.json',r/'final-census/qualification.json',r/'identity-final-compare.json'):
 if p.exists():
  row=json.loads(p.read_text());print('RESULT',p.name,row.get('status','FINDING'))
