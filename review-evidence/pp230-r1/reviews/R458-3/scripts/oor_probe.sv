module oor (input logic clk_i, input logic idx_i, input logic [63:0] d_i, output logic [63:0] q_o);
  logic [0:0][63:0] sid_r;   // N = 1 element, as N_SINKS_P = 1
  always_ff @(posedge clk_i) sid_r[0] <= d_i;
  assign q_o = sid_r[idx_i]; // idx 1 is out of range
endmodule
