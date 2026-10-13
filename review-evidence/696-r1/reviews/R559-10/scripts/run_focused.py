#!/usr/bin/env python3
"""Reproduce the bounded review checks in disposable, pinned checkouts.

Usage: python3 scripts/run_focused.py SOURCE PACKET --jobs 3
The process stays in the foreground until every child has completed.
"""
import argparse
import concurrent.futures
import os
from pathlib import Path
import re
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=3, choices=range(1, 4))
p.add_argument('--verilator', default='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
scratch = packet / 'scratch'
receipts = packet / 'receipts'
scratch.mkdir(exist_ok=True)
receipts.mkdir(exist_ok=True)
env = dict(os.environ, VERILATOR=a.verilator, VERILATOR_JOBS='4',
           TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
env['PATH'] = str(Path(a.verilator).parent) + os.pathsep + env['PATH']
env.pop('MAKEFLAGS', None)
env.pop('MFLAGS', None)

def redact(text):
    text = text.replace(str(scratch), '<scratch>').replace(str(source), '<source>')
    text = text.replace(str(packet), '<packet>')
    return re.sub(r'/home/[^/\s]+/[^\s\"\']*?(?=[\s\"\']|$)', '<compiler-runtime-path>', text)

def run(name, command, cwd):
    start = time.monotonic()
    raw = scratch / (name + '.raw.log')
    with raw.open('w') as log:
        log.write('COMMAND: ' + repr(command) + '\n')
        log.flush()
        result = subprocess.run(command, cwd=cwd, env=env, stdout=log,
                                stderr=subprocess.STDOUT, check=False)
        log.write(f'\nEXIT_STATUS={result.returncode}\nELAPSED_SECONDS={time.monotonic()-start:.3f}\n')
    (receipts / (name + '.log')).write_text(redact(raw.read_text(errors='replace')))
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, 'rc', result.returncode, 'seconds', round(time.monotonic()-start, 1), flush=True)
    return result.returncode

root = scratch / 'execution'
if not root.exists():
    assert run('clone', ['git', 'clone', '--shared', '--no-checkout', str(source), str(root)], source) == 0
    assert run('checkout', ['git', 'checkout', '--detach', '313616d1a18549d41907db389d378f0beb9bc543'], root) == 0
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    subprocess.run(['git', 'config', f'submodule.{sub}.url', str(source / sub)], cwd=root, check=True)
assert run('submodules', ['git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '--init', '--jobs', '3',
                         'protocol-processor', 'gptp-processor', 'third_party/verilog-axis'], root) == 0

commands = [
 ('maap-default', ['make', '-j16', '-C', 'tb/verilator/maap', 'all', 'VERILATOR_JOBS=4']),
 ('datapath-legs', ['make', '-j16', '-C', 'tb/verilator/milan_dp', 'ax1x1', 'notify', 'VERILATOR_JOBS=4']),
]
# MAAP has at most two four-compiler builds and the datapath recipe has two:
# at most sixteen concurrent compilation jobs. No synthesis is run.
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results = list(pool.map(lambda item: run(item[0], item[1], root), commands))
results.append(run('lint', ['python3', 'scripts/lint_rtl.py', '--check', '--jobs', '1'], root))
raise SystemExit(int(any(results)))
