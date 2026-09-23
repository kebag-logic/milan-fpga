// Reviewer disposable probe (R239-1): pinned-tool assertion semantics the #372 guide states.
`default_nettype none
module sem_probe (
  input wire clk,
  input wire rst_n,
  input wire a,
  input wire b
);
  import "DPI-C" context function void note(input string name, input int passed, input bit flag);
  logic one = 1'b1;
  ap_a: assert property (@(posedge clk) disable iff (!rst_n) a |=> b)
    note("ap_a", 1, $past(rst_n && a));
  else
    note("ap_a", 0, 1'b0);
  ap_past_one: assert property (@(posedge clk) $past(one) == 1'b1)
    note("ap_past_one", 1, 1'b1);
  else
    note("ap_past_one", 0, 1'b0);
  ap_stable_one: assert property (@(posedge clk) $stable(one))
    note("ap_stable_one", 1, 1'b1);
  else
    note("ap_stable_one", 0, 1'b0);
  as_a: assume property (@(posedge clk) disable iff (!rst_n) a |=> b)
    note("as_a", 1, 1'b1);
  else
    note("as_a", 0, 1'b0);
  cv_a: cover property (@(posedge clk) a)
    note("cv_a", 1, 1'b1);
  always_comb begin : ci_block
    ci_a: cover (a) note("ci_a", 1, 1'b1);
  end
endmodule
`default_nettype wire
