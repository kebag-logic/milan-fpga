#!/usr/bin/env python3
"""Reproduce the bounded, foreground source review checks in disposable trees."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--simulator', type=Path, required=True)
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
scratch = packet / 'scratch'
receipts = packet / 'receipts'
scratch.mkdir(exist_ok=True, parents=True)
receipts.mkdir(exist_ok=True, parents=True)
head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
assert head == '9050c4bbd25556929a0f24fb98258bc98e3bcfbe', head
version = subprocess.check_output([str(a.simulator), '--version'], text=True)
assert 'Verilator 5.050' in version, version
(receipts / 'simulator-identity.txt').write_text(version)
archive = scratch / 'source.tar'
with archive.open('wb') as out:
    subprocess.run(['git', '-C', str(source), 'archive', head], stdout=out, check=True)
for name in ['suite', 'campaign']:
    dest = scratch / name
    dest.mkdir(exist_ok=True)
    with tarfile.open(archive) as t:
        t.extractall(dest, filter='data')
wrapper = scratch / 'bounded-simulator'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\n'
                   + 'exe=' + repr(str(a.simulator.resolve())) + '\n'
                   + 'args=sys.argv[1:]\n'
                   + 'if "--build" in args: args += ["-j", "1"]\n'
                   + 'os.execv(exe,[exe]+args)\n')
wrapper.chmod(0o755)
env = os.environ.copy()
env.update(VERILATOR=str(wrapper), TMPDIR=str(scratch), MAKEFLAGS='-j16')
arms = 'lv-second-lv-ends,lv-never-ends,lv-expiry-masked,lv-expiry-last,lv-expiry-dropped,lv-sweep-misses-collision'
tasks = [
    ('srp-top', ['make', '-j16', '-C', 'tb/srp_top', 'run'], scratch / 'suite'),
    ('stream-fsms', ['make', '-j16', '-C', 'tb/srp_stream_fsms', 'RUN_ARGS=suite'], scratch / 'suite'),
    ('lv-mutants', ['python3', 'tb/srp_top/mutants.py', '--jobs', '4', '--only', arms,
                    '--output', str(receipts / 'lv-mutants')], scratch / 'campaign'),
]
def run(task):
    name, cmd, cwd = task
    start = time.monotonic()
    with (receipts / (name + '.log')).open('w') as log:
        result = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    record = dict(name=name, command=cmd, head=head, rc=result.returncode,
                  seconds=round(time.monotonic()-start, 2))
    (receipts / (name + '.json')).write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record), flush=True)
    return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, tasks))
raise SystemExit(any(results))
