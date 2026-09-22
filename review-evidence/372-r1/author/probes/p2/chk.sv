`default_nettype none
module chk (
  input wire clk,
  input wire rst_n,
  input wire a,
  input wire b,
  input wire y,
  input wire idle_i,
  input wire one_i,
  input wire two_i
);
  import "DPI-C" function void witness(input string name);
  default clocking cb @(posedge clk); endclocking
  default disable iff (!rst_n);
  ap_hold: assert property ((a && !b) |=> a)
    else $error("[SVA] ap_hold");
  ap_stable: assert property ((a && !b) |=> $stable(y) && $past(a))
    else $error("[SVA] ap_stable");
  am_env: assume property (!(a && b && !rst_n))
    else $error("[SVA] am_env");
  always_ff @(posedge clk) begin : imm
    if (rst_n && a) begin
      ai_y: assert (1'b1) witness("ai_pass"); else $error("[SVA] ai_y");
    end
  end
  logic unk_w;
  assign unk_w = $isunknown({a, b, y});
  always_ff @(posedge clk) begin : unk
    if (unk_w) witness("unknown_seen");
  end
  always_comb begin : combo
    ac_final: assert final (!(b && one_i)) else $error("[SVA] ac_final b while one");
  end
endmodule
`default_nettype wire
