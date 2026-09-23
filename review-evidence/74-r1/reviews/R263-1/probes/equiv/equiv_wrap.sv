// Reviewer probe (R263-1, #74 item 2): base-vs-head lockstep of the whole
// closed loop. Two independent loops (aligner + real KL_media_nco each), one
// shared physical frame marker and selection. KL_media_grid_align_base is
// the base revision's module, renamed by the build script and nothing else.
`default_nettype none
module equiv_wrap (
  input  wire               clk,
  input  wire               rst_n,
  input  wire               sel_i,
  input  wire               frame_ev_i,
  output wire               tick_h_o,
  output wire               tick_b_o,
  output wire signed [15:0] u_h_o,
  output wire signed [15:0] u_b_o,
  output wire signed [15:0] err_h_o,
  output wire signed [15:0] err_b_o,
  output wire               eng_h_o,
  output wire               eng_b_o
);
  wire signed [15:0] u_h, u_b;
  KL_media_grid_align #(.CLK_FREQ_HZ_P(100_000_000), .FS_HZ_P(48_000)) u_h_align (
    .clk_i(clk), .rst_n(rst_n), .sel_i(sel_i), .frame_ev_i(frame_ev_i),
    .tick_i(tick_h_o), .u_o(u_h), .engaged_o(eng_h_o), .err_cyc_o(err_h_o));
  KL_media_nco #(.CLK_FREQ_HZ_P(100_000_000), .FS_HZ_P(48_000), .TRIMW_P(18)) u_h_nco (
    .clk_i(clk), .rst_n(rst_n), .trim_i(18'sd0), .servo_trim_i(u_h),
    .servo_en_i(sel_i), .tick_o(tick_h_o), .phase_o());
  KL_media_grid_align_base #(.CLK_FREQ_HZ_P(100_000_000), .FS_HZ_P(48_000)) u_b_align (
    .clk_i(clk), .rst_n(rst_n), .sel_i(sel_i), .frame_ev_i(frame_ev_i),
    .tick_i(tick_b_o), .u_o(u_b), .engaged_o(eng_b_o), .err_cyc_o(err_b_o));
  KL_media_nco #(.CLK_FREQ_HZ_P(100_000_000), .FS_HZ_P(48_000), .TRIMW_P(18)) u_b_nco (
    .clk_i(clk), .rst_n(rst_n), .trim_i(18'sd0), .servo_trim_i(u_b),
    .servo_en_i(sel_i), .tick_o(tick_b_o), .phase_o());
  assign u_h_o = u_h;
  assign u_b_o = u_b;
endmodule
`default_nettype wire
