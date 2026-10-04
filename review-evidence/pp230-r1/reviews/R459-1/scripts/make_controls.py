#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted controls for the base-vs-head SRP lockstep.

usage: make_controls.py HEAD_SRP_DIR OUT_DIR
Each control is a copy of the head's hdl/srp with exactly one edit (the
search string must occur exactly once). `expect` says whether the edit is
a defect the lockstep must catch ("catch") or is equivalent by
construction ("equiv": the checker must stay silent).
"""
import pathlib
import shutil
import sys

C = [
    # name, file, search, replace, expect
    ("tf-ls-head-reads-tk-ram", "KL_srp_top.sv",
     "tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1]];",
     "tf_q_r[1] <= tf_tk_ram_r[tf_rptr_r[1]];", "catch"),
    ("tf-tk-head-reads-next", "KL_srp_top.sv",
     "tf_q_r[0] <= tf_tk_ram_r[tf_rptr_r[0]];",
     "tf_q_r[0] <= tf_tk_ram_r[tf_rptr_r[0] + 5'd1];", "catch"),
    ("tf-ls-write-ignores-full", "KL_srp_top.sv",
     "    if (tf_push_w[1]) begin\n      tf_ls_ram_r",
     "    if (ls_arm_v_w) begin\n      tf_ls_ram_r", "catch-at-full"),
    ("tf-tk-write-at-rptr", "KL_srp_top.sv",
     "tf_tk_ram_r[tf_wptr_r[0]]", "tf_tk_ram_r[tf_rptr_r[0]]", "catch"),
    ("tf-tk-same-entry-bypass", "KL_srp_top.sv",
     "tf_q_r[0] <= tf_tk_ram_r[tf_rptr_r[0]];",
     "tf_q_r[0] <= (tf_push_w[0] && (tf_wptr_r[0] == tf_rptr_r[0]))\n"
     "                 ? {tk_arm_cancel_w, tk_arm_slot_w, tk_arm_owner_w, tk_arm_dl_w}\n"
     "                 : tf_tk_ram_r[tf_rptr_r[0]];", "equiv"),
    ("wtsp-written-on-close", "KL_srp_talker_fsm.sv",
     "assign gate_open_acc_w = rst_n && gate_acc_w && gate_open_i;",
     "assign gate_open_acc_w = rst_n && gate_acc_w;", "catch"),
    ("wtsp-prio-rank-swapped", "KL_srp_talker_fsm.sv",
     "wval_w[111:104] = {wtsp_w[35:32], 4'd0};",
     "wval_w[111:104] = {wtsp_w[34:32], wtsp_w[35], 4'd0};", "catch"),
    ("wtsp-read-at-source-0", "KL_srp_talker_fsm.sv",
     "assign wtsp_w = wtsp_r[wsrc_r];",
     "assign wtsp_w = wtsp_r[0];", "catch"),
    ("wid-ram-read-neighbour", "KL_srp_talker_fsm.sv",
     "assign wid_w = wid_r[wsrc_r];",
     "assign wid_w = wid_r[(wsrc_r == 0) ? 1 : wsrc_r - 1];", "catch"),
    ("wid-flops-vid-of-source-0", "KL_srp_talker_fsm.sv",
     "assign wid_w = {sid_r[wsrc_r], da_r[wsrc_r], vid_r[wsrc_r]};",
     "assign wid_w = {sid_r[wsrc_r], da_r[wsrc_r], vid_r[0]};", "catch"),
    ("wid-threshold-ram-from-1", "KL_srp_talker_fsm.sv",
     "if (N_SOURCES_P > 2) begin : g_wid_ram",
     "if (N_SOURCES_P > 0) begin : g_wid_ram", "equiv"),
    ("wid-threshold-flops-always", "KL_srp_talker_fsm.sv",
     "if (N_SOURCES_P > 2) begin : g_wid_ram",
     "if (N_SOURCES_P > 99) begin : g_wid_ram", "equiv"),
    ("wsid-ram-written-on-teardown", "KL_srp_listener_fsm.sv",
     "if (rst_n && ctl_acc_w && ctl_settle_i) begin",
     "if (rst_n && ctl_acc_w) begin", "catch"),
    ("wsid-flops-read-sink-0", "KL_srp_listener_fsm.sv",
     "assign wsid_w = sid_r[wsrc_r];",
     "assign wsid_w = sid_r[0];", "catch"),
    ("slope-store-at-stage-1-index", "KL_srp_admission.sv",
     "slope_q_r[cidx_q2_r] <=", "slope_q_r[cidx_q1_r] <=", "catch"),
    ("slope-read-source-0", "KL_srp_admission.sv",
     "assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[aidx_r]};",
     "assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[0]};", "catch"),
]


def main():
    head, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    lines = []
    for name, f, a, b, expect in C:
        d = out / name / "srp"
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(head, d)
        p = d / f
        s = p.read_text()
        n = s.count(a)
        assert n == 1, f"{name}: search occurs {n} times"
        p.write_text(s.replace(a, b))
        lines.append(f"{name}\t{expect}\t{f}")
    (out / "controls.tsv").write_text("\n".join(lines) + "\n")
    print(f"{len(C)} controls written")


if __name__ == "__main__":
    main()
