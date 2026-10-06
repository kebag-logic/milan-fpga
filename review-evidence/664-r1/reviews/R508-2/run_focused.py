#!/usr/bin/env python3
"""Run a bounded, concurrent, read-only review bank; wait in the foreground."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument('repo', type=Path)
args = ap.parse_args()
packet = Path(__file__).resolve().parent
repo = args.repo.resolve()
env = {**os.environ, 'PYTHONPATH': str(packet/'scratch/markdown-deps'),
       'PYTHONDONTWRITEBYTECODE': '1', 'GIT_NO_REPLACE_OBJECTS': '1',
       'TMPDIR': str(packet/'scratch')}
commands = {
    'approval-integrity': [sys.executable, str(packet/'check_review.py'), str(repo), str(packet/'pr-body.md')],
    'docs': [sys.executable, 'scripts/docs_check.py'],
    'style': [sys.executable, 'scripts/check_doc_style.py'],
    'toc': [sys.executable, 'scripts/gen_toc.py', '--check'],
    'matrix': [sys.executable, 'docs/traceability/gen_module_matrix.py', '--check'],
    'emdash': [sys.executable, 'scripts/check_em_dash.py', '--base', '423ac5d910d09ab189b3acc39ae3ae1d10d50b19'],
    'feature-status': [sys.executable, 'scripts/check_feature_status.py'],
    'doc-paths': [sys.executable, 'scripts/check_doc_paths.py'],
    'solution': [sys.executable, 'scripts/check_solution_docs.py'],
    'mailbox-contract': [sys.executable, 'sw/mailbox/gen_mailbox.py', '--check', '--crosscheck'],
    'diff-whitespace': ['git', 'diff', '--check', '423ac5d910d09ab189b3acc39ae3ae1d10d50b19', '8fb296e3e02985aee27ef04cb08278836b734a14'],
}


def run(item):
    key, command = item
    start = time.monotonic()
    with (packet/f'{key}.log').open('w') as log:
        log.write('head 8fb296e3e02985aee27ef04cb08278836b734a14\n')
        # Keep public commands portable and free of workspace paths.
        portable = [part.replace(str(repo), '$REPO').replace(str(packet), '$PACKET') for part in command]
        log.write('command '+shlex.join(portable)+'\n')
        log.flush()
        result = subprocess.run(command, cwd=repo, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=480)
    (packet/f'{key}.rc').write_text(str(result.returncode)+'\n')
    receipt = {'check': key, 'rc': result.returncode,
               'elapsed_seconds': round(time.monotonic()-start, 3)}
    print(json.dumps(receipt), flush=True)
    return receipt


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
(packet/'focused-results.json').write_text(json.dumps(results, indent=2)+'\n')
sys.exit(any(r['rc'] for r in results))
