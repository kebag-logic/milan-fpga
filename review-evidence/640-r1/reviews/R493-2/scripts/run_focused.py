#!/usr/bin/env python3
"""Run bounded, read-only documentation checks and retain raw receipts."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('output', type=Path)
p.add_argument('--python', default='python3')
p.add_argument('--jobs', type=int, default=8)
a = p.parse_args()
assert 1 <= a.jobs <= 16
a.output.mkdir(parents=True, exist_ok=True)
scratch = a.output.parent.parent / 'scratch' / 'gate-temporaries'
scratch.mkdir(parents=True, exist_ok=True)
checks = {
    'docs': ['scripts/docs_check.py'],
    'docs-self': ['scripts/docs_check.py', '--selftest'],
    'docs-no-git': ['scripts/docs_check.py'],
    'style': ['scripts/check_doc_style.py'],
    'style-self': ['scripts/check_doc_style.py', '--selftest'],
    'paths': ['scripts/check_doc_paths.py'],
    'feature': ['scripts/check_feature_status.py'],
    'archive': ['scripts/check_archive.py'],
    'toc': ['scripts/gen_toc.py', '--check'],
    'anchors': ['scripts/gen_toc.py', '--verify-anchors'],
    'toc-self': ['scripts/gen_toc.py', '--selftest'],
    'em-dash': ['scripts/check_em_dash.py', '--base', '5603c353137e90c1fa95429f6d00ef7a2298d9ee'],
    'em-dash-self': ['scripts/check_em_dash.py', '--selftest'],
    'resource-baseline': ['syn/ooc/pp_resource_gate.py', 'check-baseline'],
    'resource-self': ['syn/ooc/pp_resource_gate.py', '--selftest'],
    'resource-mutants': ['syn/ooc/pp_resource_gate_mutants.py'],
}

def run(item):
    name, args = item
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch.resolve()))
    if name == 'docs-no-git':
        env['GIT_DIR'] = '/dev/null'
    started = time.monotonic()
    with (a.output / (name + '.log')).open('wb') as log:
        r = subprocess.run([a.python, *args], cwd=a.repo, env=env,
                           stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (a.output / (name + '.rc')).write_text(str(r.returncode) + '\n')
    return dict(name=name, command=['python3', *args], rc=r.returncode,
                seconds=round(time.monotonic()-started, 3))

with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results = list(pool.map(run, checks.items()))
(a.output / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
for row in results:
    print(row['name'], 'rc=' + str(row['rc']), str(row['seconds']) + 's')
raise SystemExit(int(any(x['rc'] != 0 for x in results)))
