`default_nettype none
module chk (
  input wire clk, input wire rst_n, input wire a, input wire b, input wire y,
  input wire idle_i, input wire one_i, input wire two_i
);
  import "DPI-C" function void witness(input string name);
  initial begin : vac
`ifdef VAC_OFF
    $assertvacuousoff;
`endif
  end
  ap_hold: assert property (@(posedge clk) disable iff (!rst_n) (a && !b) |=> a)
    witness("ap_hold_pass"); else $error("[SVA] ap_hold");
  ap_comb: assert property (@(posedge clk) disable iff (!rst_n) (a && !b) |-> !idle_i || 1'b1)
    witness("ap_comb_pass"); else $error("[SVA] ap_comb");
  ap_plain: assert property (@(posedge clk) disable iff (!rst_n) !(one_i && two_i))
    witness("ap_plain_pass"); else $error("[SVA] ap_plain");
  wire unused_ok = &{1'b0, y};
endmodule
`default_nettype wire
