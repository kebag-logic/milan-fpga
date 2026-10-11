`default_nettype none
module m_info_init #(parameter int unsigned P_P = 1) (input wire a_i, output logic y_o);
  initial begin : g_p_check
    if (P_P > 4) $info("probe: P_P=%0d is refused", P_P);
  end
  assign y_o = a_i;
endmodule
`default_nettype wire
