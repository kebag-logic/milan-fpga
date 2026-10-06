#!/usr/bin/env python3
"""Run bounded independent documentation checks under one foreground process."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet, interpreter = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
jobs = [
    ('traceability', ['docs/traceability/gen_module_matrix.py', '--check']),
    ('doc-paths', ['scripts/check_doc_paths.py']),
    ('doc-style', ['scripts/check_doc_style.py']),
    ('doc-toc', ['scripts/gen_toc.py', '--check']),
    ('docs', ['scripts/docs_check.py']),
    ('feature-status', ['scripts/check_feature_status.py']),
    ('wire-accountability', ['scripts/check_wire_accountability.py', '--self-test']),
    ('mailbox-contract', ['sw/mailbox/gen_mailbox.py', '--check', '--crosscheck']),
    ('mailbox-generator-controls', ['sw/mailbox/gen_mailbox.py', '--selftest']),
    ('em-dash', ['scripts/check_em_dash.py', '--base', '30e3c018b9add0cb182d8f1229eeec062218130d']),
]
tmp = packet / 'scratch' / 'tmp'
tmp.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(tmp), GIT_NO_REPLACE_OBJECTS='1')
env['PATH'] = str(Path(interpreter).parent) + os.pathsep + env['PATH']
(packet / 'checks').mkdir(exist_ok=True)

def run(item):
    name, args = item
    start = time.monotonic()
    with (packet / 'checks' / f'{name}.log').open('wb') as log:
        result = subprocess.run([interpreter, *args], cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=180)
    seconds = round(time.monotonic() - start, 3)
    (packet / 'checks' / f'{name}.rc').write_text(str(result.returncode) + '\n')
    print(f'{name}: rc={result.returncode}; seconds={seconds}', flush=True)
    return dict(name=name, command=['python3', *args], rc=result.returncode, seconds=seconds)

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, jobs))
(packet / 'checks' / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(any(result['rc'] != 0 for result in results))
