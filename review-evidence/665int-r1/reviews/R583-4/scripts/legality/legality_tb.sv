// R583-4: each census escape form is legal SystemVerilog and carries the value it reads.
`include "inc.svh"
module legality_tb;
  logic clk = 1'b0;
  logic pp_cd_srp_over_limit_w;   // stands in for a class-D wire
  logic st;                       // stands in for a status consumer
  logic probe_a = 1'b0, probe_q = 1'b0;
  wire \probe//w ;
  assign \probe//w = pp_cd_srp_over_limit_w;
  wire \probe"a ;
  wire probe_w2;
  assign probe_w2 = pp_cd_srp_over_limit_w;
  wire \probe"b ;
  wire probe_m = `PROBE_CD(srp_over_limit);
  always_ff @(posedge clk) if (st) probe_a <= 1'b0; else probe_q <= 1'b1;
  initial begin
    pp_cd_srp_over_limit_w = 1'b1; st = 1'b1;
    #1 clk = 1'b1; #1 clk = 1'b0; #1;
    if (probe_q !== 1'b0) $fatal(1, "begin-less else branch moved while st=1");
    if (\probe//w !== 1'b1 || probe_w2 !== 1'b1 || probe_m !== 1'b1) $fatal(1, "escaped/macro read not 1");
    st = 1'b0; pp_cd_srp_over_limit_w = 1'b0;
    #1 clk = 1'b1; #1 clk = 1'b0; #1;
    if (probe_q !== 1'b1) $fatal(1, "begin-less else branch did not follow st");
    if (\probe//w !== 1'b0 || probe_w2 !== 1'b0 || probe_m !== 1'b0) $fatal(1, "escaped/macro read not 0");
    $display("LEGALITY PASS: begin-less if/else, // and quote escaped identifiers, include paste macro");
    $finish;
  end
endmodule
