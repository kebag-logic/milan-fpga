#!/usr/bin/env python3
"""Foreground concurrent focused verification; no broad banks or hosted writes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--compiler', type=Path, required=True)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    scratch = packet / 'scratch'
    scratch.mkdir(exist_ok=True)
    work = scratch / 'exact-tree'
    if not work.exists():
        shutil.copytree(args.source, work, symlinks=True)
    env = dict(os.environ, VERILATOR=str(args.compiler), VERILATOR_JOBS='2',
               TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
               PATH=str(args.compiler.parent) + os.pathsep + os.environ['PATH'])
    specs = [
        ('maap-suite', ['make', '-j16', '-C', 'tb/verilator/maap', 'VERILATOR_JOBS=2']),
        ('datapath-legs', ['make', '-j16', '-C', 'tb/verilator/milan_dp', 'option-off', 'ax1x1', 'VERILATOR_JOBS=2']),
        ('lint', ['python3', 'scripts/lint_rtl.py', '--check', '--jobs', '2']),
    ]
    def run(spec):
        name, command = spec
        start = time.monotonic()
        print('START ' + name, flush=True)
        with (packet / (name + '.log')).open('w') as log:
            log.write('COMMAND ' + json.dumps(command) + '\n')
            log.flush()
            result = subprocess.run(command, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
        (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
        print(f'END {name} rc={result.returncode} seconds={time.monotonic()-start:.1f}', flush=True)
        return result.returncode
    with ThreadPoolExecutor(max_workers=3) as pool:
        statuses = list(pool.map(run, specs))
    return int(any(statuses))

if __name__ == '__main__':
    raise SystemExit(main())
