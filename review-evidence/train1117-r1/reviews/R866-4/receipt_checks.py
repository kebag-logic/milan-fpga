#!/usr/bin/env python3
"""Check published coverage, unchanged exceptions and image-identity evidence."""
from pathlib import Path
import re
import subprocess

P = Path(__file__).resolve().parent
A = P / 'scratch/evidence/review-evidence/train1117-r1/author-r6'
for step, point in [('step16', '1x1'), ('step15', '8x8-1if')]:
    f = A / f'receipts/{step}/measure/legs-{point}/parts-rc-{point}.txt'
    rows = [x for x in f.read_text().splitlines() if not x.startswith('====')]
    assert len(rows) == 64 and set(rows) == {'0'}
    print(step, point, '64/64 measurement parts rc=0')

old = (A / 'receipts/step12c/gates/q-0839453f/flip_check.log').read_text()
new = (P / 'flip-all.log').read_text()
over = lambda s: [x for x in s.splitlines() if x.startswith('OVER ')]
assert len(over(new)) == 11 and over(new) == over(old)
print('All-points flip refusal: exactly the prior eleven 8x8/2if lines, unchanged')

hashes = lambda f: {tuple(x.split()[:2]): x.split()[2] for x in f.read_text().splitlines()
                    if len(x.split()) == 3 and re.fullmatch('[0-9a-f]{64}', x.split()[2])}
current = hashes(A / 'receipts/step16/images/hashes.txt')
assert len(current) == 12
prior = hashes(A / 'receipts/step15/images/hashes.txt')
assert len(prior) == 12
kept = {key: value for key, value in current.items() if key[0] != '1x1'}
assert len(kept) == 8 and all(prior[key] == value for key, value in kept.items())
measured = (A / 'receipts/step15/images/img-vs-measured.txt').read_text()
for key, value in kept.items():
    if key[0] == '8x8-1if':
        assert f'{key[0]} {key[1]} fb083864 {value[:16]} measured {value[:16]} EQUAL' in measured
print('Eight 8x8 budget images unchanged; four 8x8/1if measured-hash comparison rows agree')
gate = (A / 'receipts/step16/gates/img.log').read_text()
for digest in current.values():
    assert digest in gate
print('All twelve budget image digests agree between image and gate receipts')
for point in ('1x1', '8x8'):
    d = A / 'receipts/step16/gating' / point
    s = (d / 'signoff.txt').read_text()
    corners = re.findall(r'^(\w+): WNS ([+\d.]+) ns \(0 failing\), WHS ([+\d.]+) ns \(0 failing\)', s, re.M)
    assert len(corners) == 4
    assert all(float(w) >= .030 and float(h) >= 0 for _, w, h in corners)
    assert (A / f'receipts/step16/gating/gate-{point}.log.rc').read_text().strip() == '0'
    print(point, 'four corners meet setup >= .030 ns and hold >= 0 ns:', corners)
    print(point, 'published manifest present:', (d / 'image_manifest.json').exists())

paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', '563c16e5', '--',
                                'review-evidence/train1117-r1']).decode().splitlines()
assert not any(x.endswith('/fg4-bench-images.txt') for x in paths)
print('F1: referenced fg4-bench-images.txt is absent from the entire public archive')
for point in ('1x1', '8x8'):
    print((A / f'receipts/step16/gating/{point}/artifacts.sha256').read_text().strip())
print('Public identity gate checks internal image consistency; it has no product-link comparison input')
print('No ELF or bitstream binaries were rebuilt or independently hashed by this audit')
