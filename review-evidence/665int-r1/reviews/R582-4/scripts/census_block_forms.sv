// R582-4: the escaping forms of census_block_probe.py in one module, to show
// each is legal SystemVerilog the pinned simulator elaborates.
module census_block_forms (input logic clk, input logic rstn, input logic c,
                           output logic q1, q2, q3, q4, q5, output wire q6);
  logic a1, a2, a3, a4, a5;
  always_ff @(posedge clk) if (c) begin a1 <= 1'b1; q1 <= 1'b1; end
  always_ff @(posedge clk) if (c) a2 <= 1'b1; else q2 <= 1'b1;
  always_comb case (c) 1'b0: a3 = 1'b1; default: q3 = 1'b1; endcase
  always_ff @(posedge clk iff (rstn)) begin if (c) begin a4 <= 1'b1; q4 <= 1'b1; end end
  always_ff @(posedge clk) begin a5 <= 1'b0; q5 |= c; end
  wire cw = c;
  alias cw = q6;
endmodule
