#!/usr/bin/env python3
"""Check the public archive's receipt integrity and numerical summaries."""
from pathlib import Path
import hashlib
import json
import re
import sys

archive = Path(sys.argv[1])
rows = json.loads((archive / 'MANIFEST.json').read_text())
for row in rows:
    p = archive / row['file']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == row['published_sha256'], row['file']
print('Published manifest:', len(rows), 'files match')
p = archive / 'author-r1/receipts'
images = (p / 'images/SUMMARY.txt').read_text().splitlines()[1:]
assert len(images) == 20
assert all('inputs differing: 1 of' in r and 'srp_mbx.o' in r and 'relinks equal to built: 2/2' in r
           and '3 differ' in r and r.endswith('rc 0') for r in images)
for f in sorted((p / 'images/pairs').glob('*.relink.txt')):
    t = f.read_text()
    assert t.count('EQUAL to the built image') == 2
    changed = [l for l in t.splitlines() if l.startswith(('+','-')) and not l.startswith(('+++','---'))]
    assert len(changed) == 3, f.name
    print(f.name, '; '.join(changed))

shifts = {}
for f in sorted((p / 'images/pairs').glob('*.imgdiff.txt')):
    line = next(l for l in f.read_text().splitlines() if l.startswith('  .rodata PROGBITS'))
    addresses = re.findall(r'addr 0x([0-9a-f]+)', line)
    shift = int(addresses[1], 16) - int(addresses[0], 16)
    shifts[shift] = shifts.get(shift, 0) + 1
    print(f.name, '.rodata placement delta', shift, 'bytes')
assert shifts == {0: 13, 8: 7}
print('rodata placement distribution:', shifts)

def blocks(path):
    result, block = [], []
    for line in path.read_text().splitlines():
        if line.startswith('## '):
            if block:
                result.append(block)
            block = []
        elif line and not line.startswith('#'):
            block.append(line)
    if block:
        result.append(block)
    return result

budget = blocks(p / 'images/budget-hashes.txt')
plat = blocks(p / 'images/platform-and-fixture-hashes.txt')
assert budget[-1] == budget[-2] and len(budget[-1]) == 12
assert plat[-1] == plat[-2] and len(plat[-1]) == 8
print('e5dee83b to 4224df63: all 20 image hashes equal')

def hashes(path):
    return {line.split(None,1)[1]: line.split(None,1)[0] for line in path.read_text().splitlines()}
b, h = [hashes(p / f'images/release-{side}.sha256') for side in ('base','head')]
assert b.keys() == h.keys()
for key in b:
    equal = b[key] == h[key]
    print('release', key, 'EQUAL' if equal else 'DIFFERENT')
    if key.endswith(('bios.bin','bios.elf','mem.init','rom.init','sram.init','member milan_baremetal.o',
                     '(outside its // comment lines)')):
        assert equal

total, largest = 0, (0, '')
for f in sorted((p / 'cpu/compare').glob('*-probes.txt')):
    rows = [line.split('|')[1:-1] for line in f.read_text().splitlines() if line.startswith('| `')]
    total += len(rows)
    misses = 0
    for row in rows:
        old, new = row[5].strip().split(' / ')
        assert old == new
        misses += old == 'MISS'
        delta = float(row[3])
        if abs(delta) > largest[0]:
            largest = (abs(delta), f'{f.name} {row[0].strip()} {delta:+.3f} ms')
    print(f.name, len(rows), 'unchanged verdicts;', misses, 'misses per image')
assert total == 156
print('Total paired probes:', total, 'largest change:', largest[1])
for n in range(4):
    t=(p/f'gates/4224df63/firmware-gate-shard{n}.txt').read_text()
    assert 'test_ctrl_firmware: PASS' in t and 'END rc=0' in t and '[ESCAPED]' not in t
    print('firmware shard',n,'ok lines',t.count('[ok]'),'test verdicts',t.count('verdict: PASS'),
          'talker plants',t.count('[ok] talker-'))
assert 'mutants: 825 of 825 caught' in (p/'gates/4224df63/firmware-gate-shard1.txt').read_text()
assert 'firmware coverage: PASS (40 files)' in (p/'gates/4224df63/fw-coverage.txt').read_text()
t=(p/'gates/final/docs-workflow-steps.txt').read_text()
assert len(re.findall(r'^\d+.*rc=0',t,re.M)) == 104
print('docs: 104 rc=0 rows')
for f in ('gates/4224df63/twin.txt','gates/final/builder-leg-0.txt','gates/final/builder-leg-1.txt'):
    t=(p/f).read_text()
    assert 'END rc=0' in t
    print(f, '\n'.join(l for l in t.splitlines() if 'NOT RUN' in l or 'rc=' in l))
print('RESULT PASS; this audits published receipts, not new image builds or CPU simulations')
