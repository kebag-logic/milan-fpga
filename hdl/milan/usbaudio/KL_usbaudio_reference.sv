// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Qualify 1 kHz USB interval records against the actual media oscillator.
// ITP delta units are 1/60 MHz. At 24.576 MHz that is 256/625 ticks.
// The physical latency bound is a separate, explicit qualification input.
`default_nettype none
module KL_usbaudio_reference #(
  parameter int unsigned BUS_HZ_P = 50_000_000, //! watchdog time base only
  parameter int unsigned WINDOW_LOG2_P = 13 //! USB microframes per window
)(
  input wire clk_i, //! bus clock
  input wire rst_n, //! synchronized session reset
  input wire media_locked_i, //! synchronized gPTP media-clock validity
  input wire latency_qualified_i, //! measured physical service bound accepted
  input wire reference_i, //! complete structurally valid reference
  input wire malformed_i, //! rejected reference resets qualification
  input wire [13:0] count_i, //! USB microframe count, modulo 16384
  input wire [31:0] sequence_i, //! observation sequence, modulo 2^32
  input wire [12:0] delta_i, //! ITP delta, units of 16 2/3 ns
  input wire discontinuity_i, //! sticky loss carried by firmware
  input wire [47:0] stamp_ticks_i, //! first word's cumulative media ticks
  output wire locked_o, //! full estimator window and physical qualification
  output wire [31:0] feedback_q16_o, //! measured samples per microframe
  output logic [31:0] losses_o, //! reference losses, saturating
  output wire accepted_o //! continuity-qualified scheduling observation
);
  localparam int unsigned WATCHDOG_C = BUS_HZ_P/500;
  localparam int unsigned AGE_BITS_C = $clog2(WATCHDOG_C+1);
  logic [AGE_BITS_C-1:0] age_r;
  logic baseline_r, healthy_r;
  logic [13:0] count_r;
  logic [31:0] sequence_r;
  logic [47:0] stamp_r;
  logic qualified_p_r;
  logic [31:0] events_r;
  wire measured_w;
  wire [31:0] feedback_w;
  wire [13:0] count_step_w = count_i-count_r;
  wire [47:0] delivery_ticks_w = stamp_ticks_i-stamp_r;
  // Reject deliveries outside 0.75..1.25 ms in source-clock ticks.
  // This desk bound rejects bunching; hardware must qualify its variation.
  wire continuity_w = sequence_i == sequence_r+32'd1 && count_step_w == 8
      && delivery_ticks_w >= 18432 && delivery_ticks_w <= 30720;
  wire expired_w = age_r == AGE_BITS_C'(WATCHDOG_C-1);
  wire bad_w = malformed_i || expired_w || !media_locked_i
      || (reference_i && (discontinuity_i || delta_i >= 7500
                         || (baseline_r && !continuity_w)));
  wire [31:0] delta_ticks_w = (32'(delta_i)*256)/625;
  wire [47:0] corrected_ticks_w = stamp_ticks_i-48'(delta_ticks_w);
  assign locked_o = healthy_r && measured_w && media_locked_i && latency_qualified_i;
  assign accepted_o = reference_i && !bad_w;
  assign feedback_q16_o = locked_o ? feedback_w : 32'd0;
  KL_usbaudio_feedback #(.WINDOW_LOG2_P(WINDOW_LOG2_P), .INTERVAL_LOG2_P(3)) estimator (
    .clk_i(clk_i), .rst_n(rst_n), .locked_i(healthy_r && !bad_w),
    .interval_i(qualified_p_r && !bad_w), .media_events_i(events_r),
    .feedback_q16_o(feedback_w), .measured_o(measured_w)
  );
  always_ff @(posedge clk_i) begin : reference_qualification
    if (!rst_n) begin
      age_r <= 0;
      baseline_r <= 0;
      healthy_r <= 0;
      count_r <= 0;
      sequence_r <= 0;
      stamp_r <= 0;
      qualified_p_r <= 0;
      events_r <= 0;
      losses_o <= 0;
    end else begin
      qualified_p_r <= 0;
      if (age_r < AGE_BITS_C'(WATCHDOG_C)) age_r <= age_r+1'b1;
      if (bad_w) begin
        baseline_r <= 0;
        healthy_r <= 0;
        if ((baseline_r || healthy_r || malformed_i || reference_i)
            && losses_o != 32'hffffffff) losses_o <= losses_o+1'b1;
      end
      if (reference_i) begin
        age_r <= 0;
        count_r <= count_i;
        sequence_r <= sequence_i;
        stamp_r <= stamp_ticks_i;
        // A refused observation never doubles as the replacement baseline.
        if (!bad_w) begin
          baseline_r <= 1;
          healthy_r <= 1;
          events_r <= 32'(corrected_ticks_w >> 9);
          qualified_p_r <= 1;
        end
      end
    end
  end : reference_qualification
endmodule
`default_nettype wire
