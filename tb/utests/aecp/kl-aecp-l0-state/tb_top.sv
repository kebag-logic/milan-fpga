/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`default_nettype none

module tb_top();

  import aecp_pkg::*;

  //! Clock parameter: T=8 → 125 MHz
  parameter T = 8;

  bit clk;
  bit rst_n;

  //! Clock generation
  always #(T/2) clk = ~clk;

  //! DUT inputs
  logic [63:0]    entity_id  = 64'h001BC5_FFFE_112233;
  aecp_hdr_t      hdr;
  logic           tick_1khz;
  logic           cmd_done;

  //! DUT outputs
  aecp_l0_state_t l0_state;
  logic [4:0]     status;
  logic           reject;

  //! DUT instantiation
  KL_aecp_l0_state DUT (
    .clk_i       (clk),
    .rst_n       (rst_n),
    .entity_id_i (entity_id),
    .hdr_i       (hdr),
    .tick_1khz_i (tick_1khz),
    .cmd_done_i  (cmd_done),
    .l0_state_o  (l0_state),
    .status_o    (status),
    .reject_o    (reject)
  );

  //! Known controller entity IDs
  localparam [63:0] C1 = 64'hAABBCCDDEEFF0011;
  localparam [63:0] C2 = 64'h1122334455667788;

  // ------------------------------------------------------------------
  //! Task: reset DUT and initialise all inputs to safe defaults.
  task reset_dut;
    hdr       = '0;
    tick_1khz = 1'b0;
    cmd_done  = 1'b0;
    #100;
    $display("[INFO][TOP] : Resetting the DUT");
    rst_n = 1'b1;
    repeat(5) @(posedge clk);
  endtask

  // ------------------------------------------------------------------
  //! @brief Drive one AECP header into hdr_i and pulse cmd_done.
  //! @param cmd_type  15-bit AEM command_type.
  //! @param ctlr      64-bit controller_entity_id.
  task automatic send_cmd(
    input bit [14:0] cmd_type,
    input bit [63:0] ctlr
  );
    @(posedge clk);
    hdr.hdr_valid            = 1'b1;
    hdr.message_type         = MSG_AEM_COMMAND;
    hdr.command_type         = cmd_type;
    hdr.target_entity_id     = entity_id;
    hdr.controller_entity_id = ctlr;
    hdr.sequence_id          = 16'($urandom);
    hdr.status               = 5'd0;
    hdr.control_data_length  = 11'd20;
    hdr.u_flag               = 1'b0;
    @(posedge clk);
    hdr.hdr_valid = 1'b0;
    // Allow pipeline to settle, then assert cmd_done for one cycle
    repeat(2) @(posedge clk);
    @(posedge clk); cmd_done = 1'b1;
    @(posedge clk); cmd_done = 1'b0;
    repeat(2) @(posedge clk);
  endtask

  // ------------------------------------------------------------------
  //! @brief Generate N 1 kHz tick pulses (one cycle high, one cycle low each).
  task automatic gen_ticks(input int n);
    for (int i = 0; i < n; i++) begin
      @(posedge clk); tick_1khz = 1'b1;
      @(posedge clk); tick_1khz = 1'b0;
    end
  endtask

  //! Main TB
  initial begin
    reset_dut();

    // ------------------------------------------------------------------
    // Test 1: initial state — locked=0, acquired=0
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 1 — initial state after reset");
    if (l0_state.locked || l0_state.acquired)
      $fatal(1, "[FATAL][TOP] Test 1 FAIL: expected locked=0 acquired=0 after reset, got locked=%0b acquired=%0b",
             l0_state.locked, l0_state.acquired);
    $display("[INFO][TOP] : Test 1 PASS — initial state locked=0 acquired=0");

    // ------------------------------------------------------------------
    // Test 2: LOCK_ENTITY from C1 → locked=1, status=SUCCESS
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 2 — LOCK_ENTITY from C1");
    send_cmd(CMD_LOCK_ENTITY, C1);
    if (!l0_state.locked)
      $fatal(1, "[FATAL][TOP] Test 2 FAIL: expected locked=1 after LOCK_ENTITY");
    if (status !== STATUS_SUCCESS)
      $fatal(1, "[FATAL][TOP] Test 2 FAIL: expected STATUS_SUCCESS(%0d), got %0d", STATUS_SUCCESS, status);
    $display("[INFO][TOP] : Test 2 PASS — LOCK_ENTITY accepted, locked=1, status=SUCCESS");

    // ------------------------------------------------------------------
    // Test 3: SET_NAME from C2 while entity locked by C1
    // Expected: reject_o=1, status=STATUS_ENTITY_LOCKED (3)
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 3 — SET_NAME from C2 while locked by C1");
    send_cmd(CMD_SET_NAME, C2);
    if (!reject)
      $fatal(1, "[FATAL][TOP] Test 3 FAIL: expected reject_o=1 when locked entity accessed by C2");
    if (status !== STATUS_ENTITY_LOCKED)
      $fatal(1, "[FATAL][TOP] Test 3 FAIL: expected STATUS_ENTITY_LOCKED(%0d), got %0d",
             STATUS_ENTITY_LOCKED, status);
    $display("[INFO][TOP] : Test 3 PASS — SET_NAME from C2 rejected with ENTITY_LOCKED");

    // ------------------------------------------------------------------
    // Test 4: lock auto-releases after LOCK_TIMER_TICKS_C (60000) ticks
    // Drive 60001 tick pulses and verify locked clears
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 4 — lock auto-release after 60001 1-kHz ticks");
    gen_ticks(60_001);
    repeat(2) @(posedge clk);
    if (l0_state.locked)
      $fatal(1, "[FATAL][TOP] Test 4 FAIL: expected locked=0 after lock timer expiry (60001 ticks)");
    $display("[INFO][TOP] : Test 4 PASS — lock auto-released after 60001 ticks");

    // ------------------------------------------------------------------
    // Test 5: C2 can now SET_NAME after lock has cleared → status=SUCCESS
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 5 — SET_NAME from C2 after lock released");
    send_cmd(CMD_SET_NAME, C2);
    if (reject)
      $fatal(1, "[FATAL][TOP] Test 5 FAIL: expected reject_o=0 now that lock has cleared");
    if (status !== STATUS_SUCCESS)
      $fatal(1, "[FATAL][TOP] Test 5 FAIL: expected STATUS_SUCCESS, got %0d", status);
    $display("[INFO][TOP] : Test 5 PASS — SET_NAME from C2 accepted after lock cleared");

    // ------------------------------------------------------------------
    // Test 6: ACQUIRE_ENTITY from C1 → acquired=1, acquiring_controller_id=C1
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 6 — ACQUIRE_ENTITY from C1");
    send_cmd(CMD_ACQUIRE_ENTITY, C1);
    if (!l0_state.acquired)
      $fatal(1, "[FATAL][TOP] Test 6 FAIL: expected acquired=1 after ACQUIRE_ENTITY");
    if (l0_state.acquiring_controller_id !== C1)
      $fatal(1, "[FATAL][TOP] Test 6 FAIL: acquiring_controller_id mismatch — got 0x%016h, expected 0x%016h",
             l0_state.acquiring_controller_id, C1);
    if (status !== STATUS_SUCCESS)
      $fatal(1, "[FATAL][TOP] Test 6 FAIL: expected STATUS_SUCCESS, got %0d", status);
    $display("[INFO][TOP] : Test 6 PASS — ACQUIRE_ENTITY accepted, acquired=1, controller_id=C1");

    // ------------------------------------------------------------------
    // Test 7: ACQUIRE_ENTITY (RELEASE) from C1 → acquired=0
    // Note: release is signalled by setting the u_flag or a flags field
    // in the payload; since hdr_i only carries the parsed common header,
    // the release path depends on higher-level decode of the payload.
    // We drive the command here; if release decode is not yet implemented
    // this test is marked as informational and deferred.
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 7 NOTE — ACQUIRE_ENTITY RELEASE path (payload flags required)");
    @(posedge clk);
    hdr.hdr_valid            = 1'b1;
    hdr.command_type         = CMD_ACQUIRE_ENTITY;
    hdr.controller_entity_id = C1;
    hdr.u_flag               = 1'b1; // release indication via u_flag (implementation-defined)
    @(posedge clk);
    hdr.hdr_valid = 1'b0;
    repeat(2) @(posedge clk);
    @(posedge clk); cmd_done = 1'b1;
    @(posedge clk); cmd_done = 1'b0;
    repeat(2) @(posedge clk);
    $display("[INFO][TOP] : Test 7 NOTE — ACQUIRE RELEASE deferred; flags decoded from packet payload");

    $display("[INFO][TOP] : kl-aecp-l0-state utest COMPLETE — all implemented tests PASS");
    $finish;
  end

endmodule

`default_nettype wire
