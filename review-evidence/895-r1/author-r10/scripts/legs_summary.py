#!/usr/bin/env python3
"""legs_summary.py LOG...: each harness leg log's verdict line (groups graded, refusals, budget misses, passes over the
share), its STATED lines, and its join intervals (the JOINS lines join_grade.py prints per group run), then the join
intervals over every log given: their count, group runs, shortest and longest, against 181.0 to 239.0 ms (#894's egress
ruling of 2026-11-13, item 1). Exit 1 when any interval is outside that range or any log has no verdict line."""
import re
import sys
from pathlib import Path

JOIN = re.compile(r'^JOINS (\S+): (\d+) join interval\(s\), the shortest ([\d.]+) ms and the longest ([\d.]+) ms')
LO, HI = 181.0, 239.0
total, runs, low, high, bad = 0, 0, None, None, False
for p in map(Path, sys.argv[1:]):
    text = p.read_text(errors='replace').splitlines()
    verdict = next((l for l in reversed(text) if 'groups graded' in l), None)
    stated = [l for l in text if l.startswith('STATED')]
    n = lo = hi = None
    count = 0
    for l in text:
        m = JOIN.match(l)
        if m:
            k, a, b = int(m[2]), float(m[3]), float(m[4])
            count += k
            runs += 1
            lo = a if lo is None else min(lo, a)
            hi = b if hi is None else max(hi, b)
    total += count
    if lo is not None:
        low = lo if low is None else min(low, lo)
        high = hi if high is None else max(high, hi)
        bad = bad or lo < LO or hi > HI
    bad = bad or verdict is None
    print(f'{p.name}: {verdict or "NO VERDICT LINE"}; STATED lines {len(stated)}; joins {count}'
          + (f', {lo:.3f} to {hi:.3f} ms' if lo is not None else ''))
print(f'JOIN INTERVALS: {total} in {runs} group runs, {low:.3f} to {high:.3f} ms, against {LO} to {HI}: '
      f'{"OUTSIDE" if bad else "all within"}')
sys.exit(1 if bad else 0)
