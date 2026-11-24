"""Three-way check of the conflicted plant tables at each merge: the merge holds every name either side holds,
less only a name one side removed from the merge base.

usage: python3 -I union_check.py <names-dir> <merge>:<p1>:<p2>:<base> ...
"""
import json
import sys
from pathlib import Path

d = Path(sys.argv[1])
bad = 0
for spec in sys.argv[2:]:
    m, p1, p2, b = spec.split(":")
    N = {c: json.loads((d / f"{c}.names.json").read_text()) for c in (m, p1, p2, b)}
    for table in ("aecp", "srp", "sink"):
        sets = {c: set(N[c][table]) if isinstance(N[c][table], list) else set() for c in N}
        removed = (sets[b] - sets[p1]) | (sets[b] - sets[p2])
        want = (sets[p1] | sets[p2]) - removed
        lost, extra = want - sets[m], sets[m] - want
        ok = not lost and not extra
        bad += not ok
        print(f"{m} {table}: p1 {len(sets[p1])} p2 {len(sets[p2])} base {len(sets[b])} merge {len(sets[m])} "
              f"expected {len(want)} {'OK' if ok else 'MISMATCH'} lost={sorted(lost)} extra={sorted(extra)}")
    print(f"{m} srp_filters: {N[m]['srp_filters']}")
print("RESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
sys.exit(bad != 0)
