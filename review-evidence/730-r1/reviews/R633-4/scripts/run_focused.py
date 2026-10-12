#!/usr/bin/env python3
"""Await foreground, bounded focused checks, each with its own raw receipt."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import time

packet = Path(__file__).resolve().parent.parent
repo = Path(sys.argv[1]).resolve()
sb = ['sh', str(packet / 'scripts/reviewer_sandbox.sh'), str(repo), str(packet)]
checks = {
    'selftest': ['python3', '-I', 'scripts/act_ci.py', '--selftest'],
    'r633-r1-unchanged': ['python3', '-I', '/packet/public-inputs/reviews/R633-1/probe_cpu_ranges.py', '/work'],
    'r633-r1-compatible': ['python3', '-I', '/packet/public-inputs/reviews/R633-2/probe_cpu_ranges_compat.py', '/work'],
    'r633-r2-lifecycle-unchanged': ['python3', '-I', '/packet/public-inputs/reviews/R633-2/probe_lifecycle.py', '/work'],
    'r633-r2-monitor-unchanged': ['python3', '-I', '/packet/public-inputs/reviews/R633-2/probe_monitor.py', '/work'],
    'r632-r3-probe-unchanged': ['python3', '-I', '/packet/scripts/probe_r3.py', '/work', '300'],
    'r632-r2-shutdown-unchanged': ['python3', '-I', '/packet/scripts/probe_shutdown.py', '/work'],
    'slot-proof-selftest': ['bash', 'scripts/act_slot_proof.sh', '--selftest'],
}

def run(item):
    name, args = item
    start = time.monotonic()
    with (packet / 'receipts' / f'{name}.log').open('w') as log:
        result = subprocess.run(sb + args, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (packet / 'receipts' / f'{name}.rc').write_text(f'{result.returncode}\n')
    row = {'name': name, 'command': sb + args, 'rc': result.returncode,
           'seconds': round(time.monotonic() - start, 3)}
    print(json.dumps(row), flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, checks.items()))
(packet / 'receipts/focused.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(0 if all(row['rc'] == (1 if row['name'] == 'r633-r1-unchanged' else 0) for row in results) else 1)
