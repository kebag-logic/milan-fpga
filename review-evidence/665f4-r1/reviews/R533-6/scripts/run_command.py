#!/usr/bin/env python3
"""Run a foreground command with an explicit receipt and time limit."""
import argparse
import json
import os
import subprocess
import time
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('name')
p.add_argument('command', nargs=argparse.REMAINDER)
a=p.parse_args()
packet=Path(__file__).resolve().parents[1]
start=time.monotonic()
env=dict(os.environ, TMPDIR=str(packet/'scratch'), PYTHONDONTWRITEBYTECODE='1')
with (packet/'receipts'/f'{a.name}.log').open('w') as log:
    r=subprocess.run(a.command,stdout=log,stderr=subprocess.STDOUT,env=env,timeout=590)
elapsed=time.monotonic()-start
(packet/'receipts'/f'{a.name}.rc').write_text(f'{r.returncode} {elapsed:.3f}\n')
(packet/'receipts'/f'{a.name}.command.json').write_text(json.dumps(a.command,indent=2)+'\n')
print(a.name, r.returncode, round(elapsed,3))
raise SystemExit(r.returncode)
