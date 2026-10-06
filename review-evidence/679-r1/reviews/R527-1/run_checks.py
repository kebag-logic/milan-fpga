#!/usr/bin/env python3
"""Foreground supervisor: bounded concurrent commands, individual raw logs and rc files."""
import concurrent.futures
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
phase = sys.argv[3]
scratch = packet / 'scratch'
env = {**os.environ, 'TMPDIR': str(scratch), 'PYTHONDONTWRITEBYTECODE': '1',
       'MILAN_RV32_CC': str(scratch / 'sdk/bin/riscv32-linux-gcc'),
       'PYTHONUNBUFFERED': '1', 'MAKEFLAGS': '-j16'}
phases = {
    'controls': [
        ('rv32-controls', ['python3', 'sw/firmware/gtest/fw_rv32_selftest.py', '--require-rv32'], 2),
        ('ci-events-check', ['python3', 'scripts/ci_events.py', '--check'], 1),
        ('ci-events-selftest', ['python3', 'scripts/ci_events.py', '--selftest'], 1),
        ('ci-scope-selftest', ['python3', 'scripts/ci_scope.py', '--selftest'], 1),
        ('coverage-selftest', ['python3', 'sw/firmware/gtest/fw_coverage.py', '--selftest'], 1),
        ('sdk-selftest', ['python3', 'scripts/ci_rv32_sdk_selftest.py'], 1),
        ('tally-selftest', ['python3', 'sw/firmware/gtest/tally_selftest.py', '--mutants'], 2),
    ],
    'firmware': [
        ('ctrl-suite-mutants', ['python3', 'sw/firmware/ctrl/test/test_ctrl_firmware.py', '--require-rv32', '--self-test', '--build-dir', str(scratch / 'ctrl')], 4),
        ('nvm-suite-mutants', ['python3', str(packet / 'public-evidence/author/nvm_foreground.py')], 4),
        ('coverage', ['python3', 'sw/firmware/gtest/fw_coverage.py', '--check', '--jobs', '4', '--keep', str(scratch / 'coverage')], 4),
    ],
}

def run(item):
    name, argv, jobs = item
    start = time.monotonic()
    with (packet / (name + '.log')).open('w') as log:
        child = subprocess.Popen(argv, cwd=root, env={**env, 'PYTHON_CPU_COUNT': str(jobs)},
                                 stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            rc = child.wait(timeout=570)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
            rc = 124
            log.write('\nREVIEW SUPERVISOR: 570-second command limit reached; incomplete run.\n')
    (packet / (name + '.rc')).write_text(str(rc) + '\n')
    row = {'name': name, 'argv': argv, 'cpu_count': jobs, 'returncode': rc,
           'elapsed_seconds': round(time.monotonic() - start, 3)}
    print(json.dumps(row), flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=len(phases[phase])) as pool:
    result = list(pool.map(run, phases[phase]))
(packet / (phase + '-commands.json')).write_text(json.dumps(result, indent=2) + '\n')
sys.exit(any(x['returncode'] for x in result))
