#!/usr/bin/env python3
"""Per-member LiteX seconds from hosted job logs: gap from the previous result line
(or the runner selftest line, for the first member) to each member's result line.
usage: member_seconds.py LOG..."""
import re, sys
from datetime import datetime
LINE = re.compile(r"^(\S+Z) (PASS|FAIL|SKIP|TIMEOUT) +(test_\w+)")
SELF = re.compile(r"^(\S+Z) run_litex_sims selftest:")
def ts(s): return datetime.fromisoformat(s[:26].rstrip("Z") if len(s) > 27 else s.rstrip("Z"))
best = {}
for path in sys.argv[1:]:
    prev = None; row = {}
    for line in open(path, errors="replace"):
        m = SELF.match(line)
        if m: prev = ts(m.group(1)); continue
        m = LINE.match(line)
        if m and prev is not None:
            t = ts(m.group(1)); row[m.group(3)] = round((t - prev).total_seconds()); prev = t
    print(path, row, "sum", sum(row.values()))
    for k, v in row.items(): best[k] = max(best.get(k, 0), v)
print("MAX", dict(sorted(best.items())))
