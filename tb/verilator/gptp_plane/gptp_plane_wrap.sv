/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : gptp_plane_wrap.sv
//  Project     : Milan AVB end-station -- gPTP plane integration bench
//
//  Description : Testbench wrap marrying the gptp-processor submodule's
//                KL_gptp_engine to the PARENT's real timestamp_counter --
//                the exact pairing the datapath splice will instantiate.
//                The engine's PHC face maps onto the counter's knobs:
//
//                  phc_addend_*  ->  adj_i        (adjfine, Q8.24 ns/tick,
//                                                  latched here: the engine
//                                                  pulses, the counter wants
//                                                  a level)
//                  phc_step_*    ->  offset_i + cmd_adjust_i  (adjtime)
//                  timestamp_out ->  phc_ns_i     (the clock it steers)
//
//                The addend latch is the one piece of fabric the splice
//                adds beyond wires; it lives here until then. The counter
//                runs its 125 MHz shape (8.0 ns Q8.24 increment) while the
//                bench clock is CLK_HZ_P -- the engine's µcode gain is
//                generated for the bench's ticks-per-interval, so the
//                closed loop is exact in counter time.
//---------------------------------------------------------------------------//
`default_nettype none

module gptp_plane_wrap #(
    parameter string       UCODE_HEX_P = "gptp_ucode.hex",
    parameter int unsigned CLK_HZ_P    = 2_000_000
) (
    input  wire         clk_i,
    input  wire         rst_n,

    //! RX byte face: pre-classified 0x88F7 frames, DA first
    input  wire         rx_valid_i,
    input  wire  [7:0]  rx_data_i,
    input  wire         rx_sof_i,
    input  wire         rx_eof_i,
    input  wire         rx_err_i,
    input  wire  [63:0] rx_ts_i,

    //! TX byte face
    output logic        tx_valid_o,
    output logic [7:0]  tx_data_o,
    output logic        tx_sof_o,
    output logic        tx_eof_o,
    input  wire         tx_ready_i,

    //! egress timestamp return
    input  wire         txts_valid_i,
    input  wire  [63:0] txts_ns_i,
    input  wire  [15:0] txts_seq_i,

    //! the steered clock, observable
    output wire  [63:0] phc_ns_o,

    //! steering taps for the bench (observer only)
    output logic        tap_adj_we_o,
    output logic [31:0] tap_adj_o,
    output logic        tap_step_we_o,
    output logic [63:0] tap_step_o,

    //! publish bank -- the retired software contract
    output logic [63:0] pub_gm_id_o,
    output logic [63:0] pub_parent_id_o,
    output logic [31:0] pub_flags_o,
    output logic [31:0] pub_pdelay_ns_o,
    output logic [31:0] pub_offset_o,
    output logic [63:0] pub_annq_o,
    output logic        pub_commit_o
);

  logic        adj_we_w;
  logic [31:0] adj_val_w;
  logic        step_we_w;
  logic [63:0] step_val_w;

  //! adjfine is a level at the counter: latch the engine's pulse
  //! (sync reset, matching the counter it feeds)
  logic signed [31:0] adj_r;
  always_ff @(posedge clk_i) begin : adj_latch
    if (!rst_n)        adj_r <= '0;
    else if (adj_we_w) adj_r <= $signed(adj_val_w);
  end

  timestamp_counter #(
      .COUNTER_WIDTH (64),
      .INCR_WIDTH    (32),
      .FRAC_WIDTH    (24)
  ) u_phc (
      .clk                  (clk_i),
      .resetn               (rst_n),
      .enable_i             (1'b1),
      .incr_i               (32'h0800_0000),   // 8.0 ns, the 125 MHz shape
      .adj_i                (adj_r),
      .tod_wr_i             (64'd0),
      .cmd_load_i           (1'b0),
      .offset_i             ($signed(step_val_w)),
      .cmd_adjust_i         (step_we_w),
      .cmd_snapshot_i       (1'b0),
      .timestamp_out        (phc_ns_o),
      .tod_snapshot_o       (),
      .tod_snapshot_valid_o ()
  );

  KL_gptp_engine #(
      .UCODE_HEX_P (UCODE_HEX_P),
      .CLK_HZ_P    (CLK_HZ_P)
  ) u_engine (
      .clk_i              (clk_i),
      .rst_n              (rst_n),
      .rx_valid_i         (rx_valid_i),
      .rx_data_i          (rx_data_i),
      .rx_sof_i           (rx_sof_i),
      .rx_eof_i           (rx_eof_i),
      .rx_err_i           (rx_err_i),
      .rx_ts_i            (rx_ts_i),
      .tx_valid_o         (tx_valid_o),
      .tx_data_o          (tx_data_o),
      .tx_sof_o           (tx_sof_o),
      .tx_eof_o           (tx_eof_o),
      .tx_ready_i         (tx_ready_i),
      .txts_valid_i       (txts_valid_i),
      .txts_ns_i          (txts_ns_i),
      .txts_seq_i         (txts_seq_i),
      .phc_ns_i           (phc_ns_o),
      .phc_addend_we_o    (adj_we_w),
      .phc_addend_o       (adj_val_w),
      .phc_step_we_o      (step_we_w),
      .phc_step_o         (step_val_w),
      .pub_gm_id_o        (pub_gm_id_o),
      .pub_parent_id_o    (pub_parent_id_o),
      .pub_flags_o        (pub_flags_o),
      .pub_pdelay_ns_o    (pub_pdelay_ns_o),
      .pub_offset_o       (pub_offset_o),
      .pub_annq_o         (pub_annq_o),
      .pub_commit_o       (pub_commit_o),
      .eff_nvm_stb_o      (),
      .eff_nvm_mark_o     (),
      .eff_notify_stb_o   (),
      .eff_notify_class_o (),
      .dbg_rx_drop_o      (),
      .dbg_ev_drop_o      (),
      .dbg_busy_o         (),
      .dbg_status_o       ()
  );

  assign tap_adj_we_o  = adj_we_w;
  assign tap_adj_o     = adj_val_w;
  assign tap_step_we_o = step_we_w;
  assign tap_step_o    = step_val_w;

endmodule : gptp_plane_wrap
`default_nettype wire
