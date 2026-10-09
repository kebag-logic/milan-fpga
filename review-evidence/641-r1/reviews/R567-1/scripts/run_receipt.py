#!/usr/bin/env python3
"""Run one foreground check with raw output and its actual exit status."""
import json, os, pathlib, subprocess, sys, time
packet = pathlib.Path(__file__).resolve().parents[1]
label, *command = sys.argv[1:]
env = dict(os.environ, TMPDIR=str(packet/'scratch'), PYTHONDONTWRITEBYTECODE='1')
start = time.monotonic()
with (packet/'receipts'/f'{label}.log').open('w') as log:
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, env=env)
receipt = dict(command=command, rc=result.returncode, seconds=round(time.monotonic()-start, 3))
(packet/'receipts'/f'{label}.json').write_text(json.dumps(receipt, indent=2)+'\n')
(packet/'receipts'/f'{label}.rc').write_text(str(result.returncode)+'\n')
print(label, json.dumps(receipt), flush=True)
raise SystemExit(result.returncode)
