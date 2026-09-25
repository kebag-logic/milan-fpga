// Reviewer latency probe (#545): the engine's registered outputs are driven
// by the harness; the shadow's adjfine latch, the datapath alignment block
// and the servo's staging flops are transcribed verbatim from the exact head
// (KL_gptp_shadow.sv adj_latch, milan_datapath.sv slew_rate_alignment,
// KL_mmcm_drp_servo.sv ptp_stage_S/slew_sample_stage); the CSR crossing and
// the PHC counter are the real repository modules.
`default_nettype none
module latency_wrap (
  input  wire        clk,
  input  wire        rst_n,
  input  wire        eng_we_i,     // engine phc_addend_we_o (registered)
  input  wire [31:0] eng_val_i,    // engine phc_addend_o (registered)
  input  wire        eng_level_i,  // engine phc_slew_active_o (registered)
  output logic [63:0] ptp_q_o,     // servo ptp_q_r
  output logic        slew_q_o     // servo phc_slew_q_r
);
  logic signed [31:0] phc_adj_r;
  always_ff @(posedge clk) begin : adj_latch
    if (!rst_n)        phc_adj_r <= '0;
    else if (eng_we_i) phc_adj_r <= $signed(eng_val_i);
  end
  logic [3:0] gptp_slew_tail_r;
  wire gptp_slew_eff_w = eng_level_i || (|gptp_slew_tail_r);
  always_ff @(posedge clk) begin : slew_rate_alignment
    if (!rst_n) gptp_slew_tail_r <= '0;
    else gptp_slew_tail_r <= {gptp_slew_tail_r[2:0], eng_level_i};
  end
  wire t_en; wire [31:0] t_incr, t_adj; wire [63:0] t_tod, t_off, snap, a_rd, pps_rd, t_ppst;
  wire t_load, t_adjust, t_snap, a_rdv, t_ppse, t_ppsa, snapv, pps_o_w; wire [63:0] ppsl;
  wire [63:0] ptp_now_w;
  ptp_csr_sync #(.TS_WIDTH(64), .INCR_WIDTH(32), .PPS_P(1'b0)) u_sync (
    .aclk(clk), .aresetn(rst_n), .a_enable(1'b1), .a_incr(32'h0800_0000),
    .a_adj(unsigned'(phc_adj_r)), .a_tod_wr('0), .a_offset('0), .a_cmd_load(1'b0),
    .a_cmd_adjust(1'b0), .a_cmd_snapshot(1'b0), .a_tod_rd(a_rd), .a_tod_rd_valid(a_rdv),
    .a_pps_enable(1'b0), .a_pps_target_ns('0), .a_pps_arm(1'b0), .a_pps_target_rd_ns(pps_rd),
    .ts_clk(clk), .ts_resetn(rst_n), .t_enable(t_en), .t_incr(t_incr), .t_adj(t_adj),
    .t_tod_wr(t_tod), .t_cmd_load(t_load), .t_offset(t_off), .t_cmd_adjust(t_adjust),
    .t_cmd_snapshot(t_snap), .t_tod_snapshot(snap), .t_tod_snapshot_valid(snapv),
    .t_pps_enable(t_ppse), .t_pps_target_ns(t_ppst), .t_pps_arm(t_ppsa), .t_pps_target_live_ns(ppsl));
  timestamp_counter #(.COUNTER_WIDTH(64), .INCR_WIDTH(32), .FRAC_WIDTH(24), .PPS_P(1'b0)) u_ctr (
    .clk(clk), .resetn(rst_n), .enable_i(t_en), .incr_i(t_incr), .adj_i(t_adj),
    .tod_wr_i(t_tod), .cmd_load_i(t_load), .offset_i(t_off), .cmd_adjust_i(t_adjust),
    .cmd_snapshot_i(t_snap), .pps_enable_i(1'b0), .pps_target_ns_i('0), .pps_arm_i(1'b0),
    .timestamp_out(ptp_now_w), .tod_snapshot_o(snap), .tod_snapshot_valid_o(snapv),
    .pps_o(pps_o_w), .pps_target_ns_o(ppsl));
  always_ff @(posedge clk) ptp_q_o <= ptp_now_w;
  always_ff @(posedge clk) begin
    if (!rst_n) slew_q_o <= 1'b0;
    else slew_q_o <= gptp_slew_eff_w;
  end
endmodule
`default_nettype wire
