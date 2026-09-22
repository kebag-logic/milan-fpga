// R239 scratch probe of pinned Verilator 5.050 behaviours the #372 guide states:
// two-state X, $isunknown, $past initial value, cover, assume.
`default_nettype none
module xprobe;
  logic clk = 1'b0;
  logic [7:0] v;
  logic [7:0] never_assigned;
  logic a = 1'b1;
  int edges = 0;
  initial begin
    v = 8'hxx;
    #1;
    $display("PROBE x-assign: v=%b isunknown(v)=%0d never_assigned=%b", v, $isunknown(v), never_assigned);
  end
  always #5 clk = ~clk;
  always @(posedge clk) begin
    edges <= edges + 1;
    if (edges == 0) $display("PROBE first-edge $past(a)=%0d (a is initialised 1)", $past(a));
    if (edges == 3) $finish;
  end
  cp_always: cover property (@(posedge clk) 1'b1) $display("PROBE cover hit at %0t", $time);
  am_never: assume property (@(posedge clk) edges < 2) else $display("PROBE assume failed at %0t", $time);
endmodule
`default_nettype wire
