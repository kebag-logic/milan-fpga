"""Read completed final traces for early cost growth; never claim qualification."""
import datetime,json,subprocess,sys,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');campaign=r/'final-census';out=r/'final-progress'
out.mkdir(exist_ok=True)
seen=set();merged=r/'census-preliminary-complete.json';step=0
def read(path):
 try:return json.loads(path.read_text())
 except (FileNotFoundError,json.JSONDecodeError):return None
while True:
 if (out/'stop-watch').exists():break
 if (campaign/'stop-finding.json').exists():
  print('NATIVE FINDING: inspect final-census/stop-finding.json',flush=True);break
 rows=read(campaign/'completed.json') or []
 pending=[row for row in rows if (row['variant'],row['group']) not in seen]
 manifest=read(campaign/'manifest.json') or {}
 complete=manifest.get('status','').startswith('NATIVE MEASUREMENTS COMPLETE')
 if not pending or (len(pending)<5 and seen and not complete):
  if complete:break
  time.sleep(3);continue
 step+=1;work=out/f'{step:03d}';work.mkdir()
 directories={}
 for row in pending:
  assert row['native_status']==0
  variant=row['variant'];view=work/variant;source=campaign/variant
  if variant not in directories:
   (view/'results').mkdir(parents=True)
   (view/'build.json').symlink_to(source/'build.json')
   directories[variant]=view/'results'
  for suffix in ('.log','.txt','.journal'):
   path=source/'results'/(row['group']+suffix)
   if path.exists():(view/'results'/path.name).symlink_to(path)
 with (work/'census.log').open('w') as log:
  subprocess.run([sys.executable,'-B',str(r/'census.py'),str(work/'census.json'),*map(str,directories.values())],
                 stdout=log,stderr=subprocess.STDOUT,check=True,timeout=10800)
 subprocess.run([sys.executable,'-B',str(r/'merge-census.py'),str(work/'merged.json'),str(merged),str(work/'census.json')],
                stdout=subprocess.DEVNULL,check=True,timeout=600)
 merged=work/'merged.json'
 with (work/'model.json').open('w') as log:
  subprocess.run([sys.executable,'-B',str(r/'derive-own.py'),str(merged)],stdout=log,check=True,timeout=3600)
 model=read(work/'model.json')
 seen|={(row['variant'],row['group']) for row in pending}
 record=dict(status='PARTIAL FINAL COST FORECAST',time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             completed_groups=len(seen),model=str(work/'model.json'),load=model['load'],choices=model['choices'],
             qualification=False)
 (out/'latest.json').write_text(json.dumps(record,indent=2)+'\n')
 print('FORECAST',len(seen),'groups',model['status'],'load',model['load'],
       'txL',model['choices'][0]['rows_ms']['txL'] if model['choices'] else 'NO QUALIFIED CHOICE',flush=True)
 if not model['choices']:
  (out/'owner-finding.json').write_text(json.dumps(record,indent=2)+'\n')
  break
