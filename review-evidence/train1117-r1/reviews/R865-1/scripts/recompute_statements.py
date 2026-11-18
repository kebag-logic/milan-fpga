#!/usr/bin/env python3
"""Recompute the final head's stated costs from the published survey receipts, by the rule, and compare them with the
head's tables.

usage: recompute_statements.py <clone at the head> <author-r5 receipts dir>

For every row of each survey's compare-ordinary.txt (41d2bc2b at 1x1/1if and 8x8/2if, unit375 at 8x8/1if, the image
that carries the SRP unit at 375 us), the rule (cycles at 100 MHz plus 5 %, rounded up to 5 us) is recomputed and the
row's statement is read again at the head where its source is load_grade.stated(...) or poll_grade.STATED_US[...].
A head statement below its rule is a FAIL. The restated figures of the train (spec-B.json, spec-U-adp.json, the SRP
record) are checked equal to the rule of their cycles and present at the head.
"""
import json
import math
import re
import sys
from pathlib import Path

clone, receipts = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
harness = clone / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(harness))
sys.dont_write_bytecode = True
import load_grade  # noqa: E402
import poll_grade  # noqa: E402
import edit_rows  # noqa: E402


def rule(cycles: int) -> int:
    return int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)


ROW = re.compile(r'^(\S+)\s+([\d,]+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(.*)$')
SOURCES = {'GRADED': load_grade.GRADED, 'STATED_US': load_grade.STATED_US,
           'STATED_US_DONOR': load_grade.STATED_US_DONOR}
fails, checked, moved, unresolved = [], 0, [], 0
for run, point in (('41d2bc2b', '1x1'), ('41d2bc2b', '8x8'), ('unit375', '8x8-1if')):
    f = receipts / 'measure' / run / f'survey-{point}' / 'compare-ordinary.txt'
    for line in f.read_text().splitlines():
        m = ROW.match(line)
        if not m or line.startswith('#'):
            continue
        cost, cycles, _, rcol, stated_col, _, where = m.groups()
        cycles, rcol, stated_col = int(cycles.replace(',', '')), int(rcol), int(stated_col)
        if rule(cycles) != rcol:
            fails.append(f'{run} {point} {cost}: rule column {rcol}, recomputed {rule(cycles)}')
        head = None
        s = re.match(r'load_grade\.stated\(([^)]+)\) (GRADED|STATED_US_DONOR|STATED_US) (\S+);', where)
        p = re.match(r'poll_grade\.STATED_US\[\((\d), (\d), (\d)\)\] (\S+);', where)
        if s:
            pt, table, key = s.groups()
            head = load_grade.stated(clone, pt, SOURCES[table]).get(key)
        elif p:
            shape = tuple(int(x) for x in p.groups()[:3])
            table = poll_grade.STATED_US.get(shape) or {}
            head = table.get(p.group(4))
        if head is None:
            unresolved += 1
            head = stated_col
        checked += 1
        if head != stated_col:
            moved.append(f'{run} {point} {cost}: receipt stated {stated_col}, head {head} ({where[:60]})')
        if cycles and head < rule(cycles):
            fails.append(f'{run} {point} {cost}: head states {head} us under the rule {rule(cycles)} of {cycles:,} '
                         f'cycles ({where[:70]})')

spec = json.loads((receipts / 'regrade/spec-B.json').read_text()) + \
    json.loads((receipts / 'regrade/spec-U-adp.json').read_text()) + \
    [{'table': 'own81', 'point': '8x8/1if', 'key': 'record.srp', 'us': 375, 'cycles': 35547}]
print('restated figure                          cycles   rule  spec  at the head')
for e in spec:
    r = rule(e['cycles'])
    if e['table'] == 'paced':
        head = edit_rows.PACED[e['point']][e['key']]
    elif e['table'] == 'own81':
        head = load_grade.OWN[e['point']][e['key']]
    elif e['table'] == 'e1':
        head = poll_grade.STATED_US[(1, 9, 9)][e['key']]
    elif e['table'] == 's2':
        head = load_grade.GRADED[e['point']][e['key']]
    else:
        head = None
    ok = r == e['us'] == head and e['us'] >= e['cycles'] / 100
    print(f"{e['point']:8} {e['table']:6} {e['key']:16} {e['cycles']:>7,} {r:>6} {e['us']:>5} {head!s:>6}  "
          f"{'OK' if ok else 'FAIL'}")
    if not ok:
        fails.append(f"restated {e['point']} {e['key']}: rule {r}, spec {e['us']}, head {head}")
print(f'{checked} survey rows checked ({unresolved} read from the receipt, their source not a table this reads)')
for m in moved:
    print('MOVED', m)
for f in fails:
    print('FAIL', f)
print('RESULT:', 'FAIL' if fails else 'PASS')
sys.exit(1 if fails else 0)
