// SPDX-License-Identifier: CERN-OHL-W-2.0
// R276-5 reviewer probe wrapper: KL_media_clock_restart, three talkers,
// the clause-floor hold, every port exposed to the C++ reference.
`default_nettype none
module mcr_prop_top (
  input  wire        clk_i,
  input  wire        rst_n,
  input  wire        restart_p_i,
  input  wire [15:0] clk_src_i,
  input  wire [2:0]  streaming_i,
  input  wire        frame_p_i,
  input  wire [3:0]  frame_idx_i,
  input  wire        frame_mr_i,
  output wire [2:0]  mr_o
);
  KL_media_clock_restart #(.N_TALKERS_P(3), .HOLD_PDU_P(8)) u_mcr (
    .clk_i, .rst_n, .restart_p_i, .clk_src_i, .streaming_i,
    .frame_p_i, .frame_idx_i, .frame_mr_i, .mr_o);
endmodule
`default_nettype wire
