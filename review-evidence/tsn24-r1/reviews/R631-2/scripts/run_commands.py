#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run independent commands concurrently, retaining logs and return codes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--plan', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--jobs', type=int, default=2)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=True)
env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}

def run(row):
    started = time.time()
    with (a.out / (row['name'] + '.log')).open('w') as log:
        rc = subprocess.run(row['argv'], cwd=row.get('cwd'), env=env,
                            stdout=log, stderr=subprocess.STDOUT).returncode
    (a.out / (row['name'] + '.rc')).write_text(str(rc) + '\n')
    result = dict(row, rc=rc, elapsed_seconds=round(time.time() - started, 3))
    print(json.dumps(result), flush=True)
    return result

with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results = list(pool.map(run, json.loads(a.plan.read_text())))
(a.out / 'commands.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(any(r['rc'] != 0 for r in results))
