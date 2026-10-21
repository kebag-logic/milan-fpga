#!/usr/bin/env python3
"""Write each round-2 mutation patch as one exact textual edit of the head RTL.

usage: make_patches_r2.py <processor tree>   (writes tb/srp_top/mutations/<label>.patch)
"""
import difflib
import sys
from pathlib import Path

tree = Path(sys.argv[1])
rel = "hdl/srp/KL_srp_listener_fsm.sv"
src = (tree / rel).read_text()

EDITS = {
    # re-anchored (its context line mbr_w changed), the same edit
    "listener-settle-compare-dropped": (
        "      cset_w[s] = (ctl_stream_id_i == sid_r[s]);\n",
        "      cset_w[s] = 1'b0;\n"),
    # round 2: a parked applicant joins the group of the value it holds
    "listener-parked-outside-groups": (
        "      mbr_w[s]  = rec_valid_r[s];\n",
        "      mbr_w[s]  = rec_valid_r[s] && !lvp_r[s];\n"),
    "listener-settle-skips-leave-copies": (
        "                if (ctl_sink_i == SNK_W_C'(b)) lq_r[a][b] <= lcset_w[a];\n",
        "                if (ctl_sink_i == SNK_W_C'(b)) lq_r[a][b] <= 1'b0;\n"),
    "listener-park-drops-matcher-pairs": (
        "                  lq_r[a][b] <= (a < b) ? eq_r[a][b] : eq_r[b][a];\n",
        "                  lq_r[a][b] <= 1'b0;\n"),
    "listener-merge-keeps-park": (
        "          // a parked giver owes nothing more: its slot is its matcher's\n"
        "          lvp_r[s]      <= 1'b0;\n",
        "          // a parked giver owes nothing more: its slot is its matcher's\n"),
    "listener-retire-skips-group-mark": (
        "              if (same_w[wsrc_r][t]) wdone_r[t] <= 1'b1;\n",
        "              if (t == 32'(wsrc_r)) wdone_r[t] <= 1'b1;\n"),
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
