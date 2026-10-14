#!/usr/bin/env python3
"""Repeat focused controls with the authenticated image interpreter, without containers."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
packet=Path(__file__).resolve().parent
ref=packet/'scratch/reference-python'
env=dict(os.environ,PYTHONHOME=str(ref/'usr'),
 PYTHONPATH=str(ref/'opt/python/lib/python3.12/site-packages'),PYTHONDONTWRITEBYTECODE='1',
 TMPDIR=str(packet/'scratch'),REVIEW_RECEIPT_PREFIX='reference-')
python=ref/'usr/bin/python3.12'
records=[]
def run(name):
 result=subprocess.run([str(python),str(packet/name),sys.argv[1]],env=env,capture_output=True,text=True,timeout=180)
 output=result.stdout.replace(str(packet/'scratch'),'<scratch>')
 (packet/('reference-'+name.removesuffix('.py')+'.log')).write_text(output+result.stderr.replace(str(packet/'scratch'),'<scratch>'))
 assert result.returncode==0,(name,result.returncode,result.stderr)
 return {'script':name,'rc':result.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 records=list(pool.map(run,['run_checks.py','probe_inventory.py','verify_controls.py']))
(packet/'reference-runs.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records))
