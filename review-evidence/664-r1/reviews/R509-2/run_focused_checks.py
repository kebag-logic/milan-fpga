#!/usr/bin/env python3
"""Run independent read-only documentation checks concurrently, awaiting all exits."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shlex
import subprocess
import time

BASE = '423ac5d910d09ab189b3acc39ae3ae1d10d50b19'
HEAD = '8fb296e3e02985aee27ef04cb08278836b734a14'
CHECKS = {
    'docs': ['scripts/docs_check.py'],
    'style': ['scripts/check_doc_style.py'],
    'toc': ['scripts/gen_toc.py', '--check'],
    'em-dash': ['scripts/check_em_dash.py', '--base', BASE],
    'traceability': ['docs/traceability/gen_module_matrix.py', '--check'],
    'feature-status': ['scripts/check_feature_status.py', '--self-test'],
    'solution-docs': ['scripts/check_solution_docs.py'],
    'baremetal': ['scripts/check_baremetal_only.py', '--check'],
    'wire-accountability': ['scripts/check_wire_accountability.py', '--self-test'],
    'mailbox-contract': ['sw/mailbox/gen_mailbox.py', '--check', '--crosscheck'],
}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repo', type=Path)
    ap.add_argument('--python', required=True)
    ap.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    assert 1 <= a.jobs <= 16
    a.repo = a.repo.resolve()
    a.out = a.out.resolve()
    logs = a.out / 'checks'
    logs.mkdir(exist_ok=True)
    scratch = a.out / 'scratch'
    (scratch / 'tmp').mkdir(parents=True, exist_ok=True)
    env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1', 'TMPDIR': str(scratch / 'tmp'),
           'PYTHONPYCACHEPREFIX': str(scratch / 'pycache')}
    def run(item):
        name, args = item
        command = [a.python, *args]
        started = time.monotonic()
        with (logs / (name + '.log')).open('w') as f:
            f.write('head: ' + HEAD + '\ncommand: python3 ' + shlex.join(args) + '\n')
            f.flush()
            try:
                rc = subprocess.run(command, cwd=a.repo, env=env, stdout=f,
                                    stderr=subprocess.STDOUT, timeout=500).returncode
            except subprocess.TimeoutExpired:
                f.write('\nREVIEW CHECK TIMEOUT\n')
                rc = 124
        (logs / (name + '.rc')).write_text(str(rc) + '\n')
        row = {'id': name, 'command': ['python3', *args], 'rc': rc,
               'elapsed_seconds': round(time.monotonic() - started, 3)}
        print(json.dumps(row), flush=True)
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        rows = list(pool.map(run, CHECKS.items()))
    (a.out / 'focused-results.json').write_text(json.dumps(rows, indent=2) + '\n')
    raise SystemExit(int(any(r['rc'] for r in rows)))

if __name__ == '__main__':
    main()
