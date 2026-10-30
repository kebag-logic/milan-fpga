#!/usr/bin/env python3
"""Disposable inventory probes; the reviewed checkout is read-only."""
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
copy = out / 'scratch' / 'archive'
copy.mkdir(parents=True, exist_ok=True)
archive = subprocess.check_output(['git', 'archive', 'HEAD'], cwd=root)
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
    tf.extractall(copy, filter='data')
env = dict(os.environ, TMPDIR=str(out / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
records = []
def run(label, args, expected):
    p = subprocess.run([sys.executable, *args], cwd=copy, env=env,
                       text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    records.append(f'{label}: rc={p.returncode}; expected={expected}\n' + p.stdout)
    assert p.returncode == expected, label

files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
expected = {p for p in files if p and (p.endswith('.md') or Path(p).name.upper().startswith('README'))}
page = (copy / 'docs/DOCUMENTATION_AUDIT.md').read_text()
rows = re.findall(r'^\| \[([^\]]+)\]\([^)]*\) \| (\d+) \|', page, re.M)
actual = {p.removesuffix(' (historical)') for p, _ in rows}
assert actual == expected, (expected - actual, actual - expected)
for path, lines in rows:
    path = path.removesuffix(' (historical)')
    assert int(lines) == len((copy / path).read_text().splitlines()), path
records.append(f'Independent tracked-document census: {len(expected)} documents; exact set and every line count match.\n')
run('archive without metadata or submodules', ['scripts/docs_inventory.py', '--check'], 0)
run('archive docs gate', ['scripts/docs_check.py'], 0)
run('archive status gate', ['scripts/check_feature_status.py'], 0)
target = copy / 'docs/DOCUMENTATION_AUDIT.md'
saved = target.read_bytes()
target.write_bytes(saved + b'Planted stale audit.\n')
run('planted stale audit', ['scripts/docs_inventory.py', '--check'], 1)
target.write_bytes(saved)
target = copy / 'scripts/docs_inventory.json'
saved = target.read_bytes()
changed = json.loads(saved)
changed['findings'][0]['quote'] = 'Planted quotation absent from the page.'
target.write_text(json.dumps(changed))
run('planted edited data-file finding quote', ['scripts/docs_inventory.py', '--check'], 1)
target.write_bytes(saved)
target = copy / 'docs/guides/PROJECT_MANAGER.md'
saved = target.read_bytes()
target.write_bytes(saved + b'Planted document change.\n')
run('planted stale source-page metadata', ['scripts/docs_inventory.py', '--check'], 1)
target.write_bytes(saved)
target = copy / 'README.md'
saved = target.read_bytes()
target.write_bytes(saved.replace(b'ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware.',
                                b'ADP, ACMP, AECP, MAAP and SRP default to fabric.'))
run('planted edited finding quotation', ['scripts/docs_inventory.py', '--check'], 1)
target.write_bytes(saved)
target = copy / 'docs/integration/INTEGRATION_GUIDE.md'
saved = target.read_bytes()
assert b'Shipping deployment selects 50 MHz' in saved
target.write_bytes(saved.replace(b'Shipping deployment selects 50 MHz', b'Shipping deployment selects 99 MHz'))
run('same-line numeric edit survives freshness check', ['scripts/docs_inventory.py', '--check'], 0)
target.write_bytes(saved)
run('restored archive', ['scripts/docs_inventory.py', '--check'], 0)
run('area findings export', ['scripts/docs_inventory.py', '--findings-dir', str(out / 'scratch' / 'findings')], 0)
clone = out / 'scratch' / 'without-submodules'
if not clone.exists():
    subprocess.run(['git', 'clone', '--quiet', '--no-recurse-submodules', '--no-hardlinks',
                    str(root), str(clone)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
copy = clone
run('Git checkout without submodules', ['scripts/docs_inventory.py', '--check'], 0)
run('Git checkout without submodules docs gate', ['scripts/docs_check.py'], 0)
run('Git checkout without submodules status gate', ['scripts/check_feature_status.py'], 0)
(out / 'inventory-probes.log').write_text('\n'.join(records).replace(str(out), '<packet>'))
print('\n'.join(x.splitlines()[0] for x in records))
