/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aaf_latency_taps.sv
  Description : Per-stage AAF pipeline latency taps (roadmap item 11).

                Two independent measurement chains - the AAF talker (TX) and
                the AAF listener (RX) - each latch a free-running cycle count
                at a set of documented pipeline points and expose the
                inter-stage deltas (last / min / max, saturating) plus the
                gPTP epoch of the measured reference frame over CSR.

                  TX  : CAP (ring/I2S pair in) -> PKT_SOF (packetizer first
                        beat) -> PKT_EOF (packetizer last beat) -> MAC_TX
                        (frame egresses the MAC boundary)
                  RX  : MAC_RX (frame ingress) -> ACCEPT (AVTP monitor
                        parse-complete/accept pulse) -> DEPKT (payload last
                        beat) -> PCM_RING (payload accepted at the ring
                        writer)

                MEASUREMENT MODEL - single in-flight tagged reference frame.
                Each chain follows ONE frame at a time: it ARMS on a stage-0
                valid-edge (latching the epoch cycle + gPTP time), then takes
                the NEXT valid-edge at each subsequent stage as that frame's
                progress, recording delta[k] = t(stage k) - t(stage k-1).
                When the final stage fires the sample completes (min/last/max
                updated, epoch published, samples++) and the chain re-arms;
                frames that enter while a measurement is in flight are ignored
                until it finishes. A per-stage timeout (TIMEOUT_C cycles)
                aborts and re-arms a stuck token (timeouts++), so a dropped
                frame can never wedge the chain.

                COHERENCE - the token is followed by ORDER, not by a threaded
                frame id (no invasive per-module tag). Under steady single-
                stream AAF flow the next-edge at each stage is that frame's;
                under mixed traffic a shared boundary (MAC_TX / MAC_RX) may
                catch a nearer non-AAF frame edge, so min/last/max characterise
                the latency ENVELOPE rather than one exact frame. The stage-0
                CAP edge is any captured pair, so the CAP->PKT delta spans up
                to one 6-sample accumulation window. Deltas are in axis_clk
                cycles (divide by the datapath clock for seconds). The I2S-out
                playout stage is FIFO-fill dominated (the CDC pair FIFO
                decouples PDUs from DAC frames) and stays observed via the
                existing I2SPB_STAT fill/converged rails; a DDR3 per-sample
                history ring is the documented follow-up.

  House style : mirrors hdl/common/KL_link_guard.sv.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

// ==========================================================================
//  Single-chain latency measurement engine (instantiated once per direction)
// ==========================================================================
module KL_aaf_latency_chain #(
  parameter int unsigned N_STAGES_P = 4,      //! tap points on this chain (>=2)
  parameter int unsigned CW_P       = 32,     //! free-running cycle-count width
  parameter int unsigned DW_P       = 16,     //! saturating per-stage delta width
  parameter int unsigned TIMEOUT_C  = 20000   //! per-stage re-arm guard (cycles)
) (
  input  wire                        clk_i,
  input  wire                        rst_n,       //! active-low sync reset
  input  wire                        en_i,        //! measure enable (LTAP_CTRL[1])
  input  wire                        clr_i,       //! 1-cycle stats clear (LTAP_CTRL[0])
  input  wire [CW_P-1:0]             cyc_i,        //! shared free-running cycle count
  input  wire [31:0]                 now_i,        //! gPTP ns epoch source (ptp_now[31:0])
  input  wire [N_STAGES_P-1:0]       stage_p_i,    //! per-stage valid-edge pulses

  output wire [31:0]                 epoch_o,      //! gPTP ns at last completed frame's stage 0
  output wire [15:0]                 samples_o,    //! completed reference frames (saturating)
  output wire [15:0]                 timeouts_o,   //! aborted (timed-out) tokens (saturating)
  output wire [(N_STAGES_P-1)*DW_P-1:0] last_o,    //! last inter-stage delta per stage
  output wire [(N_STAGES_P-1)*DW_P-1:0] min_o,     //! min  inter-stage delta per stage
  output wire [(N_STAGES_P-1)*DW_P-1:0] max_o,     //! max  inter-stage delta per stage
  output wire                        active_o,     //! a measurement is in flight
  output wire [2:0]                  stage_o       //! stage index currently awaited
);

  localparam int unsigned NDLT_C  = N_STAGES_P - 1;                       //! # deltas
  localparam int unsigned SIDXW_C = (N_STAGES_P <= 2) ? 1 : $clog2(N_STAGES_P);
  localparam int unsigned TOW_C   = $clog2(TIMEOUT_C + 1);

  logic                active_r;
  logic [SIDXW_C-1:0]  stg_r;          //! stage awaited (1..N-1)
  logic [CW_P-1:0]     prevc_r;        //! cycle stamp of the previous stage
  logic [31:0]         epoch_pend_r;   //! epoch latched at arm
  logic [31:0]         epoch_r;        //! published epoch
  logic [TOW_C-1:0]    to_r;           //! per-stage timeout down-counter
  logic [15:0]         samples_r, timeouts_r;
  logic [DW_P-1:0]     last_r [NDLT_C];
  logic [DW_P-1:0]     min_r  [NDLT_C];
  logic [DW_P-1:0]     max_r  [NDLT_C];

  //! current inter-stage delta (saturating into DW_P bits)
  wire [CW_P-1:0] diff_w = cyc_i - prevc_r;
  wire [DW_P-1:0] dsat_w = (|diff_w[CW_P-1:DW_P]) ? {DW_P{1'b1}}
                                                  : diff_w[DW_P-1:0];
  //! delta-array index for the awaited stage (stg_r-1 -> 0..NDLT_C-1)
  wire [SIDXW_C-1:0] didx_w = stg_r - 1'b1;

  function automatic [15:0] inc16(input [15:0] v);
    inc16 = (&v) ? v : v + 16'd1;
  endfunction

  always_ff @(posedge clk_i) begin : chain_fsm
    if (!rst_n) begin
      active_r     <= 1'b0;
      stg_r        <= SIDXW_C'(1);
      prevc_r      <= '0;
      epoch_pend_r <= '0;
      epoch_r      <= '0;
      to_r         <= '0;
      samples_r    <= '0;
      timeouts_r   <= '0;
      for (int i = 0; i < NDLT_C; i++) begin
        last_r[i] <= '0;
        min_r[i]  <= '1;
        max_r[i]  <= '0;
      end
    end
    else if (clr_i) begin
      //! stats clear wins over measurement; the in-flight token is dropped
      active_r   <= 1'b0;
      stg_r      <= SIDXW_C'(1);
      epoch_r    <= '0;
      samples_r  <= '0;
      timeouts_r <= '0;
      for (int i = 0; i < NDLT_C; i++) begin
        last_r[i] <= '0;
        min_r[i]  <= '1;
        max_r[i]  <= '0;
      end
    end
    else if (!en_i) begin
      active_r <= 1'b0;                       //! disabled: idle, stats frozen
    end
    else begin
      if (!active_r) begin
        //! ARM on a stage-0 edge: latch the epoch cycle + gPTP time
        if (stage_p_i[0]) begin
          active_r     <= 1'b1;
          stg_r        <= SIDXW_C'(1);
          prevc_r      <= cyc_i;
          epoch_pend_r <= now_i;
          to_r         <= TOW_C'(TIMEOUT_C);
        end
      end
      else if (to_r == '0) begin
        //! token timed out mid-chain: abort and re-arm
        active_r   <= 1'b0;
        timeouts_r <= inc16(timeouts_r);
      end
      else begin
        to_r <= to_r - 1'b1;
        if (stage_p_i[stg_r]) begin
          last_r[didx_w] <= dsat_w;
          if (dsat_w < min_r[didx_w]) min_r[didx_w] <= dsat_w;
          if (dsat_w > max_r[didx_w]) max_r[didx_w] <= dsat_w;
          prevc_r <= cyc_i;
          to_r    <= TOW_C'(TIMEOUT_C);       //! re-arm per-stage guard
          if (32'(stg_r) == NDLT_C) begin
            active_r  <= 1'b0;                 //! final stage: sample complete
            samples_r <= inc16(samples_r);
            epoch_r   <= epoch_pend_r;
          end
          else begin
            stg_r <= stg_r + 1'b1;
          end
        end
      end
    end
  end : chain_fsm

  genvar g;
  generate
    for (g = 0; g < NDLT_C; g++) begin : g_flat
      assign last_o[g*DW_P +: DW_P] = last_r[g];
      assign min_o [g*DW_P +: DW_P] = min_r[g];
      assign max_o [g*DW_P +: DW_P] = max_r[g];
    end
  endgenerate

  assign epoch_o    = epoch_r;
  assign samples_o  = samples_r;
  assign timeouts_o = timeouts_r;
  assign active_o   = active_r;
  assign stage_o    = active_r ? 3'(stg_r) : 3'd0;

endmodule

// ==========================================================================
//  Two-chain top: shared cycle counter + TX/RX chains + status packing
// ==========================================================================
module KL_aaf_latency_taps #(
  parameter int unsigned N_STAGES_P = 4,      //! tap points per chain
  parameter int unsigned CW_P       = 32,     //! free-running cycle-count width
  parameter int unsigned DW_P       = 16,     //! saturating per-stage delta width
  parameter int unsigned TIMEOUT_C  = 20000   //! per-stage re-arm guard (cycles)
) (
  input  wire                        clk_i,       //! datapath (axis) clock
  input  wire                        rst_n,       //! active-low sync reset
  input  wire                        en_i,        //! LTAP_CTRL[1] measure enable
  input  wire                        clr_i,       //! LTAP_CTRL[0] W1S stats clear
  input  wire [31:0]                 now_i,       //! gPTP ns (ptp_now[31:0]) epoch source

  input  wire [N_STAGES_P-1:0]       tx_stage_p_i, //! TX chain stage edges
  input  wire [N_STAGES_P-1:0]       rx_stage_p_i, //! RX chain stage edges

  output wire [31:0]                 tx_epoch_o,
  output wire [31:0]                 rx_epoch_o,
  output wire [15:0]                 tx_samples_o,
  output wire [15:0]                 rx_samples_o,
  output wire [15:0]                 tx_timeouts_o,
  output wire [15:0]                 rx_timeouts_o,
  output wire [(N_STAGES_P-1)*DW_P-1:0] tx_last_o, tx_min_o, tx_max_o,
  output wire [(N_STAGES_P-1)*DW_P-1:0] rx_last_o, rx_min_o, rx_max_o,
  output wire [31:0]                 status_o     //! {rx_stage,rx_active,tx_stage,tx_active} for LTAP_CTRL RO
);

  //! shared free-running cycle counter (the delta time base for both chains)
  logic [CW_P-1:0] cyc_r;
  always_ff @(posedge clk_i) begin : cyc_ctr
    if (!rst_n) cyc_r <= '0;
    else        cyc_r <= cyc_r + 1'b1;
  end : cyc_ctr

  wire        tx_active_w, rx_active_w;
  wire [2:0]  tx_stage_w,  rx_stage_w;

  KL_aaf_latency_chain #(
    .N_STAGES_P(N_STAGES_P), .CW_P(CW_P), .DW_P(DW_P), .TIMEOUT_C(TIMEOUT_C)
  ) tx_chain (
    .clk_i (clk_i), .rst_n (rst_n), .en_i (en_i), .clr_i (clr_i),
    .cyc_i (cyc_r), .now_i (now_i), .stage_p_i (tx_stage_p_i),
    .epoch_o (tx_epoch_o), .samples_o (tx_samples_o), .timeouts_o (tx_timeouts_o),
    .last_o (tx_last_o), .min_o (tx_min_o), .max_o (tx_max_o),
    .active_o (tx_active_w), .stage_o (tx_stage_w)
  );

  KL_aaf_latency_chain #(
    .N_STAGES_P(N_STAGES_P), .CW_P(CW_P), .DW_P(DW_P), .TIMEOUT_C(TIMEOUT_C)
  ) rx_chain (
    .clk_i (clk_i), .rst_n (rst_n), .en_i (en_i), .clr_i (clr_i),
    .cyc_i (cyc_r), .now_i (now_i), .stage_p_i (rx_stage_p_i),
    .epoch_o (rx_epoch_o), .samples_o (rx_samples_o), .timeouts_o (rx_timeouts_o),
    .last_o (rx_last_o), .min_o (rx_min_o), .max_o (rx_max_o),
    .active_o (rx_active_w), .stage_o (rx_stage_w)
  );

  //! LTAP_CTRL readback status: enable bit is OR-ed in by milan_csr at bit[1]
  assign status_o = {16'd0, rx_stage_w, rx_active_w,
                     tx_stage_w, tx_active_w, 8'd0};

endmodule

`default_nettype wire
