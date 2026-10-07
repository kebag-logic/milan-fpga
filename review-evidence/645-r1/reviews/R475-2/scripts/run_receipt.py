#!/usr/bin/env python3
"""Run one foreground command, retaining its command, output and return code."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('--packet', type=Path, default=Path(__file__).resolve().parents[1])
p.add_argument('--cwd', type=Path, required=True)
p.add_argument('name')
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
out = a.packet / 'receipts' / a.name
out.parent.mkdir(parents=True, exist_ok=True)
cmd = a.command[1:] if a.command[:1] == ['--'] else a.command
out.with_suffix('.command.json').write_text(json.dumps({'cwd':str(a.cwd), 'argv':cmd}, indent=2)+'\n')
start = time.monotonic()
with out.with_suffix('.log').open('w') as f:
    rc = subprocess.run(cmd, cwd=a.cwd, stdout=f, stderr=subprocess.STDOUT).returncode
out.with_suffix('.rc').write_text(str(rc)+'\n')
out.with_suffix('.elapsed').write_text(f'{time.monotonic()-start:.3f}\n')
print(f'{a.name}: rc={rc}, seconds={time.monotonic()-start:.3f}', flush=True)
sys.exit(rc)
