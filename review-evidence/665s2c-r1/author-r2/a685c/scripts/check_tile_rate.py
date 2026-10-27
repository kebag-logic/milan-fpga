#!/usr/bin/env python3
"""R713-1-F2 / R714-1-F2's verification: every row of the README's Vivado table against the rate
the README states, the cacheless 4.5 tiles plus one tile for each 4 KiB of data and half a tile
of tags for each way. Usage: check_tile_rate.py README"""
import re
import sys
from pathlib import Path

readme = Path(sys.argv[1]).read_text()
rate = 'one tile for each 4 KiB of data and half a tile of tags for each way'
print(f'stated: {rate in readme}')
start = readme.index('| Instruction cache | Vivado LUT / FF |')
bad = rows = 0
for line in readme[start:].splitlines()[2:]:
    if not line.startswith('|'):
        break
    cells = [c.strip() for c in line.strip('|').split(' | ')]
    tiles = float(re.search(r'\(([\d.]+)\)', cells[2]).group(1))
    m = re.match(r'(\d+) KiB, (\d+) ways?', cells[0])
    want = 4.5 + (int(m.group(1)) / 4 + 0.5 * int(m.group(2)) if m else 0)
    rows += 1
    bad += tiles != want
    print(f"{'ok ' if tiles == want else 'BAD'} {cells[0]}: {cells[2]} -> rate gives {want:g}")
print(f'{rows} rows, {bad} mismatches')
raise SystemExit(1 if bad or rate not in readme else 0)
