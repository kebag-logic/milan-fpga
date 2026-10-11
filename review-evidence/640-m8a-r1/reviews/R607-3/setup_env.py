#!/usr/bin/env python3
"""Create an isolated interpreter from the repository pins; run in the foreground."""
import os, pathlib, subprocess, sys
repo=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parent
scratch=packet/'scratch'; venv=scratch/'venv'
env=dict(os.environ,TMPDIR=str(scratch),PIP_CACHE_DIR=str(scratch/'pip-cache'),PYTHONDONTWRITEBYTECODE='1')
with (scratch/'setup.log').open('w') as log:
 def run(args):
  print('COMMAND',args,file=log,flush=True)
  subprocess.run(list(map(str,args)),env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 run([sys.executable,'-m','venv',venv])
 py=venv/'bin/python3'
 run([py,'-m','pip','install','pyyaml','-r',repo/'sw/litex/litex_pins.txt'])
 run([py,repo/'scripts/ci_litex_env.py'])
 env['PYTHON']=str(py)
 run(['bash',repo/'sw/litex/patches/apply.sh'])
 run([py,'-m','pip','freeze'])
print('isolated pinned interpreter ready')
