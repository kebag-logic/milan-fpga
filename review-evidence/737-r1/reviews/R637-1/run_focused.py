#!/usr/bin/env python3
"""Run bounded, foreground review controls; keep disposable files in scratch."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
(packet / 'scratch' / 'tmp').mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(packet / 'scratch' / 'tmp'),
           PYTHONDONTWRITEBYTECODE='1')
tests = [[sys.executable, 'scripts/' + name] for name in (
    'ci_gate_workflows_selftest.py', 'ci_case_receipts_selftest.py',
    'ci_make_cases_selftest.py', 'ci_maap_cases_selftest.py',
    'ci_capture_cases_selftest.py', 'ci_suite_pieces_selftest.py',
    'ci_suite_collect_selftest.py', 'ci_fail_fast_selftest.py',
    'ci_runtime_evidence_selftest.py', 'ci_install_cache_selftest.py',
    'ci_workflow_plan_selftest.py', 'ci_manifest_selftest.py')]
tests += [[sys.executable, 'scripts/' + name, flag] for name, flag in (
    ('ci_gate_workflows.py', '--check'), ('generate_ci_evidence_pins.py', '--check'),
    ('suite_shards.py', '--selftest'), ('ci_events.py', '--check'),
    ('ci_events.py', '--selftest'))]

def run(command):
    label = Path(command[1]).stem + ('-' + command[2].lstrip('-') if len(command) > 2 else '')
    start = time.monotonic()
    with (packet / (label + '.log')).open('wb') as log:
        result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
    row = dict(command=['python3', *command[1:]], returncode=result.returncode,
               seconds=round(time.monotonic() - start, 3), log=label + '.log')
    (packet / (label + '.rc')).write_text(str(result.returncode) + '\n')
    print(json.dumps(row), flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, tests))
(packet / 'focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(int(any(row['returncode'] for row in results)))
