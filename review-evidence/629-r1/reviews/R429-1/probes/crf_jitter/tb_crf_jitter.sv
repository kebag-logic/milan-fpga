// Disposable review probe (R429-1): how KL_crf_rx's timestamp-jump rule,
// which the proposed AAF clock meter inherits, treats picked timestamps that
// carry a bounded phase error. Stimulus: one CRF PDU per 2 ms (the meter's
// picked spacing), 0 ppm, with a per-PDU phase error that alternates +J/-J.
// IEEE 1722-2016 10.8 lets a CRF-following talker's timestamps sit anywhere
// within +/-5 % of a 48 kHz sample period (+/-1041.7 ns) of the timing points.
// Reports, per case, how many accepted PDUs saw rate_valid_o high.
`timescale 1ns/1ps
`default_nettype none
module tb_crf_jitter;
  localparam int CLK_HZ = 1_000_000;          // 1 MHz model clock: 2000 cycles / 2 ms
  localparam int CYC_PER_PDU = 2000;
  logic clk = 0, rst_n = 0;
  always #500 clk = ~clk;                     // 1 MHz

  logic        frame_p;
  logic [7:0]  seq;
  logic [63:0] ts, now;
  logic        en;
  wire signed [31:0] delta, rate;
  wire rate_valid, locked, mr_tog, dirty;
  wire [31:0] c0,c1,c2,c3,c4,c5,c6,c7,c8,c9;

  KL_crf_rx #(.CLK_FREQ_HZ_P(CLK_HZ), .IVAL_CYC_P(CLK_HZ)) dut (
    .clk_i(clk), .rst_n(rst_n),
    .frame_p_i(frame_p), .subtype_i(8'h04), .seq_i(seq),
    .sid_frame_i(64'h0011_2233_4455_0001),
    .pullbase_i({3'd0, 29'd48000}),
    .fsh_i({16'd8, 16'd96, ts[63:32]}), .fsh2_i({ts[31:0], 32'd0}),
    .type_i(8'h01), .mr_i(1'b0), .tu_i(1'b0), .ptp_now_i(now),
    .en_i(en), .sid_i(64'h0011_2233_4455_0001), .stop_i(1'b0),
    .delta_o(delta), .rate_o(rate), .rate_valid_o(rate_valid),
    .pdu_count_o(c0), .fmt_err_o(c1), .seq_err_o(c2), .mr_cnt_o(c3),
    .tu_cnt_o(c4), .late_cnt_o(c5), .early_cnt_o(c6), .locked_o(locked),
    .cnt_locked_o(c7), .cnt_unlocked_o(c8), .cnt_intr_o(c9),
    .dirty_p_o(dirty), .mr_toggle_p_o(mr_tog));

  task automatic run_case(input int jit_ns, input int n_pdu, output int n_valid,
                          output int n_locked);
    longint base;
    n_valid = 0; n_locked = 0;
    en = 0; frame_p = 0;
    repeat (4) @(posedge clk);
    en = 1;                                   // a fresh bind edge per case
    base = 64'd5_000_000_000;
    for (int n = 0; n < n_pdu; n++) begin
      repeat (CYC_PER_PDU - 1) @(posedge clk);
      ts  = base + 64'(n) * 64'd2_000_000 + ((n % 2) ? -64'(jit_ns) : 64'(jit_ns));
      now = ts - 64'd1_000_000;               // 1 ms ahead of arrival: not late, not early
      seq = 8'(n);
      frame_p = 1;
      @(posedge clk);
      frame_p = 0;
      #1;
      if (rate_valid) n_valid++;
      if (locked)     n_locked++;
    end
  endtask

  int v, l;
  initial begin
    frame_p = 0; seq = 0; ts = 0; now = 0; en = 0;
    repeat (5) @(posedge clk);
    rst_n = 1;
    foreach (cases[i]) begin
      run_case(cases[i], 600, v, l);
      $display("PROBE jitter=+/-%0d ns (pairwise spacing error %0d ns): accepted=600 locked=%0d rate_valid=%0d",
               cases[i], 2*cases[i], l, v);
    end
    $finish;
  end
  int cases[5] = '{0, 1000, 1023, 1041, 1042};
endmodule
`default_nettype wire
