#!/usr/bin/env python3
"""Reproduce focused source checks. Consumer setup is documented in REPORT.md."""
import concurrent.futures
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
p=Path(__file__).resolve().parents[1]
root=Path(sys.argv[1]).resolve()
assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()=='51f88c7e14e7e2527c09ff9a23b93dd6b857fd50'
(p/'scratch').mkdir(exist_ok=True); (p/'receipts').mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(p/'scratch'),MAKEFLAGS='-j16',PYTHONDONTWRITEBYTECODE='1')
sim=str(p/'scripts/limited-simulator.py')
os.chmod(sim,0o755)
copy=p/'scratch/decode'
if not copy.exists(): subprocess.run(['git','clone','--no-hardlinks','--quiet',str(root),str(copy)],check=True)
m=runpy.run_path(str(root/'tb/pp_top/notify_mutants.py'))
names=[x.name for x in m['MUTANTS'] if x.suite==m['NOTIFY']]
assert len(names)==22
def run(tag,argv,cwd):
    with (p/'receipts'/f'{tag}.log').open('w') as f:
        f.write(json.dumps(argv)+'\n');f.flush()
        rc=subprocess.run(argv,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    (p/'receipts'/f'{tag}.rc').write_text(str(rc)+'\n')
    print(tag,rc,flush=True)
    return rc
jobs=[
 ('notify-campaign',['python3','-B','tb/pp_top/notify_mutants.py','--jobs','2','--output',str(p/'receipts/notify'),'--verilator',sim,'--only']+names,root),
 ('d3-final',['python3','-B',str(p/'scripts/d3_final.py'),str(root),'--jobs','4'],root),
 ('decode-sweep',['make','-j16','-C','tb/aecp_cmds','run','VERILATOR='+sim],copy),
 ('command-gate',['make','-j16','aecpcmd'],copy),
]
with concurrent.futures.ThreadPoolExecutor(len(jobs)) as pool:
    results=list(pool.map(lambda j:run(*j),jobs))
raise SystemExit(any(results))
