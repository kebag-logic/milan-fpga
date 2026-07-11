/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`default_nettype none

module tb_top();

  `include "avtp_packet_gen_pkg.svh"
  `include "axi_stream_driver.svh"

  import aecp_pkg::*;
  import avtp_aecp_pkg::*;

  //! AECP packet generator
  avtp_aecp_packet_gen avtp_aecp_pkt_gen;
  logic [7:0] pkt[$];

  //! Parameters for AXI4-Stream interface and Clock
  parameter TDATA_WIDTH_P = 64;
  parameter T = 8; // 125 MHz

  bit clk;
  bit rst_n;

  //! Interfaces
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P)) s_axis_dut(clk, rst_n);
  axi_stream_driver #(.CLK_PERIOD_P(T), .TDATA_WIDTH_P(TDATA_WIDTH_P)) axis_driver;

  //! Parsed header output from DUT
  aecp_hdr_t hdr_out;
  logic      mismatch_out;

  //! Known entity IDs used in tests
  localparam [63:0] MY_ENTITY_ID  = 64'h001BC5_FFFE_AABBCC;
  localparam [63:0] BAD_ENTITY_ID = 64'hDEADBEEF_CAFEF00D;
  localparam [63:0] CTLR_ID       = 64'hAABBCCDD_EEFF0011;

  //! DUT instantiation
  KL_aecp_common_parser DUT (
    .clk_i       (clk),
    .rst_n       (rst_n),
    .entity_id_i (MY_ENTITY_ID),
    .s_axis      (s_axis_dut),
    .hdr_o       (hdr_out),
    .mismatch_o  (mismatch_out)
  );

  //! Clock generation: T/2 = 4 ns → 125 MHz
  always #(T/2) clk = ~clk;

  // ------------------------------------------------------------------
  //! Task: reset the DUT.
  task reset_dut;
    #100;
    $display("[INFO][TOP] : Resetting the DUT");
    rst_n = 1'b1;
  endtask

  //! Main TB
  initial begin
    axis_driver         = new();
    axis_driver.axis_if = s_axis_dut;
    avtp_aecp_pkt_gen   = new();
    reset_dut();

    // ------------------------------------------------------------------
    // Test 1: ACQUIRE_ENTITY command to MY_ENTITY_ID
    // Expected: hdr_o.hdr_valid fires, hdr_o.command_type == CMD_ACQUIRE_ENTITY,
    //           hdr_o.target_entity_id == MY_ENTITY_ID, mismatch_o == 0
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 1 — ACQUIRE_ENTITY to MY_ENTITY_ID");
    begin
      avtp_aecp_acquire_t sent_pkt;
      sent_pkt = avtp_aecp_pkt_gen.aecp_acquire_entity_gen(
        pkt,
        MY_ENTITY_ID,   // tgt_eid
        CTLR_ID,        // ctlr_eid
        16'h0001,       // seq_id
        32'h0000_0000,  // flags (no release, no persistent)
        CTLR_ID         // owner_id
      );
      #(T*4);
      fork
        begin
          axis_driver.drive_axi_stream(pkt);
        end
        begin
          @(posedge clk iff hdr_out.hdr_valid);
        end
      join

      if (hdr_out.command_type !== CMD_ACQUIRE_ENTITY)
        $fatal(1, "[FATAL][TOP] Test 1 FAIL: command_type=%0d, expected CMD_ACQUIRE_ENTITY(%0d)",
               hdr_out.command_type, CMD_ACQUIRE_ENTITY);
      if (hdr_out.target_entity_id !== MY_ENTITY_ID)
        $fatal(1, "[FATAL][TOP] Test 1 FAIL: target_entity_id=0x%016h, expected 0x%016h",
               hdr_out.target_entity_id, MY_ENTITY_ID);
      if (hdr_out.controller_entity_id !== CTLR_ID)
        $fatal(1, "[FATAL][TOP] Test 1 FAIL: controller_entity_id=0x%016h, expected 0x%016h",
               hdr_out.controller_entity_id, CTLR_ID);
      if (hdr_out.message_type !== MSG_AEM_COMMAND)
        $fatal(1, "[FATAL][TOP] Test 1 FAIL: message_type=%0d, expected MSG_AEM_COMMAND(%0d)",
               hdr_out.message_type, MSG_AEM_COMMAND);
      if (mismatch_out)
        $fatal(1, "[FATAL][TOP] Test 1 FAIL: mismatch_o=1 for matching entity_id");
      $display("[INFO][TOP] : Test 1 PASS — ACQUIRE_ENTITY parsed correctly, mismatch=0");
    end

    // ------------------------------------------------------------------
    // Test 2: ACQUIRE_ENTITY command to BAD_ENTITY_ID (wrong target)
    // Expected: mismatch_o fires; hdr_o.hdr_valid may or may not fire
    //           (implementation-defined), but mismatch_o must be asserted.
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 2 — ACQUIRE_ENTITY to BAD_ENTITY_ID (mismatch expected)");
    begin
      avtp_aecp_acquire_t sent_pkt;
      sent_pkt = avtp_aecp_pkt_gen.aecp_acquire_entity_gen(
        pkt,
        BAD_ENTITY_ID,  // tgt_eid — deliberately wrong
        CTLR_ID,
        16'h0002,
        32'h0000_0000,
        CTLR_ID
      );
      #(T*4);
      fork
        begin
          axis_driver.drive_axi_stream(pkt);
        end
        begin
          @(posedge clk iff (mismatch_out || hdr_out.hdr_valid));
        end
      join

      if (!mismatch_out)
        $fatal(1, "[FATAL][TOP] Test 2 FAIL: expected mismatch_o=1 for wrong target_entity_id");
      $display("[INFO][TOP] : Test 2 PASS — mismatch_o fired for wrong entity_id");
    end

    // ------------------------------------------------------------------
    // Test 3: READ_DESCRIPTOR command — verify descriptor fields parsed
    // Expected: hdr_o.command_type == CMD_READ_DESCRIPTOR,
    //           hdr_o.configuration_index, descriptor_type, descriptor_index correct
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 3 — READ_DESCRIPTOR command field parsing");
    begin
      avtp_aecp_read_desc_t sent_pkt;
      sent_pkt = avtp_aecp_pkt_gen.aecp_read_descriptor_gen(
        pkt,
        MY_ENTITY_ID,
        CTLR_ID,
        16'h0003,  // seq_id
        16'h0001,  // cfg_idx
        16'h0002,  // desc_type (AUDIO_UNIT)
        16'h0000   // desc_idx
      );
      #(T*4);
      fork
        begin
          axis_driver.drive_axi_stream(pkt);
        end
        begin
          @(posedge clk iff hdr_out.hdr_valid);
        end
      join

      if (hdr_out.command_type !== CMD_READ_DESCRIPTOR)
        $fatal(1, "[FATAL][TOP] Test 3 FAIL: command_type=%0d, expected CMD_READ_DESCRIPTOR(%0d)",
               hdr_out.command_type, CMD_READ_DESCRIPTOR);
      if (hdr_out.configuration_index !== 16'h0001)
        $fatal(1, "[FATAL][TOP] Test 3 FAIL: configuration_index=%0h, expected 0x0001",
               hdr_out.configuration_index);
      if (hdr_out.descriptor_type !== 16'h0002)
        $fatal(1, "[FATAL][TOP] Test 3 FAIL: descriptor_type=%0h, expected 0x0002",
               hdr_out.descriptor_type);
      if (hdr_out.descriptor_index !== 16'h0000)
        $fatal(1, "[FATAL][TOP] Test 3 FAIL: descriptor_index=%0h, expected 0x0000",
               hdr_out.descriptor_index);
      if (mismatch_out)
        $fatal(1, "[FATAL][TOP] Test 3 FAIL: mismatch_o=1 for matching entity_id");
      $display("[INFO][TOP] : Test 3 PASS — READ_DESCRIPTOR fields parsed correctly");
    end

    $display("[INFO][TOP] : kl-aecp-common-parser utest PASS");
    $finish;
  end

endmodule

`default_nettype wire
