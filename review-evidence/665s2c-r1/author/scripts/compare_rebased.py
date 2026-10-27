#!/usr/bin/env python3
"""Compare each arm's regrade at the re-based head with its regrade at the pre-rebase head.

The pre-rebase grade is the build's own results directory, regraded in place at 2a7b0df5. Every
per-group graded JSON must be byte-identical (no grade changed); results.json and table.md are
reported key by key and line by line, so each change the round-4 and round-5 rules make is named.
Usage: compare_rebased.py BUILDS REGRADE ARM..."""
import difflib
import json
import sys
from pathlib import Path

builds, regrade = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for arm in sys.argv[3:]:
    base, head = builds / arm / 'results', regrade / arm
    groups = sorted(p.name for p in base.glob('*.json') if p.name != 'results.json')
    changed = [g for g in groups if (base / g).read_bytes() != (head / g).read_bytes()]
    b = json.loads((base / 'results.json').read_text())
    h = json.loads((head / 'results.json').read_text())
    keys = sorted(set(b) | set(h))
    differ = [k for k in keys if b.get(k) != h.get(k)]
    bad += bool(changed)
    print(f"{arm}: {len(groups) - len(changed)} of {len(groups)} group grades byte-identical"
          f"{'' if not changed else ' (CHANGED: ' + ', '.join(changed) + ')'}; results.json keys that differ: "
          f"{differ or 'none'}")
    for k in differ:
        print(f'  results.json {k} was: {json.dumps(b.get(k))}')
        print(f'  results.json {k} now: {json.dumps(h.get(k))}')
    lines = difflib.unified_diff((base / 'table.md').read_text().splitlines(),
                                 (head / 'table.md').read_text().splitlines(), 'before', 'after', n=0, lineterm='')
    for line in list(lines)[2:]:
        print(f'  table {line}')
print(f'compare: {bad} arms with a changed group grade')
raise SystemExit(1 if bad else 0)
