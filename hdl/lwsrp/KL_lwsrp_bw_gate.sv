/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_bw_gate.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : Reservation resolution + bandwidth provisioning
//                (docs/LWSRP_FPGA_ARCHITECTURE.md §3):
//
//                  ACTIVE := talker declared AND listener READY registered
//                            AND domain ok AND granted BW <= 75 % port rate
//
//                Class-A idleSlope from the TSpec:
//                  idleSlope[bps] = MaxIntervalFrames x (MaxFrameSize + 42)
//                                   x 8 x 8000
//                (42 = preamble+hdr+VLAN+FCS+IPG; 8000 class-A measurement
//                intervals per second). N_STREAMS = 1 today, so the sum over
//                reservations is the single slope.
//
//                Ordering (FR-SRP-03 — a withdrawn reservation can never
//                leak frames):
//                  activate:  slope_en rises FIRST, the stream gate opens
//                             HOLD_CYCLES_C later (bandwidth provisioned
//                             before frames flow);
//                  teardown:  the stream gate closes IMMEDIATELY, slope_en
//                             releases HOLD_CYCLES_C later.
//
//                The slope reaches the CBS through a hardware MUX at the
//                datapath level (slope_en_o selects granted over the 0x400
//                CSR value for the class-A queue) — no CSR write-back.
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_bw_gate #(
  parameter int unsigned HOLD_CYCLES_C = 16
)(
    input  wire        clk_i,
    input  wire        rst_n,
    input  wire        enable_i,            //! lwSRP engine enable (CSR)

    // ---- reservation inputs ---------------------------------------------
    input  wire        talker_declared_i,   //! KL_lwsrp_tx
    input  wire        listener_ready_i,    //! KL_lwsrp_registrar
    input  wire        domain_ok_i,         //! KL_lwsrp_registrar
    input  wire        is_1g_i,             //! port rate (1 = 1 Gb/s, 0 = 100 Mb/s)

    // ---- TSpec (CSR stream table row 0) -----------------------------------
    input  wire [15:0] max_frame_i,
    input  wire [15:0] interval_frames_i,

    // ---- outputs ------------------------------------------------------------
    output reg         stream_gate_o,       //! AAF transmit admission
    output reg         slope_en_o,          //! CBS slope MUX select
    output reg  [31:0] idle_slope_o,        //! granted idleSlope, bps
    output wire        res_active_o,        //! reservation ACTIVE (CSR status)
    output reg         over_limit_o         //! TSpec refused by the 75 % gate
);

  // -----------------------------------------------------------------------
  // Slope + 75 % limit (registered pipeline; inputs are quasi-static CSRs)
  // -----------------------------------------------------------------------
  //! bytes on the wire per frame incl. per-frame overhead
  reg  [16:0] frame_bytes_r;
  //! bytes per measurement interval
  reg  [32:0] iv_bytes_r;
  //! bps = iv_bytes * 8 * 8000 = iv_bytes * 64000
  reg  [48:0] slope_bps_r;

  //! 75 % of the port rate, bps
  wire [48:0] limit_w = is_1g_i ? 49'd750_000_000 : 49'd75_000_000;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      frame_bytes_r <= '0; iv_bytes_r <= '0; slope_bps_r <= '0;
      over_limit_o <= 1'b0; idle_slope_o <= '0;
    end else begin
      frame_bytes_r <= 17'(max_frame_i) + 17'(MSRP_FRAME_OVERHEAD_C);
      iv_bytes_r    <= 33'(interval_frames_i) * 33'(frame_bytes_r);
      slope_bps_r   <= 49'(iv_bytes_r) * 49'(CLASS_A_INTERVALS_PS_C * 8);
      over_limit_o  <= (slope_bps_r > limit_w);
      idle_slope_o  <= (slope_bps_r > limit_w) ? 32'd0 : 32'(slope_bps_r);
    end
  end

  // -----------------------------------------------------------------------
  // Reservation resolution + gate/slope ordering
  // -----------------------------------------------------------------------
  wire active_w = enable_i && talker_declared_i && listener_ready_i &&
                  domain_ok_i && !over_limit_o;

  assign res_active_o = active_w;

  localparam int unsigned HOLD_W_C = $clog2(HOLD_CYCLES_C + 1);
  reg [HOLD_W_C-1:0] hold_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      stream_gate_o <= 1'b0;
      slope_en_o    <= 1'b0;
      hold_r        <= '0;
    end else begin
      if (active_w) begin
        // activation: slope first, gate after the hold
        slope_en_o <= 1'b1;
        if (!slope_en_o) begin
          hold_r <= HOLD_W_C'(HOLD_CYCLES_C);
        end else if (hold_r != '0) begin
          hold_r <= hold_r - 1'b1;
        end else begin
          stream_gate_o <= 1'b1;
        end
      end else begin
        // teardown: gate first, slope release after the hold
        stream_gate_o <= 1'b0;
        if (stream_gate_o) begin
          hold_r <= HOLD_W_C'(HOLD_CYCLES_C);
        end else if (hold_r != '0) begin
          hold_r <= hold_r - 1'b1;
        end else begin
          slope_en_o <= 1'b0;
        end
      end
    end
  end

endmodule

`default_nettype wire
