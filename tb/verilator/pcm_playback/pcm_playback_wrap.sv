/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness: the WHOLE item-7 playback chain, wired exactly as
//! hdl/milan/milan_datapath.sv wires it -
//!
//!   host PCM ring (C++ model on the mem_* word-fetch port)
//!     -> KL_pcm_tx        de-interleave + media-clock pace
//!     -> KL_chan_map_render  playback latch + map (src = 1) -> phys{0,1}
//!     -> KL_i2s_feed_mux  source + PACE select (media tick), LPF masked
//!     -> KL_i2s_playback  producer FIFO -> CDC -> Philips I2S serializer
//!     -> i2s_sdin_o       the DAC pin
//!
//! - the mirror of the PROVEN record path (AVTP RX -> depacketizer ->
//! KL_pcm_ring_bram -> DMA -> ALSA capture), in the direction that was
//! never continuous in fabric. The sim_main writes host ring words and
//! decodes the serial DAC output with a standard-derived I2S receiver, so
//! the claim it makes is byte-in = bit-out.
//!
//! The media tick divider is a copy of milan_datapath's chmap_media_tick
//! (same divisor for KL_pcm_tx's internal pace, exactly as the datapath
//! elaborates PB_SAMPLE_DIV_C == MEDIA_TICK_DIV_C), and the legacy listener
//! render tap is exposed too so the DEFAULT (chmap disarmed) path can be
//! proven unchanged in the same harness.

`default_nettype none

module pcm_playback_wrap #(
  parameter int unsigned N_STREAMS_P  = 2,          //! playback streams
  parameter int unsigned TICK_DIV_P   = 64,         //! clk cycles per 48 kHz
                                                    //! media frame (sim-fast)
  parameter int unsigned N_PHYS_P     = 10,         //! physical render outs
  parameter int          CLK_FREQ_HZ_P = 49_152_000,//! clk_i frequency
  parameter int          PREFILL_P    = 4,          //! DAC prefill release
  parameter int          SETPOINT_P   = 0           //! task #28 fill target
                                                    //! (0 = legacy midpoint)
)(
  input  wire        clk,               //! datapath clock
  input  wire        clk_audio,         //! clean audio clock (MMCM)
  input  wire        rst_n,

  //! --- playback engine control (the migen playback CSR block) ------------
  input  wire        pb_enable_i,
  input  wire [N_STREAMS_P-1:0] pb_stream_en_i,
  input  wire        pb_underrun_silence_i,
  input  wire [31:0] pb_ring_len_i,
  input  wire [31:0] pb_ring_stride_i,
  input  wire [N_STREAMS_P*32-1:0] pb_wr_ptr_i,

  //! --- host ring word fetch (the SoC's DRAM read shim, modelled in C++) --
  output wire [31:0] mem_addr_o,
  output wire        mem_rd_o,
  input  wire [63:0] mem_data_i,
  input  wire        mem_valid_i,

  //! --- chmap fabric (CHMAP_CTRL 0x900 + the map write port) --------------
  input  wire        chmap_enable_i,    //! CHMAP_CTRL[0] = feed-mux select
  input  wire        map_wr_en_i,
  input  wire [3:0]  map_wr_addr_i,
  input  wire [7:0]  map_wr_data_i,     //! {en[7], src[6], idx[5:0]}

  //! --- legacy listener render tap (the compliance path, for the bypass leg) ----
  input  wire [63:0] tap_tdata_i,
  input  wire        tap_tvalid_i,
  input  wire        tap_tready_i,
  input  wire        tap_tlast_i,
  input  wire [7:0]  tap_chans_i,
  input  wire        lpf_active_i,

  //! --- DAC pins ----------------------------------------------------------
  output wire        i2s_mclk_o,
  output wire        i2s_sclk_o,
  output wire        i2s_lrck_o,
  output wire        i2s_sdin_o,

  //! --- observability (the PBK 0x8C8 group + the engine rails) ------------
  output wire [N_STREAMS_P*32-1:0] pb_rd_ptr_o,
  output wire [N_STREAMS_P*16-1:0] pb_underrun_o,
  output wire [N_STREAMS_P*16-1:0] pb_overrun_o,
  output wire        pb_playing_o,
  output wire [31:0] feeds_o,
  output wire [15:0] unarmed_o,
  output wire        src_render_o,
  output wire        feed_lpf_active_o, //! the LPF override AS SEEN by the DAC
  output wire [7:0]  feed_chans_o,      //! the walker stride the DAC is given
  output wire [N_PHYS_P-1:0]     pb_mask_o,
  output wire [N_PHYS_P-1:0]     mapped_mask_o,
  output wire [N_PHYS_P*24-1:0]  phys_smp_o,
  output wire        phys_valid_o,
  output wire [15:0] i2s_underruns_o,
  output wire [15:0] i2s_overruns_o,
  input  wire        recenter_p_i,      //! task #22 drill: GM-step snap
  output wire        converged_o,
  output wire        media_reset_p_o,
  output wire [15:0] i2s_fill_o
);

  // ---- 48 kHz media grid (copy of milan_datapath chmap_media_tick) --------
  logic [$clog2(TICK_DIV_P)-1:0] tick_cnt_r;
  logic                          media_tick_p;

  always_ff @(posedge clk) begin : media_tick
    if (!rst_n) begin
      tick_cnt_r   <= '0;
      media_tick_p <= 1'b0;
    end
    else if (32'(tick_cnt_r) == TICK_DIV_P - 1) begin
      tick_cnt_r   <= '0;
      media_tick_p <= 1'b1;
    end
    else begin
      tick_cnt_r   <= tick_cnt_r + 1'b1;
      media_tick_p <= 1'b0;
    end
  end : media_tick

  // ---- host PCM ring -> AAF pair stream ----------------------------------
  wire        pb_pv_w;
  wire [3:0]  pb_slot_w;
  wire [23:0] pb_l_w, pb_r_w;

  KL_pcm_tx #(
    .N_STREAMS_P   (N_STREAMS_P),
    .CHANS_P       (2),                 //! stereo pair stream (the NxN shape)
    .SAMPLE_DIV_C  (TICK_DIV_P),        //! datapath: PB_SAMPLE_DIV_C == tick
    .USE_EXT_TICK_P(1'b0)
  ) u_pcm_tx (
    .clk_i (clk), .rst_n (rst_n),
    .enable_i (pb_enable_i), .stream_en_i (pb_stream_en_i),
    .underrun_silence_i (pb_underrun_silence_i),
    .ring_base_i (64'd0), .ring_len_i (pb_ring_len_i),
    .ring_stride_i (pb_ring_stride_i), .wr_ptr_i (pb_wr_ptr_i),
    .smp_tick_i (1'b0),
    .mem_addr_o (mem_addr_o), .mem_rd_o (mem_rd_o),
    .mem_data_i (mem_data_i), .mem_valid_i (mem_valid_i),
    .pair_valid_o (pb_pv_w), .pair_slot_o (pb_slot_w),
    .pair_l_o (pb_l_w), .pair_r_o (pb_r_w),
    .rd_ptr_o (pb_rd_ptr_o), .underrun_o (pb_underrun_o),
    .overrun_o (pb_overrun_o), .smp_tick_o (), .playing_o (pb_playing_o)
  );

  // ---- render crossbar: the playback latch + the map ---------------------
  wire [N_PHYS_P*24-1:0] phys_w;
  wire                   phys_v_w;

  KL_chan_map_render #(
    .N_STREAMS_P  (N_STREAMS_P),
    .N_CH_P       (8),
    .N_PHYS_P     (N_PHYS_P),
    .N_PB_SLOTS_P (N_STREAMS_P)
  ) u_render (
    .clk_i (clk), .rst_n (rst_n),
    //! no AVB listener traffic in this harness: the playback source is the
    //! whole point, and a silent RX side is the honest field condition
    .s_tdata_i (64'd0), .s_tvalid_i (1'b0), .s_tlast_i (1'b0),
    .s_tuser_i (4'd0), .wire_chans_i ('0),
    .pb_valid_i (pb_pv_w), .pb_slot_i (pb_slot_w),
    .pb_l_i (pb_l_w), .pb_r_i (pb_r_w),
    .tick_i (media_tick_p),
    .map_wr_en_i (map_wr_en_i),
    .map_wr_addr_i (map_wr_addr_i[$clog2(N_PHYS_P)-1:0]),
    .map_wr_data_i (map_wr_data_i),
    .map_rd_addr_i ('0), .map_rd_data_o (),
    .phys_smp_o (phys_w), .phys_valid_o (phys_v_w),
    .mapped_mask_o (mapped_mask_o), .pb_mask_o (pb_mask_o)
  );

  assign phys_smp_o   = phys_w;
  assign phys_valid_o = phys_v_w;

  // ---- DAC feed selector (source AND pace) -------------------------------
  wire [63:0] feed_tdata_w;
  wire        feed_tvalid_w, feed_tready_w, feed_tlast_w, feed_lpf_w;
  wire [7:0]  feed_chans_w;

  KL_i2s_feed_mux u_feed (
    .clk_i (clk), .rst_n (rst_n),
    .sel_render_i (chmap_enable_i),
    .tap_tdata_i (tap_tdata_i), .tap_tvalid_i (tap_tvalid_i),
    .tap_tready_i (tap_tready_i), .tap_tlast_i (tap_tlast_i),
    .tap_chans_i (tap_chans_i), .lpf_active_i (lpf_active_i),
    .phys_l_i (phys_w[0*24 +: 24]), .phys_r_i (phys_w[1*24 +: 24]),
    .phys_valid_i (phys_v_w),
    .phys_armed_i (|mapped_mask_o[1:0]),
    .pcm_tdata_o (feed_tdata_w), .pcm_tvalid_o (feed_tvalid_w),
    .pcm_tready_o (feed_tready_w), .pcm_tlast_o (feed_tlast_w),
    .chans_o (feed_chans_w), .lpf_active_o (feed_lpf_w),
    .feeds_o (feeds_o), .unarmed_o (unarmed_o), .src_render_o (src_render_o)
  );

  assign feed_lpf_active_o = feed_lpf_w;
  assign feed_chans_o      = feed_chans_w;

  // ---- the DAC ------------------------------------------------------------
  KL_i2s_playback #(
    .MCLK_DIV_LOG2 (2),
    .CLK_FREQ_HZ   (CLK_FREQ_HZ_P),
    .PREFILL_C     (PREFILL_P),
    .SETPOINT_P    (SETPOINT_P)
  ) u_dac (
    .clk_i (clk), .rst_n (rst_n),
    .recenter_p_i (recenter_p_i),
    .clk_audio_i (clk_audio),
    .servo_en_i (1'b0),
    .pcm_tdata_i (feed_tdata_w),
    //! the LPF instance itself is out of this harness's scope; what matters
    //! is that the feed mux MASKS its override in render mode (defect 2) -
    //! lpf_tvalid is held so an unmasked override would starve the DAC and
    //! the bit-exact leg would fail loudly instead of silently
    .lpf_tdata_i (64'd0), .lpf_tvalid_i (1'b0),
    .lpf_active_i (feed_lpf_w),
    .pcm_tvalid_i (feed_tvalid_w),
    .pcm_tready_i (feed_tready_w),
    .pcm_tlast_i (feed_tlast_w),
    .wire_chans_i (feed_chans_w),
    .i2s_mclk_o (i2s_mclk_o), .i2s_sclk_o (i2s_sclk_o),
    .i2s_lrck_o (i2s_lrck_o), .i2s_sdin_o (i2s_sdin_o),
    .clr_under_i (1'b0), .clr_over_i (1'b0),
    .underruns_o (i2s_underruns_o), .overruns_o (i2s_overruns_o),
    .trim_o (), .fill_o (i2s_fill_o),
    .media_reset_p_o (media_reset_p_o), .converged_o (converged_o),
    .dbg_frame_o ()
  );

endmodule

`default_nettype wire
