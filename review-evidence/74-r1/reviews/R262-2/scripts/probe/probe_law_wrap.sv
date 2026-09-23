// SPDX-License-Identifier: CERN-OHL-W-2.0
// Review probe: the REAL KL_chan_map_capture junction counters with the tick
// and the slot-0 frame marker both driven from C++ (any interleaving,
// coincidences included). Same parameters as the media_grid_align wrap.
`default_nettype none
module probe_law_wrap (
  input  wire        clk,
  input  wire        rst_n,
  input  wire        frame_ev_i,
  input  wire        tick_i,
  output wire [15:0] tdm_dup_cnt_o,
  output wire [15:0] tdm_skip_cnt_o
);
  KL_chan_map_capture #(
    .N_SLOTS_P (2), .N_TDM_P (2), .N_LB_STREAMS_P (1), .N_LB_CH_P (2)
  ) u_junction (
    .clk_i (clk), .rst_n (rst_n),
    .map_wr_en_i (1'b0), .map_wr_addr_i (2'd0), .map_wr_data_i (13'd0),
    .map_rd_en_i (1'b0), .map_rd_addr_i (2'd0),
    .map_rd_data_o (), .map_rd_valid_o (), .map_flat_o (),
    .i2s_pair_valid_i (1'b0), .i2s_l_i (24'd0), .i2s_r_i (24'd0),
    .tdm_pair_valid_i (frame_ev_i), .tdm_pair_slot_i (4'd0),
    .tdm_l_i (24'd0), .tdm_r_i (24'd0),
    .tone_smp_i (24'd0),
    .tick_i (tick_i),
    .pair_valid_o (), .pair_slot_o (), .pair_l_o (), .pair_r_o (),
    .lb_dup_cnt_o (), .lb_skip_cnt_o (),
    .tdm_dup_cnt_o (tdm_dup_cnt_o), .tdm_skip_cnt_o (tdm_skip_cnt_o)
  );
endmodule
`default_nettype wire
