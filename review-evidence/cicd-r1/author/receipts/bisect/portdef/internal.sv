module sub (input wire [7:0] chans_i = '0, output logic [7:0] a_o);
  assign a_o = chans_i;
endmodule
module top (input wire clk_i, input wire [7:0] pcm_chans_i, output wire [7:0] a_o, output wire [7:0] b_o, output wire [7:0] c_o);
  wire [7:0] inv_w = ~pcm_chans_i;           // a computed internal net
  logic [7:0] reg_r; always_ff @(posedge clk_i) reg_r <= pcm_chans_i;   // a flop
  sub u_port (.chans_i(pcm_chans_i), .a_o(a_o));   // straight from a top input
  sub u_net  (.chans_i(inv_w),       .a_o(b_o));
  sub u_reg  (.chans_i(reg_r),       .a_o(c_o));
endmodule
