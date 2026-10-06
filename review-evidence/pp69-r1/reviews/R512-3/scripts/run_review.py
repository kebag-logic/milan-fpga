#!/usr/bin/env python3
"""Portable foreground coordinator; all disposable work stays under packet/scratch."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--compiler', type=Path, required=True)
a = ap.parse_args()
scripts = Path(__file__).resolve().parent
p = a.packet.resolve()
p.mkdir(parents=True, exist_ok=True)
(p / 'receipts').mkdir(exist_ok=True)
(p / 'initial-index.txt').write_bytes(subprocess.check_output(['git', 'ls-files', '--stage'], cwd=a.repo))
focus = [sys.executable, str(scripts / 'run_focus.py'), '--repo', str(a.repo), '--packet', str(p), '--compiler', str(a.compiler)]
subprocess.run([*focus, '--prepare-only'], check=True)


def run(name, cmd):
    with (p / 'receipts' / (name + '-coordinator.log')).open('w') as f:
        rc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT).returncode
    (p / 'receipts' / (name + '-coordinator.rc')).write_text(str(rc) + '\n')
    return rc


with ThreadPoolExecutor(2) as pool:
    f1 = pool.submit(run, 'focus', [*focus, '--prepared'])
    f2 = pool.submit(run, 'remainder', [sys.executable, str(scripts / 'run_remainder.py'), '--packet', str(p)])
    codes = [f1.result()]
    # Run document gates while the longer remainder campaign continues.
    codes.append(run('docs', [sys.executable, str(scripts / 'run_docs.py'), '--repo', str(a.repo), '--packet', str(p)]))
    codes.append(f2.result())
for name, argv in [
        ('delta', ['check_delta.py', '--repo', str(a.repo), '--output', str(p / 'receipts/delta-checks.json')]),
        ('campaign', ['summarize_campaign.py', '--repo', str(a.repo), '--packet', str(p)]),
        ('shapes', ['check_shapes.py', '--packet', str(p)]),
        ('integrity', ['check_integrity.py', '--repo', str(a.repo), '--packet', str(p)])]:
    codes.append(run(name, [sys.executable, str(scripts / argv[0]), *argv[1:]]))
raise SystemExit(any(codes))
