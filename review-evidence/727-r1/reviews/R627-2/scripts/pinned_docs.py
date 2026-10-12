#!/usr/bin/env python3
"""Run renderer-dependent gates with the isolated pinned environment."""
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import subprocess
import sys
root,packet=map(lambda p:Path(p).resolve(),sys.argv[1:])
python=packet/'scratch/markdown-env/bin/python'
env=dict(os.environ,TMPDIR=str(packet/'scratch'),PYTHONDONTWRITEBYTECODE='1')
commands={'toc-pinned':[str(python),'scripts/gen_toc.py','--check'],
          'em-dash-pinned':[str(python),'scripts/check_em_dash.py','--base','c6bd08c6']}
def run(item):
 name,cmd=item
 result=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=540)
 (packet/'receipts'/(name+'.log')).write_text(result.stdout+result.stderr)
 (packet/'receipts'/(name+'.rc')).write_text(str(result.returncode)+'\n')
 return name,result.returncode
with ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,commands.items()))
for name,rc in results: print(name,rc)
sys.exit(1 if any(rc for _,rc in results) else 0)
