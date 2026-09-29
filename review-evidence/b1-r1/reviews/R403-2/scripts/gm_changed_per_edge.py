#!/usr/bin/env python3
"""Split the DUT's GPTP_GM_CHANGED (AVB_INTERFACE counter bit 5) and the DUT
CLOCK_DOMAIN LOCKED/UNLOCKED counters of each software-grandmaster run into
the takeover and release edge, from the archived per-run analysis.json, and
count the grandmaster changes the console and the wire saw per edge.

usage: gm_changed_per_edge.py <packet-r1-dir>
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "bench"
MID = 27.0  # seconds after gm start: between the takeover (~4 s) and release (~50 s) edges
for n in range(1, 6):
    a = json.loads((root / f"gm{n:02d}" / "analysis.json").read_text())
    tr = a["counter_transitions"]

    def split(key, bit):
        pts = tr[key]
        first = pts[0][1][bit]
        at_mid = [v[bit] for t, v in pts if t < MID][-1]
        last = pts[-1][1][bit]
        return at_mid - first, last - at_mid

    gm = split("dut:counter-9-0", "5")
    cd_key = next(k for k in tr if k.startswith("dut:counter-36"))
    lk, ul = split(cd_key, "0"), split(cd_key, "1")
    cons = [t for t, _ in a["gm"]][1:]
    wire = [t for t, _ in a["announce_gm"]][1:]
    print(f"gm{n:02d}: GPTP_GM_CHANGED takeover +{gm[0]} release +{gm[1]}; "
          f"CLOCK_DOMAIN LOCKED +{lk[0]}/+{lk[1]} UNLOCKED +{ul[0]}/+{ul[1]}; "
          f"console GM changes {len(cons)} at {cons}; wire Announce GM changes {len(wire)}")
