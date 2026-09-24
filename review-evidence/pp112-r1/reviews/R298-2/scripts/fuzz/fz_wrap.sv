// R298-2 reviewer probe: two KL_srp_admission variants in lockstep behind one
// declaration register (captured at the invalidation edge, as KL_srp_top does).
`default_nettype none
module fz_wrap #(parameter int unsigned N = 8) (
    input  wire              clk_i,
    input  wire              rst_n,
    input  wire [7:0]        chg_i,
    input  wire [7:0]        req_i,
    input  wire [7:0][15:0]  mfs_i,
    input  wire [7:0][15:0]  mif_i,
    input  wire [31:0]       rate_i,
    output logic [7:0]       adm_a_o,
    output logic [7:0][31:0] gs_a_o,
    output wire  [31:0]      sum_a_o,
    output wire              over_a_o,
    output wire              rnd_a_o,
    output logic [7:0]       adm_b_o,
    output logic [7:0][31:0] gs_b_o,
    output wire  [31:0]      sum_b_o,
    output wire              over_b_o,
    output wire              rnd_b_o
);
  logic [N-1:0] req_r;
  logic [N-1:0][15:0] mfs_r, mif_r;
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin req_r <= '0; mfs_r <= '0; mif_r <= '0; end
    else for (int s = 0; s < N; s++) if (chg_i[s]) begin
      req_r[s] <= req_i[s]; mfs_r[s] <= mfs_i[s]; mif_r[s] <= mif_i[s];
    end
  end
  wire [N-1:0] aa, ab; wire [N-1:0][31:0] ga, gb;
  `DUT_A #(.N_SOURCES_P(N)) u_a (.clk_i, .rst_n, .req_i(req_r), .invalidate_i(chg_i[N-1:0]),
      .max_frame_i(mfs_r), .interval_frames_i(mif_r), .port_rate_bps_i(rate_i),
      .sr_admitted_o(aa), .granted_slope_bps_o(ga), .sum_slope_bps_o(sum_a_o),
      .over_limit_o(over_a_o), .round_done_o(rnd_a_o));
  KL_srp_admission_eq #(.N_SOURCES_P(N)) u_b (.clk_i, .rst_n, .req_i(req_r), .invalidate_i(chg_i[N-1:0]),
      .max_frame_i(mfs_r), .interval_frames_i(mif_r), .port_rate_bps_i(rate_i),
      .sr_admitted_o(ab), .granted_slope_bps_o(gb), .sum_slope_bps_o(sum_b_o),
      .over_limit_o(over_b_o), .round_done_o(rnd_b_o));
  always_comb begin
    adm_a_o = '0; gs_a_o = '0; adm_b_o = '0; gs_b_o = '0;
    adm_a_o[N-1:0] = aa; gs_a_o[N-1:0] = ga; adm_b_o[N-1:0] = ab; gs_b_o[N-1:0] = gb;
  end
endmodule
`default_nettype wire
