/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : traffic_controller_802_1q.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-05
  Description : Top-level module for IEEE 802.1Q traffic shaping.

                It includes:
                - `traffic_classifier`: Extracts packet priority and maps it to queue index.
                - `traffic_queues`: Buffers packets per queue using AXI-Stream FIFOs.
                - `traffic_shaping_core`: Grants transmission based on Credit-Based Shaping (CBS)
                                           and coordinates packet flow from queues to output.

                This controller ensures bandwidth-aware packet forwarding using a per-class
                credit-based shaping policy.

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper

------------------------------------------------------------------------------
*/

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module traffic_controller_802_1q #(
  parameter int TDATA_WIDTH = 64,             //! AXI-Stream data bus width
  parameter bit BIG_ENDIAN = 1,               //! Determines byte order for classifier
  parameter int CLASSIFIER_FIFO_DEPTH = 64,   //! FIFO depth for classification stage
  parameter int NUMBER_OF_QUEUES = 4,         //! Number of traffic classes/queues
  parameter int BUFFER_FIFO_DEPTH = 1024     //! Per-queue FIFO depth
)(
  input wire clk,                             //! Clock signal
  input wire resetn,                          //! Active-low synchronous reset
  input wire is_1g_i,                         //! High when the link rate is 1GBps

  //! --- 802.1Q classifier runtime config (from milan_csr, REQ-CLS-01..04) ---
  input wire        cls_use_pcp_i,            //! 1 = classify by PCP table, 0 = legacy EtherType
  input wire        cls_dmac_check_i,         //! Enable reserved-DMAC validation (unused placeholder)
  input wire [2:0]  cls_default_pcp_i,        //! Default port priority for untagged frames
  input wire [23:0] cls_pcp_tc_map_i,         //! PCP->traffic-class table, 8x3 bits
  input wire [23:0] cls_prio_regen_i,         //! Priority regeneration table, 8x3 bits
  input wire [31:0] cls_tc_queue_map_i,       //! Traffic-class->queue map, 8x4 bits

  //! --- per-queue CBS runtime config, packed [q*32 +: 32] (from milan_csr) ---
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_idle_slope_i, //! idleSlope per queue, bits/s
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_hi_credit_i,  //! hiCredit per queue, signed bytes
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_lo_credit_i,  //! loCredit per queue, signed bytes
  input wire [NUMBER_OF_QUEUES-1:0]    cbs_shaped_i,     //! 1 = shaped, 0 = strict priority

  axi_stream_if.slave s_axis,                 //! slave interface of AXIS
  axi_stream_if.master m_axis                 //! master interface of AXIS
);

  //! Width of `tdest` field
  localparam TDEST_WIDTH = $clog2(NUMBER_OF_QUEUES);

  //! AXIS interface from traffic_classifier to traffic_queues
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) classifier_to_queue();
  //! AXIS interface from traffic_queues to traffic_shaping_core
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) queue_to_shaper();

  //! One-hot queue grant signals
  wire [NUMBER_OF_QUEUES-1:0] queue_grant;
  //! One-hot queue data availability
  wire [NUMBER_OF_QUEUES-1:0] queue_has_data;

  // ---------------------------------------------------------------------------
  //! Classifier: Extracts priority and assigns `tdest` value
  // ---------------------------------------------------------------------------

  traffic_classifier #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(BIG_ENDIAN),
    .NUMBER_OF_QUEUES(NUMBER_OF_QUEUES),
    .FIFO_DEPTH(CLASSIFIER_FIFO_DEPTH)
  )
  classifier(
    .clk(clk),
    .resetn(resetn),
    .use_pcp_i(cls_use_pcp_i),
    .dmac_check_i(cls_dmac_check_i),
    .default_pcp_i(cls_default_pcp_i),
    .pcp_tc_map_i(cls_pcp_tc_map_i),
    .prio_regen_i(cls_prio_regen_i),
    .tc_queue_map_i(cls_tc_queue_map_i),
    .s_axis(s_axis),
    .m_axis(classifier_to_queue)
  );

  // ---------------------------------------------------------------------------
  //! buffer_queues: One FIFO per queue, stores packets based on `tdest`
  // ---------------------------------------------------------------------------

  traffic_queues #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .NUMBER_OF_QUEUES(NUMBER_OF_QUEUES),
    .FIFO_DEPTH(BUFFER_FIFO_DEPTH)
  )
  buffer_queues(
    .clk(clk),
    .resetn(resetn),
    .queue_grant_i(queue_grant),
    .queue_has_data_o(queue_has_data),
    .s_axis(classifier_to_queue), 
    .m_axis(queue_to_shaper) 
  );

  // ---------------------------------------------------------------------------
  //! Shaper: Applies Credit-Based Shaping (CBS) to regulate egress flow
  // ---------------------------------------------------------------------------

  traffic_shaping_core #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .NUMBER_OF_QUEUES(NUMBER_OF_QUEUES)
  )
  traffic_shaper(
    .clk(clk),
    .resetn(resetn),
    .queue_has_data_i(queue_has_data),
    .is_1g_i(is_1g_i),
    .cbs_idle_slope_i(cbs_idle_slope_i),
    .cbs_hi_credit_i(cbs_hi_credit_i),
    .cbs_lo_credit_i(cbs_lo_credit_i),
    .cbs_shaped_i(cbs_shaped_i),
    .grant_queue_o(queue_grant),
    .s_axis(queue_to_shaper),
    .m_axis(m_axis)
  );

endmodule

`default_nettype wire
