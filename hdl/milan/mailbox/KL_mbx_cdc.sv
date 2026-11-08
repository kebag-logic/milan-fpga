// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//---------------------------------------------------------------------------//
//  File        : KL_mbx_cdc.sv
//  Description : The split placement's crossing between the mailbox (KL_mbx,
//                the CPU's clock, sys) and the datapath (milan_datapath's
//                clock, milan_cd), one interface (#665 F-INT PR 2). The
//                control frames cross in the SoC's async FIFOs; everything
//                else crosses here, through the approved primitives alone
//                (CONTRIBUTING.md section 1):
//
//                  publication  a free-running cdc_handshake: each transfer
//                               carries one coherent snapshot of the whole
//                               block, so the datapath never sees half of
//                               a multi-word value; firmware's write order
//                               is kept, as every snapshot is one sys cycle
//                  settings     KL_mbx holds every fw_*_o from fw_send_o
//                               until fw_ack_p_i; one cdc_pulse carries
//                               the request in and one the
//                               acknowledgement out, and the datapath
//                               clock takes the held bus on the edge that
//                               turns the acknowledgement
//                  windows      per window, one cdc_handshake carries the
//                               request and its tag in, a requester holds
//                               the datapath's req and fields until wait
//                               falls, and one carries the answer and the
//                               same tag back
//                  events       a free-running cdc_handshake carries the
//                               counter-change pending bits in the
//                               contract's layout, the three face events,
//                               the grandmaster change, and the GM identity,
//                               the domain and the LINK level as they are;
//                               the mailbox side posts each pending bit as
//                               one pulse
//
//                THE BOUNDS. A commit's acknowledgement and a window's
//                answer each take two crossings, a few cycles of each clock
//                (the window's own serving time aside), well inside the
//                contract's 64-cycle bounds (MBX_FACE_ACK_CYCLES_C,
//                MBX_WIN_*_WAIT_CYCLES_C) at the 100 MHz mailbox and 50 MHz
//                datapath clocks. A publication lands in the datapath clock
//                within one snapshot after it is written, before any frame
//                the firmware commits after it can cross the egress FIFO.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_mbx_cdc
  import KL_mbx_pkg::*;
#(
  parameter int unsigned S_C = MBX_N_PUB_SOURCES_C,   //! sources per interface
  parameter int unsigned K_C = MBX_N_PUB_SINKS_C      //! sinks per interface
) (
  input  wire              sys_clk_i,     //! the mailbox's clock
  input  wire              sys_rst_n,     //! synchronous active-low reset, sys
  input  wire              dp_clk_i,      //! the datapath's clock
  input  wire              dp_rst_n,      //! synchronous active-low reset, dp

  // ---- the mailbox side (sys), interface 0 of KL_mbx -----------------------
  input  wire  [S_C-1:0]   m_pub_da_gate_i,
  input  wire  [S_C-1:0]   m_pub_licence_i,
  input  wire  [S_C-1:0]   m_pub_talker_decl_i,
  input  wire  [S_C*64-1:0] m_pub_src_sid_i,
  input  wire  [31:0]      m_pub_idle_slope_bps_i,
  input  wire  [11:0]      m_pub_dom_vid_i,
  input  wire  [2:0]       m_pub_dom_prio_i,
  input  wire              m_pub_dom_adopted_i,
  input  wire  [K_C-1:0]   m_pub_bound_i,
  input  wire  [K_C-1:0]   m_pub_sid_valid_i,
  input  wire  [K_C-1:0]   m_pub_started_i,
  input  wire  [K_C*64-1:0] m_pub_sid_i,
  input  wire              m_fw_send_i,         //! a commit waits: every m_fw_* holds
  output logic             m_fw_ack_p_o,        //! the datapath took it
  input  wire  [15:0]      m_fw_cur_config_i,
  input  wire  [7:0]       m_fw_identify_i,
  input  wire  [15:0]      m_fw_clk_src_index_i,
  input  wire              m_fw_lock_held_i,
  input  wire              m_fw_dyn_dirty_i,
  input  wire  [S_C*32-1:0] m_fw_pt_offset_ns_i,
  input  wire  [S_C-1:0]   m_fw_pt_offset_v_i,
  input  wire  [S_C*64-1:0] m_fw_fmt_out_i,
  input  wire  [S_C-1:0]   m_fw_fmt_out_v_i,
  input  wire  [K_C*64-1:0] m_fw_fmt_in_i,
  input  wire  [K_C-1:0]   m_fw_fmt_in_v_i,
  input  wire  [5:0]       m_fw_restore_i,      //! {RB, CLOSED, BLANK, FAIL, DONE, BUSY}
  input  wire  [2:0]       m_fw_rs_cause_i,
  input  wire  [1:0]       m_fw_restore_cause_i,
  input  wire  [5:0]       m_fw_nvm_i,          //! {IMG_VALID, PEND, STALE, DIRTY, ALARM, BACKED}
  input  wire  [3:0]       m_fw_nvm_verdict_i,
  //! the four windows: a request with its tag and fields, held while open
  input  wire              m_ctr_req_i,
  input  wire  [MBX_CTR_STATUS_TAG_WIDTH_C-1:0] m_ctr_tag_i,
  input  wire  [15:0]      m_ctr_type_i,
  input  wire  [15:0]      m_ctr_index_i,
  input  wire  [5:0]       m_ctr_word_i,
  output logic             m_ctr_ans_p_o,
  output logic [MBX_CTR_STATUS_TAG_WIDTH_C-1:0] m_ctr_ans_tag_o,
  output logic [31:0]      m_ctr_ans_data_o,
  input  wire              m_amap_req_i,
  input  wire  [MBX_AMAP_STATUS_TAG_WIDTH_C-1:0] m_amap_tag_i,
  input  wire  [15:0]      m_amap_type_i,
  input  wire  [15:0]      m_amap_index_i,
  input  wire  [15:0]      m_amap_map_index_i,
  input  wire  [1:0]       m_amap_sel_i,
  input  wire  [7:0]       m_amap_rec_i,
  output logic             m_amap_ans_p_o,
  output logic [MBX_AMAP_STATUS_TAG_WIDTH_C-1:0] m_amap_ans_tag_o,
  output logic [63:0]      m_amap_ans_data_o,
  input  wire              m_edit_req_i,
  input  wire  [MBX_EDIT_STATUS_TAG_WIDTH_C-1:0] m_edit_tag_i,
  input  wire  [15:0]      m_edit_type_i,
  input  wire  [15:0]      m_edit_index_i,
  input  wire  [2:0]       m_edit_phase_i,
  input  wire              m_edit_remove_i,
  input  wire  [7:0]       m_edit_rec_i,
  input  wire  [15:0]      m_edit_count_i,
  input  wire  [63:0]      m_edit_record_i,
  input  wire  [63:0]      m_edit_value_i,
  output logic             m_edit_ans_p_o,
  output logic [MBX_EDIT_STATUS_TAG_WIDTH_C-1:0] m_edit_ans_tag_o,
  output logic [63:0]      m_edit_ans_data_o,
  input  wire              m_gsi_req_i,
  input  wire  [MBX_GSI_STATUS_TAG_WIDTH_C-1:0] m_gsi_tag_i,
  input  wire  [15:0]      m_gsi_type_i,
  input  wire  [15:0]      m_gsi_index_i,
  input  wire  [1:0]       m_gsi_kind_i,
  input  wire  [3:0]       m_gsi_sel_i,
  input  wire  [7:0]       m_gsi_ord_i,
  input  wire  [63:0]      m_gsi_prop_i,
  output logic             m_gsi_ans_p_o,
  output logic [MBX_GSI_STATUS_TAG_WIDTH_C-1:0] m_gsi_ans_tag_o,
  output logic [63:0]      m_gsi_ans_data_o,
  //! the face events and the GM and LINK sources, posted to KL_mbx
  output logic             m_ctr_chg_p_o,
  output logic [15:0]      m_ctr_chg_type_o,
  output logic [15:0]      m_ctr_chg_index_o,
  output logic             m_avb_chg_p_o,
  output logic             m_asp_chg_p_o,
  output logic             m_amap_wr_p_o,
  output logic             m_link_up_o,
  output logic             m_gm_change_p_o,
  output logic [63:0]      m_gm_id_o,
  output logic [7:0]       m_gptp_domain_o,

  // ---- the datapath side (dp), milan_datapath's ctl ports ------------------
  output logic [S_C-1:0]   d_pub_da_gate_o,
  output logic [S_C-1:0]   d_pub_licence_o,
  output logic [S_C-1:0]   d_pub_talker_decl_o,
  output logic [S_C*64-1:0] d_pub_src_sid_o,
  output logic [31:0]      d_pub_idle_slope_bps_o,
  output logic [11:0]      d_pub_dom_vid_o,
  output logic [2:0]       d_pub_dom_prio_o,
  output logic             d_pub_dom_adopted_o,
  output logic [K_C-1:0]   d_pub_bound_o,
  output logic [K_C-1:0]   d_pub_sid_valid_o,
  output logic [K_C-1:0]   d_pub_started_o,
  output logic [K_C*64-1:0] d_pub_sid_o,
  output logic [15:0]      d_cur_config_o,
  output logic [7:0]       d_identify_o,
  output logic [15:0]      d_clk_src_index_o,
  output logic             d_lock_held_o,
  output logic             d_dyn_dirty_o,
  output logic [S_C*32-1:0] d_pt_offset_ns_o,
  output logic [S_C-1:0]   d_pt_offset_v_o,
  output logic [S_C*64-1:0] d_fmt_out_o,
  output logic [S_C-1:0]   d_fmt_out_v_o,
  output logic [K_C*64-1:0] d_fmt_in_o,
  output logic [K_C-1:0]   d_fmt_in_v_o,
  output logic [5:0]       d_restore_o,
  output logic [2:0]       d_rs_cause_o,
  output logic [1:0]       d_restore_cause_o,
  output logic [5:0]       d_nvm_o,
  output logic [3:0]       d_nvm_verdict_o,
  output logic             d_ctr_req_o,
  output logic [15:0]      d_ctr_type_o,
  output logic [15:0]      d_ctr_index_o,
  output logic [5:0]       d_ctr_word_o,
  input  wire  [31:0]      d_ctr_data_i,
  input  wire              d_ctr_wait_i,
  output logic             d_amap_req_o,
  output logic [15:0]      d_amap_type_o,
  output logic [15:0]      d_amap_index_o,
  output logic [15:0]      d_amap_map_index_o,
  output logic [1:0]       d_amap_sel_o,
  output logic [7:0]       d_amap_rec_o,
  input  wire  [63:0]      d_amap_data_i,
  input  wire              d_amap_wait_i,
  output logic             d_edit_req_o,
  output logic [2:0]       d_edit_phase_o,
  output logic             d_edit_remove_o,
  output logic [15:0]      d_edit_type_o,
  output logic [15:0]      d_edit_index_o,
  output logic [15:0]      d_edit_count_o,
  output logic [7:0]       d_edit_rec_o,
  output logic [63:0]      d_edit_record_o,
  output logic [63:0]      d_edit_value_o,
  input  wire  [63:0]      d_edit_data_i,
  input  wire              d_edit_wait_i,
  output logic             d_gsi_req_o,
  output logic [1:0]       d_gsi_kind_o,
  output logic [15:0]      d_gsi_type_o,
  output logic [15:0]      d_gsi_index_o,
  output logic [3:0]       d_gsi_sel_o,
  output logic [7:0]       d_gsi_ord_o,
  output logic [63:0]      d_gsi_prop_o,
  input  wire  [63:0]      d_gsi_data_i,
  input  wire              d_gsi_wait_i,
  input  wire              d_ctr_chg_valid_i,   //! one descriptor a cycle while any is pending
  input  wire  [15:0]      d_ctr_chg_type_i,
  input  wire  [15:0]      d_ctr_chg_index_i,
  input  wire              d_avb_chg_p_i,
  input  wire              d_asp_chg_p_i,
  input  wire              d_amap_wr_p_i,
  input  wire              d_link_up_i,
  input  wire              d_gm_change_p_i,
  input  wire  [63:0]      d_gm_id_i,
  input  wire  [7:0]       d_gptp_domain_i
);

  // ======================================================================= //
  //  The publication block: one coherent snapshot per transfer             //
  // ======================================================================= //
  localparam int unsigned PUB_W_C = 3 * S_C + S_C * 64 + 32 + 12 + 3 + 1 + 3 * K_C + K_C * 64;
  logic [PUB_W_C-1:0] pub_src_w, pub_dst_w;
  logic               pub_send_r, pub_rcv_w;
  assign pub_src_w = {m_pub_da_gate_i, m_pub_licence_i, m_pub_talker_decl_i, m_pub_src_sid_i,
                      m_pub_idle_slope_bps_i, m_pub_dom_vid_i, m_pub_dom_prio_i, m_pub_dom_adopted_i,
                      m_pub_bound_i, m_pub_sid_valid_i, m_pub_started_i, m_pub_sid_i};
  //! send, wait for the destination's capture, drop for one cycle, send again
  always_ff @(posedge sys_clk_i) begin : pub_loop
    if (!sys_rst_n) pub_send_r <= 1'b0;
    else if (pub_send_r) pub_send_r <= ~pub_rcv_w;
    else pub_send_r <= 1'b1;
  end : pub_loop
  cdc_handshake #(.WIDTH(PUB_W_C)) u_pub (
    .src_clk(sys_clk_i), .src_rst_n(sys_rst_n), .src_in(pub_src_w), .src_send(pub_send_r), .src_rcv(pub_rcv_w),
    .dest_clk(dp_clk_i), .dest_rst_n(dp_rst_n), .dest_out(pub_dst_w), .dest_req());
  //! dest_out holds the last snapshot until the next one lands
  assign {d_pub_da_gate_o, d_pub_licence_o, d_pub_talker_decl_o, d_pub_src_sid_o,
          d_pub_idle_slope_bps_o, d_pub_dom_vid_o, d_pub_dom_prio_o, d_pub_dom_adopted_o,
          d_pub_bound_o, d_pub_sid_valid_o, d_pub_started_o, d_pub_sid_o} = pub_dst_w;

  // ======================================================================= //
  //  The settings: the held bus, taken on the request                      //
  // ======================================================================= //
  localparam int unsigned FW_W_C = 16 + 8 + 16 + 1 + 1 + S_C * 32 + S_C + S_C * 64 + S_C + K_C * 64 + K_C
                                   + 6 + 3 + 2 + 6 + 4;
  logic [FW_W_C-1:0] fw_bus_w, fw_r;
  assign fw_bus_w = {m_fw_cur_config_i, m_fw_identify_i, m_fw_clk_src_index_i, m_fw_lock_held_i,
                     m_fw_dyn_dirty_i, m_fw_pt_offset_ns_i, m_fw_pt_offset_v_i, m_fw_fmt_out_i, m_fw_fmt_out_v_i,
                     m_fw_fmt_in_i, m_fw_fmt_in_v_i, m_fw_restore_i, m_fw_rs_cause_i, m_fw_restore_cause_i,
                     m_fw_nvm_i, m_fw_nvm_verdict_i};
  //! Two cdc_pulse crossings, with KL_mbx's hold in place of cdc_handshake's
  //! data_hold: KL_mbx holds every m_fw_* from fw_send_o until fw_ack_p_i.
  //! The datapath takes the bus on the edge the request's dest_pulse is high,
  //! and that same pulse turns the acknowledgement's source level on that
  //! same edge, so no acknowledgement can let the bus move before it is taken.
  logic fw_send_q_r, fw_req_p_w, fw_take_p_w;
  always_ff @(posedge sys_clk_i) begin : fw_req
    if (!sys_rst_n) fw_send_q_r <= 1'b0;
    else            fw_send_q_r <= m_fw_send_i;
  end : fw_req
  assign fw_req_p_w = m_fw_send_i & ~fw_send_q_r;
  cdc_pulse u_fw_req (.src_clk(sys_clk_i), .src_rst_n(sys_rst_n), .src_pulse(fw_req_p_w),
                      .dest_clk(dp_clk_i), .dest_rst_n(dp_rst_n), .dest_pulse(fw_take_p_w));
  cdc_pulse u_fw_ack (.src_clk(dp_clk_i), .src_rst_n(dp_rst_n), .src_pulse(fw_take_p_w),
                      .dest_clk(sys_clk_i), .dest_rst_n(sys_rst_n), .dest_pulse(m_fw_ack_p_o));
  always_ff @(posedge dp_clk_i) begin : fw_take
    if (!dp_rst_n)        fw_r <= '0;
    else if (fw_take_p_w) fw_r <= fw_bus_w;
  end : fw_take
  assign {d_cur_config_o, d_identify_o, d_clk_src_index_o, d_lock_held_o, d_dyn_dirty_o, d_pt_offset_ns_o,
          d_pt_offset_v_o, d_fmt_out_o, d_fmt_out_v_o, d_fmt_in_o, d_fmt_in_v_o, d_restore_o, d_rs_cause_o,
          d_restore_cause_o, d_nvm_o, d_nvm_verdict_o} = fw_r;

  // ======================================================================= //
  //  The four windows                                                       //
  // ======================================================================= //
  localparam int unsigned CTR_RQ_C  = 16 + 16 + 6;
  localparam int unsigned AMAP_RQ_C = 16 + 16 + 16 + 2 + 8;
  localparam int unsigned EDIT_RQ_C = 3 + 1 + 16 + 16 + 16 + 8 + 64 + 64;
  localparam int unsigned GSI_RQ_C  = 2 + 16 + 16 + 4 + 8 + 64;
  logic [CTR_RQ_C-1:0]  ctr_rq_w;
  logic [AMAP_RQ_C-1:0] amap_rq_w;
  logic [EDIT_RQ_C-1:0] edit_rq_w;
  logic [GSI_RQ_C-1:0]  gsi_rq_w;

  KL_mbx_cdc_window #(.TAG_W_P(MBX_CTR_STATUS_TAG_WIDTH_C), .RQ_W_P(CTR_RQ_C), .ANS_W_P(32)) u_ctr (
    .sys_clk_i, .sys_rst_n, .dp_clk_i, .dp_rst_n,
    .m_req_i(m_ctr_req_i), .m_tag_i(m_ctr_tag_i), .m_rq_i({m_ctr_type_i, m_ctr_index_i, m_ctr_word_i}),
    .m_ans_p_o(m_ctr_ans_p_o), .m_ans_tag_o(m_ctr_ans_tag_o), .m_ans_data_o(m_ctr_ans_data_o),
    .d_req_o(d_ctr_req_o), .d_rq_o(ctr_rq_w), .d_data_i(d_ctr_data_i), .d_wait_i(d_ctr_wait_i));
  assign {d_ctr_type_o, d_ctr_index_o, d_ctr_word_o} = ctr_rq_w;

  KL_mbx_cdc_window #(.TAG_W_P(MBX_AMAP_STATUS_TAG_WIDTH_C), .RQ_W_P(AMAP_RQ_C), .ANS_W_P(64)) u_amap (
    .sys_clk_i, .sys_rst_n, .dp_clk_i, .dp_rst_n,
    .m_req_i(m_amap_req_i), .m_tag_i(m_amap_tag_i),
    .m_rq_i({m_amap_type_i, m_amap_index_i, m_amap_map_index_i, m_amap_sel_i, m_amap_rec_i}),
    .m_ans_p_o(m_amap_ans_p_o), .m_ans_tag_o(m_amap_ans_tag_o), .m_ans_data_o(m_amap_ans_data_o),
    .d_req_o(d_amap_req_o), .d_rq_o(amap_rq_w), .d_data_i(d_amap_data_i), .d_wait_i(d_amap_wait_i));
  assign {d_amap_type_o, d_amap_index_o, d_amap_map_index_o, d_amap_sel_o, d_amap_rec_o} = amap_rq_w;

  KL_mbx_cdc_window #(.TAG_W_P(MBX_EDIT_STATUS_TAG_WIDTH_C), .RQ_W_P(EDIT_RQ_C), .ANS_W_P(64)) u_edit (
    .sys_clk_i, .sys_rst_n, .dp_clk_i, .dp_rst_n,
    .m_req_i(m_edit_req_i), .m_tag_i(m_edit_tag_i),
    .m_rq_i({m_edit_phase_i, m_edit_remove_i, m_edit_type_i, m_edit_index_i, m_edit_count_i, m_edit_rec_i,
             m_edit_record_i, m_edit_value_i}),
    .m_ans_p_o(m_edit_ans_p_o), .m_ans_tag_o(m_edit_ans_tag_o), .m_ans_data_o(m_edit_ans_data_o),
    .d_req_o(d_edit_req_o), .d_rq_o(edit_rq_w), .d_data_i(d_edit_data_i), .d_wait_i(d_edit_wait_i));
  assign {d_edit_phase_o, d_edit_remove_o, d_edit_type_o, d_edit_index_o, d_edit_count_o, d_edit_rec_o,
          d_edit_record_o, d_edit_value_o} = edit_rq_w;

  KL_mbx_cdc_window #(.TAG_W_P(MBX_GSI_STATUS_TAG_WIDTH_C), .RQ_W_P(GSI_RQ_C), .ANS_W_P(64)) u_gsi (
    .sys_clk_i, .sys_rst_n, .dp_clk_i, .dp_rst_n,
    .m_req_i(m_gsi_req_i), .m_tag_i(m_gsi_tag_i),
    .m_rq_i({m_gsi_kind_i, m_gsi_type_i, m_gsi_index_i, m_gsi_sel_i, m_gsi_ord_i, m_gsi_prop_i}),
    .m_ans_p_o(m_gsi_ans_p_o), .m_ans_tag_o(m_gsi_ans_tag_o), .m_ans_data_o(m_gsi_ans_data_o),
    .d_req_o(d_gsi_req_o), .d_rq_o(gsi_rq_w), .d_data_i(d_gsi_data_i), .d_wait_i(d_gsi_wait_i));
  assign {d_gsi_kind_o, d_gsi_type_o, d_gsi_index_o, d_gsi_sel_o, d_gsi_ord_o, d_gsi_prop_o} = gsi_rq_w;

  // ======================================================================= //
  //  The events: pending bits out of the datapath clock                     //
  // ======================================================================= //
  //! A counter change maps to its descriptor's pending bit in the contract's
  //! layout (MBX_CTRCHG_*), any other descriptor to the ALL bit, as KL_mbx
  //! keeps them; then the three face events and the GM change.
  localparam int unsigned NP_C  = MBX_CTRCHG_N_PEND_C;
  localparam int unsigned EV_W_C = NP_C + 5;
  logic [NP_C-1:0]   ctr_bit_w;
  always_comb begin : ctr_bit
    ctr_bit_w = '0;
    if (d_ctr_chg_valid_i) begin
      ctr_bit_w[MBX_CTRCHG_ALL_BIT_C] = 1'b1;
      for (int unsigned f = 0; f < MBX_CTRCHG_N_SRC_C; f++) begin
        if ((32'(d_ctr_chg_type_i) == MBX_CTRCHG_TYPE_TBL_C[f])
            && (32'(d_ctr_chg_index_i) < MBX_CTRCHG_COUNT_TBL_C[f])) begin
          ctr_bit_w[MBX_CTRCHG_ALL_BIT_C] = 1'b0;
          ctr_bit_w[MBX_CTRCHG_FIRST_TBL_C[f] + 32'(d_ctr_chg_index_i)] = 1'b1;
        end
      end
    end
  end : ctr_bit

  logic [EV_W_C-1:0] ev_pend_r, ev_new_w, ev_hold_r;
  logic [63:0]       ev_gm_r;
  logic [7:0]        ev_dom_r;
  logic              ev_send_r, ev_rcv_w, ev_req_w;
  logic [EV_W_C+72-1:0] ev_src_w, ev_dst_w;
  assign ev_new_w = {1'b0, d_gm_change_p_i, d_amap_wr_p_i, d_asp_chg_p_i, d_avb_chg_p_i, ctr_bit_w};
  //! The datapath side gathers pending bits; a transfer takes all of them at
  //! its rising edge and new ones gather behind it, so none is lost. Several
  //! events of one source inside one transfer post once: KL_mbx coalesces
  //! them into one record anyway (contract 2.3, the face events).
  always_ff @(posedge dp_clk_i) begin : ev_gather
    if (!dp_rst_n) begin
      ev_pend_r <= '0;
      ev_hold_r <= '0;
      ev_gm_r   <= 64'd0;
      ev_dom_r  <= 8'd0;
      ev_send_r <= 1'b0;
    end else if (!ev_send_r) begin
      //! start a transfer: hand the pending bits over, with the GM's current
      //! identity and the LINK level, each as it is now
      ev_hold_r <= {d_link_up_i, ev_pend_r[EV_W_C-2:0] | ev_new_w[EV_W_C-2:0]};
      ev_gm_r   <= d_gm_id_i;
      ev_dom_r  <= d_gptp_domain_i;
      ev_pend_r <= '0;
      ev_send_r <= 1'b1;
    end else begin
      ev_pend_r <= ev_pend_r | ev_new_w;
      if (ev_rcv_w) ev_send_r <= 1'b0;
    end
  end : ev_gather
  assign ev_src_w = {ev_hold_r, ev_gm_r, ev_dom_r};
  cdc_handshake #(.WIDTH(EV_W_C + 72)) u_ev (
    .src_clk(dp_clk_i), .src_rst_n(dp_rst_n), .src_in(ev_src_w), .src_send(ev_send_r), .src_rcv(ev_rcv_w),
    .dest_clk(sys_clk_i), .dest_rst_n(sys_rst_n), .dest_out(ev_dst_w), .dest_req(ev_req_w));

  //! the mailbox side: every received bit pending until it is posted, the
  //! counter changes one a cycle, lowest bit first; the GM identity held
  logic [NP_C-1:0] mc_pend_r;
  logic [2:0]      mf_pend_r;
  logic            mg_pend_r;
  logic [NP_C-1:0] mc_pick_w;
  logic [15:0]     mc_type_w, mc_index_w;
  always_comb begin : mc_pick
    mc_pick_w  = '0;
    mc_type_w  = 16'd0;
    mc_index_w = 16'd0;
    for (int unsigned b = 0; b < NP_C; b++) begin
      if (mc_pend_r[b] && (mc_pick_w == '0)) begin
        mc_pick_w[b] = 1'b1;
        //! the ALL bit names no descriptor KL_mbx serves per descriptor
        mc_type_w  = 16'hFFFF;
        mc_index_w = 16'd0;
        for (int unsigned f = 0; f < MBX_CTRCHG_N_SRC_C; f++) begin
          if ((b >= MBX_CTRCHG_FIRST_TBL_C[f]) && (b < MBX_CTRCHG_FIRST_TBL_C[f] + MBX_CTRCHG_COUNT_TBL_C[f])) begin
            mc_type_w  = 16'(MBX_CTRCHG_TYPE_TBL_C[f]);
            mc_index_w = 16'(b - MBX_CTRCHG_FIRST_TBL_C[f]);
          end
        end
      end
    end
  end : mc_pick

  always_ff @(posedge sys_clk_i) begin : m_post
    if (!sys_rst_n) begin
      mc_pend_r         <= '0;
      mf_pend_r         <= 3'd0;
      mg_pend_r         <= 1'b0;
      m_gm_id_o         <= 64'd0;
      m_gptp_domain_o   <= 8'd0;
      m_ctr_chg_p_o     <= 1'b0;
      m_ctr_chg_type_o  <= 16'd0;
      m_ctr_chg_index_o <= 16'd0;
      m_avb_chg_p_o     <= 1'b0;
      m_asp_chg_p_o     <= 1'b0;
      m_amap_wr_p_o     <= 1'b0;
      m_gm_change_p_o   <= 1'b0;
      m_link_up_o       <= 1'b0;
    end else begin
      //! one pulse a cycle per source, each with its descriptor
      m_ctr_chg_p_o     <= |mc_pick_w;
      m_ctr_chg_type_o  <= mc_type_w;
      m_ctr_chg_index_o <= mc_index_w;
      {m_amap_wr_p_o, m_asp_chg_p_o, m_avb_chg_p_o} <= mf_pend_r;
      //! the GM pulse a cycle after the identity it reports is held
      m_gm_change_p_o   <= mg_pend_r;
      mc_pend_r <= mc_pend_r & ~mc_pick_w;
      mf_pend_r <= 3'd0;
      mg_pend_r <= 1'b0;
      if (ev_req_w) begin
        mc_pend_r       <= (mc_pend_r & ~mc_pick_w) | ev_dst_w[72 +: NP_C];
        mf_pend_r       <= ev_dst_w[72 + NP_C +: 3];
        mg_pend_r       <= ev_dst_w[72 + NP_C + 3];
        m_link_up_o     <= ev_dst_w[72 + NP_C + 4];
        m_gm_id_o       <= ev_dst_w[8 +: 64];
        m_gptp_domain_o <= ev_dst_w[0 +: 8];
      end
    end
  end : m_post

endmodule

`default_nettype wire
