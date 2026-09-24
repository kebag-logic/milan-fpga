#!/usr/bin/env python3
"""Run one foreground command with a generous timeout and retain its exit status."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
name, *command = sys.argv[1:]
env = os.environ.copy()
if 'A288_DOCS_ENV' in env:
    env['PATH'] = str(Path(env['A288_DOCS_ENV']) / 'bin') + ':' + env['PATH']
env['PYTHONUNBUFFERED'] = '1'
start = time.monotonic()
with (out / (name + '.log')).open('w') as log:
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                            env=env, timeout=7200)
meta = {'command': command, 'rc': result.returncode,
        'seconds': round(time.monotonic() - start, 3)}
(out / (name + '.json')).write_text(json.dumps(meta, indent=2) + '\n')
print(json.dumps(meta), flush=True)
lines = (out / (name + '.log')).read_text(errors='replace').splitlines()
print('\n'.join(lines[-14:]), flush=True)
raise SystemExit(result.returncode)
