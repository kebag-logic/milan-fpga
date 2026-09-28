"""Run both full builder modes at one committed source head."""
from pathlib import Path
import gzip
import shutil
import hashlib
import json
import os
import subprocess
import time
out=Path(__file__).parent
root=Path.cwd()
assert root==Path('$LANES/590-592-599-firmware')
head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True).strip()
assert not subprocess.check_output(['rtk','proxy','git','diff','--name-only'],text=True).strip()
python='$WORKSPACE_HOME/litex-milan/venv/bin/python'
common=['rtk','proxy','timeout','14400','env','PYTHONHASHSEED=0','PYTHONDONTWRITEBYTECODE=1','PYTHONUNBUFFERED=1',python,'-B']
checks=[('builder-present-with-firmware-census',['sw/builder/test_builder.py','--require-elaboration','--require-rv32']),
        ('builder-absent',[str(out/'full-builder-absent.py')])]
results=[]
for name,args in checks:
    command=common+args
    log=Path('$VALIDATION_STORAGE/590-a411')/('final-'+name+'.log')
    start=time.monotonic()
    with log.open('w') as stream:
        result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT)
    raw=log.read_bytes()
    body=gzip.compress(raw,mtime=0) if len(raw)>200000 else raw
    filename=log.name+('.gz' if len(raw)>200000 else '')
    stored=[]
    for index,start_at in enumerate(range(0,len(body),190000)):
        part=body[start_at:start_at+190000]
        target=out/'logs'/(filename+(f'.part{index:02d}' if len(body)>190000 else ''))
        target.write_bytes(part)
        stored.append(dict(path=str(target.relative_to(out)),size=len(part),sha256=hashlib.sha256(part).hexdigest()))
    results.append(dict(name=name,head=head,command=command,rc=result.returncode,
                        seconds=round(time.monotonic()-start,3),stored=stored,size=len(raw),
                        sha256=hashlib.sha256(raw).hexdigest()))
    (out/'final-builder-gates.json').write_text(json.dumps(results,indent=2)+'\n')
    print(name,result.returncode,flush=True)
assert subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True).strip()==head
assert all(r['rc']==0 for r in results)
