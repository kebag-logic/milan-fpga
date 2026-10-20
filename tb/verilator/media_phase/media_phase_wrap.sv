// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The media-clock phase loop at the production 512 ms window (#632, #764):
// the followed CRF stream through the real KL_crf_rx into KL_mmcm_drp_servo,
// the harness's MMCM model moving the audio clock, a frame grid divided from
// that clock, the domain's media event (KL_media_domain_event) back into the
// servo's phase detector, and the real, phased KL_crf_tx out.
//
// Clocks are scaled for wall-clock time, never the loop: clk_i runs at
// CLK_FREQ_HZ_P and the audio clock at AUD_HZ_P, with the servo's tick at
// AUD_HZ_P / 1000 audio cycles = 1 ms and its silicon 512 ms window, so every
// gain and bandwidth is the shipping one. The PS step is the silicon 16.9 ps
// (GAIN_NUM_P 59), so the plant gain is the shipping one too.
`default_nettype none
module media_phase_wrap #(
  parameter int unsigned CLK_FREQ_HZ_P = 3_125_000,
  parameter int unsigned AUD_HZ_P      = 768_000,
  parameter int unsigned FS_HZ_P       = 48_000
)(
  input  wire         clk_i,          //! datapath clock (also the PSCLK here)
  input  wire         rst_n,
  input  wire         clk_audio_i,    //! the modeled MMCM CLKOUT0
  input  wire  [63:0] ptp_now_i,      //! gPTP ns
  input  wire         sel_i,          //! CRF followed (0 = INTERNAL: servo IDLE)
  input  wire         ph_en_i,        //! the phase term may run
  input  wire         phc_slew_i,     //! the local PHC's policy slew level (#545)

  //! the followed CRF talker's PDU, already parsed
  input  wire         frame_p_i,
  input  wire  [63:0] ts_ns_i,
  input  wire  [7:0]  seq_i,
  input  wire         mr_i,
  input  wire         tu_i,

  //! MMCME2_ADV ports, to the harness's model
  output wire  [6:0]  drp_addr_o,
  output wire         drp_en_o,
  output wire         drp_we_o,
  output wire  [15:0] drp_di_o,
  input  wire  [15:0] drp_do_i,
  input  wire         drp_rdy_i,
  output wire         mmcm_rst_o,
  input  wire         mmcm_locked_i,
  output wire         ps_en_o,
  output wire         ps_incdec_o,
  input  wire         ps_done_i,

  output wire  [31:0] status_o,
  output wire  [31:0] phase_o,
  output wire         locked_o,
  output wire         ph_settled_o,
  output wire         rx_locked_o,
  output wire         rate_valid_o,

  //! the frame grid's start strobe in the audio domain (the harness reads the
  //! true frame instant off the edge that raises it)
  output wire         frame_a_o,
  //! the domain media event as the servo and KL_crf_tx see it
  output wire         ev_p_o,
  output wire  [63:0] ev_ns_o,
  output wire         ev_live_o,

  //! KL_crf_tx frames
  output wire  [63:0] crft_tdata_o,
  output wire         crft_tvalid_o,
  output wire         crft_tlast_o
);
  localparam int unsigned FRAME_DIV_C = AUD_HZ_P / FS_HZ_P;
  localparam int unsigned TICK_CYC_C  = AUD_HZ_P / 1000;
  //! the frame marker: the frame-start edge toggles cdc_pulse's source level,
  //! and the pulse leaves its 2-flop synchroniser 2 to 3 clk_i edges later; the
  //! domain event samples the PHC on the edge after. Back-dated by the mean.
  localparam int unsigned MARK_LAT_NS_C = (5 * (1_000_000_000 / CLK_FREQ_HZ_P)) / 2;

  // ---- the frame grid (the timing owner's frame divider, modeled) ----------
  logic [1:0] arst_n_r;
  always_ff @(posedge clk_audio_i) arst_n_r <= {arst_n_r[0], rst_n};
  logic [$clog2(FRAME_DIV_C)-1:0] fdiv_r;
  always_ff @(posedge clk_audio_i) begin : frame_div
    if (!arst_n_r[1]) fdiv_r <= '0;
    else fdiv_r <= (32'(fdiv_r) == FRAME_DIV_C - 1) ? '0 : fdiv_r + 1'b1;
  end : frame_div
  assign frame_a_o = (fdiv_r == '0);
  wire mark_w;
  cdc_pulse u_mark (
    .src_clk (clk_audio_i), .src_rst_n (arst_n_r[1]),
    .src_pulse (32'(fdiv_r) == FRAME_DIV_C - 1),
    .dest_clk (clk_i), .dest_rst_n (rst_n), .dest_pulse (mark_w)
  );

  KL_media_domain_event #(
    .MARK_LAT_NS_P (MARK_LAT_NS_C),
    .TIMEOUT_CYC_P (4 * (CLK_FREQ_HZ_P / FS_HZ_P))
  ) u_dom (
    .clk_i (clk_i), .rst_n (rst_n), .mark_i (mark_w), .alt_i (1'b0),
    .ptp_ns_i (ptp_now_i),
    .ev_p_o (ev_p_o), .ev_ns_o (ev_ns_o), .mark_ns_o (), .live_o (ev_live_o)
  );

  // ---- the followed reference ----------------------------------------------
  wire signed [31:0] rate_w;
  wire        ts_p_w;
  wire [63:0] ts_w;
  wire        mr_tgl_w;
  KL_crf_rx #(.CLK_FREQ_HZ_P (CLK_FREQ_HZ_P)) u_rx (
    .clk_i (clk_i), .rst_n (rst_n), .frame_p_i (frame_p_i),
    .subtype_i (8'd4), .seq_i (seq_i), .sid_frame_i (64'd1),
    .pullbase_i (32'd48000), .type_i (8'd1),
    .fsh_i ({16'd8, 16'd96, ts_ns_i[63:32]}),
    .fsh2_i ({ts_ns_i[31:0], 32'd0}),
    .mr_i (mr_i), .tu_i (tu_i), .ptp_now_i (ptp_now_i),
    .en_i (1'b1), .sid_i (64'd1), .stop_i (1'b0),
    .rate_o (rate_w), .rate_valid_o (rate_valid_o), .locked_o (rx_locked_o),
    .ts_p_o (ts_p_w), .ts_o (ts_w), .mr_toggle_p_o (mr_tgl_w),
    .cnt_unlocked_o (), .delta_o (), .pdu_count_o (), .fmt_err_o (),
    .seq_err_o (), .mr_cnt_o (), .tu_cnt_o (), .late_cnt_o (),
    .early_cnt_o (), .cnt_locked_o (), .cnt_intr_o (), .dirty_p_o ()
  );

  // ---- the servo, silicon window, scaled tick divider ---------------------
  KL_mmcm_drp_servo #(
    .CLK_FREQ_HZ_P (CLK_FREQ_HZ_P),
    .TICK_CYC_P    (TICK_CYC_C),
    .RELOCK_TOUT_P (20_000)
  ) servo (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .ps_clk_i (clk_i), .ptp_now_i (ptp_now_i),
    .phc_slew_active_i (phc_slew_i), .sel_i (sel_i),
    .ref_locked_i (rx_locked_o), .ref_rate_valid_i (rate_valid_o),
    .ref_rate_ns_i (rate_w),
    .ph_en_i (ph_en_i && ev_live_o), .dom_ev_p_i (ev_p_o), .dom_ns_i (ev_ns_o[31:0]),
    .ref_ts_p_i (ts_p_w), .ref_ts_ns_i (ts_w[31:0]), .ref_restart_p_i (mr_tgl_w),
    .auto_repair_i (1'b0), .ps_invert_i (1'b0),
    .drp_addr_o (drp_addr_o), .drp_en_o (drp_en_o), .drp_we_o (drp_we_o),
    .drp_di_o (drp_di_o), .drp_do_i (drp_do_i), .drp_rdy_i (drp_rdy_i),
    .mmcm_rst_o (mmcm_rst_o), .mmcm_locked_i (mmcm_locked_i),
    .ps_en_o (ps_en_o), .ps_incdec_o (ps_incdec_o), .ps_done_i (ps_done_i),
    .status_o (status_o), .phase_o (phase_o), .locked_o (locked_o),
    .ph_settled_o (ph_settled_o)
  );

  // ---- the domain's CRF output, phased from the same events ----------------
  KL_crf_tx u_tx (
    .clk_i (clk_i), .rst_n (rst_n), .ev_p_i (ev_p_o), .ev_ns_i (ev_ns_o),
    .enable_i (1'b1), .sid_i (64'h0011_2233_4455_0001),
    .dest_mac_i (48'h91E0_F000_FE00), .station_mac_i (48'h0011_2233_4455),
    .transit_ns_i (32'd2_000_000), .ts_uncertain_i (1'b0), .mr_i (1'b0),
    .tu_last_o (), .mr_last_o (), .vlan_en_i (1'b0), .vlan_pcp_i (3'd3),
    .vlan_vid_i (12'd2), .m_axis_tdata (crft_tdata_o), .m_axis_tkeep (),
    .m_axis_tvalid (crft_tvalid_o), .m_axis_tlast (crft_tlast_o),
    .m_axis_tready (1'b1), .tx_count_o ()
  );
endmodule
`default_nettype wire
