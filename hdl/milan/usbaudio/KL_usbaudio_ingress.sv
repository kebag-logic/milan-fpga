// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Socket 3 discriminator. Length, never a ready-flag edge, ends a record.
// The first interval word owns its media-clock timestamp until validation.
`default_nettype none
module KL_usbaudio_ingress #(
  parameter logic [15:0] DIGEST_P = 16'h84ff //! eight-channel profile digest
)(
  input wire clk_i, //! bus clock
  input wire rst_n, //! session reset with synchronized release
  input wire valid_i, //! a complete received bus word
  output wire ready_o, //! backpressure preserves framing
  input wire [15:0] data_i, //! little-endian word
  input wire [47:0] media_ticks_i, //! coherent source-clock counter
  output wire record_valid_o, //! complete playback/state record
  input wire record_ready_i, //! state and PCM accepted
  output wire [31:0] playback_epoch_o, //! independent playback epoch
  output wire [31:0] capture_epoch_o, //! independent capture epoch
  output wire [2:0] flags_o, //! playback, clock, capture flags
  output wire [2:0] frames_o, //! zero to seven whole frames
  output wire [1791:0] pcm_o, //! channel zero in the low subslot
  output logic reference_p_o, //! completed valid interval structure
  output logic loss_p_o, //! malformed interval or unrecognized magic
  output logic [13:0] count_o, //! host microframe number
  output logic [31:0] sequence_o, //! selected ITP sequence
  output logic [12:0] delta_o, //! USB units of 1/60 MHz
  output logic discontinuity_o, //! reference-loss flag
  output logic [47:0] stamp_ticks_o, //! timestamp of the record's first word
  output wire [31:0] rejected_o, //! refused playback/state records
  output wire [31:0] digest_errors_o //! refused playback/state digests
);
  typedef enum logic [1:0] { FIRST_S, PCM_S, REFERENCE_S } state_t;
  state_t state_r;
  logic [3:0] word_r;
  logic [159:0] reference_r;
  logic [47:0] stamp_r;
  wire pcm_ready_w, pcm_done_w;
  wire pcm_word_w = state_r == PCM_S || (state_r == FIRST_S && data_i == 16'h554f);
  wire take_w = valid_i && ready_o;
  assign ready_o = pcm_word_w ? pcm_ready_w : !record_valid_o;
  KL_usbaudio_record #(.DIGEST_P(DIGEST_P)) records (
    .clk_i(clk_i), .rst_n(rst_n), .valid_i(valid_i && pcm_word_w),
    .ready_o(pcm_ready_w), .data_i(data_i), .record_valid_o(record_valid_o),
    .record_ready_i(record_ready_i), .playback_epoch_o(playback_epoch_o),
    .capture_epoch_o(capture_epoch_o), .flags_o(flags_o), .frames_o(frames_o),
    .pcm_o(pcm_o), .rejected_o(rejected_o), .digest_errors_o(digest_errors_o),
    .done_o(pcm_done_w)
  );
  wire structure_good_w = reference_r[31:16] == 20
      && reference_r[47:32] == 16'h0801
      && reference_r[63:62] == 0 && reference_r[50:48] == 0
      && reference_r[109:96] == reference_r[61:48]
      && reference_r[127:123] == 0 && reference_r[143:129] == 0
      && data_i == DIGEST_P;
  always_ff @(posedge clk_i) begin : discriminator
    if (!rst_n) begin
      state_r <= FIRST_S;
      word_r <= 0;
      reference_r <= 0;
      stamp_r <= 0;
      reference_p_o <= 0;
      loss_p_o <= 0;
      count_o <= 0;
      sequence_o <= 0;
      delta_o <= 0;
      discontinuity_o <= 0;
      stamp_ticks_o <= 0;
    end else begin
      reference_p_o <= 0;
      loss_p_o <= 0;
      if (pcm_done_w) state_r <= FIRST_S;
      if (take_w) begin
        case (state_r)
          FIRST_S: begin
            if (data_i == 16'h554f) state_r <= PCM_S;
            else begin
              // Unknown magic consumes the fixed reference envelope, reports
              // loss, and cannot accidentally present PCM as a new header.
              state_r <= REFERENCE_S;
              reference_r <= {144'd0, data_i};
              stamp_r <= media_ticks_i;
              word_r <= 1;
              if (data_i != 16'h5549) loss_p_o <= 1;
            end
          end
          REFERENCE_S: begin
            reference_r[8'(word_r)*16 +: 16] <= data_i;
            word_r <= word_r + 1'b1;
            if (word_r == 9) begin
              state_r <= FIRST_S;
              if (structure_good_w && reference_r[15:0] == 16'h5549) begin
                count_o <= reference_r[61:48];
                sequence_o <= reference_r[95:64];
                delta_o <= reference_r[122:110];
                discontinuity_o <= reference_r[128];
                stamp_ticks_o <= stamp_r;
                reference_p_o <= 1;
              end else loss_p_o <= 1;
            end
          end
          default: ;
        endcase
      end
    end
  end : discriminator
endmodule
`default_nettype wire
