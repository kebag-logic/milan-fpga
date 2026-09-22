// Reviewer-owned measurement; the stream checker is the exact reviewed source.
`timescale 1ns/1ps
module semantics_probe(
  input wire clk, rst_n, valid, ready,
  input wire [7:0] data,
  input wire keep, last
);
  logic one = 1'b1;
  import "DPI-C" context function void probe_result(input string rule_name, input bit passed);
  axis_stream_source_sva #(.TDATA_WIDTH_P(8)) real_checker(
    .clk_i(clk), .rst_n(rst_n), .tvalid_i(valid), .tready_i(ready),
    .tdata_i(data), .tkeep_i(keep), .tlast_i(last)
  );
  ap_past_one: assert property (@(posedge clk) $past(one) == 1'b1)
    probe_result("past_one", 1'b1);
  else probe_result("past_one", 1'b0);
  ap_stable_one: assert property (@(posedge clk) $stable(one))
    probe_result("stable_one", 1'b1);
  else probe_result("stable_one", 1'b0);
  // Deliberately incorrect flag: demonstrates the false coverage F1 describes.
  ap_bad_flag: assert property (@(posedge clk) disable iff (!rst_n) (valid && !ready) |=> valid)
    probe_result("bad_flag", $past(valid && !ready));
  else probe_result("unexpected_fail", 1'b1);
endmodule
