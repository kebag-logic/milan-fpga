/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
// Capture declarations at the same edge as KL_srp_top. Fixed-width bench
// ports let the identical C++ oracle cover one through eight sources.
`default_nettype none
module srp_admission_wrap #(
    parameter int unsigned N_SOURCES_P = 8
) (
    input wire clk_i,
    input wire rst_n,
    input wire [7:0] change_i,
    input wire [7:0] req_i,
    input wire [7:0][15:0] max_frame_i,
    input wire [7:0][15:0] interval_frames_i,
    input wire [31:0] port_rate_bps_i,
    output logic [7:0] admitted_o,
    output logic [7:0][31:0] granted_o,
    output wire [31:0] sum_o,
    output wire over_o,
    output wire round_o,
    output wire [7:0] sample_index_o
);
  logic [N_SOURCES_P-1:0] req_r;
  logic [N_SOURCES_P-1:0][15:0] mfs_r, mif_r;
  wire [N_SOURCES_P-1:0] admitted_w;
  wire [N_SOURCES_P-1:0][31:0] granted_w;
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      req_r <= '0;
      mfs_r <= '0;
      mif_r <= '0;
    end else begin
      for (int s = 0; s < N_SOURCES_P; s++) begin
        if (change_i[s]) begin
          req_r[s] <= req_i[s];
          mfs_r[s] <= max_frame_i[s];
          mif_r[s] <= interval_frames_i[s];
        end
      end
    end
  end
  KL_srp_admission #(.N_SOURCES_P(N_SOURCES_P)) u_dut (
      .clk_i(clk_i), .rst_n(rst_n), .req_i(req_r),

      .max_frame_i(mfs_r), .interval_frames_i(mif_r),
      .port_rate_bps_i(port_rate_bps_i), .sr_admitted_o(admitted_w),
      .granted_slope_bps_o(granted_w), .sum_slope_bps_o(sum_o),
      .over_limit_o(over_o), .round_done_o(round_o)
  );
  always_comb begin
    admitted_o = '0;
    granted_o = '0;
    admitted_o[N_SOURCES_P-1:0] = admitted_w;
    granted_o[N_SOURCES_P-1:0] = granted_w;
  end
  assign sample_index_o = 8'(u_dut.cidx_r);
endmodule
`default_nettype wire
