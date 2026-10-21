#!/usr/bin/env python3
"""Reviewer-planted probes on the round-3 walk terms of KL_srp_listener_fsm.

usage: make_r3_mutants.py <tree root> <arm>
Edits <tree>/hdl/srp/KL_srp_listener_fsm.sv in place for one arm, refusing
drift (each old text must occur exactly once). These are probes, not
proposed controls: the suite run on the edited tree shows which checks, if
any, see the edit.
"""
import sys
from pathlib import Path

ARMS = {
    # the group mark also on a transmit that leaves the applicant LA/LO
    # (drops the exception); expected to be equivalent on the suite
    "rv3-group-mark-on-lo": (
        "if (walk_tx_w && !(wnext_w inside {A_LA_C, A_LO_C})) begin\n"
        "            for (int unsigned t = 0; t < N_SINKS_P; t++) begin\n"
        "              if (same_w[wsrc_r][t]) wdone_r[t] <= 1'b1;",
        "if (walk_tx_w) begin\n"
        "            for (int unsigned t = 0; t < N_SINKS_P; t++) begin\n"
        "              if (same_w[wsrc_r][t]) wdone_r[t] <= 1'b1;"),
    # the done strobe fires at the end of the first pass although the walk
    # goes round again (the re-walk's push lands after the strobe)
    "rv3-done-before-rewalk": (
        "txop_done_o <= &wdone_r;",
        "txop_done_o <= 1'b1;"),
    # the second pass starts where the first ended, not at slot 0
    "rv3-rewalk-keeps-wsrc": (
        "          wsrc_r      <= '0;\n          walk_r      <= (&wdone_r) ? W_IDLE : W_EVAL;",
        "          walk_r      <= (&wdone_r) ? W_IDLE : W_EVAL;"),
    # a handover keeps the taker's own mark instead of carrying the giver's
    "rv3-take-keeps-taker-mark": (
        "wdone_r[t]    <= (walk_r != W_IDLE) && wdone_r[take_src_w[t]];",
        "wdone_r[t]    <= (walk_r != W_IDLE) && wdone_r[t];"),
}

tree = Path(sys.argv[1])
arm = sys.argv[2]
rtl = tree / "hdl/srp/KL_srp_listener_fsm.sv"
text = rtl.read_text()
old, new = ARMS[arm]
assert text.count(old) == 1, arm
rtl.write_text(text.replace(old, new))
print("planted", arm)
