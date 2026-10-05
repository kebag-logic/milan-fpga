#!/usr/bin/env python3
"""Grade ADPDU sequences that follow the adopted processor rule (IEEE 1722.1-2021 6.2.2.15 as the
processor implements it at ead80360: ++ after each ENTITY_AVAILABLE, DEPARTING carries the current value,
then 0) with the parent's wire-truth check wt.adp.available-index-advances.
Usage: wire_truth_adp_probe.py <checkout-root>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "tb" / "tools"))
from avtp_wire_truth_frames import build_adp_frame  # noqa: E402
from avtp_wire_truth_checks import WireTruth  # noqa: E402

def frame(kind, idx):
    f = bytearray(build_adp_frame(available_index=idx))
    if kind == "DEP":
        f[14 + 1] = (f[14 + 1] & 0xF0) | 1   # message_type ENTITY_DEPARTING
    return bytes(f)

def grade(seq):
    wt = WireTruth()
    for i, (k, idx) in enumerate(seq):
        wt.feed(float(i), frame(k, idx))
    return [(v.check, v.verdict) for v in wt.check_adp_frame_rule() if "available-index" in v.check]

cases = {
    "normal: AVAIL 0,1 then DEP 2, re-enable AVAIL 0,1": [("AV", 0), ("AV", 1), ("DEP", 2), ("AV", 0), ("AV", 1)],
    "disable during first DELAY: DEP 0, re-enable AVAIL 0,1": [("DEP", 0), ("AV", 0), ("AV", 1)],
}
for name, seq in cases.items():
    print(f"{name}: {grade(seq)}")
