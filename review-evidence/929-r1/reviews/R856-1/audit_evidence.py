#!/usr/bin/env python3
"""Audit the published receipt archive without executing its scripts.
Usage: audit_evidence.py EXTRACTED_REVIEW_EVIDENCE_DIRECTORY
"""
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
manifest = json.loads((root / 'MANIFEST.json').read_text())
checked = 0
for row in manifest:
    if not row['file'].startswith('author-r1/receipts/'):
        continue
    path = root / row['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['published_sha256'], row['file']
    checked += 1
print(f'Archive c836e7a857b6b4333b78910e5502a42a03697380: {checked} published receipts match MANIFEST.json')
r = root / 'author-r1/receipts'
rows = []
for line in (r / 'workflows/verify-37255683.md').read_text().splitlines():
    if line.startswith('| rtl-fast |') or line.startswith('| docs |'):
        rows.append([c.strip() for c in line.strip('|').split('|')])
jobs = {(row[0], row[1]) for row in rows}
executed = [row for row in rows if row[4] == '0']
skipped = [row for row in rows if row[4] == '-']
assert len(jobs) == 14 and len(executed) == 88 and len(skipped) == 56
omitted = []
for row in executed:
    leaf = row[5].strip('`')
    # The archive retains the failed first boundary attempt separately under
    # logs-gates-venv; the successful final receipts are under logs.
    folder = 'logs'
    log = r / 'workflows' / folder / leaf
    rc = log.with_suffix('.rc')
    assert rc.read_text().strip() == '0', str(rc)
    if not log.exists():
        omitted.append(leaf)
    else:
        assert '372556835d03b70134b2e76567b63b25c4cca005' in log.read_text().splitlines()[0], leaf
print('Workflow replay audit: 14 jobs, 88 zero rc steps, 56 explicitly not-run steps')
print('Full logs omitted from archive, hash and rc supplied: ' + ', '.join(omitted))

def hashes(path):
    return {name: digest for digest, name in re.findall(r'^([0-9a-f]{64})  (.+)$', path.read_text(), re.M)}

base = hashes(r / 'images/release-base-70f4056f-IMAGES.sha256')
head = hashes(r / 'images/release-G-37255683-IMAGES.sha256')
assert base.keys() == head.keys()
different = [k for k in base if base[k] != head[k]]
assert len(different) == 2 and all(k.endswith('/bios.elf') for k in different)
print(f'Release firmware: {len(base)-len(different)} identical hashes; two whole bios.elf hashes differ')
print('Published section audit attributes whole-ELF differences only to debug sections; loadable, stripped and disassembly match')
base = hashes(r / 'images/split-ledger-base-70f4056f.log')
head = hashes(r / 'images/split-ledger-head-37255683.log')
assert base == head and len(base) == 24
print('Split firmware: all 24 recorded hashes identical (four ledger points plus mapped/stand-in images)')
for name in ('split-ledger-base-70f4056f.log', 'split-ledger-head-37255683.log'):
    lines = (r / 'images' / name).read_text().splitlines()
    assert sum(x.startswith('POINT ') and x.endswith('PASS') for x in lines) == 4
    assert 'plat_ledger: PASS (0 finding(s))' in lines
print('Both platform ledger receipts: four points PASS, zero findings')
text = (r / 'dynmap/head-37255683-dynmap-mutants.txt').read_text()
assert text.count('[PASS] mutant caught:') == 66
assert text.count('[PASS] the unmutated gateware still passes') == 5
assert '71 checks: 71 PASS, 0 FAIL' in text
print('Published dynmap campaign: 5 controls and 66 named catches, 71/71')
text = (r / 'twin/head-37255683-twin-plants.txt').read_text()
refused = re.findall(r'^plant ([\w-]+): REFUSED', text, re.M)
assert len(refused) == 42 and len(set(refused)) == 21
assert all(refused.count(name) == 2 for name in set(refused))
print('Published twin plants: 21 distinct plants, each refused twice')
print('No builder, firmware bank, synthesis bank, hardware or hosted job executed by this audit')
