/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`timescale 1ns/1ps
import ethernet_packet_pkg::*;

`include "parameters.svh"

module tb_traffic_queues;

  //! Parameter declaration, IP cores in DUT requires manually edit therfore no external
  //! parameter was used.
  localparam TDATA_WIDTH = 64;
  localparam TDEST_WIDTH = 2;
  localparam NUM_QUEUES = 4;
  localparam CLK_PERIOD = 8;

  //! Clock and async reset signal
  logic clk = 0;
  logic resetn = 0;
  //! DUT signals
  logic [NUM_QUEUES-1:0] queue_grant;
  wire [NUM_QUEUES-1:0] queue_has_data;

  //! DUT interfaces
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) s_axis();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) m_axis();



  //! Clock generation
  always #(CLK_PERIOD/2) clk = ~clk;

  //! Instantiate DUT
  traffic_queues #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .NUMBER_OF_QUEUES(NUM_QUEUES),
    .FIFO_DEPTH(32)
  ) dut (
    .clk(clk),
    .resetn(resetn),
    .queue_grant_i(queue_grant),
    .queue_has_data_o(queue_has_data),
    .s_axis(s_axis),
    .m_axis(m_axis)
  );

  // ------------------------------------------------------------------
  //! @brief Send ethernet frame to the queue based on input signal tdest will be assigned.
  //! @param[in] qid queue_id for determining which queue the packet will be stored in
  task automatic send_packet_to_queue(input int qid);
    logic [7:0] pkt[];
    int i;
    int j;

    pkt = new[128];

    foreach(pkt[i]) pkt[i] = i;

    j = 0;

    while (j < pkt.size()) begin
      s_axis.tdata = pkt[j] | (pkt[j+1] << 8);
      s_axis.tkeep = 8'hff;
      s_axis.tvalid = 1;
      s_axis.tlast = (j >= pkt.size() - 8);
      s_axis.tdest = qid;
      wait (s_axis.tready && clk);
      @(posedge clk);
      j += 8;
    end

    s_axis.tvalid = 0;
    s_axis.tlast = 0;
  endtask



  initial begin
    resetn = 0;
    s_axis.tvalid = 0;
    m_axis.tready = 1;
    queue_grant = 'b0000;

    //! reset generation
    repeat(5) @(posedge clk);
    resetn = 1;

    //! send some packet to DUT and they should be stored queue 0 and 2
    send_packet_to_queue(0);
    repeat(20) @(posedge clk); //! allow first packet to be fully accepted
    
    send_packet_to_queue(2);
    repeat(20) @(posedge clk); //! allow second packet to be accepted

    //! check queue_has_data output if it is correct
    $display("[CHECK] queue_has_data = %b", queue_has_data);
    assert(queue_has_data[0] && queue_has_data[2])
      else $fatal("[FAIL] FIFO queue has_data incorrect");

    $display("[PASS] traffic_queues FIFO write path test passed");
    $finish;
  end
endmodule
