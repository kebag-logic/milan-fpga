module sd(input logic a_i, output logic y_o);
  assign y_o = a_i;
endmodule
module second_driver(input logic a_i, output logic z_o);
  wire w = 1'b0;          // declaration initialiser: a continuous driver
  sd u (.a_i(a_i), .y_o(w));
  assign z_o = w;
endmodule
