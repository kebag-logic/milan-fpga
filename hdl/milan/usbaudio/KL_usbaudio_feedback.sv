// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Feedback window arithmetic (#1021), not a USB interval-reference source.
// Each qualified interval arrives with a coherent cumulative media count.
// A PCLK divider cannot provide interval_i. Integration must prove its source.
`default_nettype none
module KL_usbaudio_feedback #(
  parameter int unsigned WINDOW_LOG2_P = 13 //! window of USB microframes
)(
  input wire clk_i, //! measurement domain clock
  input wire rst_n, //! synchronous session reset, active low
  input wire locked_i, //! master media clock locked
  input wire interval_i, //! independently qualified USB microframe boundary
  input wire [31:0] media_events_i, //! atomic cumulative count at this boundary
  output wire [31:0] feedback_q16_o, //! samples per 125 us; zero while unlocked
  output logic measured_o //! one full measurement window completed
);
  logic started_r;
  logic [WINDOW_LOG2_P-1:0] intervals_r;
  logic [31:0] baseline_r, feedback_r;
  wire [31:0] events_w = media_events_i - baseline_r;
  assign feedback_q16_o = locked_i ? feedback_r : 32'd0;
  initial begin : parameter_guard
    if (WINDOW_LOG2_P < 3 || WINDOW_LOG2_P > 16)
      $error("feedback window must fit Q16.16 event scaling");
  end : parameter_guard
  always_ff @(posedge clk_i) begin : feedback_engine
    if (!rst_n || !locked_i) begin
      started_r <= 0;
      intervals_r <= 0;
      baseline_r <= 0;
      feedback_r <= 32'h00060000;
      measured_o <= 0;
    end else if (interval_i) begin
      if (!started_r) begin
        started_r <= 1;
        baseline_r <= media_events_i;
      end else begin
        intervals_r <= intervals_r + 1'b1;
        if (&intervals_r) begin
          feedback_r <= events_w << (16 - WINDOW_LOG2_P);
          baseline_r <= media_events_i;
          measured_o <= 1;
        end
      end
    end
  end : feedback_engine
endmodule
`default_nettype wire
