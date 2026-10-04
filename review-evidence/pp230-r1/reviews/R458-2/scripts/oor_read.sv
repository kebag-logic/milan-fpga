// R458-2 disposable: what Verilator 5.050 returns for an out-of-range read of a
// one-element unpacked array indexed by a 1-bit signal, at several widths.
module oor_read (
    input  wire        clk_i,
    input  wire        idx_i,
    input  wire [63:0] d_i,
    input  wire        we_i,
    output logic [63:0] q64_o,
    output logic [47:0] q48_o,
    output logic [11:0] q12_o,
    output logic [31:0] q32_o,
    output logic [63:0] q64r_o
);
  logic [63:0] a64 [0:0];
  logic [47:0] a48 [0:0];
  logic [11:0] a12 [0:0];
  logic [31:0] a32 [0:0];
  logic [63:0] b64 [0:0];  // a second 64-bit array beside a 48-bit read in one concat
  always_ff @(posedge clk_i) if (we_i) begin
    a64[0] <= d_i; a48[0] <= d_i[47:0]; a12[0] <= d_i[11:0]; a32[0] <= d_i[31:0]; b64[0] <= d_i;
  end
  assign q64_o  = a64[idx_i];
  assign q48_o  = a48[idx_i];
  assign q12_o  = a12[idx_i];
  assign q32_o  = a32[idx_i];
  assign q64r_o = b64[idx_i];
endmodule
