/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`timescale 1ns/1ps
import ethernet_packet_pkg::*;

`include "parameters.svh"

module tb_traffic_classifier;

  //! Data width of AXI-Stream interface
  parameter int TDATA_WIDTH = `AXIS_DATA_WIDTH;
  //! Tdest width of AXIS interface
  parameter int TDEST_WIDTH = `AXIS_TDEST_WIDTH;
  //! Endianness configuration (1 for big endian)
  parameter bit BIG_ENDIAN = `USE_BIG_ENDIAN;
  //! Number of packets to generate
  parameter int NUM_PACKETS = 15;

  //! Clock and async reset signals
  logic clk = 0;
  logic aresetn = 0;

  //! Packet attributes for VLAN enable, PTP flag, and priority code point
  bit vlan_en;
  bit ptp;
  bit atdecc;
  byte pcp;
  logic[3:0] queue_has_data;

  //! Clock generation: 8ns period (125MHz)
  always #4 clk = ~clk;

  //! AXI-Stream slave interface for input packets
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) s_axis();
  //! AXI-Stream master interface for output packets with 3-bit tdest
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) m_axis();

  //! DUT instantiation with parameters
  traffic_classifier #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(BIG_ENDIAN),
    .FIFO_DEPTH(`ETH_FIFO_DEPTH)
  ) dut (
    .clk(clk),
    .resetn(aresetn),
    .s_axis(s_axis),
    .m_axis(m_axis)
  );


  // ------------------------------------------------------------------
  //! @brief Create an Ethernet packet with optional VLAN tag and PTP flag.
  //! @param[out] bytes Array of bytes containing the generated packet.
  //! @param[in] pcp Priority Code Point value for VLAN tag (default: 0).
  //! @param[in] include_vlan Enable VLAN tagging (default: 1).
  //! @param[in] ptp_packet Mark packet as PTP type (default: 0).
  function automatic void create_vlan_packet(
    output logic [7:0] bytes[],
    input byte pcp = 0,
    input bit include_vlan = 1,
    input bit ptp_packet = 0,
    input bit atdecc_packet = 0
  );
    int idx = 12;
    bytes = new[$urandom_range(64,1580)];
  
    // MAC Addresses
    bytes[ 0] = 8'hBA;
    bytes[ 1] = 8'hBA;
    bytes[ 2] = 8'hBA;
    bytes[ 3] = 8'hBA;
    bytes[ 4] = 8'hDE;
    bytes[ 5] = 8'hDE;
    bytes[ 6] = 8'hDE;
    bytes[ 7] = 8'hDE;
    bytes[ 8] = 8'h12;
    bytes[ 9] = 8'h34;
    bytes[10] = 8'h56;
    bytes[11] = 8'h78;
  
    if (include_vlan) begin
      bytes[idx + 0] = 8'h81;
      bytes[idx + 1] = 8'h00;
      bytes[idx + 2] = {pcp, 5'b00000};
      bytes[idx + 3] = 8'h00;
      idx += 4;
    end
  
    if (ptp_packet) begin
      bytes[idx + 0] = 8'h88;
      bytes[idx + 1] = 8'hF7;
    end 
    else if (atdecc_packet)begin
      bytes[idx + 0] = 8'h22;
      bytes[idx + 1] = 8'hF0;
    end
    else begin
      bytes[idx + 0] = 8'h80;
      bytes[idx + 1] = 8'h00;
    end
    idx += 2;
  
    for (int i = idx; i < bytes.size(); i++) begin
      bytes[i] = i;
    end
  
  endfunction
  

  // ------------------------------------------------------------------
  //! @brief Drive the packet bytes over the s_axis interface as AXI-Stream words.
  //! @param[in] bytes Array of bytes to send.
  task automatic drive_packet(input logic [7:0] bytes[]);
    int i = 0;
    logic [TDATA_WIDTH-1:0] word;
    logic [TDATA_WIDTH/8-1:0] keep;

    while (i < bytes.size()) begin
      word = 0;
      keep = 0;
      for (int b = 0; b < TDATA_WIDTH/8; b++) begin
        if (i + b < bytes.size()) begin
          word |= bytes[i + b] << (8*(BIG_ENDIAN ? (TDATA_WIDTH/8 - 1 - b) : b));
          keep[b] = 1;
        end
      end

      @(posedge clk);
      s_axis.tdata  <= word;
      s_axis.tkeep  <= keep;
      s_axis.tvalid <= 1;
      s_axis.tlast  <= ((i + TDATA_WIDTH/8) >= bytes.size());
      wait (s_axis.tready);
      i += TDATA_WIDTH/8;
    end

    @(posedge clk);
    s_axis.tvalid <= 0;
    s_axis.tlast  <= 0;
  endtask

  // ------------------------------------------------------------------
  //! @brief Check that the received packet has the expected priority code point in tdest.
  //! @param[in] expected_priority Expected priority.
  function automatic expect_tdest(input network_priority_t expected_priority);
    $display("[CHECK] Got tdest = %0d, expected = %0d", m_axis.tdest, expected_priority);
    assert(m_axis.tdest === expected_priority)
      else $fatal("[FAIL] TDEST mismatch! Got %0d, expected %0d", m_axis.tdest, expected_priority);
  endfunction

  // ------------------------------------------------------------------
  //! Main TB Sequence
  initial begin
    aresetn = 0;
    s_axis.tvalid = 0;
    m_axis.tready = 1;

    repeat (5) @(posedge clk);
    aresetn = 1;

    for (int i = 0; i < NUM_PACKETS; i++) begin
      logic [7:0] packet_bytes[];

      vlan_en = (i % 2 == 0);
      ptp     = (i == NUM_PACKETS-1) || (i == NUM_PACKETS-10)|| (i == NUM_PACKETS-4);
      atdecc  = i % 3 ;
      pcp    = i % 8;

      create_vlan_packet(packet_bytes, pcp, vlan_en, ptp, atdecc);
      $display("[TB] Sending packet #%0d - VLAN=%0b PTP=%0b PCP=%0d", i, vlan_en, ptp, pcp);

      drive_packet(packet_bytes);
      if (ptp)
        expect_tdest(GPTP_CLASS);
      else if(atdecc && vlan_en)
        expect_tdest(SRA_CLASS);
      else if (atdecc)
        expect_tdest(CONTROLL_CLASS);
      else
        expect_tdest(BEST_EFFORT);
    end
    $display("[PASS] classifier tdest segregation logic works");
    $finish;
  end

endmodule
