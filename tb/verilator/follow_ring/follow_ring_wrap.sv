// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : follow_ring_wrap.sv
  Description : The media-clock plane and the two listener rings it paces,
                bound as milan_datapath binds them on the shipping AX7101 1x1
                TDM8 shape, for #645 (the loopback ring slips one frame after
                an INTERNAL-to-AAF set) and #647 (a running stream keeps a
                render-latency shift after an INTERNAL aligner pull-in).

                Real RTL: the AAF clock meter, the CRF receiver, the MMCM
                servo, the media NCO, the grid aligner, the capture crossbar's
                LOOP bucket (KL_chan_map_capture: the ring SLIP_LB counts) and
                the render setpoint stage (KL_render_setpoint: the ring the
                #386 recentre re-centres). The datapath's own glue between
                them - the clock-source decode, the servo's reference mux with
                its W2 presentation, the A2-a aligner select with its keep-off
                and one-cycle-late tick, the #386 settled-grid trigger, the
                #645 settle recentre and the render stage's recentre set - is
                copied verbatim out of milan_datapath.sv by dp_glue.py at
                build time, never restated here. The one binding restated is
                the settle pulse into the LOOP bucket's lb_recentre_i, as
                milan_datapath binds it on its one listener stream.

                Scaled, and why (the harness header states the arithmetic):
                  * clk_i is CLK_HZ_P (6.25 MHz, an eighth of the shipping
                    50 MHz axis clock). Every loop the rings see runs on
                    gPTP time or on the audio clock, so the clock rate
                    changes no rate; the aligner's gains are the one place
                    its loop arithmetic is in clk_i cycles, so its KP_LOG2_P
                    and KI_LOG2_P are derived from the shipping 2 and 12 by
                    the clock ratio (2 + 3 and 12 - 3 at an eighth), which
                    keeps its loop in SAMPLE units the shipping one; its
                    keep-off (a quarter sample) and the #386 settle band
                    (1/64 sample) derive from the clock as the datapath
                    derives them;
                  * the audio clock is the shipping 24.576 MHz divided by 32
                    with TICK_CYC_P = 768 and GAIN_NUM_P = 1, as
                    tb/verilator/aaf_clock_meter/meter_servo_wrap.sv runs the
                    servo's silicon loop; one physical frame is 16 of its
                    cycles, so the frame grid is the physical 48 kHz grid;
                  * the capture crossbar's slot walk is cut to two slots with
                    a one-cycle gap: only its LOOP bucket is graded, and the
                    pre-walk pop that bucket's law lives in is unchanged.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module follow_ring_wrap #(
  parameter int unsigned CLK_HZ_P      = 6_250_000, //! the axis clock
  parameter int unsigned TICK_CYC_P    = 768,       //! audio cycles per 1 ms servo tick
  parameter int unsigned FRAME_DIV_P   = 16,        //! audio cycles per physical frame
  parameter int unsigned RX_CH_P       = 8          //! the shape's listener wire width
)(
  input  wire         clk_i,
  input  wire         rst_n,
  input  wire         clk_audio_i,
  input  wire         ps_clk_i,
  input  wire [63:0]  ptp_now_i,
  //! the stored CLOCK_SOURCE index (the processor's pp_aecp_clk_src_index_w)
  input  wire [15:0]  clk_src_idx_i,
  //! the serial-clock hold: the physical frame divider stops while high
  input  wire         frame_hold_i,
  //! the followed AAF talker's PDUs on STREAM_INPUT 0 (the parser bundle)
  input  wire         aaf_match_p_i,
  input  wire [7:0]   aaf_seq_i,
  input  wire [31:0]  aaf_ts_i,
  input  wire         aaf_mr_i,
  //! the CRF talker's PDUs on STREAM_INPUT 1 (the parser bundle)
  input  wire         crf_frame_p_i,
  input  wire [7:0]   crf_seq_i,
  input  wire [63:0]  crf_ts_i,
  input  wire         crf_mr_i,
  //! STREAM_INPUT 0's depacketizer payload clone (accepted beats)
  input  wire [63:0]  pcm_tdata_i,
  input  wire         pcm_tvalid_i,
  input  wire         pcm_tlast_i,
  input  wire [3:0]   pcm_chans_i,     //! the wire channels_per_frame
  input  wire         bind_fall_i,     //! STREAM_INPUT 0's bind wipe pulse
  //! harness control only: an extra recentre pulse into the render stage,
  //! ORed beside the datapath's own (a planted control, never a design path)
  input  wire         tb_recentre_p_i,
  //! MMCME2_ADV model ports
  output wire [6:0]   drp_addr_o,
  output wire         drp_en_o,
  output wire         drp_we_o,
  output wire [15:0]  drp_di_o,
  input  wire [15:0]  drp_do_i,
  input  wire         drp_rdy_i,
  output wire         mmcm_rst_o,
  input  wire         mmcm_locked_i,
  output wire         ps_en_o,
  output wire         ps_incdec_o,
  input  wire         ps_done_i,
  //! observation
  output wire [31:0]  servo_status_o,
  output wire [15:0]  lb_dup_o,
  output wire [15:0]  lb_skip_o,
  output wire [7:0]   render_fill_o,
  output wire         render_prefill_o,
  output wire [15:0]  render_rails_o,
  output wire [15:0]  render_recentres_o,
  output wire [15:0]  render_underruns_o,
  output wire         render_pop_p_o,
  output wire         render_pdu_end_p_o
);

  // ---------------------------------------------------------------------- //
  // The names the datapath's glue reads, bound to this harness             //
  // ---------------------------------------------------------------------- //
  localparam int unsigned MILAN_CLK_FREQ_HZ = CLK_HZ_P;
  localparam int unsigned N_STREAMS = 1;
  //! the aligner's gains, scaled from the shipping 50 MHz ones (KP_LOG2 2,
  //! KI_LOG2 12) by the clock ratio, which must be a power of two
  localparam int unsigned SHIP_CLK_HZ_C    = 50_000_000;
  localparam int unsigned MGA_SCALE_LOG2_C = $clog2(SHIP_CLK_HZ_C / CLK_HZ_P);
  localparam int unsigned MGA_KP_LOG2_C    = 2 + MGA_SCALE_LOG2_C;
  localparam int unsigned MGA_KI_LOG2_C    = 12 - MGA_SCALE_LOG2_C;
  if ((SHIP_CLK_HZ_C % CLK_HZ_P) != 0 ||
      (SHIP_CLK_HZ_C / CLK_HZ_P) != (1 << MGA_SCALE_LOG2_C)) begin : g_chk_clk
    $error("follow_ring_wrap: CLK_HZ_P=%0d must be 50 MHz over a power of two, or the aligner's gains do not scale",
           CLK_HZ_P);
  end : g_chk_clk
  wire axis_clk    = clk_i;
  wire axis_resetn = rst_n;
  //! the shipping AX7101 1x1 TDM8 shape's clock-source tables (+incdir)
  `include "gen/adp_shape_defaults.svh"

  wire [15:0] pp_aecp_clk_src_index_w = clk_src_idx_i;
  logic [15:0] media_clk_src_r    /* verilator public_flat_rd */;
  logic        crf_clk_selected_r /* verilator public_flat_rd */;
  logic        aaf_clk_selected_r /* verilator public_flat_rd */;
  logic        follow_sel_r       /* verilator public_flat_rd */;
  logic        int_clk_selected_r /* verilator public_flat_rd */;

  wire               aafm_locked_w /* verilator public_flat_rd */;
  wire signed [31:0] aafm_rate_w /* verilator public_flat_rd */;
  wire               aafm_rate_valid_w /* verilator public_flat_rd */;
  wire               crf_locked_w /* verilator public_flat_rd */;
  wire signed [31:0] crf_rate_w /* verilator public_flat_rd */;
  wire               crf_rate_valid_w /* verilator public_flat_rd */;

  wire               media_tick_p /* verilator public_flat_rd */;
  wire               mga_engaged_w /* verilator public_flat_rd */;
  wire signed [15:0] mga_err_w /* verilator public_flat_rd */;
  wire signed [15:0] mnco_servo_trim_w /* verilator public_flat_rd */;
  //! no PHC step in this harness: the gPTP plane is ideal
  wire               media_rebase_p_w = 1'b0;
  //! the servo's LOCKED, which the settle recentre counts
  wire               mcsrv_locked_w /* verilator public_flat_rd */;
  //! the settle recentre's pulse (milan_datapath declares it at the capture
  //! crossbar's instance, ahead of the glue that drives it)
  logic              settle_recentre_p_r /* verilator public_flat_rd */;

  //! milan_datapath's glue, copied verbatim by dp_glue.py at build time
  `include "dp_glue.svh"

  // ---------------------------------------------------------------------- //
  // The followed measurements                                              //
  // ---------------------------------------------------------------------- //
  //! the Base format the meter consumes, at the stream's wire channel count:
  //! 6 samples x 4 octets x channels
  wire [63:0] aaf_fsh_w = {8'h02, 4'h5, 2'b00, 10'(pcm_chans_i), 8'd32,
                           16'(24 * pcm_chans_i), 16'd0};
  KL_aaf_clock_meter #(
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),
    .N_LISTENERS_P (N_STREAMS)
  ) aaf_clock_meter (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .en_i (aaf_clk_selected_r), .follow_idx_i (aaf_follow_idx_r),
    .bind_rise_i (1'b0), .stopped_i (1'b0),
    .match_p_i (aaf_match_p_i), .match_idx_i (1'b0), .subtype_i (8'h02),
    .tv_i (1'b1), .tu_i (1'b0), .mr_i (aaf_mr_i), .seq_i (aaf_seq_i),
    .ts_ns_i (aaf_ts_i), .fsh_i (aaf_fsh_w),
    .locked_o (aafm_locked_w), .rate_ns_o (aafm_rate_w),
    .rate_valid_o (aafm_rate_valid_w), .disrupt_p_o (), .mr_toggle_p_o (),
    .max_dev_ns_o (), .status_o ()
  );

  localparam logic [63:0] CRF_SID_C = 64'h0000_0000_0000_0001;
  KL_crf_rx #(
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ)
  ) crf_rx (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .frame_p_i (crf_frame_p_i), .subtype_i (8'h04), .seq_i (crf_seq_i),
    .sid_frame_i (CRF_SID_C), .pullbase_i (32'd48000),
    .fsh_i ({16'd8, 16'd96, crf_ts_i[63:32]}), .fsh2_i ({crf_ts_i[31:0], 32'd0}),
    .type_i (8'd1), .mr_i (crf_mr_i), .tu_i (1'b0), .ptp_now_i (ptp_now_i),
    .en_i (1'b1), .sid_i (CRF_SID_C), .stop_i (1'b0),
    .delta_o (), .rate_o (crf_rate_w), .rate_valid_o (crf_rate_valid_w),
    .pdu_count_o (), .fmt_err_o (), .seq_err_o (), .mr_cnt_o (), .tu_cnt_o (),
    .late_cnt_o (), .early_cnt_o (), .locked_o (crf_locked_w),
    .cnt_locked_o (), .cnt_unlocked_o (), .cnt_intr_o (), .dirty_p_o (),
    .mr_toggle_p_o ()
  );

  // ---------------------------------------------------------------------- //
  // The servo: its silicon loop, the meter_servo_wrap.sv scaling            //
  // ---------------------------------------------------------------------- //
  KL_mmcm_drp_servo #(
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),
    .TICK_CYC_P    (TICK_CYC_P),
    .WIN_LOG2_P    (MCSRV_WIN_LOG2_C),
    .GAIN_NUM_P    (1)
  ) mmcm_servo (
    .clk_i (axis_clk), .rst_n (axis_resetn), .clk_audio_i (clk_audio_i),
    .ps_clk_i (ps_clk_i), .ptp_now_i (ptp_now_i), .phc_slew_active_i (1'b0),
`ifdef FR_MUT_W1
    //! mutation arm W1 (mutants.py): every change of the followed source
    //! drops the select for the one cycle W2 presents the reference unlocked,
    //! so a switch passes servo IDLE and the trim restarts from the plan
    .sel_i (follow_sel_r && !ref_src_chg_w), .ref_locked_i (ref_locked_w),
`else
    .sel_i (follow_sel_r), .ref_locked_i (ref_locked_w),
`endif
    .ref_rate_ns_i (ref_rate_w), .ref_rate_valid_i (ref_rate_valid_w),
    .auto_repair_i (1'b0), .ps_invert_i (1'b0),
    .drp_addr_o (drp_addr_o), .drp_en_o (drp_en_o), .drp_we_o (drp_we_o),
    .drp_di_o (drp_di_o), .drp_do_i (drp_do_i), .drp_rdy_i (drp_rdy_i),
    .mmcm_rst_o (mmcm_rst_o), .mmcm_locked_i (mmcm_locked_i),
    .ps_en_o (ps_en_o), .ps_incdec_o (ps_incdec_o), .ps_done_i (ps_done_i),
    .status_o (servo_status_o), .locked_o (mcsrv_locked_w)
  );

  // ---------------------------------------------------------------------- //
  // The physical frame grid and the packet grid                            //
  // ---------------------------------------------------------------------- //
  //! the physical frame: FRAME_DIV_P audio cycles; the hold stops the divider
  //! where it stands, as a held serial clock stops the TDM master's frame
  logic [$clog2(FRAME_DIV_P)-1:0] fdiv_r;
  logic                           frame_tgl_r;
  logic [1:0]                     ahold_sync_r;
  logic [1:0]                     arst_sync_r;
  always_ff @(posedge clk_audio_i) begin : phys_frame
    arst_sync_r  <= {arst_sync_r[0], rst_n};
    ahold_sync_r <= {ahold_sync_r[0], frame_hold_i};
    if (!arst_sync_r[1]) begin
      fdiv_r      <= '0;
      frame_tgl_r <= 1'b0;
    end else if (!ahold_sync_r[1]) begin
      if (fdiv_r == $bits(fdiv_r)'(FRAME_DIV_P - 1)) begin
        fdiv_r      <= '0;
        frame_tgl_r <= ~frame_tgl_r;
      end else begin
        fdiv_r <= fdiv_r + 1'b1;
      end
    end
  end : phys_frame
  //! into clk_i: two flops and an edge, the frame close's crossing
  logic [2:0] frame_sync_r;
  always_ff @(posedge axis_clk) begin : frame_cdc
    if (!axis_resetn) frame_sync_r <= '0;
    else              frame_sync_r <= {frame_sync_r[1:0], frame_tgl_r};
  end : frame_cdc
  wire frame_ev_w /* verilator public_flat_rd */ = frame_sync_r[2] ^ frame_sync_r[1];

  wire mnco_servo_en_w = mga_sel_w;
  KL_media_nco #(
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),
    .FS_HZ_P       (48_000),
    .TRIMW_P       (18)
  ) media_nco (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .trim_i (18'sd0),
    .servo_trim_i (mnco_servo_trim_w), .servo_en_i (mnco_servo_en_w),
    .tick_o (media_tick_p), .phase_o ()
  );

  KL_media_grid_align #(
    .CLK_FREQ_HZ_P      (MILAN_CLK_FREQ_HZ),
    .FS_HZ_P            (48_000),
    .KP_LOG2_P          (MGA_KP_LOG2_C),
    .KI_LOG2_P          (MGA_KI_LOG2_C),
    .LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C)
  ) media_grid_align (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .sel_i (mga_sel_w), .frame_ev_i (frame_ev_w), .tick_i (media_tick_q_r),
    .u_o (mnco_servo_trim_w), .engaged_o (mga_engaged_w), .err_cyc_o (mga_err_w)
  );

  // ---------------------------------------------------------------------- //
  // The two listener rings, both on STREAM_INPUT 0's payload clone          //
  // ---------------------------------------------------------------------- //
  //! the loopback ring (SLIP_LB): the capture crossbar's LOOP bucket, with
  //! milan_datapath's settle recentre on its one stream
`ifdef FR_MUT_RENDER_ONLY
  //! mutation arm (mutants.py): the settle recentre reaches the render stage
  //! only, so nothing re-centres the loopback ring after a source change
  wire lb_recentre_w = 1'b0;
`else
  wire lb_recentre_w = settle_recentre_p_r;
`endif
  KL_chan_map_capture #(
    .N_SLOTS_P (2), .N_TDM_P (2), .GAP_CYC_P (1),
    .N_LB_STREAMS_P (N_STREAMS), .N_LB_CH_P (RX_CH_P)
  ) chan_map_capture (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .map_wr_en_i (1'b0), .map_wr_addr_i ('0), .map_wr_data_i (13'd0),
    .map_rd_en_i (1'b0), .map_rd_addr_i ('0),
    .map_rd_data_o (), .map_rd_valid_o (), .map_flat_o (),
    .i2s_pair_valid_i (1'b0), .i2s_l_i (24'd0), .i2s_r_i (24'd0),
    .tdm_pair_valid_i (1'b0), .tdm_pair_slot_i (4'd0),
    .tdm_l_i (24'd0), .tdm_r_i (24'd0), .tone_smp_i (24'd0),
    .lb_tdata_i (pcm_tdata_i), .lb_tvalid_i (pcm_tvalid_i),
    .lb_tlast_i (pcm_tlast_i), .lb_tuser_i (4'd0),
    .lb_wire_chans_i (pcm_chans_i), .lb_flush_i (bind_fall_i),
    .lb_recentre_i (lb_recentre_w),
    .tick_i (media_tick_p),
    .pair_valid_o (), .pair_slot_o (), .pair_l_o (), .pair_r_o (),
    .lb_dup_cnt_o (lb_dup_o), .lb_skip_cnt_o (lb_skip_o),
    .tdm_dup_cnt_o (), .tdm_skip_cnt_o ()
  );

  //! the render ring: the #386 setpoint stage, bound as the datapath binds it
  wire [7:0] rsp_fill_w;
  KL_render_setpoint #(
    .N_STREAMS_P (N_STREAMS), .N_CH_P (RX_CH_P), .DEPTH_LOG2_P (5),
    .PDU_EVENTS_P (6), .SETPOINT_EVT_P (8), .CONV_BAND_EVT_P (3),
    .RESET_BAND_EVT_P (6), .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ)
  ) render_setpoint (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_tdata_i (pcm_tdata_i), .s_tvalid_i (pcm_tvalid_i),
    .s_tlast_i (pcm_tlast_i), .s_tuser_i (4'd0), .wire_chans_i (pcm_chans_i),
    .tick_i (media_tick_p), .recentre_p_i (render_recentre_p_w | tb_recentre_p_i),
    .flush_i (bind_fall_i),
    .m_tdata_o (), .m_tvalid_o (), .m_tlast_o (), .m_tuser_o (),
    .m_wire_chans_o (), .render_tick_p_o (),
    .pop_p_o (render_pop_p_o), .fill_o (rsp_fill_w),
    .prefill_o (render_prefill_o), .converged_o (),
    .underruns_o (render_underruns_o), .overruns_o (), .rails_o (render_rails_o),
    .recentres_o (render_recentres_o)
  );
  assign render_fill_o = rsp_fill_w;
  //! the stage's grading instant (#643): the accepted beat with tlast
  assign render_pdu_end_p_o = pcm_tvalid_i && pcm_tlast_i;

endmodule

`default_nettype wire
