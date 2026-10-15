`default_nettype none
module settle_ooc (
  input  wire        axis_clk,
  input  wire        axis_resetn,
  input  wire [15:0] media_clk_src_r,
  input  wire        follow_sel_r,
  input  wire        mga_engaged_w,
  input  wire        mcsrv_locked_w,
  input  wire signed [15:0] mga_err_w,
  input  wire        media_tick_p,
  input  wire        lb_tap_tvalid_w,
  input  wire        lb_tap_tlast_w,
  input  wire [3:0]  lb_tap_tuser_w,
  input  wire [8-1:0] strtbl_bind_rise_w,
  input  wire [8-1:0] strtbl_bind_fall_w,
  output logic       settle_recentre_p_r,
  output logic       src_recentre_p_r_o
);
  localparam int unsigned MILAN_CLK_FREQ_HZ = 50_000_000;
  localparam int unsigned MCSRV_WIN_LOG2_C  = 9;
  localparam int LB_STREAMS_C = 8;
  localparam int unsigned SRC_SETTLE_ERR_C   = (MILAN_CLK_FREQ_HZ / 48_000) / 64;
  localparam int unsigned SRC_SETTLE_TICKS_C = 2048;
  localparam int unsigned SRC_SETTLE_CEIL_C  = 32768;
  logic [15:0] src_recentre_q_r;   //! the selected index last seen
  logic        src_pend_r;         //! a recentre awaits the settle
  logic        mga_engaged_q_r;
  logic [15:0] src_band_ticks_r;   //! ticks with the grid inside the band
  logic [15:0] src_eng_ticks_r;    //! ticks with the aligner engaged
  //! public: the milan_dp true-ratio leg counts the pulse under a live
  //! selection
  logic        src_recentre_p_r /* verilator public_flat_rd */;
  wire signed [15:0] mga_err_abs_w = (mga_err_w < 16'sd0) ? -mga_err_w : mga_err_w;
  wire src_grid_ok_w = !follow_sel_r ||
                       (mga_engaged_w && (mga_err_abs_w <= 16'(signed'(SRC_SETTLE_ERR_C))));
  wire src_settled_w = (32'(src_band_ticks_r) >= SRC_SETTLE_TICKS_C) ||
                       (32'(src_eng_ticks_r)  >= SRC_SETTLE_CEIL_C);
  always_ff @(posedge axis_clk) begin : g_src_recentre
    if (!axis_resetn) begin
      src_recentre_q_r <= 16'd0;
      src_pend_r       <= 1'b0;
      mga_engaged_q_r  <= 1'b0;
      src_band_ticks_r <= 16'd0;
      src_eng_ticks_r  <= 16'd0;
      src_recentre_p_r <= 1'b0;
    end else begin
      src_recentre_q_r <= media_clk_src_r;
      mga_engaged_q_r  <= mga_engaged_w;
      src_recentre_p_r <= 1'b0;
      if ((media_clk_src_r != src_recentre_q_r) ||
          (mga_engaged_w && !mga_engaged_q_r)) begin
        src_pend_r       <= 1'b1;
        src_band_ticks_r <= 16'd0;
        src_eng_ticks_r  <= 16'd0;
      end else if (src_pend_r) begin
        if (media_tick_p) begin
          src_band_ticks_r <= src_grid_ok_w ? src_band_ticks_r + 16'd1 : 16'd0;
          src_eng_ticks_r  <= (follow_sel_r && mga_engaged_w)
                              ? src_eng_ticks_r + 16'd1 : 16'd0;
        end
        if (src_settled_w) begin
          src_pend_r       <= 1'b0;
          src_recentre_p_r <= 1'b1;
          src_band_ticks_r <= 16'd0;
          src_eng_ticks_r  <= 16'd0;
        end
      end
    end
  end : g_src_recentre
  //! #645 / #647: THE SETTLE RECENTRE. The #386 trigger above stays the
  //! at-switch render recentre, but it fires while the media plane is still
  //! moving: under following the servo locks frequency only, so the phase
  //! walk of its pull-in (1.4 ticks from INTERNAL at a 5.9 ppm offset) lands
  //! in both listener rings after it, and an aligner pull-in at INTERNAL
  //! arms nothing at all. This one recentre per transient fires once the
  //! plane has settled and goes to both rings: the render stage and the
  //! capture crossbar's LOOP queues (settle_recentre_p_r, declared at that
  //! instance). Armed by a change of the selected index, by the aligner's
  //! re-engagement, at INTERNAL by a listener bind's first PDU (below), and,
  //! outside recovery, by an aligner excursion past the quiet band (a
  //! pull-in under a running stream). SETTLED means:
  //! under a followed source, the servo LOCKED for SETTLE_LOCK_WIN_C windows
  //! running, since the frequency-only loop's phase tail falls about 0.64 a
  //! window; at INTERNAL, the aligner inside the settle band for
  //! SRC_SETTLE_TICKS_C ticks running, or not engaged at all (no pull to
  //! wait out). An excursion while pending restarts that run. The ceiling,
  //! 2^SETTLE_CEIL_LOG2_C ticks (21.8 s) from the arming, fires it whatever
  //! the loops do. After an action, excursion arming stays disabled until
  //! the engaged aligner has spent 2048 consecutive ticks in the quiet band.
  //! Reuse the pending dwell counter for that recovery qualification; a
  //! source change or re-engagement still arms immediately.
  //! Twice the quiet +/-1 axis-cycle quantisation, independent of the
  //! clock-frequency-scaled #386 settling band.
  localparam int unsigned SETTLE_EXC_ERR_C   = 2;
  localparam int unsigned SETTLE_LOCK_WIN_C  = 8;
  //! one servo window in media ticks: 2^MCSRV_WIN_LOG2_C ticks of 1 ms
  localparam int unsigned SETTLE_LOCK_TICKS_C =
      SETTLE_LOCK_WIN_C * (1 << MCSRV_WIN_LOG2_C) * (48_000 / 1000);
  localparam int unsigned SETTLE_RUN_W_C     = $clog2(SETTLE_LOCK_TICKS_C + 1);
  localparam int unsigned SETTLE_CEIL_LOG2_C = 20;
  logic                        settle_pend_r /* verilator public_flat_rd */;
  logic                        settle_recover_r /* verilator public_flat_rd */;
  logic [SETTLE_RUN_W_C-1:0]   settle_run_ticks_r /* verilator public_flat_rd */;
  logic [SETTLE_CEIL_LOG2_C:0] settle_ceil_ticks_r;
  wire settle_exc_w = mga_engaged_w &&
                      (mga_err_abs_w > 16'(signed'(SETTLE_EXC_ERR_C)));
  //! #645, bench lane B17: A LISTENER BIND'S FIRST PDU AT INTERNAL. The
  //! capture crossbar's LOOP queue primes where a bound stream's first PDU
  //! lands (KL_chan_map_capture PRIME: its accepted tlast beat), and at
  //! INTERNAL no other term arms this recentre, so the ring kept that phase,
  //! within a tick of its empty edge, until the first late burst slipped it
  //! one frame: once in each of B17's 10 binds. Each LOOP stream waits from
  //! its bind's rise for that beat, and at INTERNAL the beat arms the
  //! recentre, which then fires as every INTERNAL arming does. Under
  //! following the beat only ends the wait, so the switch rules alone arm
  //! there; an unbind ends it too. No LOOP feed (LOOPBACK_P = 0), no arm.
  logic [LB_STREAMS_C-1:0] settle_bind_wait_r;
  logic [LB_STREAMS_C-1:0] settle_bind_pdu_w;
  always_comb begin : settle_bind_pdu
    for (int s = 0; s < LB_STREAMS_C; s++) begin
      settle_bind_pdu_w[s] = settle_bind_wait_r[s] && lb_tap_tvalid_w &&
                             lb_tap_tlast_w && (32'(lb_tap_tuser_w) == s);
    end
  end : settle_bind_pdu
  wire settle_bind_arm_w = !follow_sel_r && (|settle_bind_pdu_w);
  always_ff @(posedge axis_clk) begin : g_settle_bind_wait
    if (!axis_resetn) settle_bind_wait_r <= '0;
    else settle_bind_wait_r <= (settle_bind_wait_r | strtbl_bind_rise_w[LB_STREAMS_C-1:0]) &
                               ~settle_bind_pdu_w & ~strtbl_bind_fall_w[LB_STREAMS_C-1:0];
  end : g_settle_bind_wait
  //! the #386 block's registered copies give the change and re-engagement
  wire settle_arm_w = (media_clk_src_r != src_recentre_q_r) ||
                      (mga_engaged_w && !mga_engaged_q_r) ||
                      settle_bind_arm_w ||
                      (settle_exc_w && !settle_pend_r && !settle_recover_r);
  wire settle_steady_w = follow_sel_r
                         ? mcsrv_locked_w
                         : (!mga_engaged_w ||
                            (mga_err_abs_w <= 16'(signed'(SRC_SETTLE_ERR_C))));
  wire [SETTLE_RUN_W_C-1:0] settle_need_w = follow_sel_r
                                            ? SETTLE_RUN_W_C'(SETTLE_LOCK_TICKS_C)
                                            : SETTLE_RUN_W_C'(SRC_SETTLE_TICKS_C);
  wire settle_fire_w = (settle_run_ticks_r >= settle_need_w) ||
                       settle_ceil_ticks_r[SETTLE_CEIL_LOG2_C];
  always_ff @(posedge axis_clk) begin : g_settle_recentre
    if (!axis_resetn) begin
      settle_pend_r       <= 1'b0;
      settle_recover_r    <= 1'b0;
      settle_run_ticks_r  <= '0;
      settle_ceil_ticks_r <= '0;
      settle_recentre_p_r <= 1'b0;
    end else begin
      settle_recentre_p_r <= 1'b0;
      if (settle_arm_w) begin
        settle_pend_r       <= 1'b1;
        settle_run_ticks_r  <= '0;
        settle_ceil_ticks_r <= '0;
      end else if (settle_pend_r) begin
        if (settle_fire_w) begin
          settle_pend_r       <= 1'b0;
          settle_run_ticks_r  <= '0;
          settle_ceil_ticks_r <= '0;
          settle_recentre_p_r <= 1'b1;
          settle_recover_r    <= 1'b1;
        end else begin
          if (media_tick_p) begin
            settle_run_ticks_r  <= settle_steady_w ? settle_run_ticks_r + 1'b1 : '0;
            settle_ceil_ticks_r <= settle_ceil_ticks_r + 1'b1;
          end
          if (settle_exc_w) settle_run_ticks_r <= '0;
        end
      end else if (settle_recover_r) begin
        if (!mga_engaged_w || settle_exc_w) begin
          settle_run_ticks_r <= '0;
        end else if (settle_run_ticks_r >= SETTLE_RUN_W_C'(SRC_SETTLE_TICKS_C)) begin
          settle_recover_r   <= 1'b0;
          settle_run_ticks_r <= '0;
        end else if (media_tick_p) begin
          settle_run_ticks_r <= settle_run_ticks_r + 1'b1;
        end
      end
    end
  end : g_settle_recentre
  assign src_recentre_p_r_o = src_recentre_p_r;
endmodule
`default_nettype wire
