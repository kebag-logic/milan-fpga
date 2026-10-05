#!/usr/bin/env python3
"""Foreground concurrent scoped checks; at most sixteen compilation jobs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import io
import os
from pathlib import Path
import subprocess
import tarfile
import time

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--verilator', type=Path, required=True)
a = ap.parse_args()
a.repo = a.repo.resolve()
a.packet = a.packet.resolve()
scratch = a.packet / 'scratch'
(scratch / 'tmp').mkdir(parents=True, exist_ok=True)
(scratch / 'raw').mkdir(exist_ok=True)
env = {**os.environ, 'TMPDIR': str(scratch / 'tmp'), 'PYTHONDONTWRITEBYTECODE': '1',
       'VERILATOR': str(a.verilator), 'PATH': str(a.verilator.parent) + os.pathsep + os.environ['PATH']}
version = subprocess.check_output([str(a.verilator), '--version'], text=True)
assert version.startswith('Verilator 5.050 '), version
(a.packet / 'receipts' / 'compiler-identity.txt').write_text(version)
copy = scratch / 'cosim-source'
copy.mkdir(exist_ok=True)
archive = subprocess.check_output(['git', 'archive', 'HEAD', 'hdl/milan/mailbox', 'tb/verilator/mbx',
                                  'tb/common', 'sw/firmware/ctrl'], cwd=a.repo)
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
    tf.extractall(copy, filter='data')
vflags = '--cc --exe --build -j 3 --top-module tb_mbx_top -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I' + str(copy / 'sw/firmware/ctrl/mbx') + '"'
tasks = [
 ('firmware', ['python3', '-B', 'sw/firmware/ctrl/test/test_ctrl_firmware.py', '--require-rv32', '--self-test',
               '--build-dir', str(scratch / 'firmware')], a.repo),
 ('mailbox-campaign', ['python3', '-B', str(a.packet / 'scripts/rtl_campaign.py'), '--repo', str(a.repo),
                        '--packet', str(a.packet), '--jobs', '3'], a.repo),
 ('cosim', ['make', '-j16', 'run-cosim', 'VFLAGS=' + vflags], copy / 'tb/verilator/mbx'),
 ('contract', ['python3', '-B', 'sw/mailbox/gen_mailbox.py', '--check', '--crosscheck', '--selftest'], a.repo),
 ('ci-scope', ['python3', '-B', 'scripts/ci_scope.py', '--selftest'], a.repo),
]

def run(task):
    name, argv, cwd = task
    start = time.monotonic()
    raw = scratch / 'raw' / (name + '.log')
    with raw.open('w') as f:
        res = subprocess.run(argv, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=1800)
    log = raw.read_text(errors='replace')
    public = log.replace(str(a.packet), '<packet>').replace(str(a.repo), '<review-root>')
    public = public.replace(str(Path.home()), '<home>')
    (a.packet / 'receipts' / (name + '.log')).write_text(public)
    (a.packet / 'receipts' / (name + '.rc')).write_text(str(res.returncode) + '\n')
    print(f'{name}: rc={res.returncode}, seconds={time.monotonic()-start:.1f}', flush=True)
    return res.returncode

with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
    results = list(pool.map(run, tasks))
raise SystemExit(0 if all(rc == 0 for rc in results) else 1)
