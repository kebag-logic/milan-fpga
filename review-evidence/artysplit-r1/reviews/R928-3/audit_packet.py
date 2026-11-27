"""Verify downloaded public receipts against their published inventories.

Usage: python3 -B audit_packet.py SOURCE PACKET_SCRATCH
PACKET_SCRATCH contains author-r7 and author-r8 from the pinned evidence commit.
"""
import hashlib
import json
import sys
from pathlib import Path

source, scratch = map(Path, sys.argv[1:])
sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
import receipt_regrade

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(folder):
    record = json.loads((folder / 'FILES.manifest.json').read_text())
    data = receipt_regrade.read_parts(folder, record)
    return {p: (int(size), digest) for p, size, digest in
            (line.split('\t') for line in data.decode().splitlines()[1:] if line)}

r8 = scratch / 'author-r8/receipts'
r7 = scratch / 'author-r7/receipts'
inv8, inv7 = inventory(r8), inventory(r7)
mismatches = []
for name, (size, digest) in inv8.items():
    path = r8 / name
    assert path.stat().st_size == size, name
    if sha(path) != digest:
        mismatches.append(name)
print(f'Round-8 FILES inventory: {len(inv8)} files, {len(mismatches)} digest mismatches')
extract = r8 / 'census-extract'
files = json.loads((extract / 'FILES.json').read_text())
sources = set()
for row in files:
    if sha(extract / row['path']) != row['sha256']:
        assert 'census-extract/' + row['path'] in mismatches, row['path']
    for parent in row['sources']:
        assert inv7[parent['path']][1] == parent['sha256'], parent['path']
        sources.add(parent['path'])
print(f'Extract mapping: {len(files)} files, same {len(mismatches)} digest mismatches; '
      f'all {len(sources)} source inventory references match')
census = json.loads((extract / 'census.json').read_text())
identity = json.loads((r8 / 'identity/paired-identity.json').read_text())
print('Identity keys:', sorted(identity))
for row in identity['variants']:
    for key in ('executable', 'executable_recorded', 'elf', 'flash_image', 'xip'):
        assert row[key][0] == row[key][1], (row['variant'], key)
    assert row['executable'] == row['executable_recorded']
    assert row['flash_image'] == [None, None] and row['xip'] == [False, False]
print(f'PASS executable/ELF identity: {len(identity["variants"])} variants; flash null and non-XIP')
by_case = {r['case']: r for r in identity['cases']}
variants = {r['variant']: r for r in identity['variants']}
for row in census['cases']:
    path = extract / row['manifest']
    assert sha(path) == row['sha256'], row['case']
    manifest = json.loads(path.read_text())
    pair = by_case[row['case']]['stimulus']
    assert pair[0] == pair[1] == manifest['stimulus']['sha256']
    assert sha(path.parent / 'stimulus.txt') == pair[0]
    variant = variants[row['case'].split('/')[0]]
    assert manifest['executable_sha256'] == variant['executable'][0]
    assert manifest['firmware_sha256'] == variant['elf'][0]
print(f'PASS census manifest digests: {len(census["cases"])} cases')
print(f'PASS paired stimulus and executable/ELF bindings: {len(by_case)} cases')
for row in json.loads((r8 / 'MANIFEST.json').read_text()):
    assert sha(r8 / row['path']) == row['sha256'], row['path']
print('PASS round-8 redacted receipt manifest')
commit = json.loads((scratch / 'evidence-commit.json').read_text())
print('Evidence commit verification:', commit['verification']['verified'], commit['verification']['reason'])
if mismatches:
    raise SystemExit(1)
