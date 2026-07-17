/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : avtp_stream_parser.sv
  Author      : Kebag Logic

  Date        : 2026-07-05
  Description : AVTP stream identifier + presentation-time extractor — the first
                RTL increment of the "AVTP stream engine" (S1 in
                docs/overview/AVB_SWITCH_DIRECTION.md hook A). It is a NON-INTRUSIVE
                MONITOR on an RX AXI-Stream carrying full Ethernet frames: it
                never backpressures or modifies the data path, it just parses
                each frame's header and, for AVTP stream packets whose
                stream_id matches a programmable table, emits one metadata pulse
                per frame carrying the matched stream index, the 64-bit
                stream_id, the 32-bit AVTP presentation timestamp and the
                subtype. Downstream (a later increment) uses `match_index` to
                route the sample payload into that stream's sample ring so
                PipeWire wakes per audio period, not per packet.

                Frame byte layout parsed (big-endian on the wire; this module
                converts LE beats when BIG_ENDIAN=0, like traffic_classifier):
                  [0..11]  dst/src MAC
                  [12..13] TPID: 0x8100 -> C-VLAN present (AVTP hdr +4), else
                           this is the EtherType
                  AVTP EtherType 0x22F0 at [12] (no VLAN) or [16] (VLAN)
                  AVTP common stream header at O = 14 (no VLAN) / 18 (VLAN):
                    O+0      subtype
                    O+1      [7]sv [6:4]version [0]tv (timestamp valid)
                    O+2      sequence_num
                    O+3      [0]tu
                    O+4..11  stream_id (64-bit, MS byte first)
                    O+12..15 avtp_timestamp (32-bit presentation time)

                Only STREAM subtypes (AAF/CVF/CRF/IIDC/MMA/TSCF/SVF/RVF) with
                sv=1 are considered; control subtypes (ADP/AECP/ACMP/MAAP) and
                non-AVTP frames produce no match. The parse reads a registered
                header buffer, so `match_valid` pulses one cycle, at the beat on
                which the last needed header byte (O+15) has been captured.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;
import avtp_subtype_pkg::*;

`default_nettype none

module avtp_stream_parser #(
  parameter int TDATA_WIDTH = 64,     //! AXIS data width
  parameter bit BIG_ENDIAN  = 0,      //! 0 = LE beats (datapath default)
  parameter int N_STREAMS   = 8       //! programmable stream-match table depth
)(
  input  wire clk,                    //! clock
  input  wire resetn,                 //! synchronous active-low reset

  //! --- programmable stream-match table (from CSR, later integration) ---
  input  wire [64*N_STREAMS-1:0] cfg_stream_id_i,   //! per-entry match stream_id
  input  wire [N_STREAMS-1:0]    cfg_stream_en_i,   //! per-entry valid

  //! --- monitored RX AXI-Stream (observed, never driven) ---
  input  wire [TDATA_WIDTH-1:0]     s_tdata_i,
  input  wire [TDATA_WIDTH/8-1:0]   s_tkeep_i,
  input  wire                       s_tvalid_i,
  input  wire                       s_tready_i,
  input  wire                       s_tlast_i,

  //! --- extracted per-frame metadata (one-cycle pulse on match) ---
  output logic                      match_valid_o,   //! matched AVTP stream frame
  output logic [$clog2(N_STREAMS)-1:0] match_index_o,//! matched table entry
  output logic [63:0]               stream_id_o,     //! parsed stream_id
  output logic [31:0]               avtp_ts_o,       //! presentation time
  output logic [7:0]                subtype_o,       //! AVTP subtype
  output logic                      ts_valid_o,      //! tv bit (ts is meaningful)
  output logic [7:0]                seq_num_o,       //! sequence_num (O+2)
  output logic                      ts_uncertain_o,  //! tu bit (O+3 bit 0)
  output logic [63:0]               fsh_o,           //! format-specific header
                                                     //! bytes O+16..O+23 (AAF:
                                                     //! format/nsr/ch/depth/
                                                     //! data_len/sp+evt)
  //! free-running counters (RMON-style, cleared by reset)
  output logic [31:0]               avtp_frames_o,   //! AVTP stream frames seen
  output logic [31:0]               matched_frames_o //! of those, matched a stream
);

  // Enough header bytes: worst case VLAN -> O=18, last needed byte is the
  // format-specific header's O+23 = 41 (AAF sp/event live at O+22).
  localparam int HDR_BYTES  = 48;                 // 6 beats @ 64b, covers 42
  localparam int HDRW       = HDR_BYTES * 8;
  localparam int BPW        = TDATA_WIDTH / 8;     // bytes per beat
  localparam int IDXW       = (N_STREAMS <= 1) ? 1 : $clog2(N_STREAMS);

  //! beat in big-endian byte order (byte 0 of the beat in the MS lane)
  wire [TDATA_WIDTH-1:0] beat_be = BIG_ENDIAN ? s_tdata_i
                                              : reorder_endian_func(s_tdata_i, TDATA_WIDTH);

  //! rolling header buffer, MS byte = frame byte 0 (same convention as the
  //! classifier). Shift a beat in on every accepted input beat until we hold
  //! HDR_BYTES; `bytes_in` saturates so mid/late beats don't disturb it.
  logic [HDRW-1:0]              hdr;
  logic [$clog2(HDR_BYTES+BPW):0] bytes_in;
  wire  in_acc  = s_tvalid_i && s_tready_i;
  wire  hdr_full_next = (bytes_in + BPW) >= HDR_BYTES;
  logic parsed;                                    // one match/count per frame

  //! byte accessor into the MS-first buffer
  function automatic [7:0] hbyte(input int n);
    return hdr[HDRW-1 - n*8 -: 8];
  endfunction

  //! --- combinational field extraction from the (current) header buffer ---
  wire        vlan     = (hbyte(12) == ETH_TYPE_VLAN[15:8]) &&
                         (hbyte(13) == ETH_TYPE_VLAN[7:0]);
  wire [4:0]  et_off   = vlan ? 5'd16 : 5'd12;     // EtherType byte offset
  wire        is_avtp  = (hbyte(et_off)   == ETH_TYPE_AVTP[15:8]) &&
                         (hbyte(et_off+1) == ETH_TYPE_AVTP[7:0]);
  wire [5:0]  o        = et_off + 6'd2;            // AVTP common header offset
  wire [7:0]  subtype  = hbyte(o);
  wire [7:0]  b1       = hbyte(o+1);
  wire        sv       = b1[7];
  wire        tv       = b1[0];
  wire [63:0] sid      = {hbyte(o+4), hbyte(o+5), hbyte(o+6),  hbyte(o+7),
                          hbyte(o+8), hbyte(o+9), hbyte(o+10), hbyte(o+11)};
  wire [31:0] ats      = {hbyte(o+12), hbyte(o+13), hbyte(o+14), hbyte(o+15)};
  wire [7:0]  seq      = hbyte(o+2);
  wire        tu       = hbyte(o+3) & 8'h01 ? 1'b1 : 1'b0;
  wire [63:0] fsh      = {hbyte(o+16), hbyte(o+17), hbyte(o+18), hbyte(o+19),
                          hbyte(o+20), hbyte(o+21), hbyte(o+22), hbyte(o+23)};

  //! stream subtypes (IEEE 1722-2016 Table 6): 0x00..0x07 are the stream data
  //! subtypes (IIDC, MMA, AAF, CVF, CRF, TSCF, SVF, RVF).
  wire is_stream_subtype = (subtype <= 8'h07);

  //! match the parsed stream_id against the enabled table entries
  logic                match_hit;
  logic [IDXW-1:0]     match_idx;
  always_comb begin
    match_hit = 1'b0;
    match_idx = '0;
    for (int e = 0; e < N_STREAMS; e++) begin
      if (cfg_stream_en_i[e] && (cfg_stream_id_i[e*64 +: 64] == sid)) begin
        match_hit = 1'b1;
        match_idx = IDXW'(e);
      end
    end
  end

  //! the parse fires on the beat that completes the AVTP header (byte o+15),
  //! exactly once per frame, and only for AVTP stream packets with sv=1.
  wire hdr_ready = (bytes_in >= HDR_BYTES);
  wire fire      = in_acc && hdr_ready && !parsed && is_avtp && is_stream_subtype && sv;

  always_ff @(posedge clk) begin : parse
    if (!resetn) begin
      hdr            <= '0;
      bytes_in       <= '0;
      parsed         <= 1'b0;
      match_valid_o  <= 1'b0;
      match_index_o  <= '0;
      stream_id_o    <= '0;
      avtp_ts_o      <= '0;
      subtype_o      <= '0;
      ts_valid_o     <= 1'b0;
      seq_num_o      <= '0;
      ts_uncertain_o <= 1'b0;
      fsh_o          <= '0;
      avtp_frames_o  <= '0;
      matched_frames_o <= '0;
    end else begin
      match_valid_o <= 1'b0;               // default: single-cycle pulse

      if (in_acc) begin
        // shift the beat in until the buffer holds the header
        if (!hdr_ready)
          hdr <= {hdr[HDRW-TDATA_WIDTH-1:0], beat_be};
        if (!hdr_full_next && !hdr_ready)
          bytes_in <= bytes_in + BPW;
        else if (!hdr_ready)
          bytes_in <= HDR_BYTES[$clog2(HDR_BYTES+BPW):0];

        if (fire) begin
          parsed           <= 1'b1;
          match_index_o    <= IDXW'(match_idx);
          stream_id_o      <= sid;
          avtp_ts_o        <= ats;
          subtype_o        <= subtype;
          ts_valid_o       <= tv;
          seq_num_o        <= seq;
          ts_uncertain_o   <= tu;
          fsh_o            <= fsh;
          match_valid_o    <= match_hit;
          avtp_frames_o    <= avtp_frames_o + 1'b1;
          if (match_hit) matched_frames_o <= matched_frames_o + 1'b1;
        end

        if (s_tlast_i) begin               // end of frame: rearm for the next
          bytes_in <= '0;
          parsed   <= 1'b0;
        end
      end
    end
  end : parse

endmodule

`default_nettype wire
