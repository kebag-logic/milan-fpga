#!/usr/bin/env python3
"""Focused campaigns, joined in the foreground, at most sixteen simulations."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(os.environ['REVIEW_ROOT'])
PACKET = Path(os.environ['REVIEW_PACKET'])
HARNESS = ROOT / 'tb/verilator/ctrl_service_budget'

def campaign(pair):
    name, point = pair
    out = PACKET / 'measurements' / name
    out.mkdir(parents=True, exist_ok=True)
    argv = [sys.executable, '-B', str(HARNESS / 'run.py'), '--point', point,
            '--build-dir', str(PACKET / 'scratch' / name), '--reuse-build', '--jobs', '8',
            '--groups', 'backlog,backlog-adp,backlog-adp-refill,backlog-owed,aecp',
            '--out', str(out), '--record-budget-findings']
    start = time.monotonic()
    with (PACKET / (name + '-delta.log')).open('w') as log:
        rc = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT).returncode
    record = dict(returncode=rc, seconds=round(time.monotonic()-start, 3), groups=argv[-5:])
    (PACKET / (name + '-delta.rc.json')).write_text(json.dumps(record, indent=2)+'\n')
    print(name, record, flush=True)
    return rc

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(campaign, [('A1', '1x1'), ('A8', '8x8')]))
raise SystemExit(bool(any(results)))
