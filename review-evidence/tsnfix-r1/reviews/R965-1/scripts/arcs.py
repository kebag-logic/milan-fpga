#!/usr/bin/env python3
"""arcs.py SRC BUILD: per-line gcov arcs of src/adp.c and per-function arc totals of adp.c and acmp.c,
read with SRC's own scripts/coverage.py reader, before exclusions."""
import sys
from pathlib import Path
src, build = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(src / "scripts"))
import coverage as reader
merged = reader.collect([build])
for rel in ("src/adp.c", "src/acmp.c"):
    s = merged[rel]
    text = (src / rel).read_text().splitlines()
    def owner(n):
        return next((f for f, (a, b) in s.functions.items() if a <= n <= b), "?")
    per_fn = {}
    for n in sorted(s.lines):
        ln = s.lines[n]
        per_fn.setdefault(owner(n), [0, 0])
        per_fn[owner(n)][0] += 1
        per_fn[owner(n)][1] += len(ln.arcs)
        if rel == "src/adp.c" and ln.arcs:
            print(f"{rel}:{n:<4} {owner(n):28} arcs={ln.arcs} uncovered={sum(1 for a in ln.arcs if a == 0)}  {text[n-1].strip()[:90]}")
    print(f"{rel} raw: lines {sum(1 for l in s.lines.values() if l.count > 0)}/{len(s.lines)} arcs {sum(1 for l in s.lines.values() for a in l.arcs if a > 0)}/{sum(len(l.arcs) for l in s.lines.values())}")
    for f, (nl, na) in sorted(per_fn.items()):
        print(f"  {rel} fn {f:34} lines {nl:4} arcs {na:4}")
