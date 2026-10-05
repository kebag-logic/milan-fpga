#!/usr/bin/env python3
"""Run one foreground command, preserving its output, status and elapsed time."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--cwd', type=Path, required=True)
p.add_argument('--name', required=True)
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
cmd = a.command[1:] if a.command[:1] == ['--'] else a.command
env = os.environ.copy()
env['TMPDIR'] = str(a.packet / 'scratch')
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['PATH'] = str(a.packet / 'scratch/venv/bin') + os.pathsep + env['PATH']
env['MAKEFLAGS'] = '-j16'
start = time.monotonic()
with (a.packet / 'receipts' / (a.name + '.log')).open('w') as log:
    log.write(json.dumps({'command': cmd, 'cwd': str(a.cwd)}) + '\n')
    log.flush()
    result = subprocess.run(cmd, cwd=a.cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
elapsed = round(time.monotonic() - start, 3)
(a.packet / 'receipts' / (a.name + '.rc')).write_text(str(result.returncode) + '\n')
(a.packet / 'receipts' / (a.name + '.time')).write_text(str(elapsed) + '\n')
print(f'{a.name}: rc={result.returncode}, elapsed={elapsed}s', flush=True)
raise SystemExit(result.returncode)
