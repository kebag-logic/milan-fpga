/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`timescale 1ns/1ps
import ethernet_packet_pkg::*;

`include "parameters.svh"

module tb_traffic_controller_802_1q;

  //! Data width of AXI-Stream interface
  parameter int TDATA_WIDTH = `AXIS_DATA_WIDTH;
  //! Tdest width of AXIS interface
  parameter int TDEST_WIDTH = `AXIS_TDEST_WIDTH;
  //! Endianness configuration (1 for big endian)
  parameter bit BIG_ENDIAN = `USE_BIG_ENDIAN;
  //! Number of packets to generate
  parameter int NUM_PACKETS = 100;

  //! Clock and async reset signals
  logic clk = 0;
  logic aresetn = 0;

  //! Packet attributes for VLAN enable, PTP flag, and priority code point
  bit vlan_en;
  bit ptp;
  bit atdecc;
  byte pcp;
  logic[3:0] queue_has_data;

  //! Clock generation: 5ns period (100MHz)
  always #5 clk = ~clk;

  //! AXI-Stream slave interface for input packets
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) s_axis();
  //! AXI-Stream master interface for output packets with 3-bit tdest
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) m_axis();
  
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) buffer_m_axis();

  //! DUT instantiation
  traffic_controller_802_1q #(
  .TDATA_WIDTH(TDATA_WIDTH),
  .BIG_ENDIAN(BIG_ENDIAN),
  .CLASSIFIER_FIFO_DEPTH(64),
  .NUMBER_OF_QUEUES(4),
  .BUFFER_FIFO_DEPTH(16384)
  )dut(
  .clk(clk),
  .resetn(aresetn),
  .is_1g_i('d1),

  .s_axis(s_axis),
  .m_axis(buffer_m_axis)
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


task automatic send_packet_of_class(network_priority_t cls, int pcp = 0);
  logic [7:0] packet_bytes[];
  bit vlan_en, ptp, atdecc;

  vlan_en = 0;
  ptp     = 0;
  atdecc  = 0;

  case (cls)
    SRA_CLASS: begin
      vlan_en = 1;
      atdecc  = 1;
    end

    CONTROL_CLASS: begin
      vlan_en = 0;
      atdecc  = 1;
    end

    GPTP_CLASS: begin
      vlan_en = 0; // optional, could also test with VLAN=1
      ptp     = 1;
    end

    BEST_EFFORT: begin
      vlan_en = 1;
      ptp     = 0;
      atdecc  = 0; // use IPv4 eth_type in create_vlan_packet
    end
  endcase

  create_vlan_packet(packet_bytes, pcp, vlan_en, ptp, atdecc);
  $display("[TB] Sending %s packet (PCP=%0d VLAN=%0b PTP=%0b ATDECC=%0b)",
           cls.name(), pcp, vlan_en, ptp, atdecc);
  drive_packet(packet_bytes);
endtask
  // ------------------------------------------------------------------
  //! Main TB Sequence
  initial begin
    aresetn = 0;
    s_axis.tvalid = 0;
   // m_axis.tready = 1;
    buffer_m_axis.tready = 1;

    repeat (5) @(posedge clk);
    aresetn = 1;

    for (int i = 0; i < NUM_PACKETS; i++) begin
      send_packet_of_class(SRA_CLASS,      i % 4);
      send_packet_of_class(CONTROL_CLASS,  i % 8);
      send_packet_of_class(GPTP_CLASS);
      send_packet_of_class(BEST_EFFORT);
    end

  end

endmodule
