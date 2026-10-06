#!/usr/bin/env python3
"""Run independent probes concurrently, in an awaited foreground process.

Usage: python3 run_focused.py REPOSITORY PACKET
At most eleven compiler jobs run together (eight codec, two tally, one ADP).
Each campaign has its own log and return-code file.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import subprocess
import sys
import time

root, packet = (Path(p).resolve() for p in sys.argv[1:3])

def run(mode):
    log = packet / 'receipts' / (mode + '.log')
    started = time.monotonic()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUNBUFFERED': '1'}
    with log.open('w') as f:
        res = subprocess.run([sys.executable, str(packet / 'scripts/focused.py'), str(root), str(packet), mode],
                             cwd=root, stdout=f, stderr=subprocess.STDOUT, env=env, timeout=540, check=False)
    (packet / 'receipts' / (mode + '.rc')).write_text(str(res.returncode) + '\n')
    print(f'{mode}: rc={res.returncode}, elapsed={time.monotonic()-started:.1f}s', flush=True)
    return res.returncode

with ThreadPoolExecutor(max_workers=3) as pool:
    codes = list(pool.map(run, ('codec', 'tally', 'adp')))
sys.exit(1 if any(codes) else 0)
