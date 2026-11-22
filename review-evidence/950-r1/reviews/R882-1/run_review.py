#!/usr/bin/env python3
"""Foreground supervisor: four independent campaigns, <=16 compiler jobs total."""
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
(packet / 'receipts').mkdir(exist_ok=True)
def run(mode):
    log = packet / 'receipts' / (mode + '.log')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
    with log.open('w') as out:
        p = subprocess.run([sys.executable, '-B', str(packet / 'focused.py'), str(repo), str(packet), mode],
                           stdout=out, stderr=subprocess.STDOUT, env=env)
    (packet / 'receipts' / (mode + '.rc')).write_text(str(p.returncode) + '\n')
    print(mode, 'rc', p.returncode, flush=True)
    return p.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, ('head', 'base', 'aecp-plants', 'control-plants')))
raise SystemExit(int(any(results)))
