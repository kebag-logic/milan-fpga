/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : traffic_classifier.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-06-28
  Description : Ethernet packet classifier that extracts PCP information
                from VLAN or PTP headers. Supports configurable endian and
                TDATA width.

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper

  Notes       : 
    - Tested with TDATA_WIDTH = 32, 64, 128.
    - Automatically detects and decodes Ethernet headers.
    - Endianness configurable per instance.
    - Current Limitation : There should be at least one clock cycle delay incoming packets.
------------------------------------------------------------------------------
*/

//! This module implements an Ethernet packet classifier that parses incoming AXIS frames and 
//! assigns traffic priority based on the VLAN PCP field or Ethertype (e.g., PTP detection).
//! The module is working with different tdata_widths, 32,64,128 are tested.
//! Parsing is always performed in **big endian** byte order for consistent decoding.
//! If `BIG_ENDIAN` is set to 0 (little endian system), the module automatically converts input
//! data to big endian internally for parsing. Output data remains in its original endian format
//! and is forwarded unmodified.

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module traffic_classifier #(
  parameter int TDATA_WIDTH = 64,      //! Width of tdata bus
  parameter bit BIG_ENDIAN = 1,        //! Big endian logic
  parameter int NUMBER_OF_QUEUES = 4,  //! Number of egress queues
  parameter int FIFO_DEPTH = 64        //! FIFO depth
)(
  input wire clk,                  //! clock signal
  input wire resetn,               //! synchronous active low reset

  //! --- runtime configuration (milan_csr classifier group, REQ-CLS-01..04) ---
  input wire        use_pcp_i,      //! 1 = PCP-table classification, 0 = legacy EtherType
  input wire        dmac_check_i,   //! Enable reserved-DMAC validation (placeholder, REQ-CLS-07)
  input wire [2:0]  default_pcp_i,  //! Default port priority for untagged frames
  input wire [23:0] pcp_tc_map_i,   //! PCP->traffic-class table, 8x3 bits
  input wire [23:0] prio_regen_i,   //! Priority regeneration table, 8x3 bits
  input wire [31:0] tc_queue_map_i, //! Traffic-class->queue table, 8x4 bits

  axi_stream_if.slave s_axis,      //! slave interface of AXIS
  axi_stream_if.master m_axis      //! master interface of AXIS
);

//! Master axis interface from fifo.
axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) m_axis_fifo();
//! Storing incoming packets in the fifo till headers parsing is completed.
//! Open-core AXIS FIFO (Forencich verilog-axis), replacing xpm_fifo_axis — makes
//! this module Verilator-simulatable and vendor-neutral (see docs/integration/OPEN_SOURCE_MIGRATION.md).
//! Common-clock, non-packet (FRAME_FIFO=0), tkeep+tlast, no tid/tdest/tuser.
axis_fifo #(
   .DEPTH(FIFO_DEPTH),
   .DATA_WIDTH(TDATA_WIDTH),
   .KEEP_ENABLE(1),
   .KEEP_WIDTH(TDATA_WIDTH/8),
   .LAST_ENABLE(1),
   .ID_ENABLE(0),
   .DEST_ENABLE(0),
   .USER_ENABLE(0),
   .FRAME_FIFO(0)
)
eth_packet_buffer(
  .clk(clk),
  .rst(~resetn),

  .s_axis_tdata(s_axis.tdata),
  .s_axis_tkeep(s_axis.tkeep),
  .s_axis_tvalid(s_axis.tvalid),
  .s_axis_tready(s_axis.tready),
  .s_axis_tlast(s_axis.tlast),
  .s_axis_tid('0),
  .s_axis_tdest('0),
  .s_axis_tuser('0),

  .m_axis_tdata(m_axis_fifo.tdata),
  .m_axis_tkeep(m_axis_fifo.tkeep),
  .m_axis_tvalid(m_axis_fifo.tvalid),
  .m_axis_tready(m_axis_fifo.tready),
  .m_axis_tlast(m_axis_fifo.tlast),
  .m_axis_tid(),
  .m_axis_tdest(),
  .m_axis_tuser(),

  .pause_req(1'b0),
  .pause_ack(),
  .status_depth(),
  .status_depth_commit(),
  .status_overflow(),
  .status_bad_frame(),
  .status_good_frame()
);

//! Flag indicates ethernet headers are received.
logic header_ready;
//! Ethernet header staging buffer (input-side shift, big-endian byte order).
logic [ETH_HEADER_BUFFER_WIDTH-1:0] eth_header;
//! Counter for detecting whether ethernet header is captured or not.
logic [$clog2(ETH_HEADER_WIDTH):0] byte_counter;
//! ethernet type register when VLAN tag exists it is 8100.
logic [ETH_TYPE_BIT_WIDTH-1:0] eth_type_raw;

//! ---- per-frame tdest sideband (REDESIGN 2026-07-05, docs/findings/CBS_DATAPATH_BUG.md) ----
//! The old scheme delayed the DATA by a fixed 1 beat and drove tdest
//! combinationally from a single staged header. Broken two ways on silicon:
//! (a) 1 beat of delay cannot cover the 3-beat header parse, so under
//! back-to-back frames the first output beats carried the PREVIOUS frame's
//! classification — the downstream demux then split frames across queues,
//! stranding beats and wedging the store-and-forward PacketFIFO (the CBS
//! interference TX lockup); (b) the parse counter was only reset by a tlast
//! that arrived with header_ready, so tight/short frames desynced the parser.
//! Now the input side classifies each frame as soon as its header completes
//! (or at tlast for sub-header runts) and pushes ONE queue index into this
//! sideband queue; the output side gates each frame's FIRST beat on its entry
//! and pops at tlast. tdest is correct and stable from the first output beat
//! by construction, with no data-path delay registers at all.
localparam int TQ_DEPTH = 32;   //! > max frames resident in the data FIFO
localparam int TQW = (NUMBER_OF_QUEUES <= 1) ? 1 : $clog2(NUMBER_OF_QUEUES);
logic [TQW-1:0] tq_mem [0:TQ_DEPTH-1];
logic [$clog2(TQ_DEPTH):0] tq_wr, tq_rd;
wire tq_empty = (tq_wr == tq_rd);
wire [$clog2(TQ_DEPTH)-1:0] tq_wr_idx = tq_wr[$clog2(TQ_DEPTH)-1:0];
wire [$clog2(TQ_DEPTH)-1:0] tq_rd_idx = tq_rd[$clog2(TQ_DEPTH)-1:0];
//! this frame's classification has been pushed (one push per input frame)
logic tq_pushed;

//! input-side helper views
wire in_acc = s_axis.tvalid && s_axis.tready;
//! current beat in big-endian parse order (mirrors the original shift path)
wire [TDATA_WIDTH-1:0] beat_be = BIG_ENDIAN ? s_axis.tdata
                                            : reorder_endian_func(s_axis.tdata, TDATA_WIDTH);
//! staging buffer as it will look AFTER shifting in the current beat
wire [ETH_HEADER_BUFFER_WIDTH-1:0] hdr_shifted =
      {eth_header[ETH_HEADER_BUFFER_WIDTH-TDATA_WIDTH-1:0], beat_be};
//! the current beat completes the header
wire completes_now = !header_ready &&
      (byte_counter + (TDATA_WIDTH / BYTE_TO_BIT) >= ETH_HEADER_WIDTH);
//! classify-and-push this cycle: once per frame, at header completion — or at
//! tlast for sub-header runts (classified from a partial buffer: garbage-but-
//! deterministic queue for an already-invalid frame; the point is ONE entry
//! per frame so the output gating can never starve).
wire do_push = in_acc && !tq_pushed && (completes_now || s_axis.tlast);
//! header view used for the classification pushed THIS cycle
wire [ETH_HEADER_BUFFER_WIDTH-1:0] hdr_eff = header_ready ? eth_header : hdr_shifted;

//! ethernet_vlan_hdr_t struct instantiation.
ethernet_vlan_hdr_t eth_packet;

//! Parsed VLAN/priority fields fed to the runtime class map.
wire        vlan_valid = (eth_packet.vlan_tpid == ETH_TYPE_VLAN);
wire [2:0]  frame_pcp  = eth_packet.vlan_tci[VLAN_TCI_BIT_WIDTH-1 -: PCP_BIT_WIDTH];
wire        frame_dei  = eth_packet.vlan_tci[VLAN_TCI_BIT_WIDTH-1-PCP_BIT_WIDTH];
//! network priority / queue index from the runtime class map.
wire [$clog2(NUMBER_OF_QUEUES)-1:0] network_priority;

//! dmac_check_i is reserved for reserved-DMAC validation (REQ-CLS-07); tie off.
wire _unused_dmac = dmac_check_i;

assign header_ready = (byte_counter >= ETH_HEADER_WIDTH);


//! Output = data-FIFO passthrough, gated so a frame's FIRST beat waits until
//! its classification is at the head of the sideband queue (mid-frame beats
//! then stream freely; the entry pops at tlast). tdest is stable and correct
//! for the whole frame, so the downstream demux can never split a frame.
assign m_axis.tdata  = m_axis_fifo.tdata;
assign m_axis.tkeep  = m_axis_fifo.tkeep;
assign m_axis.tvalid = m_axis_fifo.tvalid && !tq_empty;
assign m_axis.tlast  = m_axis_fifo.tlast;
assign m_axis.tdest  = tq_mem[tq_rd_idx];
assign m_axis_fifo.tready = m_axis.tready && !tq_empty;

//! Runtime 802.1Q priority-to-queue classification (REQ-CLS-01..04).
traffic_class_map #(
  .NUMBER_OF_QUEUES(NUMBER_OF_QUEUES)
) class_map (
  .use_pcp_i     (use_pcp_i),
  .default_pcp_i (default_pcp_i),
  .pcp_tc_map_i  (pcp_tc_map_i),
  .prio_regen_i  (prio_regen_i),
  .tc_queue_map_i(tc_queue_map_i),
  .vlan_valid_i  (vlan_valid),
  .pcp_i         (frame_pcp),
  .dei_i         (frame_dei),
  .eth_type_i    (eth_packet.eth_common_hdr.eth_type),
  .tdest_o       (network_priority)
);


//! Input-side parse: shift header beats into the staging buffer (converted to
//! big endian for parsing only — data is conveyed unmodified through the FIFO),
//! and reset the parse state on EVERY end-of-frame, including frames that end
//! before the header completes (the old code only reset when a tlast arrived
//! with header_ready, desyncing the parser on tight/short frames).
always_ff @(posedge clk)begin : data_slice
  if(!resetn)begin
    byte_counter <= 'd0;
    eth_header <= 'd0;
  end
  else if (in_acc) begin
    if (s_axis.tlast)
      byte_counter <= 'd0;                       // next frame parses fresh
    else if (!header_ready)
      byte_counter <= byte_counter + (TDATA_WIDTH / BYTE_TO_BIT);
    if (!header_ready)
      eth_header <= hdr_shifted;
  end
end

//! Sideband push/pop: one classification per input frame (at do_push), one pop
//! per output frame (at the egress tlast handshake). The queue cannot overflow:
//! the data FIFO backpressures the input long before TQ_DEPTH frames of >= 1
//! beat each are resident, and it cannot starve: every frame pushes no later
//! than its tlast beat.
always_ff @(posedge clk)begin : tdest_sideband
  if(!resetn) begin
    tq_wr <= '0;
    tq_rd <= '0;
    tq_pushed <= 1'b0;
  end
  else begin
    if (do_push) begin
      tq_mem[tq_wr_idx] <= network_priority;
      tq_wr <= tq_wr + 1'b1;
    end
    if (in_acc)
      tq_pushed <= s_axis.tlast ? 1'b0 : (tq_pushed || do_push);
    if (m_axis.tvalid && m_axis.tready && m_axis.tlast)
      tq_rd <= tq_rd + 1'b1;
  end
end

//! Decode the effective header view combinationally — `hdr_eff` includes the
//! beat completing the header THIS cycle, so the classification registered
//! into the sideband at do_push is that of the frame being received.
always_comb begin : parse_eth_header
  //! Default assignments
  eth_packet = '0;
  eth_type_raw = '0;

  //! Decode Ethernet fields from the effective header view
  eth_packet.eth_common_hdr.dst_mac =
    hdr_eff[ETH_HEADER_BUFFER_WIDTH-1 -: MAC_ADDR_BIT_WIDTH];
  eth_packet.eth_common_hdr.src_mac =
    hdr_eff[ETH_HEADER_BUFFER_WIDTH-MAC_ADDR_BIT_WIDTH-1 -: MAC_ADDR_BIT_WIDTH];
  eth_type_raw =
    hdr_eff[ETH_HEADER_BUFFER_WIDTH-(2*MAC_ADDR_BIT_WIDTH)-1 -: ETH_TYPE_BIT_WIDTH];
  //! VLAN case (tagged)
  if(eth_type_raw == ETH_TYPE_VLAN)begin
    eth_packet.vlan_tpid = eth_type_raw;
    eth_packet.vlan_tci = hdr_eff[ETH_HEADER_BUFFER_WIDTH-(2*MAC_ADDR_BIT_WIDTH)-
                            ETH_TYPE_BIT_WIDTH-1 -: VLAN_TCI_BIT_WIDTH];
    eth_packet.eth_common_hdr.eth_type = hdr_eff[ETH_HEADER_BUFFER_WIDTH-(2*MAC_ADDR_BIT_WIDTH)-
                            ETH_TYPE_BIT_WIDTH-VLAN_TCI_BIT_WIDTH-1 -: ETH_TYPE_BIT_WIDTH];
  end
  else begin //! if it is not VLAN tagged then eth_type_raw is real eth_type
    eth_packet.eth_common_hdr.eth_type = eth_type_raw;
  end
end

endmodule

`default_nettype wire
