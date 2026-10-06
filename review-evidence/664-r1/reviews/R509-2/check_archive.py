#!/usr/bin/env python3
"""Check the exact candidate's documentation in an export without metadata."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tarfile

HEAD = '8fb296e3e02985aee27ef04cb08278836b734a14'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repo', type=Path)
    ap.add_argument('--python', required=True)
    ap.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
    a = ap.parse_args()
    a.out = a.out.resolve()
    scratch = a.out / 'scratch'
    dest = scratch / 'archive-export'
    dest.mkdir()
    archive = scratch / 'candidate.tar'
    subprocess.run(['git', '-C', str(a.repo), 'archive', HEAD, '--output', str(archive)], check=True)
    with tarfile.open(archive) as tf:
        tf.extractall(dest, filter='data')
    assert not (dest / '.git').exists()
    env = {**os.environ, 'TMPDIR': str(scratch / 'tmp'),
           'PYTHONPYCACHEPREFIX': str(scratch / 'pycache')}
    def run(name):
        args = [a.python, 'scripts/' + name + '.py']
        r = subprocess.run(args, cwd=dest, env=env, text=True, capture_output=True, timeout=500)
        label = 'archive-' + name
        (a.out / 'checks' / (label + '.log')).write_text(
            'head: ' + HEAD + '\ncommand: python3 scripts/' + name + '.py\n' + r.stdout + r.stderr)
        (a.out / 'checks' / (label + '.rc')).write_text(str(r.returncode) + '\n')
        row = {'check': label, 'rc': r.returncode, 'git_metadata': False}
        print(json.dumps(row), flush=True)
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(run, ['docs_check', 'check_feature_status']))
    (a.out / 'archive-results.json').write_text(json.dumps(rows, indent=2) + '\n')
    raise SystemExit(int(any(r['rc'] for r in rows)))

if __name__ == '__main__':
    main()
