#!/usr/bin/env python3
"""Focused portable grading checks; no simulation or image build."""
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
commands={
 'harness-selftest':['tb/verilator/ctrl_service_budget/run.py','--self-test','--jobs','4'],
 'load':['tb/verilator/ctrl_service_budget/load_grade.py','--check'],
 'flip-1x1':['tb/verilator/ctrl_service_budget/flip_grade.py','--check','--point','1x1/1if'],
 'flip-8x8':['tb/verilator/ctrl_service_budget/flip_grade.py','--check','--point','8x8/1if'],
 'shape':['tb/verilator/ctrl_service_budget/shape_costs.py','--check'],
}
def run(row):
    name,args=row
    env={**os.environ,'TMPDIR':str(packet/'scratch')}
    with (packet/(name+'.log')).open('w') as f:
        try:
            rc=subprocess.run([sys.executable,'-B',*args],cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=500).returncode
        except subprocess.TimeoutExpired:
            rc=124
            f.write('\nREVIEW RUNNER: 500-second limit reached; no completed verdict.\n')
    (packet/(name+'.rc')).write_text(str(rc)+'\n')
    print(f'{name}: rc {rc}',flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run,commands.items()))
raise SystemExit(bool(any(results)))
