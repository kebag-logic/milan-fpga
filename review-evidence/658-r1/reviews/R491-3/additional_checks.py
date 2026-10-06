#!/usr/bin/env python3
"""Additional focused checks, after review_checks.py. Arguments: REPO PACKET."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(sys.argv[2]).resolve()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet/'scratch'),
           GIT_NO_REPLACE_OBJECTS='1')
cases = [
    ('pre-move-idiom', ['python3', 'scripts/check_py_idiom.py'], packet/'scratch/before', 1),
    ('docs-check', ['python3', 'scripts/docs_check.py'], repo, 0),
    ('doc-paths', ['python3', 'scripts/check_doc_paths.py'], repo, 0),
    ('foreign-cwd-import', ['python3', str(repo/'scripts/measure_test_evidence.py'), '--check'],
     packet/'scratch', 0),
]

def run(case):
    name, command, cwd, expected = case
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True)
    (packet/f'{name}.stdout').write_bytes(result.stdout)
    (packet/f'{name}.stderr').write_bytes(result.stderr)
    (packet/f'{name}.rc').write_text(str(result.returncode)+'\n')
    return dict(name=name, command=command, expected_rc=expected, actual_rc=result.returncode)

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, cases))
(packet/'additional-commands.json').write_text(json.dumps(results, indent=2)+'\n')
assert all(row['expected_rc'] == row['actual_rc'] for row in results)
assert b'long module 11 > ratchet 10' in (packet/'pre-move-idiom.stderr').read_bytes()
assert (packet/'foreign-cwd-import.stdout').read_bytes() == (packet/'head-check.stdout').read_bytes()
print('PASS: pre-move ratchet failure, documentation gates, foreign-directory import parity.')
