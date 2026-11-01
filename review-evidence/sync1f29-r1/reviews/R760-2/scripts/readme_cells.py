#!/usr/bin/env python3
"""readme_cells.py HEAD_TREE BOOTDIR WINDOWS_HEAD WINDOWS_NOSTAGE: compares each restated README cell with this round's own runs."""

import re, sys
from pathlib import Path
tree, boot, wh, wn = map(Path, sys.argv[1:5])
bad = 0
boot_md = (tree / 'tb/verilator/ctrl_split_boot/README.md').read_text()
for shape, s in (('1x1', '1x1, one interface'), ('8x8', '8x8, one interface')):
    for stage, tag in (('staged', 'staged'), ('none', 'nostage')):
        row = next(l for l in boot_md.splitlines() if l.startswith(f'| {s} | {stage} |'))
        cells = [c.strip() for c in row.strip('|').split('|')]
        log = (boot / f'{tag}-{shape}.log').read_text()
        m = re.search(r'BOOT ready at bus cycle \d+ \((\d+) CPU cycles\): ([\d.]+) ms', log)
        st = re.search(r'UART milan_status: .*span ([\d.]+) ms; to the first byte ([\d.]+) ms; longest gap between bytes ([\d.]+) ms', log)
        gt = re.findall(r'UART milan_gettime: .*span ([\d.]+) ms; to the first byte ([\d.]+) ms; longest gap between bytes ([\d.]+) ms', log)
        worst = [f'{max(float(g[i]) for g in gt):.3f}' for i in range(3)]
        want = [f'{m.group(2)} ms', f'{int(m.group(1)):,}', '18 of 18 equal', ' / '.join(st.groups()) + ' ms', ' / '.join(worst) + ' ms']
        ok = cells[2:] == want
        bad += not ok
        print('ok ' if ok else 'BAD', shape, stage, cells[2:], '' if ok else want)
md = (tree / 'tb/verilator/ctrl_service_budget/README.md').read_text()
for stage, f in (('staged', wh), ('none', wn)):
    for line in f.read_text().splitlines():
        m = re.match(r"(\S+): GM committed (\d+) of defined 15; ring depth 16; occupancy at open (\d+); passes (\d+); longest [\d,]+ CPU cycles \(([\d.]+) ms\); window ([\d.]+) ms; unreleased (\{.*\})", line)
        if not m:
            continue
        name, gm, _, passes, longest, window, unrel = m.groups()
        un = ', '.join(f'{k} {v}' for k, v in eval(unrel).items())
        graded = 'yes' if gm == '15' else 'refused'
        want = f'| `{name}` | {stage} | {gm} | {graded} | {float(window) + 1e-9:.2f} | {passes} | {float(longest) + 1e-9:.2f} | {un} |'
        ok = want in md
        bad += not ok
        print('ok ' if ok else 'BAD', want)
print('mismatches:', bad)
sys.exit(bool(bad))
