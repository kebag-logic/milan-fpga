#!/usr/bin/env python3
# R500-1 probe D: DR2c (SAVED_STATE_MATERIALIZATION.md section 15.1) allows at
# most three firmware transaction attempts per UNCHANGED captured work set and
# says "After exhaustion, keep the alarm until reset". This drives the reviewed
# store unchanged over the host flash model with a device that drops every
# program, then (a) a change call that leaves every value as it was (the
# store's own --touch word, a repeated identical SET), and (b) a healthy device.
from __future__ import annotations

import sys

from r500_common import bench

STEM = sys.argv[1] if len(sys.argv) > 1 else "endstation_ax7101_1x1_tdm8"
b = bench(STEM, "reviewed")
golden = b.file("g.bin", b.assemble(b.frames, 5))
rid = max(b.frames)
plen = len(b.frames[rid]) - 8
new = bytes((rid * 13 + j * 11 + 4) & 0xFF for j in range(plen)).hex()
base = ["--slot-b", golden, "--boot", "--fault", "program-drop:99999", "--set", f"{rid}:{new}",
        "--run-ms", "15000"]
cases = {
    "exhausted": base,
    "exhausted_then_identical_change_call": base + ["--touch", str(rid)],
    "identical_change_call_every_5s_for_60s": base + sum(
        (["--touch", str(rid), "--run-ms", "5000"] for _ in range(12)), []),
    "exhausted_then_healthy_new_change": base + ["--fault", "none:0", "--set", f"{rid}:{new[:-2]}00",
                                                 "--until-idle"],
}
keys = ("ok", "failed", "erases", "attempts", "exhausted", "stale", "dirty", "first", "last")
for name, script in cases.items():
    r = b.run(*script)
    print(name, " ".join(f"{k}={r.s.get(k)}" for k in keys))
