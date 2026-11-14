#!/usr/bin/env python3
"""Check arithmetic and counts in the published exact-head receipts."""
import re
from pathlib import Path

base = Path(__file__).resolve().parent / 'scratch/review-evidence/894-r1/author-r8'
images = (base / 'receipts/images/every-image-final.txt').read_text()
pattern = r'^(# base: )?([^ :]+): rc (\d+) rom (\d+) in (\d+), sram (\d+) in (\d+), tiles ([\d.]+)'
now, old = {}, {}
for m in re.finditer(pattern, images, re.M):
    row = tuple(float(v) if i == 5 else int(v) for i, v in enumerate(m.groups()[2:]))
    (old if m[1] else now)[m[2]] = row
for name, row in now.items():
    rc, rom, rom_cap, sram, sram_cap, tiles = row
    delta = rom - old[name][1]
    print(f'{name}: ROM delta {delta} B; ROM slack {rom_cap-rom} B; SRAM slack {sram_cap-sram} B; {tiles} tiles')
    assert rc == 0 and rom <= rom_cap and sram <= sram_cap
    cap = (59.0 if name.startswith('fixture') else 60.5) if name.endswith('8x8-2if') else 56
    assert tiles <= cap
print('All caps hold. Universal +176 B claim:', all(row[1]-old[name][1] == 176 for name, row in now.items()))

text = (base / 'receipts/gates/harness-head-builds.txt').read_text()
count, unplanted, short, long = 0, 0, [], []
for section in text.split('== ')[1:]:
    label = section.splitlines()[0]
    m = re.search(r'JOINS .*?: (\d+) join interval\(s\), the shortest ([\d.]+) ms and the longest ([\d.]+) ms', section)
    if m:
        n = int(m[1]); count += n; unplanted += n if label != 'C-R1' else 0
        short.append(float(m[2])); long.append(float(m[3]))
print(f'Intervals total {count}, unplanted {unplanted}, shortest {min(short)}, longest {max(long)} ms')

workflow = (base / 'receipts/gates/workflows-verify.md').read_text().splitlines()
rows = [x.split('|') for x in workflow if x.startswith('| ') and len(x.split('|')) == 8][1:]
counts = {}
for row in rows:
    counts[row[5].strip()] = counts.get(row[5].strip(), 0) + 1
print('Workflow receipt statuses:', counts)

missing, mismatched = [], []
import hashlib
for m in re.finditer(r'^\| `([^`]+)` \| [\d,]+ \| `([0-9a-f]{64})`', (base/'INDEX.md').read_text(), re.M):
    p = base/m[1]
    if not p.exists(): missing.append(m[1])
    elif hashlib.sha256(p.read_bytes()).hexdigest() != m[2]: mismatched.append(m[1])
print('Author INDEX missing entries:', missing)
print('Author INDEX differing entries (root manifest hashes were checked separately):', mismatched)
