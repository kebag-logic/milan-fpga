/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : d3a_shadow_proxy.sv   (COST PROXY, design evidence #500)
//
//  Description : The STORAGE candidate (a) needs and candidate (b) does not:
//                one shadow per group, in the image of KL_acmp_nvm_shadow's
//                "RAM-shaped sync-read array", sized by the record payloads
//                of the saved-state allocation at the shape. It is a FLOOR:
//                names and maps are shadowed as 64-bit lanes (8 lanes a name,
//                one lane a map entry), the narrowest read the managers could
//                serialise from, where KL_acmp_nvm_shadow reads its whole
//                projection in one cycle. The per-group control is priced
//                separately, as KL_acmp_nvm_shadow itself.
//---------------------------------------------------------------------------//
`default_nettype none

module d3a_shadow_proxy #(
    parameter int unsigned N_STREAM_IN_P  = 2,
    parameter int unsigned N_STREAM_OUT_P = 2,
    parameter int unsigned N_MAP_ENT_P    = 25,   //! map entries, both directions
    parameter int unsigned N_NAME_P       = 38
) (
    input  wire         clk_i,
    input  wire  [3:0]  grp_i,        //! which shadow the port addresses
    input  wire         we_i,
    input  wire  [11:0] waddr_i,
    input  wire  [63:0] wdata_i,
    input  wire  [11:0] raddr_i,
    output logic [63:0] rdata_o
);
  localparam int unsigned N_FMT_C  = N_STREAM_IN_P + N_STREAM_OUT_P;
  localparam int unsigned N_LANE_C = 8 * N_NAME_P;

  logic [63:0] fmt_r  [N_FMT_C];          //! stream formats in and out
  logic [31:0] ptof_r [N_STREAM_OUT_P];   //! presentation time offsets
  logic [63:0] map_r  [N_MAP_ENT_P];      //! one lane per map entry
  logic [63:0] name_r [N_LANE_C];         //! eight lanes per name
  logic [31:0] rate_r;
  logic [15:0] clks_r, cfg_r;
  logic [63:0] q_fmt_r, q_map_r, q_name_r;
  logic [31:0] q_ptof_r;
  logic [3:0]  grp_q_r;

  always_ff @(posedge clk_i) begin
    if (we_i && (grp_i == 4'd0) && (32'(waddr_i) < N_FMT_C))        fmt_r[waddr_i]  <= wdata_i;
    if (we_i && (grp_i == 4'd1) && (32'(waddr_i) < N_STREAM_OUT_P)) ptof_r[waddr_i] <= wdata_i[31:0];
    if (we_i && (grp_i == 4'd2) && (32'(waddr_i) < N_MAP_ENT_P))    map_r[waddr_i]  <= wdata_i;
    if (we_i && (grp_i == 4'd3) && (32'(waddr_i) < N_LANE_C))       name_r[waddr_i] <= wdata_i;
    if (we_i && (grp_i == 4'd4)) rate_r <= wdata_i[31:0];
    if (we_i && (grp_i == 4'd5)) clks_r <= wdata_i[15:0];
    if (we_i && (grp_i == 4'd6)) cfg_r  <= wdata_i[15:0];
    q_fmt_r  <= fmt_r[raddr_i];
    q_ptof_r <= ptof_r[raddr_i];
    q_map_r  <= map_r[raddr_i];
    q_name_r <= name_r[raddr_i];
    grp_q_r  <= grp_i;
  end

  always_comb begin
    unique case (grp_q_r)
      4'd0:    rdata_o = q_fmt_r;
      4'd1:    rdata_o = {32'd0, q_ptof_r};
      4'd2:    rdata_o = q_map_r;
      4'd3:    rdata_o = q_name_r;
      4'd4:    rdata_o = {32'd0, rate_r};
      4'd5:    rdata_o = {48'd0, clks_r};
      default: rdata_o = {48'd0, cfg_r};
    endcase
  end
endmodule

`default_nettype wire
