#!/usr/bin/env python3
"""Round-2 check of the S2 wording: DUT MSRP PDU spacing in the baseline and
final captures, and the class of every DUT PDU off the 1.000 s periodic grid.

Usage: msrp_spacing_r2.py <archived author dir>
Classes: 'reply' (within 10 ms after a bridge LeaveAll), 'own LeaveAll'
(the PDU carries a DUT LeaveAll), 'join after own LeaveAll' (0.2 s +- 2 ms
after the DUT's own LeaveAll), else 'UNEXPLAINED'.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import replay_b2 as R  # noqa: E402

pkt = Path(sys.argv[1])
bad = 0
for cap in ("baseline", "final"):
    m = R.tsv(pkt / "bind" / cap / "msrp.tsv")
    dut = sorted({r["t"] for r in m if r["sender"] == "DUT"})
    own_la = sorted({r["t"] for r in m if r["sender"] == "DUT" and r["event"] == "LeaveAll"})
    br_la = sorted({r["t"] for r in m if r["sender"] == "bridge" and r["event"] == "LeaveAll"})
    grid0 = dut[0]
    gaps = [round(b - a, 6) for a, b in zip(dut, dut[1:])]
    print(f"== {cap}: {len(dut)} DUT PDUs, spacing min {min(gaps):.6f} max {max(gaps):.6f} s")
    for t in dut:
        phase = (t - grid0) % 1.0
        on_grid = min(phase, 1.0 - phase) < 0.001
        cls = []
        if any(0 <= t - b < 0.010 for b in br_la):
            cls.append("reply")
        if t in own_la:
            cls.append("own LeaveAll")
        if any(abs(t - o - 0.2) < 0.002 for o in own_la):
            cls.append("join after own LeaveAll")
        if not on_grid:
            if not cls:
                bad += 1
                cls.append("UNEXPLAINED")
            print(f"   off-grid {t:.6f}: {', '.join(cls)}")
        elif cls:
            print(f"   on-grid  {t:.6f}: also {', '.join(cls)}")
print("unexplained off-grid DUT PDUs:", bad)
