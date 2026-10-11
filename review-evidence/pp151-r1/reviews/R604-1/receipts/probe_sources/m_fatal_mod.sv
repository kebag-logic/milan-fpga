module probe #(parameter int P = 0) (input logic a_i, output logic b_o);
  assign b_o = a_i;
  if (P != 0) begin : g_chk
    $fatal(1, "probe: P=%0d violates", P);
  end
endmodule
