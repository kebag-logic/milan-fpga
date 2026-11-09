#!/usr/bin/env python3
"""cmp_counts.py <tree> <campaign log> [--only a,b,...]: pair each MUTANTS row of <tree>/tb/srp_top/mutants.py
(the --only subset when the campaign ran with one, in declared order) with its result line in the campaign log,
then, for every README table row that names the arm in backticks in its first cell, compare the first count the row
records (the first later cell that starts with a number) with the measured failures. each suite's README is
read for that suite's rows (tb/<suite>/README.md); a srp_top row whose second cell is a group
name is compared only with that group's run. Prints one line per compared row and the number that differ."""
import ast
import re
import sys
from pathlib import Path

tree, log = Path(sys.argv[1]), Path(sys.argv[2])
only = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
src = (tree / 'tb/srp_top/mutants.py').read_text()
muts = next(ast.literal_eval(n.value) for n in ast.parse(src).body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'MUTANTS')
sel = [m for m in muts if only is None or m[0] in only]
res = [m.group(0) for line in log.read_text().splitlines()
       for m in [re.match(r'^[A-Za-z0-9-]+: rc=\d+ failures=\d+ (KILLED|UNPROVEN)', line)] if m]
assert len(sel) == len(res), (len(sel), len(res))
measured: dict[tuple[str, str, str], set[int]] = {}
for (arm, suite, group, _), line in zip(sel, res):
    assert line.startswith(arm + ':'), (arm, line)
    measured.setdefault((arm, suite, group), set()).add(int(re.search(r'failures=(\d+)', line).group(1)))
readme = {s: (tree / f'tb/{s}/README.md').read_text().splitlines() for s in sorted({m[1] for m in muts})}
groups = {g for (_, s, g) in measured if s == 'srp_top'} | {m[2] for m in muts if m[1] == 'srp_top'}
differ = 0
for (arm, suite, group), got in sorted(measured.items()):
    for no, line in enumerate(readme[suite], 1):
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) < 2 or f'`{arm}`' not in cells[0]:
            continue
        if suite == 'srp_top' and cells[1] in groups and cells[1] != group:
            continue
        rec = next((int(m.group(1)) for c in cells[1:] for m in [re.match(r'^(\d+)\b', c)] if m), None)
        if rec is None:
            continue
        bad = rec not in got or len(got) != 1
        differ += bad
        print(f"{'DIFFERS ' if bad else 'same    '}{suite}:{no} {arm} [{group or '-'}] recorded {rec} "
              f"measured {sorted(got)}")
print(f'{differ} rows differ')
