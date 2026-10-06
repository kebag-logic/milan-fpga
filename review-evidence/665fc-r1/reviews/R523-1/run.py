#!/usr/bin/env python3
"""Run one foreground command with separate stdout/stderr log and exit receipt.
Usage: python3 run.py LABEL CWD COMMAND [ARG ...]
All temporary files go under the packet scratch directory.
"""
import os,sys,subprocess,json,time
from pathlib import Path
p=Path(__file__).resolve().parent
label,cwd,*cmd=sys.argv[1:]
env=os.environ.copy()
env.update(TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',PYTHON_CPU_COUNT='4')
start=time.time()
(p/(label+'.command.json')).write_text(json.dumps({'cwd':cwd,'argv':cmd,'environment':{k:env[k] for k in ('TMPDIR','PYTHONDONTWRITEBYTECODE','PYTHONUNBUFFERED','PYTHON_CPU_COUNT')}},indent=2)+'\n')
with (p/(label+'.log')).open('w') as log:
 rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(p/(label+'.rc')).write_text(str(rc)+'\n')
print(f'{label}: rc={rc}, elapsed={time.time()-start:.1f}s')
print('\n'.join((p/(label+'.log')).read_text(errors='replace').splitlines()[-12:]))
sys.exit(rc)
