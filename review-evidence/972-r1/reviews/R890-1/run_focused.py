#!/usr/bin/env python3
"""Foreground coordinator: at most four checks, two compiler jobs each."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parent
checkout = Path(sys.argv[1]).resolve()
tasks = sys.argv[2:] or ['adp', 'plat1', 'plat2', 'adp-plants', 'phy-plants', 'forced-head', 'forced-base']
(packet / 'receipts').mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
def run(task):
    cmd = [sys.executable, '-B', str(packet / 'focused.py'), str(checkout), str(packet), task, '--jobs', '2']
    with (packet / 'receipts' / (task + '.log')).open('w') as log:
        r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)
    (packet / 'receipts' / (task + '.rc')).write_text(str(r.returncode) + '\n')
    return task, r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for f in concurrent.futures.as_completed([pool.submit(run, t) for t in tasks]):
        print(*f.result(), flush=True)
