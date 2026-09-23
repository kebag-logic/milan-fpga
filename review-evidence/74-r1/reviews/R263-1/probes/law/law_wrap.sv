// Reviewer probe (R263-1, #74 item 2): the junction counter law, head vs
// base, on one shared random stream of slot writes and ticks. Both
// instances are the smallest legal shape the media_grid_align wrap uses;
// KL_chan_map_capture_base is the base file with only its module renamed.
`default_nettype none
module law_wrap (
  input  wire        clk,
  input  wire        rst_n,
  input  wire        pv_i,
  input  wire [3:0]  slot_i,
  input  wire        tick_i,
  output wire [15:0] dup_h_o,
  output wire [15:0] skip_h_o,
  output wire [15:0] dup_b_o,
  output wire [15:0] skip_b_o
);
  KL_chan_map_capture #(.N_SLOTS_P(2), .N_TDM_P(2), .N_LB_STREAMS_P(1), .N_LB_CH_P(2)) u_h (
    .clk_i(clk), .rst_n(rst_n),
    .map_wr_en_i(1'b0), .map_wr_addr_i(2'd0), .map_wr_data_i(13'd0),
    .map_rd_en_i(1'b0), .map_rd_addr_i(2'd0),
    .map_rd_data_o(), .map_rd_valid_o(), .map_flat_o(),
    .i2s_pair_valid_i(1'b0), .i2s_l_i(24'd0), .i2s_r_i(24'd0),
    .tdm_pair_valid_i(pv_i), .tdm_pair_slot_i(slot_i), .tdm_l_i(24'd0), .tdm_r_i(24'd0),
    .tone_smp_i(24'd0), .tick_i(tick_i),
    .pair_valid_o(), .pair_slot_o(), .pair_l_o(), .pair_r_o(),
    .lb_dup_cnt_o(), .lb_skip_cnt_o(),
    .tdm_dup_cnt_o(dup_h_o), .tdm_skip_cnt_o(skip_h_o));
  KL_chan_map_capture_base #(.N_SLOTS_P(2), .N_TDM_P(2), .N_LB_STREAMS_P(1), .N_LB_CH_P(2)) u_b (
    .clk_i(clk), .rst_n(rst_n),
    .map_wr_en_i(1'b0), .map_wr_addr_i(2'd0), .map_wr_data_i(13'd0),
    .map_rd_en_i(1'b0), .map_rd_addr_i(2'd0),
    .map_rd_data_o(), .map_rd_valid_o(), .map_flat_o(),
    .i2s_pair_valid_i(1'b0), .i2s_l_i(24'd0), .i2s_r_i(24'd0),
    .tdm_pair_valid_i(pv_i), .tdm_pair_slot_i(slot_i), .tdm_l_i(24'd0), .tdm_r_i(24'd0),
    .tone_smp_i(24'd0), .tick_i(tick_i),
    .pair_valid_o(), .pair_slot_o(), .pair_l_o(), .pair_r_o(),
    .lb_dup_cnt_o(), .lb_skip_cnt_o(),
    .tdm_dup_cnt_o(dup_b_o), .tdm_skip_cnt_o(skip_b_o));
endmodule
`default_nettype wire
