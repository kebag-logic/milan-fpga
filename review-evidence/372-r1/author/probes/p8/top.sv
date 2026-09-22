`default_nettype none
module top (input wire clk, input wire rst_n, input wire a, input wire b);
  logic x_w;
  assign x_w = 1'bx;
  ap_one: assert property (@(posedge clk) disable iff (!rst_n) !a) else $error("[SVA] ap_one a high");
  ap_two: assert property (@(posedge clk) disable iff (!rst_n) !(a && b)) else $error("[SVA] ap_two a and b");
  always_ff @(posedge clk) begin : unk
    if (rst_n) begin
      ai_unknown: assert (!$isunknown(x_w)) else $error("[SVA] ai_unknown saw X");
    end
  end
  initial $display("isunknown(x_w)=%0d x_w=%b", $isunknown(x_w), x_w);
endmodule
`default_nettype wire
