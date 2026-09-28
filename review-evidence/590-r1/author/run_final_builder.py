"""Run both full builder modes at one committed source head."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time
out=Path(__file__).parent
root=Path.cwd()
assert root==Path('$LANES/590-592-599-firmware')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert not subprocess.check_output(['git','diff','--name-only'],text=True).strip()
python='$WORKSPACE_HOME/litex-milan/venv/bin/python'
common=['rtk','proxy','timeout','14400','env','PYTHONHASHSEED=0','PYTHONDONTWRITEBYTECODE=1','PYTHONUNBUFFERED=1',python,'-B']
checks=[('builder-present-with-firmware-census',['sw/builder/test_builder.py','--require-elaboration','--require-rv32']),
        ('builder-absent',[str(out/'full-builder-absent.py')])]
results=[]
for name,args in checks:
    command=common+args
    log=Path('/tmp/a385-final-'+name+'.log')
    start=time.monotonic()
    with log.open('w') as stream:
        result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT)
    results.append(dict(name=name,head=head,command=command,rc=result.returncode,
                        seconds=round(time.monotonic()-start,3),path=str(log),size=log.stat().st_size,
                        sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
    (out/'final-builder-gates.json').write_text(json.dumps(results,indent=2)+'\n')
    print(name,result.returncode,flush=True)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==head
assert all(r['rc']==0 for r in results)
