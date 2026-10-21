#!/usr/bin/env python3
"""Write each round-3 mutation patch as one exact textual edit of the head RTL.

usage: make_patches_r3.py <processor tree>   (writes tb/srp_top/mutations/<label>.patch)
"""
import difflib
import sys
from pathlib import Path

tree = Path(sys.argv[1])
rel = "hdl/srp/KL_srp_listener_fsm.sv"
src = (tree / rel).read_text()

EDITS = {
    # re-anchored (its context lines changed), the same edit
    "listener-retire-skips-group-mark": (
        "              if (same_w[wsrc_r][t]) wdone_r[t] <= 1'b1;\n",
        "              if (t == 32'(wsrc_r)) wdone_r[t] <= 1'b1;\n"),
    # re-anchored (its trailing context line changed), the same edit
    "listener-park-never-retires": (
        "            lvp_r[wsrc_r]      <= 1'b0;\n",
        ""),
    # re-anchored (the two-sink compares now read g_wsid_flops' lsid_r,
    # which follows these lines), the same edits
    "listener-csid-flops-ignores-park": (
        "    assign csid_w = lvp_r[ctl_sink_i] ? lsid_r[ctl_sink_i]\n"
        "                                      : sid_r[ctl_sink_i];\n",
        "    assign csid_w = sid_r[ctl_sink_i];\n"),
    "lsid-flops-read-sink-0": (
        "    assign wsid_w = sid_r[wsrc_r];\n"
        "    assign lsid_w = lsid_r[wsrc_r];\n",
        "    assign wsid_w = sid_r[wsrc_r];\n"
        "    assign lsid_w = lsid_r[0];\n"),
    # round 3: the walk goes back to a slot holding an applicant not served
    "listener-walk-ends-owing-a-transmit": (
        "          walk_r      <= (&wdone_r) ? W_IDLE : W_EVAL;\n"
        "          txop_done_o <= &wdone_r;\n",
        "          walk_r      <= W_IDLE;\n"
        "          txop_done_o <= 1'b1;\n"),
    # the walk marks only the slots it serves, not every slot it passes
    "listener-walk-marks-only-served-slots": (
        "          if (walk_grant_w) wdone_r[wsrc_r] <= 1'b1;\n",
        "          if (walk_tx_w) wdone_r[wsrc_r] <= 1'b1;\n"),
    # the walk marks the group it serves only when a park retires (round 2)
    "listener-walk-marks-group-only-on-retire": (
        "          if (walk_tx_w && !(wnext_w inside {A_LA_C, A_LO_C})) begin\n",
        "          if (walk_tx_w && lvp_r[wsrc_r]\n"
        "              && !(wnext_w inside {A_LA_C, A_LO_C})) begin\n"),
    # a sink parked again takes the pairs of the stream it re-bound to first
    "listener-repark-takes-matcher-pairs": (
        "if ((ctl_sink_i == SNK_W_C'(a)) && lv_take_w && !lvp_r[a]) begin\n",
        "if ((ctl_sink_i == SNK_W_C'(a)) && lv_take_w) begin\n"),
    # two parked applicants are paired by the leave-copy map
    "listener-two-parks-grouped": (
        "        end else if (!mbr_w[s] || !mbr_w[t] || (lvp_r[s] && lvp_r[t])) begin\n",
        "        end else if (!mbr_w[s] || !mbr_w[t]) begin\n"),
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
