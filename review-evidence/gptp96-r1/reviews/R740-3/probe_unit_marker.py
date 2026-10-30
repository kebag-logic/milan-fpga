#!/usr/bin/env python3
"""Check the documented Meaning-cell unit inference against its comma delimiter."""
from pathlib import Path
import json
import os
import subprocess

P=Path(__file__).resolve().parent
ROOT=P/'scratch/probe-tree'
integration=ROOT/'docs/INTEGRATION.md'
hdl=ROOT/'docs/HDL_DEVELOPER.md'
saved_int=integration.read_bytes();saved_hdl=hdl.read_bytes()
env=dict(os.environ,TMPDIR=str(P/'scratch'),PYTHONDONTWRITEBYTECODE='1')
rows=[]
def run(label):
    cmd=['make','-j16','docs']
    r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
    (P/(label+'.log')).write_text(r.stdout+r.stderr)
    (P/(label+'.rc')).write_text(str(r.returncode)+'\n')
    rows.append({'name':label,'command':cmd,'rc':r.returncode})
try:
    hdl.write_bytes(saved_hdl+b'\nA 375 ms watch.\n')
    run('unit-comma-control')
    text=saved_int.decode()
    assert text.count('syncReceiptTimeout, ms')==1
    integration.write_text(text.replace('syncReceiptTimeout, ms','syncReceiptTimeout ms'))
    run('unit-no-comma')
finally:
    integration.write_bytes(saved_int);hdl.write_bytes(saved_hdl)
run('unit-marker-restored')
(P/'unit-marker-probes.json').write_text(json.dumps(rows,indent=2)+'\n')
assert [r['rc'] for r in rows]==[2,0,0]
assert 'restates SYNC_RTO_MS_C' in (P/'unit-comma-control.log').read_text()
print([(r['name'],r['rc']) for r in rows])
