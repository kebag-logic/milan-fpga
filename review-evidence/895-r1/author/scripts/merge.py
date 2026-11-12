#!/usr/bin/env python3
"""Merge a split harness leg's runs and regrade them as one (lane 895).

usage: merge.py NAME POINT CLONE [run.py args]

For every group of the point (run.py's all_groups), the completed log (one that ends in its RESULT line) and its
script from any of builds/NAME's results directories, copied into results-all; a group with no completed log is
named and the merge refuses. Then run.py --regrade on results-all, which writes its results.json and table.md.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

name, point, clone = sys.argv[1:4]
extra = sys.argv[4:]
T = Path('/data-2/milan/tmp/895-a775')
B = T / 'builds' / name
H = Path(clone) / 'tb/verilator/ctrl_service_budget'
sys.path[:0] = [str(H)]
os.chdir(H)
import run  # noqa: E402
import scenario  # noqa: E402

spec = json.loads((B / 'build.json').read_text())
order = run.all_groups(scenario.point(point, spec), spec)
out = B / 'results-all'
out.mkdir(exist_ok=True)
missing, sources = [], {}
for g in order:
    found = None
    for d in sorted(B.glob('results*')):
        if d == out:
            continue
        log = d / f'{g.name}.log'
        if log.exists() and b'\nRESULT' in log.read_bytes()[-400:]:
            found = d
            break
    if found is None:
        missing.append(g.name)
        continue
    sources[g.name] = found.name
    for suffix in ('.txt', '.log'):
        shutil.copyfile(found / f'{g.name}{suffix}', out / f'{g.name}{suffix}')
(out / 'merged-from.json').write_text(json.dumps(sources, indent=1) + '\n')
if missing:
    print(f'MERGE REFUSED: {len(missing)} group(s) with no completed log: {",".join(missing)}')
    sys.exit(2)
print(f'merged {len(sources)} groups from {sorted(set(sources.values()))}', flush=True)
rc = subprocess.run(['python3', '-B', str(H / 'run.py'), '--point', point, '--build-dir', str(B), '--regrade',
                     '--out', str(out), '--record-budget-findings', '--record-share-findings', *extra]).returncode
print(f'regrade rc={rc}')
sys.exit(rc)
