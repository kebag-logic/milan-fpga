#!/usr/bin/env python3
"""Concurrent read-only budget graders, evidence digest audit and source integrity."""
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
budget = repo / 'tb/verilator/ctrl_service_budget'
commands = {
    'flip-1x1': [sys.executable, '-B', str(budget / 'flip_grade.py'), '--check', '--point', '1x1/1if'],
    'flip-8x8': [sys.executable, '-B', str(budget / 'flip_grade.py'), '--check', '--point', '8x8/1if'],
    'load': [sys.executable, '-B', str(budget / 'load_grade.py'), '--check'],
    'shape-costs': [sys.executable, '-B', str(budget / 'shape_costs.py'), '--check'],
    'integrity': [sys.executable, '-B', str(packet / 'integrity.py'), str(repo)],
}
def run(item):
    name, cmd = item
    with (packet / 'receipts' / (name + '.log')).open('w') as log:
        result = subprocess.run(cmd, cwd=repo, stdout=log, stderr=subprocess.STDOUT,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch')))
    (packet / 'receipts' / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, result.returncode, flush=True)
    return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
evidence = packet / 'scratch/review-evidence/950-r1'
manifest = json.loads((evidence / 'MANIFEST.json').read_text())
lines = []
for row in manifest:
    f = evidence / row['file']
    if not f.is_file():
        continue
    digest = hashlib.sha256(f.read_bytes()).hexdigest()
    assert digest == row['published_sha256'], row['file']
    lines.append(f"{digest}  {row['file']}")
(packet / 'receipts/public-evidence-digests.log').write_text('\n'.join(lines) + '\n')
print('public evidence verified', len(lines), 'files')
raise SystemExit(int(any(results)))
