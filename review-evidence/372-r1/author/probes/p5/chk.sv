`default_nettype none
module chk (
  input wire clk, input wire rst_n, input wire a, input wire b, input wire y,
  input wire idle_i, input wire one_i, input wire two_i
);
  import "DPI-C" function void witness(input string name);
  logic stall_q;
  always_ff @(posedge clk) begin : track
    if (!rst_n) stall_q <= 1'b0;
    else        stall_q <= a && !b;
  end
  always_ff @(posedge clk) begin : wit
    if (rst_n) begin
      cw_stall: cover (stall_q) witness("imm_cover_stall");
      aw_stall: assert (!stall_q || a) witness("imm_assert_pass"); else $error("[SVA] aw_stall");
    end
  end
  ap_hold: assert property (@(posedge clk) disable iff (!rst_n) (a && !b) |=> a) else $error("[SVA] ap_hold");
  wire unused_ok = &{1'b0, y, idle_i, one_i, two_i};
endmodule
`default_nettype wire
