#!/usr/bin/env python3
"""Complete the default suites' supplementary shapes after run_focused.py."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
p=argparse.ArgumentParser()
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--jobs',type=int,required=True)
a=p.parse_args()
assert 1<=a.jobs<=4
s=a.packet/'scratch'
env=dict(os.environ,VERILATOR=str(s/'limited-simulator'),TMPDIR=str(s),PYTHONDONTWRITEBYTECODE='1')
units=[(n,'srp_top','storage') for n in ['top-default','second-lv-default','never-ends-default']]
units.append(('fsm-default','srp_stream_fsms','walk'))
def run(unit):
    name,suite,group=unit
    label=name+'-'+group
    log=a.packet/'receipts/focused'/f'{label}.log'
    with log.open('w') as out:
        r=subprocess.run(['make','-j16','all','RUN_ARGS='+group],cwd=s/name/'tb'/suite,
                         env=env,stdout=out,stderr=subprocess.STDOUT,timeout=580)
    (log.with_suffix('.rc')).write_text(str(r.returncode)+'\n')
    tallies=[l for l in log.read_text().splitlines() if 'checks:' in l]
    print(label,r.returncode,tallies,flush=True)
    return r.returncode
with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool: codes=list(pool.map(run,units))
raise SystemExit(any(codes))
