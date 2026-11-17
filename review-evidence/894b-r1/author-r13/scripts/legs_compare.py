#!/usr/bin/env python3
"""Round 13's 8x8/1if legs against their round 10 measurement on 46cf2a7d's image: for each leg (a build directory
holding results/), each group's simulation log by sha256, its graded text (<group>.txt, its COMMAND, HEAD and END lines
apart) and the leg's table.md (host paths apart), and every value of the group's grade (<group>.json) that differs,
by its path. Prints the receipt; exit 1 when a simulation log or graded text differs, or a grade differs anywhere but
a stated cost the tree states (STATED_KEYS).
usage: python3 -I legs_compare.py NEW_BUILD:OLD_BUILD ..."""
import hashlib
import json
import re
import sys
from pathlib import Path

#: A grade's keys that carry the tree's statements, not a measurement: the stated costs grading reads.
STATED_KEYS = ('reclaim',)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
paths = lambda s: re.sub(r'/data-2/\S*?(?=[\s|)"]|$)', '<path>', s)
bad = []


def walk(a, b, at=''):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            yield from walk(a.get(k), b.get(k), f'{at}.{k}')
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk(x, y, f'{at}[{i}]')
    elif a != b and not (isinstance(a, str) and isinstance(b, str) and paths(a) == paths(b)):
        yield at, a, b


print('# 8x8/1if legs on the head image against round 10 on 46cf2a7d image')
for pair in sys.argv[1:]:
    new, old = (Path(x) / 'results' for x in pair.split(':'))
    print(f'\n## {new.parent.name} against {old.parent.name}')
    tn, to = (paths((d / 'table.md').read_text()) for d in (new, old))
    print(f'- table.md: {"identical" if tn == to else "DIFFERS"} (host paths apart)')
    if tn != to:
        bad.append(f'{new.parent.name} table.md')
    for log in sorted(new.glob('*.log')):
        g = log.stem
        a, b = sha(log), sha(old / log.name)
        keep = lambda p: [l for l in p.read_text().splitlines() if not l.startswith(('COMMAND', 'HEAD', 'END'))]
        txt = keep(new / f'{g}.txt') == keep(old / f'{g}.txt')
        moved = list(walk(json.loads((new / f'{g}.json').read_text()), json.loads((old / f'{g}.json').read_text())))
        print(f'- {g}: log {a[:16]} {"identical" if a == b else "DIFFERS from " + b[:16]}, {log.stat().st_size:,} B; '
              f'graded text {"identical" if txt else "DIFFERS"}; grade values differing: {len(moved)}')
        for at, x, y in moved:
            stated = at.rsplit('.', 1)[-1] in STATED_KEYS
            print(f'  - {at}: {x} (round 10: {y}){", a stated cost the tree states" if stated else ""}')
            if not stated:
                bad.append(f'{g} {at}')
        if a != b or not txt:
            bad.append(g)
print(f'\nRESULT: {"FAIL " + ", ".join(bad) if bad else "PASS: every simulation log and graded text identical"}')
sys.exit(1 if bad else 0)
