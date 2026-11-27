// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Socket 3 record staging for the fixed eight-channel profile (#1021).
// A record becomes visible only after its complete header and payload.
// Epoch application, media queues and the shared bus live outside this block.
`default_nettype none
module KL_usbaudio_record #(
  parameter logic [15:0] DIGEST_P = 16'h84ff //! pinned eight-channel profile
)(
  input wire clk_i, //! bus clock
  input wire rst_n, //! synchronous session reset, active low
  input wire valid_i, //! socket 3 word available, including while inactive
  output wire ready_o, //! retains the completed record until accepted
  input wire [15:0] data_i, //! little-endian bus word
  output wire record_valid_o, //! entire validated record is immutable
  input wire record_ready_i, //! consumer applied state and retained payload
  output logic [31:0] playback_epoch_o, //! independent playback epoch
  output logic [31:0] capture_epoch_o, //! independent capture epoch
  output logic [2:0] flags_o, //! playback active, clock valid, capture requested
  output logic [2:0] frames_o, //! whole eight-channel frames, zero for state
  output logic [1791:0] pcm_o, //! seven frames maximum; channel zero in low bits
  output logic [31:0] rejected_o, //! rejected complete records, saturating
  output logic [31:0] digest_errors_o, //! rejected digests, saturating
  output wire done_o //! last word consumed, including refused records
);
  if (DIGEST_P != 16'h84ff) begin : parameter_guard
    $error("AUDIO_PARAMETER_RECORD: only the fixed eight-channel profile is supported");
  end : parameter_guard
  typedef enum logic [1:0] { HEADER_S, PAYLOAD_S, COMPLETE_S } state_t;
  state_t state_r;
  logic [2:0] header_word_r;
  logic [15:0] length_bytes_r;
  logic [15:0] payload_word_r;
  logic good_r, digest_bad_r, flags_good_r;
  wire accept_w = valid_i && ready_o;
  wire last_payload_w = payload_word_r == ((length_bytes_r - 16'd1) >> 1);
  wire finish_w = accept_w && ((state_r == HEADER_S && header_word_r == 3'd7
                              && length_bytes_r == 0)
                              || (state_r == PAYLOAD_S && last_payload_w));
  wire header_good_w = good_r && data_i == DIGEST_P && flags_good_r;
  wire finish_good_w = state_r == HEADER_S ? header_good_w : good_r;
  wire finish_digest_bad_w = state_r == HEADER_S ? data_i != DIGEST_P : digest_bad_r;
  assign ready_o = state_r != COMPLETE_S;
  assign record_valid_o = state_r == COMPLETE_S;
  assign done_o = finish_w;
  wire clear_pcm_w = !rst_n || (state_r == COMPLETE_S && record_ready_i)
      || (finish_w && !finish_good_w);

  // Separate fixed-word banks expose a shared synchronous clear and one
  // write enable per word. No full-record variable write mask is needed.
  for (genvar word_index = 0; word_index < 112; word_index++) begin : g_pcm_word
    always_ff @(posedge clk_i) begin : word_storage
      if (clear_pcm_w) pcm_o[word_index*16 +: 16] <= 0;
      else if (accept_w && state_r == PAYLOAD_S && payload_word_r == 16'(word_index))
        pcm_o[word_index*16 +: 16] <= data_i;
    end : word_storage
  end

  always_ff @(posedge clk_i) begin : record_engine
    if (!rst_n) begin
      state_r <= HEADER_S;
      header_word_r <= 0;
      length_bytes_r <= 0;
      flags_good_r <= 0;
      payload_word_r <= 0;
      good_r <= 1;
      digest_bad_r <= 0;
      playback_epoch_o <= 0;
      capture_epoch_o <= 0;
      flags_o <= 0;
      frames_o <= 0;
      rejected_o <= 0;
      digest_errors_o <= 0;
    end else begin
      if (state_r == COMPLETE_S && record_ready_i) begin
        state_r <= HEADER_S;
        header_word_r <= 0;
        good_r <= 1;
        digest_bad_r <= 0;
      end
      if (accept_w && state_r == HEADER_S) begin
        header_word_r <= header_word_r + 1'b1;
        case (header_word_r)
          0: good_r <= data_i == 16'h554f;
          1: begin
            length_bytes_r <= data_i;
            good_r <= good_r && data_i <= 224 && data_i[4:0] == 0;
            frames_o <= 3'(data_i >> 5);
          end
          2: playback_epoch_o[15:0] <= data_i;
          3: playback_epoch_o[31:16] <= data_i;
          4: capture_epoch_o[15:0] <= data_i;
          5: capture_epoch_o[31:16] <= data_i;
          6: begin
            flags_good_r <= data_i[15:3] == 0
                && (length_bytes_r == 0 || data_i[1:0] == 2'b11);
            flags_o <= data_i[2:0];
          end
          default: begin
            good_r <= header_good_w;
            digest_bad_r <= data_i != DIGEST_P;
            payload_word_r <= 0;
            if (length_bytes_r != 0) state_r <= PAYLOAD_S;
          end
        endcase
      end
      if (accept_w && state_r == PAYLOAD_S) begin
        // Drain the declared length even when refused. Odd invalid lengths
        // occupy a final bus word. Only a session reset restarts lost framing.
        payload_word_r <= payload_word_r + 1'b1;
      end
      if (finish_w) begin
        if (finish_good_w) state_r <= COMPLETE_S;
        else begin
          state_r <= HEADER_S;
          header_word_r <= 0;
          good_r <= 1;
          digest_bad_r <= 0;
          if (rejected_o != 32'hffffffff) rejected_o <= rejected_o + 1'b1;
          if (finish_digest_bad_w && digest_errors_o != 32'hffffffff)
            digest_errors_o <= digest_errors_o + 1'b1;
        end
      end
    end
  end : record_engine
endmodule
`default_nettype wire
