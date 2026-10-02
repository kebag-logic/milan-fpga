// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : clkv_double.sv
  Description : A TEST DOUBLE of KL_ptp_clock_validity for the #629 root leg
                (tb/verilator/milan_dp_mclk), compiled IN PLACE of
                hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv and in
                no other suite.

                WHY. The CLOCK_DOMAIN LOCKED/UNLOCKED counters count edges of
                one level, ~tu & (~follow | servo LOCKED) since #629's D5 =
                C1. The ownerless elaboration this leg runs (the gPTP plane
                pruned, as obj_aclk) holds tu at 1 structurally, so neither
                counter can move there, and the plane-on elaboration needs a
                grandmaster exchange this leg does not model. The double
                gives the harness the one input of the verdict it needs: tu
                is a register the harness writes through a public tap. The
                real module's rules (sync, holdover, the Table 5.4 interval
                count) are graded by its own suite and by milan_dp_gptp.

                Same parameters and ports as the real module. as_capable_o,
                stat_o and tu_ivals_o follow the tap so the CSR words stay
                coherent; none of them is graded here.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_ptp_clock_validity #(
  parameter int unsigned QTICK_CYC_P  = 25_000_000,
  parameter int unsigned HOLD_QTICK_P = 2,
  parameter bit FABRIC_GPTP_P = 1'b0
) (
  input  wire        clk_i,
  input  wire        rst_n,
  input  wire        fabric_sync_ok_i,
  input  wire        fabric_as_cap_i,
  input  wire        fabric_disc_p_i,
  input  wire        phc_load_p_i,
  input  wire        phc_adj_p_i,
  input  wire [63:0] gm_id_i,
  output wire        ts_uncertain_o,
  output wire        as_capable_o,
  output wire [31:0] stat_o,
  output wire [31:0] tu_ivals_o
);

  //! the harness's tu: 1 (uncertain) from reset, as the real module's
  //! reset state, until the harness declares the clock valid
  logic tu_tap_r /* verilator public_flat_rw */;

  always_ff @(posedge clk_i) begin : p_tap
    if (!rst_n) tu_tap_r <= 1'b1;
  end : p_tap

  assign ts_uncertain_o = tu_tap_r;
  assign as_capable_o   = ~tu_tap_r;
  assign stat_o         = {31'd0, tu_tap_r};
  assign tu_ivals_o     = 32'd0;

endmodule

`default_nettype wire
