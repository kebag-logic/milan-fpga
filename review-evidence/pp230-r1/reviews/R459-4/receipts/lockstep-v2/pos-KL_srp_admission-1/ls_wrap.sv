module ls_wrap (
    output logic [4:0] mm_o,
    output logic [4:0] act_o,
    input  wire clk_i,
    input  wire rst_n,
    input  wire req_i,
    input  wire invalidate_i,
    input  wire [15:0] max_frame_i,
    input  wire [15:0] interval_frames_i,
    input  wire [31:0] port_rate_bps_i
);
  wire a_sr_admitted_o, b_sr_admitted_o;
  wire [31:0] a_granted_slope_bps_o, b_granted_slope_bps_o;
  wire [31:0] a_sum_slope_bps_o, b_sum_slope_bps_o;
  wire a_over_limit_o, b_over_limit_o;
  wire a_round_done_o, b_round_done_o;
  B_KL_srp_admission #(.N_SOURCES_P(1)) u_a (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .req_i(req_i),
    .invalidate_i(invalidate_i),
    .max_frame_i(max_frame_i),
    .interval_frames_i(interval_frames_i),
    .port_rate_bps_i(port_rate_bps_i),
    .sr_admitted_o(a_sr_admitted_o),
    .granted_slope_bps_o(a_granted_slope_bps_o),
    .sum_slope_bps_o(a_sum_slope_bps_o),
    .over_limit_o(a_over_limit_o),
    .round_done_o(a_round_done_o));
  KL_srp_admission #(.N_SOURCES_P(1)) u_b (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .req_i(req_i),
    .invalidate_i(invalidate_i),
    .max_frame_i(max_frame_i),
    .interval_frames_i(interval_frames_i),
    .port_rate_bps_i(port_rate_bps_i),
    .sr_admitted_o(b_sr_admitted_o),
    .granted_slope_bps_o(b_granted_slope_bps_o),
    .sum_slope_bps_o(b_sum_slope_bps_o),
    .over_limit_o(b_over_limit_o),
    .round_done_o(b_round_done_o));
  assign mm_o[0] = (a_sr_admitted_o != b_sr_admitted_o);
  assign act_o[0] = |b_sr_admitted_o;
  assign mm_o[1] = (a_granted_slope_bps_o != b_granted_slope_bps_o);
  assign act_o[1] = |b_granted_slope_bps_o;
  assign mm_o[2] = (a_sum_slope_bps_o != b_sum_slope_bps_o);
  assign act_o[2] = |b_sum_slope_bps_o;
  assign mm_o[3] = (a_over_limit_o != b_over_limit_o);
  assign act_o[3] = |b_over_limit_o;
  assign mm_o[4] = (a_round_done_o != b_round_done_o);
  assign act_o[4] = |b_round_done_o;
endmodule
