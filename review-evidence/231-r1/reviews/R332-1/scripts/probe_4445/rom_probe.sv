// Minimal $readmemh consumer for the missing-image diagnostic probe.
module rom_probe #(parameter string HEX_P = "absent.hex") (
  input  logic       clk,
  input  logic [6:0] addr,
  output logic [31:0] data
);
  logic [31:0] rom [0:127];
  initial $readmemh(HEX_P, rom);
  always_ff @(posedge clk) data <= rom[addr];
endmodule
