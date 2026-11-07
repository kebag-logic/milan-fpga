// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//---------------------------------------------------------------------------//
//  File        : tb_split_top.sv
//  Description : The split placement's control path as the SoC composes it
//                (#665 F-INT PR 2), for sim_split.cpp: KL_mbx on the mailbox
//                clock, KL_mbx_cdc, the two byte crossings, and milan_datapath
//                with CTRL_SPLIT_P = 1 on the datapath clock. The host port
//                is KL_mbx's own, so a check reaches the datapath only
//                through the contract's registers, the crossing and the ctl
//                ports. The frame crossings are verilog-axis async FIFOs in
//                place of the SoC's LiteX ones, sixteen bytes deep as the
//                SoC's are. The receive filter is pruned (RXFILT_P = 0): the
//                straight wire it is when promiscuous. The gPTP plane is off, as
//                in the broad legs: no face here reads it.
//
//                The probes are the datapath nets each face must reach, read
//                by hierarchical reference, so the bench sees what the
//                datapath's consumers read rather than what the ports carry.
//---------------------------------------------------------------------------//
`default_nettype none

module tb_split_top
  import KL_mbx_pkg::*;
#(
  parameter int SPLIT_P = 1     //! the datapath's CTRL_SPLIT_P
) (
  input  wire                     sys_clk,
  input  wire                     sys_rst_n,
  input  wire                     dp_clk,
  input  wire                     dp_rst_n,
  //! ---- KL_mbx's host port, and its millisecond
  input  wire                     host_req_i,
  input  wire                     host_we_i,
  input  wire  [MBX_ADDR_W_C-1:0] host_addr_i,
  input  wire  [31:0]             host_wdata_i,
  input  wire  [3:0]              host_be_i,
  output logic                    host_ack_o,
  output logic [31:0]             host_rdata_o,
  input  wire                     ms_tick_p_i,
  //! ---- the datapath's MAC boundary
  input  wire  [63:0]             rx_tdata,
  input  wire  [7:0]              rx_tkeep,
  input  wire                     rx_tvalid,
  input  wire                     rx_tlast,
  output wire                     rx_tready,
  output wire  [63:0]             tx_tdata,
  output wire  [7:0]              tx_tkeep,
  output wire                     tx_tvalid,
  output wire                     tx_tlast,
  input  wire                     tx_tready,
  input  wire                     link_up,
  //! ---- probes: what the datapath's consumers read
  output wire  [15:0]             p_declaring,
  output wire  [15:0]             p_active,
  output wire  [15:0]             p_admitted,
  output wire  [15:0]             p_bound,
  output wire  [15:0]             p_started,
  output wire  [63:0]             p_bound_sid0,
  output wire  [63:0]             p_src_sid0,
  output wire  [11:0]             p_vid,
  output wire  [2:0]              p_prio,
  output wire                     p_adopted,
  output wire  [31:0]             p_slope,
  output wire  [1:0]              p_tk_decl0,
  output wire  [15:0]             p_clk_src,
  output wire  [15:0]             p_cur_config,
  output wire  [7:0]              p_identify,
  output wire                     p_lock_held,
  output wire  [63:0]             p_fmt_out0,
  output wire                     p_fmt_out_v0,
  output wire  [31:0]             p_pt_offset0,
  output wire                     p_restore_done,
  output wire                     p_nvm_backed,
  output wire  [15:0]             p_rx_frames,
  output wire  [15:0]             p_tx_frames
);

  localparam int unsigned S = MBX_N_PUB_SOURCES_C;
  localparam int unsigned K = MBX_N_PUB_SINKS_C;

  // ---- the mailbox side ------------------------------------------------------
  logic [S-1:0] pub_da_gate, pub_licence, pub_talker_decl;
  logic [S*64-1:0] pub_src_sid;
  logic [31:0] pub_idle_slope;
  logic [11:0] pub_dom_vid;
  logic [2:0]  pub_dom_prio;
  logic        pub_dom_adopted;
  logic [K-1:0] pub_bound, pub_sid_valid, pub_started;
  logic [K*64-1:0] pub_sid;
  logic fw_send, fw_ack_p, fw_ctrl_ready;
  logic [15:0] fw_cur_config, fw_clk_src;
  logic [7:0]  fw_identify;
  logic fw_lock_held, fw_dyn_dirty;
  logic fw_r_busy, fw_r_done, fw_r_fail, fw_r_blank, fw_r_closed, fw_r_rb;
  logic [2:0] fw_rs_cause;
  logic [1:0] fw_restore_cause;
  logic fw_n_backed, fw_n_alarm, fw_n_dirty, fw_n_stale, fw_n_pend, fw_n_img_valid;
  logic [3:0] fw_nvm_verdict;
  logic [S*32-1:0] fw_pt_offset;
  logic [S-1:0] fw_pt_offset_v, fw_fmt_out_v;
  logic [S*64-1:0] fw_fmt_out;
  logic [K*64-1:0] fw_fmt_in;
  logic [K-1:0] fw_fmt_in_v;
  logic ctr_req, amap_req, edit_req, gsi_req;
  logic [MBX_CTR_STATUS_TAG_WIDTH_C-1:0]  ctr_tag;
  logic [MBX_AMAP_STATUS_TAG_WIDTH_C-1:0] amap_tag;
  logic [MBX_EDIT_STATUS_TAG_WIDTH_C-1:0] edit_tag;
  logic [MBX_GSI_STATUS_TAG_WIDTH_C-1:0]  gsi_tag;
  logic [15:0] ctr_type, ctr_index, amap_type, amap_index, amap_map_index, edit_type, edit_index, edit_count;
  logic [15:0] gsi_type, gsi_index;
  logic [5:0]  ctr_word;
  logic [1:0]  amap_sel, gsi_kind;
  logic [7:0]  amap_rec, edit_rec, gsi_ord;
  logic [2:0]  edit_phase;
  logic        edit_remove;
  logic [3:0]  gsi_sel;
  logic [63:0] edit_record, edit_value, gsi_prop;
  logic ctr_ans_p, amap_ans_p, edit_ans_p, gsi_ans_p;
  logic [MBX_CTR_STATUS_TAG_WIDTH_C-1:0]  ctr_ans_tag;
  logic [MBX_AMAP_STATUS_TAG_WIDTH_C-1:0] amap_ans_tag;
  logic [MBX_EDIT_STATUS_TAG_WIDTH_C-1:0] edit_ans_tag;
  logic [MBX_GSI_STATUS_TAG_WIDTH_C-1:0]  gsi_ans_tag;
  logic [31:0] ctr_ans_data;
  logic [63:0] amap_ans_data, edit_ans_data, gsi_ans_data;
  logic ctr_chg_p, avb_chg_p, asp_chg_p, amap_wr_p;
  logic [15:0] ctr_chg_type, ctr_chg_index;
  logic m_link_up, m_gm_change_p;
  logic [63:0] m_gm_id;
  logic [7:0]  m_gptp_domain;
  logic        m_rx_valid, m_rx_ready, m_rx_last, m_tx_valid, m_tx_ready, m_tx_last;
  logic [7:0]  m_rx_data, m_tx_data;
  logic        m_tx_if;
  logic [MBX_CH_W_C-1:0] m_tx_ch;

  KL_mbx u_mbx (
    .clk_i(sys_clk), .rst_n(sys_rst_n),
    .host_req_i, .host_we_i, .host_addr_i, .host_wdata_i, .host_be_i, .host_ack_o, .host_rdata_o,
    .irq_o(), .ms_tick_p_i,
    .link_up_i(m_link_up), .gm_change_p_i(m_gm_change_p), .gm_id_i(m_gm_id), .gptp_domain_i(m_gptp_domain),
    .rx_valid_i(m_rx_valid), .rx_ready_o(m_rx_ready), .rx_data_i(m_rx_data), .rx_last_i(m_rx_last), .rx_if_i('0),
    .tx_valid_o(m_tx_valid), .tx_ready_i(m_tx_ready), .tx_data_o(m_tx_data), .tx_last_o(m_tx_last),
    .tx_if_o(m_tx_if), .tx_ch_o(m_tx_ch),
    .pub_da_gate_o(pub_da_gate), .pub_licence_o(pub_licence), .pub_idle_slope_bps_o(pub_idle_slope),
    .pub_dom_vid_o(pub_dom_vid), .pub_dom_prio_o(pub_dom_prio), .pub_dom_adopted_o(pub_dom_adopted),
    .pub_talker_decl_o(pub_talker_decl), .pub_src_sid_o(pub_src_sid), .pub_bound_o(pub_bound),
    .pub_sid_valid_o(pub_sid_valid), .pub_started_o(pub_started), .pub_sid_o(pub_sid),
    .fw_send_o(fw_send), .fw_ack_p_i(fw_ack_p), .fw_ctrl_ready_o(fw_ctrl_ready),
    .fw_entity_cur_config_o(fw_cur_config), .fw_entity_identify_o(fw_identify),
    .fw_clock_source_index_o(fw_clk_src), .fw_aecp_lock_held_o(fw_lock_held), .fw_aecp_dyn_dirty_o(fw_dyn_dirty),
    .fw_restore_busy_o(fw_r_busy), .fw_restore_done_o(fw_r_done), .fw_restore_fail_o(fw_r_fail),
    .fw_restore_blank_o(fw_r_blank), .fw_restore_closed_o(fw_r_closed), .fw_restore_rb_o(fw_r_rb),
    .fw_restore_rs_cause_o(fw_rs_cause), .fw_restore_cause_o(fw_restore_cause),
    .fw_nvm_backed_o(fw_n_backed), .fw_nvm_alarm_o(fw_n_alarm), .fw_nvm_dirty_o(fw_n_dirty),
    .fw_nvm_stale_o(fw_n_stale), .fw_nvm_pend_o(fw_n_pend), .fw_nvm_img_valid_o(fw_n_img_valid),
    .fw_nvm_verdict_o(fw_nvm_verdict),
    .fw_pt_offset_ns_o(fw_pt_offset), .fw_pt_offset_v_o(fw_pt_offset_v), .fw_fmt_out_o(fw_fmt_out),
    .fw_fmt_out_v_o(fw_fmt_out_v), .fw_fmt_in_o(fw_fmt_in), .fw_fmt_in_v_o(fw_fmt_in_v),
    .ctr_req_o(ctr_req), .ctr_tag_o(ctr_tag), .ctr_type_o(ctr_type), .ctr_index_o(ctr_index), .ctr_word_o(ctr_word),
    .ctr_ans_p_i(ctr_ans_p), .ctr_ans_tag_i(ctr_ans_tag), .ctr_ans_data_i(ctr_ans_data),
    .amap_req_o(amap_req), .amap_tag_o(amap_tag), .amap_type_o(amap_type), .amap_index_o(amap_index),
    .amap_map_index_o(amap_map_index), .amap_sel_o(amap_sel), .amap_rec_o(amap_rec),
    .amap_ans_p_i(amap_ans_p), .amap_ans_tag_i(amap_ans_tag), .amap_ans_data_i(amap_ans_data),
    .edit_req_o(edit_req), .edit_tag_o(edit_tag), .edit_type_o(edit_type), .edit_index_o(edit_index),
    .edit_phase_o(edit_phase), .edit_remove_o(edit_remove), .edit_rec_o(edit_rec), .edit_count_o(edit_count),
    .edit_record_o(edit_record), .edit_value_o(edit_value),
    .edit_ans_p_i(edit_ans_p), .edit_ans_tag_i(edit_ans_tag), .edit_ans_data_i(edit_ans_data),
    .gsi_req_o(gsi_req), .gsi_tag_o(gsi_tag), .gsi_type_o(gsi_type), .gsi_index_o(gsi_index),
    .gsi_kind_o(gsi_kind), .gsi_sel_o(gsi_sel), .gsi_ord_o(gsi_ord), .gsi_prop_o(gsi_prop),
    .gsi_ans_p_i(gsi_ans_p), .gsi_ans_tag_i(gsi_ans_tag), .gsi_ans_data_i(gsi_ans_data),
    .ctr_chg_p_i(ctr_chg_p), .ctr_chg_type_i(ctr_chg_type), .ctr_chg_index_i(ctr_chg_index),
    .avb_chg_p_i(avb_chg_p), .asp_chg_p_i(asp_chg_p), .amap_wr_p_i(amap_wr_p));

  // ---- the datapath side's ctl nets ----------------------------------------------
  logic [S-1:0] d_da_gate, d_licence, d_talker_decl, d_pt_offset_v, d_fmt_out_v;
  logic [S*64-1:0] d_src_sid, d_fmt_out;
  logic [31:0] d_idle_slope;
  logic [11:0] d_dom_vid;
  logic [2:0] d_dom_prio, d_rs_cause;
  logic d_dom_adopted, d_lock_held, d_dyn_dirty;
  logic [K-1:0] d_bound, d_sid_valid, d_started, d_fmt_in_v;
  logic [K*64-1:0] d_sid, d_fmt_in;
  logic [15:0] d_cur_config, d_clk_src;
  logic [7:0] d_identify;
  logic [S*32-1:0] d_pt_offset;
  logic [5:0] d_restore, d_nvm;
  logic [1:0] d_restore_cause;
  logic [3:0] d_nvm_verdict;
  logic d_ctr_req, d_amap_req, d_edit_req, d_gsi_req, d_ctr_wait, d_amap_wait, d_edit_wait, d_gsi_wait;
  logic [15:0] d_ctr_type, d_ctr_index, d_amap_type, d_amap_index, d_amap_map_index, d_edit_type, d_edit_index;
  logic [15:0] d_edit_count, d_gsi_type, d_gsi_index;
  logic [5:0] d_ctr_word;
  logic [1:0] d_amap_sel, d_gsi_kind;
  logic [7:0] d_amap_rec, d_edit_rec, d_gsi_ord;
  logic [2:0] d_edit_phase;
  logic d_edit_remove;
  logic [3:0] d_gsi_sel;
  logic [63:0] d_edit_record, d_edit_value, d_gsi_prop, d_amap_data, d_edit_data, d_gsi_data;
  logic [31:0] d_ctr_data;
  logic d_ctr_chg_valid, d_avb_chg_p, d_asp_chg_p, d_amap_wr_p, d_link_up, d_gm_change_p;
  logic [15:0] d_ctr_chg_type, d_ctr_chg_index;
  logic [63:0] d_gm_id;
  logic [7:0] d_gptp_domain;
  logic d_rx_valid, d_rx_ready, d_rx_last, d_tx_valid, d_tx_ready, d_tx_last;
  logic [7:0] d_rx_data, d_tx_data;

  KL_mbx_cdc u_cdc (
    .sys_clk_i(sys_clk), .sys_rst_n, .dp_clk_i(dp_clk), .dp_rst_n,
    .m_pub_da_gate_i(pub_da_gate), .m_pub_licence_i(pub_licence), .m_pub_talker_decl_i(pub_talker_decl),
    .m_pub_src_sid_i(pub_src_sid), .m_pub_idle_slope_i(pub_idle_slope), .m_pub_dom_vid_i(pub_dom_vid),
    .m_pub_dom_prio_i(pub_dom_prio), .m_pub_dom_adopted_i(pub_dom_adopted), .m_pub_bound_i(pub_bound),
    .m_pub_sid_valid_i(pub_sid_valid), .m_pub_started_i(pub_started), .m_pub_sid_i(pub_sid),
    .m_fw_send_i(fw_send), .m_fw_ack_p_o(fw_ack_p), .m_fw_cur_config_i(fw_cur_config),
    .m_fw_identify_i(fw_identify), .m_fw_clk_src_index_i(fw_clk_src), .m_fw_lock_held_i(fw_lock_held),
    .m_fw_dyn_dirty_i(fw_dyn_dirty), .m_fw_pt_offset_i(fw_pt_offset), .m_fw_pt_offset_v_i(fw_pt_offset_v),
    .m_fw_fmt_out_i(fw_fmt_out), .m_fw_fmt_out_v_i(fw_fmt_out_v), .m_fw_fmt_in_i(fw_fmt_in),
    .m_fw_fmt_in_v_i(fw_fmt_in_v),
    .m_fw_restore_i({fw_r_rb, fw_r_closed, fw_r_blank, fw_r_fail, fw_r_done, fw_r_busy}),
    .m_fw_rs_cause_i(fw_rs_cause), .m_fw_restore_cause_i(fw_restore_cause),
    .m_fw_nvm_i({fw_n_img_valid, fw_n_pend, fw_n_stale, fw_n_dirty, fw_n_alarm, fw_n_backed}),
    .m_fw_nvm_verdict_i(fw_nvm_verdict),
    .m_ctr_req_i(ctr_req), .m_ctr_tag_i(ctr_tag), .m_ctr_type_i(ctr_type), .m_ctr_index_i(ctr_index),
    .m_ctr_word_i(ctr_word), .m_ctr_ans_p_o(ctr_ans_p), .m_ctr_ans_tag_o(ctr_ans_tag), .m_ctr_ans_data_o(ctr_ans_data),
    .m_amap_req_i(amap_req), .m_amap_tag_i(amap_tag), .m_amap_type_i(amap_type), .m_amap_index_i(amap_index),
    .m_amap_map_index_i(amap_map_index), .m_amap_sel_i(amap_sel), .m_amap_rec_i(amap_rec),
    .m_amap_ans_p_o(amap_ans_p), .m_amap_ans_tag_o(amap_ans_tag), .m_amap_ans_data_o(amap_ans_data),
    .m_edit_req_i(edit_req), .m_edit_tag_i(edit_tag), .m_edit_type_i(edit_type), .m_edit_index_i(edit_index),
    .m_edit_phase_i(edit_phase), .m_edit_remove_i(edit_remove), .m_edit_rec_i(edit_rec),
    .m_edit_count_i(edit_count), .m_edit_record_i(edit_record), .m_edit_value_i(edit_value),
    .m_edit_ans_p_o(edit_ans_p), .m_edit_ans_tag_o(edit_ans_tag), .m_edit_ans_data_o(edit_ans_data),
    .m_gsi_req_i(gsi_req), .m_gsi_tag_i(gsi_tag), .m_gsi_type_i(gsi_type), .m_gsi_index_i(gsi_index),
    .m_gsi_kind_i(gsi_kind), .m_gsi_sel_i(gsi_sel), .m_gsi_ord_i(gsi_ord), .m_gsi_prop_i(gsi_prop),
    .m_gsi_ans_p_o(gsi_ans_p), .m_gsi_ans_tag_o(gsi_ans_tag), .m_gsi_ans_data_o(gsi_ans_data),
    .m_ctr_chg_p_o(ctr_chg_p), .m_ctr_chg_type_o(ctr_chg_type), .m_ctr_chg_index_o(ctr_chg_index),
    .m_avb_chg_p_o(avb_chg_p), .m_asp_chg_p_o(asp_chg_p), .m_amap_wr_p_o(amap_wr_p),
    .m_link_up_o(m_link_up), .m_gm_change_p_o(m_gm_change_p), .m_gm_id_o(m_gm_id),
    .m_gptp_domain_o(m_gptp_domain),
    .d_pub_da_gate_o(d_da_gate), .d_pub_licence_o(d_licence), .d_pub_talker_decl_o(d_talker_decl),
    .d_pub_src_sid_o(d_src_sid), .d_pub_idle_slope_o(d_idle_slope), .d_pub_dom_vid_o(d_dom_vid),
    .d_pub_dom_prio_o(d_dom_prio), .d_pub_dom_adopted_o(d_dom_adopted), .d_pub_bound_o(d_bound),
    .d_pub_sid_valid_o(d_sid_valid), .d_pub_started_o(d_started), .d_pub_sid_o(d_sid),
    .d_cur_config_o(d_cur_config), .d_identify_o(d_identify), .d_clk_src_index_o(d_clk_src),
    .d_lock_held_o(d_lock_held), .d_dyn_dirty_o(d_dyn_dirty), .d_pt_offset_o(d_pt_offset),
    .d_pt_offset_v_o(d_pt_offset_v), .d_fmt_out_o(d_fmt_out), .d_fmt_out_v_o(d_fmt_out_v),
    .d_fmt_in_o(d_fmt_in), .d_fmt_in_v_o(d_fmt_in_v), .d_restore_o(d_restore), .d_rs_cause_o(d_rs_cause),
    .d_restore_cause_o(d_restore_cause), .d_nvm_o(d_nvm), .d_nvm_verdict_o(d_nvm_verdict),
    .d_ctr_req_o(d_ctr_req), .d_ctr_type_o(d_ctr_type), .d_ctr_index_o(d_ctr_index), .d_ctr_word_o(d_ctr_word),
    .d_ctr_data_i(d_ctr_data), .d_ctr_wait_i(d_ctr_wait),
    .d_amap_req_o(d_amap_req), .d_amap_type_o(d_amap_type), .d_amap_index_o(d_amap_index),
    .d_amap_map_index_o(d_amap_map_index), .d_amap_sel_o(d_amap_sel), .d_amap_rec_o(d_amap_rec),
    .d_amap_data_i(d_amap_data), .d_amap_wait_i(d_amap_wait),
    .d_edit_req_o(d_edit_req), .d_edit_phase_o(d_edit_phase), .d_edit_remove_o(d_edit_remove),
    .d_edit_type_o(d_edit_type), .d_edit_index_o(d_edit_index), .d_edit_count_o(d_edit_count),
    .d_edit_rec_o(d_edit_rec), .d_edit_record_o(d_edit_record), .d_edit_value_o(d_edit_value),
    .d_edit_data_i(d_edit_data), .d_edit_wait_i(d_edit_wait),
    .d_gsi_req_o(d_gsi_req), .d_gsi_kind_o(d_gsi_kind), .d_gsi_type_o(d_gsi_type), .d_gsi_index_o(d_gsi_index),
    .d_gsi_sel_o(d_gsi_sel), .d_gsi_ord_o(d_gsi_ord), .d_gsi_prop_o(d_gsi_prop),
    .d_gsi_data_i(d_gsi_data), .d_gsi_wait_i(d_gsi_wait),
    .d_ctr_chg_valid_i(d_ctr_chg_valid), .d_ctr_chg_type_i(d_ctr_chg_type), .d_ctr_chg_index_i(d_ctr_chg_index),
    .d_avb_chg_p_i(d_avb_chg_p), .d_asp_chg_p_i(d_asp_chg_p), .d_amap_wr_p_i(d_amap_wr_p),
    .d_link_up_i(d_link_up), .d_gm_change_p_i(d_gm_change_p), .d_gm_id_i(d_gm_id), .d_gptp_domain_i(d_gptp_domain));

  // ---- the frame crossings, sixteen bytes deep each way ----------------------------
  axis_async_fifo #(.DEPTH(16), .DATA_WIDTH(8), .KEEP_ENABLE(0), .LAST_ENABLE(1), .USER_ENABLE(0)) u_rx_x (
    .s_clk(dp_clk), .s_rst(~dp_rst_n), .s_axis_tdata(d_rx_data), .s_axis_tkeep(1'b1), .s_axis_tvalid(d_rx_valid),
    .s_axis_tready(d_rx_ready), .s_axis_tlast(d_rx_last), .s_axis_tid('0), .s_axis_tdest('0), .s_axis_tuser('0),
    .m_clk(sys_clk), .m_rst(~sys_rst_n), .m_axis_tdata(m_rx_data), .m_axis_tkeep(), .m_axis_tvalid(m_rx_valid),
    .m_axis_tready(m_rx_ready), .m_axis_tlast(m_rx_last), .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),
    .s_pause_req(1'b0), .s_pause_ack(), .m_pause_req(1'b0), .m_pause_ack(),
    .s_status_depth(), .s_status_depth_commit(), .s_status_overflow(), .s_status_bad_frame(),
    .s_status_good_frame(), .m_status_depth(), .m_status_depth_commit(), .m_status_overflow(),
    .m_status_bad_frame(), .m_status_good_frame());
  axis_async_fifo #(.DEPTH(16), .DATA_WIDTH(8), .KEEP_ENABLE(0), .LAST_ENABLE(1), .USER_ENABLE(0)) u_tx_x (
    .s_clk(sys_clk), .s_rst(~sys_rst_n), .s_axis_tdata(m_tx_data), .s_axis_tkeep(1'b1), .s_axis_tvalid(m_tx_valid),
    .s_axis_tready(m_tx_ready), .s_axis_tlast(m_tx_last), .s_axis_tid('0), .s_axis_tdest('0), .s_axis_tuser('0),
    .m_clk(dp_clk), .m_rst(~dp_rst_n), .m_axis_tdata(d_tx_data), .m_axis_tkeep(), .m_axis_tvalid(d_tx_valid),
    .m_axis_tready(d_tx_ready), .m_axis_tlast(d_tx_last), .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),
    .s_pause_req(1'b0), .s_pause_ack(), .m_pause_req(1'b0), .m_pause_ack(),
    .s_status_depth(), .s_status_depth_commit(), .s_status_overflow(), .s_status_bad_frame(),
    .s_status_good_frame(), .m_status_depth(), .m_status_depth_commit(), .m_status_overflow(),
    .m_status_bad_frame(), .m_status_good_frame());

  // ---- the split datapath ----------------------------------------------------------
  milan_datapath #(.CTRL_SPLIT_P(SPLIT_P), .RXFILT_P(0), .GPTP_PLANE_EN_P(1'b0)) u_dp (
    .axis_clk(dp_clk), .axis_resetn(dp_rst_n), .gtx_clk(dp_clk), .gtx_resetn(dp_rst_n),
    .clk_audio_i(dp_clk), .clk_tdm_i(dp_clk), .i_ps_clk(dp_clk), .i_mmcm_locked(1'b1),
    .s_axis_mac_rx_tdata(rx_tdata), .s_axis_mac_rx_tkeep(rx_tkeep), .s_axis_mac_rx_tvalid(rx_tvalid),
    .s_axis_mac_rx_tlast(rx_tlast), .s_axis_mac_rx_tready(rx_tready),
    .m_axis_mac_tx_tdata(tx_tdata), .m_axis_mac_tx_tkeep(tx_tkeep), .m_axis_mac_tx_tvalid(tx_tvalid),
    .m_axis_mac_tx_tlast(tx_tlast), .m_axis_mac_tx_tready(tx_tready),
    .i_mac_speed(2'd2), .i_link_up(link_up), .i_full_duplex(1'b1),
    .s_axi_awaddr(16'd0), .s_axi_awvalid(1'b0), .s_axi_wdata(32'd0), .s_axi_wstrb(4'd0), .s_axi_wvalid(1'b0),
    .s_axi_bready(1'b1), .s_axi_araddr(16'd0), .s_axi_arvalid(1'b0), .s_axi_rready(1'b1),
    .o_ctl_rx_valid(d_rx_valid), .o_ctl_rx_data(d_rx_data), .o_ctl_rx_last(d_rx_last), .i_ctl_rx_ready(d_rx_ready),
    .i_ctl_tx_valid(d_tx_valid), .i_ctl_tx_data(d_tx_data), .i_ctl_tx_last(d_tx_last), .o_ctl_tx_ready(d_tx_ready),
    .o_ctl_link_up(d_link_up), .o_ctl_gm_change_p(d_gm_change_p), .o_ctl_gm_id(d_gm_id),
    .o_ctl_gptp_domain(d_gptp_domain),
    .i_ctl_pub_da_gate(d_da_gate), .i_ctl_pub_licence(d_licence), .i_ctl_pub_talker_decl(d_talker_decl),
    .i_ctl_pub_src_sid(d_src_sid), .i_ctl_pub_idle_slope(d_idle_slope), .i_ctl_pub_dom_vid(d_dom_vid),
    .i_ctl_pub_dom_prio(d_dom_prio), .i_ctl_pub_dom_adopted(d_dom_adopted), .i_ctl_pub_bound(d_bound),
    .i_ctl_pub_sid_valid(d_sid_valid), .i_ctl_pub_started(d_started), .i_ctl_pub_sid(d_sid),
    .i_ctl_cur_config(d_cur_config), .i_ctl_identify(d_identify), .i_ctl_clk_src_index(d_clk_src),
    .i_ctl_lock_held(d_lock_held), .i_ctl_dyn_dirty(d_dyn_dirty), .i_ctl_pt_offset(d_pt_offset),
    .i_ctl_pt_offset_v(d_pt_offset_v), .i_ctl_fmt_out(d_fmt_out), .i_ctl_fmt_out_v(d_fmt_out_v),
    .i_ctl_fmt_in(d_fmt_in), .i_ctl_fmt_in_v(d_fmt_in_v), .i_ctl_restore(d_restore), .i_ctl_rs_cause(d_rs_cause),
    .i_ctl_restore_cause(d_restore_cause), .i_ctl_nvm(d_nvm), .i_ctl_nvm_verdict(d_nvm_verdict),
    .i_ctl_ctr_req(d_ctr_req), .i_ctl_ctr_type(d_ctr_type), .i_ctl_ctr_index(d_ctr_index),
    .i_ctl_ctr_word(d_ctr_word), .o_ctl_ctr_data(d_ctr_data), .o_ctl_ctr_wait(d_ctr_wait),
    .i_ctl_amap_req(d_amap_req), .i_ctl_amap_type(d_amap_type), .i_ctl_amap_index(d_amap_index),
    .i_ctl_amap_map_index(d_amap_map_index), .i_ctl_amap_sel(d_amap_sel), .i_ctl_amap_rec(d_amap_rec),
    .o_ctl_amap_data(d_amap_data), .o_ctl_amap_wait(d_amap_wait),
    .i_ctl_edit_req(d_edit_req), .i_ctl_edit_phase(d_edit_phase), .i_ctl_edit_remove(d_edit_remove),
    .i_ctl_edit_type(d_edit_type), .i_ctl_edit_index(d_edit_index), .i_ctl_edit_count(d_edit_count),
    .i_ctl_edit_rec(d_edit_rec), .i_ctl_edit_record(d_edit_record), .i_ctl_edit_value(d_edit_value),
    .o_ctl_edit_data(d_edit_data), .o_ctl_edit_wait(d_edit_wait),
    .i_ctl_gsi_req(d_gsi_req), .i_ctl_gsi_kind(d_gsi_kind), .i_ctl_gsi_type(d_gsi_type),
    .i_ctl_gsi_index(d_gsi_index), .i_ctl_gsi_sel(d_gsi_sel), .i_ctl_gsi_ord(d_gsi_ord), .i_ctl_gsi_prop(d_gsi_prop),
    .o_ctl_gsi_data(d_gsi_data), .o_ctl_gsi_wait(d_gsi_wait),
    .o_ctl_ctr_chg_valid(d_ctr_chg_valid), .o_ctl_ctr_chg_type(d_ctr_chg_type),
    .o_ctl_ctr_chg_index(d_ctr_chg_index), .o_ctl_avb_chg_p(d_avb_chg_p), .o_ctl_asp_chg_p(d_asp_chg_p),
    .o_ctl_amap_wr_p(d_amap_wr_p));

  // ---- the probes --------------------------------------------------------------------
  localparam int unsigned NSRC = $bits(u_dp.pp_cd_acmp_declaring_w);
  localparam int unsigned NSNK = $bits(u_dp.pp_cd_acmp_bound_w);
  assign p_declaring    = 16'(u_dp.pp_cd_acmp_declaring_w);
  assign p_active       = 16'(u_dp.pp_cd_srp_active_w);
  assign p_admitted     = 16'(u_dp.pp_cd_srp_sr_admitted_w);
  assign p_bound        = 16'(u_dp.pp_cd_acmp_bound_w);
  assign p_started      = 16'(u_dp.pp_aecp_strm_started_w);
  assign p_bound_sid0   = u_dp.pp_cd_acmp_bound_sid_w[63:0];
  assign p_src_sid0     = u_dp.pp_cd_src_stream_id_w[63:0];
  assign p_vid          = u_dp.pp_cd_srp_class_a_vid_w;
  assign p_prio         = u_dp.pp_cd_srp_class_a_prio_w;
  assign p_adopted      = u_dp.pp_cd_srp_domain_adopted_w;
  assign p_slope        = u_dp.pp_cd_srp_sum_slope_bps_w;
  assign p_tk_decl0     = u_dp.pp_cd_srp_tk_decl_state_w[1:0];
  assign p_clk_src      = u_dp.pp_aecp_clk_src_index_w;
  assign p_cur_config   = u_dp.pp_aecp_cur_config_w;
  assign p_identify     = u_dp.pp_aecp_identify_w;
  assign p_lock_held    = u_dp.aecp_locked;
  assign p_fmt_out0     = u_dp.pp_aecp_fmt_out_w[63:0];
  assign p_fmt_out_v0   = u_dp.pp_aecp_fmt_out_v_w[0];
  assign p_pt_offset0   = u_dp.pp_aecp_pt_offset_w[31:0];
  assign p_restore_done = u_dp.pp_restore_done_w;
  assign p_nvm_backed   = u_dp.pp_nvm_backed_w;
  assign p_rx_frames    = u_dp.pp_rx_frames_w;
  assign p_tx_frames    = u_dp.pp_tx_frames_w;

  // the counts are the shape's: read so a width change is visible here
  logic unused_ok;
  assign unused_ok = &{1'b0, NSRC[0], NSNK[0], fw_ctrl_ready, m_tx_if, m_tx_ch};

endmodule

`default_nettype wire
