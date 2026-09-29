#!/usr/bin/env python3
"""Own MSRP LeaveAll soon after a received bridge LeaveAll (802.1Q-2014 Table 10-5: rLA! restarts
the leavealltimer, so a conformant participant sends no LeaveAll within its 10-15 s draw after one).
usage: leaveall_damping.py <packet author dir>"""
import sys
from pathlib import Path
A = Path(sys.argv[1]); LIM = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
caps = sorted(p.parent for p in A.rglob("msrp.tsv"))
hit, gaps = [], []
for d in caps:
    rows = [l.split("\t") for l in (d / "msrp.tsv").read_text().splitlines()[1:]]
    br = sorted({float(r[0]) for r in rows if r[1] == "bridge" and r[3] == "LeaveAll"})
    own = sorted({float(r[0]) for r in rows if r[1] == "DUT" and r[3] == "LeaveAll"})
    g = [o - max(b for b in br if b < o) for o in own if any(b < o for b in br)]
    g = [x for x in g if x < LIM]
    if g:
        hit.append((d.name, round(min(g), 6))); gaps += g
print(f"captures: {len(caps)}; captures with an own LeaveAll < {LIM} s after a received bridge LeaveAll: {len(hit)}; minimum gap {min(gaps):.6f} s")
print("cycle-022:", [h for h in hit if h[0] == "cycle-022"])
