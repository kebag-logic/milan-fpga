#!/usr/bin/env python3
"""Record exact argv, times, exit and raw stdout/stderr for a review command."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
name, *argv = sys.argv[1:]
assert name and '/' not in name
log = out / (name + '.log')
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.monotonic()
env = dict(os.environ, MAKEFLAGS='-j1', PYTHONDONTWRITEBYTECODE='1', GIT_NO_REPLACE_OBJECTS='1')
with log.open('wb') as f:
    result = subprocess.run(['rtk','proxy',*argv], stdout=f, stderr=subprocess.STDOUT, env=env, check=False)
receipt = dict(argv=['rtk','proxy',*argv],cwd=os.getcwd(),start_utc=start,
               duration_seconds=time.monotonic()-t,exit=result.returncode,
               log=log.name,sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
               environment_overrides={k:env[k] for k in ['MAKEFLAGS','PYTHONDONTWRITEBYTECODE','GIT_NO_REPLACE_OBJECTS']})
(out/(name+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
sys.exit(result.returncode)
