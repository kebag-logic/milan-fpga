#!/usr/bin/env python3
"""Count own (DUT) MSRP LeaveAlls that follow a received bridge MSRP LeaveAll
inside the same capture. Under 802.1Q-2014 Table 10-5 / 10.6 a received
LeaveAll restarts the local leavealltimer (10-15 s, Milan Table 4.3), so an own
LeaveAll less than 10 s after a received one is the processor's open
deviation (processor issue #108). Usage: leaveall_damping.py <packet author dir>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import replay_b2 as R
pkt = Path(sys.argv[1])
hits = []
caps = 0
for d in sorted(list((pkt / "cycles").iterdir()) + list((pkt / "bind").iterdir())):
    f = d / "msrp.tsv"
    if not f.exists():
        continue
    caps += 1
    m = R.tsv(f)
    br = sorted({r["t"] for r in m if r["sender"] == "bridge" and r["event"] == "LeaveAll"
                 and r["type"] in ("Listener", "TalkerAdvertise", "TalkerFailed", "Domain")})
    own = sorted({r["t"] for r in m if r["sender"] == "DUT" and r["event"] == "LeaveAll"})
    for o in own:
        prev = [b for b in br if b < o]
        if prev and o - prev[-1] < 10.0:
            hits.append((d.name, round(o - prev[-1], 6)))
print("captures", caps, "own LeaveAll < 10 s after a received bridge LeaveAll:", len(hits))
gaps = sorted(h[1] for h in hits)
if gaps:
    print("gap min/median/max s", gaps[0], gaps[len(gaps) // 2], gaps[-1])
for h in hits:
    if h[0] == "cycle-022" or h[1] < 1.0:
        print(" ", h)
