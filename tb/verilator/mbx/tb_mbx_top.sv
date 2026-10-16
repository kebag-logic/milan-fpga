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
  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C*64-1:0]         pub_sid_o          //! SID_HI:SID_LO per sink
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
    .pub_sid_o         (pub_sid_o)
  );

endmodule : tb_mbx_top

`default_nettype wire
