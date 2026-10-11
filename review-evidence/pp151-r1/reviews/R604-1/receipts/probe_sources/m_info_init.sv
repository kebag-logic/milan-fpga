module probe #(parameter int P = 0) (input logic a_i, output logic b_o);
  assign b_o = a_i;
  initial begin : g_chk
    if (P != 0)
      $info("probe: P=%0d violates", P);
  end
endmodule
