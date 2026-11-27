// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Timestamp source: the disciplined 24.576 MHz media oscillator, not PCLK.
// Gray counter paths require a one-source-period skew/delay constraint.
`default_nettype none
module KL_usbaudio_clock (
  input wire media_clk_i, //! actual disciplined media oscillator
  input wire media_rst_n, //! synchronized session reset
  input wire bus_clk_i, //! interval parser clock
  input wire bus_rst_n, //! synchronized session reset
  output logic [47:0] ticks_o //! coherent cumulative media-oscillator ticks
);
  logic [47:0] counter_r, gray_r;
  (* ASYNC_REG = "TRUE" *) logic [47:0] meta_r, sync_r;
  wire [47:0] next_w = counter_r+48'd1;
  always_ff @(posedge media_clk_i) begin : media_counter
    if (!media_rst_n) begin
      counter_r <= 0;
      gray_r <= 0;
    end else begin
      counter_r <= next_w;
      gray_r <= next_w ^ (next_w >> 1);
    end
  end : media_counter
  always_ff @(posedge bus_clk_i) begin : counter_crossing
    if (!bus_rst_n) begin
      meta_r <= 0;
      sync_r <= 0;
    end else begin
      meta_r <= gray_r;
      sync_r <= meta_r;
    end
  end : counter_crossing
  for (genvar bit_index = 0; bit_index < 48; bit_index++) begin : g_gray_decode
    assign ticks_o[bit_index] = ^sync_r[47:bit_index];
  end : g_gray_decode
endmodule
`default_nettype wire
