#!/usr/bin/env python3
"""signoff.py <dir>: each signoff corner's WNS/WHS from <dir>/alinx_ax7101_signoff_<corner>_timing.rpt, and whether
every corner meets the build gate's floors (WNS >= +0.030 ns, WHS >= 0). Exit 0 when it does, 1 when not, 2 unread."""
import re, sys
from pathlib import Path
d = Path(sys.argv[1]); rows = {}
for c in ("Slow_85C", "Slow_0C", "Fast_85C", "Fast_0C"):
    p = d / f"alinx_ax7101_signoff_{c}_timing.rpt"
    if not p.exists():
        print(f"{c}: no report"); sys.exit(2)
    t = p.read_text(errors="replace")
    m = re.search(r"\n\s+WNS\(ns\).*\n\s+-+.*\n\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)", t)
    rows[c] = (float(m[1]), int(m[3]), float(m[5]), int(m[7]))
    print(f"{c}: WNS {rows[c][0]:+.3f} ns ({rows[c][1]} failing), WHS {rows[c][2]:+.3f} ns ({rows[c][3]} failing)")
ok = all(w >= 0.030 and h >= 0 for w, _, h, _ in rows.values())
print("floors met at every corner" if ok else "floors NOT met")
sys.exit(0 if ok else 1)
