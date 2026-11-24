"""One foreground RTL leg; mutation controls affect only the disposable input fixture."""
import json,os,subprocess
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4'); fixture=r/'rtl-fixture'
temporary=r/'tmp';temporary.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(temporary),MAKEFLAGS='-j1',
         MILAN_LITEX_PYTHON='<home-path>/litex-milan/venv/bin/python3',
         VERILATOR=str(r/'verilator-limited.py'),VERILATOR_JOBS='8',PYTHONHASHSEED='0')
cases=[('gptp-txts',['make','-j1','-C','tb/verilator/gptp_txts']),
       ('milan-dp-latw',['make','-j1','-C','tb/verilator/milan_dp','gptp-latw']),
       ('gptp-shadow',['make','-j1','-C','tb/verilator/gptp_shadow'])]
records=[]
for name,command in cases:
 print('START',name,flush=True)
 with (r/(name+'.log')).open('w') as log:
  proc=subprocess.run(command,cwd=fixture,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=21600)
 record=dict(case=name,command=command,returncode=proc.returncode)
 records.append(record)
 (r/'rtl-results.json').write_text(json.dumps(records,indent=2)+'\n')
 print('DONE',name,proc.returncode,flush=True)
 # A failing case does not prevent the other affected suites from running.
restored=subprocess.run(['git','diff','--exit-code'],cwd=fixture,capture_output=True,text=True)
(r/'rtl-fixture-restoration.log').write_text(restored.stdout+restored.stderr)
print('RESTORED',restored.returncode==0,flush=True)
raise SystemExit(bool(restored.returncode or any(x['returncode'] for x in records)))
