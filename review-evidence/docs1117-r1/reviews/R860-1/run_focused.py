#!/usr/bin/env python3
"""Run bounded documentation checks against a caller-supplied checkout."""
import concurrent.futures
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
python = sys.argv[3]
scratch = out / 'scratch'
scratch.mkdir(exist_ok=True)
logs = out / 'logs'
logs.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))
checks = {
    'docs_check': [python, 'scripts/docs_check.py'],
    'doc_style': [python, 'scripts/check_doc_style.py'],
    'em_dash': [python, 'scripts/check_em_dash.py', '--base', '6b66f66d'],
    'contents': [python, 'scripts/gen_toc.py', '--check'],
    'anchors': [python, 'scripts/gen_toc.py', '--verify-anchors'],
    'doc_paths': [python, 'scripts/check_doc_paths.py'],
    'inventory': [python, 'scripts/docs_inventory.py', '--check'],
    'feature_status': [python, 'scripts/check_feature_status.py'],
    'diff_check': ['git', 'diff', '--check', '6b66f66d..HEAD'],
}
def run(pair):
    name, cmd = pair
    with (logs / (name + '.log')).open('w') as f:
        p = subprocess.run(cmd, cwd=root, env=env, stdout=f, stderr=subprocess.STDOUT)
    (logs / (name + '.rc')).write_text(str(p.returncode) + '\n')
    return dict(name=name, command=cmd, rc=p.returncode)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(run, checks.items()))
(out / 'focused-results.json').write_text(json.dumps(rows, indent=2) + '\n')
for r in rows:
    print(r['name'], 'rc=' + str(r['rc']))
raise SystemExit(any(r['rc'] for r in rows))
