#!/usr/bin/env python3
"""Reviewer probe: point test_builder.py's two #386 render-recentre anchors at
the head's RTL text in a disposable tree, to see whether anything else in
test_baremetal_profile_contract refuses the #387 datapath. Not a proposed fix.
Usage: builder_pin_probe.py <tree>"""
import sys
from pathlib import Path

p = Path(sys.argv[1]) / "sw/builder/test_builder.py"
t = p.read_text()
reps = [
    ('"gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load "\n            "| src_recentre_p_r",',
     '"media_rebase_p_w | src_recentre_p_r",'),
    ('"       gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load\\n"\n        "       | src_recentre_p_r;",\n        "       gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load\\n"\n        "       | src_recentre_p_r | cfg_adp_enable;",',
     '"       media_rebase_p_w\\n"\n        "       | src_recentre_p_r;",\n        "       media_rebase_p_w\\n"\n        "       | src_recentre_p_r | cfg_adp_enable;",'),
]
for a, b in reps:
    n = t.count(a)
    if n != 1:
        sys.exit(f"anchor count {n} != 1: {a[:60]!r}")
    t = t.replace(a, b)
p.write_text(t)
print("re-pointed 2 anchors")
