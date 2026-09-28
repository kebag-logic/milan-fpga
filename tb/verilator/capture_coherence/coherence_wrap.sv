/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness wrapper for the TDM capture junction (#617): the real
//! front end, the real media grid and the real crossbar and packetizer,
//! bound as milan_datapath binds them on the shipping AX7101 1x1 TDM8 shape.
//!
//!   KL_tdm_capture_master  the TDM8 bus MASTER (milan_datapath g_solo arm):
//!                          bclk/fsync out, tdm_data_i in, the {slot, L, R}
//!                          pair stream in clk
//!   KL_media_nco           the packet grid media_tick_p (INTERNAL free-run)
//!   KL_media_grid_align    the #74 aligner: under a CRF selection it steers
//!                          the NCO onto the front end's slot-0 marker
//!   KL_chan_map_capture    THE DEVICE UNDER TEST: the TDM bucket and the
//!                          media-tick walk
//!   KL_aaf_packetizer      one 8-channel talker, the AAF PDUs on AXIS
//!
//! The C++ side is the SoC: it reads bclk/fsync at the pins and shifts the
//! #451 pattern into tdm_data_i, then decodes every AAF sample column the
//! packetizer emits. The oracle is the PDU on the AXIS port; the pair taps
//! below time the frames and the walks and are never the verdict on their
//! own.
//!
//! Shape constants arrive as parameters from the Makefile, which hands the
//! same numbers to the harness as -D values, so the two cannot drift.

`default_nettype none

module coherence_wrap #(
  parameter int unsigned CLK_HZ_P       = 50_000_000, //! axis clock (Hz)
  parameter int unsigned N_TALKERS_P    = 1,          //! talker streams
  parameter int unsigned WIRE_CHANS_P   = 8,          //! channels per talker
  parameter int unsigned TDM_SLOTS_P    = 8,          //! TDM slots per frame
  parameter int unsigned LB_STREAMS_P   = 1,          //! LOOP bucket streams
  parameter int unsigned LB_CH_P        = 8           //! LOOP bucket channels
)(
  input  wire         clk,             //! axis clock (milan domain)
  input  wire         clk_tdm,         //! TDM master clock (clk_tdm_i)
  input  wire         rst_n,           //! active-low synchronous reset

  //! the resolved clock-source verdict (milan_datapath crf_clk_selected_r):
  //! 0 = INTERNAL, the grid free-runs; 1 = CRF, the aligner steers it
  input  wire         sel_crf_i,

  //! --- TDM pins (the SoC model drives data and reads the clocks) --------
  output wire         tdm_bclk_o,
  output wire         tdm_fsync_o,
  input  wire         tdm_data_i,

  //! --- capture map write port (per-channel 13-bit entry) ----------------
  input  wire         map_wr_en_i,
  input  wire [$clog2(2*N_TALKERS_P*4)-1:0] map_wr_addr_i,
  input  wire [12:0]  map_wr_data_i,

  //! --- talker admission --------------------------------------------------
  input  wire [N_TALKERS_P-1:0] stream_en_i,

  //! --- timing taps (the frames entering, the grid, the walk leaving) ----
  output wire         tick_o,          //! media_tick_p
  output wire         engaged_o,       //! aligner reference captured
  output wire         cap_pv_o,        //! front-end pair strobe
  output wire [3:0]   cap_slot_o,      //! its TDM pair index
  output wire [23:0]  cap_l_o,
  output wire [23:0]  cap_r_o,
  output wire         walk_pv_o,       //! crossbar inject strobe
  output wire [4:0]   walk_slot_o,
  output wire [23:0]  walk_l_o,
  output wire [23:0]  walk_r_o,
  output wire [15:0]  tdm_dup_cnt_o,   //! the shipped junction counters
  output wire [15:0]  tdm_skip_cnt_o,

  //! --- the talker's AAF PDUs ---------------------------------------------
  output wire [63:0]  tdata_o,
  output wire [7:0]   tkeep_o,
  output wire         tvalid_o,
  output wire         tlast_o
);

  localparam int unsigned N_SLOTS_C  = N_TALKERS_P * 4;
  localparam int unsigned FS_HZ_C    = 48_000;
  localparam int unsigned WORD_BITS_C = 32;

  // ---------------------------------------------------------------------- //
  //  Front end: the TDM master, bound as milan_datapath's g_solo arm        //
  // ---------------------------------------------------------------------- //
  wire        cap_pv_w;
  wire [3:0]  cap_slot_w;
  wire [23:0] cap_l_w, cap_r_w;

  KL_tdm_capture_master #(
    .SLOTS_P      (TDM_SLOTS_P),
    .WORD_BITS_P  (WORD_BITS_C),
    .BCLK_HALF_P  (1),
    .DATA_DELAY_P (1'b1)
  ) u_front (
    .clk_i (clk), .rst_n (rst_n),
    .clk_audio_i (clk_tdm),
    .tdm_mclk_o (), .tdm_bclk_o (tdm_bclk_o),
    .tdm_fsync_o (tdm_fsync_o), .tdm_data_i (tdm_data_i),
    .bclk_rise_o (), .bclk_fall_o (), .frame_pos_o (),
    .pair_valid_o (cap_pv_w), .pair_slot_o (cap_slot_w),
    .pair_l_o (cap_l_w), .pair_r_o (cap_r_w),
    .pairs_captured_o ()
  );

  assign cap_pv_o   = cap_pv_w;
  assign cap_slot_o = cap_slot_w;
  assign cap_l_o    = cap_l_w;
  assign cap_r_o    = cap_r_w;

  // ---------------------------------------------------------------------- //
  //  Packet grid: the NCO, steered by the aligner only under CRF (#74)      //
  // ---------------------------------------------------------------------- //
  wire               tick_w;
  wire signed [15:0] u_w;

  KL_media_nco #(
    .CLK_FREQ_HZ_P (CLK_HZ_P),
    .FS_HZ_P       (FS_HZ_C),
    .TRIMW_P       (18)
  ) u_nco (
    .clk_i (clk), .rst_n (rst_n),
    .trim_i (18'sd0),
    .servo_trim_i (u_w),
    .servo_en_i (sel_crf_i),
    .tick_o (tick_w),
    .phase_o ()
  );

  KL_media_grid_align #(
    .CLK_FREQ_HZ_P (CLK_HZ_P),
    .FS_HZ_P       (FS_HZ_C)
  ) u_align (
    .clk_i (clk), .rst_n (rst_n),
    .sel_i (sel_crf_i),
    .frame_ev_i (cap_pv_w && (cap_slot_w == 4'd0)),
    .tick_i (tick_w),
    .u_o (u_w),
    .engaged_o (engaged_o),
    .err_cyc_o ()
  );

  assign tick_o = tick_w;

  // ---------------------------------------------------------------------- //
  //  The capture crossbar under test, fed as milan_datapath feeds it: the   //
  //  one front-end pair stream on both the I2S and the TDM ports            //
  // ---------------------------------------------------------------------- //
  wire        walk_pv_w;
  wire [4:0]  walk_slot_w;
  wire [23:0] walk_l_w, walk_r_w;

  KL_chan_map_capture #(
    .N_SLOTS_P      (N_SLOTS_C),
    .N_TDM_P        (8),
    //! milan_datapath's CMAP_TDM_FRAME_PAIRS_C on a solo TDM master: the
    //! front end's TDM_SLOTS_P/2 pairs, all kept by the 4-pair bucket
    .TDM_FRAME_PAIRS_P (TDM_SLOTS_P / 2),
    .N_LB_STREAMS_P (LB_STREAMS_P),
    .N_LB_CH_P      (LB_CH_P)
  ) u_xbar (
    .clk_i (clk), .rst_n (rst_n),
    .map_wr_en_i (map_wr_en_i), .map_wr_addr_i (map_wr_addr_i),
    .map_wr_data_i (map_wr_data_i),
    .map_rd_en_i (1'b0), .map_rd_addr_i ('0),
    .map_rd_data_o (), .map_rd_valid_o (), .map_flat_o (),
    .i2s_pair_valid_i (cap_pv_w), .i2s_l_i (cap_l_w), .i2s_r_i (cap_r_w),
    .tdm_pair_valid_i (cap_pv_w), .tdm_pair_slot_i (cap_slot_w),
    .tdm_l_i (cap_l_w), .tdm_r_i (cap_r_w),
    .tone_smp_i (24'd0),
    .tick_i (tick_w),
    .pair_valid_o (walk_pv_w), .pair_slot_o (walk_slot_w),
    .pair_l_o (walk_l_w), .pair_r_o (walk_r_w),
    .lb_dup_cnt_o (), .lb_skip_cnt_o (),
    .tdm_dup_cnt_o (tdm_dup_cnt_o), .tdm_skip_cnt_o (tdm_skip_cnt_o)
  );

  assign walk_pv_o   = walk_pv_w;
  assign walk_slot_o = walk_slot_w;
  assign walk_l_o    = walk_l_w;
  assign walk_r_o    = walk_r_w;

  // ---------------------------------------------------------------------- //
  //  The talker: one 8-channel AAF stream on the shared packetizer          //
  // ---------------------------------------------------------------------- //
  KL_aaf_packetizer #(
    .N_TALKERS_P  (N_TALKERS_P),
    .WIRE_CHANS_P (WIRE_CHANS_P)
  ) u_pkt (
    .clk_i (clk), .rst_n (rst_n),
    .pair_valid_i (walk_pv_w), .pair_slot_i (walk_slot_w),
    .pair_l_i (walk_l_w), .pair_r_i (walk_r_w),
    .stream_en_i (stream_en_i),
    .dest_mac_i (48'h91E0F000FE01), .station_mac_i (48'h020000000002),
    .vlan_vid_i (12'd2), .vlan_pcp_i (3'd3), .dom_ovr_i (1'b0),
    .transit_ns_i ({N_TALKERS_P{32'd2_000_000}}),
    .ptp_ns_i (64'd0),
    .ts_uncertain_i (1'b0),
    .mr_i ('0),
    .tctx_wr_en_i (1'b0), .tctx_wr_addr_i (7'd0), .tctx_wr_data_i (32'd0),
    .tctx_wr_rdy_o (),
    .tctx_rd_en_i (1'b0), .tctx_rd_addr_i (7'd0),
    .tctx_rd_data_o (), .tctx_rd_valid_o (),
    .m_axis_tdata (tdata_o), .m_axis_tkeep (tkeep_o),
    .m_axis_tvalid (tvalid_o), .m_axis_tlast (tlast_o),
    .m_axis_tready (1'b1),
    .frames_sent_o (),
    .frame_p_o (), .frame_idx_o (), .frame_tu_o (), .frame_mr_o ()
  );

endmodule

`default_nettype wire
