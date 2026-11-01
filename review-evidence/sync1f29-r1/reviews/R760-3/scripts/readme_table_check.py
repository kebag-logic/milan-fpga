#!/usr/bin/env python3
"""readme_table_check.py TREE RAWDIR README: compare every cell of the README's window table with the raw logs read through TREE's grade.py. Exit 1 on any mismatch."""
import re, sys
from pathlib import Path
tree, raw, readme = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
sys.dont_write_bytecode = True
sys.path[:0] = [str(tree / 'tb/verilator/ctrl_service_budget'), str(tree / 'sw/mailbox'), str(tree / 'sw/litex')]
import grade
ARM = {'staged': 'head', 'none': 'nostage'}
rows = re.findall(r'^\| `(backlog[a-z-]*)` \| (staged|none) \| (\d+) \| (yes|refused) \| ([\d.]+) \| (\d+) \| ([\d.]+) \| ([^|]+) \|$', readme.read_text(), re.M)
bad = cells = 0
for name, stage, gm, graded, win, passes, longest, un in rows:
    log = grade.parse((raw / f'{ARM[stage]}-xip64-{name}.log').read_text(), 100_000_000, 50_000_000)
    marks = dict((n, c) for c, n in log.marks)
    s, e = marks['composed'], marks['composed_end']
    ps = grade.composed_passes(log, s, e)
    u = ', '.join(f'{k} {v}' for k, v in sorted(grade.unreleased(log, s, e).items()) if v)
    want = {'GM': str(grade.population(log, s, e)['GM']), 'graded': 'yes' if grade.population(log, s, e)['GM'] == 15 else 'refused',
            'window': f'{(e - s) / 100000:.2f}', 'passes': str(len(ps)), 'longest': f'{max(p.cycles for p in ps) / 50000:.2f}', 'unreleased': u}
    got = {'GM': gm, 'graded': graded, 'window': win, 'passes': passes, 'longest': longest, 'unreleased': un.strip()}
    for k in want:
        cells += 1
        if want[k] != got[k]:
            bad += 1
            print(f'MISMATCH {name} {stage} {k}: README {got[k]!r}, logs {want[k]!r}')
print(f'{len(rows)} rows, {cells} cells, {bad} mismatches')
sys.exit(1 if bad or len(rows) != 8 else 0)
