#!/usr/bin/env python3
"""Run one foreground validation with direct file output and its real status."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
label, *command = sys.argv[1:]
env = dict(os.environ)
env['PATH'] = '$VALIDATION_TOOLS/verilator-v5.050/bin:' + env['PATH']
started = time.monotonic()
print(f'{label}: {shlex.join(command)}', flush=True)
with (out / f'{label}.log').open('w') as log:
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                            env=env, timeout=7200)
elapsed = time.monotonic() - started
(out / f'{label}.rc').write_text(f'{result.returncode}\n')
(out / f'{label}.json').write_text(json.dumps({
    'command': command, 'cwd': os.getcwd(), 'rc': result.returncode,
    'elapsed_seconds': elapsed, 'timeout_seconds': 7200,
    'path_prefix': '$VALIDATION_TOOLS/verilator-v5.050/bin',
    'output': f'{label}.log', 'piped': False,
}, indent=2) + '\n')
print(f'{label}: rc {result.returncode}, {elapsed:.1f}s; {out / (label + ".log")}', flush=True)
print((out / f'{label}.log').read_text(), end='')
sys.exit(result.returncode)
