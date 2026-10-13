#!/usr/bin/env python3
"""Run one foreground check; keep the unfiltered log and a portable receipt."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
name, *cmd = sys.argv[1:]
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
           MILAN_RV32_CC=str(scratch / 'rv32-sdk/bin/riscv32-linux-gcc'))
env.pop('MAKEFLAGS', None)
env['PATH'] = str(scratch / 'venv/bin') + os.pathsep + env['PATH']
started = time.monotonic()
with (scratch / (name + '.raw.log')).open('w') as log:
    res = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT)
elapsed = time.monotonic() - started
raw = (scratch / (name + '.raw.log')).read_text(errors='replace')
def public(text):
    return text.replace(str(packet), '$PACKET').replace(str(Path.cwd()), '$REPO').replace(str(Path.home()), '$HOME')
(packet / (name + '.log')).write_text(public(raw))
(packet / (name + '.rc')).write_text(str(res.returncode) + '\n')
(packet / (name + '.json')).write_text(json.dumps({
    'argv': [public(x) for x in cmd], 'rc': res.returncode, 'seconds': round(elapsed, 3),
    'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
    'log_normalization': 'Only checkout, packet and home path prefixes replaced; raw log retained in scratch.'
}, indent=2) + '\n')
print(name, 'rc', res.returncode, 'seconds', round(elapsed, 2), flush=True)
print(public(raw[-1500:]), flush=True)
sys.exit(res.returncode)
