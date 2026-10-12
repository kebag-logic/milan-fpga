#!/usr/bin/env python3
"""Run bounded read-only gates concurrently; wait for all foreground children.

Usage: python3 run_gates.py CHECKOUT PACKET [PYTHON_FOR_DOC_GATES]
The runner itself and its self-test are deliberately excluded.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
python = sys.argv[3] if len(sys.argv) > 3 else sys.executable
receipt = packet / 'receipts'
receipt.mkdir(exist_ok=True)
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
           GIT_NO_REPLACE_OBJECTS='1')
jobs = {
    'ci-contract': [sys.executable, 'scripts/ci_events.py', '--check'],
    'ci-contract-selftest': [sys.executable, 'scripts/ci_events.py', '--selftest'],
    'python-idiom': [sys.executable, 'scripts/check_py_idiom.py'],
    'baremetal': [sys.executable, 'scripts/check_baremetal_only.py', '--check'],
    'docs': [python, 'scripts/docs_check.py'],
    'doc-style': [python, 'scripts/check_doc_style.py'],
    'doc-paths': [python, 'scripts/check_doc_paths.py'],
    'toc': [python, 'scripts/gen_toc.py', '--check'],
    'anchors': [python, 'scripts/gen_toc.py', '--verify-anchors'],
    'em-dash': [python, 'scripts/check_em_dash.py', '--base', 'dc4d06cb'],
    'whitespace': ['git', 'diff', '--check', 'dc4d06cb', 'HEAD'],
    'original-r1-probe': [sys.executable, str(packet/'probe_cpu_ranges_r1.py'), str(root)],
    'compatible-r1-probe': [sys.executable, str(packet/'probe_cpu_ranges_compat.py'), str(root)],
}

def run(item):
    name, command = item
    start = time.monotonic()
    with (receipt / (name + '.log')).open('w') as out:
        try:
            result = subprocess.run(command, cwd=root, env=env, stdout=out,
                                    stderr=subprocess.STDOUT, timeout=480)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            rc = 124
            out.write('\nREVIEW GATE DEADLINE EXCEEDED\n')
    (receipt / (name + '.rc')).write_text(str(rc) + '\n')
    shown = [str(x).replace(str(root), '<checkout>').replace(str(packet), '<packet>') for x in command]
    return {'gate': name, 'argv': shown, 'rc': rc,
            'elapsed_seconds': round(time.monotonic()-start, 3)}

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, jobs.items()))
(receipt / 'gates.json').write_text(json.dumps(results, indent=2)+'\n')
for row in results:
    print(row['gate'], 'rc='+str(row['rc']), str(row['elapsed_seconds'])+'s')
