#!/usr/bin/env python3
"""Reproduce independent matrix, composition suite and focused docs checks.

Run after run_focused.py and check_planting.py. All children remain attached and
are waited for. No external service or repository is changed.
"""
import argparse
import concurrent.futures
import os
from pathlib import Path
import shutil
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--jobs',type=int,required=True)
a=p.parse_args()
assert 1<=a.jobs<=4
scratch=a.packet/'scratch'
matrix=scratch/'supplemental-matrix'
notify=scratch/'supplemental-notify'
for tree,suite in [(matrix,'srp_stream_fsms'),(notify,'aecp_notify')]:
    for path in ['hdl','tb/common','tb/'+suite]:
        shutil.copytree(a.source/path,tree/path,dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('obj*','__pycache__'))
shutil.copyfile(a.packet/'scripts/collision_matrix.cpp',matrix/'tb/srp_stream_fsms/collision_matrix.cpp')
env=dict(os.environ,VERILATOR=str(scratch/'limited-simulator'),TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1')
units=[('matrix',['make','-j16','run','CPP=collision_matrix.cpp'],matrix/'tb/srp_stream_fsms'),
       ('notify-composition',['make','-j16','run'],notify/'tb/aecp_notify'),
       ('docs-checks',['make','-j16','ids','figures','links','matrix','modmatrix','params','stale'],a.source)]
def run(unit):
    name,cmd,cwd=unit
    with (a.packet/'receipts'/f'{name}.log').open('w') as log:
        result=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=580)
    (a.packet/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
    print(name,result.returncode,flush=True)
    return result.returncode
with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
    codes=list(pool.map(run,units))
raise SystemExit(any(codes))
