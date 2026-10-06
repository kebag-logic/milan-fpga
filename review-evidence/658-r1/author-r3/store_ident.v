module store_ident (input clk, input rst_n, input we, input [2:0] wa, input [7:0] wd,
                 input [2:0] ra, output [7:0] rd);
  reg [63:0] s;
  always @(posedge clk or negedge rst_n)
    if (!rst_n) s <= 64'h8786858483828180;
    else if (we) s[wa*8 +: 8] <= wd;
  assign rd = s[ra*8 +: 8];
endmodule
