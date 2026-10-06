// scratch: milan_datapath's #386 settle block as shipped, standalone for OOC area
module settle_base #(parameter int unsigned MILAN_CLK_FREQ_HZ = 50_000_000) (
  input  wire        axis_clk, input wire axis_resetn,
  input  wire [15:0] media_clk_src_r, input wire mga_engaged_w,
  input  wire signed [15:0] mga_err_w, input wire follow_sel_r,
  input  wire        media_tick_p, input wire mcsrv_locked_w,
  output wire        recentre_p_o);
`include "settle_piece.svh"
  assign recentre_p_o = src_recentre_p_r;
endmodule
