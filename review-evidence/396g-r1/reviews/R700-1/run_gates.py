#!/usr/bin/env python3
"""Run independent review gates concurrently; wait for all in the foreground."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
(out / "scratch").mkdir(exist_ok=True)
md = sys.argv[2]
py = sys.executable
jobs = {
    'selftest': ([py, '-B', 'tb/tools/torture_campaign.py', '--self-test'], repo),
    'mutants': ([py, '-B', 'tb/tools/torture_release_mutants.py'], repo),
    'behave': ([py, '-B', '-m', 'behave', '--no-capture', '-f', 'plain'], repo / 'tests'),
    'plan': ([py, '-B', 'tb/tools/torture_campaign.py', '--plan', '--areas', 'soak,audio,power', '--json'], repo),
    'coverage': ([py, '-B', 'tb/tools/torture_campaign.py', '--coverage-by-area', '--areas', 'soak,audio,power'], repo),
}
for name, args in {
    'docs_check': ['scripts/docs_check.py'],
    'doc_paths': ['scripts/check_doc_paths.py'],
    'toc': ['scripts/gen_toc.py', '--check'],
    'anchors': ['scripts/gen_toc.py', '--verify-anchors'],
    'em_dash': ['scripts/check_em_dash.py', '--base', 'e76a755afc0536453161e3cd33f6f4d2dcd7641f'],
    'doc_style': ['scripts/check_doc_style.py'],
    'py_idiom': ['scripts/check_py_idiom.py'],
    'feature_status': ['scripts/check_feature_status.py'],
    'feature_status_selftest': ['scripts/check_feature_status.py', '--self-test'],
}.items():
    jobs[name] = ([md, '-B'] + args, repo)
jobs['diff_check'] = (['git', 'diff', '--check', 'e76a755a', 'HEAD'], repo)

def run(item):
    name, (argv, cwd) = item
    begin = time.monotonic()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(out / 'scratch'))
    with (out / (name + '.log')).open('w') as log:
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    rc = result.returncode
    (out / (name + '.rc')).write_text(str(rc) + '\n')
    record = dict(name=name, argv=argv, cwd=str(cwd), rc=rc, seconds=round(time.monotonic()-begin, 3))
    print(json.dumps(record), flush=True)
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, jobs.items()))
(out / 'gates.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(any(r['rc'] for r in results))
