#!/usr/bin/env python3
"""Run independent lightweight checks concurrently; wait for every receipt."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
md = sys.argv[2] if len(sys.argv) > 2 else sys.executable
out = Path(__file__).resolve().parent
(out / 'receipts').mkdir(exist_ok=True)
(out / 'scratch').mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(out / 'scratch'))
jobs = {
    'selftest': [sys.executable, '-B', 'tb/tools/torture_campaign.py', '--self-test'],
    'behave': [sys.executable, '-B', '-m', 'behave', '--no-capture', '-f', 'plain'],
    'coverage': [sys.executable, '-B', 'tb/tools/torture_campaign.py', '--coverage-by-area', '--areas', 'soak,audio,power'],
    'docs': [md, '-B', 'scripts/docs_check.py'],
    'paths': [md, '-B', 'scripts/check_doc_paths.py'],
    'toc': [md, '-B', 'scripts/gen_toc.py', '--check'],
    'anchors': [md, '-B', 'scripts/gen_toc.py', '--verify-anchors'],
    'em_dash': [md, '-B', 'scripts/check_em_dash.py', '--base', 'e76a755a'],
    'style': [md, '-B', 'scripts/check_doc_style.py'],
    'idiom': [sys.executable, '-B', 'scripts/check_py_idiom.py'],
    'feature_status': [sys.executable, '-B', 'scripts/check_feature_status.py'],
    'feature_selftest': [sys.executable, '-B', 'scripts/check_feature_status.py', '--self-test'],
    'diff_check': ['git', 'diff', '--check', 'e76a755a', 'HEAD'],
}

def run(item):
    name, command = item
    start = time.monotonic()
    with (out / 'receipts' / (name + '.log')).open('wb') as log:
        result = subprocess.run(command, cwd=root / 'tests' if name == 'behave' else root,
                                stdout=log, stderr=subprocess.STDOUT, env=env, timeout=1200)
    (out / 'receipts' / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, result.returncode, flush=True)
    return dict(name=name, command=command, cwd='tests' if name == 'behave' else '.',
                rc=result.returncode, seconds=round(time.monotonic()-start, 3))

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, jobs.items()))
(out / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(any(row['rc'] for row in results))
