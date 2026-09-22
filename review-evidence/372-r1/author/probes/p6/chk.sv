`default_nettype none
module chk (
  input wire clk, input wire rst_n, input wire a, input wire b, input wire y,
  input wire idle_i, input wire one_i, input wire two_i
);
  import "DPI-C" function void witness_flag(input string name, input bit nonvacuous);
  ap_hold: assert property (@(posedge clk) disable iff (!rst_n) (a && !b) |=> a)
    witness_flag("ap_hold", $past(rst_n && a && !b)); else $error("[SVA] ap_hold");
  wire unused_ok = &{1'b0, y, idle_i, one_i, two_i};
endmodule
`default_nettype wire
