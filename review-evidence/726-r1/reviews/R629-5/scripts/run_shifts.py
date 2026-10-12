#!/usr/bin/env python3
"""Run the unchanged earlier shift launcher; verify its child's recorded status."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

p = Path(sys.argv[1]).resolve()
def run(item):
    shape, shift = item
    log = p / 'receipts' / f'shift-{shape}-{shift}.log'
    result = subprocess.run(['sh', str(p/'scripts/run_shift.sh'),
                             str(p/'scratch'/f'direct-{shape}'), str(shift), str(log)])
    body = log.read_text()
    assert result.returncode == 0 and body.endswith('rc=0\n') and 'RESULT: PASS' in body and '[FAIL]' not in body
    print(shape, shift, 'PASS', flush=True)
    return dict(shape=shape, shift_cycles=shift, rc=0)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, [(s,t) for s in [1,8] for t in [0,200,300,800,900,1000000]]))
(p/'receipts/shift-results.json').write_text(json.dumps(results, indent=2)+'\n')
