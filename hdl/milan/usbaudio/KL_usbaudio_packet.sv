// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Capture packet storage retains every word under ordinary bus stalls.
// Only an explicit capture epoch fences and abandons a partial packet.
`default_nettype none
module KL_usbaudio_packet #(
  parameter int unsigned BUS_HZ_P = 50_000_000 //! local scheduling clock
)(
  input wire clk_i, //! bus clock
  input wire rst_n, //! synchronized session reset
  input wire reference_i, //! qualified selected USB reference, each eight microframes
  input wire enabled_i, //! fresh lock, active capture and published acknowledgement
  input wire fence_i, //! capture epoch transition, distinct from backpressure
  input wire [31:0] epoch_i, //! applied capture epoch
  input wire frame_valid_i, //! whole captured frame available
  output wire frame_ready_o, //! take one whole frame
  input wire [287:0] frame_i, //! capture epoch and eight PCM subslots
  input wire [6:0] level_i, //! conservative complete-frame count
  output wire valid_o, //! capture word available for socket zero
  input wire ready_i, //! word transferred to the receiver
  output wire [15:0] data_o, //! low byte first
  output wire last_o, //! final word commits this interval
  output logic [31:0] gaps_o, //! empty or missed scheduled intervals
  output logic [31:0] abandoned_o //! whole frames discarded by epoch fencing
);
  if (BUS_HZ_P < 8000) begin : parameter_guard
    $error("AUDIO_PARAMETER_PACKET: clock must provide at least one cycle per USB microframe");
  end : parameter_guard
  typedef enum logic [1:0] { WAIT_S, FILL_S, SEND_S } state_t;
  state_t state_r;
  logic [1791:0] packet_r;
  logic [2:0] frames_r, filled_r;
  logic [6:0] word_r;
  logic [31:0] reference_age_r, service_period_r, service_age_r;
  logic reference_seen_r, schedule_r, started_r;
  wire service_w = schedule_r && service_age_r >= service_period_r-1'b1;
  wire matching_w = frame_i[287:256] == epoch_i;
  wire take_frame_w = frame_valid_i && frame_ready_o;
  wire [2:0] available_w = level_i >= 7 ? 3'd7 : 3'(level_i);
  assign frame_ready_o = !fence_i && (!enabled_i || !matching_w || state_r == FILL_S);
  assign valid_o = state_r == SEND_S && enabled_i && !fence_i;
  assign data_o = packet_r[11'(word_r)*16 +: 16];
  assign last_o = valid_o && word_r == {frames_r, 4'b0}-1'b1;
  always_ff @(posedge clk_i) begin : capture_intervals
    if (!rst_n) begin
      state_r <= WAIT_S;
      packet_r <= 0;
      frames_r <= 0;
      filled_r <= 0;
      word_r <= 0;
      reference_age_r <= 0;
      service_age_r <= 0;
      service_period_r <= BUS_HZ_P/8000;
      reference_seen_r <= 0;
      schedule_r <= 0;
      started_r <= 0;
      gaps_o <= 0;
      abandoned_o <= 0;
    end else begin
      if (reference_age_r != 32'hffffffff) reference_age_r <= reference_age_r+1'b1;
      if (schedule_r) service_age_r <= service_age_r+1'b1;
      if (service_w) service_age_r <= 0;
      if (reference_i) begin
        reference_age_r <= 0;
        reference_seen_r <= 1;
        if (reference_seen_r) begin
          service_period_r <= (reference_age_r+1'b1) >> 3;
          schedule_r <= 1;
          if (!schedule_r) service_age_r <= 0;
        end
      end
      if (reference_age_r >= BUS_HZ_P/500) begin
        schedule_r <= 0;
        reference_seen_r <= 0;
      end
      if (service_w && enabled_i) begin
        if (state_r == WAIT_S && matching_w && frame_valid_i
            && (started_r || level_i >= 12) && available_w != 0) begin
          state_r <= FILL_S;
          frames_r <= available_w;
          filled_r <= 0;
          word_r <= 0;
          started_r <= 1;
        end else if (started_r && gaps_o != 32'hffffffff) gaps_o <= gaps_o+1'b1;
      end
      if (state_r == FILL_S && take_frame_w && matching_w && enabled_i) begin
        packet_r[11'(filled_r)*256 +: 256] <= frame_i[255:0];
        filled_r <= filled_r+1'b1;
        if (filled_r == frames_r-1'b1) state_r <= SEND_S;
      end
      if (valid_o && ready_i) begin
        if (last_o) state_r <= WAIT_S;
        else word_r <= word_r+1'b1;
      end
      if (fence_i) begin
        if (state_r != WAIT_S && abandoned_o <= 32'hfffffff8)
          abandoned_o <= abandoned_o+32'(state_r == FILL_S ? filled_r : frames_r);
        state_r <= WAIT_S;
        started_r <= 0;
        packet_r <= 0;
        filled_r <= 0;
        word_r <= 0;
      end
    end
  end : capture_intervals
endmodule
`default_nettype wire
