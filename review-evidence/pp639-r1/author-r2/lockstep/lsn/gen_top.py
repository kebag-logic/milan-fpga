#!/usr/bin/env python3
"""Write tb_lsn.sv: main's KL_pp_acmp_listener (renamed _ref) beside a candidate,
identical inputs, every output concatenated per instance for the C++ compare."""
OUTS = [  # name, width expression
    ("txn_ready_o", "1"), ("evt_tk_ready_o", "1"), ("pre_ready_o", "1"),
    ("strm_set_ready_o", "1"), ("strm_set_error_o", "1"), ("strm_started_o", "N_SINKS_P"),
    ("tmr_arm_valid_o", "1"), ("tmr_arm_cancel_o", "1"), ("tmr_arm_slot_o", "7"),
    ("tmr_arm_owner_o", "8"), ("tmr_arm_deadline_ms_o", "32"),
    ("draw_req_o", "1"), ("draw_kind_o", "3"),
    ("rxs_rd_slot_o", "2"), ("rxs_rd_addr_o", "10"), ("rxs_rd_en_o", "1"),
    ("rxs_free_o", "1"), ("rxs_free_slot_o", "2"),
    ("txs_alloc_req_o", "1"), ("txs_oversize_o", "1"), ("txs_wr_slot_o", "3"),
    ("txs_wr_addr_o", "11"), ("txs_wr_valid_o", "1"), ("txs_wr_data_o", "8"),
    ("txs_wr_commit_o", "1"), ("txs_wr_len_o", "11"),
    ("txreq_valid_o", "1"), ("txreq_slot_o", "3"),
    ("act_settle_o", "1"), ("act_settle_sid_o", "64"), ("act_settle_da_o", "48"),
    ("act_settle_vlan_o", "12"), ("act_teardown_o", "1"), ("act_disc_arm_o", "1"),
    ("act_disc_talker_eid_o", "64"), ("act_disc_disarm_o", "1"), ("act_nvm_o", "1"),
    ("act_nvm_set_o", "1"), ("act_notify_o", "1"), ("act_sink_o", "SINK_W_C"),
    ("dbg_busy_o", "1"), ("dbg_strq_drop_o", "16"), ("act_strt_chg_o", "1"),
    ("act_strt_cmd_chg_o", "1"), ("dbg_recwr_o", "1"), ("dbg_recwr_sink_o", "SINK_W_C"),
    ("dbg_recwr_rec_o", "384"),
]
INS = ["clk_i", "rst_n", "entity_id_i", "txn_valid_i", "txn_i", "evt_tk_valid_i",
       "evt_tk_kind_i", "evt_tk_failed_i", "evt_tk_sink_i", "pre_valid_i", "pre_sink_i",
       "pre_talker_eid_i", "pre_talker_uid_i", "pre_ctlr_eid_i", "pre_sw_i", "pre_started_i",
       "strm_set_valid_i", "strm_set_sink_i", "strm_set_val_i", "now_ms_i",
       "tmr_exp_valid_i", "tmr_exp_slot_i", "tmr_exp_owner_i", "draw_busy_i",
       "draw_valid_i", "draw_ms_i", "rxs_rd_data_i", "txs_alloc_gnt_i", "txs_alloc_slot_i",
       "lock_held_i", "lock_ctlr_i"]
L = []
L.append("`default_nettype none")
L.append("module tb_lsn import pp_pkg::*; import pp_acmp_pkg::*; #(")
L.append("  parameter int unsigned N_SINKS_P = 2,")
L.append("  localparam int unsigned SINK_W_C = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1")
L.append(") (")
L.append("""  input  wire clk_i, input wire rst_n,
  input  wire [63:0] entity_id_i,
  input  wire txn_valid_i,
  input  wire [PP_TXN_W_C-1:0] txn_raw_i,
  input  wire txn_acmp_i, input wire [3:0] txn_msg_i, input wire txn_eid_ours_i,
  input  wire [63:0] txn_ctlr_i, input wire [15:0] txn_uid_i, input wire [2:0] txn_slot_i,
  input  wire [4:0] txn_status_i, input wire [15:0] txn_seq_i,
  input  wire evt_tk_valid_i, input wire [1:0] evt_tk_kind_i, input wire evt_tk_failed_i,
  input  wire [15:0] evt_tk_sink_i,
  input  wire pre_valid_i, input wire [15:0] pre_sink_i, input wire [63:0] pre_talker_eid_i,
  input  wire [15:0] pre_talker_uid_i, input wire [63:0] pre_ctlr_eid_i, input wire pre_sw_i,
  input  wire pre_started_i,
  input  wire strm_set_valid_i, input wire [15:0] strm_set_sink_i, input wire strm_set_val_i,
  input  wire [31:0] now_ms_i,
  input  wire tmr_exp_valid_i, input wire [6:0] tmr_exp_slot_i, input wire [7:0] tmr_exp_owner_i,
  input  wire draw_busy_i, input wire draw_valid_i, input wire [15:0] draw_ms_i,
  input  wire [7:0] rxs_rd_data_i,
  input  wire txs_alloc_gnt_i, input wire [2:0] txs_alloc_slot_i,
  input  wire lock_held_i, input wire [63:0] lock_ctlr_i,""")
tot = " + ".join(f"({w})" for _, w in OUTS)
L.append(f"  output logic [{tot}-1:0] r_all_o,")
L.append(f"  output logic [{tot}-1:0] d_all_o,")
L.append("  output logic [4:0] r_xs_o, output logic [4:0] d_xs_o")
L.append(");")
L.append("  pp_txn_t txn_i;")
L.append("""  always_comb begin : txn_build
    txn_i = pp_txn_t'(txn_raw_i);
    if (txn_acmp_i) txn_i.protocol = PP_PROTO_ACMP;
    txn_i.msg_type = txn_msg_i;
    if (txn_eid_ours_i) txn_i.target_eid = entity_id_i;
    txn_i.controller_eid = txn_ctlr_i;
    txn_i.operands.unique_id = txn_uid_i;
    txn_i.rx_slot = txn_slot_i;
    txn_i.status_in = txn_status_i;
    txn_i.sequence_id = txn_seq_i;
  end""")
for p in ("r", "d"):
    for n, w in OUTS:
        L.append(f"  logic [{w}-1:0] {p}_{n};")
for p, mod in (("r", "KL_pp_acmp_listener_ref"), ("d", "KL_pp_acmp_listener")):
    L.append(f"  {mod} #(.N_SINKS_P(N_SINKS_P), .STRM_TIMEOUT_CYC_P(32)) u_{p} (")
    conns = [f"    .{i}({i})" for i in INS] + [f"    .{n}({p}_{n})" for n, _ in OUTS]
    L.append(",\n".join(conns))
    L.append("  );")
    L.append(f"  assign {p}_all_o = {{" + ", ".join(f"{p}_{n}" for n, _ in OUTS) + "};")
    L.append(f"  assign {p}_xs_o = 5'(u_{p}.xs_r);")
L.append("endmodule")
L.append("`default_nettype wire")
open("tb_lsn.sv", "w").write("\n".join(L) + "\n")
# field map for diagnostics, MSB first in the concatenation
off = []
import re
print("outputs:", len(OUTS))
open("fields.txt", "w").write("\n".join(f"{n} {w}" for n, w in OUTS) + "\n")
