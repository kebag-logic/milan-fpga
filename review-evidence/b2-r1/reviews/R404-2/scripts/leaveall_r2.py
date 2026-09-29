#!/usr/bin/env python3
"""Round-2 check of the cycle-22 attribution numbers (F3).

Counts DUT MSRP LeaveAll PDUs that come less than 10 s after a received
bridge MSRP LeaveAll inside the same capture, both per PDU and per distinct
capture, and prints cycle 22's gap. Same predicate as round 1's
leaveall_damping.py; round 1 printed only the PDU count.

Usage: leaveall_r2.py <archived author dir>
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import replay_b2 as R  # noqa: E402

pkt = Path(sys.argv[1])
TYPES = ("Listener", "TalkerAdvertise", "TalkerFailed", "Domain")
hits, caps, own_total = [], 0, 0
for d in sorted(list((pkt / "cycles").iterdir()) + list((pkt / "bind").iterdir())):
    f = d / "msrp.tsv"
    if not f.exists():
        continue
    caps += 1
    m = R.tsv(f)
    br = sorted({r["t"] for r in m if r["sender"] == "bridge" and r["event"] == "LeaveAll" and r["type"] in TYPES})
    own = sorted({r["t"] for r in m if r["sender"] == "DUT" and r["event"] == "LeaveAll"})
    own_total += len(own)
    for o in own:
        prev = [b for b in br if b < o]
        if prev and o - prev[-1] < 10.0:
            hits.append((d.name, round(o - prev[-1], 6)))
gaps = sorted(h[1] for h in hits)
print("captures with msrp.tsv:", caps)
print("DUT LeaveAll PDU instants in all captures:", own_total)
print("DUT LeaveAll PDUs < 10 s after a received bridge LeaveAll:", len(hits))
print("distinct captures carrying at least one such PDU:", len({h[0] for h in hits}))
print("gap min / median / max s: %.6f / %.6f / %.6f" % (gaps[0], statistics.median(gaps), gaps[-1]))
print("gaps under 1 s:", sum(g < 1.0 for g in gaps))
print("gaps under 9.5 s (Milan Table 4.3 lower bound less tolerance):", sum(g < 9.5 for g in gaps))
print("cycle-022 gaps:", [h[1] for h in hits if h[0] == "cycle-022"])
multi = {}
for h in hits:
    multi[h[0]] = multi.get(h[0], 0) + 1
print("captures with more than one such PDU:", sorted((k, v) for k, v in multi.items() if v > 1))
