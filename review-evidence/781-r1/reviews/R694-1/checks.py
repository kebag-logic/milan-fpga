#!/usr/bin/env python3
"""Run bounded review checks in the foreground and retain raw results."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
p.add_argument('name')
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
out = Path(__file__).resolve().parent / 'checks'
out.mkdir(exist_ok=True)
temporary = Path(__file__).resolve().parent / 'scratch' / 'tmp'
temporary.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(temporary))
start = time.time()
with (out / (a.name + '.log')).open('w') as log:
    result = subprocess.run(a.command, cwd=a.root, env=env, stdout=log,
                            stderr=subprocess.STDOUT, timeout=540)
record = dict(command=a.command, cwd=str(a.root), rc=result.returncode,
              elapsed_seconds=round(time.time()-start, 3))
(out / (a.name + '.json')).write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record))
print('\n'.join((out / (a.name + '.log')).read_text().splitlines()[-8:]))
raise SystemExit(result.returncode)
