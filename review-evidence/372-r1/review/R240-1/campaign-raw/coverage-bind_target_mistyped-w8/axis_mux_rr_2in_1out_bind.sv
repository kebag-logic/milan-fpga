/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : axis_mux_rr_2in_1out_bind.sv
//  Project     : Milan TSN NIC -- assertion-based verification (#372)
//
//  Description : Attaches axis_mux_rr_2in_1out_sva, as instance `u_sva`, to
//                EVERY instance of axis_mux_rr_2in_1out in the elaborated
//                design. The product RTL is not edited and carries no
//                simulation-only code; compiling this file is what adds the
//                checker, and leaving it out removes it.
//
//                Pinned Verilator 5.050 binds by MODULE name only, never by
//                instance path, and it accepts a bind whose target module
//                does not exist without any diagnostic, even under -Wall.
//                A mistyped target therefore builds a design with no checker
//                in it. The harness that compiles this file must prove the
//                checker is present (docs/testing/ASSERTIONS.md), because the
//                tool will not.
//
//                Every connection below is resolved in the scope of the bound
//                mux instance, so the ownership flags are its own `state`
//                decoded against its own enum literals, and TDATA_WIDTH_P
//                follows each instance's TDATA_WIDTH.
//---------------------------------------------------------------------------//

`default_nettype none

bind axis_mux_rr_2in_1out_mistyped axis_mux_rr_2in_1out_sva #(
  .TDATA_WIDTH_P(TDATA_WIDTH)
) u_sva (
  .clk_i       (clk),
  .rst_n       (rst_n),

  .s0_tdata_i  (s0_tdata),
  .s0_tvalid_i (s0_tvalid),
  .s0_tready_i (s0_tready),
  .s0_tlast_i  (s0_tlast),
  .s0_tkeep_i  (s0_tkeep),

  .s1_tdata_i  (s1_tdata),
  .s1_tvalid_i (s1_tvalid),
  .s1_tready_i (s1_tready),
  .s1_tlast_i  (s1_tlast),
  .s1_tkeep_i  (s1_tkeep),

  .m_tdata_i   (m_tdata),
  .m_tvalid_i  (m_tvalid),
  .m_tready_i  (m_tready),
  .m_tlast_i   (m_tlast),
  .m_tkeep_i   (m_tkeep),

  .owner_none_i(state == IDLE),
  .owner_s0_i  (state == STREAM_0),
  .owner_s1_i  (state == STREAM_1)
);

`default_nettype wire
