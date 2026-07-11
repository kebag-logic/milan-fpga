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
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P)) m_axis_dut(clk, rst_n);
  axi_stream_driver #(.CLK_PERIOD_P(T), .TDATA_WIDTH_P(TDATA_WIDTH_P)) axis_driver;

  //! Sideband outputs from DUT
  logic        valid_dut;
  logic        drop_dut;
  logic [4:0]  status_dut;
  logic [3:0]  msg_type_dut;

  //! Packet counters
  int valid_count = 0;
  int drop_count  = 0;

  //! DUT instantiation
  KL_aecp_packet_validator DUT (
    .clk_i         (clk),
    .rst_n         (rst_n),
    .s_axis        (s_axis_dut),
    .m_axis        (m_axis_dut),
    .valid_o       (valid_dut),
    .drop_o        (drop_dut),
    .status_o      (status_dut),
    .message_type_o(msg_type_dut)
  );

  //! Clock generation: T/2 = 4 ns → 125 MHz
  always #(T/2) clk = ~clk;

  //! Monitor: accumulate valid/drop pulses
  always @(posedge clk) begin
    if (valid_dut) valid_count++;
    if (drop_dut)  drop_count++;
  end

  //! Drain m_axis — always ready so it never stalls the DUT
  always @(posedge clk) m_axis_dut.tready = 1'b1;

  // ------------------------------------------------------------------
  //! Task for resetting the DUT.
  task reset_dut;
    #100;
    $display("[INFO][TOP] : Resetting the DUT");
    rst_n = 1'b1;
  endtask

  // ------------------------------------------------------------------
  //! @brief Build a minimal AECP packet byte-queue.
  //! @param q        Output byte queue (cleared and rebuilt).
  //! @param msg_type 4-bit AECP message_type field.
  //! @param cdl      11-bit control_data_length value.
  function automatic void build_aecp_pkt(
    ref   logic [7:0] q[$],
    input bit  [3:0]  msg_type,
    input bit  [10:0] cdl
  );
    q = '{};
    // EtherType 0x22F0
    q.push_back(8'h22);
    q.push_back(8'hF0);
    // AECP subtype 0xFB
    q.push_back(8'hFB);
    // Byte 3: {sv=1, h=0, ver=3'b0, msg_type[3:0]}
    q.push_back({1'b1, 1'b0, 3'b0, msg_type});
    // Byte 4: {status[4:0]=0, cdl[10:8]}
    q.push_back({5'b0, cdl[10:8]});
    // Byte 5: cdl[7:0]
    q.push_back(cdl[7:0]);
    // Bytes 6-13: target_entity_id (8 bytes, random)
    repeat(8) q.push_back(logic'($urandom_range(0, 255)));
    // Bytes 14-21: controller_entity_id (8 bytes, random)
    repeat(8) q.push_back(logic'($urandom_range(0, 255)));
    // Bytes 22-23: sequence_id
    q.push_back(8'h00);
    q.push_back(8'h01);
    // Bytes 24-25: {u_flag=0, command_type=ACQUIRE_ENTITY}
    q.push_back(8'h00);
    q.push_back(8'h00);
    // Pad remaining bytes up to cdl (cdl is measured from byte 2 of the AVTP payload)
    // Payload bytes already pushed: 3..25 = 23 bytes; cdl counts from byte 6 offset
    // Fill to ensure packet is at least cdl bytes from byte index 6
    for (int i = 26; i < (int'(cdl) - 8 + 14); i++)
      q.push_back(8'h00);
  endfunction

  //! Main TB
  initial begin
    axis_driver         = new();
    axis_driver.axis_if = s_axis_dut;
    avtp_aecp_pkt_gen   = new();
    reset_dut();

    // ------------------------------------------------------------------
    // Test 1: 50 valid AEM_COMMAND packets (msg_type=0, cdl=20)
    // Expected: valid_o fires for each; drop_o stays low
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 1 — 50 valid AEM_COMMAND packets (msg_type=0, cdl=20)");
    for (int i = 0; i < 50; i++) begin
      build_aecp_pkt(pkt, 4'h0, 11'd20);
      #(T*4);
      axis_driver.drive_axi_stream(pkt);
      @(posedge clk iff (valid_dut || drop_dut));
      if (!valid_dut || drop_dut)
        $fatal(1, "[FATAL][TOP] Test 1 FAIL: expected valid_o=1 drop_o=0 on packet %0d, got valid=%0b drop=%0b",
               i, valid_dut, drop_dut);
    end
    if (valid_count !== 50)
      $fatal(1, "[FATAL][TOP] Test 1 FAIL: valid_count=%0d, expected 50", valid_count);
    $display("[INFO][TOP] : Test 1 PASS — %0d valid packets detected", valid_count);

    // ------------------------------------------------------------------
    // Test 2: 25 invalid message_type packets
    // Bad types: 2, 3, 4, 5 (cycled), cdl=20
    // Expected: drop_o fires, status_o = STATUS_INVALID_COMMAND (10)
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 2 — 25 invalid message_type packets");
    begin
      int drop_before = drop_count;
      for (int i = 0; i < 25; i++) begin
        bit [3:0] bad_type;
        bad_type = 4'h2 + i[1:0]; // cycles through 2, 3, 4, 5
        build_aecp_pkt(pkt, bad_type, 11'd20);
        #(T*4);
        axis_driver.drive_axi_stream(pkt);
        @(posedge clk iff (valid_dut || drop_dut));
        if (!drop_dut)
          $fatal(1, "[FATAL][TOP] Test 2 FAIL: expected drop_o on bad msg_type=%0d (packet %0d)",
                 bad_type, i);
        if (status_dut !== STATUS_INVALID_COMMAND)
          $fatal(1, "[FATAL][TOP] Test 2 FAIL: expected STATUS_INVALID_COMMAND(%0d), got %0d",
                 STATUS_INVALID_COMMAND, status_dut);
      end
      if (drop_count - drop_before !== 25)
        $fatal(1, "[FATAL][TOP] Test 2 FAIL: expected 25 drops, got %0d", drop_count - drop_before);
    end
    $display("[INFO][TOP] : Test 2 PASS — 25 invalid-msgtype drops detected");

    // ------------------------------------------------------------------
    // Test 3: 25 short CDL packets (cdl < 20, msg_type=0)
    // CDL values: 10, 11, ... 25 are generated, but we keep only cdl < 20
    // We use cdl = 0 .. 19 (all < 20) cycling via i % 20
    // Expected: drop_o fires, status_o = STATUS_BAD_ARGUMENTS (7)
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 3 — 25 short CDL packets (cdl < 20)");
    begin
      int drop_before = drop_count;
      for (int i = 0; i < 25; i++) begin
        bit [10:0] short_cdl;
        short_cdl = 11'(i % 20); // 0 .. 19, all below minimum
        build_aecp_pkt(pkt, 4'h0, short_cdl);
        #(T*4);
        axis_driver.drive_axi_stream(pkt);
        @(posedge clk iff (valid_dut || drop_dut));
        if (!drop_dut)
          $fatal(1, "[FATAL][TOP] Test 3 FAIL: expected drop_o on short CDL=%0d (packet %0d)",
                 short_cdl, i);
        if (status_dut !== STATUS_BAD_ARGUMENTS)
          $fatal(1, "[FATAL][TOP] Test 3 FAIL: expected STATUS_BAD_ARGUMENTS(%0d), got %0d",
                 STATUS_BAD_ARGUMENTS, status_dut);
      end
      if (drop_count - drop_before !== 25)
        $fatal(1, "[FATAL][TOP] Test 3 FAIL: expected 25 drops, got %0d", drop_count - drop_before);
    end
    $display("[INFO][TOP] : Test 3 PASS — 25 short-CDL drops detected");

    $display("[INFO][TOP] : kl-aecp-packet-validator utest PASS — valid=%0d drop=%0d",
             valid_count, drop_count);
    $finish;
  end

endmodule

`default_nettype wire
