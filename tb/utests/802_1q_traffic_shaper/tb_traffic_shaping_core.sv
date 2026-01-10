/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`timescale 1ns/1ps
import ethernet_packet_pkg::*;
`include "parameters.svh"

module tb_traffic_shaping_core;

  //! Local parameters
  localparam TDATA_WIDTH = `AXIS_DATA_WIDTH;
  localparam NUM_QUEUES = 4;
  localparam CLK_PERIOD = 8;

  //! Clock and reset DUT signal declerations
  logic clk = 0;
  logic resetn = 0;
  logic [NUM_QUEUES-1:0] queue_has_data;
  wire [NUM_QUEUES-1:0] grant_queue;

  //! DUT interface declaration
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(2)) s_axis();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(2)) m_axis();

  //! Clock generation
  always #(CLK_PERIOD/2) clk = ~clk;

  //! DUT instantiation
  traffic_shaping_core #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .NUMBER_OF_QUEUES(NUM_QUEUES)
  ) dut (
    .clk(clk),
    .resetn(resetn),
    .queue_has_data_i(queue_has_data),
    .is_1g_i('d1),
    .grant_queue_o(grant_queue),
    .s_axis(s_axis),
    .m_axis(m_axis)
  );

  initial begin

    //! Reset generation
    resetn = 0;
    s_axis.tvalid = 0;
    m_axis.tready = 1;
    queue_has_data = 4'b0010;

    repeat(5) @(posedge clk);
    resetn = 1;

    //! Send a mock packet
    @(posedge clk);
    s_axis.tvalid = 1;
    s_axis.tkeep = 8'hFF;
    s_axis.tdata = 64'hAABBCCDDEEFF1122;
    s_axis.tdest = 2;
    s_axis.tlast = 1;

    @(posedge clk);
    s_axis.tvalid = 0;

    repeat (3) @(posedge clk);
    $display("[INFO] Grant queue = %b", grant_queue);

    assert(grant_queue == 4'b0010)
      else $fatal("[FAIL] Incorrect grant assignment");

    $display("[PASS] traffic_shaping_core grant logic works");
    $finish;
  end
endmodule
