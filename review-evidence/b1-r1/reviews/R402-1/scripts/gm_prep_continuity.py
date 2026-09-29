#!/usr/bin/env python3
"""GPTP_GM_CHANGED continuity across the software-grandmaster prep phases.
The alignment phase of each run precedes its console/controller capture, so a GM change
caused by it would appear as a gap between one run's last and the next run's first count.
usage: gm_prep_continuity.py <packet-root: .../review-evidence/b1-r1>"""
import json, sys
from pathlib import Path
B = Path(sys.argv[1]) / "author" / "bench"
seq = ["cycle10", "gm01", "gm02", "gm03", "gm04", "gm05"]
prev = None
bad = 0
for n in seq:
    ce = json.loads((B / n / "analysis.json").read_text())["counter_endpoints"]
    d = (ce["dut:counter-9-0"]["first"]["5"], ce["peer:counter-9-0"]["first"]["5"])
    e = (ce["dut:counter-9-0"]["last"]["5"], ce["peer:counter-9-0"]["last"]["5"])
    if prev is not None:
        ok = prev == d
        bad += not ok
        print("%s %s first DUT/peer GPTP_GM_CHANGED %s, previous last %s" % ("PASS" if ok else "FAIL", n, d, prev))
    prev = e
print("final DUT/peer GPTP_GM_CHANGED", prev)
sys.exit(1 if bad else 0)
