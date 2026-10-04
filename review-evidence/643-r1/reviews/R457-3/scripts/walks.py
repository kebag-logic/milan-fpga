#!/usr/bin/env python3
"""R457-2: tabulate, per law window in the given leg logs, the two offset
ranges the harness prints ("the first pop after the end is taken A..B" and
"the pop nearest the boundary C..D"), the walk it reports (the smaller), and
the range of the pop nearest the boundary itself when that range does not
wrap a tick (C and D on the same side of the end and less than half a tick
apart).

usage: walks.py LOG...
"""
import re
import sys

LINE = re.compile(r"\[i\]\s+(T30 [A-Z]+ LAW(?: \+\d+)?): over (\d+) steady PDU ends "
                  r"the first pop after the end is taken ([+-]\d+)\.\.([+-]\d+) cycles "
                  r"from it and the pop nearest the boundary ([+-]\d+)\.\.([+-]\d+) "
                  r"\(walk (\d+)\); the least clearance is (\d+)")
rows = []
for path in sys.argv[1:]:
    for m in LINE.finditer(open(path, errors="replace").read()):
        tag, ends, n0, n1, d0, d1, walk, clear = m.groups()
        n0, n1, d0, d1, walk, clear = map(int, (n0, n1, d0, d1, walk, clear))
        wraps = (d0 <= 0 < d1) or (d1 - d0) > 1000
        near = None if wraps else d1 - d0
        rows.append((path.split("/")[-1], tag, int(ends), n1 - n0, near, walk, clear))
print("log\twindow\tsteady_ends\tnext_range\tnearest_range\treported_walk\tleast_clearance")
for r in rows:
    print("\t".join("-" if x is None else str(x) for x in r))
law = [r for r in rows if "INTERNAL" in r[1]]
crf = [r for r in rows if "CRF" in r[1]]
for name, rs in (("[LAW] windows", law), ("CRF windows", crf)):
    if not rs:
        continue
    print(f"# {name}: {len(rs)}; max reported walk {max(r[5] for r in rs)}; "
          f"max next-pop range {max(r[3] for r in rs)}; max nearest-pop range "
          f"(non-wrapping) {max((r[4] for r in rs if r[4] is not None), default='-')}; "
          f"windows whose nearest-pop range exceeds the reported walk: "
          f"{sum(1 for r in rs if r[4] is not None and r[4] > r[5])}")
