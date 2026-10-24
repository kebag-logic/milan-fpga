#!/usr/bin/env python3
"""Run independent focused checks concurrently; wait for every foreground child."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import time

packet = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve()
verilator = os.environ.get('REVIEW_VERILATOR', os.environ.get('VERILATOR', 'verilator'))
env = dict(os.environ, VERILATOR=verilator, VERILATOR_JOBS='8', TMPDIR=str(packet/'scratch'))
env['PATH'] = str(Path(verilator).parent) + os.pathsep + env['PATH']
tasks = [
    ('capture_dp', repo/'tb/verilator/capture_coherence', ['make','-j16','dp','VERILATOR_JOBS=8',f'VERILATOR={verilator}']),
    ('behave', repo/'tests', [sys.executable,'-m','behave']),
    ('lint', repo, [sys.executable,'scripts/lint_rtl.py','--check']),
]

def run(task):
    name, cwd, command = task
    start = time.monotonic()
    with (packet/f'{name}.log').open('w') as log:
        log.write(f'Head: {subprocess.check_output(["git","rev-parse","HEAD"],cwd=repo,text=True).strip()}\n')
        log.write(f'Working directory relative to probe: {cwd.relative_to(repo)}\nCommand: {command!r}\n')
        log.flush()
        result = subprocess.run(command,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
    (packet/f'{name}.rc').write_text(f'{result.returncode}\n')
    print(f'{name}: rc={result.returncode}, seconds={time.monotonic()-start:.1f}',flush=True)
    return result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run,tasks))
sys.exit(any(results))
