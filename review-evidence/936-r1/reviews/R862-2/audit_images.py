#!/usr/bin/env python3
"""Compare public image receipts without rebuilding images.
Usage: python3 -B audit_images.py CHECKOUT ARCHIVE_ROOT
"""
import re
import subprocess
import sys
from pathlib import Path

checkout, archive = map(Path, sys.argv[1:3])
prefix = 'review-evidence/936-r1/author-r1/receipts/'
def old(path):
    return subprocess.check_output(['git', '-C', str(checkout), 'show', 'b06d0f563f908f09907579d88b9688c565925dc8:' + prefix + path]).decode()
r2 = archive / 'author-r2/receipts'
new = (r2 / 'final-head/r4-img.log').read_text()
platform = re.compile(r'^POINT (\S+): rom ([\d,]+) B, sram ([\d,]+) B, .*ctrl_plat (\d+) B: PASS$', re.M)
fixture = re.compile(r'^(endstation_\S+ if[12] none): rom ([\d,]+) B in [\d,]+, sram ([\d,]+) B,', re.M)
def rows(pattern, text):
    return {r[0]: tuple(int(x.replace(',', '')) for x in r[1:]) for r in pattern.findall(text)}
for label, pattern, previous in (
    ('platform', platform, old('final/images/plat-ledger-b496c99e.log')),
    ('fixture', fixture, old('final/head-7cfb8a04/images/fix-k.txt')),
):
    a, b = rows(pattern, previous), rows(pattern, new)
    assert len(a) == len(b) == 4
    for point, before in a.items():
        after = b[point]
        expected = 8 if ('if2' in point or label == 'platform' and point == '8x8-if1') else 0
        assert after[0] - before[0] == expected
        assert after[1:] == before[1:]
        print(f'{label} {point}: ROM {before[0]} -> {after[0]} (+{expected}); SRAM and ctrl_plat unchanged')
assert 'plat_ledger: PASS (0 finding(s))' in new
print('PASS: published final-head platform ledger; five existing split images grow by 8 bytes')
for name in ('fix.sha256', 'led.sha256'):
    def hashes(rev):
        text = (r2 / 'images' / rev / name).read_text()
        return sorted(re.findall(r'^([0-9a-f]{64})\s+(\.\/.*)$', text, re.M))
    a, b = hashes('33f24ca3'), hashes('d1aa4c44')
    assert a and a == b
    print(f'PASS: {name}: {len(a)} full image hashes identical between firmware fix and final refactor')
release = (r2 / 'images/d1aa4c44/rel-base.cmp').read_text()
pattern = r'^([0-9a-f]{64})\s+(\.\/.*)$'
same = set(re.findall(pattern, release, re.M))
base = set(re.findall(pattern, old('images/rel-base-IMAGES.sha256'), re.M))
final = set(re.findall(pattern, (r2 / 'images/d1aa4c44/rel-IMAGES.sha256').read_text(), re.M))
assert len(same) == 6 and same <= base and same <= final
print('PASS: six release comparison hashes match both base and final image lists')
for digest, name in sorted(same):
    print(digest, name)
print('Image bytes were not rebuilt here; these are hash and numeric consistency checks of published author receipts.')
