module sub (input wire clk_i, input wire [3:0] sel_i = 4'd0, input wire [7:0] chans_i, output logic [3:0] q_o);
  logic [3:0] raw_w;
  always_comb begin : lookup
    raw_w = 4'd0;
    for (int s = 0; s < 2; s++) if (32'(sel_i) == s) raw_w = chans_i[s*4 +: 4];
  end
  always_ff @(posedge clk_i) q_o <= (raw_w == 4'd0) ? 4'd2 : raw_w;
endmodule
module top (input wire clk_i, input wire [3:0] sel_i, input wire [7:0] pcm_chans_i, output wire [3:0] q_o);
  sub u (.clk_i(clk_i), .sel_i(sel_i), .chans_i(pcm_chans_i), .q_o(q_o));
endmodule
