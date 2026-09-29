#!/usr/bin/env python3
"""Scratch: regenerate the item-1 patch arms against the lane's KL_srp_top.sv."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(sys.argv[1])
TOP = "hdl/srp/KL_srp_top.sv"
PEER_MSRP = ("      if (|dec_la_msrp_w) begin\n"
             "        need_draw_r[0] <= 1'b1;\n"
             "        la_msrp_pend_r <= 1'b0;\n")
PEER_MVRP = ("      if (dec_la_mvrp_w) begin\n"
             "        need_draw_r[1] <= 1'b1;\n"
             "        la_mvrp_pend_r <= 1'b0;\n")

SPECS = {
    # regenerated round-1 arms (same edit, new context)
    "expiry-outranks-peer": [(
        PEER_MSRP,
        "      if ((|dec_la_msrp_w) && !(cad_hit_w && (cad_exp_ix_w == CAD_LA_MSRP_C))) begin\n"
        "        need_draw_r[0] <= 1'b1;\n"
        "        la_msrp_pend_r <= 1'b0;\n")],
    "mvrp-supersedes-msrp": [(
        PEER_MSRP,
        "      if ((|dec_la_msrp_w) || dec_la_mvrp_w) begin\n"
        "        need_draw_r[0] <= 1'b1;\n"
        "        la_msrp_pend_r <= 1'b0;\n")],
    "pending-peer-ignored": [(
        PEER_MSRP,
        "      if (1'b0) begin\n"
        "        need_draw_r[0] <= 1'b1;\n"
        "        la_msrp_pend_r <= 1'b0;\n")],
    "reset-retains-intent": [(
        "      la_wait_r         <= 1'b0;\n      la_cancel_r       <= 1'b0;\n",
        "      // pending preparation incorrectly retained at reset\n"
        "      la_cancel_r       <= 1'b0;\n")],
    "my-expiry-pulse": [
        ("  logic       la_msrp_pend_r;  // timer intent, not a registrar event\n",
         "  logic       la_msrp_pend_r;  // timer intent, not a registrar event\n"
         "  logic       my_exp_r;\n"),
        ("      .leaveall_rx_i       (dec_la_msrp_w),\n"
         "      .leaveall_own_i      (p_la_msrp_w),\n",
         "      .leaveall_rx_i       (dec_la_msrp_w),\n"
         "      .leaveall_own_i      (p_la_msrp_w || my_exp_r),\n"),
        ("      .leaveall_rx_i           (dec_la_msrp_w),\n"
         "      .leaveall_own_i          (p_la_msrp_w),\n",
         "      .leaveall_rx_i           (dec_la_msrp_w),\n"
         "      .leaveall_own_i          (p_la_msrp_w || my_exp_r),\n"),
        ("      la_mvrp_pend_r    <= 1'b0;\n      join_msrp_pend_r  <= 1'b0;\n",
         "      la_mvrp_pend_r    <= 1'b0;\n      my_exp_r <= 1'b0;\n"
         "      join_msrp_pend_r  <= 1'b0;\n"),
        ("      p_la_mvrp_r  <= 1'b0;\n      enc_join_r   <= 2'b00;\n",
         "      p_la_mvrp_r  <= 1'b0;\n      my_exp_r <= 1'b0;\n"
         "      enc_join_r   <= 2'b00;\n"),
        ("              la_msrp_pend_r <= 1'b1;  // wait for a supported sLA opportunity\n",
         "              la_msrp_pend_r <= 1'b1;  // wait for a supported sLA opportunity\n"
         "              my_exp_r <= 1'b1;\n"),
    ],
    # item 1 (issue #108): each removes one half of Table 10-5 rLA!
    "expiry-only-redraw": [(
        PEER_MSRP,
        "      if (|dec_la_msrp_w) begin\n"
        "        la_msrp_pend_r <= 1'b0;\n")],
    "mvrp-expiry-only-redraw": [(
        PEER_MVRP,
        "      if (dec_la_mvrp_w) begin\n"
        "        la_mvrp_pend_r <= 1'b0;\n")],
    "stale-expiry-honoured": [(
        "            if (!la_rearm_w[0]) begin\n",
        "            if (1'b1) begin\n")],
    "mvrp-stale-expiry-honoured": [(
        "            if (!la_rearm_w[1]) begin\n",
        "            if (1'b1) begin\n")],
    "mvrp-passive-lost": [(
        PEER_MVRP,
        "      if (dec_la_mvrp_w) begin\n"
        "        need_draw_r[1] <= 1'b1;\n")],
    "mvrp-flag-at-expiry": [(
        "              la_mvrp_pend_r <= 1'b1;  // the flag waits for the next drain\n",
        "              enc_la_r[1]    <= 1'b1;\n")],
}


def write(label, reps):
    text = (REPO / TOP).read_text()
    new = text
    for old, rep in reps:
        n = new.count(old)
        if n != 1:
            raise SystemExit(f"{label}: old text occurs {n} times: {old!r}")
        new = new.replace(old, rep)
    with tempfile.TemporaryDirectory() as tmp:
        a, b = Path(tmp) / "a", Path(tmp) / "b"
        a.write_text(text)
        b.write_text(new)
        res = subprocess.run(["diff", "-u", "--label", f"a/{TOP}", "--label", f"b/{TOP}",
                              str(a), str(b)], capture_output=True, text=True)
    if res.returncode != 1:
        raise SystemExit(f"{label}: diff rc {res.returncode}")
    (REPO / "tb/srp_top/mutations" / f"{label}.patch").write_text(res.stdout)
    print("wrote", label)


for lbl in (sys.argv[2:] or SPECS):
    write(lbl, SPECS[lbl])
