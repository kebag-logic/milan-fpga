module t #(parameter int unsigned L = 568) (input logic clk_i, output logic o);
  if (L < 576) begin : g_floor
    `ifdef USE_FATAL
    $fatal(1, "L=%0d is below 576", L);
    `else
    $error("L=%0d is below 576", L);
    `endif
  end
  assign o = clk_i;
endmodule
