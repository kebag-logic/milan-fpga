#!/usr/bin/env python3
"""Verify the public archive and regenerate records using its audited helper.

Usage: verify_resources.py REPO PACKET RECEIPT_ROOT
RECEIPT_ROOT is author-r2/resource-receipts from archive 84add8ed.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('receipts', type=Path)
a = p.parse_args()
repo, packet, receipts = a.repo.resolve(), a.packet.resolve(), a.receipts.resolve()
os.environ['TMPDIR'] = str(packet / 'scratch')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
listed = set()
bad_hashes = []
for line in (receipts / 'MANIFEST.sha256').read_text().splitlines():
    digest, name = line.split(None, 1)
    name = name.lstrip('*')
    assert name not in listed and '..' not in Path(name).parts
    listed.add(name)
    actual_hash = hashlib.sha256((receipts / name).read_bytes()).hexdigest()
    if actual_hash != digest:
        bad_hashes.append(name)
        print(f'FAIL archive hash: {name}: expected {digest}, actual {actual_hash}', flush=True)
actual = {str(p.relative_to(receipts)) for p in receipts.rglob('*') if p.is_file()}
assert actual - {'MANIFEST.sha256'} == listed
print(f'Archive manifest: {len(listed)} files, {len(bad_hashes)} hash mismatches, no unlisted files.', flush=True)

head = '48f12dc14099a3630a98eb07e9ec790695a72bfb'
jobs = [(endpoint, folder, commit) for endpoint in ('route-1x1', 'ooc-1x1', 'ooc-8x8')
        for folder, commit in [('r2-48f12dc1', head),
                               ('r1-c7b69cd0', 'c7b69cd0fb2bdf980546ab413b3b82198267cbd8')]]
def regen(job):
    endpoint, folder, commit = job
    result = subprocess.run([sys.executable, str(receipts / 'scripts/regen_record.py'),
                             str(repo), str(receipts / folder / endpoint), endpoint,
                             '--git', commit], capture_output=True, text=True, timeout=90)
    name = folder + '-' + endpoint
    (packet / 'receipts' / (name+'.log')).write_text(result.stdout+result.stderr)
    (packet / 'receipts' / (name+'.rc')).write_text(str(result.returncode)+'\n')
    return name, result.returncode, result.stdout
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(regen, jobs))
for name, rc, output in results:
    print(name, 'rc', rc)
    print(output)
assert all(rc == 0 for _, rc, _ in results)

sys.path.insert(0, str(repo / 'syn/ooc'))
import pp_resource_gate as gate
current = gate.load(repo / 'syn/ooc/pp_resource_baseline.json')
base_text = subprocess.check_output(['git', '-C', str(repo), 'show',
    '291710b1:syn/ooc/pp_resource_baseline.json'], text=True)
base = gate.load(Path('baseline-F'), base_text)
assert not gate.check_baseline(current, repo / 'docs/design/AREA_BUDGET.md')
for endpoint in ('route-1x1', 'ooc-1x1', 'ooc-8x8'):
    before, after = base['endpoints'][endpoint], current['endpoints'][endpoint]
    for policy in gate.POLICY:
        assert before.get(policy) == after.get(policy), (endpoint, policy)
    assert before['record']['identity'] == after['record']['identity']
    assert 'set_param synth.maxThreads 1' in after['record']['identity']['flow']
    rc, lines = gate.judge(before, after['record'], [])
    print(endpoint, 'against baseline F: rc', rc)
    print('\n'.join(lines))
    assert rc == 0
print('PASS: all six records reproduced; current policies unchanged and all three endpoints pass baseline F.')
raise SystemExit(1 if bad_hashes else 0)
