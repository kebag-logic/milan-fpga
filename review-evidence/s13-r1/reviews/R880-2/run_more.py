#!/usr/bin/env python3
import concurrent.futures, os, pathlib, subprocess, sys
repo,out=map(pathlib.Path,sys.argv[1:]); py=os.environ.get('LITEX_PYTHON',sys.executable)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(out/'scratch'),PYTHONHASHSEED='0')
jobs={'focused-delta':['python3','-B',str(out/'focused_delta.py'),str(repo),str(out/'scratch/prepare')],
 'register-equipped':[py,'-B','scripts/gen_register_reference.py','--check'],
 'register-selftest-equipped':[py,'-B','scripts/gen_register_reference.py','--selftest']}
def run(item):
 name,cmd=item
 with (out/(name+'.log')).open('w') as f:
  f.write('COMMAND '+repr(cmd)+'\n'); f.flush(); rc=subprocess.run(cmd,cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (out/(name+'.rc')).write_text(str(rc)+'\n'); print(name,rc,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: list(pool.map(run,jobs.items()))
