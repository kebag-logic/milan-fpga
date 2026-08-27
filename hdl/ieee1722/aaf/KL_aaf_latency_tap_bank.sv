/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aaf_latency_tap_bank.sv
  Description : Observation-point adapter for the AAF per-stage latency taps
                (roadmap item 11): it turns the datapath's AXIS observation
                points into the eight stage pulses KL_aaf_latency_taps
                measures, and packs that core's results into the sixteen
                read-only words of the LTAP CSR window (base 0x870).

                ONE RESPONSIBILITY - adapt observation points to the LTAP CSR
                window. The measurement model (single in-flight tagged
                reference frame, per-stage re-arm timeout, saturating
                last/min/max) belongs to KL_aaf_latency_taps and is not
                restated here. This module owns three things the core cannot
                see: which handshake edge marks each stage, the uniform
                one-cycle stage-pulse delay that keeps the RX filter's CAM
                cone out of the tap chain, and the CSR word order.

                PURE OBSERVER. Every port is an input except regs_o and
                status_o, which reach nothing but the CSR read multiplexer.
                The module cannot backpressure, gate or otherwise perturb any
                stream it watches - the property syn/yosys/check_tap_purity.sh
                checks, made structural by the port list rather than argued
                from the body of a 7,000-line parent.

                STAGE-PULSE PIPELINE. Every stage pulse is delayed by one
                uniform axis_clk cycle. An asl v47 route failed timing
                (WNS -0.168) on a cone running from the RX filter's CAM entry
                masks through the MAC-stream handshake into the taps' reset
                term: the frame-accept qualifier is combinational off the CAM
                compare and the arm logic extended that cone. The taps are
                pure observers, so delaying EVERY stage pulse together is
                invisible to every measurement they make - last/min/max are
                stage-to-stage DELTAS between pulses that all shift by the
                same cycle, and the epoch timestamp moves by one clock period
                on a diagnostic. The CAM cone terminates in this module's
                eight-bit register instead of inside the tap chain's resets.

                PRUNING. ENABLE_P = 0 removes the core and presents the
                post-clear state: every epoch, sample count, timeout count,
                last/min/max and the status word read 0. That is a STRUCTURAL
                zero and NOT a latency measurement - a reader who cannot tell
                the two apart would report 0 ns end to end, so the builder
                gate refuses to prune the taps in a configuration that keeps
                its probes (board.constraints.strip_probes: false).

  House style : mirrors hdl/ieee1722/aaf/KL_aaf_latency_taps.sv.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_aaf_latency_tap_bank #(
  //! 0 prunes the measurement core and ties the whole CSR window to a
  //! structural zero. See the PRUNING note in the banner.
  parameter int ENABLE_P  = 1,
  //! per-stage re-arm guard, in clk_i cycles; the caller derives it from the
  //! datapath clock rather than restating a cycle count here.
  parameter int TIMEOUT_C = 50000
) (
  input  wire        clk_i,               //! datapath (AXIS) clock
  input  wire        rst_n,               //! synchronous active-low reset

  input  wire        en_i,                //! LTAP_CTRL.en
  input  wire        clr_i,               //! LTAP_CTRL.clr strobe
  input  wire [31:0] now_i,               //! gPTP nanoseconds, low word

  //! TX stage 0 - a captured ring/I2S sample pair enters the talker
  input  wire        cap_pair_p_i,
  //! TX stages 1-2 - AAF packetizer output stream
  input  wire        aaf_tx_tvalid_i,
  input  wire        aaf_tx_tready_i,
  input  wire        aaf_tx_tlast_i,
  //! TX stage 3 - frame egress at the MAC boundary
  input  wire        mac_tx_tvalid_i,
  input  wire        mac_tx_tready_i,
  input  wire        mac_tx_tlast_i,

  //! RX stage 0 - frame ingress from the MAC
  input  wire        mac_rx_tvalid_i,
  input  wire        mac_rx_tready_i,
  input  wire        mac_rx_tlast_i,
  //! RX stage 1 - AVTP monitor parse-complete/accept
  input  wire        avtp_accept_p_i,
  //! RX stage 2 - depacketizer payload stream
  input  wire        dpkt_tvalid_i,
  input  wire        dpkt_tready_i,
  input  wire        dpkt_tlast_i,
  //! RX stage 3 - payload accepted at the PCM ring writer
  input  wire        ring_tvalid_i,
  input  wire        ring_tready_i,
  input  wire        ring_tlast_i,

  //! the sixteen read-only LTAP words, in CSR order (0x874..0x8B0)
  output wire [16*32-1:0] regs_o,
  //! LTAP_STATUS (0x870 + 0x04 group base word)
  output wire [31:0]      status_o
);

  // ==========================================================================
  //  Observation points -> stage edges
  // ==========================================================================
  wire aaf_tx_acc_w = aaf_tx_tvalid_i & aaf_tx_tready_i;
  wire mac_tx_acc_w = mac_tx_tvalid_i & mac_tx_tready_i;
  wire mac_rx_acc_w = mac_rx_tvalid_i & mac_rx_tready_i;
  wire dpkt_acc_w   = dpkt_tvalid_i   & dpkt_tready_i;
  wire ring_acc_w   = ring_tvalid_i   & ring_tready_i;

  //! start-of-frame trackers for the two shared AXIS boundaries
  logic aaf_tx_inframe_r, mac_rx_inframe_r;
  always_ff @(posedge clk_i) begin : ltap_inframe
    if (!rst_n) begin
      aaf_tx_inframe_r <= 1'b0;
      mac_rx_inframe_r <= 1'b0;
    end
    else begin
      if (aaf_tx_acc_w) aaf_tx_inframe_r <= ~aaf_tx_tlast_i;
      if (mac_rx_acc_w) mac_rx_inframe_r <= ~mac_rx_tlast_i;
    end
  end : ltap_inframe

  //! single-cycle stage edges (stage 0 = the chain's arm/epoch trigger)
  wire ltap_txcap_w  = cap_pair_p_i;                             //! ring/I2S pair in
  wire ltap_txsof_w  = aaf_tx_acc_w & ~aaf_tx_inframe_r;         //! packetizer first beat
  wire ltap_txeof_w  = aaf_tx_acc_w &  aaf_tx_tlast_i;           //! packetizer last beat
  wire ltap_txmac_w  = mac_tx_acc_w &  mac_tx_tlast_i;           //! frame egress at MAC
  wire ltap_rxsof_w  = mac_rx_acc_w & ~mac_rx_inframe_r;         //! frame ingress from MAC
  wire ltap_rxacc_w  = avtp_accept_p_i;                          //! AVTP monitor accept/parse
  wire ltap_rxdpk_w  = dpkt_acc_w & dpkt_tlast_i;                //! depacketizer payload last
  wire ltap_rxring_w = ring_acc_w & ring_tlast_i;                //! payload into the PCM ring

  wire [31:0]     ltap_tx_epoch_w, ltap_rx_epoch_w;
  wire [15:0]     ltap_tx_smp_w, ltap_rx_smp_w, ltap_tx_to_w, ltap_rx_to_w;
  wire [3*16-1:0] ltap_tx_last_w, ltap_tx_min_w, ltap_tx_max_w;
  wire [3*16-1:0] ltap_rx_last_w, ltap_rx_min_w, ltap_rx_max_w;

  generate if (ENABLE_P != 0) begin : g_ltap
  //! See the STAGE-PULSE PIPELINE note in the banner: one uniform cycle of
  //! delay on every stage pulse terminates the CAM cone here.
  logic [3:0] ltap_txp_q_r, ltap_rxp_q_r;
  always_ff @(posedge clk_i) begin : ltap_stage_pipe
    if (!rst_n) begin
      ltap_txp_q_r <= 4'd0;
      ltap_rxp_q_r <= 4'd0;
    end else begin
      ltap_txp_q_r <= {ltap_txmac_w, ltap_txeof_w, ltap_txsof_w, ltap_txcap_w};
      ltap_rxp_q_r <= {ltap_rxring_w, ltap_rxdpk_w, ltap_rxacc_w, ltap_rxsof_w};
    end
  end
  KL_aaf_latency_taps #(
    .N_STAGES_P (4), .CW_P (32), .DW_P (16),
    .TIMEOUT_C  (TIMEOUT_C)
  ) aaf_latency_taps (
    .clk_i (clk_i), .rst_n (rst_n),
    .en_i  (en_i), .clr_i (clr_i),
    .now_i (now_i),
    .tx_stage_p_i (ltap_txp_q_r),
    .rx_stage_p_i (ltap_rxp_q_r),
    .tx_epoch_o (ltap_tx_epoch_w), .rx_epoch_o (ltap_rx_epoch_w),
    .tx_samples_o (ltap_tx_smp_w), .rx_samples_o (ltap_rx_smp_w),
    .tx_timeouts_o (ltap_tx_to_w), .rx_timeouts_o (ltap_rx_to_w),
    .tx_last_o (ltap_tx_last_w), .tx_min_o (ltap_tx_min_w), .tx_max_o (ltap_tx_max_w),
    .rx_last_o (ltap_rx_last_w), .rx_min_o (ltap_rx_min_w), .rx_max_o (ltap_rx_max_w),
    .status_o (status_o)
  );
  end else begin : g_no_ltap
    assign ltap_tx_epoch_w = 32'd0;
    assign ltap_rx_epoch_w = 32'd0;
    assign ltap_tx_smp_w   = 16'd0;
    assign ltap_rx_smp_w   = 16'd0;
    assign ltap_tx_to_w    = 16'd0;
    assign ltap_rx_to_w    = 16'd0;
    assign ltap_tx_last_w  = {(3*16){1'b0}};
    assign ltap_tx_min_w   = {(3*16){1'b0}};
    assign ltap_tx_max_w   = {(3*16){1'b0}};
    assign ltap_rx_last_w  = {(3*16){1'b0}};
    assign ltap_rx_min_w   = {(3*16){1'b0}};
    assign ltap_rx_max_w   = {(3*16){1'b0}};
    assign status_o        = 32'd0;
  end endgenerate

  //! pack the 16 RO words in the exact LTAP CSR order (0x874..0x8B0). Per
  //! delta d: word{2d} = {max16, last16}, word{2d+1} = {16'd0, min16}.
  assign regs_o[32*0  +: 32] = ltap_tx_epoch_w;
  assign regs_o[32*1  +: 32] = {ltap_tx_to_w, ltap_tx_smp_w};
  assign regs_o[32*2  +: 32] = {ltap_tx_max_w[16*0 +: 16], ltap_tx_last_w[16*0 +: 16]};
  assign regs_o[32*3  +: 32] = {16'd0,                     ltap_tx_min_w [16*0 +: 16]};
  assign regs_o[32*4  +: 32] = {ltap_tx_max_w[16*1 +: 16], ltap_tx_last_w[16*1 +: 16]};
  assign regs_o[32*5  +: 32] = {16'd0,                     ltap_tx_min_w [16*1 +: 16]};
  assign regs_o[32*6  +: 32] = {ltap_tx_max_w[16*2 +: 16], ltap_tx_last_w[16*2 +: 16]};
  assign regs_o[32*7  +: 32] = {16'd0,                     ltap_tx_min_w [16*2 +: 16]};
  assign regs_o[32*8  +: 32] = ltap_rx_epoch_w;
  assign regs_o[32*9  +: 32] = {ltap_rx_to_w, ltap_rx_smp_w};
  assign regs_o[32*10 +: 32] = {ltap_rx_max_w[16*0 +: 16], ltap_rx_last_w[16*0 +: 16]};
  assign regs_o[32*11 +: 32] = {16'd0,                     ltap_rx_min_w [16*0 +: 16]};
  assign regs_o[32*12 +: 32] = {ltap_rx_max_w[16*1 +: 16], ltap_rx_last_w[16*1 +: 16]};
  assign regs_o[32*13 +: 32] = {16'd0,                     ltap_rx_min_w [16*1 +: 16]};
  assign regs_o[32*14 +: 32] = {ltap_rx_max_w[16*2 +: 16], ltap_rx_last_w[16*2 +: 16]};
  assign regs_o[32*15 +: 32] = {16'd0,                     ltap_rx_min_w [16*2 +: 16]};

endmodule

`default_nettype wire
