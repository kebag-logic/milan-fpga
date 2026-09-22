#!/usr/bin/env python3
"""Run one scoped command and retain argv, raw streams, exit and elapsed time."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
p.add_argument('label')
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
out = Path(__file__).resolve().parent
cmd = a.command[1:] if a.command[0] == '--' else a.command
cmd = ['rtk', 'proxy', *cmd]
start = time.time()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0',
           GIT_NO_REPLACE_OBJECTS='1', MAKEFLAGS='-j8', CMAKE_BUILD_PARALLEL_LEVEL='8',
           OMP_NUM_THREADS='1')
with (out / (a.label + '.stdout')).open('wb') as stdout, (out / (a.label + '.stderr')).open('wb') as stderr:
    result = subprocess.run(cmd, cwd=a.root, env=env, stdout=stdout, stderr=stderr)
receipt = {'command': cmd, 'cwd': str(a.root), 'exit': result.returncode,
           'elapsed_seconds': round(time.time() - start, 3), 'started_epoch': start,
           'source_head': subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(a.root), 'rev-parse', 'HEAD']).decode().strip()}
(out / (a.label + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
print((out / (a.label + '.stdout')).read_text()[-4000:])
print((out / (a.label + '.stderr')).read_text()[-4000:])
raise SystemExit(result.returncode)
