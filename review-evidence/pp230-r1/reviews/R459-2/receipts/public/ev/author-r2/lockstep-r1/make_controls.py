#!/usr/bin/env python3
"""Scratch (never committed): planted controls for the #230 lockstep bench.

Each control is a copy of the RTL under test with one exact edit; the bench
must report mismatches for every one at every shape where the edited code is
elaborated (the g_wid_ram / g_wsid_ram arms from three contexts, the
g_wid_flops / g_wsid_flops arms at one and two).
usage: make_controls.py <hdl/srp> <outdir>
"""
import shutil
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])

CONTROLS = [
    # lever 2: the two FIFO memories
    ("tf-heads-swapped", "KL_srp_top.sv",
     "    tf_q_r[0] <= tf_tk_ram_r[tf_rptr_r[0]];\n    tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1]];",
     "    tf_q_r[0] <= tf_ls_ram_r[tf_rptr_r[0]];\n    tf_q_r[1] <= tf_tk_ram_r[tf_rptr_r[1]];"),
    ("tf-head-at-write-pointer", "KL_srp_top.sv",
     "    tf_q_r[0] <= tf_tk_ram_r[tf_rptr_r[0]];",
     "    tf_q_r[0] <= tf_tk_ram_r[tf_wptr_r[0] - 5'd1];"),
    ("tf-listener-push-dropped", "KL_srp_top.sv",
     "    if (tf_push_w[1]) begin\n      tf_ls_ram_r[tf_wptr_r[1]]",
     "    if (tf_push_w[1] && !tf_push_w[0]) begin\n      tf_ls_ram_r[tf_wptr_r[1]]"),
    # lever 4: the talker's walk record
    ("walk-record-written-on-close", "KL_srp_talker_fsm.sv",
     "  assign gate_open_acc_w = rst_n && gate_acc_w && gate_open_i;",
     "  assign gate_open_acc_w = rst_n && gate_acc_w;"),
    ("wtsp-first-open-only", "KL_srp_talker_fsm.sv",
     "  always_ff @(posedge clk_i) begin : walk_tspec_write\n    if (gate_open_acc_w) begin",
     "  always_ff @(posedge clk_i) begin : walk_tspec_write\n    if (gate_open_acc_w && !rec_valid_r[gate_src_i]) begin"),
    ("wtsp-latency-field-shifted", "KL_srp_talker_fsm.sv",
     "    wval_w[103:72]  = wtsp_w[31:0];",
     "    wval_w[103:72]  = wtsp_w[32:1];"),
    ("wtsp-read-at-gate-source", "KL_srp_talker_fsm.sv",
     "  assign wtsp_w = wtsp_r[wsrc_r];",
     "  assign wtsp_w = wtsp_r[gate_src_i];"),
    ("wid-ram-first-open-only", "KL_srp_talker_fsm.sv",
     "    always_ff @(posedge clk_i) begin : walk_id_write\n      if (gate_open_acc_w) begin",
     "    always_ff @(posedge clk_i) begin : walk_id_write\n      if (gate_open_acc_w && !rec_valid_r[gate_src_i]) begin"),
    ("wid-ram-read-at-gate-source", "KL_srp_talker_fsm.sv",
     "    assign wid_w = wid_r[wsrc_r];",
     "    assign wid_w = wid_r[gate_src_i];"),
    ("wid-flops-da-of-gate-source", "KL_srp_talker_fsm.sv",
     "    assign wid_w = {sid_r[wsrc_r], da_r[wsrc_r], vid_r[wsrc_r]};",
     "    assign wid_w = {sid_r[wsrc_r], da_r[gate_src_i], vid_r[wsrc_r]};"),
    # lever 4: the listener's walk stream_id
    ("wsid-ram-written-on-teardown", "KL_srp_listener_fsm.sv",
     "      if (rst_n && ctl_acc_w && ctl_settle_i) begin\n        wsid_r[ctl_sink_i]",
     "      if (rst_n && ctl_acc_w) begin\n        wsid_r[ctl_sink_i]"),
    ("wsid-ram-first-settle-only", "KL_srp_listener_fsm.sv",
     "      if (rst_n && ctl_acc_w && ctl_settle_i) begin\n        wsid_r[ctl_sink_i]",
     "      if (rst_n && ctl_acc_w && ctl_settle_i && !rec_valid_r[ctl_sink_i]) begin\n        wsid_r[ctl_sink_i]"),
    ("wsid-flops-of-control-sink", "KL_srp_listener_fsm.sv",
     "    assign wsid_w = sid_r[wsrc_r];",
     "    assign wsid_w = sid_r[ctl_sink_i];"),
    # lever 4: the admission slopes
    ("slope-stored-at-stage-2-index", "KL_srp_admission.sv",
     "      slope_q_r[cidx_q2_r] <= (iv_bytes_r > IV_MAX_C)",
     "      slope_q_r[cidx_q1_r] <= (iv_bytes_r > IV_MAX_C)"),
    ("slope-store-source-0-only", "KL_srp_admission.sv",
     "    if (rst_n) begin\n      slope_q_r[cidx_q2_r]",
     "    if (rst_n && (cidx_q2_r == '0)) begin\n      slope_q_r[cidx_q2_r]"),
    # the reset argument: a stored value read without its valid bit is caught
    ("talker-vid-unreset", "KL_srp_talker_fsm.sv",
     "      vid_r       <= '0;\n      app_r       <= '0;",
     "      app_r       <= '0;"),
]

for name, fname, old, new in CONTROLS:
    d = OUT / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(SRC, d)
    p = d / fname
    s = p.read_text()
    assert s.count(old) == 1, (name, s.count(old))
    p.write_text(s.replace(old, new))
    print(name)
