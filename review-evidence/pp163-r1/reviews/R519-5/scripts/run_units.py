#!/usr/bin/env python3
"""Run the three focused shared-service suites in a foreground disposable tree."""
import json
import os
from pathlib import Path
import subprocess
import time
packet = Path(__file__).resolve().parents[1]
env = os.environ.copy()
env['TMPDIR'] = str(packet/'scratch')
records=[]
for suite in ('tx_arbiter','originator','aecp_notify'):
    argv=['make','-j16','VERILATOR='+str(packet/'scripts/compiler_bound.py')]
    start=time.monotonic()
    with (packet/'receipts/runs'/f'{suite}.log').open('w') as log:
        rc=subprocess.run(argv,cwd=packet/'scratch/golden/tb'/suite,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (packet/'receipts/runs'/f'{suite}.rc').write_text(str(rc)+'\n')
    row={'suite':suite,'rc':rc,'seconds':round(time.monotonic()-start,2)}
    records.append(row)
    print(json.dumps(row),flush=True)
(packet/'receipts/runs/units.json').write_text(json.dumps(records,indent=2)+'\n')
