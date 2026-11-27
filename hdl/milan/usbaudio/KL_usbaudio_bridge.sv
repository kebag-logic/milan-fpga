// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Fixed 8x8 bridge. Session reset owns every parser, queue and clock crossing.
// State and PCM cross atomically; independent epochs fence their own direction.
`default_nettype none
module KL_usbaudio_bridge #(
  parameter int unsigned BUS_HZ_P = 50_000_000, //! bus clock frequency
  parameter int unsigned WINDOW_LOG2_P = 13, //! selected USB measurement window
  parameter logic [15:0] DIGEST_P = 16'h84ff //! pinned eight-channel profile
)(
  input wire bus_clk_i, //! GPIF scheduler clock
  input wire media_clk_i, //! datapath clock
  input wire oscillator_clk_i, //! actual gPTP-disciplined 24.576 MHz oscillator
  input wire reset_i, //! common session reset, asynchronous assertion
  input wire media_locked_i, //! media-domain clock health
  input wire latency_qualified_i, //! bus-domain physical qualification latch
  input wire rx_valid_i, //! socket three word
  output wire rx_ready_o, //! keep reading inactive streams too
  input wire [15:0] rx_data_i, //! little-endian received word
  output wire capture_valid_o, //! socket zero word
  input wire capture_ready_i, //! socket zero accepted word
  output wire [15:0] capture_data_o, //! little-endian PCM
  output wire capture_last_o, //! final interval word
  output wire capture_abort_o, //! abandon old capture interval at epoch boundary
  output wire status_valid_o, //! socket one word
  input wire status_ready_i, //! socket one accepted word
  output wire [15:0] status_data_o, //! exact twenty-byte status
  output wire status_last_o, //! final status word
  input wire media_tick_i, //! media frame grid
  input wire [31:0] media_ns_i, //! current media-frame instant
  input wire [63:0] render_data_i, //! render queue pair
  input wire render_valid_i, //! render queue accepted beat
  input wire render_last_i, //! end of stream frame
  input wire [3:0] render_stream_i, //! stream identity
  input wire render_tick_i, //! presentation-stage frame complete
  output wire pair_valid_o, //! whole-frame playback pair walk
  output wire [3:0] pair_slot_o, //! logical channel pair
  output wire [31:0] pair_l_o, //! complete left subslot
  output wire [31:0] pair_r_o, //! complete right subslot
  output wire [31:0] frame_ns_o, //! playback frame instant
  output wire capture_tick_o, //! capture-mapper snapshot after pair three
  output wire locked_o, //! fully qualified feedback
  output wire [31:0] feedback_q16_o, //! measured feedback
  output logic error_o, //! sticky error until session reset
  output logic [31:0] playback_drops_o, //! whole frames refused by full queue
  output wire [31:0] playback_gaps_o, //! whole playback gaps on media grid
  output wire [31:0] capture_drops_o, //! whole render frames refused by crossing
  output wire [31:0] reference_losses_o, //! rejected reference windows
  output wire [31:0] rejected_records_o, //! malformed playback/state records
  output wire [31:0] digest_errors_o, //! playback/state profile mismatches
  output wire [31:0] media_frames_o, //! media-domain grid count
  output wire [13:0] playback_extremes_o, //! media-domain maximum/minimum FIFO level
  output wire [13:0] capture_extremes_o //! bus-domain maximum/minimum FIFO level
);
  if (BUS_HZ_P < 8000 || BUS_HZ_P % 1000 != 0 || WINDOW_LOG2_P < 4
      || WINDOW_LOG2_P > 16 || DIGEST_P != 16'h84ff) begin : parameter_guard
    $error("AUDIO_PARAMETER_BRIDGE: clock must be whole kHz, window 4..16, and profile 84ff");
  end : parameter_guard
  wire bus_rst_n_w, media_rst_n_w, oscillator_rst_n_w;
  KL_usbaudio_reset bus_reset (.clk_i(bus_clk_i), .reset_i(reset_i), .rst_n(bus_rst_n_w));
  KL_usbaudio_reset media_reset (.clk_i(media_clk_i), .reset_i(reset_i), .rst_n(media_rst_n_w));
  KL_usbaudio_reset oscillator_reset (.clk_i(oscillator_clk_i), .reset_i(reset_i), .rst_n(oscillator_rst_n_w));
  wire [47:0] ticks_w;
  KL_usbaudio_clock clock_stamp (
    .media_clk_i(oscillator_clk_i), .media_rst_n(oscillator_rst_n_w),
    .bus_clk_i(bus_clk_i), .bus_rst_n(bus_rst_n_w), .ticks_o(ticks_w)
  );
  (* ASYNC_REG = "TRUE" *) logic [1:0] lock_r, error_r;
  wire media_error_w;
  wire [1:0] media_running_w;
  logic [2:0] media_levels_r;
  // Decoded levels may glitch as their source flops settle. Launch only
  // registered levels into the independent bus-domain synchronizers.
  always_ff @(posedge media_clk_i) begin : launch_status_levels
    if (!media_rst_n_w) media_levels_r <= 0;
    else media_levels_r <= {media_locked_i, media_running_w};
  end : launch_status_levels
  (* ASYNC_REG = "TRUE" *) logic [1:0] running_meta_r, running_sync_r;
  always_ff @(posedge bus_clk_i) begin : status_levels
    if (!bus_rst_n_w) begin
      lock_r <= 0;
      error_r <= 0;
      running_meta_r <= 0;
      running_sync_r <= 0;
    end else begin
      lock_r <= {lock_r[0], media_levels_r[2]};
      error_r <= {error_r[0], media_error_w};
      running_meta_r <= media_levels_r[1:0];
      running_sync_r <= running_meta_r;
    end
  end : status_levels
  wire record_valid_w, record_ready_w, reference_w, malformed_w, discontinuity_w;
  wire [31:0] playback_epoch_w, capture_epoch_w, sequence_w, rejected_w, digest_errors_w;
  assign rejected_records_o = rejected_w;
  assign digest_errors_o = digest_errors_w;
  wire [2:0] flags_w, frames_w;
  wire [1791:0] pcm_w;
  wire [13:0] count_w;
  wire [12:0] delta_w;
  wire [47:0] stamp_w;
  wire accepted_reference_w;
  KL_usbaudio_ingress #(.DIGEST_P(DIGEST_P)) ingress (
    .clk_i(bus_clk_i), .rst_n(bus_rst_n_w), .valid_i(rx_valid_i), .ready_o(rx_ready_o),
    .data_i(rx_data_i), .media_ticks_i(ticks_w), .record_valid_o(record_valid_w),
    .record_ready_i(record_ready_w), .playback_epoch_o(playback_epoch_w),
    .capture_epoch_o(capture_epoch_w), .flags_o(flags_w), .frames_o(frames_w),
    .pcm_o(pcm_w), .reference_p_o(reference_w), .loss_p_o(malformed_w),
    .count_o(count_w), .sequence_o(sequence_w), .delta_usb_cycles_o(delta_w),
    .discontinuity_o(discontinuity_w), .stamp_ticks_o(stamp_w),
    .rejected_o(rejected_w), .digest_errors_o(digest_errors_w)
  );
  KL_usbaudio_reference #(.BUS_HZ_P(BUS_HZ_P), .WINDOW_LOG2_P(WINDOW_LOG2_P)) reference_clock (
    .clk_i(bus_clk_i), .rst_n(bus_rst_n_w), .media_locked_i(lock_r[1]),
    .latency_qualified_i(latency_qualified_i), .reference_i(reference_w),
    .malformed_i(malformed_w), .count_i(count_w), .sequence_i(sequence_w),
    .delta_usb_cycles_i(delta_w), .discontinuity_i(discontinuity_w), .stamp_ticks_i(stamp_w),
    .locked_o(locked_o), .feedback_samples_q16_o(feedback_q16_o), .losses_o(reference_losses_o),
    .accepted_o(accepted_reference_w)
  );
  logic applying_r;
  logic [2:0] frame_r;
  logic [31:0] bus_capture_epoch_r, bus_playback_epoch_r;
  logic [2:0] bus_flags_r;
  wire state_ready_w;
  wire [31:0] packet_gaps_w, abandoned_w;
  wire changed_w = capture_epoch_w != bus_capture_epoch_r
      || playback_epoch_w != bus_playback_epoch_r || flags_w != bus_flags_r;
  wire state_valid_w = record_valid_w && !applying_r && changed_w;
  wire apply_w = record_valid_w && !applying_r && (!changed_w || state_ready_w);
  assign capture_abort_o = apply_w && capture_epoch_w != bus_capture_epoch_r;
  assign record_ready_w = applying_r && frame_r == frames_w;
  wire pcm_valid_w = applying_r && frame_r < frames_w;
  wire pcm_ready_w;
  always_ff @(posedge bus_clk_i) begin : record_application
    if (!bus_rst_n_w) begin
      applying_r <= 0;
      frame_r <= 0;
      bus_capture_epoch_r <= 0;
      bus_playback_epoch_r <= 0;
      bus_flags_r <= 0;
      playback_drops_o <= 0;
      error_o <= 0;
    end else begin
      if (apply_w) begin
        applying_r <= 1;
        frame_r <= 0;
        bus_capture_epoch_r <= capture_epoch_w;
        bus_playback_epoch_r <= playback_epoch_w;
        bus_flags_r <= flags_w;
      end
      if (pcm_valid_w) begin
        frame_r <= frame_r+1'b1;
        // The record must drain even with a stopped media reader, so a full
        // frame is refused and counted instead of wedging state/reference.
        if (!pcm_ready_w) begin
          error_o <= 1;
          if (playback_drops_o != 32'hffffffff) playback_drops_o <= playback_drops_o+1'b1;
        end
      end
      if (record_ready_w) applying_r <= 0;
      if (error_r[1] || rejected_w != 0 || digest_errors_w != 0
          || packet_gaps_w != 0) error_o <= 1;
    end
  end : record_application
  wire [66:0] media_state_w;
  wire media_state_valid_w, media_state_ready_w;
  KL_usbaudio_crossing #(.WIDTH_P(67), .DEPTH_P(4)) state_crossing (
    .s_clk_i(bus_clk_i), .s_rst_n(bus_rst_n_w),
    .data_i({capture_epoch_w, playback_epoch_w, flags_w}),
    .valid_i(state_valid_w), .ready_o(state_ready_w), .m_clk_i(media_clk_i),
    .m_rst_n(media_rst_n_w), .data_o(media_state_w), .valid_o(media_state_valid_w),
    .ready_i(media_state_ready_w), .level_o() // handshake alone controls state flow
  );
  wire [287:0] playback_w, capture_w, bus_capture_w;
  wire playback_valid_w, playback_ready_w, capture_valid_w, capture_ready_w;
  wire bus_capture_valid_w, bus_capture_ready_w;
  wire [6:0] playback_level_w, capture_level_w;
  logic [6:0] capture_minimum_r, capture_maximum_r;
  assign capture_extremes_o = {capture_maximum_r, capture_minimum_r};
  always_ff @(posedge bus_clk_i) begin : capture_levels
    if (!bus_rst_n_w) begin
      capture_minimum_r <= 7'h7f;
      capture_maximum_r <= 0;
    end else if (bus_capture_valid_w && bus_flags_r[2] && locked_o) begin
      if (capture_level_w < capture_minimum_r) capture_minimum_r <= capture_level_w;
      if (capture_level_w > capture_maximum_r) capture_maximum_r <= capture_level_w;
    end
  end : capture_levels
  KL_usbaudio_crossing playback_crossing (
    .s_clk_i(bus_clk_i), .s_rst_n(bus_rst_n_w),
    .data_i({playback_epoch_w, pcm_w[11'(frame_r)*256 +: 256]}),
    .valid_i(pcm_valid_w), .ready_o(pcm_ready_w), .m_clk_i(media_clk_i),
    .m_rst_n(media_rst_n_w), .data_o(playback_w), .valid_o(playback_valid_w),
    .ready_i(playback_ready_w), .level_o(playback_level_w)
  );
  KL_usbaudio_crossing capture_crossing (
    .s_clk_i(media_clk_i), .s_rst_n(media_rst_n_w), .data_i(capture_w),
    .valid_i(capture_valid_w), .ready_o(capture_ready_w), .m_clk_i(bus_clk_i),
    .m_rst_n(bus_rst_n_w), .data_o(bus_capture_w), .valid_o(bus_capture_valid_w),
    .ready_i(bus_capture_ready_w), .level_o(capture_level_w)
  );
  wire ack_valid_w, ack_ready_w, bus_ack_valid_w;
  wire [31:0] ack_epoch_w, bus_ack_epoch_w;
  KL_usbaudio_media media (
    .clk_i(media_clk_i), .rst_n(media_rst_n_w), .media_tick_i(media_tick_i),
    .media_ns_i(media_ns_i), .state_valid_i(media_state_valid_w),
    .state_ready_o(media_state_ready_w), .state_i(media_state_w),
    .ack_valid_o(ack_valid_w), .ack_ready_i(ack_ready_w), .ack_epoch_o(ack_epoch_w),
    .playback_valid_i(playback_valid_w), .playback_ready_o(playback_ready_w),
    .playback_i(playback_w), .playback_level_i(playback_level_w),
    .pair_valid_o(pair_valid_o), .pair_slot_o(pair_slot_o), .pair_l_o(pair_l_o),
    .pair_r_o(pair_r_o), .frame_ns_o(frame_ns_o), .capture_tick_o(capture_tick_o),
    .render_data_i(render_data_i), .render_valid_i(render_valid_i),
    .render_last_i(render_last_i), .render_stream_i(render_stream_i), .render_tick_i(render_tick_i),
    .capture_valid_o(capture_valid_w), .capture_ready_i(capture_ready_w), .capture_o(capture_w),
    .gaps_o(playback_gaps_o), .drops_o(capture_drops_o), .frames_o(media_frames_o),
    .running_o(media_running_w), .playback_extremes_o(playback_extremes_o),
    .error_o(media_error_w)
  );
  KL_usbaudio_crossing #(.WIDTH_P(32), .DEPTH_P(4)) acknowledgement (
    .s_clk_i(media_clk_i), .s_rst_n(media_rst_n_w), .data_i(ack_epoch_w),
    .valid_i(ack_valid_w), .ready_o(ack_ready_w), .m_clk_i(bus_clk_i),
    .m_rst_n(bus_rst_n_w), .data_o(bus_ack_epoch_w), .valid_o(bus_ack_valid_w),
    .ready_i(1'b1), .level_o() // every returned acknowledgement is consumed immediately
  );
  logic [31:0] applied_epoch_r, published_epoch_r, status_epoch_r;
  logic [31:0] status_age_r;
  wire snapshot_ready_w;
  wire snapshot_w = snapshot_ready_w && status_age_r >= BUS_HZ_P/2000;
  always_ff @(posedge bus_clk_i) begin : status_schedule
    if (!bus_rst_n_w) begin
      applied_epoch_r <= 0;
      published_epoch_r <= 32'hffffffff;
      status_epoch_r <= 0;
      status_age_r <= BUS_HZ_P/2000;
    end else begin
      if (bus_ack_valid_w) applied_epoch_r <= bus_ack_epoch_w;
      if (status_age_r != 32'hffffffff) status_age_r <= status_age_r+1'b1;
      if (snapshot_w) begin
        status_age_r <= 0;
        status_epoch_r <= applied_epoch_r;
      end
      if (status_valid_o && status_ready_i && status_last_o) published_epoch_r <= status_epoch_r;
    end
  end : status_schedule
  KL_usbaudio_status #(.DIGEST_P(DIGEST_P)) status_record (
    .clk_i(bus_clk_i), .rst_n(bus_rst_n_w), .snapshot_valid_i(snapshot_w),
    .snapshot_ready_o(snapshot_ready_w), .feedback_samples_q16_i(feedback_q16_o),
    .rate_hz_i(32'd48000), // the fixed profile runs at 48000 Hz
    .flags_i({error_o, running_sync_r, locked_o}),
    .capture_epoch_i(applied_epoch_r), .valid_o(status_valid_o), .ready_i(status_ready_i),
    .data_o(status_data_o), .last_o(status_last_o)
  );
  KL_usbaudio_packet #(.BUS_HZ_P(BUS_HZ_P)) capture_packet (
    .clk_i(bus_clk_i), .rst_n(bus_rst_n_w),
    .reference_i(accepted_reference_w),
    .enabled_i(locked_o && bus_flags_r[2] && bus_flags_r[1]
        && applied_epoch_r == bus_capture_epoch_r && published_epoch_r == bus_capture_epoch_r),
    .fence_i(capture_abort_o), .epoch_i(bus_capture_epoch_r),
    .frame_valid_i(bus_capture_valid_w), .frame_ready_o(bus_capture_ready_w),
    .frame_i(bus_capture_w), .level_i(capture_level_w),
    .valid_o(capture_valid_o), .ready_i(capture_ready_i),
    .data_o(capture_data_o), .last_o(capture_last_o),
    .gaps_o(packet_gaps_w), .abandoned_o(abandoned_w)
  );
endmodule
`default_nettype wire
