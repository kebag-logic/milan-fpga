#!/usr/bin/env python3
"""Run focused checks concurrently, await every child, retain logs and exits."""
import concurrent.futures
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
receipts = packet / 'receipts'
scratch = packet / 'scratch'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch), GIT_NO_REPLACE_OBJECTS='1')
py = sys.executable
checks = [
    ('docs_check', [py, 'scripts/docs_check.py']),
    ('doc_style', [py, 'scripts/check_doc_style.py']),
    ('doc_paths', [py, 'scripts/check_doc_paths.py']),
    ('feature_status', [py, 'scripts/check_feature_status.py', '--self-test']),
    ('toc_check', [py, 'scripts/gen_toc.py', '--check']),
    ('toc_anchors', [py, 'scripts/gen_toc.py', '--verify-anchors']),
    ('em_dash', [py, 'scripts/check_em_dash.py', '--base', 'c6bd08c6f52632c6d33d834ce842ac3cf63f29cc']),
    ('module_matrix', [py, 'docs/traceability/gen_module_matrix.py', '--check']),
    ('archive', [py, 'scripts/check_archive.py']),
    ('solution_docs', [py, 'scripts/check_solution_docs.py']),
    ('submodule_docs', [py, 'scripts/check_submodule_docs.py']),
    ('gptp_docs', [py, 'scripts/check_gptp_docs.py', '--with-submodule']),
    ('baseline', [py, 'syn/ooc/pp_resource_gate.py', 'check-baseline']),
]

def run(item):
    name, argv = item
    start = time.monotonic()
    with (receipts / (name + '.log')).open('w') as log:
        result = subprocess.run(argv, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    elapsed = round(time.monotonic() - start, 3)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, 'rc', result.returncode, 'seconds', elapsed, flush=True)
    return {'name': name, 'argv': argv, 'rc': result.returncode, 'elapsed_s': elapsed}

stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
if len(sys.argv) > 2:
    selected = set(sys.argv[2:])
    checks = [item for item in checks if item[0] in selected]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, checks))
(receipts / ('checks-retry.json' if len(sys.argv) > 2 else 'checks.json')).write_text(json.dumps({'started_utc': stamp, 'results': results}, indent=2) + '\n')
sys.exit(int(any(r['rc'] for r in results)))
