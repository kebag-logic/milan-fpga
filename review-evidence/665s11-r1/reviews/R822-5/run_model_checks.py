#!/usr/bin/env python3
"""Reproduce the focused model commands; this does not run simulation banks."""
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

tree, packet = (Path(x).resolve() for x in sys.argv[1:3])
root = tree / 'tb/verilator/ctrl_service_budget'
commands = [
    ('record_classes.py---selftest', 'record_classes.py', '--selftest'),
    ('load_grade.py---check', 'load_grade.py', '--check'),
    ('load_grade.py---selftest', 'load_grade.py', '--selftest'),
    ('flip_grade.py---selftest', 'flip_grade.py', '--selftest'),
    ('rows_tiers.py---selftest', 'rows_tiers.py', '--selftest'),
    ('flip-check', 'flip_grade.py', '--check', '--point', '1x1/1if'),
    ('tier-grid', 'tier_grid.py', '--point', '1x1/1if'),
]
def run(entry):
    label, script, *args = entry
    cmd = [sys.executable, str(root / script), *args]
    with (packet / (label + '.log')).open('w') as log:
        result = subprocess.run(cmd, cwd=tree, stdout=log, stderr=subprocess.STDOUT)
    (packet / (label + '.rc')).write_text(str(result.returncode) + '\n')
    return dict(command=[script, *args], rc=result.returncode, receipt=label+'.log')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, commands))
print(json.dumps(results, indent=2))
raise SystemExit(int(any(x['rc'] for x in results)))

