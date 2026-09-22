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
  // T4 probe: a && !b |=> a  (like valid && !ready |=> valid)
  ap_hold: assert property (@(posedge clk) disable iff (!rst_n) (a && !b) |=> a)
    else $error("[SVA] ap_hold: a dropped while b low");
  ap_legal: assert property (@(posedge clk) disable iff (!rst_n) $onehot({idle_i, one_i, two_i}));
  cp_stall: cover property (@(posedge clk) disable iff (!rst_n) (a && !b)) witness("cp_stall");
  always_ff @(posedge clk) begin : imm
    if (rst_n && a) begin
      ai_y: assert (1'b1) witness("ai_pass"); else $error("[SVA] ai_y");
    end
  end
  always_comb begin : combo
    ac_final: assert final (!(idle_i && one_i)) else $error("[SVA] ac_final");
  end
  final begin : fin
    $display("CHK-FINAL %m");
  end
endmodule
`default_nettype wire
