#!/usr/bin/env python3
"""Compare this head's regrade with the previous head's regrade of the same logs.

Every log and per-group JSON must be byte-identical, every results.json key identical but the
composed maximum, whose record may only gain rows, not_run and partial, and table.md may differ
only in its composed maximum line. Prints each arm's composed maximum record and table line.
Usage: compare_regrade.py BASE_RUNS HEAD_RUNS ARM..."""
import json
import sys
from pathlib import Path

ADDED = {'rows', 'not_run', 'partial'}
base, head = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for arm in sys.argv[3:]:
    logs = sorted(p.name for p in (base / arm).glob('*.log'))
    same_logs = [g for g in logs if (base / arm / g).read_bytes() == (head / arm / g).read_bytes()]
    groups = sorted(p.name for p in (base / arm).glob('*.json') if p.name != 'results.json')
    same = [g for g in groups if (base / arm / g).read_bytes() == (head / arm / g).read_bytes()]
    b = json.loads((base / arm / 'results.json').read_text())
    h = json.loads((head / arm / 'results.json').read_text())
    rest_same = set(b) == set(h) and all(h[k] == b[k] for k in b if k != 'composed_maximum')
    bc, hc = b.get('composed_maximum'), h.get('composed_maximum')
    record_ok = (bc is None and hc is None) or (bc is not None and hc is not None and set(hc) - set(bc) == ADDED
                                                and {k: v for k, v in hc.items() if k in bc} == bc)
    bt = (base / arm / 'table.md').read_text().splitlines()
    ht = (head / arm / 'table.md').read_text().splitlines()
    changed = [(x, y) for x, y in zip(bt, ht) if x != y]
    table_ok = len(bt) == len(ht) and all(x.startswith('Composed maximum') for x, _ in changed)
    ok = (len(same_logs) == len(logs) and len(same) == len(groups) and rest_same and record_ok and table_ok)
    bad += not ok
    print(f"{arm}: {len(same_logs)} of {len(logs)} logs and {len(same)} of {len(groups)} group grades "
          f"byte-identical; results.json keys {'identical' if rest_same else 'DIFFER'} but composed_maximum, "
          f"whose record {('is null in both' if hc is None else 'only gains ' + str(sorted(ADDED))) if record_ok else 'DIFFERS'}; "
          f"table.md lines changed: {len(changed)}{'' if table_ok else ' (NOT only the composed maximum line)'}")
    print(f'  composed_maximum: {json.dumps(hc)}')
    for x, y in changed:
        print(f'  table was: {x}\n  table now: {y}')
print(f'compare: {bad} arms differ')
raise SystemExit(1 if bad else 0)
