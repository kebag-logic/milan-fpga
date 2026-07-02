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

//! Latency assignment to make aligment with tdest in master axis interface.
localparam int LATENCY = (TDATA_WIDTH == 32) ? 'd3 : (TDATA_WIDTH == 64) ? 'd1 :
                      (TDATA_WIDTH == 128) ? 'd0 : 'd1;
//! When Latency is 0, t*_delay ports will be invalid therefore safe calculation.
localparam int LATENCY_SAFE = (LATENCY > 0) ? LATENCY : 1;

//! Master axis interface from fifo.
axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) m_axis_fifo();
//! Storing incoming packets in the fifo till headers parsing is completed.
//! Open-core AXIS FIFO (Forencich verilog-axis), replacing xpm_fifo_axis — makes
//! this module Verilator-simulatable and vendor-neutral (see docs/OPEN_SOURCE_MIGRATION.md).
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
//! Ethernet header buffer assigned combinationally.
logic [ETH_HEADER_BUFFER_WIDTH-1:0] eth_header;
//! Ethernet header buffer assigned sequentially.
logic [ETH_HEADER_BUFFER_WIDTH-1:0] eth_header_buf;
//! Counter for detecting whether ethernet header is captured or not.
logic [$clog2(ETH_HEADER_WIDTH):0] byte_counter;
//! ethernet type register when VLAN tag exists it is 8100.
logic [ETH_TYPE_BIT_WIDTH-1:0] eth_type_raw;
//! Flag that indicates a packet is being sent currently.
logic packet_in_progress;
//! tdata delay register.
logic [TDATA_WIDTH-1:0] tdata_delay   [0:LATENCY_SAFE-1];
//! tkeep delay register.
logic [TDATA_WIDTH/8-1:0] tkeep_delay [0:LATENCY_SAFE-1];
//! tvalid delay register.
logic tvalid_delay [0:LATENCY_SAFE-1];
//! tlast delay register.
logic tlast_delay  [0:LATENCY_SAFE-1];

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


assign m_axis.tdata  = (LATENCY == 0) ? m_axis_fifo.tdata  : tdata_delay[LATENCY-1];
assign m_axis.tkeep  = (LATENCY == 0) ? m_axis_fifo.tkeep  : tkeep_delay[LATENCY-1];
assign m_axis.tvalid = (LATENCY == 0) ? m_axis_fifo.tvalid : tvalid_delay[LATENCY-1];
assign m_axis.tlast  = (LATENCY == 0) ? m_axis_fifo.tlast  : tlast_delay[LATENCY-1];
assign m_axis.tdest = network_priority;
assign m_axis_fifo.tready = m_axis.tready;

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


//! If headers are not ready add tdata into the eth_header slice, if the module is instantiated
//! little endian, parser logic will convert into big endian for ONLY parsing logic, data will be
//! conveyed little endian again.
always_ff @(posedge clk)begin : data_slice
  if(!resetn)begin
    byte_counter <= 'd0;
    eth_header <= 'd0;
  end
  else begin
    if(s_axis.tready && s_axis.tvalid && !header_ready) begin
      byte_counter <= byte_counter + (TDATA_WIDTH / BYTE_TO_BIT);
      if(BIG_ENDIAN) begin
        eth_header <= {eth_header[ETH_HEADER_BUFFER_WIDTH-TDATA_WIDTH-1:0], s_axis.tdata};
      end
      else begin
        eth_header <= {eth_header[ETH_HEADER_BUFFER_WIDTH-TDATA_WIDTH-1:0],
                      reorder_endian_func(s_axis.tdata, TDATA_WIDTH)};
      end
    end
    else if(s_axis.tready && s_axis.tvalid && s_axis.tlast) begin
      byte_counter <= 'd0;
    end
  end
end

//! register eth_header content to not lose due to immediate new packet override.
always_ff @(posedge clk)begin : eth_hdr_buffer
  if(!resetn) begin
    eth_header_buf <= 'd0;
    packet_in_progress <= 'd0;
  end
  else begin
    if(header_ready && !packet_in_progress)begin
      eth_header_buf <= eth_header;
      packet_in_progress <= 'd1;
    end
    if(m_axis.tvalid && m_axis.tready && m_axis.tlast)begin
      packet_in_progress <= 'd0;
    end
  end
end

//! Immediately decode eth_header_buf combinationally.
always_comb begin : parse_eth_header
  //! Default assignments
  eth_packet = '0;
  eth_type_raw = '0;

  //! Decode Ethernet fields from eth_header_buf
  eth_packet.eth_common_hdr.dst_mac =
    eth_header_buf[ETH_HEADER_BUFFER_WIDTH-1 -: MAC_ADDR_BIT_WIDTH];
  eth_packet.eth_common_hdr.src_mac =
    eth_header_buf[ETH_HEADER_BUFFER_WIDTH-MAC_ADDR_BIT_WIDTH-1 -: MAC_ADDR_BIT_WIDTH];
  eth_type_raw =
    eth_header_buf[ETH_HEADER_BUFFER_WIDTH-(2*MAC_ADDR_BIT_WIDTH)-1 -: ETH_TYPE_BIT_WIDTH];
  //! VLAN case (tagged)
  if(eth_type_raw == ETH_TYPE_VLAN)begin
    eth_packet.vlan_tpid = eth_type_raw;
    eth_packet.vlan_tci = eth_header_buf[ETH_HEADER_BUFFER_WIDTH-(2*MAC_ADDR_BIT_WIDTH)-
                            ETH_TYPE_BIT_WIDTH-1 -: VLAN_TCI_BIT_WIDTH];
    eth_packet.eth_common_hdr.eth_type = eth_header_buf[ETH_HEADER_BUFFER_WIDTH-(2*MAC_ADDR_BIT_WIDTH)-
                            ETH_TYPE_BIT_WIDTH-VLAN_TCI_BIT_WIDTH-1 -: ETH_TYPE_BIT_WIDTH];
  end
  else begin //! if it is not VLAN tagged then eth_type_raw is real eth_type
    eth_packet.eth_common_hdr.eth_type = eth_type_raw;
  end
end

//! Delay master interface for tdest alignment.
always_ff @(posedge clk) begin : m_axis_allignment
  if (!resetn) begin
    for (int i = 0; i < LATENCY; i++) begin
      tdata_delay[i]   <= '0;
      tkeep_delay[i]   <= '0;
      tvalid_delay[i]  <= '0;
      tlast_delay[i]   <= '0;
    end
  end else begin
    tdata_delay[0]   <= m_axis_fifo.tdata;
    tkeep_delay[0]   <= m_axis_fifo.tkeep;
    tvalid_delay[0]  <= m_axis_fifo.tvalid;
    tlast_delay[0]   <= m_axis_fifo.tlast;

    for (int i = 1; i < LATENCY; i++) begin
      tdata_delay[i]   <= tdata_delay[i-1];
      tkeep_delay[i]   <= tkeep_delay[i-1];
      tvalid_delay[i]  <= tvalid_delay[i-1];
      tlast_delay[i]   <= tlast_delay[i-1];
    end
  end
end

endmodule

`default_nettype wire
