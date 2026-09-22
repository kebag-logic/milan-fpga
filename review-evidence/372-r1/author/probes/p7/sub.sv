`default_nettype none
module sub_chk (input wire clk, input wire rst_n, input wire a, input wire b);
  import "DPI-C" context function void sva_witness(input string rule, input bit nonvacuous);
  ap_hold: assert property (@(posedge clk) disable iff (!rst_n) (a && !b) |=> a)
    sva_witness("ap_hold", $past(rst_n && a && !b)); else $error("[SVA] ap_hold");
endmodule
module chk (input wire clk, input wire rst_n, input wire a, input wire b, input wire one_i);
  import "DPI-C" context function void sva_witness(input string rule, input bit nonvacuous);
  sub_chk u_a (.clk(clk), .rst_n(rst_n), .a(a), .b(b));
  sub_chk u_b (.clk(clk), .rst_n(rst_n), .a(b), .b(a));
  ap_one: assert property (@(posedge clk) disable iff (!rst_n) one_i || !one_i)
    sva_witness("ap_one", 1'b1); else $error("[SVA] ap_one");
  always_ff @(posedge clk) begin : imm_clocked
    if (rst_n && one_i) begin
      ai_c: assert (one_i) sva_witness("ai_c", 1'b1); else $error("[SVA] ai_c");
    end
  end
  always_comb begin : imm_comb
    if (one_i) begin
      ai_f: assert final (one_i) sva_witness("ai_f", 1'b1); else $error("[SVA] ai_f");
    end
  end
endmodule
`default_nettype wire
