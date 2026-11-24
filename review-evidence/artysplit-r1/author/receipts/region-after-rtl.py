"""Continue the same single test slot after the RTL campaign finishes."""
import json,os,subprocess,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4'); root=Path.cwd()
while not (r/'rtl-fixture-rerun-restoration.log').exists():
 time.sleep(5)
assert len(json.loads((r/'rtl-rerun-results.json').read_text()))==2
env=dict(os.environ,TMPDIR=str(r/'tmp'),PYTHONHASHSEED='0',COURSIER_MODE='offline',SBT_OPTS='-Dsbt.offline=true')
python='<home-path>/litex-milan/venv/bin/python3'
jobs=[('arty-region',[python,'-B','tb/verilator/ctrl_region_decode/run.py','--shape','endstation_arty_split',
                      '--build-dir',str(r/'arty-region'),'--self-test']),
      ('arty-boot-placement',[python,'-B','tb/verilator/ctrl_split_boot/run.py','--shape','endstation_arty_split',
                              '--build-dir',str(r/'arty-boot'),'--placement-controls'])]
records=[]
for name,argv in jobs:
 print('START',name,flush=True)
 with (r/(name+'.log')).open('w') as log:
  proc=subprocess.run(argv,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=10800)
 records.append(dict(name=name,command=argv,returncode=proc.returncode))
 (r/'region-placement-results.json').write_text(json.dumps(records,indent=2)+'\n')
 print('DONE',name,proc.returncode,flush=True)
raise SystemExit(any(x['returncode'] for x in records))
