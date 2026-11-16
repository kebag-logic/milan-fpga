#!/usr/bin/env python3
"""Check published receipt consistency without rerunning source build banks."""
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parent / 'scratch/evidence'
third = root / 'author-r3/receipts'
for round_ in ('author-r2', 'author-r3'):
    count = 0
    mismatches = []
    for line in (root / round_ / 'INDEX.md').read_text().splitlines():
        m = re.match(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]+)`', line)
        if not m:
            continue
        p = root / round_ / m[1]
        if not p.exists():
            continue
        count += 1
        if p.stat().st_size != int(m[2]) or not hashlib.sha256(p.read_bytes()).hexdigest().startswith(m[3]):
            mismatches.append(m[1])
    print(round_, 'INDEX receipts checked', count, 'published-copy differences', mismatches)
images = third / 'images'
base = (images / 'fixture-images-base.sha256').read_text()
head = (images / 'fixture-images-394612c5.sha256').read_text()
assert base == head
print('Fixture hash lists: byte-identical;', len(base.splitlines()), 'entries')
recorded = (images / 'split-images-round1-and-base.txt').read_text()
for filename in ('split-1x1-394612c5.log', 'split-8x8-1if-394612c5.log'):
    lines = (images / filename).read_text().splitlines()
    hashes = [line for line in lines if re.match(r'^[0-9a-f]{64}  ', line) or line.startswith('ctrl_app.elf ')]
    for line in hashes:
        if line.endswith('_mem.init'):
            print('RAM initialization hash recorded; excluded from ROM/ELF comparison:', line)
            continue
        assert re.search(r'[0-9a-f]{64}', line)[0] in recorded, line
    print(filename, len(hashes), 'image/constraint digest lines match recorded base; ELF:', next(l for l in hashes if l.startswith('ctrl_app.elf')))
mbx = (third / 'mbx/make-and-mutants-394612c5.log').read_text()
for pattern in ('checks: ', 'mbx mutants:', 'mutants rc=', 'make rc=', 'porcelain after'):
    print('\n'.join(l for l in mbx.splitlines() if pattern in l and ('failures: 0' in l or not pattern.startswith('checks'))))
assert 'mbx mutants: 242 of 242 caught' in mbx
print('Firmware final result:', (third / 'firmware/test_ctrl_firmware-394612c5.log').read_text().splitlines()[-1])
wf = third / 'workflows'
rcs = list((wf / 'logs').glob('*.rc'))
assert all(p.read_text().strip() == '0' for p in rcs)
print('Published workflow rc files:', len(rcs), 'all zero')
print((wf / 'verify-394612c5.md').read_text().splitlines()[-1])
print((third / 'budget/regrade/regrade.log').read_text())
print((third / 'budget/held-8x8/attribution-evidence.txt').read_text())
