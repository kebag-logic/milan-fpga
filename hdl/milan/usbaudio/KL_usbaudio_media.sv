// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Eight-channel media endpoint. One FIFO beat is one frame, epoch included.
// Capture maps stream zero channels 0..7 explicitly; playback closes pair 3.
`default_nettype none
module KL_usbaudio_media #(
  parameter int unsigned PREFILL_FRAMES_P = 12 //! playback startup buffering
)(
  input wire clk_i, //! datapath clock
  input wire rst_n, //! synchronized session reset
  input wire media_tick_i, //! gPTP media frame grid
  input wire [31:0] media_ns_i, //! that frame's presentation instant
  input wire state_valid_i, //! complete state snapshot
  output wire state_ready_o, //! applies state only with acknowledgement room
  input wire [66:0] state_i, //! capture epoch, playback epoch, flags
  output wire ack_valid_o, //! applied capture epoch snapshot
  input wire ack_ready_i, //! acknowledgement crossing has room
  output wire [31:0] ack_epoch_o, //! applied capture epoch
  input wire playback_valid_i, //! complete playback frame
  output wire playback_ready_o, //! consume or discard whole frame
  input wire [287:0] playback_i, //! playback epoch above 8 PCM subslots
  input wire [6:0] playback_level_i, //! conservative queued frame count
  output logic pair_valid_o, //! capture mapper pair strobe
  output logic [3:0] pair_slot_o, //! pair 0..3 in channel order
  output logic [31:0] pair_l_o, //! all subslot bits
  output logic [31:0] pair_r_o, //! all subslot bits
  output logic [31:0] frame_ns_o, //! timestamp held through the frame walk
  output logic capture_tick_o, //! mapper walk after the whole frame closed
  input wire [63:0] render_data_i, //! render queue's S32BE pair
  input wire render_valid_i, //! render queue accepted pair
  input wire render_last_i, //! last pair of the stream frame
  input wire [3:0] render_stream_i, //! explicitly select stream zero
  input wire render_tick_i, //! all render frames for this grid have arrived
  output wire capture_valid_o, //! complete frame with applied capture epoch
  input wire capture_ready_i, //! crossing accepts frame
  output wire [287:0] capture_o, //! epoch and channel-ordered PCM
  output logic [31:0] gaps_o, //! playback empty-at-grid whole frames
  output logic [31:0] drops_o, //! render frames lost at full crossing
  output logic [31:0] frames_o, //! observed media grid events
  output wire [1:0] running_o, //! media-applied playback and capture activity
  output wire [13:0] playback_extremes_o, //! maximum then minimum complete frames
  output logic error_o //! sticky whole-frame transport error
);
  logic [31:0] playback_epoch_r, capture_epoch_r;
  logic [2:0] flags_r;
  logic primed_r;
  logic [255:0] playback_r, render_r;
  logic [2:0] emit_r, render_pair_r;
  logic render_complete_r, render_discard_r, render_fenced_r;
  logic [6:0] minimum_r, maximum_r;
  wire state_take_w = state_valid_i && state_ready_o;
  wire playback_changed_w = state_valid_i && state_i[34:3] != playback_epoch_r;
  wire capture_changed_w = state_valid_i && state_i[66:35] != capture_epoch_r;
  wire playback_on_w = flags_r[0] && flags_r[1];
  wire epoch_matches_w = playback_i[287:256] == playback_epoch_r;
  wire pop_w = media_tick_i && playback_on_w && primed_r && emit_r == 0;
  assign running_o = {playback_on_w && primed_r, flags_r[2] && flags_r[1]};
  assign playback_extremes_o = {maximum_r, minimum_r};
  // A playback transition cannot cancel the grid event or an active pair
  // walk. Finish that atomic frame before applying and acknowledging state.
  wire state_boundary_w = !playback_changed_w || (emit_r == 0 && !media_tick_i);
  assign state_ready_o = ack_ready_i && state_boundary_w;
  assign ack_valid_o = state_valid_i && state_boundary_w;
  assign ack_epoch_o = state_i[66:35];
  assign playback_ready_o = !playback_changed_w &&
      (!epoch_matches_w || !playback_on_w || pop_w);
  assign capture_o = {capture_epoch_r, render_r};
  assign capture_valid_o = render_tick_i && render_complete_r
      && flags_r[2] && flags_r[1] && !capture_changed_w && !render_fenced_r;
  function automatic logic [31:0] from_wire(input logic [31:0] value);
    return {value[7:0], value[15:8], value[23:16], value[31:24]};
  endfunction
  always_ff @(posedge clk_i) begin : media_frames
    if (!rst_n) begin
      playback_epoch_r <= 0;
      capture_epoch_r <= 0;
      flags_r <= 0;
      primed_r <= 0;
      playback_r <= 0;
      render_r <= 0;
      emit_r <= 0;
      render_pair_r <= 0;
      render_complete_r <= 0;
      render_discard_r <= 0;
      render_fenced_r <= 0;
      pair_valid_o <= 0;
      pair_slot_o <= 0;
      pair_l_o <= 0;
      pair_r_o <= 0;
      frame_ns_o <= 0;
      capture_tick_o <= 0;
      gaps_o <= 0;
      drops_o <= 0;
      frames_o <= 0;
      error_o <= 0;
      minimum_r <= 7'h7f;
      maximum_r <= 0;
    end else begin
      pair_valid_o <= 0;
      capture_tick_o <= 0;
      if (media_tick_i && frames_o != 32'hffffffff) frames_o <= frames_o+1'b1;
      if (pop_w) begin
        if (playback_level_i < minimum_r) minimum_r <= playback_level_i;
        if (playback_level_i > maximum_r) maximum_r <= playback_level_i;
      end
      if (playback_on_w && epoch_matches_w && playback_valid_i
          && playback_level_i >= 7'(PREFILL_FRAMES_P)) primed_r <= 1;
      if (media_tick_i && emit_r == 0) begin
        playback_r <= pop_w && playback_valid_i && epoch_matches_w
            && !playback_changed_w ? playback_i[255:0] : 256'd0;
        frame_ns_o <= media_ns_i;
        emit_r <= 1;
        if (pop_w && !playback_changed_w && (!playback_valid_i || !epoch_matches_w)) begin
          error_o <= 1;
          if (gaps_o != 32'hffffffff) gaps_o <= gaps_o+1'b1;
        end
      end
      if (emit_r != 0) begin
        emit_r <= emit_r+1'b1;
        if (emit_r <= 4) begin
          pair_valid_o <= 1;
          pair_slot_o <= 4'(emit_r-1'b1);
          pair_l_o <= playback_r[31:0];
          pair_r_o <= playback_r[63:32];
          playback_r <= playback_r >> 64;
        end else if (emit_r == 6) begin
          capture_tick_o <= 1;
          emit_r <= 0;
        end
      end
      if (render_valid_i && render_stream_i == 0) begin
        if (render_discard_r) begin
          if (render_last_i) begin
            render_discard_r <= 0;
            render_pair_r <= 0;
          end
        end else begin
          if (render_pair_r < 4)
            render_r[8'(render_pair_r)*64 +: 64] <=
                {from_wire(render_data_i[63:32]), from_wire(render_data_i[31:0])};
          render_pair_r <= render_pair_r+1'b1;
          if (render_last_i) begin
            render_complete_r <= render_pair_r == 3;
            render_pair_r <= 0;
            if (render_pair_r != 3 && !capture_changed_w) error_o <= 1;
          end
        end
      end
      if (render_tick_i) begin
        render_complete_r <= 0;
        render_fenced_r <= 0;
        if (flags_r[2] && flags_r[1] && !render_fenced_r && !capture_changed_w
            && (!render_complete_r || !capture_ready_i)) begin
          error_o <= 1;
          if (drops_o != 32'hffffffff) drops_o <= drops_o+1'b1;
        end
      end
      if (state_take_w) begin
        flags_r <= state_i[2:0];
        if (playback_epoch_r != state_i[34:3]) begin
          playback_epoch_r <= state_i[34:3];
          primed_r <= 0;
          emit_r <= 0;
          pair_valid_o <= 0;
          capture_tick_o <= 0;
          playback_r <= 0;
        end
        if (capture_epoch_r != state_i[66:35]) begin
          capture_epoch_r <= state_i[66:35];
          render_complete_r <= 0;
          render_pair_r <= 0;
          // Drain the remainder of a frame already begun under the old
          // epoch. Its normal last/tick edges are an intentional fence,
          // not an incomplete new frame or an active transport failure.
          render_discard_r <= !render_tick_i && !render_last_i
              && (render_pair_r != 0 || render_valid_i);
          render_fenced_r <= !render_tick_i
              && (render_pair_r != 0 || render_valid_i || render_complete_r);
        end
      end
    end
  end : media_frames
endmodule
`default_nettype wire
