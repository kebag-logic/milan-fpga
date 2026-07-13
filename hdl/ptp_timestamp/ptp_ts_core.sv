/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : ptp_ts_core.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-13
  Description : PTP timestamping core to extract gPTP sequence_id and timestamp
                from Ethernet frames. Supports TX and RX modes.

                - AXI-Stream pass-through for Ethernet frames.
                - Detects start of packet on AXI-Stream.
                - Captures timestamp from global 64-bit counter.
                - Parses PTP Ethernet frame to extract sequence ID.
                - Outputs metadata (timestamp + sequence ID) on a separate AXI-Stream.

  Company     : Kebag Logic
  Project     : PTP Timestamping for Custom RGMII MAC

------------------------------------------------------------------------------
*/

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module ptp_ts_core #(
  parameter int IS_TX = 1,                 //! Set to 1 for TX mode, 0 for RX
  parameter int TDATA_WIDTH = 64,          //! AXI-Stream data width
  parameter int TS_WIDTH = 64,             //! Timestamp width
  parameter int METADATA_TDATA_WIDTH = 64, //! Metadata output width
  parameter bit BIG_ENDIAN = 1,            //! Endianness for field extraction
  parameter bit [15:0] ETH_TYPE = 'h88F7  //! EtherType for PTP
)(
  //! ts_src_clk Source clock domain for timestamp input
  input wire ts_src_clk,
  //! ts_src_resetn Active-low reset for source clock domain
  input wire ts_src_resetn,
  //! ts_dst_clk Destination clock domain for AXI-Stream processing
  input wire ts_dst_clk,
  //! ts_dst_resetn Active-low reset for destination clock domain
  input wire ts_dst_resetn,
  //! ts_in Global timestamp input (source clock domain)
  input wire [TS_WIDTH-1:0] ts_in,

  //! s_axis Input AXI-Stream interface for Ethernet frames
  axi_stream_if.slave s_axis,
  //! m_axis Output AXI-Stream interface (passthrough of input)
  axi_stream_if.master m_axis,
  //! ts_m_axis Output AXI-Stream interface for timestamp metadata
  axi_stream_if.master ts_m_axis
);

localparam int BEAT_BYTES = TDATA_WIDTH / BYTE_TO_BIT;

//! Timestamp after CDC
logic [TS_WIDTH-1:0] ts_cdc_out;
//! Timestamp latched in source domain
logic [TS_WIDTH-1:0] ts_captured_src;
//! Flag to indicate start-of-packet
logic start_packet = '0;
//! Byte count from SOP
logic [$clog2(PTP_SEQ_ID_OFFSET + BEAT_BYTES):0] byte_counter;
//! Indicates start of valid frame
logic sop_detected;
//! Pulse for timestamp capture
wire cdc_trigger;

//! Extracted sequence ID from PTP header
logic [PTP_SEQ_ID_BIT_WIDTH-1:0] ptp_seq_id;
 //! Latch to mark sequence ID of PTP has been extracted
logic ptp_seq_id_valid = 0;
//! Flag to indicate seq_id is captured
logic seq_id_received;
//! Indicates frame is PTP (ETH_TYPE matched)
logic is_ptp;
//! Extracted ethertype
logic [ETH_TYPE_BIT_WIDTH-1:0] eth_type;
//! Latch to mark eth_type has been extracted
logic eth_type_valid = 0;

//! Acknowledment from destination logic that data recived
logic src_rcv;
//! Assertion of signal allows the data will be synchronised
logic src_send;
//! Assertion of signal inform that the data is ready to be used in dest domain
logic dest_req;
//! Captured-timestamp holding register (dest domain): every SOP fills it via
//! the CDC handshake; the frame's TLAST decision consumes it (emit or drop)
logic [TS_WIDTH-1:0] ts_hold;
logic ts_hold_v;
//! Frame qualified at TLAST (valid ethertype extract matched) + its seq
logic qual_pend;
logic [PTP_SEQ_ID_BIT_WIDTH-1:0] seq_snap;

//! Metadata packet to send to PS
ts_metadata ts_reg;

typedef enum logic[1:0]{
  IDLE_S,      //! Waiting for end of PTP packet
  SEND_HIGH_S, //! Send upper 64 bits of metadata (timestamp)
  SEND_LOW_S   //! Send lower 64 bits (seq_id + flags)
}ts_state_t;

ts_state_t ts_state; //! FSM state register

// -----------------------------------------------------------------------------
//! AXI-Stream Passthrough
// -----------------------------------------------------------------------------

assign m_axis.tdata = s_axis.tdata;
assign m_axis.tvalid = s_axis.tvalid;
assign m_axis.tkeep = s_axis.tkeep;
assign m_axis.tlast = s_axis.tlast;
assign s_axis.tready = m_axis.tready;

//! Start of packet logic
assign sop_detected = (s_axis.tvalid && s_axis.tready && start_packet);
assign seq_id_received = (byte_counter >= PTP_SEQ_ID_OFFSET);
assign is_ptp = (eth_type == ETH_TYPE);

// -----------------------------------------------------------------------------
//! SOP Pulse CDC: Triggers timestamp capture from SOP event
// -----------------------------------------------------------------------------

//! Open-core pulse CDC (replaces xpm_cdc_pulse) — SOP event AXIS domain -> PTP
//! counter domain. See docs/integration/OPEN_SOURCE_MIGRATION.md Track 1.4.
cdc_pulse #(
    .DEST_SYNC_FF(2)
) sop_pulse_cdc (
    .src_clk(ts_dst_clk),
    .src_rst_n(ts_dst_resetn),
    .src_pulse(sop_detected),
    .dest_clk(ts_src_clk),
    .dest_rst_n(ts_src_resetn),
    .dest_pulse(cdc_trigger)
);

// -----------------------------------------------------------------------------
//! Timestamp Capture in Source Domain
// -----------------------------------------------------------------------------
always_ff @(posedge ts_src_clk) begin : on_demand_timestamp_capture
  if (!ts_src_resetn) begin
      ts_captured_src <= '0;
      src_send <= '0;
  end
  else begin
      //! Capture only when the previous handshake finished: overwriting src_in
      //! mid-handshake would corrupt the in-flight value. A skipped capture
      //! (frames < ~8 cycles apart - never at real PTP rates) self-heals via
      //! the stale-qual clear on the next SOP.
      if (cdc_trigger && !src_send) begin
        //! Capture timestamp only when needed (at start of packet)
        ts_captured_src <= ts_in;
        src_send <= 'd1;
      end
      else if (src_rcv)begin
        src_send <= 'd0;
      end
  end
end

// -----------------------------------------------------------------------------
// Timestamp CDC to AXI Domain
// -----------------------------------------------------------------------------
//! Open-core value CDC (replaces xpm_cdc_handshake) — captured timestamp PTP
//! domain -> AXIS domain via a 4-phase handshake. Track 1.4.
cdc_handshake #(
   .WIDTH(TS_WIDTH),
   .DEST_SYNC_FF(2),
   .SRC_SYNC_FF(2)
) timestamp_cdc (
   .src_clk(ts_src_clk),
   .src_rst_n(ts_src_resetn),
   .src_in(ts_captured_src),
   .src_send(src_send),
   .src_rcv(src_rcv),
   .dest_clk(ts_dst_clk),
   .dest_rst_n(ts_dst_resetn),
   .dest_out(ts_cdc_out),
   .dest_req(dest_req)
);

// -----------------------------------------------------------------------------
//! Start of Packet Detection
// -----------------------------------------------------------------------------
always_ff @(posedge ts_dst_clk) begin : sop_detect_and_timestamp
  if(!ts_dst_resetn)begin
    start_packet <= 'd1;
  end
  else begin
    if(s_axis.tvalid && s_axis.tready && start_packet)begin
      start_packet <= 'd0;
    end
    else if(s_axis.tvalid && s_axis.tready && s_axis.tlast)begin
      start_packet <= 'd1;
    end
  end
end

// -----------------------------------------------------------------------------
//! Byte Counter Logic
// -----------------------------------------------------------------------------
always_ff @(posedge ts_dst_clk) begin : byte_counter_logic
  if(!ts_dst_resetn)begin
    byte_counter <= 0;
  end
  else begin
    if(s_axis.tvalid && s_axis.tready && !seq_id_received)begin
      byte_counter <= byte_counter + BEAT_BYTES;
    end
    else if(s_axis.tvalid && s_axis.tready && s_axis.tlast)begin
      byte_counter <= 0;
    end
  end
end

// -----------------------------------------------------------------------------
//! Field Extraction (ETH_TYPE and PTP Sequence ID)
// -----------------------------------------------------------------------------
always_ff @(posedge ts_dst_clk) begin : field_extraction
  if (!ts_dst_resetn) begin
      eth_type <= 16'h0000;
      ptp_seq_id <= 16'h0000;
      eth_type_valid <= 1'b0;
      ptp_seq_id_valid <= 1'b0;
  end
  else begin
    if (s_axis.tvalid && s_axis.tready) begin
      //! Extract Ethernet type (at byte offset 12-13)
      if (!eth_type_valid && byte_counter <= ETH_HEADER_NO_VLAN_OFFSET &&
          ETH_HEADER_NO_VLAN_OFFSET < byte_counter + BEAT_BYTES) begin
        case (ETH_HEADER_NO_VLAN_OFFSET - byte_counter)
          3'd0: eth_type <= BIG_ENDIAN ? {s_axis.tdata[63:56], s_axis.tdata[55:48]} :
                                          {s_axis.tdata[15:8], s_axis.tdata[7:0]};
          3'd1: eth_type <= BIG_ENDIAN ? {s_axis.tdata[55:48], s_axis.tdata[47:40]} :
                                          {s_axis.tdata[23:16], s_axis.tdata[15:8]};
          3'd2: eth_type <= BIG_ENDIAN ? {s_axis.tdata[47:40], s_axis.tdata[39:32]} :
                                          {s_axis.tdata[31:24], s_axis.tdata[23:16]};
          3'd3: eth_type <= BIG_ENDIAN ? {s_axis.tdata[39:32], s_axis.tdata[31:24]} :
                                          {s_axis.tdata[39:32], s_axis.tdata[31:24]};
          3'd4: eth_type <= BIG_ENDIAN ? {s_axis.tdata[31:24], s_axis.tdata[23:16]} :
                                          {s_axis.tdata[47:40], s_axis.tdata[39:32]};
          3'd5: eth_type <= BIG_ENDIAN ? {s_axis.tdata[23:16], s_axis.tdata[15:8]} :
                                          {s_axis.tdata[55:48], s_axis.tdata[47:40]};
          3'd6: eth_type <= BIG_ENDIAN ? {s_axis.tdata[15:8], s_axis.tdata[7:0]} :
                                          {s_axis.tdata[63:56], s_axis.tdata[55:48]};
          default: eth_type <= BIG_ENDIAN ? {s_axis.tdata[15:8], s_axis.tdata[7:0]} :
                                          {s_axis.tdata[15:8], s_axis.tdata[7:0]};
        endcase
        eth_type_valid <= 1'b1;
      end
      //! Extract PTP sequence ID (at PTP_SEQ_ID_OFFSET)
      if (!ptp_seq_id_valid && byte_counter <= PTP_SEQ_ID_OFFSET &&
          PTP_SEQ_ID_OFFSET < byte_counter + BEAT_BYTES) begin
        case (PTP_SEQ_ID_OFFSET - byte_counter)
          3'd0: ptp_seq_id <= BIG_ENDIAN ? {s_axis.tdata[63:56], s_axis.tdata[55:48]} :
                                            {s_axis.tdata[15:8], s_axis.tdata[7:0]};
          3'd1: ptp_seq_id <= BIG_ENDIAN ? {s_axis.tdata[55:48], s_axis.tdata[47:40]} :
                                            {s_axis.tdata[23:16], s_axis.tdata[15:8]};
          3'd2: ptp_seq_id <= BIG_ENDIAN ? {s_axis.tdata[47:40], s_axis.tdata[39:32]} :
                                            {s_axis.tdata[31:24], s_axis.tdata[23:16]};
          3'd3: ptp_seq_id <= BIG_ENDIAN ? {s_axis.tdata[39:32], s_axis.tdata[31:24]} :
                                            {s_axis.tdata[39:32], s_axis.tdata[31:24]};
          3'd4: ptp_seq_id <= BIG_ENDIAN ? {s_axis.tdata[31:24], s_axis.tdata[23:16]} :
                                            {s_axis.tdata[47:40], s_axis.tdata[39:32]};
          3'd5: ptp_seq_id <= BIG_ENDIAN ? {s_axis.tdata[23:16], s_axis.tdata[15:8]} :
                                            {s_axis.tdata[55:48], s_axis.tdata[47:40]};
          3'd6: ptp_seq_id <= BIG_ENDIAN ? {s_axis.tdata[15:8], s_axis.tdata[7:0]} :
                                            {s_axis.tdata[63:56], s_axis.tdata[55:48]};
          default: ptp_seq_id <= BIG_ENDIAN ? {s_axis.tdata[63:56], s_axis.tdata[55:48]} :
                                            {s_axis.tdata[15:8], s_axis.tdata[7:0]};
        endcase
        ptp_seq_id_valid <= 1'b1;
      end
    end

    if (s_axis.tvalid && s_axis.tready && s_axis.tlast) begin
      eth_type_valid <= 1'b0;
      ptp_seq_id_valid <= 1'b0;
    end
  end
end

// -----------------------------------------------------------------------------
//! Decoupled capture / qualify / emit (2026-07-13 rewrite). The original made
//! the record decision at handshake-return time (`dest_req && is_ptp`), which
//! races BOTH ways against the ingress rate:
//!   * slow beats (MII 100M into the 50 MHz datapath): the ethertype beat has
//!     not arrived when dest_req fires -> the FIRST record never emits and
//!     every later one pairs the CURRENT timestamp with the PREVIOUS frame's
//!     metadata (one-frame-stale; the silicon "zero records" of phase B);
//!   * back-to-back minimal frames: dest_req can land after tlast instead.
//! Now dest_req only fills ts_hold (one per SOP); the frame QUALIFIES at TLAST
//! when ethertype+seq extracts are definitively valid; the emitter fires on
//! qual_pend && ts_hold_v in either arrival order. A non-PTP tlast CONSUMES
//! its capture so it cannot poison the next frame; a new SOP clears a stale
//! unpaired qual (missed capture - self-heals). Gated: tb/verilator/ptp_ts.
// -----------------------------------------------------------------------------
always_ff @(posedge ts_dst_clk) begin : capture_qualify
  if(!ts_dst_resetn)begin
    ts_hold   <= 'd0;
    ts_hold_v <= 'd0;
    qual_pend <= 'd0;
    seq_snap  <= 'd0;
  end
  else begin
    if(ts_state == IDLE_S && qual_pend && ts_hold_v)begin
      qual_pend <= 'd0;               // consumed by the emitter (ts_reg latch)
      ts_hold_v <= 'd0;
    end
    if(sop_detected && qual_pend && !ts_hold_v)begin
      qual_pend <= 'd0;               // stale qual without a capture: abandon
    end
    if(s_axis.tvalid && s_axis.tready && s_axis.tlast)begin
      if(eth_type_valid && is_ptp && ptp_seq_id_valid)begin
        qual_pend <= 'd1;
        seq_snap  <= (BIG_ENDIAN) ? ptp_seq_id
                                  : {ptp_seq_id[7:0], ptp_seq_id[15:8]};
      end
      else begin
        ts_hold_v <= 'd0;             // non-PTP frame consumes its capture
      end
    end
    if(dest_req)begin                 // LAST: a new capture beats same-cycle clears
      ts_hold   <= ts_cdc_out;
      ts_hold_v <= 'd1;
    end
  end
end
// -----------------------------------------------------------------------------
//! Timestamp Metadata Output FSM
// -----------------------------------------------------------------------------
always_ff @(posedge ts_dst_clk) begin : to_ps_fifo_logic
  if(!ts_dst_resetn)begin
    ts_m_axis.tvalid <= 'd0;
    ts_m_axis.tdata <= 'd0;
    ts_m_axis.tkeep <= 8'h00;
    ts_m_axis.tlast <= 'd0;
    ts_state <= IDLE_S;
  end
  else begin
    case(ts_state)
      IDLE_S: begin
        if(qual_pend && ts_hold_v)begin
          ts_state <= SEND_HIGH_S;
          ts_reg.direction <= IS_TX[0];
          ts_reg.seq_id    <= seq_snap;
          ts_reg.timestamp <= ts_hold;
        end
        else begin
          ts_m_axis.tvalid <= 'd0;
          ts_m_axis.tdata <= 'd0;
          ts_m_axis.tkeep <= 8'h00;
          ts_m_axis.tlast <= 'd0;
          ts_state <= IDLE_S;
        end
      end

      SEND_HIGH_S : begin
        ts_m_axis.tvalid <= 'd1;
        ts_m_axis.tlast <= 'd0;
        ts_m_axis.tkeep <= 8'hff;
        ts_m_axis.tdata <= ts_reg.timestamp;
        if(ts_m_axis.tready)begin
          ts_state <= SEND_LOW_S;
        end
        else begin
          ts_state <= SEND_HIGH_S;
        end
      end

      SEND_LOW_S : begin
        ts_m_axis.tvalid <= 'd1;
        ts_m_axis.tlast <= 'd1;
        ts_m_axis.tkeep <= 8'h07;
        ts_m_axis.tdata <= {40'd0, ts_reg.seq_id, 7'd0, ts_reg.direction};
        if(ts_m_axis.tready)begin
          ts_state <= IDLE_S;
        end
        else begin
          ts_state <= SEND_LOW_S;
        end
      end
      default : ts_state <= IDLE_S;
    endcase
  end
end

endmodule

`default_nettype wire
