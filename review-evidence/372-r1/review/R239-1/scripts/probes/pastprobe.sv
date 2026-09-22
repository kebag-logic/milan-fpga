// R239 scratch probe: what does $past / $stable / |=> see at the first clock
// edge, for a variable whose declared initial value is 1 and which never
// changes? The #372 guide says "the variable's initial value".
`default_nettype none
module pastprobe;
  logic clk = 1'b0;
  logic one = 1'b1;
  int edges = 0;
  always #5 clk = ~clk;
  always @(posedge clk) begin
    edges <= edges + 1;
    if (edges == 3) $finish;
  end
  ap_past_is_initial: assert property (@(posedge clk) $past(one) == 1'b1)
    else $display("PROBE ap_past_is_initial FAILED at %0t: $past(one) is not 1", $time);
  ap_stable_initial: assert property (@(posedge clk) $stable(one))
    else $display("PROBE ap_stable_initial FAILED at %0t: $stable(one) is false", $time);
  ap_implication_initial: assert property (@(posedge clk) 1'b1 |=> one)
    $display("PROBE ap_implication_initial passed at %0t", $time);
endmodule
`default_nettype wire
