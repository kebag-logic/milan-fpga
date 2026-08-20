/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : gptp_shadow_wrap.sv
//  Project     : Milan AVB end-station -- gPTP fabric-slice bench
//
//  Description : Testbench wrap of the WHOLE fabric slice the splice will
//                instantiate: KL_gptp_shadow (tap + engine + lane), the
//                real timestamp_counter it steers, and KL_gptp_txstamp
//                observing the TX lane as the stand-in MAC boundary (in
//                fabric the stamper sits after the merges; the pairing
//                contract is identical). NO timestamp enters from the
//                harness: ingress stamps come from the tap's commit-FIFO
//                transport, egress stamps from the boundary observer --
//                the loop closes entirely in fabric.
//---------------------------------------------------------------------------//
`default_nettype none

module gptp_shadow_wrap #(
    parameter string       UCODE_HEX_P = "gptp_ucode.hex",
    parameter int unsigned CLK_HZ_P    = 2_000_000
) (
    input  wire clk_i,
    input  wire rst_n,

    //! the MAC RX tap face (wide)
    input  wire [63:0] rx_tdata_i,
    input  wire [7:0]  rx_tkeep_i,
    input  wire        rx_tvalid_i,
    input  wire        rx_tready_i,
    input  wire        rx_tlast_i,

    //! the TX lane out (wide; the harness is the merge/MAC)
    output wire [63:0] tx_tdata_o,
    output wire [7:0]  tx_tkeep_o,
    output wire        tx_tvalid_o,
    output wire        tx_tlast_o,
    input  wire        tx_tready_i,

    //! the steered clock, observable
    output wire [63:0] phc_ns_o,

    //! publish bank
    output wire [63:0] pub_gm_id_o,
    output wire [63:0] pub_parent_id_o,
    output wire [31:0] pub_flags_o,
    output wire [31:0] pub_pdelay_ns_o,
    output wire [31:0] pub_offset_o,
    output wire [63:0] pub_annq_o,
    output wire        pub_commit_o,

    //! diagnostics
    output wire [15:0] dbg_tap_drop_o,
    output wire [15:0] dbg_rx_drop_o,
    output wire [63:0] dbg_rx_ts_o,
    output wire [63:0] dbg_txts_o,
    output wire        dbg_txts_v_o,
    output wire        dbg_tspush_v_o,
    output wire [63:0] dbg_tspush_o,
    output wire        dbg_tspop_v_o,
    output wire [15:0] dbg_txts_seq_o
);

  logic signed [31:0] adj_w;
  logic               step_we_w;
  logic [63:0]        step_w;
  logic               sent_w;
  logic               tsv_w;
  logic [63:0]        tsn_w;
  logic [15:0]        tsq_w;

  timestamp_counter #(
      .COUNTER_WIDTH (64),
      .INCR_WIDTH    (32),
      .FRAC_WIDTH    (24)
  ) u_phc (
      .clk                  (clk_i),
      .resetn               (rst_n),
      .enable_i             (1'b1),
      .incr_i               (32'h0800_0000),   // 8.0 ns, the 125 MHz shape
      .adj_i                (adj_w),
      .tod_wr_i             (64'd0),
      .cmd_load_i           (1'b0),
      .offset_i             ($signed(step_w)),
      .cmd_adjust_i         (step_we_w),
      .cmd_snapshot_i       (1'b0),
      .timestamp_out        (phc_ns_o),
      .tod_snapshot_o       (),
      .tod_snapshot_valid_o ()
  );

  KL_gptp_shadow #(
      .TDATA_WIDTH_P (64),
      .CLK_HZ_P      (CLK_HZ_P),
      .UCODE_HEX_P   (UCODE_HEX_P)
  ) u_shadow (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .rx_tdata_i      (rx_tdata_i),
      .rx_tkeep_i      (rx_tkeep_i),
      .rx_tvalid_i     (rx_tvalid_i),
      .rx_tready_i     (rx_tready_i),
      .rx_tlast_i      (rx_tlast_i),
      .phc_ns_i        (phc_ns_o),
      .phc_adj_o       (adj_w),
      .phc_step_we_o   (step_we_w),
      .phc_step_o      (step_w),
      .tx_tdata_o      (tx_tdata_o),
      .tx_tkeep_o      (tx_tkeep_o),
      .tx_tvalid_o     (tx_tvalid_o),
      .tx_tlast_o      (tx_tlast_o),
      .tx_tready_i     (tx_tready_i),
      .txts_valid_i    (tsv_w),
      .txts_ns_i       (tsn_w),
      .txts_seq_i      (tsq_w),
      .tx_sent_o       (sent_w),
      .pub_gm_id_o     (pub_gm_id_o),
      .pub_parent_id_o (pub_parent_id_o),
      .pub_flags_o     (pub_flags_o),
      .pub_pdelay_ns_o (pub_pdelay_ns_o),
      .pub_offset_o    (pub_offset_o),
      .pub_annq_o      (pub_annq_o),
      .pub_commit_o    (pub_commit_o),
      .dbg_tap_drop_o  (dbg_tap_drop_o),
      .dbg_rx_drop_o   (dbg_rx_drop_o),
      .dbg_ev_drop_o   (),
      .dbg_busy_o      (),
      .dbg_rx_ts_o     (dbg_rx_ts_o),
      .dbg_tspush_v_o  (dbg_tspush_v_o),
      .dbg_tspush_o    (dbg_tspush_o),
      .dbg_tspop_v_o   (dbg_tspop_v_o)
  );

  KL_gptp_txstamp #(
      .TDATA_WIDTH_P (64)
  ) u_txstamp (
      .clk_i      (clk_i),
      .rst_n      (rst_n),
      .tx_tdata_i (tx_tdata_o),
      .tx_tvalid_i(tx_tvalid_o),
      .tx_tready_i(tx_tready_i),
      .tx_tlast_i (tx_tlast_o),
      .phc_ns_i   (phc_ns_o),
      .armed_i    (sent_w),
      .ts_valid_o (tsv_w),
      .ts_ns_o    (tsn_w),
      .ts_seq_o   (tsq_w)
  );

  assign dbg_txts_o    = tsn_w;
  assign dbg_txts_v_o  = tsv_w;
  assign dbg_txts_seq_o = tsq_w;

endmodule : gptp_shadow_wrap
`default_nettype wire
