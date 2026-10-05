#!/usr/bin/env python3
"""Save raw execution output from every already-built RTL control/mutant."""
import argparse
import concurrent.futures
from pathlib import Path
import sys
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--jobs', type=int, default=8)
args = ap.parse_args()
repo, packet = args.repo.resolve(), args.packet.resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / 'tb/verilator/mbx'))
import mutants

jobs = [('control-' + str(host), host, None) for host in (0, 1)]
jobs += [(arm.name, arm.host, arm.needle) for arm in mutants.ARMS]
def run(spec):
    name, host, needle = spec
    exe = packet / 'scratch/rtl-campaign' / name / 'obj/Vmbx'
    r = subprocess.run([str(exe), str(host)], capture_output=True, text=True)
    log = r.stdout + r.stderr
    (packet / 'receipts' / ('rtl-' + name + '.log')).write_text(log)
    (packet / 'receipts' / ('rtl-' + name + '.rc')).write_text(str(r.returncode) + '\n')
    ok = r.returncode == (0 if needle is None else 1)
    if needle is not None:
        ok &= any('[FAIL]' in line and needle in line for line in log.splitlines())
    print(f'{name}: rc={r.returncode}, named expectation={ok}', flush=True)
    return ok
with concurrent.futures.ThreadPoolExecutor(max_workers=min(16, max(1, args.jobs))) as pool:
    results = list(pool.map(run, jobs))
raise SystemExit(int(not all(results)))
