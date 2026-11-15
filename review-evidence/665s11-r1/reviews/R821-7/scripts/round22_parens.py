#!/usr/bin/env python3
"""round22_parens.py REPO HEAD ROUND22: compare every cell of SPLIT_CONTROL_MEMORY.md's polls-by-source table at
HEAD with the same row's cell at ROUND22: a cell "a (b)" must have b equal to round 22's figure, and a bare cell
must equal it; also report each head figure against poll_grade.STATED_US at HEAD. Exit 1 on any difference."""
import re, subprocess, sys
repo, head, r22 = sys.argv[1:]
def show(rev, path):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], check=True, capture_output=True, text=True).stdout
def table(text):
    rows, on = {}, False
    for line in text.splitlines():
        if line.startswith('| Item | Function | Source'): on = True; continue
        if on and not line.startswith('|'): break
        if on and not line.startswith('|---'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            rows[cells[0]] = cells[-2:]
    return rows
doc = 'docs/design/SPLIT_CONTROL_MEMORY.md'
h, r = table(show(head, doc)), table(show(r22, doc))
src = show(head, 'tb/verilator/ctrl_service_budget/poll_grade.py')
m = re.search(r'^STATED_US = \{1: dict\((.*?)\),\s*2: dict\((.*?)\)\}', src, re.S | re.M)
st = {k: dict((a.split('=')[0].strip(), int(a.split('=')[1])) for a in g.replace('\n', ' ').split(',') if '=' in a)
      for k, g in zip((1, 2), m.groups())}
num = lambda s: int(s.replace(',', ''))
bad = parens = 0
for item, cells in h.items():
    key = 'base' if item == 'the base' else item
    for col, (cell, old) in enumerate(zip(cells, r[item]), 1):
        mm = re.fullmatch(r'([\d,]+)(?: \(([\d,]+)\))?', cell)
        now, was = num(mm[1]), num(mm[2]) if mm[2] else num(mm[1])
        parens += bool(mm[2])
        ok = was == num(old) and now == st[col][key]
        bad += not ok
        print(f'{item:9} col{col} head {cell:12} round22 {old:6} STATED_US {st[col][key]:5} {"OK" if ok else "DIFFER"}')
print(f'{parens} parentheses; {len(h)*2} cells; {bad} differing')
sys.exit(1 if bad else 0)
