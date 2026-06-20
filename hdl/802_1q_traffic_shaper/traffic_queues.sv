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
  localparam TDEST_WIDTH = $clog2(NUMBER_OF_QUEUES);
  localparam string FIFO_TYPES [NUMBER_OF_QUEUES] = '{"block","block","block","distributed"};
  localparam int FIFO_CASCADE_HEIGHTS [NUMBER_OF_QUEUES] = '{0, 0, 0, 32};


  //! Packed signals for mux switch outputs (to FIFOs)
  wire [(NUMBER_OF_QUEUES*TDATA_WIDTH)-1:0] mux_to_fifo_tdata;
  wire [(NUMBER_OF_QUEUES*(TDATA_WIDTH/8))-1:0] mux_to_fifo_tkeep;
  wire [NUMBER_OF_QUEUES-1:0] mux_to_fifo_tvalid;
  wire [NUMBER_OF_QUEUES-1:0] mux_to_fifo_tready;
  wire [NUMBER_OF_QUEUES-1:0] mux_to_fifo_tlast;
  wire [(NUMBER_OF_QUEUES*TDEST_WIDTH)-1:0] mux_to_fifo_tdest;

  //! Packed signals for FIFO outputs (to demux)
  wire [(NUMBER_OF_QUEUES*TDATA_WIDTH)-1:0] fifo_to_demux_tdata;
  wire [(NUMBER_OF_QUEUES*(TDATA_WIDTH/8))-1:0] fifo_to_demux_tkeep;
  wire [NUMBER_OF_QUEUES-1:0] fifo_to_demux_tvalid;
  wire [NUMBER_OF_QUEUES-1:0] fifo_to_demux_tready;
  wire [NUMBER_OF_QUEUES-1:0] fifo_to_demux_tlast;
  wire [(NUMBER_OF_QUEUES*TDEST_WIDTH)-1:0] fifo_to_demux_tdest;

  //! Unpacked array views for easier indexing inside generate
  wire [TDATA_WIDTH-1:0]    mux_to_fifo_tdata_array[NUMBER_OF_QUEUES-1:0];
  wire [(TDATA_WIDTH/8)-1:0] mux_to_fifo_tkeep_array[NUMBER_OF_QUEUES-1:0];
  wire mux_to_fifo_tvalid_array[NUMBER_OF_QUEUES-1:0];
  wire mux_to_fifo_tready_array[NUMBER_OF_QUEUES-1:0];
  wire mux_to_fifo_tlast_array[NUMBER_OF_QUEUES-1:0];
  wire [TDEST_WIDTH-1:0] mux_to_fifo_tdest_array[NUMBER_OF_QUEUES-1:0];

  wire [TDATA_WIDTH-1:0] fifo_to_demux_tdata_array[NUMBER_OF_QUEUES-1:0];
  wire [(TDATA_WIDTH/8)-1:0] fifo_to_demux_tkeep_array[NUMBER_OF_QUEUES-1:0];
  wire [TDEST_WIDTH-1:0] fifo_to_demux_tdest_array[NUMBER_OF_QUEUES-1:0];
  wire fifo_to_demux_tvalid_array[NUMBER_OF_QUEUES-1:0];
  wire fifo_to_demux_tready_array[NUMBER_OF_QUEUES-1:0];
  wire fifo_to_demux_tlast_array[NUMBER_OF_QUEUES-1:0];
  wire fifo_empty[NUMBER_OF_QUEUES-1:0];

  //! --- Assign packed to unpacked and vice versa ---
  genvar i;
  generate
    for(i=0; i < NUMBER_OF_QUEUES; i++) begin
      //! mux_to_fifo unpack
      assign mux_to_fifo_tdata_array[i] = mux_to_fifo_tdata[(i+1)*TDATA_WIDTH-1 -: TDATA_WIDTH];
      assign mux_to_fifo_tkeep_array[i] = mux_to_fifo_tkeep[(i+1)*(TDATA_WIDTH/8)-1 -:
                                          (TDATA_WIDTH/8)];
      assign mux_to_fifo_tvalid_array[i] = mux_to_fifo_tvalid[i];
      assign mux_to_fifo_tlast_array[i] = mux_to_fifo_tlast[i];
      assign mux_to_fifo_tdest_array[i] = mux_to_fifo_tdest[ (i+1)*TDEST_WIDTH-1 -: TDEST_WIDTH];

      //! mux_to_fifo ready packed from array
      assign mux_to_fifo_tready[i] = mux_to_fifo_tready_array[i];

      //! output queue_has_data logic derived from fifo_empty signal
      assign queue_has_data_o[i] = ~fifo_empty[i];

      //! fifo_to_demux pack
      assign fifo_to_demux_tdata[(i+1)*TDATA_WIDTH-1 -: TDATA_WIDTH] = fifo_to_demux_tdata_array[i];
      assign fifo_to_demux_tkeep[(i+1)*(TDATA_WIDTH/8)-1 -:
                                            (TDATA_WIDTH/8)] = fifo_to_demux_tkeep_array[i] ;
      assign fifo_to_demux_tdest[(i+1)*TDEST_WIDTH-1 -: TDEST_WIDTH] = fifo_to_demux_tdest_array[i];
      assign fifo_to_demux_tvalid[i] = fifo_to_demux_tvalid_array[i];
      assign fifo_to_demux_tlast[i] = fifo_to_demux_tlast_array[i];

      // fifo_to_demux ready packed from array
      assign fifo_to_demux_tready_array[i] = fifo_to_demux_tready[i];
    end
  endgenerate


  //! Instantiate axis_switch: multiple inputs, single output (mux)
  axis_switch_1in_4out_64b_tdest_2b_tlast mux_queues (
    .aclk(clk),
    .aresetn(resetn),
    .s_axis_tvalid(s_axis.tvalid),
    .s_axis_tready(s_axis.tready),
    .s_axis_tdata(s_axis.tdata),
    .s_axis_tkeep(s_axis.tkeep),
    .s_axis_tlast(s_axis.tlast),
    .s_axis_tdest(s_axis.tdest),
    .m_axis_tvalid(mux_to_fifo_tvalid),
    .m_axis_tready(mux_to_fifo_tready),
    .m_axis_tdata(mux_to_fifo_tdata),
    .m_axis_tkeep(mux_to_fifo_tkeep),
    .m_axis_tlast(mux_to_fifo_tlast),
    .m_axis_tdest(mux_to_fifo_tdest),
    .s_decode_err()
  );

  //! Instantiate FIFO per queue, connecting unpacked array signals
  generate
    for(i=0; i < NUMBER_OF_QUEUES; i++) begin : fifo_gen
      xpm_fifo_axis #(
        .CLOCKING_MODE("common_clock"),
        .CASCADE_HEIGHT(FIFO_CASCADE_HEIGHTS[i]),
        .FIFO_DEPTH(FIFO_DEPTH),
        .FIFO_MEMORY_TYPE(FIFO_TYPES[i]),
        .PACKET_FIFO("false"),
        .TDATA_WIDTH(TDATA_WIDTH),
        .TDEST_WIDTH(TDEST_WIDTH),
        .USE_ADV_FEATURES("1200"), //! enable prog empty signal
        .PROG_EMPTY_THRESH(5)      //! assert prog_empty_axis when FIFO <= 5 word
      ) eth_packet_buffer (
        .s_aclk(clk),
        .s_aresetn(resetn),

        .s_axis_tdata(mux_to_fifo_tdata_array[i]),
        .s_axis_tkeep(mux_to_fifo_tkeep_array[i]),
        .s_axis_tlast(mux_to_fifo_tlast_array[i]),
        .s_axis_tdest(mux_to_fifo_tdest_array[i]),
        .s_axis_tready(mux_to_fifo_tready_array[i]),
        .s_axis_tvalid(mux_to_fifo_tvalid_array[i]),

        .m_axis_tdata(fifo_to_demux_tdata_array[i]),
        .m_axis_tkeep(fifo_to_demux_tkeep_array[i]),
        .m_axis_tlast(fifo_to_demux_tlast_array[i]),
        .m_axis_tdest(fifo_to_demux_tdest_array[i]),
        .m_axis_tready(fifo_to_demux_tready_array[i]),
        .m_axis_tvalid(fifo_to_demux_tvalid_array[i]),
        .prog_empty_axis(fifo_empty[i])
      );
    end
  endgenerate


  //! Instantiate axis_switch: multiple inputs, single output (demux)
  axis_switch_4in_1out_64b_tlast demux_queues (
    .aclk(clk),
    .aresetn(resetn),
    .s_axis_tvalid(fifo_to_demux_tvalid),
    .s_axis_tready(fifo_to_demux_tready),
    .s_axis_tdata(fifo_to_demux_tdata),
    .s_axis_tkeep(fifo_to_demux_tkeep),
    .s_axis_tlast(fifo_to_demux_tlast),
    .s_axis_tuser(fifo_to_demux_tdest),
    .m_axis_tvalid(m_axis.tvalid),
    .m_axis_tready(m_axis.tready),
    .m_axis_tdata(m_axis.tdata),
    .m_axis_tkeep(m_axis.tkeep),
    .m_axis_tlast(m_axis.tlast),
    .m_axis_tuser(m_axis.tdest),
    .s_req_suppress(~queue_grant_i), //! Suppress queues not granted by CBS
    .s_decode_err()
  );

endmodule

`default_nettype wire
