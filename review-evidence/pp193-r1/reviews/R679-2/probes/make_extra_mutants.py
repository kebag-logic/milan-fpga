#!/usr/bin/env python3
"""Reviewer-planted extra controls on round-2 terms of KL_srp_listener_fsm.

usage: make_extra_mutants.py <tree root>
Writes <tree>/tb/srp_top/mutations/rv-*.patch (git-apply format) and appends
one MUTANTS entry per arm and suite to <tree>/tb/srp_top/mutants.py with the
expected tag ':' (any failing check), so the campaign prints which checks,
if any, each arm fails. These are probes, not proposed controls.
"""
import difflib
import sys
from pathlib import Path

tree = Path(sys.argv[1])
rtl_rel = "hdl/srp/KL_srp_listener_fsm.sv"
rtl = (tree / rtl_rel).read_text()

ARMS = {
    # a parked sink parked again overwrites its leave-copy pairs from the
    # matcher pairs of the stream it is leaving (drops the "keeps its own" term)
    "rv-repark-overwrites-pairs": (
        "if ((ctl_sink_i == SNK_W_C'(a)) && lv_take_w && !lvp_r[a]) begin",
        "if ((ctl_sink_i == SNK_W_C'(a)) && lv_take_w) begin"),
    # two parked applicants are grouped by the leave-copy pair map
    "rv-both-parked-grouped": (
        "end else if (!mbr_w[s] || !mbr_w[t] || (lvp_r[s] && lvp_r[t])) begin",
        "end else if (!mbr_w[s] || !mbr_w[t]) begin"),
    # the compare copy of the leave copies is never written
    "rv-leave-compare-copy-unwritten": (
        "if (rst_n && lv_take_w && (ctl_sink_i == SNK_W_C'(s))) begin\n          lcp_r[s] <= csid_w;",
        "if (1'b0) begin\n          lcp_r[s] <= csid_w;"),
    # a parked giver keeps its walk mark semantics but the taker's mark is
    # cleared (the handover forgets the walk mark)
    "rv-take-forgets-walk-mark": (
        "wdone_r[t]    <= (walk_r != W_IDLE) && wdone_r[take_src_w[t]];",
        "wdone_r[t]    <= 1'b0;"),
    # a parked member's group read uses the matcher pairs, not the leave copy
    "rv-parked-uses-matcher-pairs": (
        "        end else if (lvp_r[s]) begin\n          same_w[s][t] = lq_r[s][t];\n"
        "        end else if (lvp_r[t]) begin\n          same_w[s][t] = lq_r[t][s];\n",
        ""),
}

mut_py = tree / "tb/srp_top/mutants.py"
mp = mut_py.read_text()
entries = ""
for name, (old, new) in ARMS.items():
    assert rtl.count(old) == 1, name
    mutated = rtl.replace(old, new)
    diff = "".join(difflib.unified_diff(
        rtl.splitlines(keepends=True), mutated.splitlines(keepends=True),
        fromfile="a/" + rtl_rel, tofile="b/" + rtl_rel, n=3))
    (tree / "tb/srp_top/mutations" / (name + ".patch")).write_text(diff)
    entries += f"    ('{name}', 'srp_stream_fsms', 'suite', ':'),\n"
    entries += f"    ('{name}', 'srp_top', '', ':'),\n"
anchor = "    ('listener-park-drops-matcher-pairs', 'srp_stream_fsms', 'suite', 'SH16:'),\n]"
assert mp.count(anchor) == 1
mp = mp.replace(anchor, anchor[:-1] + entries + "]")
mut_py.write_text(mp)
print("planted", len(ARMS), "arms")
