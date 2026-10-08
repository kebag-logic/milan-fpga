#!/usr/bin/env python3
"""Replay the exact-head MAAP harness and its mutations in disposable storage.

Usage: run_focused.py REPO PACKET SIMULATOR [--jobs 4]
Each worker has at most four compiler jobs. All children are joined.
"""
import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('simulator')
p.add_argument('--jobs', type=int, default=4)
a = p.parse_args()
assert 1 <= a.jobs <= 4
repo, packet = a.repo.resolve(), a.packet.resolve()
work = packet / 'scratch' / 'focused'
logs = packet / 'receipts' / 'focused'
logs.mkdir(parents=True, exist_ok=True)
for path in ['tb/verilator/maap/Makefile', 'tb/verilator/maap/sim_main.cpp',
             'tb/verilator/maap/mutants.py', 'tb/common/verilator_harness.hpp']:
    dest = work / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(repo / path, dest)
spec = importlib.util.spec_from_file_location('mutations', work / 'tb/verilator/maap/mutants.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
source = (repo / 'hdl/ieee1722/maap/KL_maap.sv').read_text()
cases = [('clean', source, None)]
for name, item, anchor, replacement, failure in m.MUTANTS:
    assert source.count(anchor) == 1, name
    cases.append((name, source.replace(anchor, replacement), failure))
assert {row[1] for row in m.MUTANTS} - {0} == {1, 2, 3, 4}

def run(case):
    name, text, failure = case
    lane = work / name
    lane.mkdir(parents=True, exist_ok=True)
    rtl = lane / 'KL_maap.sv'
    rtl.write_text(text)
    cmd = ['make', '-j16', '-s', '-C', str(work / 'tb/verilator/maap'), 'build',
           f'MAAP_RTL={rtl}', f'MDIR={lane / "obj"}', f'VERILATOR={a.simulator}',
           'VERILATOR_JOBS=4']
    with (logs / f'{name}.build.log').open('w') as f:
        build = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, timeout=180)
    (logs / f'{name}.build.rc').write_text(str(build.returncode)+'\n')
    rc = None
    output = ''
    if build.returncode == 0:
        result = subprocess.run([str(lane / 'obj/VKL_maap_sim')], capture_output=True,
                                text=True, timeout=120)
        rc, output = result.returncode, result.stdout + result.stderr
        (logs / f'{name}.run.log').write_text(output)
        (logs / f'{name}.run.rc').write_text(str(rc)+'\n')
    good = build.returncode == 0 and ((rc == 0 and '130 checks, 0 failures' in output)
                                    if failure is None else
                                    (rc == 1 and '[FAIL] '+failure in output))
    row = dict(name=name, build_rc=build.returncode, run_rc=rc,
               named_failure=failure, passed=good)
    print(json.dumps(row), flush=True)
    return row

clean = run(cases[0])
assert clean['passed'], 'clean control failed'
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
    rows = [clean, *pool.map(run, cases[1:])]
(logs / 'summary.json').write_text(json.dumps(rows, indent=2)+'\n')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
