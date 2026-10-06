#!/usr/bin/env python3
"""Run bounded independent checks concurrently and wait for every result."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = (Path(value).resolve() for value in sys.argv[1:3])
(packet / 'scratch').mkdir(exist_ok=True)
(packet / 'receipts').mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
commands = {
    'evidence-check': ['python3', 'scripts/measure_test_evidence.py', '--check'],
    'evidence-selftest': ['python3', 'scripts/measure_test_evidence.py', '--selftest'],
    'shell-syntax': ['bash', '-n', 'scripts/run_all_suites.sh'],
    'shards-selftest': ['python3', 'scripts/suite_shards.py', '--selftest'],
    'tally-selftest': ['python3', 'scripts/suite_tally.py', '--selftest'],
    'cancellation': ['python3', 'scripts/test_suite_cancellation.py'],
    'docs-check': ['python3', 'scripts/docs_check.py'],
    'doc-paths': ['python3', 'scripts/check_doc_paths.py'],
    'doc-style': ['python3', 'scripts/check_doc_style.py'],
    'workflow-check': ['python3', 'scripts/ci_events.py', '--check'],
    'diff-check': ['git', 'diff', '--check', 'bd884631684ccf5060339efa92263d5c3e5c262c', 'HEAD'],
}

def run(item):
    name, command = item
    start = time.monotonic()
    with (packet / 'receipts' / (name + '.log')).open('wb') as log:
        result = subprocess.run(command, cwd=root, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=540)
    elapsed = round(time.monotonic() - start, 3)
    (packet / 'receipts' / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return {'name': name, 'argv': command, 'rc': result.returncode, 'seconds': elapsed}

with ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, commands.items()))
(packet / 'receipts/focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(json.dumps(result))
raise SystemExit(any(result['rc'] != 0 for result in results))
