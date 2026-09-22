`default_nettype none
module chk (
  input wire clk, input wire rst_n, input wire a, input wire b, input wire y,
  input wire idle_i, input wire one_i, input wire two_i
);
  default clocking cb @(posedge clk); endclocking
  default disable iff (!rst_n);
  am_env: assume property (!(a && b))
    else $error("[SVA] am_env: a and b together");
  always_comb begin : combo
    ac_final: assert final (!(b && one_i)) else $error("[SVA] ac_final: b while one");
  end
  wire unused_ok = &{1'b0, y, idle_i, two_i};
endmodule
`default_nettype wire
