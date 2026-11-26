// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Socket 1 serializer (#1021). Snapshot input must already cross atomically.
// Its ten words stay immutable under stalls, including the capture epoch.
`default_nettype none
module KL_usbaudio_status #(
  parameter logic [15:0] DIGEST_P = 16'h84ff //! pinned eight-channel profile
)(
  input wire clk_i, //! bus clock
  input wire rst_n, //! synchronous session reset, active low
  input wire snapshot_valid_i, //! coherent status available
  output wire snapshot_ready_o, //! accepts one snapshot, never overwrites it
  input wire [31:0] feedback_q16_i, //! measured samples per USB microframe
  input wire [31:0] rate_hz_i, //! actual media rate, including unsupported values
  input wire [3:0] flags_i, //! locked, capture running, playback running, error
  input wire [31:0] capture_epoch_i, //! last applied capture epoch
  output wire valid_o, //! socket 1 word available
  input wire ready_i, //! socket 1 accepts this word
  output wire [15:0] data_o, //! exact little-endian status word
  output wire last_o //! commit with packet end on this tenth word
);
  logic busy_r;
  logic [3:0] word_r;
  logic [15:0] sequence_r;
  logic [159:0] record_r;
  assign snapshot_ready_o = !busy_r;
  assign valid_o = busy_r;
  assign last_o = busy_r && word_r == 9;
  assign data_o = record_r[8'(word_r) * 16 +: 16];
  always_ff @(posedge clk_i) begin : status_engine
    if (!rst_n) begin
      busy_r <= 0;
      word_r <= 0;
      sequence_r <= 0;
      record_r <= 0;
    end else begin
      if (snapshot_valid_i && snapshot_ready_o) begin
        record_r <= {capture_epoch_i, DIGEST_P, 12'b0, flags_i,
                     rate_hz_i, feedback_q16_i, sequence_r, 16'h5541};
        busy_r <= 1;
        word_r <= 0;
      end
      if (valid_o && ready_i) begin
        if (last_o) begin
          busy_r <= 0;
          sequence_r <= sequence_r + 1'b1;
        end else word_r <= word_r + 1'b1;
      end
    end
  end : status_engine
endmodule
`default_nettype wire
