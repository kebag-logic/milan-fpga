#!/usr/bin/env python3
"""Use the selector's documented gh run view log format for measurement."""
import concurrent.futures
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
jobs = [115739516717, 115739516836, 115739516680, 115739516629, 115739516619, 115739516595]

def fetch(job):
    path = packet / 'scratch/hosted' / f'gh-job-{job}.log'
    data = subprocess.check_output(['gh', 'run', 'view', '38529993870', '-R', 'kebag-logic/milan-fpga', '--job', str(job), '--log'])
    path.write_bytes(data)
    return str(path)

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    paths = list(pool.map(fetch, jobs))
sys.exit(subprocess.run(['python3', 'scripts/suite_shards.py', '--measure', *paths], cwd=repo).returncode)
