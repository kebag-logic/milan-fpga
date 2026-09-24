#!/usr/bin/env python3
"""Run one foreground command with a two-hour limit and retain its exit code."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
name, cwd, *command = sys.argv[1:]
os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:8])
start = time.monotonic()
with (out / (name + '.log')).open('w') as log:
    try:
        result = subprocess.run(command, cwd=cwd, stdout=log,
                                stderr=subprocess.STDOUT, timeout=7200,
                                check=False)
        rc = result.returncode
    except subprocess.TimeoutExpired:
        rc = 124
record = {'name': name, 'cwd': cwd, 'command': command, 'rc': rc,
          'seconds': round(time.monotonic() - start, 2)}
with (out / 'gates.jsonl').open('a') as ledger:
    ledger.write(json.dumps(record) + '\n')
print(json.dumps(record), flush=True)
print('\n'.join((out / (name + '.log')).read_text(errors='replace').splitlines()[-15:]))
raise SystemExit(rc)
