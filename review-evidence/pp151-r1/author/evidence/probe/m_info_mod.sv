`default_nettype none
module m_info_mod #(parameter int unsigned P_P = 1) (input wire a_i, output logic y_o);
  if (P_P > 4) begin : g_p_check
    $info("probe: P_P=%0d is refused", P_P);
  end
  assign y_o = a_i;
endmodule
`default_nettype wire
