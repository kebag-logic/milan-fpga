/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : traffic_shaping_core.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-05
  Description : Top-level module for IEEE 802.1Qav Credit-Based Traffic Shaping.
                Implements multi-queue arbitration using per-queue CBS instances.

                - Each queue is monitored for data availability and credit level.
                - Only one queue is granted for transmission at a time.
                - Grants are held until the end of a packet (`tlast`).
                - Transmission eligibility is driven by credit logic (CBS).

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper

------------------------------------------------------------------------------
*/

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module traffic_shaping_core #(
  parameter int TDATA_WIDTH = 64,     //! Widht of tdata bus
  parameter int NUMBER_OF_QUEUES = 4  //! Number of network queues
)(
  input wire clk,                     //! clock signal
  input wire resetn,                  //! syncronous active low reset
  //! One-hot: indicates which queues contain data
  input wire [NUMBER_OF_QUEUES-1:0] queue_has_data_i,
  input wire is_1g_i,                 //! High when the link rate is 1GBps

  //! One-hot: indicates which queue is granted
  output logic [NUMBER_OF_QUEUES-1:0] grant_queue_o,
  axi_stream_if.slave  s_axis,        //! slave interface of AXIS
  axi_stream_if.master m_axis         //! master interface of AXIS
);

  //! Indicates whether each queue is currently transmitting
  logic [NUMBER_OF_QUEUES-1:0] is_transmitting = 0;
  logic [NUMBER_OF_QUEUES-1:0] is_transmitting_raw = 0;
  //! Number of bytes transmitted in the current cycle (per queue)
  logic [15:0] bytes_sent_raw [NUMBER_OF_QUEUES];
  logic [15:0] bytes_sent [NUMBER_OF_QUEUES];
  //! Credit-based decision signal from CBS modules
  logic [NUMBER_OF_QUEUES-1:0] allow_transmit;
  //! Currently active queue index
  logic [$clog2(NUMBER_OF_QUEUES)-1:0] active_queue;
  //! Latch to hold current grant until end of packet (tlast)
  logic hold_grant;
  //! Priory encode selection
  int sel;

  assign m_axis.tdata = s_axis.tdata;
  assign m_axis.tvalid = s_axis.tvalid;
  assign m_axis.tkeep = s_axis.tkeep;
  assign m_axis.tlast = s_axis.tlast;
  assign m_axis.tdest = s_axis.tdest;
  assign s_axis.tready = m_axis.tready;

  assign grant_queue_o = hold_grant ? (1 << active_queue) : '0;

  for (genvar i = 0; i < NUMBER_OF_QUEUES; i++) begin : gen_cbs
    //! CBS modules instantiation, parameters are located on ethernet_packet_pkg.sv
    credit_based_shaper #(
      .IDLE_SLOPE_1G(IDLE_SLOPE_1G[i]),
      .IDLE_SLOPE_100M(IDLE_SLOPE_100M[i]),
      .HI_CREDIT (HI_CREDIT),
      .LO_CREDIT (LO_CREDIT),
      .CLK_FREQ_HZ(CLK_FREQ_HZ)
    ) u_cbs (
      .clk               (clk),
      .resetn            (resetn),
      .queue_has_data_i  (queue_has_data_i[i]),
      .is_1g_i           (is_1g_i),
      .is_transmitting_i (is_transmitting[i]),
      .bytes_sent_i      (bytes_sent[i]),
      .allow_transmit_o  (allow_transmit[i])
    );
  end

  for (genvar i = 0; i < NUMBER_OF_QUEUES; i++) begin : gen_transmit_info
    //! Track transmission status and byte count
    always_comb begin : transmissionStatus
      is_transmitting_raw[i] = ((m_axis.tdest == i) && m_axis.tvalid && m_axis.tready);
      bytes_sent_raw[i] = is_transmitting_raw[i] ? $countones(m_axis.tkeep) : 0;
    end

    always_ff @(posedge clk) begin
      if (!resetn) begin
        bytes_sent[i] <= 0;
        is_transmitting[i] <= 0;
      end else begin
        bytes_sent[i] <= bytes_sent_raw[i];
        is_transmitting[i] <= is_transmitting_raw[i];
      end
    end
  end

  //! Queue grant logic - one queue should be grant a time
  always_ff @(posedge clk) begin
    if (!resetn) begin
      active_queue <= 0;
      hold_grant   <= 0;
    end else begin
      if (hold_grant) begin
        //! Release grant after end of packet
        if (m_axis.tvalid && m_axis.tready && m_axis.tlast)
          hold_grant <= 0;
      end else begin
      sel = priority_encode(allow_transmit & queue_has_data_i);
      if (sel >= 0) begin
        active_queue <= sel;
        hold_grant   <= 1;
      end
    end
    end
  end


endmodule

`default_nettype wire
