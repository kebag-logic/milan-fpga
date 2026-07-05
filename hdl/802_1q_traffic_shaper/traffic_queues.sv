/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : traffic_queues.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-03
  Description : Ethernet packet buffering system with support for multiple
                prioritized network queues. Each incoming AXI-Stream packet
                is routed to one of the internal queues based on its `tdest`.

                - A multiplexer (`axis_switch`) distributes packets into per-queue FIFOs.
                - A demultiplexer (`axis_switch`) selects the granted queue for transmission.
                - Grant control is external and determined by credit-based shapers.
                - FIFO `prog_empty` is used to determine if the queue has data.

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper

------------------------------------------------------------------------------
*/

`default_nettype none

module traffic_queues #(
  parameter int TDATA_WIDTH = 64,     //! Width of tdata bus
  parameter int NUMBER_OF_QUEUES = 4, //! Number of network queues
  parameter int FIFO_DEPTH = 16384    //! Buffer depth
)(
  input wire clk,                     //! clock signal
  input wire resetn,                  //! syncronous active low reset
  //! One-hot: indicates granted queue
  input wire [NUMBER_OF_QUEUES-1:0] queue_grant_i,

  //! One-hot: queue data availability
  output wire [NUMBER_OF_QUEUES-1:0] queue_has_data_o,
  axi_stream_if.slave  s_axis,        //! slave interface of AXIS
  axi_stream_if.master m_axis         //! master interface of AXIS
);

  //! Width of `tdest` field
  localparam TDEST_WIDTH = (NUMBER_OF_QUEUES <= 1) ? 1 : $clog2(NUMBER_OF_QUEUES);
  localparam int KW = TDATA_WIDTH/8;
  //! prog_empty threshold: queue reports "has data" only above this depth (was the
  //! xpm PROG_EMPTY_THRESH; keeps the CBS scheduler's underrun margin unchanged).
  localparam int PROG_EMPTY_THRESH = 5;

  // ==========================================================================
  //  Open-core datapath (Forencich verilog-axis) replacing the Xilinx
  //  axis_switch IP + xpm_fifo_axis (docs/OPEN_SOURCE_MIGRATION.md Track 1.3):
  //    axis_demux (1->N by tdest) -> N x axis_fifo -> axis_arb_mux (N->1).
  //  The 4->1 grant suppression (s_req_suppress) is reproduced by gating each
  //  arbiter input's tvalid with queue_grant_i; the final m_axis.tdest is the
  //  granted queue index (reconstructed at the arbiter), matching the old switch.
  // ==========================================================================

  //! demux (1 -> N) outputs, packed
  wire [NUMBER_OF_QUEUES*TDATA_WIDTH-1:0] dm_tdata;
  wire [NUMBER_OF_QUEUES*KW-1:0]          dm_tkeep;
  wire [NUMBER_OF_QUEUES-1:0]             dm_tvalid, dm_tready, dm_tlast;

  //! fifo outputs, packed
  wire [NUMBER_OF_QUEUES*TDATA_WIDTH-1:0] ff_tdata;
  wire [NUMBER_OF_QUEUES*KW-1:0]          ff_tkeep;
  wire [NUMBER_OF_QUEUES-1:0]             ff_tvalid, ff_tlast;
  wire [NUMBER_OF_QUEUES-1:0]             arb_tready;   //! tready driven by the arbiter
  wire fifo_empty [NUMBER_OF_QUEUES-1:0];

  //! route select = incoming tdest (queue index), resized to the demux select width
  wire [TDEST_WIDTH-1:0] route_sel = TDEST_WIDTH'(s_axis.tdest);

  //! 1 -> N demultiplex by tdest into the per-queue FIFOs
  axis_demux #(
    .M_COUNT(NUMBER_OF_QUEUES), .DATA_WIDTH(TDATA_WIDTH),
    .KEEP_ENABLE(1), .KEEP_WIDTH(KW),
    .ID_ENABLE(0), .DEST_ENABLE(0), .USER_ENABLE(0), .TDEST_ROUTE(0)
  ) mux_queues (
    .clk(clk), .rst(~resetn),
    .s_axis_tdata(s_axis.tdata), .s_axis_tkeep(s_axis.tkeep),
    .s_axis_tvalid(s_axis.tvalid), .s_axis_tready(s_axis.tready),
    .s_axis_tlast(s_axis.tlast), .s_axis_tid('0), .s_axis_tdest('0), .s_axis_tuser('0),
    .m_axis_tdata(dm_tdata), .m_axis_tkeep(dm_tkeep),
    .m_axis_tvalid(dm_tvalid), .m_axis_tready(dm_tready), .m_axis_tlast(dm_tlast),
    .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),
    .enable(1'b1), .drop(1'b0), .select(route_sel)
  );

  //! per-queue AXIS FIFO
  genvar i;
  generate
    for (i = 0; i < NUMBER_OF_QUEUES; i++) begin : fifo_gen
      wire [$clog2(FIFO_DEPTH):0] depth;
      axis_fifo #(
        .DEPTH(FIFO_DEPTH), .DATA_WIDTH(TDATA_WIDTH),
        .KEEP_ENABLE(1), .KEEP_WIDTH(KW),
        .LAST_ENABLE(1), .ID_ENABLE(0), .DEST_ENABLE(0), .USER_ENABLE(0), .FRAME_FIFO(0)
      ) eth_packet_buffer (
        .clk(clk), .rst(~resetn),
        .s_axis_tdata(dm_tdata[i*TDATA_WIDTH +: TDATA_WIDTH]),
        .s_axis_tkeep(dm_tkeep[i*KW +: KW]),
        .s_axis_tvalid(dm_tvalid[i]), .s_axis_tready(dm_tready[i]),
        .s_axis_tlast(dm_tlast[i]), .s_axis_tid('0), .s_axis_tdest('0), .s_axis_tuser('0),
        .m_axis_tdata(ff_tdata[i*TDATA_WIDTH +: TDATA_WIDTH]),
        .m_axis_tkeep(ff_tkeep[i*KW +: KW]),
        .m_axis_tvalid(ff_tvalid[i]),
        //! drain only while granted: gate tready too (the arbiter prefetches its
        //! input skid reg via tready, so gating tvalid alone would eat the frame)
        .m_axis_tready(arb_tready[i] & queue_grant_i[i]),
        .m_axis_tlast(ff_tlast[i]), .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),
        .pause_req(1'b0), .pause_ack(),
        .status_depth(depth), .status_depth_commit(),
        .status_overflow(), .status_bad_frame(), .status_good_frame()
      );
      //! prog_empty equivalent: below the underrun-margin threshold
      assign fifo_empty[i]        = (depth <= PROG_EMPTY_THRESH[$clog2(FIFO_DEPTH):0]);
      assign queue_has_data_o[i]  = ~fifo_empty[i];
    end
  endgenerate

  //! N -> 1 GRANT-INDEXED MUX (fix 2026-07-05, docs/CBS_DATAPATH_BUG.md).
  //! This was an axis_arb_mux — its OWN round-robin arbiter + per-frame lock —
  //! fed by grant-gated valids. That stacked a SECOND arbiter on top of the CBS
  //! grant, and the two could lock onto DIFFERENT queues: the arb mux locks its
  //! round-robin pointer at one frame's start, then the CBS grant moves to
  //! another queue at the next frame; the arb mux waits forever for a valid
  //! from its (now un-granted, gated-off) input while the granted queue's full
  //! FIFO never drains — a hard cross-lock (silicon: TX wedge under CBS
  //! two-flow interference; sim: tb/verilator/controller_rate mixed-size, state
  //! grant=q1 while the arb mux is parked on q0, q2s_valid stuck at 0). The CBS
  //! grant in traffic_shaping_core is ALREADY frame-locked (hold_grant until
  //! tlast), so a plain combinational mux selected by the grant IS the arbiter:
  //! one selector, nothing to cross-lock.
  logic [TDEST_WIDTH-1:0] gsel;
  always_comb begin
    gsel = '0;
    for (int k = 0; k < NUMBER_OF_QUEUES; k++)
      if (queue_grant_i[k]) gsel = TDEST_WIDTH'(k);
  end
  assign m_axis.tdata  = ff_tdata[gsel*TDATA_WIDTH +: TDATA_WIDTH];
  assign m_axis.tkeep  = ff_tkeep[gsel*KW +: KW];
  assign m_axis.tvalid = (|queue_grant_i) && ff_tvalid[gsel];
  assign m_axis.tlast  = ff_tlast[gsel];
  assign m_axis.tdest  = gsel;
  //! the granted FIFO pops when the downstream accepts (its m_axis_tready is
  //! already & queue_grant_i above); ungranted FIFOs hold.
  generate
    for (i = 0; i < NUMBER_OF_QUEUES; i++)
      assign arb_tready[i] = m_axis.tready;
  endgenerate

endmodule

`default_nettype wire
