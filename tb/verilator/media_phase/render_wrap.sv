// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// A SYNTHETIC clock domain with two RENDER interfaces whose post-grid delays
// differ by a frame (#632, the owner's one-clock, many-interfaces
// requirement, on the listener side). One KL_render_queue serves both from
// the domain's one media event, each interface's read applying its own
// derived out-lead:
//   A  TDM8 x 32 bits, bit clock 12.288 MHz: the domain's frame-timing owner
//      (its capture master's marker is the domain event), rendered by
//      KL_tdm_render_master on A's bus through the crossbar and slot adapter
//      milan_datapath binds: the shipping AX7101 1x1 lane;
//   B  TDM4 x 32 bits, bit clock 6.144 MHz on the same audio clock, rendered
//      the same way, through a one-frame output hold between its crossbar and
//      its adapter (a downstream stage that keeps one frame, as a converter
//      or a DSP block would): its post-grid delay is a frame longer.
// Both crossbars take the queue's beats; A maps stream 0's channels 0..5 to
// its slots 0..5 and stream 2's channels 0..1 to slots 6..7, B maps stream
// 0's channels 0..1 to slots 0..1 and stream 1's channels 0..1 to slots 2..3,
// so stream 0's first two channels reach both interfaces' pins. Each interface's out-lead is derived here from its
// own parameters (KL_media_if_latency_pkg out_pipe_ns and out_lead_frames,
// plus B's hold frame), never measured.
`default_nettype none
module render_wrap #(
  parameter int unsigned CLK_HZ_P   = 50_000_000,
  parameter int unsigned AUD_HZ_P   = 24_576_000,
  parameter int unsigned PAY_LEAD_CYC_P = 16
)(
  input  wire         clk_i,
  input  wire         rst_n,
  input  wire         clk_audio_i,
  input  wire  [63:0] ptp_now_i,
  //! the depacketizer read side the harness plays
  input  wire         hdr_p_i,
  input  wire  [31:0] hdr_ts_ns_i,
  input  wire         hdr_tv_i,
  input  wire  [63:0] s_tdata_i,
  input  wire         s_tvalid_i,
  input  wire         s_tlast_i,
  input  wire  [3:0]  s_tuser_i,
  //! the two crossbars' map write ports
  input  wire         map_a_we_i,
  input  wire  [2:0]  map_a_addr_i,
  input  wire  [7:0]  map_a_data_i,
  input  wire         map_b_we_i,
  input  wire  [1:0]  map_b_addr_i,
  input  wire  [7:0]  map_b_data_i,
  //! the pins
  output wire         a_bclk_o, a_fsync_o, a_dout_o,
  output wire         b_bclk_o, b_fsync_o, b_dout_o,
  //! the queue's verdicts and the derived out-leads
  output wire  [15:0] late_o, early_o, untimed_o, slips_o,
  output wire  [7:0]  a_lead_o, b_lead_o
);
  import KL_media_if_latency_pkg::*;
  localparam int unsigned FS_C = 48_000;
  localparam int unsigned N_STREAMS_C = 3;
  localparam int unsigned N_CH_C = 8;
  localparam int unsigned PAIRS_C = N_CH_C / 2;
  localparam int unsigned KEPT_C = 4;
  localparam int unsigned A_SLOTS_C = 8, B_SLOTS_C = 4;
  localparam longint A_BIT_HZ_C = longint'(A_SLOTS_C) * 32 * FS_C;
  localparam longint B_BIT_HZ_C = longint'(B_SLOTS_C) * 32 * FS_C;
  localparam int A_CLOSE_C = close_pair((A_SLOTS_C / 2 < KEPT_C) ? A_SLOTS_C / 2 : KEPT_C);
  //! the domain event's latency: A's marker, as milan_datapath derives it
  localparam int unsigned A_LAT_C = 32'(mark_lat_ns(pair_end_bits(A_CLOSE_C, 32, 1),
                                                    A_BIT_HZ_C, AUD_HZ_P, 1, CLK_HZ_P));
  //! each interface's out-lead: A is the queue's interface 0, B its 1; B's
  //! hold keeps a frame more
  localparam int unsigned B_HOLD_C = 1;
  localparam longint A_PIPE_C = out_pipe_ns(0, N_STREAMS_C, PAIRS_C, A_SLOTS_C, CLK_HZ_P, AUD_HZ_P, 1'b1);
  localparam longint B_PIPE_C = out_pipe_ns(1, N_STREAMS_C, PAIRS_C, B_SLOTS_C, CLK_HZ_P, AUD_HZ_P, 1'b1);
  localparam int unsigned A_LEAD_C = 32'(out_lead_frames(A_LAT_C, A_PIPE_C, FS_C));
  localparam int unsigned B_LEAD_C = 32'(out_lead_frames(A_LAT_C, B_PIPE_C, FS_C)) + B_HOLD_C;
  if (!out_lead_ok(A_LAT_C, out_pipe_ns(0, N_STREAMS_C, PAIRS_C, A_SLOTS_C, CLK_HZ_P, AUD_HZ_P, 1'b0),
                   A_PIPE_C, FS_C, 50) ||
      !out_lead_ok(A_LAT_C, out_pipe_ns(1, N_STREAMS_C, PAIRS_C, B_SLOTS_C, CLK_HZ_P, AUD_HZ_P, 1'b0),
                   B_PIPE_C, FS_C, 50)) begin : g_lead_guard
    $error("render_wrap: an out-lead straddles a frame start");
  end : g_lead_guard
  assign a_lead_o = 8'(A_LEAD_C);
  assign b_lead_o = 8'(B_LEAD_C);

  //! the two buses' timing owners
  wire       a_pv_w;
  wire [3:0] a_slot_w;
  wire       a_rise_w, a_fall_w, b_rise_w, b_fall_w;
  wire [7:0] a_pos_w;
  wire [6:0] b_pos_w;
  KL_tdm_capture_master #(
    .SLOTS_P (A_SLOTS_C), .WORD_BITS_P (32),
    .BCLK_HALF_P (32'(AUD_HZ_P / (2 * A_BIT_HZ_C))), .DATA_DELAY_P (1'b1)
  ) u_a (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tdm_mclk_o (), .tdm_bclk_o (a_bclk_o), .tdm_fsync_o (a_fsync_o),
    .tdm_data_i (1'b0), .bclk_rise_o (a_rise_w), .bclk_fall_o (a_fall_w), .frame_pos_o (a_pos_w),
    .pair_valid_o (a_pv_w), .pair_slot_o (a_slot_w), .pair_l_o (), .pair_r_o (),
    .pairs_captured_o ()
  );
  KL_tdm_capture_master #(
    .SLOTS_P (B_SLOTS_C), .WORD_BITS_P (32),
    .BCLK_HALF_P (32'(AUD_HZ_P / (2 * B_BIT_HZ_C))), .DATA_DELAY_P (1'b1)
  ) u_b (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tdm_mclk_o (), .tdm_bclk_o (b_bclk_o), .tdm_fsync_o (b_fsync_o),
    .tdm_data_i (1'b0), .bclk_rise_o (b_rise_w), .bclk_fall_o (b_fall_w), .frame_pos_o (b_pos_w),
    .pair_valid_o (), .pair_slot_o (), .pair_l_o (), .pair_r_o (),
    .pairs_captured_o ()
  );

  //! the domain's media event: the owner's frame marker, back-dated
  wire        ev_p_w;
  wire [63:0] ev_ns_w;
  KL_media_domain_event #(
    .MARK_LAT_NS_P (A_LAT_C), .TIMEOUT_CYC_P (4 * (CLK_HZ_P / FS_C))
  ) u_dom (
    .clk_i (clk_i), .rst_n (rst_n),
    .mark_i (a_pv_w && (32'(a_slot_w) == A_CLOSE_C)), .alt_i (1'b0),
    .ptp_ns_i (ptp_now_i), .ev_p_o (ev_p_w), .ev_ns_o (ev_ns_w),
    .mark_ns_o (), .live_o ()
  );

  //! the queue, both interfaces' reads from the one event
  wire [63:0] q_tdata_w;
  wire [1:0]  q_tvalid_w, q_tick_w;
  wire        q_tlast_w;
  wire [3:0]  q_tuser_w;
  wire [N_STREAMS_C*4-1:0] q_chans_w;
  KL_render_queue #(
    .N_STREAMS_P (N_STREAMS_C), .N_CH_P (N_CH_C), .FS_HZ_P (FS_C),
    .MAX_HOLD_NS_P (2_126_000), .EV_LAT_NS_P (A_LAT_C), .N_IF_P (2),
    .IF_LEAD_P ({16'd0, 8'(B_LEAD_C), 8'(A_LEAD_C)}),
    .PAY_LEAD_CYC_P (PAY_LEAD_CYC_P), .CLK_FREQ_HZ_P (CLK_HZ_P)
  ) u_q (
    .clk_i (clk_i), .rst_n (rst_n),
    .hdr_p_i (hdr_p_i), .hdr_ts_ns_i (hdr_ts_ns_i), .hdr_tv_i (hdr_tv_i),
    .s_tdata_i (s_tdata_i), .s_tvalid_i (s_tvalid_i), .s_tlast_i (s_tlast_i),
    .s_tuser_i (s_tuser_i), .wire_chans_i ({N_STREAMS_C{4'd8}}),
    .ev_p_i (ev_p_w), .ev_ns_i (ev_ns_w[31:0]), .flush_i ('0),
    .m_tdata_o (q_tdata_w), .m_tvalid_o (q_tvalid_w), .m_tlast_o (q_tlast_w),
    .m_tuser_o (q_tuser_w), .m_wire_chans_o (q_chans_w), .render_tick_p_o (q_tick_w),
    .pop_p_o (), .lead_o (), .idle_o (), .converged_o (),
    .late_o (late_o), .early_o (early_o), .refused_o (), .untimed_o (untimed_o),
    .slips_o (slips_o)
  );

  //! one crossbar per interface, on its own read's beats and tick
  wire [A_SLOTS_C*24-1:0] a_phys_w;
  wire [B_SLOTS_C*24-1:0] b_phys_w;
  wire                    a_phys_v_w, b_phys_v_w;
  KL_chan_map_render #(.N_STREAMS_P (N_STREAMS_C), .N_CH_P (N_CH_C), .N_PHYS_P (A_SLOTS_C)) u_xa (
    .clk_i (clk_i), .rst_n (rst_n),
    .s_tdata_i (q_tdata_w), .s_tvalid_i (q_tvalid_w[0]), .s_tlast_i (q_tlast_w),
    .s_tuser_i (q_tuser_w), .wire_chans_i (q_chans_w), .tick_i (q_tick_w[0]),
    .map_wr_en_i (map_a_we_i), .map_wr_addr_i (map_a_addr_i), .map_wr_data_i (map_a_data_i),
    .map_rd_addr_i ('0), .map_rd_data_o (), .map_flat_o (),
    .phys_smp_o (a_phys_w), .phys_valid_o (a_phys_v_w), .mapped_mask_o ()
  );
  KL_chan_map_render #(.N_STREAMS_P (N_STREAMS_C), .N_CH_P (N_CH_C), .N_PHYS_P (B_SLOTS_C)) u_xb (
    .clk_i (clk_i), .rst_n (rst_n),
    .s_tdata_i (q_tdata_w), .s_tvalid_i (q_tvalid_w[1]), .s_tlast_i (q_tlast_w),
    .s_tuser_i (q_tuser_w), .wire_chans_i (q_chans_w), .tick_i (q_tick_w[1]),
    .map_wr_en_i (map_b_we_i), .map_wr_addr_i (map_b_addr_i), .map_wr_data_i (map_b_data_i),
    .map_rd_addr_i ('0), .map_rd_data_o (), .map_flat_o (),
    .phys_smp_o (b_phys_w), .phys_valid_o (b_phys_v_w), .mapped_mask_o ()
  );

  //! B's one-frame hold: each frame waits for the next frame's render
  logic [B_SLOTS_C*24-1:0] b_cur_r, b_prev_r;
  logic                    b_hold_v_r;
  always_ff @(posedge clk_i) begin : b_hold
    if (!rst_n) begin
      b_cur_r    <= '0;
      b_prev_r   <= '0;
      b_hold_v_r <= 1'b0;
    end else begin
      b_hold_v_r <= b_phys_v_w;
      if (b_phys_v_w) begin
        b_cur_r  <= b_phys_w;
        b_prev_r <= b_cur_r;
      end
    end
  end : b_hold

  //! each interface's slot adapter, milan_datapath's chmap_tdm_adapter
  logic       a_we_r, a_tick_r, a_busy_r, b_we_r, b_tick_r, b_busy_r;
  logic [2:0] a_slot_r;
  logic [1:0] b_slot_r;
  logic [23:0] a_data_r, b_data_r;
  wire        a_cen_w, b_cen_w;
  always_ff @(posedge clk_i) begin : a_adapter
    if (!rst_n) begin
      a_we_r <= 1'b0; a_slot_r <= '0; a_data_r <= '0; a_tick_r <= 1'b0; a_busy_r <= 1'b0;
    end else begin
      a_we_r   <= 1'b0;
      a_tick_r <= 1'b0;
      if (!a_cen_w) begin
        a_busy_r <= 1'b0;
      end else if (!a_busy_r) begin
        if (a_phys_v_w) begin
          a_busy_r <= 1'b1; a_slot_r <= '0; a_we_r <= 1'b1; a_data_r <= a_phys_w[23:0];
        end
      end else if (32'(a_slot_r) == A_SLOTS_C - 1) begin
        a_busy_r <= 1'b0;
        a_tick_r <= 1'b1;
      end else begin
        a_slot_r <= a_slot_r + 1'b1;
        a_we_r   <= 1'b1;
        a_data_r <= a_phys_w[(32'(a_slot_r) + 1)*24 +: 24];
      end
    end
  end : a_adapter
  always_ff @(posedge clk_i) begin : b_adapter
    if (!rst_n) begin
      b_we_r <= 1'b0; b_slot_r <= '0; b_data_r <= '0; b_tick_r <= 1'b0; b_busy_r <= 1'b0;
    end else begin
      b_we_r   <= 1'b0;
      b_tick_r <= 1'b0;
      if (!b_cen_w) begin
        b_busy_r <= 1'b0;
      end else if (!b_busy_r) begin
        if (b_hold_v_r) begin
          b_busy_r <= 1'b1; b_slot_r <= '0; b_we_r <= 1'b1; b_data_r <= b_prev_r[23:0];
        end
      end else if (32'(b_slot_r) == B_SLOTS_C - 1) begin
        b_busy_r <= 1'b0;
        b_tick_r <= 1'b1;
      end else begin
        b_slot_r <= b_slot_r + 1'b1;
        b_we_r   <= 1'b1;
        b_data_r <= b_prev_r[(32'(b_slot_r) + 1)*24 +: 24];
      end
    end
  end : b_adapter

  //! the serializers, each on its own bus's exported timing
  KL_tdm_render_master #(.SLOTS_P (A_SLOTS_C), .SLOT_BITS_P (32), .FIFO_LOG2_P (2), .FRAME_POS_W_P (8)) u_ra (
    .clk_i (clk_i), .rst_n (rst_n),
    .smp_wr_en_i (a_we_r), .smp_wr_slot_i (a_slot_r), .smp_wr_data_i (a_data_r), .tick_i (a_tick_r),
    .epoch_evt_i (1'b0), .fresh_i (1'b1), .commit_en_o (a_cen_w),
    .clk_tdm_i (clk_audio_i), .bclk_rise_i (a_rise_w), .bclk_fall_i (a_fall_w), .frame_pos_i (a_pos_w),
    .tdm_dout_o (a_dout_o), .frame_start_o (), .adopt_p_o (),
    .frames_o (), .underruns_o (), .skips_o (), .overruns_o (), .epochs_o ()
  );
  KL_tdm_render_master #(.SLOTS_P (B_SLOTS_C), .SLOT_BITS_P (32), .FIFO_LOG2_P (2), .FRAME_POS_W_P (7)) u_rb (
    .clk_i (clk_i), .rst_n (rst_n),
    .smp_wr_en_i (b_we_r), .smp_wr_slot_i (b_slot_r), .smp_wr_data_i (b_data_r), .tick_i (b_tick_r),
    .epoch_evt_i (1'b0), .fresh_i (1'b1), .commit_en_o (b_cen_w),
    .clk_tdm_i (clk_audio_i), .bclk_rise_i (b_rise_w), .bclk_fall_i (b_fall_w), .frame_pos_i (b_pos_w),
    .tdm_dout_o (b_dout_o), .frame_start_o (), .adopt_p_o (),
    .frames_o (), .underruns_o (), .skips_o (), .overruns_o (), .epochs_o ()
  );
endmodule
`default_nettype wire
