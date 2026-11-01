module leaf #(parameter int unsigned T = 8) (output logic [31:0] o); assign o = T; endmodule
module top #(parameter int unsigned GPTP_ETH_TICK_NS_P = 8) (output logic [31:0] o);
  if (1) begin : g
    localparam logic [(1 == 1 ? 31 : 31):0] GPTP_ETH_TICK_NS_P = 40;
    leaf #(.T(GPTP_ETH_TICK_NS_P)) u (.o(o));
  end
endmodule
