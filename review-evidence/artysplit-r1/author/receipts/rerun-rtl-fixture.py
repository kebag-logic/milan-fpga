"""One foreground RTL slot, rerunning only the two setup failures."""
import json,os,subprocess
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4'); fixture=r/'rtl-fixture'
env=dict(os.environ,TMPDIR=str(r/'tmp'),MAKEFLAGS='-j1',
         MILAN_LITEX_PYTHON='<home-path>/litex-milan/venv/bin/python3',
         VERILATOR=str(r/'verilator-limited.py'),VERILATOR_JOBS='8',PYTHONHASHSEED='0')
cases=[('milan-dp-latw-rerun',['make','-j1','-C','tb/verilator/milan_dp','gptp-latw'],fixture),
       ('gptp-shadow-mutants-rerun',['python3','mutants.py'],fixture/'tb/verilator/gptp_shadow')]
records=[]
for name,command,cwd in cases:
 print('START',name,flush=True)
 with (r/(name+'.log')).open('w') as log:
  proc=subprocess.run(command,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=21600)
 records.append(dict(case=name,command=command,returncode=proc.returncode))
 (r/'rtl-rerun-results.json').write_text(json.dumps(records,indent=2)+'\n')
 print('DONE',name,proc.returncode,flush=True)
restored=subprocess.run(['git','diff','--exit-code'],cwd=fixture,capture_output=True,text=True)
(r/'rtl-fixture-rerun-restoration.log').write_text(restored.stdout+restored.stderr)
print('RESTORED',restored.returncode==0,flush=True)
raise SystemExit(bool(restored.returncode or any(x['returncode'] for x in records)))
