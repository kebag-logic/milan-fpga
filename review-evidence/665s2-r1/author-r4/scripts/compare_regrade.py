#!/usr/bin/env python3
"""Compare a head regrade with the base regrade of the same logs: every per-group JSON and every
results.json key must be identical, but the composed maximum the head adds; print it per arm.
Usage: compare_regrade.py BASE_RUNS HEAD_RUNS ARM..."""
import json
import sys
from pathlib import Path

base, head = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for arm in sys.argv[3:]:
    groups = sorted(p.name for p in (base / arm).glob('*.json') if p.name != 'results.json')
    same = [g for g in groups if (base / arm / g).read_bytes() == (head / arm / g).read_bytes()]
    b = json.loads((base / arm / 'results.json').read_text())
    h = json.loads((head / arm / 'results.json').read_text())
    added = sorted(set(h) - set(b))
    rest = {k: v for k, v in h.items() if k in b}
    ok = len(same) == len(groups) and rest == b and set(b) <= set(h)
    bad += not ok
    print(f"{arm}: {len(same)} of {len(groups)} group grades byte-identical; results.json keys "
          f"{'identical' if rest == b else 'DIFFER'} but the added {added}; composed_maximum "
          f"{json.dumps(h.get('composed_maximum'))}")
print(f'compare: {bad} arms differ')
raise SystemExit(1 if bad else 0)
