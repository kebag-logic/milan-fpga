#!/usr/bin/env python3
# R500-1 probe T: the LiteSPI port's time base is the fabric PHC, held at its
# last value when the PHC steps backwards (plat/nvm_flash_litespi.c ls_now_us).
# A grandmaster restart steps domain time backwards by the grandmaster's whole
# previous uptime (docs/design/PRESENTATION_TIME_WRAP.md). This drives the
# reviewed store over the reviewed LiteSPI port and moves only the modelled PHC.
from __future__ import annotations

import sys

from r500_common import PHC_SEAMS, bench, planted_tree

STEM = sys.argv[1] if len(sys.argv) > 1 else "endstation_ax7101_1x1_tdm8"
tree = planted_tree("phc_harness", PHC_SEAMS)
b = bench(STEM, "phc_harness", tree)
golden = b.file("g.bin", b.assemble(b.frames, 5))
rid = max(b.frames)
plen = len(b.frames[rid]) - 8
new = bytes((rid * 13 + j * 11 + 9) & 0xFF for j in range(plen)).hex()
HOUR = "3600000"

cases = {
    # control: no PHC step; the change commits about 1 s after it is made
    "control_no_step": ["--litespi", "--phc-shift-ms", HOUR, "--slot-b", golden, "--boot",
                        "--set", f"{rid}:{new}", "--run-ms", "10000"],
    # the PHC steps back 60 s, 200 ms after the change: nothing commits in the next 10 s
    "back_60s_after_change": ["--litespi", "--phc-shift-ms", HOUR, "--slot-b", golden, "--boot",
                              "--set", f"{rid}:{new}", "--run-ms", "200",
                              "--phc-shift-ms", "-60000", "--run-ms", "10000"],
    # the same, but run 61 s after the step: the commit only lands once the PHC
    # has climbed back past the held value
    "back_60s_then_70s": ["--litespi", "--phc-shift-ms", HOUR, "--slot-b", golden, "--boot",
                          "--set", f"{rid}:{new}", "--run-ms", "200",
                          "--phc-shift-ms", "-60000", "--run-ms", "70000"],
    # a step back of 30 minutes, then 10 minutes of running: still nothing durable
    "back_30min_then_10min": ["--litespi", "--phc-shift-ms", HOUR, "--slot-b", golden, "--boot",
                              "--set", f"{rid}:{new}", "--run-ms", "200",
                              "--phc-shift-ms", "-1800000", "--run-ms", "600000"],
    # forward steps during a 3 s erase: each ends the wait early as a failed
    # attempt; three of them exhaust a healthy device's work set
    "forward_steps_in_erase": ["--litespi", "--phc-shift-ms", HOUR,
                               "--slot-b", golden, "--boot", "--times", "3000:1000",
                               "--set", f"{rid}:{new}",
                               "--run-ms", "1100", "--phc-shift-ms", "60000", "--run-ms", "1100",
                               "--phc-shift-ms", "60000", "--run-ms", "1100",
                               "--phc-shift-ms", "60000", "--run-ms", "20000"],
}
keys = ("ok", "failed", "erases", "dirty", "pending", "exhausted", "attempts", "first", "last",
        "phase", "now_ms")
for name, script in cases.items():
    r = b.run(*script)
    print(name, " ".join(f"{k}={r.s.get(k)}" for k in keys), "ERASES_US", r.erases)
