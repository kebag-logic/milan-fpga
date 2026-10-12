#!/usr/bin/env python3
"""Reproduce the two focused clean runs; all children are awaited."""
import concurrent.futures
import os
from pathlib import Path
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
compiler = Path(sys.argv[2]).resolve()
packet = Path(__file__).resolve().parents[1]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
version = subprocess.check_output([str(compiler), '--version'], text=True)
assert 'Verilator 5.050 ' in version, version
print(version.strip())

def run(kind):
    build = packet / 'scratch' / kind
    build.mkdir(parents=True, exist_ok=True)
    target, variable = ('run', 'MDIR') if kind == 'unit' else ('integration-build', 'DP_MDIR')
    cmd = ['make', '-j16', '-C', str(repo / 'tb/verilator/maap'), target,
           f'VERILATOR={compiler}', 'VERILATOR_JOBS=8', f'{variable}={build}']
    raw = packet / 'scratch' / f'{kind}-reproduction-raw.log'
    with raw.open('w') as log:
        result = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
        if kind == 'integration' and result.returncode == 0:
            result = subprocess.run([str(build / 'maap_integration')], cwd=build, env=env,
                                    stdout=log, stderr=subprocess.STDOUT, timeout=540)
    out = re.sub(r'/home/[^\s/]+/\.local/share/containers/storage/overlay/[^\s/]+/diff',
                 '<compiler-install>', raw.read_text())
    (packet / 'receipts' / f'{kind}-reproduction.log').write_text(out)
    (packet / 'receipts' / f'{kind}-reproduction.rc').write_text(str(result.returncode) + '\n')
    print(kind, 'rc', result.returncode, flush=True)
    return result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, ('unit', 'integration')))
sys.exit(int(any(results)))
