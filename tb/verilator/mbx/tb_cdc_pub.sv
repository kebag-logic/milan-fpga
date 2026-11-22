/*
* SPDX-FileCopyrightText: 2026 Kebag Logic
* SPDX-License-Identifier: CERN-OHL-W-2.0
*/
//! @file tb_cdc_pub.sv
//! @brief KL_mbx_cdc's gPTP publication crossing on its own (#884, REQ-PTP-07).
//!
//! The contract (mailbox.yaml, GPTP_STATE) makes a write whose GEN moved the
//! commit of every GPTP_* word, and the datapath takes each snapshot whole.
//! So every snapshot this bench sees land must be the words of one commit, in
//! the order they were committed, and each scenario's last commit must land,
//! whatever the firmware writes while a crossing is in flight. Two crossings
//! take the same register bank, the datapath clock under (50 MHz) and over
//! (125 MHz) the mailbox's 100 MHz. The stimulus writes one word a mailbox
//! cycle, faster than any processor store.
//!
//! The scenarios: an idle commit; a commit while one is in flight, then an
//! update begun and not committed (the ordering that tears a crossing of the live words); three
//! commits back to back; an update begun after an idle commit; a commit on the
//! edge the crossing takes the one before; GEN wrapping
//! through 0xFF; a write that leaves GEN where it was; reset of both clocks
//! and of the mailbox's alone with a crossing in flight.
// Built with --timescale 1ns/1ps (Makefile, run-cdc-pub): the RTL it takes names none.
`default_nettype none

module tb_cdc_pub;
  import KL_mbx_pkg::*;

  localparam int unsigned W_C = MBX_PUB_GPTP_WORDS_C * 32;
  localparam int unsigned STATE_C = (MBX_PUB_REG_GPTP_STATE_C - MBX_PUB_REG_GPTP_GM_LO_C) / 4;
  localparam int unsigned GEN_C = 32 * STATE_C + MBX_GPTP_STATE_GEN_LSB_C;

  logic sys_clk, dp_slow, dp_fast, sys_rst_n, dp_rst_n;
  initial begin
    sys_clk = 1'b0;
    forever #5 sys_clk = ~sys_clk;
  end
  initial begin
    dp_slow = 1'b0;
    forever #10 dp_slow = ~dp_slow;
  end
  initial begin
    dp_fast = 1'b0;
    forever #4 dp_fast = ~dp_fast;
  end

  //! KL_mbx's publication registers, as the firmware writes them
  logic [W_C-1:0] words;
  logic [W_C-1:0] got [2];
  logic           landed [2];

  // the crossing's other channels stay idle: this bench is the publication's
  /* verilator lint_off PINMISSING */
  KL_mbx_cdc u_slow (.sys_clk_i(sys_clk), .sys_rst_n(sys_rst_n), .dp_clk_i(dp_slow), .dp_rst_n(dp_rst_n),
                     .m_pub_gptp_i(words), .d_pub_gptp_o(got[0]), .d_pub_gptp_p_o(landed[0]));
  KL_mbx_cdc u_fast (.sys_clk_i(sys_clk), .sys_rst_n(sys_rst_n), .dp_clk_i(dp_fast), .dp_rst_n(dp_rst_n),
                     .m_pub_gptp_i(words), .d_pub_gptp_o(got[1]), .d_pub_gptp_p_o(landed[1]));
  /* verilator lint_on PINMISSING */

  // ---- the checker ----
  //! every commit since the last reset, index 0 the reset bank (all zero)
  logic [W_C-1:0] committed [$];
  int last [2];        //! index of the newest commit each crossing delivered
  int lands [2];
  int checks, failures;
  //! landings in commit order; across a reset any commit, or the reset bank, may land once more
  bit strict;

  task automatic check(input string label, input bit ok);
    checks++;
    if (!ok) failures++;
    $display("  [%s] %s", ok ? "PASS" : "FAIL", label);
  endtask

  //! a landing: one commit's words, newer than the one before (any commit across a reset)
  function automatic void landing(int d, logic [W_C-1:0] v);
    int at = -1;
    for (int i = strict ? last[d] + 1 : 0; i < committed.size(); i++) if (committed[i] == v) at = i;
    lands[d]++;
    checks++;
    if (at < 0) begin
      failures++;
      $display("  [FAIL] %s crossing landed GEN %0d words %h, not a commit newer than the last it took",
               d != 0 ? "the fast" : "the slow", v[GEN_C +: 8], v);
    end else begin
      last[d] = at;
    end
  endfunction

  always @(posedge dp_slow) if (dp_rst_n && landed[0]) landing(0, got[0]);
  always @(posedge dp_fast) if (dp_rst_n && landed[1]) landing(1, got[1]);

  // ---- the stimulus: one word a mailbox cycle ----
  task automatic put(input int k, input logic [31:0] v);
    @(negedge sys_clk);
    words[32 * k +: 32] = v;
  endtask

  //! GPTP_GM_LO, GPTP_GM_HI, then GPTP_STATE with GEN `gen`: a commit when GEN moves
  task automatic commit(input logic [63:0] gm, input logic [7:0] gen);
    logic [31:0] state = 32'(gen) << MBX_GPTP_STATE_GEN_LSB_C | 32'h0300;   // asCapable, SYNC_OK
    put(0, gm[31:0]);
    put(1, gm[63:32]);
    put(STATE_C, state);
    committed.push_back(words);
  endtask

  //! GPTP_STATE alone with GEN `gen`: the other words stand, and GEN's move commits them all again
  task automatic commit_state(input logic [7:0] gen);
    put(STATE_C, 32'(gen) << MBX_GPTP_STATE_GEN_LSB_C | 32'h0300);
    committed.push_back(words);
  endtask

  task automatic quiet();
    repeat (80) @(negedge sys_clk);
  endtask

  //! the scenario's last commit landed on both crossings
  task automatic newest_landed(input string label);
    quiet();
    check({label, ": the last commit landed, slow"}, last[0] == committed.size() - 1);
    check({label, ": the last commit landed, fast"}, last[1] == committed.size() - 1);
  endtask

  task automatic reset(input bit dp_too);
    strict = 1'b0;
    @(negedge sys_clk);
    sys_rst_n = 1'b0;
    if (dp_too) dp_rst_n = 1'b0;
    words = '0;                         // KL_mbx's registers reset with the mailbox
    repeat (5) @(negedge sys_clk);
    sys_rst_n = 1'b1;
    dp_rst_n = 1'b1;
  endtask

  int lands_then [2];
  initial begin
    sys_rst_n = 1'b0;
    dp_rst_n = 1'b0;
    words = '0;
    checks = 0;
    failures = 0;
    strict = 1'b1;
    committed.push_back('0);
    last = '{0, 0};
    lands = '{0, 0};
    repeat (4) @(negedge sys_clk);
    sys_rst_n = 1'b1;
    dp_rst_n = 1'b1;
    repeat (4) @(negedge sys_clk);

    commit(64'h1111_1111_1111_1111, 8'd1);
    newest_landed("an idle commit");

    commit(64'h1212_1212_1212_1212, 8'd2);
    commit(64'h2222_2222_2222_2222, 8'd3);   // committed while the one before crosses
    put(0, 32'h3333_3333);                   // the next update begun, not committed
    newest_landed("a commit while one crosses, then an update begun");

    commit(64'h4444_4444_4444_4444, 8'd4);
    commit(64'h5555_5555_5555_5555, 8'd5);
    commit(64'h6666_6666_6666_6666, 8'd6);
    newest_landed("three commits back to back");

    commit(64'h7777_7777_7777_7777, 8'd7);
    put(0, 32'h8888_8888);
    put(1, 32'h8888_8888);
    newest_landed("an update begun after an idle commit");

    // the idle crossing raises its send the cycle after a commit and takes the bank the cycle after that: a
    // second commit two mailbox cycles after the first lands on that very edge, and must still be sent
    commit(64'h7878_7878_7878_7878, 8'd8);
    @(negedge sys_clk);
    commit_state(8'd9);
    newest_landed("a commit on the edge the crossing takes the one before");

    commit(64'h0000_00FE_0000_00FE, 8'hFE);
    newest_landed("GEN at 0xFE");
    commit(64'h0000_00FF_0000_00FF, 8'hFF);
    newest_landed("GEN at 0xFF");
    commit(64'h0000_0100_0000_0100, 8'h00);
    newest_landed("GEN wrapped to 0x00");
    commit(64'h0000_0101_0000_0101, 8'h01);
    newest_landed("GEN at 0x01 after the wrap");

    lands_then = lands;
    put(0, 32'h9999_9999);
    put(1, 32'h9999_9999);
    put(STATE_C, words[32 * STATE_C +: 32] ^ 32'h0000_0100);   // asCapable moves, GEN does not
    quiet();
    check("a write that leaves GEN where it was crosses nothing",
          lands[0] == lands_then[0] && lands[1] == lands_then[1]);

    commit(64'hAAAA_AAAA_AAAA_AAAA, 8'h10);
    repeat (2) @(negedge sys_clk);
    reset(1'b1);
    commit(64'hBBBB_BBBB_BBBB_BBBB, 8'h11);
    newest_landed("reset of both clocks with a crossing in flight");
    strict = 1'b1;

    commit(64'hCCCC_CCCC_CCCC_CCCC, 8'h12);
    repeat (2) @(negedge sys_clk);
    reset(1'b0);
    commit(64'hDDDD_DDDD_DDDD_DDDD, 8'h13);
    newest_landed("reset of the mailbox's clock alone with a crossing in flight");
    strict = 1'b1;

    $display("== mbx gPTP publication crossing (KL_mbx_cdc): checks: %0d   failures: %0d ==", checks, failures);
    if (failures != 0) $fatal(1, "a snapshot landed that no commit made, or a commit never landed");
    $finish;
  end
endmodule

`default_nettype wire
