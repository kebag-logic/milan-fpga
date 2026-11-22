#!/usr/bin/env python3
"""Run focused review checks in foreground, with bounded concurrent children."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
SCRATCH = PACKET / 'scratch'
SCRATCH.mkdir(parents=True, exist_ok=True)
V = os.environ.get('VERILATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(SCRATCH), VERILATOR=V)

def run(name, cmd, cwd=ROOT):
    with (PACKET / (name + '.log')).open('w') as log:
        log.write('COMMAND: ' + repr(cmd) + '\n'); log.flush()
        result = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (PACKET / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, result.returncode, flush=True)
    return result.returncode

flags = '--cc --exe --build -j 4 -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
jobs = [
    ('core-mutants', ['python3', '-B', 'sw/firmware/ctrl/test/gptp_mutants.py', '--jobs', '8', '--build-dir', str(SCRATCH/'core-mutants')], ROOT),
    ('tsu', ['make', '-j16', 'run', 'VERILATOR='+V, 'MDIR='+str(SCRATCH/'tsu'), 'VFLAGS='+flags], ROOT/'tb/verilator/gptp_tsu'),
    ('mailbox-generation', ['python3', '-B', 'sw/mailbox/gen_mailbox.py', '--check', '--crosscheck', '--selftest'], ROOT),
    ('register-generation', ['python3', '-B', 'scripts/gen_register_reference.py', '--check'], ROOT),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    outcomes = list(pool.map(lambda job: run(*job), jobs))
sys.exit(any(outcomes))
