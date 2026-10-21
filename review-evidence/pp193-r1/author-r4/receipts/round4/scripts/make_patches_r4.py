#!/usr/bin/env python3
"""Write the round-4 mutation patch as one exact textual edit of the head RTL.

usage: make_patches_r4.py <processor tree>   (writes tb/srp_top/mutations/<label>.patch)
"""
import difflib
import sys
from pathlib import Path

tree = Path(sys.argv[1])
rel = "hdl/srp/KL_srp_listener_fsm.sv"
src = (tree / rel).read_text()

EDITS = {
    # the done strobe at the end of the first pass, the second pass kept
    "listener-walk-done-before-second-pass": (
        "          txop_done_o <= &wdone_r;\n",
        "          txop_done_o <= 1'b1;\n"),
}

out = tree / "tb" / "srp_top" / "mutations"
for label, (old, new) in EDITS.items():
    if src.count(old) != 1:
        sys.exit(f"{label}: the edit's anchor occurs {src.count(old)} times")
    mutated = src.replace(old, new)
    diff = difflib.unified_diff(src.splitlines(keepends=True),
                                mutated.splitlines(keepends=True),
                                fromfile="a/" + rel, tofile="b/" + rel, n=3)
    (out / f"{label}.patch").write_text("".join(diff))
    print("wrote", label)
