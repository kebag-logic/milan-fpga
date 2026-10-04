// R458-2 disposable: out-of-range read of a one-element PACKED array indexed by a
// 1-bit signal, as KL_srp_listener_fsm's sid_r [N_SINKS_P-1:0][63:0] at one sink.
module oor_packed (
    input  wire        clk_i,
    input  wire        idx_i,
    input  wire [63:0] d_i,
    input  wire        we_i,
    output logic [63:0] q64_o,
    output logic [47:0] q48_o,
    output logic [11:0] q12_o
);
  logic [0:0][63:0] p64;
  logic [0:0][47:0] p48;
  logic [0:0][11:0] p12;
  always_ff @(posedge clk_i) if (we_i) begin
    p64[0] <= d_i; p48[0] <= d_i[47:0]; p12[0] <= d_i[11:0];
  end
  assign q64_o = p64[idx_i];
  assign q48_o = p48[idx_i];
  assign q12_o = p12[idx_i];
endmodule
