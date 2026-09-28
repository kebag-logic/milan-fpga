// Evaluates the documented RETRY_BACKOFF_CYC_P form as a parameter of an
// `int unsigned CLK_HZ_P` (the pinned top's declaration) and compares it
// with an exact 64-bit ceil(CLK_HZ_P * 500 / 1000) reference.
module backoff_one #(parameter int unsigned CLK_HZ_P = 100_000_000,
                     parameter int unsigned RETRY_BACKOFF_CYC_P =
                       (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2)) (output logic ok);
  localparam longint unsigned REF = (64'(CLK_HZ_P) * 64'd500 + 64'd999) / 64'd1000;
  initial begin
    ok = (64'(RETRY_BACKOFF_CYC_P) == REF);
    $display("CLK_HZ_P=%0d BACKOFF=%0d REF=%0d %s", CLK_HZ_P, RETRY_BACKOFF_CYC_P, REF, ok ? "MATCH" : "MISMATCH");
  end
endmodule
module backoff_probe;
  logic [7:0] ok;
  backoff_one #(.CLK_HZ_P(32'd0))          u0 (.ok(ok[0]));
  backoff_one #(.CLK_HZ_P(32'd1))          u1 (.ok(ok[1]));
  backoff_one #(.CLK_HZ_P(32'd3))          u2 (.ok(ok[2]));
  backoff_one #(.CLK_HZ_P(32'd50_000_000)) u3 (.ok(ok[3]));
  backoff_one #(.CLK_HZ_P(32'd100_000_000))u4 (.ok(ok[4]));
  backoff_one #(.CLK_HZ_P(32'd156_250_001))u5 (.ok(ok[5]));
  backoff_one #(.CLK_HZ_P(32'hFFFF_FFFE))  u6 (.ok(ok[6]));
  backoff_one #(.CLK_HZ_P(32'hFFFF_FFFF))  u7 (.ok(ok[7]));
  initial begin
    #1;
    if (ok == 8'hFF) $display("BACKOFF_PROBE PASS 8/8");
    else $display("BACKOFF_PROBE FAIL ok=%b", ok);
    $finish;
  end
endmodule
