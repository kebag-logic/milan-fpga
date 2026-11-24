"""Read completed final traces for early cost growth; never claim qualification."""
import datetime,json,math,subprocess,sys,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected');campaign=r/'final-census';out=r/'final-progress'
out.mkdir(exist_ok=True)
seen=set();merged=r/'census-preliminary-complete.json';step=0
sys.path.insert(0,str(Path.cwd()/'tb/verilator/ctrl_service_budget'))
import shape_costs
installed=shape_costs.at(shape_costs.Shape(1,1,2),Path.cwd())
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
 if not pending:
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
 if model['choices']:
  choice=model['choices'][0];costs=model['costs']
  wanted=dict(CTRL_LOOP_SLICE_US=choice['slice_us'],CTRL_LOOP_BUILD_PASS_US=costs['build'],
   CTRL_LOOP_BUILD_ONE_PASS_US=costs['build_one'],CTRL_LOOP_SRP_UNIT_US=costs['record.srp'],
   CTRL_LOOP_RETRY_COLD_US=model['retry_us'][0],CTRL_LOOP_RETRY_ATTEMPT_US=model['retry_us'][1],
   CTRL_LOOP_QUEUED_MS=choice['queued_ms'],CTRL_LOOP_TX_MS=math.ceil(choice['rows_ms']['tx']-1e-9),CTRL_LOOP_STEP_PASS_US=costs['step'],
   CTRL_LOOP_TICK_US=costs['centisecond'],AECP_NOTICE_US=model['retry_us'][2],AECP_PACE_MS=choice['pace_ms'])
  changes={key:dict(installed=installed[key],measured=value) for key,value in wanted.items() if installed[key]!=value}
  if changes:
   record['firmware_changes']=changes
   (campaign/'cost-adjustment-needed.json').write_text(json.dumps(record,indent=2)+'\n')
   print('FIRMWARE COST ADJUSTMENT REQUIRED',changes,flush=True)
   break
 if not model['choices']:
  (out/'owner-finding.json').write_text(json.dumps(record,indent=2)+'\n')
  break
