#!/usr/bin/env python3
"""Build and run both disposable probes concurrently; preserve individual statuses."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

p=Path(sys.argv[1]); s=p/'scratch/probes'
env=dict(os.environ,TMPDIR=str(p/'scratch'),PATH=str(p/'scratch/bin')+':'+os.environ['PATH'])
v='VERILATOR='+str(p/'scratch/bin/verilator')
def run(suite,build,run):
    with (p/f'receipts/probe-{suite}.log').open('w') as f:
        rc=subprocess.run(['make','-j16',*build,v],cwd=s/'tb'/suite,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
        if rc==0 and run:
            rc=subprocess.run(run,cwd=s/'tb'/suite,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    (p/f'receipts/probe-{suite}.rc').write_text(str(rc)+'\n')
    print(suite,'rc',rc,flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    a=pool.submit(run,'pp_top',['gsi-build'],['./obj_dir/Vpp_top_sim','--acmp-only'])
    b=pool.submit(run,'srp_stream_fsms',['RUN_ARGS=suite'],[])
    sys.exit(bool(a.result() or b.result()))
