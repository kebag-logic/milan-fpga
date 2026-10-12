#!/usr/bin/env python3
"""Independently reproduce the public R626-1/F1 threshold-control finding."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
source = (repo / 'scripts/suite_shards.py').read_text()
workflow = (repo / '.github/workflows/rtl.yml').read_text()
names = sorted(d.name for d in (repo / 'tb/verilator').iterdir() if d.is_dir() and (d / 'Makefile').is_file())
cases = {
    'pristine': source,
    'percent-75': source.replace('HEADROOM_PERCENT = 60', 'HEADROOM_PERCENT = 75'),
    'percent-100': source.replace('HEADROOM_PERCENT = 60', 'HEADROOM_PERCENT = 100'),
    'divisor-10': source.replace('return timeout_minutes * 60 * HEADROOM_PERCENT // 100',
                                'return timeout_minutes * 60 * HEADROOM_PERCENT // 10'),
}
rows = []
for label, text in cases.items():
    root = packet / 'scratch' / ('prior-f1-' + label)
    (root / 'scripts').mkdir(parents=True, exist_ok=True)
    (root / '.github/workflows').mkdir(parents=True, exist_ok=True)
    (root / 'scripts/suite_shards.py').write_text(text)
    (root / '.github/workflows/rtl.yml').write_text(workflow)
    for name in names:
        d = root / 'tb/verilator' / name
        d.mkdir(parents=True, exist_ok=True)
        (d / 'Makefile').touch()
    r = subprocess.run([sys.executable, 'scripts/suite_shards.py', '--selftest'], cwd=root,
                       env=dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1'),
                       capture_output=True, text=True, timeout=30)
    (packet / 'receipts' / ('prior-f1-' + label + '.log')).write_text(r.stdout + r.stderr)
    (packet / 'receipts' / ('prior-f1-' + label + '.rc')).write_text(str(r.returncode) + '\n')
    row = {'case': label, 'rc': r.returncode,
           'head_workers': [line.strip() for line in r.stdout.splitlines() if 'head worker' in line],
           'selftest_pass': 'selftest: PASS' in r.stdout,
           'escaped_count': r.stdout.count('ESCAPED')}
    rows.append(row)
    assert r.returncode == 0 and row['selftest_pass'] and row['escaped_count'] == 0
    print(json.dumps(row), flush=True)
(packet / 'receipts/prior-f1-reproduction.json').write_text(json.dumps(rows, indent=2) + '\n')
print('CONFIRMED: all three bound-loosening mutants survive the source self-test.')
