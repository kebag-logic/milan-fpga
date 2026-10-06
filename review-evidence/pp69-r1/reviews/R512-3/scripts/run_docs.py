#!/usr/bin/env python3
"""Run documentation gates with the history needed by freshness checks."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
a = ap.parse_args()
p = a.packet.resolve()
d = p / 'scratch/docs-tree'
r = p / 'receipts'
start = time.time()
with (r / 'docs-check.log').open('w') as f:
    if not d.exists():
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', str(a.repo.resolve()), str(d)],
                       stdout=f, stderr=subprocess.STDOUT, check=True)
        subprocess.run(['git', 'checkout', '--detach', '669ded57b1fabc2bbf274b8ad05493c7593e0a0a'],
                       cwd=d, stdout=f, stderr=subprocess.STDOUT, check=True)
    env = dict(os.environ, TMPDIR=str(p / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
    rc = subprocess.run(['make', '-j16', 'check'], cwd=d, env=env, stdout=f, stderr=subprocess.STDOUT).returncode
(r / 'docs-check.rc').write_text(str(rc) + '\n')
row = {'rc': rc, 'seconds': round(time.time() - start, 2), 'cwd': str(d), 'command': ['make', '-j16', 'check']}
(r / 'docs-check-run.json').write_text(json.dumps(row, indent=2) + '\n')
print(json.dumps(row))
raise SystemExit(rc)
