module rom_probe #(parameter string HEX_P = "missing_image.hex") (
  input  logic       clk_i,
  input  logic [6:0] a_i,
  output logic [31:0] d_o
);
  logic [31:0] rom_r [0:127];
  initial $readmemh(HEX_P, rom_r);
  always_ff @(posedge clk_i) d_o <= rom_r[a_i];
endmodule
