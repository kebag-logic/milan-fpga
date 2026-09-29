#!/usr/bin/env python3
"""Compare a re-run of the author's analyzer on archived raw console/controller/events
against the archived analysis.json; wire (tap) fields are skipped because no tap pcap is archived.
usage: compare_rerun.py <rerun-bench-dir> <archived-bench-dir> <name>..."""
import json, sys
from pathlib import Path
rr, ar = Path(sys.argv[1]), Path(sys.argv[2])
WIRE = {"wire", "tap_records", "tap_anchor_spread_s", "announce_gm", "clock_offset_s", "clock_half_rtt_s"}
bad = 0
for n in sys.argv[3:]:
    x = json.loads((rr / n / "analysis.json").read_text()); y = json.loads((ar / n / "analysis.json").read_text())
    keys = sorted(set(x) | set(y))
    for k in keys:
        if k in WIRE:
            continue
        same = x.get(k) == y.get(k)
        bad += not same
        print(("SAME " if same else "DIFF ") + n + " " + k + ("" if same else " rerun=%s archived=%s" % (str(x.get(k))[:200], str(y.get(k))[:200])))
print("TOTAL diff=%d" % bad); sys.exit(1 if bad else 0)
