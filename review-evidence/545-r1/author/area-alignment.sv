module KL_slew_alignment(input wire axis_clk, axis_resetn, gptp_slew_active_w, output wire gptp_slew_eff_w);
  logic [3:0] gptp_slew_tail_r;
  assign gptp_slew_eff_w = gptp_slew_active_w || (|gptp_slew_tail_r);
  always_ff @(posedge axis_clk) begin : slew_rate_alignment
    if (!axis_resetn) gptp_slew_tail_r <= '0;
    else gptp_slew_tail_r <= {gptp_slew_tail_r[2:0], gptp_slew_active_w};
  end : slew_rate_alignment
endmodule
