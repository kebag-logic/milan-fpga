#!/usr/bin/env python3
"""Feed the candidate's own judge() the shipping-image figures PR #634 published.

Run from the candidate tree's syn/ooc directory:
    python3 judge_probe.py
The record keeps the baseline's identity (same recipe and tool) and a
different input digest (the candidate's RTL differs from dev 1269cdaf), and
takes LUT, FF, slices, WNS and WHS from PR #634's body. Figures #634 does not
publish (BRAM, DSP, CARRY4) are held at the recorded values, which can only
make the probe more lenient. Read-only: nothing is written.
"""
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd()))
import pp_resource_gate as gate

entry = json.loads(Path("pp_resource_baseline.json").read_text())["endpoints"]["route-1x1"]
candidate = copy.deepcopy(entry["record"])
candidate["inputs_sha256"] = "0" * 64
candidate["figures"].update({"LUT": 50767, "FF": 59634, "SLICE": 15832,
                             "WNS_ns": 0.193, "WHS_ns": 0.024})
status, lines = gate.judge(entry, candidate, [])
print("\n".join(lines))
print(f"judge() exit status: {status}")
