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

    //! Test-only return-order control. The held tuple always comes from the
    //! real boundary stamper; the harness can delay one selected type and
    //! later replay that exact tuple to prove engine tag matching without
    //! fabricating a timestamp. A live raw return wins over release.
    input  wire        txts_hold_en_i,
    input  wire [3:0]  txts_hold_type_i,
    input  wire        txts_release_i,

    //! the steered clock, observable
    output wire [63:0] phc_ns_o,

    //! publish bank
    output wire [63:0] pub_gm_id_o,
    output wire [63:0] pub_parent_id_o,
    output wire [31:0] pub_flags_o,
    output wire [31:0] pub_pdelay_ns_o,
    output wire [31:0] pub_offset_o,

    //! diagnostics
    output wire [15:0] dbg_tap_drop_o,
    output wire [15:0] dbg_rx_drop_o,
    output wire [63:0] dbg_rx_ts_o,
    output wire [63:0] dbg_txts_o,
    output wire        dbg_txts_v_o,
    output wire        dbg_tspush_v_o,
    output wire [63:0] dbg_tspush_o,
    output wire        dbg_tspop_v_o,
    output wire [15:0] dbg_txts_seq_o,
    //! how many times the engine's uCPU has STARTED a program. The engine
    //! brings `dbg_busy_o` out of the slice already; this wrapper counts
    //! its rising edges so a bench can ask "did anything dispatch?" of a
    //! window rather than of an instant. A frame the parser refuses must
    //! never move this: the refusal and the dispatch are exclusive, which
    //! is the invariant the tsn_fuzz unlisted-messageType probe rests on
    output wire [15:0] dbg_prog_run_o,
    //! the stamper's messageType tag, beside the sequence tag: a returning
    //! stamp must name the frame it belongs to by BOTH (milan-fpga #214)
    output wire [3:0]  dbg_txts_type_o,
    //! the same tag where the engine boundary sees it: the slice PORT,
    //! combinational, so it must equal the stamper's in the very cycle
    //! txts_valid_i is high. A register here would lag by a leg
    output wire [3:0]  dbg_slice_type_o,
    //! Test-gate diagnostics: expose both the atomically held real tuple and
    //! the exact tuple delivered at the engine face. These are observations,
    //! not alternate timestamp sources.
    output wire        dbg_txts_held_o,
    output wire [63:0] dbg_txts_held_ns_o,
    output wire [15:0] dbg_txts_held_seq_o,
    output wire [3:0]  dbg_txts_held_type_o,
    output wire        dbg_eng_txts_v_o,
    output wire [63:0] dbg_eng_txts_ns_o,
    output wire [15:0] dbg_eng_txts_seq_o,
    output wire [3:0]  dbg_eng_txts_type_o,
    output wire [15:0] dbg_txts_gate_conflict_o,
    output wire [15:0] dbg_ev_drop_o
);

  logic               busy_w;
  logic [3:0]         tst_w;
  logic signed [31:0] adj_w;
  logic               step_we_w;
  logic [63:0]        step_w;
  logic               sent_w;
  logic               tsv_w;
  logic [63:0]        tsn_w;
  logic [15:0]        tsq_w;
  logic               eng_tsv_w;
  logic [63:0]        eng_tsn_w;
  logic [15:0]        eng_tsq_w;
  logic [3:0]         eng_tst_w;
  logic               held_v_r;
  logic [63:0]        held_n_r;
  logic [15:0]        held_q_r;
  logic [3:0]         held_t_r;
  logic               hold_hit_w;
  logic               raw_pass_w;
  logic               release_w;
  logic               gate_conflict_w;
  logic [15:0]        gate_conflict_r;

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
      .txts_valid_i    (eng_tsv_w),
      .txts_ns_i       (eng_tsn_w),
      .txts_seq_i      (eng_tsq_w),
      .txts_type_i     (eng_tst_w),
      .tx_sent_o       (sent_w),
      .pub_gm_id_o     (pub_gm_id_o),
      .pub_parent_id_o (pub_parent_id_o),
      .pub_flags_o     (pub_flags_o),
      .pub_pdelay_ns_o (pub_pdelay_ns_o),
      .pub_offset_o    (pub_offset_o),
      .pub_annq_o      (),
      .pub_commit_o    (),
      .dbg_tap_drop_o  (dbg_tap_drop_o),
      .dbg_rx_drop_o   (dbg_rx_drop_o),
      .dbg_ev_drop_o   (dbg_ev_drop_o),
      .dbg_busy_o      (busy_w),
      .dbg_rx_ts_o     (dbg_rx_ts_o),
      .dbg_tspush_v_o  (dbg_tspush_v_o),
      .dbg_tspush_o    (dbg_tspush_o),
      .dbg_tspop_v_o   (dbg_tspop_v_o),
      .dbg_txts_type_o (dbg_slice_type_o)
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
      .ts_seq_o   (tsq_w),
      .ts_type_o  (tst_w)
  );

  //! Return-order fault injection for the two #214 collision proofs. This is
  //! deliberately outside shipping RTL. It captures a complete tuple emitted
  //! by KL_gptp_txstamp and can delay only the first matching return. While a
  //! tuple is held, every later raw return passes normally. Release waits for
  //! an idle raw cycle, so neither path can overwrite the other (donor #31).
  assign hold_hit_w = tsv_w && txts_hold_en_i && !held_v_r &&
                      (tst_w == txts_hold_type_i);
  assign raw_pass_w = tsv_w && !hold_hit_w;
  assign release_w  = held_v_r && txts_release_i && !tsv_w;
  //! A second selected capture while the slot is full, or a release request
  //! coincident with a raw return, would make the intended delivery order
  //! ambiguous. Count either condition so every collision phase can prove
  //! that its test-only reordering was lossless and serialized.
  assign gate_conflict_w =
      (tsv_w && txts_hold_en_i && held_v_r &&
       (tst_w == txts_hold_type_i)) ||
      (txts_release_i && held_v_r && tsv_w);
  assign eng_tsv_w  = raw_pass_w || release_w;
  assign eng_tsn_w  = raw_pass_w ? tsn_w : held_n_r;
  assign eng_tsq_w  = raw_pass_w ? tsq_w : held_q_r;
  //! Show the raw tag during its capture cycle as well; the engine-valid pulse
  //! is suppressed then, and the held value is selected on replay.
  assign eng_tst_w  = (raw_pass_w || hold_hit_w) ? tst_w : held_t_r;

  always_ff @(posedge clk_i) begin : hold_one_real_stamp
    if (!rst_n) begin
      held_v_r <= 1'b0;
      held_n_r <= '0;
      held_q_r <= '0;
      held_t_r <= '0;
      gate_conflict_r <= '0;
    end else begin
      if (gate_conflict_w) gate_conflict_r <= gate_conflict_r + 16'd1;
      if (hold_hit_w) begin
        held_v_r <= 1'b1;
        held_n_r <= tsn_w;
        held_q_r <= tsq_w;
        held_t_r <= tst_w;
      end else if (release_w) begin
        held_v_r <= 1'b0;
      end
    end
  end : hold_one_real_stamp

  assign dbg_txts_o    = tsn_w;
  assign dbg_txts_v_o  = tsv_w;
  assign dbg_txts_seq_o = tsq_w;
  assign dbg_txts_type_o = tst_w;
  assign dbg_txts_held_o = held_v_r;
  assign dbg_txts_held_ns_o = held_n_r;
  assign dbg_txts_held_seq_o = held_q_r;
  assign dbg_txts_held_type_o = held_t_r;
  assign dbg_eng_txts_v_o = eng_tsv_w;
  assign dbg_eng_txts_ns_o = eng_tsn_w;
  assign dbg_eng_txts_seq_o = eng_tsq_w;
  assign dbg_eng_txts_type_o = eng_tst_w;
  assign dbg_txts_gate_conflict_o = gate_conflict_r;

  //! program-start counter: one per rising edge of the engine's busy line
  logic        busy_r;
  logic [15:0] prog_run_r;
  always_ff @(posedge clk_i) begin : prog_run
    if (!rst_n) begin
      busy_r     <= 1'b0;
      prog_run_r <= '0;
    end else begin
      busy_r <= busy_w;
      if (busy_w && !busy_r) prog_run_r <= prog_run_r + 16'd1;
    end
  end
  assign dbg_prog_run_o = prog_run_r;

endmodule : gptp_shadow_wrap
`default_nettype wire
