#!/usr/bin/env python3
"""Run just the two sync-added split gate plants in disposable source copies."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
compiler = sys.argv[2]
sys.path.insert(0, str(repo / 'tb/verilator/milan_dp'))
import split_mutants

def run_one(item):
    n, (name, src, old, new, label) = item
    out = packet / 'scratch' / f'split-plant-{n}'
    out.mkdir(parents=True, exist_ok=True)
    text = src.read_text()
    assert text.count(old) == 1
    source = out / src.name
    source.write_text(text.replace(old, new))
    cmd = ['make', '-j16', '-C', str(repo / 'tb/verilator/milan_dp'), 'build-split',
           f'VERILATOR={compiler}', 'VERILATOR_JOBS=6', f'SPLIT_MDIR={out / "obj"}', f'DP_SRC={source}']
    with (packet / f'split-plant-{n}-build.log').open('w') as log:
        built = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    (packet / f'split-plant-{n}-build.rc').write_text(str(built.returncode) + '\n')
    assert built.returncode == 0, name
    ran = subprocess.run([str(out / 'obj/Vmilan_dp_split')],
                         cwd=repo / 'tb/verilator/milan_dp', capture_output=True, text=True)
    (packet / f'split-plant-{n}.log').write_text(ran.stdout + ran.stderr)
    (packet / f'split-plant-{n}.rc').write_text(str(ran.returncode) + '\n')
    caught = ran.returncode > 0 and any(line.startswith('FAIL ' + label) for line in ran.stdout.splitlines())
    assert caught, (name, ran.returncode)
    return f'CAUGHT {name}: {label}; simulation rc={ran.returncode}'

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for result in pool.map(run_one, enumerate(split_mutants.ARMS[-2:])):
        print(result)
print('PASS two sync-added plants caught by their named checks')
