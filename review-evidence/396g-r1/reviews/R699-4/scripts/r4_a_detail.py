#!/usr/bin/env python3
"""located_within of the remaining r3_probe group-A deviations at this head.

Usage: python3 -I r4_a_detail.py <path-to-tb/tools> <dir holding r3_probe.py>
"""
import json
import sys

sys.path.insert(0, sys.argv[2])
sys.argv = [sys.argv[0], sys.argv[1]]
import r3_probe as p  # noqa: E402

for name, at, ops in (("A-drop4096-40-after-flip", 740, [("shift", 740, 4096)]),
                      ("A-drop4096-900-after-repeat", 1400, [("shift", 1400, 4096)]),
                      ("A-drop4096-5-after-repeat", 505, [("shift", 505, 4096)]),
                      ("A-drop4096-5-after-flip", 705, [("shift", 705, 4096)])):
    v, d, dut = p.grade(16384, ops)
    inside = all(e.get("located_within", [e["capture_index"]] * 2)[0] <= at <= e.get("located_within", [e["capture_index"]] * 2)[1]
                 for e in dut)
    print(name, v, "arms-missed", len(d["planted_missed"]), "true-sample-inside-every-event", inside,
          json.dumps([p.brief(e) for e in dut]))
