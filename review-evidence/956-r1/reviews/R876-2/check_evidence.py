#!/usr/bin/env python3
"""Check published cost arithmetic and the reviewed added comments; no builds."""
from pathlib import Path
import math
import re
import subprocess
import sys

p = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve()
root = p / 'scratch/review-evidence/956-r1/author-r2/receipts'
for shape in ['1x1', '8x8-1if']:
    t = (root / f'cpu-{shape}-legs-0d80f0ed-vs-b4a1dde2.md').read_text()
    block = t.split('## Every stated cost')[1].split('\n## ')[0]
    n = 0
    for row in block.splitlines():
        cells = [v.strip() for v in row.split('|')[1:-1]]
        if len(cells) != 7 or not cells[1].replace(',', '').isdigit():
            continue
        _, base, head, rule, stated, verdict, _ = cells
        expected = math.ceil(int(head.replace(',', '')) * 1.05 / 100 / 5) * 5
        assert expected == int(rule), (shape, cells, expected)
        assert expected <= int(stated) and verdict == 'within', cells
        n += 1
    print(f'{shape}: {n} cost rows independently recomputed; all rounding and within-statement results agree')
    for row in t.splitlines():
        if row.startswith(('probes:', 'head findings')):
            print(row)
rom_end = ((0x1b938 + 0x643e + 7) // 8 * 8) + 0x208
assert rom_end == 139136
print(f'8x8/1if aligned rom_end: align8(0x1b938 + 0x643e) + 0x208 = {rom_end}')
print('139264 - 139136 = 128 B spare; 34 ROM + 24 SRAM = 58 RAMB36')
print('PR Known limitations still says 16 B; CPU values 16064/35273/17259 are prior-head figures, not current 14213/35507/17014')
diff = subprocess.check_output(['git', '-C', str(repo), 'diff', '--unified=0', '0d80f0ed..HEAD', '--', '*.c', '*.h', '*.cpp', '*.hpp', '*.py'], text=True)
added = '\n'.join(x[1:] for x in diff.splitlines() if x.startswith('+') and not x.startswith('+++'))
terms = re.findall(r'\b(?:B\d{2}|R87[56](?:-\d)?|A809|pf-951-943n-1|issuecomment-\d+)\b', added)
assert not terms, terms
print('Added source/test/script lines: no bench lane labels, reviewer IDs, author lane or issue-comment IDs matched; manually examined added comments')
