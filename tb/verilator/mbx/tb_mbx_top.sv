/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : tb_mbx_top.sv
//  Project     : Milan FPGA Platform (packet mailbox suite, #665 lane F0)
//
//  Description : Pure wiring: one KL_mbx behind ONE of its two bus
//                adapters, chosen by HOST_P (0 the Wishbone adapter the
//                on-chip RISC-V reaches, 1 the AXI4-Lite adapter a hard core
//                reaches). The harness builds this top twice and runs the
//                same checks through each, so the two hosts are graded
//                against one contract rather than each against its own
//                expectations.
//
//                The one decision that matters: the adapter that is not
//                built is not tied into the mailbox. Its bus inputs are read
//                into an unused sink and its outputs are driven to zero, so
//                a check that passes through the wrong adapter cannot pass.
//---------------------------------------------------------------------------//

`default_nettype none

module tb_mbx_top
  import KL_mbx_pkg::*;
#(
  parameter int unsigned HOST_P = 0   //! 0 Wishbone (KL_mbx_wb), 1 AXI4-Lite (KL_mbx_axil)
) (
  input  wire                        clk_i,          //! the mailbox clock
  input  wire                        rst_n,          //! synchronous active-low reset

  input  wire                        wb_cyc_i,       //! Wishbone CYC
  input  wire                        wb_stb_i,       //! Wishbone STB
  input  wire                        wb_we_i,        //! Wishbone WE
  input  wire  [29:0]                wb_adr_i,       //! Wishbone word address
  input  wire  [31:0]                wb_dat_i,       //! Wishbone write data
  input  wire  [3:0]                 wb_sel_i,       //! Wishbone byte selects
  output logic                       wb_ack_o,       //! Wishbone ACK
  output logic [31:0]                wb_dat_o,       //! Wishbone read data
  output logic                       wb_err_o,       //! Wishbone ERR

  input  wire                        s_awvalid_i,    //! AXI4-Lite AWVALID
  output logic                       s_awready_o,    //! AXI4-Lite AWREADY
  input  wire  [MBX_ADDR_W_C+1:0]    s_awaddr_i,     //! AXI4-Lite AWADDR
  input  wire                        s_wvalid_i,     //! AXI4-Lite WVALID
  output logic                       s_wready_o,     //! AXI4-Lite WREADY
  input  wire  [31:0]                s_wdata_i,      //! AXI4-Lite WDATA
  input  wire  [3:0]                 s_wstrb_i,      //! AXI4-Lite WSTRB
  output logic                       s_bvalid_o,     //! AXI4-Lite BVALID
  input  wire                        s_bready_i,     //! AXI4-Lite BREADY
  output logic [1:0]                 s_bresp_o,      //! AXI4-Lite BRESP
  input  wire                        s_arvalid_i,    //! AXI4-Lite ARVALID
  output logic                       s_arready_o,    //! AXI4-Lite ARREADY
  input  wire  [MBX_ADDR_W_C+1:0]    s_araddr_i,     //! AXI4-Lite ARADDR
  output logic                       s_rvalid_o,     //! AXI4-Lite RVALID
  input  wire                        s_rready_i,     //! AXI4-Lite RREADY
  output logic [31:0]                s_rdata_o,      //! AXI4-Lite RDATA
  output logic [1:0]                 s_rresp_o,      //! AXI4-Lite RRESP

  output logic                       irq_o,          //! the mailbox interrupt

  input  wire                        ms_tick_p_i,    //! one-cycle pulse per millisecond
  input  wire  [MBX_N_IF_C-1:0]      link_up_i,      //! link level per interface
  input  wire  [MBX_N_IF_C-1:0]      gm_change_p_i,  //! grandmaster change pulse per interface
  input  wire  [MBX_N_IF_C*64-1:0]   gm_id_i,        //! gptp_grandmaster_id per interface
  input  wire  [MBX_N_IF_C*8-1:0]    gptp_domain_i,  //! gptp_domain_number per interface

  input  wire                        rx_valid_i,     //! ingress byte offered
  output logic                       rx_ready_o,     //! ingress byte taken
  input  wire  [7:0]                 rx_data_i,      //! ingress byte
  input  wire                        rx_last_i,      //! ingress last byte
  input  wire  [MBX_IF_W_C-1:0]      rx_if_i,        //! ingress interface

  output logic                       tx_valid_o,     //! egress byte offered
  input  wire                        tx_ready_i,     //! egress byte taken
  output logic [7:0]                 tx_data_o,      //! egress byte
  output logic                       tx_last_o,      //! egress last byte
  output logic [MBX_IF_W_C-1:0]      tx_if_o,        //! egress interface
  output logic [MBX_CH_W_C-1:0]      tx_ch_o,        //! egress channel

  // the publication block's outputs, KL_mbx's own (lane F-INT)
  output logic [MBX_N_IF_C*MBX_N_PUB_SOURCES_C-1:0]          pub_da_gate_o,     //! DA_GATE.OPEN
  output logic [MBX_N_IF_C*MBX_N_PUB_SOURCES_C-1:0]          pub_licence_o,     //! LICENCE.ACTIVE
  output logic [MBX_N_IF_C*MBX_IDLE_SLOPE_BPS_WIDTH_C-1:0]   pub_idle_slope_bps_o, //! IDLE_SLOPE.BPS
  output logic [MBX_N_IF_C*MBX_SR_DOMAIN_VID_WIDTH_C-1:0]    pub_dom_vid_o,     //! SR_DOMAIN.VID
  output logic [MBX_N_IF_C*MBX_SR_DOMAIN_PRIORITY_WIDTH_C-1:0] pub_dom_prio_o,  //! SR_DOMAIN.PRIORITY
  output logic [MBX_N_IF_C*MBX_SR_DOMAIN_ADOPTED_WIDTH_C-1:0]  pub_dom_adopted_o, //! SR_DOMAIN.ADOPTED
  output logic [MBX_N_IF_C*MBX_N_PUB_SOURCES_C-1:0]          pub_talker_decl_o, //! TALKER_DECL.DECLARED
  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C-1:0]            pub_bound_o,       //! BINDING.BOUND per sink
  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C-1:0]            pub_sid_valid_o,   //! BINDING.SID_VALID per sink
  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C-1:0]            pub_started_o,     //! BINDING.STARTED per sink
  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C*64-1:0]         pub_sid_o,         //! SID_HI:SID_LO per sink

  // the face block's ports, KL_mbx's own (contract 2.3): the bench answers the
  // windows and acknowledges the commits as the datapath of the split would
  // the face block: the settings, held from a commit until its acknowledgement
  output logic [MBX_N_IF_C-1:0] fw_send_o,   //! a commit waits for its acknowledgement: every fw_*_o holds
  input  wire  [MBX_N_IF_C-1:0] fw_ack_p_i,   //! one-cycle pulse per interface: the datapath took the commit
  output logic [MBX_N_IF_C*MBX_F_CTRL_READY_WIDTH_C-1:0] fw_ctrl_ready_o,   //! F_CTRL.READY per interface
  output logic [MBX_N_IF_C*MBX_F_ENTITY_CUR_CONFIG_WIDTH_C-1:0] fw_entity_cur_config_o,   //! F_ENTITY.CUR_CONFIG per interface
  output logic [MBX_N_IF_C*MBX_F_ENTITY_IDENTIFY_WIDTH_C-1:0] fw_entity_identify_o,   //! F_ENTITY.IDENTIFY per interface
  output logic [MBX_N_IF_C*MBX_F_CLOCK_SOURCE_INDEX_WIDTH_C-1:0] fw_clock_source_index_o,   //! F_CLOCK.SOURCE_INDEX per interface
  output logic [MBX_N_IF_C*MBX_F_AECP_LOCK_HELD_WIDTH_C-1:0] fw_aecp_lock_held_o,   //! F_AECP.LOCK_HELD per interface
  output logic [MBX_N_IF_C*MBX_F_AECP_DYN_DIRTY_WIDTH_C-1:0] fw_aecp_dyn_dirty_o,   //! F_AECP.DYN_DIRTY per interface
  output logic [MBX_N_IF_C*MBX_F_RESTORE_BUSY_WIDTH_C-1:0] fw_restore_busy_o,   //! F_RESTORE.BUSY per interface
  output logic [MBX_N_IF_C*MBX_F_RESTORE_DONE_WIDTH_C-1:0] fw_restore_done_o,   //! F_RESTORE.DONE per interface
  output logic [MBX_N_IF_C*MBX_F_RESTORE_FAIL_WIDTH_C-1:0] fw_restore_fail_o,   //! F_RESTORE.FAIL per interface
  output logic [MBX_N_IF_C*MBX_F_RESTORE_BLANK_WIDTH_C-1:0] fw_restore_blank_o,   //! F_RESTORE.BLANK per interface
  output logic [MBX_N_IF_C*MBX_F_RESTORE_CLOSED_WIDTH_C-1:0] fw_restore_closed_o,   //! F_RESTORE.CLOSED per interface
  output logic [MBX_N_IF_C*MBX_F_RESTORE_RB_WIDTH_C-1:0] fw_restore_rb_o,   //! F_RESTORE.RB per interface
  output logic [MBX_N_IF_C*MBX_F_RESTORE_RS_CAUSE_WIDTH_C-1:0] fw_restore_rs_cause_o,   //! F_RESTORE.RS_CAUSE per interface
  output logic [MBX_N_IF_C*MBX_F_RESTORE_CAUSE_WIDTH_C-1:0] fw_restore_cause_o,   //! F_RESTORE.CAUSE per interface
  output logic [MBX_N_IF_C*MBX_F_NVM_BACKED_WIDTH_C-1:0] fw_nvm_backed_o,   //! F_NVM.BACKED per interface
  output logic [MBX_N_IF_C*MBX_F_NVM_ALARM_WIDTH_C-1:0] fw_nvm_alarm_o,   //! F_NVM.ALARM per interface
  output logic [MBX_N_IF_C*MBX_F_NVM_DIRTY_WIDTH_C-1:0] fw_nvm_dirty_o,   //! F_NVM.DIRTY per interface
  output logic [MBX_N_IF_C*MBX_F_NVM_STALE_WIDTH_C-1:0] fw_nvm_stale_o,   //! F_NVM.STALE per interface
  output logic [MBX_N_IF_C*MBX_F_NVM_PEND_WIDTH_C-1:0] fw_nvm_pend_o,   //! F_NVM.PEND per interface
  output logic [MBX_N_IF_C*MBX_F_NVM_IMG_VALID_WIDTH_C-1:0] fw_nvm_img_valid_o,   //! F_NVM.IMG_VALID per interface
  output logic [MBX_N_IF_C*MBX_F_NVM_VERDICT_WIDTH_C-1:0] fw_nvm_verdict_o,   //! F_NVM.VERDICT per interface
  output logic [MBX_N_IF_C*MBX_N_PUB_SOURCES_C*32-1:0] fw_pt_offset_ns_o,   //! F_PT_OFFSET.NS per source
  output logic [MBX_N_IF_C*MBX_N_PUB_SOURCES_C*1-1:0] fw_pt_offset_v_o,   //! F_SRC_VALID.PT_OFFSET per source
  output logic [MBX_N_IF_C*MBX_N_PUB_SOURCES_C*64-1:0] fw_fmt_out_o,   //! F_FMT_OUT_HI.FMT:F_FMT_OUT_LO.FMT per source
  output logic [MBX_N_IF_C*MBX_N_PUB_SOURCES_C*1-1:0] fw_fmt_out_v_o,   //! F_SRC_VALID.FMT_OUT per source
  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C*64-1:0] fw_fmt_in_o,   //! F_FMT_IN_HI.FMT:F_FMT_IN_LO.FMT per sink
  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C*1-1:0] fw_fmt_in_v_o,   //! F_SNK_VALID.FMT_IN per sink
  // the CTR window: the request holds from its GO until its answer or 64 cycles
  output logic [MBX_N_IF_C-1:0] ctr_req_o,   //! a request is open: its fields and tag hold
  output logic [MBX_N_IF_C*MBX_CTR_STATUS_TAG_WIDTH_C-1:0] ctr_tag_o,   //! the open request's tag
  output logic [MBX_N_IF_C*16-1:0] ctr_type_o,   //! CTR_REQ.TYPE per interface
  output logic [MBX_N_IF_C*16-1:0] ctr_index_o,   //! CTR_REQ.INDEX per interface
  output logic [MBX_N_IF_C*6-1:0] ctr_word_o,   //! CTR_WORD.WORD per interface
  input  wire  [MBX_N_IF_C-1:0] ctr_ans_p_i,   //! one-cycle pulse: the answer, with its data and tag
  input  wire  [MBX_N_IF_C*MBX_CTR_STATUS_TAG_WIDTH_C-1:0] ctr_ans_tag_i,   //! the tag of the request it answers
  input  wire  [MBX_N_IF_C*32-1:0] ctr_ans_data_i,   //! the answer, valid with ctr_ans_p_i
  // the AMAP window: the request holds from its GO until its answer or 64 cycles
  output logic [MBX_N_IF_C-1:0] amap_req_o,   //! a request is open: its fields and tag hold
  output logic [MBX_N_IF_C*MBX_AMAP_STATUS_TAG_WIDTH_C-1:0] amap_tag_o,   //! the open request's tag
  output logic [MBX_N_IF_C*16-1:0] amap_type_o,   //! AMAP_REQ.TYPE per interface
  output logic [MBX_N_IF_C*16-1:0] amap_index_o,   //! AMAP_REQ.INDEX per interface
  output logic [MBX_N_IF_C*16-1:0] amap_map_index_o,   //! AMAP_PAGE.MAP_INDEX per interface
  output logic [MBX_N_IF_C*2-1:0] amap_sel_o,   //! AMAP_PAGE.SEL per interface
  output logic [MBX_N_IF_C*8-1:0] amap_rec_o,   //! AMAP_PAGE.REC per interface
  input  wire  [MBX_N_IF_C-1:0] amap_ans_p_i,   //! one-cycle pulse: the answer, with its data and tag
  input  wire  [MBX_N_IF_C*MBX_AMAP_STATUS_TAG_WIDTH_C-1:0] amap_ans_tag_i,   //! the tag of the request it answers
  input  wire  [MBX_N_IF_C*64-1:0] amap_ans_data_i,   //! the answer, valid with amap_ans_p_i
  // the EDIT window: the request holds from its GO until its answer or 64 cycles
  output logic [MBX_N_IF_C-1:0] edit_req_o,   //! a request is open: its fields and tag hold
  output logic [MBX_N_IF_C*MBX_EDIT_STATUS_TAG_WIDTH_C-1:0] edit_tag_o,   //! the open request's tag
  output logic [MBX_N_IF_C*16-1:0] edit_type_o,   //! EDIT_REQ.TYPE per interface
  output logic [MBX_N_IF_C*16-1:0] edit_index_o,   //! EDIT_REQ.INDEX per interface
  output logic [MBX_N_IF_C*3-1:0] edit_phase_o,   //! EDIT_BEAT.PHASE per interface
  output logic [MBX_N_IF_C*1-1:0] edit_remove_o,   //! EDIT_BEAT.REMOVE per interface
  output logic [MBX_N_IF_C*8-1:0] edit_rec_o,   //! EDIT_BEAT.REC per interface
  output logic [MBX_N_IF_C*16-1:0] edit_count_o,   //! EDIT_BEAT.COUNT per interface
  output logic [MBX_N_IF_C*64-1:0] edit_record_o,   //! EDIT_RECORD_HI.RECORD:EDIT_RECORD_LO.RECORD per interface
  output logic [MBX_N_IF_C*64-1:0] edit_value_o,   //! EDIT_VALUE_HI.VALUE:EDIT_VALUE_LO.VALUE per interface
  input  wire  [MBX_N_IF_C-1:0] edit_ans_p_i,   //! one-cycle pulse: the answer, with its data and tag
  input  wire  [MBX_N_IF_C*MBX_EDIT_STATUS_TAG_WIDTH_C-1:0] edit_ans_tag_i,   //! the tag of the request it answers
  input  wire  [MBX_N_IF_C*64-1:0] edit_ans_data_i,   //! the answer, valid with edit_ans_p_i
  // the GSI window: the request holds from its GO until its answer or 64 cycles
  output logic [MBX_N_IF_C-1:0] gsi_req_o,   //! a request is open: its fields and tag hold
  output logic [MBX_N_IF_C*MBX_GSI_STATUS_TAG_WIDTH_C-1:0] gsi_tag_o,   //! the open request's tag
  output logic [MBX_N_IF_C*16-1:0] gsi_type_o,   //! GSI_REQ.TYPE per interface
  output logic [MBX_N_IF_C*16-1:0] gsi_index_o,   //! GSI_REQ.INDEX per interface
  output logic [MBX_N_IF_C*2-1:0] gsi_kind_o,   //! GSI_SEL.KIND per interface
  output logic [MBX_N_IF_C*4-1:0] gsi_sel_o,   //! GSI_SEL.SEL per interface
  output logic [MBX_N_IF_C*8-1:0] gsi_ord_o,   //! GSI_SEL.ORD per interface
  output logic [MBX_N_IF_C*64-1:0] gsi_prop_o,   //! GSI_PROP_HI.FMT:GSI_PROP_LO.FMT per interface
  input  wire  [MBX_N_IF_C-1:0] gsi_ans_p_i,   //! one-cycle pulse: the answer, with its data and tag
  input  wire  [MBX_N_IF_C*MBX_GSI_STATUS_TAG_WIDTH_C-1:0] gsi_ans_tag_i,   //! the tag of the request it answers
  input  wire  [MBX_N_IF_C*64-1:0] gsi_ans_data_i,   //! the answer, valid with gsi_ans_p_i
  // the face block's events, one-cycle pulses per interface with their qualifiers
  input  wire  [MBX_N_IF_C-1:0] ctr_chg_p_i,   //! a served descriptor's counters moved
  input  wire  [MBX_N_IF_C*16-1:0] ctr_chg_type_i,   //! its descriptor_type, valid with ctr_chg_p_i
  input  wire  [MBX_N_IF_C*16-1:0] ctr_chg_index_i,   //! its descriptor_index, valid with ctr_chg_p_i
  input  wire  [MBX_N_IF_C-1:0] avb_chg_p_i,   //! a served GET_AVB_INFO word changed
  input  wire  [MBX_N_IF_C-1:0] asp_chg_p_i,   //! the served AS_PATH sequence changed
  input  wire  [MBX_N_IF_C-1:0] amap_wr_p_i   //! an edit's commit beat changed the live map
);

  logic                    host_req_w;
  logic                    host_we_w;
  logic [MBX_ADDR_W_C-1:0] host_addr_w;
  logic [31:0]             host_wdata_w;
  logic [3:0]              host_be_w;
  logic                    host_ack_w;
  logic [31:0]             host_rdata_w;

  if (HOST_P == 0) begin : g_wb
    KL_mbx_wb u_wb (
      .clk_i        (clk_i),
      .rst_n        (rst_n),
      .wb_cyc_i     (wb_cyc_i),
      .wb_stb_i     (wb_stb_i),
      .wb_we_i      (wb_we_i),
      .wb_adr_i     (wb_adr_i),
      .wb_dat_i     (wb_dat_i),
      .wb_sel_i     (wb_sel_i),
      .wb_ack_o     (wb_ack_o),
      .wb_dat_o     (wb_dat_o),
      .wb_err_o     (wb_err_o),
      .host_req_o   (host_req_w),
      .host_we_o    (host_we_w),
      .host_addr_o  (host_addr_w),
      .host_wdata_o (host_wdata_w),
      .host_be_o    (host_be_w),
      .host_ack_i   (host_ack_w),
      .host_rdata_i (host_rdata_w)
    );
    assign s_awready_o = 1'b0;
    assign s_wready_o  = 1'b0;
    assign s_bvalid_o  = 1'b0;
    assign s_bresp_o   = 2'b00;
    assign s_arready_o = 1'b0;
    assign s_rvalid_o  = 1'b0;
    assign s_rdata_o   = '0;
    assign s_rresp_o   = 2'b00;
    logic unused_axil_w;
    assign unused_axil_w = ^{s_awvalid_i, s_awaddr_i, s_wvalid_i, s_wdata_i, s_wstrb_i, s_bready_i,
                             s_arvalid_i, s_araddr_i, s_rready_i};
  end : g_wb
  else begin : g_axil
    KL_mbx_axil u_axil (
      .clk_i        (clk_i),
      .rst_n        (rst_n),
      .s_awvalid_i  (s_awvalid_i),
      .s_awready_o  (s_awready_o),
      .s_awaddr_i   (s_awaddr_i),
      .s_wvalid_i   (s_wvalid_i),
      .s_wready_o   (s_wready_o),
      .s_wdata_i    (s_wdata_i),
      .s_wstrb_i    (s_wstrb_i),
      .s_bvalid_o   (s_bvalid_o),
      .s_bready_i   (s_bready_i),
      .s_bresp_o    (s_bresp_o),
      .s_arvalid_i  (s_arvalid_i),
      .s_arready_o  (s_arready_o),
      .s_araddr_i   (s_araddr_i),
      .s_rvalid_o   (s_rvalid_o),
      .s_rready_i   (s_rready_i),
      .s_rdata_o    (s_rdata_o),
      .s_rresp_o    (s_rresp_o),
      .host_req_o   (host_req_w),
      .host_we_o    (host_we_w),
      .host_addr_o  (host_addr_w),
      .host_wdata_o (host_wdata_w),
      .host_be_o    (host_be_w),
      .host_ack_i   (host_ack_w),
      .host_rdata_i (host_rdata_w)
    );
    assign wb_ack_o = 1'b0;
    assign wb_dat_o = '0;
    assign wb_err_o = 1'b0;
    logic unused_wb_w;
    assign unused_wb_w = ^{wb_cyc_i, wb_stb_i, wb_we_i, wb_adr_i, wb_dat_i, wb_sel_i};
  end : g_axil

  KL_mbx u_mbx (
    .clk_i         (clk_i),
    .rst_n         (rst_n),
    .host_req_i    (host_req_w),
    .host_we_i     (host_we_w),
    .host_addr_i   (host_addr_w),
    .host_wdata_i  (host_wdata_w),
    .host_be_i     (host_be_w),
    .host_ack_o    (host_ack_w),
    .host_rdata_o  (host_rdata_w),
    .irq_o         (irq_o),
    .ms_tick_p_i   (ms_tick_p_i),
    .link_up_i     (link_up_i),
    .gm_change_p_i (gm_change_p_i),
    .gm_id_i       (gm_id_i),
    .gptp_domain_i (gptp_domain_i),
    .rx_valid_i    (rx_valid_i),
    .rx_ready_o    (rx_ready_o),
    .rx_data_i     (rx_data_i),
    .rx_last_i     (rx_last_i),
    .rx_if_i       (rx_if_i),
    .tx_valid_o    (tx_valid_o),
    .tx_ready_i    (tx_ready_i),
    .tx_data_o     (tx_data_o),
    .tx_last_o     (tx_last_o),
    .tx_if_o       (tx_if_o),
    .tx_ch_o       (tx_ch_o),
    .pub_da_gate_o     (pub_da_gate_o),
    .pub_licence_o     (pub_licence_o),
    .pub_idle_slope_bps_o (pub_idle_slope_bps_o),
    .pub_dom_vid_o     (pub_dom_vid_o),
    .pub_dom_prio_o    (pub_dom_prio_o),
    .pub_dom_adopted_o (pub_dom_adopted_o),
    .pub_talker_decl_o (pub_talker_decl_o),
    .pub_bound_o       (pub_bound_o),
    .pub_sid_valid_o   (pub_sid_valid_o),
    .pub_started_o     (pub_started_o),
    .pub_sid_o         (pub_sid_o),
    .fw_send_o                (fw_send_o),
    .fw_ack_p_i               (fw_ack_p_i),
    .fw_ctrl_ready_o          (fw_ctrl_ready_o),
    .fw_entity_cur_config_o   (fw_entity_cur_config_o),
    .fw_entity_identify_o     (fw_entity_identify_o),
    .fw_clock_source_index_o  (fw_clock_source_index_o),
    .fw_aecp_lock_held_o      (fw_aecp_lock_held_o),
    .fw_aecp_dyn_dirty_o      (fw_aecp_dyn_dirty_o),
    .fw_restore_busy_o        (fw_restore_busy_o),
    .fw_restore_done_o        (fw_restore_done_o),
    .fw_restore_fail_o        (fw_restore_fail_o),
    .fw_restore_blank_o       (fw_restore_blank_o),
    .fw_restore_closed_o      (fw_restore_closed_o),
    .fw_restore_rb_o          (fw_restore_rb_o),
    .fw_restore_rs_cause_o    (fw_restore_rs_cause_o),
    .fw_restore_cause_o       (fw_restore_cause_o),
    .fw_nvm_backed_o          (fw_nvm_backed_o),
    .fw_nvm_alarm_o           (fw_nvm_alarm_o),
    .fw_nvm_dirty_o           (fw_nvm_dirty_o),
    .fw_nvm_stale_o           (fw_nvm_stale_o),
    .fw_nvm_pend_o            (fw_nvm_pend_o),
    .fw_nvm_img_valid_o       (fw_nvm_img_valid_o),
    .fw_nvm_verdict_o         (fw_nvm_verdict_o),
    .fw_pt_offset_ns_o        (fw_pt_offset_ns_o),
    .fw_pt_offset_v_o         (fw_pt_offset_v_o),
    .fw_fmt_out_o             (fw_fmt_out_o),
    .fw_fmt_out_v_o           (fw_fmt_out_v_o),
    .fw_fmt_in_o              (fw_fmt_in_o),
    .fw_fmt_in_v_o            (fw_fmt_in_v_o),
    .ctr_req_o                (ctr_req_o),
    .ctr_tag_o                (ctr_tag_o),
    .ctr_type_o               (ctr_type_o),
    .ctr_index_o              (ctr_index_o),
    .ctr_word_o               (ctr_word_o),
    .ctr_ans_p_i              (ctr_ans_p_i),
    .ctr_ans_tag_i            (ctr_ans_tag_i),
    .ctr_ans_data_i           (ctr_ans_data_i),
    .amap_req_o               (amap_req_o),
    .amap_tag_o               (amap_tag_o),
    .amap_type_o              (amap_type_o),
    .amap_index_o             (amap_index_o),
    .amap_map_index_o         (amap_map_index_o),
    .amap_sel_o               (amap_sel_o),
    .amap_rec_o               (amap_rec_o),
    .amap_ans_p_i             (amap_ans_p_i),
    .amap_ans_tag_i           (amap_ans_tag_i),
    .amap_ans_data_i          (amap_ans_data_i),
    .edit_req_o               (edit_req_o),
    .edit_tag_o               (edit_tag_o),
    .edit_type_o              (edit_type_o),
    .edit_index_o             (edit_index_o),
    .edit_phase_o             (edit_phase_o),
    .edit_remove_o            (edit_remove_o),
    .edit_rec_o               (edit_rec_o),
    .edit_count_o             (edit_count_o),
    .edit_record_o            (edit_record_o),
    .edit_value_o             (edit_value_o),
    .edit_ans_p_i             (edit_ans_p_i),
    .edit_ans_tag_i           (edit_ans_tag_i),
    .edit_ans_data_i          (edit_ans_data_i),
    .gsi_req_o                (gsi_req_o),
    .gsi_tag_o                (gsi_tag_o),
    .gsi_type_o               (gsi_type_o),
    .gsi_index_o              (gsi_index_o),
    .gsi_kind_o               (gsi_kind_o),
    .gsi_sel_o                (gsi_sel_o),
    .gsi_ord_o                (gsi_ord_o),
    .gsi_prop_o               (gsi_prop_o),
    .gsi_ans_p_i              (gsi_ans_p_i),
    .gsi_ans_tag_i            (gsi_ans_tag_i),
    .gsi_ans_data_i           (gsi_ans_data_i),
    .ctr_chg_p_i              (ctr_chg_p_i),
    .ctr_chg_type_i           (ctr_chg_type_i),
    .ctr_chg_index_i          (ctr_chg_index_i),
    .avb_chg_p_i              (avb_chg_p_i),
    .asp_chg_p_i              (asp_chg_p_i),
    .amap_wr_p_i              (amap_wr_p_i)
  );

endmodule : tb_mbx_top

`default_nettype wire
