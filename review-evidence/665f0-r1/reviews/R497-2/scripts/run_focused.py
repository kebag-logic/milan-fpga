#!/usr/bin/env python3
"""Run independent focused checks concurrently; keep each command's log and exit code."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import io
import tarfile
import time

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--simulator', type=Path, required=True)
args = ap.parse_args()
repo, packet = args.repo.resolve(), args.packet.resolve()
scratch = packet / 'scratch'
scratch.mkdir(parents=True, exist_ok=True)
(packet / 'receipts').mkdir(parents=True, exist_ok=True)
if not (scratch / 'tree').exists():
    (scratch / 'tree').mkdir()
    archive = subprocess.check_output(['git', 'archive', 'HEAD'], cwd=repo)
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(scratch / 'tree', filter='data')
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
           VERILATOR=str(args.simulator.resolve()))
native = ['python3', '-B', 'sw/firmware/ctrl/test/test_ctrl_firmware.py', '--self-test',
          '--build-dir', str(scratch / 'native')]
recipe = subprocess.check_output(['make', '-s', 'print-vflags'],
    cwd=scratch / 'tree/tb/verilator/mbx', env=env, text=True).splitlines()
# The recipe's -j 0 must not escape the unit's total concurrency budget.
import shlex
flags = recipe[1:] + ['-j', '2']
jobs = [
    ('rtl-campaign', ['python3', '-B', 'tb/verilator/mbx/mutants.py', '--jobs', '3',
                     '--keep', str(scratch / 'rtl-campaign')], repo),
    ('native-campaign', native, repo),
    ('cosimulation', ['make', '-j16', 'run-cosim', 'VFLAGS=' + shlex.join(flags)],
                    scratch / 'tree/tb/verilator/mbx'),
    ('ci-scope', ['python3', '-B', 'scripts/ci_scope.py', '--selftest'], repo),
    ('generator', ['python3', '-B', 'sw/mailbox/gen_mailbox.py', '--check', '--crosscheck', '--selftest'], repo),
]

def run(job):
    name, argv, cwd = job
    start = time.monotonic()
    with (packet / 'receipts' / (name + '.log')).open('w') as log:
        log.write('ARGV: ' + shlex.join(argv) + '\n')
        log.flush()
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (packet / 'receipts' / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(f'{name}: rc={result.returncode} elapsed={time.monotonic()-start:.1f}s', flush=True)
    return result.returncode

# Maximum compiler jobs: 3*4 RTL + 2 co-simulation + 1 native = 15.
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    codes = list(pool.map(run, jobs))
raise SystemExit(int(any(codes)))
