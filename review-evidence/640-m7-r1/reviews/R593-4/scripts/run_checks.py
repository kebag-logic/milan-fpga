#!/usr/bin/env python3
"""Run the bounded round-four checks; all child processes are waited for."""
import argparse
import concurrent.futures
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import time

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--verilator', type=Path, required=True)
ap.add_argument('--m7-only', action='store_true')
a = ap.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
scratch = packet / 'scratch'
receipts = packet / 'receipts'
scratch.mkdir(exist_ok=True)
receipts.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
           VERILATOR=str(a.verilator.resolve()), VERILATOR_JOBS='8', MAKEFLAGS='-j16')
results = {}

def run(name, argv, cwd=repo):
    started = time.monotonic()
    with (receipts / (name + '.log')).open('w') as log:
        log.write('COMMAND: ' + json.dumps(argv) + '\n')
        log.write('CWD: ' + str(cwd.relative_to(packet) if cwd.is_relative_to(packet) else '.') + '\n')
        log.flush()
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    results[name] = {'rc': result.returncode, 'seconds': round(time.monotonic() - started, 2)}
    print(name, results[name], flush=True)
    return result.returncode

def donor(revision, label):
    dest = scratch / ('donor-' + label)
    dest.mkdir(exist_ok=True)
    archive = subprocess.check_output(['git', '-C', str(repo / 'gptp-processor'),
        'archive', revision, 'tb/verilator/parser', 'tb/common', 'hdl', 'syn/ooc'])
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(dest, filter='data')
    run(label + '-clock-source', ['python3', 'syn/ooc/check_ooc_clock.py'], dest)
    run(label + '-clock-controls', ['python3', 'syn/ooc/check_ooc_clock.py', '--selftest'], dest)
    vflags = ('--cc --exe --build -j 2 --top-module KL_gptp_rx_parser '
              '-Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL '
              '-Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM '
              '-CFLAGS "-std=c++17 -O2 -I. -Wall -Wextra"')
    run(label + '-parser', ['make', '-j16', 'run', 'VFLAGS=' + vflags], dest / 'tb/verilator/parser')

def m7():
    sys.path[:0] = [str(repo / 'scripts'), str(repo / 'tb/verilator/gptp_shadow')]
    from owned_process import OwnedProcesses
    from private_inputs import copy_inputs
    dest = scratch / 'm7-baseline'
    dest.mkdir(exist_ok=True)
    suite = repo / 'tb/verilator/gptp_tables'
    with OwnedProcesses() as owner:
        copy_inputs(repo, suite, dest, owner, [])
    run('m7-baseline', ['make', '-j16', 'run'], dest / 'tb/verilator/gptp_tables')
    run('m7-mutations', ['python3', '-u', 'tb/verilator/gptp_tables/mutants.py'])

def quick():
    checks = [
        ('python-idiom', ['python3', 'scripts/check_py_idiom.py']),
        ('cpp-idiom', ['python3', 'scripts/check_cpp_idiom.py']),
        ('limits-table', ['python3', 'scripts/gen_one_valued_table.py', '--check']),
        ('ci-scope', ['python3', 'scripts/ci_scope.py', '--selftest']),
        ('ci-events', ['python3', 'scripts/ci_events.py', '--check']),
        ('submodule-docs', ['python3', 'scripts/check_submodule_docs.py']),
        ('gptp-docs', ['python3', 'scripts/check_gptp_docs.py', '--with-submodule']),
        ('timesync-diagram', ['python3', 'docs/diagrams/timesync_chain.gen.py', '--check']),
        ('rom-generator', ['python3', 'gptp-processor/hdl/ucode/gen_gptp_ucode.py',
                           '-o', str(scratch / 'gptp_ucode.hex')]),
    ]
    for name, argv in checks:
        run(name, argv)

if a.m7_only:
    m7()
    sys.exit(any(r['rc'] for r in results.values()))

run('compiler-identity', [str(a.verilator.resolve()), '--version'])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(donor, '6b5a4282586a3851117674891d1955253e3de452', 'before'),
               pool.submit(donor, 'e4869fd0c42889b2ac806587cc5c78afb1c33461', 'after'),
               pool.submit(run, 'm7-worker', ['python3', str(Path(__file__).resolve()),
                   '--repo', str(repo), '--packet', str(packet),
                   '--verilator', str(a.verilator.resolve()), '--m7-only']),
               pool.submit(quick)]
    for future in futures:
        future.result()
(receipts / 'focused-checks.json').write_text(json.dumps(results, indent=2, sort_keys=True) + '\n')
sys.exit(any(r['rc'] for r in results.values()))
