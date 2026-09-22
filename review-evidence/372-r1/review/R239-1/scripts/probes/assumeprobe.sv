// R239 scratch probe: an assume property with NO action block, and an assert
// property with none, on pinned Verilator 5.050: what line does each print?
`default_nettype none
module assumeprobe;
  logic clk = 1'b0;
  int edges = 0;
  always #5 clk = ~clk;
  always @(posedge clk) begin
    edges <= edges + 1;
    if (edges == 3) $finish;
  end
  am_bare: assume property (@(posedge clk) edges < 2);
  ap_bare: assert property (@(posedge clk) edges < 2);
endmodule
`default_nettype wire
