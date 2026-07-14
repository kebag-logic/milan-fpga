/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_timers.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : Centralised MRP timer strobes for the lwSRP engine
//                (docs/LWSRP_FPGA_ARCHITECTURE.md §3) — the KL_aecp_timers
//                recipe: a CLK_FREQ_HZ_P-derived 1 kHz base tick, then the
//                three MRP periods as one-cycle pulses.
//
//                  tick_1khz_o     1 ms   — the registrar leave downcounters
//                  join_tick_o     200 ms — applicant refresh (JoinTime)
//                  leaveall_tick_o 10 s   — our LeaveAll turn (LeaveAllTime)
//
//                CLK_FREQ_HZ_P MUST be passed by the instantiating layer:
//                the ADP tick ran at the 100 MHz default on the 50 MHz Arty
//                datapath for a week (2 s ticks, c3b0e82) because the LiteX
//                Instance() never forwarded the parameter.
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_timers #(
  //! Datapath clock (AX7101 100 MHz, Arty 50 MHz)
  parameter int unsigned CLK_FREQ_HZ_P = 100_000_000
) (
  input  wire  clk_i,
  input  wire  rst_n,
  output logic tick_1khz_o,      //! 1 ms strobe (registrar leave timers)
  output logic join_tick_o,      //! JoinTime strobe (applicant TX refresh)
  output logic leaveall_tick_o   //! LeaveAllTime strobe (our LeaveAll turn)
);

  // ------------------------------------------------------------------ //
  // 1 kHz base generator                                                //
  // ------------------------------------------------------------------ //
  localparam int unsigned TICK_DIV_C   = CLK_FREQ_HZ_P / 1_000;
  localparam int unsigned TICK_CNT_W_C = $clog2(TICK_DIV_C);

  logic [TICK_CNT_W_C-1:0] ms_ctr_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      ms_ctr_r    <= '0;
      tick_1khz_o <= 1'b0;
    end else begin
      tick_1khz_o <= 1'b0;
      if (ms_ctr_r == TICK_CNT_W_C'(TICK_DIV_C - 1)) begin
        ms_ctr_r    <= '0;
        tick_1khz_o <= 1'b1;
      end else begin
        ms_ctr_r <= ms_ctr_r + 1'b1;
      end
    end
  end

  // ------------------------------------------------------------------ //
  // JoinTime (200 ms) + LeaveAllTime (10 s) dividers off the 1 kHz tick //
  // ------------------------------------------------------------------ //
  logic [$clog2(JOIN_TIME_MS_C)-1:0]     join_ctr_r;
  logic [$clog2(LEAVEALL_TIME_MS_C)-1:0] la_ctr_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      join_ctr_r      <= '0;
      la_ctr_r        <= '0;
      join_tick_o     <= 1'b0;
      leaveall_tick_o <= 1'b0;
    end else begin
      join_tick_o     <= 1'b0;
      leaveall_tick_o <= 1'b0;
      if (tick_1khz_o) begin
        if (join_ctr_r == ($clog2(JOIN_TIME_MS_C))'(JOIN_TIME_MS_C - 1)) begin
          join_ctr_r  <= '0;
          join_tick_o <= 1'b1;
        end else begin
          join_ctr_r <= join_ctr_r + 1'b1;
        end
        if (la_ctr_r == ($clog2(LEAVEALL_TIME_MS_C))'(LEAVEALL_TIME_MS_C - 1)) begin
          la_ctr_r        <= '0;
          leaveall_tick_o <= 1'b1;
        end else begin
          la_ctr_r <= la_ctr_r + 1'b1;
        end
      end
    end
  end

endmodule

`default_nettype wire
