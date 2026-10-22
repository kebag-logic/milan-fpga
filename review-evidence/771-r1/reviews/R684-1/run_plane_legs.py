#!/usr/bin/env python3
"""Run just the two adopted plane-on datapath legs, with bounded compilers."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
compiler = sys.argv[2]
packet = Path(__file__).resolve().parent
assert root.is_relative_to(packet / 'scratch'), 'use only a disposable clone'
suite = root / 'tb/verilator/milan_dp'
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
# One make owns shared generated prerequisites; its two build targets run concurrently.
command = ['make', '-j16', '-C', str(suite), 'build-gptp', 'build-gptp-lat',
           'VERILATOR=' + compiler, 'VERILATOR_JOBS=4']
with (packet / 'scratch/plane-build.log').open('wb') as log:
    build = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
(packet / 'plane-build.rc').write_text(str(build.returncode) + '\n')
assert build.returncode == 0

def run(name):
    command = ['make', '-j16', '--no-print-directory', 'exec-' + name]
    with (packet / ('plane-' + name + '.log')).open('wb') as log:
        p = subprocess.run(command, cwd=suite, env=env, stdout=log, stderr=subprocess.STDOUT,
                           timeout=300)
    (packet / ('plane-' + name + '.rc')).write_text(str(p.returncode) + '\n')
    return name, p.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = dict(pool.map(run, ['gptp', 'gptp-lat']))
(packet / 'plane-results.json').write_text(json.dumps(results, indent=2) + '\n')
print(results)
assert not any(results.values())
