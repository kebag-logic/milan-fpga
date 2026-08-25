/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : ptp_ts_core.sv
  Description : gPTP frame timestamping core (TX or RX tap).

                - AXI-Stream pass-through for Ethernet frames (combinational,
                  never stalls the tap).
                - Latches the PHC value at each frame's FIRST beat (SOP), with
                  the SW-programmed per-port latency correction applied
                  (REQ-PTP-06): RX SUBTRACTS the ingress latency (the wire SFD
                  preceded this AXIS SOP), TX ADDS the egress latency (the SFD
                  follows it). Reset 0 = uncorrected, i.e. today's behaviour.
                - Parses ethertype / PTP messageType / sequenceId at the
                  untagged-gPTP offsets, and at the C-TAG-shifted offsets when
                  the frame carries an 802.1Q tag (REQ-PTP-09): TPID 0x8100 at
                  bytes 12-13 moves ethertype to 16-17, messageType to 18 and
                  sequenceId to 48-49. 802.1AS-2020 §11.3.3 lets a port send
                  gPTP with a VLAN tag; before this the tagged frames simply
                  never matched ETH_TYPE and silently produced no timestamp.
                - Qualifies at TLAST: ethertype match AND an EVENT message
                  (msgType[3:2]==00 - Sync/Delay_Req/Pdelay_Req/Pdelay_Resp,
                  REQ-PTP-05). General messages (Announce, Follow_Up,
                  Pdelay_Resp_FUp, Signaling, Delay_Resp, Management) and the
                  reserved types 0x4-0x7 carry no wire timestamp semantics and
                  would only waste record slots and invite seq collisions
                  downstream.
                - Queues {timestamp, seqId, msgType} in a 4-deep record fifo
                  (the emitter needs ~4 cycles/record vs >=9 beat-cycles/frame,
                  so the fifo absorbs bursts incl. RR-mux backpressure), then
                  emits 2-beat metadata records:
                    beat0 = timestamp[63:0] (integer ns, disciplined PHC)
                    beat1 = {40'0, seq[15:0], msgType[3:0], 2'0, marker=1, dir}

  2026-07-13 REDESIGN (docs/findings/PTP_TS_METADATA_FIX.md): the original
  captured the timestamp through a per-event pulse+handshake CDC and decided
  the record at handshake-return time. That raced the ingress rate (slow-beat
  MII: first record never emitted, later ones one-frame-stale; fast frames:
  return after tlast) and could MIS-PAIR timestamps with frames under
  back-to-back interfering traffic (capture-skip and hold-overwrite windows).
  Both real instantiations tie gtx_clk == axis_clk, so `ts_in` is sampled
  SYNCHRONOUSLY at SOP - exact per-frame pairing by construction, no
  handshake, no skip windows. REQUIREMENT: ts_in must be synchronous to
  ts_dst_clk (ptp_ts_top drives the counter from gtx_clk == axis_clk; a
  future truly-async MAC clock needs a gray-coded counter image instead).
  ts_src_clk/ts_src_resetn remain as ports for interface stability but are
  UNUSED. Gated by tb/verilator/ptp_ts (interference suite) and the
  milan_dp end-to-end record check.
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
  parameter bit BIG_ENDIAN = 0,            //! 0 = first wire byte in tdata[7:0] - the
                                           //! MAC-side convention (Forencich AXIS; see
                                           //! adp_advertiser.sv, silicon-proven). 1 =
                                           //! first byte in tdata[63:56].
  parameter bit [15:0] ETH_TYPE = 'h88F7  //! EtherType, natural wire value (the
                                           //! extraction picks bytes explicitly, so no
                                           //! pre-swapped constant regardless of lanes)
)(
  //! ts_src_clk / ts_src_resetn: RETAINED FOR PORT COMPATIBILITY, UNUSED
  //! (see the 2026-07-13 redesign note - ts_in is dst-domain synchronous)
  input wire ts_src_clk,
  input wire ts_src_resetn,
  //! ts_dst_clk Clock domain for AXI-Stream processing AND ts_in
  input wire ts_dst_clk,
  //! ts_dst_resetn Active-low reset
  input wire ts_dst_resetn,
  //! ts_in Global timestamp input - MUST be synchronous to ts_dst_clk
  input wire [TS_WIDTH-1:0] ts_in,
  //! lat_corr_i Per-port latency correction, ns, UNSIGNED magnitude
  //! (PTP_INGRESS_LAT on an RX tap, PTP_EGRESS_LAT on a TX tap). The DIRECTION
  //! is fixed by IS_TX so software never has to negate: RX capture - lat_corr,
  //! TX capture + lat_corr (REQ-PTP-06). 0 = disabled = today's behaviour.
  input wire [31:0] lat_corr_i,

  //! Frame input. Keep this face FLAT: when ptp_ts_core is nested inside
  //! ptp_ts_top, sv2v 0.0.12/0.0.13 drops interface-port associations and
  //! emits undriven hierarchical wires. Flat pins preserve the same AXIS
  //! contract while making the shipping hierarchy portable to Yosys.
  input  wire [TDATA_WIDTH-1:0] s_axis_tdata,
  input  wire                   s_axis_tvalid,
  output wire                   s_axis_tready,
  input  wire                   s_axis_tlast,
  input  wire [(TDATA_WIDTH/8)-1:0] s_axis_tkeep,

  //! Frame output (combinational passthrough of the accepted input)
  output wire [TDATA_WIDTH-1:0] m_axis_tdata,
  output wire                   m_axis_tvalid,
  input  wire                   m_axis_tready,
  output wire                   m_axis_tlast,
  output wire [(TDATA_WIDTH/8)-1:0] m_axis_tkeep,

  //! Timestamp metadata output
  output wire [METADATA_TDATA_WIDTH-1:0] ts_m_axis_tdata,
  output wire                            ts_m_axis_tvalid,
  input  wire                            ts_m_axis_tready,
  output wire                            ts_m_axis_tlast,
  output wire [(METADATA_TDATA_WIDTH/8)-1:0] ts_m_axis_tkeep
);

localparam int BEAT_BYTES = TDATA_WIDTH / BYTE_TO_BIT;

// Fixed gPTP byte offsets and the beats that carry them (64-bit beats):
//   UNTAGGED: ethertype @12-13 + messageType @14 in beat 1 (bytes 8-15);
//             sequenceId @44-45 in beat 5 (bytes 40-47).
//   C-TAGGED (REQ-PTP-09, +4 bytes of tag): TPID 0x8100 @12-13 in beat 1;
//             ethertype @16-17 + messageType @18 in beat 2 (bytes 16-23);
//             sequenceId @48-49 in beat 6 (bytes 48-55).
// Both offset sets land on beat boundaries only because BEAT_BYTES == 8, which
// is what both real instantiations use (milan_datapath / milan_top).
localparam int ETHTYPE_BEAT_OFF     = 8;
localparam int SEQID_BEAT_OFF       = 40;
localparam int TAG_ETHTYPE_BEAT_OFF = 16;
localparam int TAG_SEQID_BEAT_OFF   = 48;

//! Byte-lane LSB index by WIRE order within a beat, as ELABORATION constants
//! (a function capturing the BIG_ENDIAN parameter is legal SV but is exactly
//! the construct class Vivado silently mis-folds - the 2026-07-13 dead-cores
//! netlist; localparam arithmetic is the silicon-proven idiom here)
localparam int LANE12 = BIG_ENDIAN ? 8*(BEAT_BYTES-1-4) : 8*4;  // frame byte 12
localparam int LANE13 = BIG_ENDIAN ? 8*(BEAT_BYTES-1-5) : 8*5;  // frame byte 13
localparam int LANE14 = BIG_ENDIAN ? 8*(BEAT_BYTES-1-6) : 8*6;  // frame byte 14
localparam int LANE44 = BIG_ENDIAN ? 8*(BEAT_BYTES-1-4) : 8*4;  // frame byte 44
localparam int LANE45 = BIG_ENDIAN ? 8*(BEAT_BYTES-1-5) : 8*5;  // frame byte 45
//! C-TAG-shifted extracts (REQ-PTP-09): bytes 16/17/18 and 48/49 all sit at
//! lane offsets 0/1/2 of their beat.
localparam int LANE_B0 = BIG_ENDIAN ? 8*(BEAT_BYTES-1-0) : 8*0;  // bytes 16 / 48
localparam int LANE_B1 = BIG_ENDIAN ? 8*(BEAT_BYTES-1-1) : 8*1;  // bytes 17 / 49
localparam int LANE_B2 = BIG_ENDIAN ? 8*(BEAT_BYTES-1-2) : 8*2;  // byte  18

//! Flag indicating the next accepted beat is a frame's first (SOP)
logic start_packet = 1'b1;
//! Byte offset of the current beat from frame start (stops past the extracts -
//! now the C-TAG-shifted seqId beat, the furthest field we look at)
logic [$clog2(TAG_SEQID_BEAT_OFF + 2*BEAT_BYTES):0] byte_counter;
//! PHC value latched at the current frame's SOP
logic [TS_WIDTH-1:0] ts_sop;

//! Field extracts + their per-frame valid latches. The ethertype COMPARISON is
//! done at capture time and stored as a 1-bit flag (same set-at-beat shape as
//! the valid latches) instead of registering the 16-bit value and comparing at
//! TLAST - functionally identical, a shorter qualify cone, and it sidesteps
//! the registered-value-vs-constant compare structure that the 2026-07-13
//! netlist forensics could not prove sound through synthesis.
logic        eth_match;              // {b12,b13} == ETH_TYPE, captured at beat 1
logic        eth_type_valid = 1'b0;
logic [3:0]  msg_type;
logic [15:0] ptp_seq_id;             // held in WIRE byte order {b44, b45}
logic        ptp_seq_id_valid = 1'b0;
//! Frame carries an 802.1Q C-TAG (TPID 0x8100 at bytes 12-13), latched at
//! beat 1 so the shifted extract beats below can select on it (REQ-PTP-09).
logic        vlan_tagged = 1'b0;

wire beat_acc = s_axis_tvalid && s_axis_tready;
//! EVENT-message qualification (REQ-PTP-05, IEEE 1588-2019 Table 36 / §7.3.4).
//! The ONLY event messages are Sync (0x0), Delay_Req (0x1), Pdelay_Req (0x2)
//! and Pdelay_Resp (0x3) - they alone carry a wire timestamp semantic. General
//! messages (Follow_Up 0x8, Delay_Resp 0x9, Pdelay_Resp_Follow_Up 0xA,
//! Announce 0xB, Signaling 0xC, Management 0xD) must not consume a record slot,
//! and neither must the RESERVED types 0x4-0x7: the older `!msg_type[3]` test
//! let all four through, minting records for messages that can never have a
//! timestamp and inviting seqId collisions in the driver's TX-stamp lookup.
wire is_ptp_event = eth_type_valid && eth_match &&
                    ptp_seq_id_valid && (msg_type[3:2] == 2'b00);

// -----------------------------------------------------------------------------
//! AXI-Stream Passthrough
// -----------------------------------------------------------------------------
assign m_axis_tdata  = s_axis_tdata;
assign m_axis_tvalid = s_axis_tvalid;
assign m_axis_tkeep  = s_axis_tkeep;
assign m_axis_tlast  = s_axis_tlast;
assign s_axis_tready = m_axis_tready;

// -----------------------------------------------------------------------------
//! Per-port latency correction (REQ-PTP-06, 802.1AS-2020 §8.4.3). The capture
//! point is the AXIS start-of-packet, which is NOT the GMII SFD: on RX the SFD
//! crossed the pins some nanoseconds BEFORE this beat, on TX it leaves some
//! nanoseconds AFTER. PTP_INGRESS_LAT/PTP_EGRESS_LAT carry those constants and
//! the sign is applied here so software never has to think about it. Both reset
//! to 0. The explicit option-OFF bench may apply measured constants in ptp4l
//! instead; move one or the other, never both, or the correction double-counts.
//! NOTE: this is the register half of REQ-PTP-06. True SFD capture needs a tap
//! at the GMII/PHY boundary; nothing at this AXIS boundary can synthesise it,
//! so the constants remain characterisation-derived.
// -----------------------------------------------------------------------------
wire [TS_WIDTH-1:0] lat_corr_w = {{(TS_WIDTH-32){1'b0}}, lat_corr_i};
wire [TS_WIDTH-1:0] ts_corrected = IS_TX ? (ts_in + lat_corr_w)
                                         : (ts_in - lat_corr_w);

// -----------------------------------------------------------------------------
//! SOP / byte counter / synchronous SOP timestamp
// -----------------------------------------------------------------------------
always_ff @(posedge ts_dst_clk) begin : sop_and_counter
  if (!ts_dst_resetn) begin
    start_packet <= 1'b1;
    byte_counter <= '0;
  end
  else if (beat_acc) begin
    if (s_axis_tlast) begin
      start_packet <= 1'b1;
      byte_counter <= '0;
    end
    else begin
      start_packet <= 1'b0;
      // stop counting once every extract offset has passed (overflow-safe
      // for any frame length; comparisons below only need exact low values)
      if (byte_counter <= TAG_SEQID_BEAT_OFF)
        byte_counter <= byte_counter + BEAT_BYTES;
    end
    if (start_packet)
      ts_sop <= ts_corrected; // exact per-frame pairing: SOP(N+1) is always
                            // after TLAST(N), so ts_sop is stable frame-long
  end
end

// -----------------------------------------------------------------------------
//! Field extraction at fixed beats, explicit lane slices
// -----------------------------------------------------------------------------
wire [7:0] et_hi = s_axis_tdata[LANE12 +: 8];
wire [7:0] et_lo = s_axis_tdata[LANE13 +: 8];
wire [7:0] mt_b  = s_axis_tdata[LANE14 +: 8];
wire [7:0] sq_hi = s_axis_tdata[LANE44 +: 8];
wire [7:0] sq_lo = s_axis_tdata[LANE45 +: 8];
//! C-TAG-shifted views of the same fields (REQ-PTP-09)
wire [7:0] tet_hi = s_axis_tdata[LANE_B0 +: 8];   // frame byte 16
wire [7:0] tet_lo = s_axis_tdata[LANE_B1 +: 8];   // frame byte 17
wire [7:0] tmt_b  = s_axis_tdata[LANE_B2 +: 8];   // frame byte 18
wire [7:0] tsq_hi = s_axis_tdata[LANE_B0 +: 8];   // frame byte 48
wire [7:0] tsq_lo = s_axis_tdata[LANE_B1 +: 8];   // frame byte 49

always_ff @(posedge ts_dst_clk) begin : field_extraction
  if (!ts_dst_resetn) begin
    eth_match        <= 1'b0;
    msg_type         <= '0;
    ptp_seq_id       <= '0;
    eth_type_valid   <= 1'b0;
    ptp_seq_id_valid <= 1'b0;
    vlan_tagged      <= 1'b0;
  end
  else if (beat_acc) begin
    //! Beat 1 (bytes 8-15): either the untagged ethertype+messageType, or the
    //! C-TAG's TPID - in which case the real fields are 4 bytes further on and
    //! nothing is qualified yet (REQ-PTP-09).
    if (!start_packet && byte_counter == ETHTYPE_BEAT_OFF) begin
      vlan_tagged <= ({et_hi, et_lo} == ETH_TYPE_VLAN);
      if ({et_hi, et_lo} != ETH_TYPE_VLAN) begin
        eth_match <= ({et_hi, et_lo} == ETH_TYPE);
        msg_type <= mt_b[3:0];
        eth_type_valid <= 1'b1;
      end
    end
    //! Beat 2 (bytes 16-23), tagged frames only: the C-TAG-shifted ethertype
    //! and messageType.
    if (!start_packet && vlan_tagged && byte_counter == TAG_ETHTYPE_BEAT_OFF) begin
      eth_match <= ({tet_hi, tet_lo} == ETH_TYPE);
      msg_type <= tmt_b[3:0];
      eth_type_valid <= 1'b1;
    end
    if (!start_packet && !vlan_tagged && byte_counter == SEQID_BEAT_OFF) begin
      ptp_seq_id <= {sq_hi, sq_lo};
      ptp_seq_id_valid <= 1'b1;
    end
    if (!start_packet && vlan_tagged && byte_counter == TAG_SEQID_BEAT_OFF) begin
      ptp_seq_id <= {tsq_hi, tsq_lo};
      ptp_seq_id_valid <= 1'b1;
    end
    if (s_axis_tlast) begin
      eth_type_valid   <= 1'b0;
      eth_match        <= 1'b0;
      ptp_seq_id_valid <= 1'b0;
      vlan_tagged      <= 1'b0;
    end
  end
end

// -----------------------------------------------------------------------------
//! Record fifo: qualified at TLAST, drained by the send FSM. Depth 4 absorbs
//! emitter latency + RR-mux arbitration; a full fifo drops the record whole
//! (cannot happen at legal frame rates: >=9 beat-cycles/frame vs ~4/record).
// -----------------------------------------------------------------------------
// EXPLICIT flop queue - no arrays at all. The 4-deep array version (both as a
// packed-struct array and as parallel plain arrays) got LUTRAM-inferred and
// the cross-hierarchy optimizer mis-wired the 16-bit RAM data inputs in the
// full build (silicon + funcsim-netlist dead while source-sim passed; the
// 64-bit ts entries survived, seq/mtype arrived zero - see
// PTP_TS_METADATA_FIX.md). Registers + explicit muxes are immune, and depth 2
// is rigorously enough: pushes arrive >= 9 beat-cycles apart (minimum frame)
// while the emitter needs <= 6 cycles/record, and the 16-deep downstream
// axis_fifo absorbs backpressure bursts.
logic [TS_WIDTH-1:0] q0_ts, q1_ts;
logic [15:0]         q0_seq, q1_seq;
logic [3:0]          q0_mt, q1_mt;
logic [1:0]          rec_lvl;                  // 0..2 entries (q0 = head)
wire rec_empty = rec_lvl == 2'd0;
wire rec_full  = rec_lvl == 2'd2;
wire rec_push  = beat_acc && s_axis_tlast && is_ptp_event && !rec_full;
wire rec_pop;                                  // from the emitter FSM

always_ff @(posedge ts_dst_clk) begin : record_queue
  if (!ts_dst_resetn) begin
    rec_lvl <= 2'd0;
  end
  else begin
    case ({rec_push, rec_pop})
      2'b10: rec_lvl <= rec_lvl + 2'd1;
      2'b01: rec_lvl <= rec_lvl - 2'd1;
      default: ;                               // both or neither: level holds
    endcase
    if (rec_push && (rec_lvl == 2'd0 || (rec_lvl == 2'd1 && rec_pop))) begin
      q0_ts <= ts_sop; q0_seq <= ptp_seq_id; q0_mt <= msg_type;
    end
    else if (rec_push) begin                   // level 1 (no pop) -> tail slot
      q1_ts <= ts_sop; q1_seq <= ptp_seq_id; q1_mt <= msg_type;
    end
    else if (rec_pop && rec_lvl == 2'd2) begin // shift tail to head
      q0_ts <= q1_ts; q0_seq <= q1_seq; q0_mt <= q1_mt;
    end
  end
end

// -----------------------------------------------------------------------------
//! Metadata output FSM: 2 beats per record. Outputs derive COMBINATIONALLY
//! from the state (valid never depends on ready - AXI-Stream compliant), so
//! backpressure holds a beat exactly and back-to-back records stream with
//! neither duplicated nor dropped beats (the registered-output staging of the
//! first rewrite double-sent the HIGH beat - caught by the interference TB).
// -----------------------------------------------------------------------------
typedef enum logic [1:0] {
  IDLE_S,      //! Wait for a queued record
  SEND_HIGH_S, //! Beat 0: timestamp
  SEND_LOW_S   //! Beat 1: {seq, msgType, dir}, tlast
} ts_state_t;

ts_state_t ts_state;
logic [TS_WIDTH-1:0] cur_ts;
logic [15:0]         cur_seq;
logic [3:0]          cur_mt;
logic pop_r;
assign rec_pop = pop_r;

assign ts_m_axis_tvalid = (ts_state != IDLE_S);
assign ts_m_axis_tlast  = (ts_state == SEND_LOW_S);
assign ts_m_axis_tkeep  = (ts_state == SEND_LOW_S) ? 8'h07 : 8'hFF;
// word1 bit[1] is an ALWAYS-1 marker: the DMA lands word0 then word1 a few
// bus-cycles later, so the DRIVER's slot sentinel is word1 (marker set =>
// word0 is complete). A ns-based sentinel would race that window.
assign ts_m_axis_tdata  = (ts_state == SEND_LOW_S)
                          ? {40'd0, cur_seq, cur_mt, 2'd0, 1'b1, IS_TX[0]}
                          : cur_ts;

always_ff @(posedge ts_dst_clk) begin : to_ps_fifo_logic
  if (!ts_dst_resetn) begin
    ts_state <= IDLE_S;
    pop_r    <= 1'b0;
  end
  else begin
    pop_r <= 1'b0;
    case (ts_state)
      IDLE_S: begin
        if (!rec_empty) begin
          cur_ts   <= q0_ts;
          cur_seq  <= q0_seq;
          cur_mt   <= q0_mt;
          pop_r    <= 1'b1;
          ts_state <= SEND_HIGH_S;
        end
      end

      SEND_HIGH_S: begin
        if (ts_m_axis_tready)
          ts_state <= SEND_LOW_S;
      end

      SEND_LOW_S: begin
        if (ts_m_axis_tready) begin
          if (!rec_empty) begin           // stream the next record seamlessly
            cur_ts   <= q0_ts;
            cur_seq  <= q0_seq;
            cur_mt   <= q0_mt;
            pop_r    <= 1'b1;
            ts_state <= SEND_HIGH_S;
          end
          else begin
            ts_state <= IDLE_S;
          end
        end
      end

      default: ts_state <= IDLE_S;
    endcase
  end
end

endmodule

`default_nettype wire
