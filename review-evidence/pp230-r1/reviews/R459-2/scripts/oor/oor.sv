// SPDX-License-Identifier: CERN-OHL-W-2.0
// Out-of-range read of a one-element packed array, as the flop arms at one
// context see a parked index: what does the simulator return for index 1?
module oor (
    input  wire        clk_i,
    input  wire        idx_i,          // 1 bit, as SNK_W_C/SRC_W_C at one context
    input  wire [63:0] w64_i,
    input  wire [47:0] w48_i,
    output logic [63:0] r64_o,
    output logic [47:0] r48_o
);
  logic [0:0][63:0] a64_r;
  logic [0:0][47:0] a48_r;
  always_ff @(posedge clk_i) begin
    a64_r[0] <= w64_i;
    a48_r[0] <= w48_i;
  end
  assign r64_o = a64_r[idx_i];
  assign r48_o = a48_r[idx_i];
endmodule
