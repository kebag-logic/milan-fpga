module sub (input wire clk_i, input wire [7:0] chans_i = '0, input wire [3:0] sel_i = 4'd0, output logic [7:0] a_o, output logic [3:0] b_o, output logic [3:0] c_o);
  assign a_o = chans_i;
  always_ff @(posedge clk_i) b_o <= chans_i[3:0];
  assign c_o = chans_i[sel_i*4 +: 4];
endmodule
module top (input wire clk_i, input wire [3:0] sel_i, input wire [7:0] pcm_chans_i, output wire [7:0] a_o, output wire [3:0] b_o, output wire [3:0] c_o);
  sub u (.clk_i(clk_i), .sel_i(sel_i), .chans_i(pcm_chans_i), .a_o(a_o), .b_o(b_o), .c_o(c_o));
endmodule
