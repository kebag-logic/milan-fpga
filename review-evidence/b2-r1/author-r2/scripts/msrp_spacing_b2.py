#!/usr/bin/env python3
"""DUT MSRP PDU spacing in the baseline and final captures (R404-1 S2, R405-1 S2).

usage: msrp_spacing_b2.py <round-1 packet author dir>

One DUT MRPDU is one distinct DUT timestamp in bind/<capture>/msrp.tsv. The
first DUT MRPDU sets a 1.000 s grid. Every DUT MRPDU off that grid is labelled:
its reply to a bridge LeaveAll (within 0.05 s after one), its own LeaveAll, or
the PDU one 0.2 s join period after its own LeaveAll. Exit 0 only when every
off-grid DUT MRPDU carries one of those labels. Times only; no identifier.
"""
import sys
from pathlib import Path

A = Path(sys.argv[1])
bad = 0
for w in ("baseline", "final"):
    rows = [l.split("\t") for l in (A / "bind" / w / "msrp.tsv").read_text().splitlines()[1:] if l.strip()]
    dut = sorted({float(r[0]) for r in rows if r[1] == "DUT"})
    own_la = sorted({float(r[0]) for r in rows if r[1] == "DUT" and r[3] == "LeaveAll"})
    br_la = sorted({float(r[0]) for r in rows if r[1] == "bridge" and r[3] == "LeaveAll"})
    gaps = [round(b - a, 3) for a, b in zip(dut, dut[1:])]
    print(f"== {w}: {len(dut)} DUT MRPDUs; gaps, s: {gaps}")
    print(f"   bridge LeaveAll at {[round(x, 3) for x in br_la]}; DUT LeaveAll at {[round(x, 3) for x in own_la]}")
    on = 0
    for t in dut:
        if round((t - dut[0]) % 1.0, 3) in (0.0, 1.0):
            on += 1
            continue
        if t in own_la:
            lab = "own LeaveAll, %.3f s after the bridge's" % (t - max(b for b in br_la if b < t)) if any(b < t for b in br_la) else "own LeaveAll"
        elif any(0 <= t - b <= 0.05 for b in br_la):
            lab = "reply %.3f s after the bridge's LeaveAll" % min(t - b for b in br_la if t >= b)
        elif any(abs(t - o - 0.2) < 0.002 for o in own_la):
            lab = "0.200 s after its own LeaveAll"
        else:
            lab = "UNEXPLAINED"
            bad += 1
        print(f"   off-grid {t:.3f}: {lab}")
    after = [round(min(t for t in dut if t > o) - o, 3) for o in own_la if any(t > o for t in dut)]
    print(f"   on the 1.000 s grid: {on} of {len(dut)}; next DUT MRPDU after each own LeaveAll, s: {after}")
print("RESULT", "PASS" if bad == 0 else "FAIL")
sys.exit(1 if bad else 0)
