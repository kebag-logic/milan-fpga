#!/usr/bin/env python3
"""Replay identity/census receipts offline; output only public-safe results.

Usage: python3 check_support.py PACKET_ROOT PROVENANCE_ROOT OUTPUT_ROOT
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys

packet, provenance, output = [Path(x).resolve() for x in sys.argv[1:]]
a = packet / 'author'
scratch = output / 'scratch' / 'support'
scratch.mkdir(parents=True, exist_ok=True)
raw = json.loads((a / 'RAW-ARTIFACTS.json').read_text())['files']
print('Raw index:', len(raw), 'files;', sum(x['bytes'] for x in raw), 'bytes;',
      sum(x['bytes'] > 200000 for x in raw), 'files over 200000 bytes')
for part in ('identity', 'identity-end'):
    dest = scratch / part
    shutil.copytree(a / part, dest, dirs_exist_ok=True)
    args = ['python3', '-B', str(a / 'tools/identity_b15.py'), str(dest)]
    r = subprocess.run(args, capture_output=True, timeout=30)
    assert r.returncode == 0
    same = (dest / 'identity-verdict.txt').read_bytes() == (a / part / 'identity-verdict.txt').read_bytes()
    assert same
    print(part, 'offline replay RC=0; verdict byte-identical')
    # Negative control changes the observed CRC, never a candidate source file.
    path = dest / 'console-identity.txt'
    text = path.read_text()
    assert '5ba355eb' in text
    path.write_text(text.replace('5ba355eb', '00000000'))
    mutant = subprocess.run(args, capture_output=True, timeout=30)
    assert mutant.returncode == 1 and b'IDENTITY GATE: FAIL' in mutant.stdout
    print(part, 'CRC mismatch control RC=1; rejected')

r = subprocess.run(['python3', '-B', str(a / 'tools/census_cmp.py'),
                    str(a / 'restore/census-start.jsonl'), str(a / 'restore/census-end.jsonl')],
                   capture_output=True, timeout=30)
assert r.returncode == 0
assert r.stdout == (a / 'restore/census-compare.txt').read_bytes()
rows = [json.loads(line) for line in r.stdout.splitlines()]
print('Census comparison byte-identical:', rows[0], rows[-1])
for row in rows[1:-1]:
    before, after = row['a'], row['b']
    keys = [key for key in before.keys() | after.keys() if before.get(key) != after.get(key)]
    print('Census differing row', row['index'], 'fields', keys)
assert (a / 'restore/outlets-start.txt').read_bytes() == (a / 'restore/outlets-end.txt').read_bytes()
print('Outlets: starting and closing readbacks byte-identical')
probes = sorted((a / 'box4').glob('counters-probe-*.log'))
assert len(probes) == 2
left, right = [p.read_text().splitlines() for p in probes]
assert len(left) == len(right)
different = [(i + 1, x, y) for i, (x, y) in enumerate(zip(left, right)) if x != y]
assert len(different) == 1 and all(s.startswith('PROBE: DUT entity ') for s in different[0][1:])
print('Counters probes: one differing line (line 4, target identity); all result lines byte-equal')
enums = [json.loads(x) for x in (a / 'box4/enumeration-summary.txt').read_text().splitlines() if x.startswith('{')]
assert len(enums) == 3
for x in enums:
    assert x['complaints_dut'] == 0 and x['total_descriptors'] == 42
    assert set(x['verdict']['compatibility_flags']) == {'IEEE17221', 'MILAN'}
    print('Enumeration', x['run'], 'DUT complaints=0; descriptors=42; compatibility flags agree')
p = json.loads((provenance / 'provenance.json').read_text())
layout = json.loads((provenance / 'flashboot_layout.json').read_text())
assert p['source']['dev_merge'] == '9ef717727e6fdac11ee7f01672fefae948452343'
assert p['build']['aem_desc_sha256'] == layout['aem_image_sha256']
assert p['build']['aem_desc_bytes'] == layout['aem_image_bytes'] == 7512
assert layout['aem_image_crc32'] == int('5ba355eb', 16)
flash = (provenance / 'flash.log').read_text()
for token in ('FLASH_RC=0', 'POWERCYCLE_RC=0', 'write+verify aem', 'write+verify bitstream'):
    assert token in flash, token
print('Provenance: source, AEM hash/size/CRC, verified image writes and successful cold cycle agree')
print('Support checks complete; all operations offline and inside disposable scratch.')
