#!/usr/bin/env python3
"""Await the two unchanged public campaigns concurrently, eight workers each."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import time

p = Path(__file__).resolve().parent.parent

def run(round_number):
    name = f'mutants-r{round_number}-unchanged'
    command = ['python3', '-I', str(p / f'scripts/mutants_r{round_number}.py'),
               str(p), str(p / 'scratch/pristine'), '--jobs', '8']
    started = time.monotonic()
    with (p / 'receipts' / f'{name}.log').open('w') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (p / 'receipts' / f'{name}.rc').write_text(f'{result.returncode}\n')
    row = {'name':name, 'command':command, 'rc':result.returncode,
           'seconds':round(time.monotonic()-started,3)}
    print(json.dumps(row), flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    rows = list(pool.map(run, (2,3)))
(p / 'receipts/mutation-campaigns.json').write_text(json.dumps(rows, indent=2)+'\n')
sys.exit(0 if all(r['rc']==0 for r in rows) else 1)
