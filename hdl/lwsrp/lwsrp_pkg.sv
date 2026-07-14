/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : lwsrp_pkg.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : Wire-format and timing constants for the lightweight SRP
//                talker endpoint (docs/LWSRP_FPGA_ARCHITECTURE.md).
//                Byte-exact contract extracted from the pipewire module-avb
//                reference (mrp.c/msrp.c/mvrp.c) 2026-07-14:
//                  - MRPDU = version(1)=0, Messages, message-list EndMark.
//                  - MSRP message header carries AttributeListLength(2)
//                    (= vector hdr + FirstValue + event[+param] bytes + the
//                    2-byte vector EndMark); MVRP has NO such field.
//                  - VectorHeader(2) = {LeaveAllEvent[15:13], NumberOfValues
//                    [12:0]}; RX treats ANY nonzero LeaveAllEvent as LeaveAll.
//                  - ThreePacked = e0*36 + e1*6 + e2 (e0 most significant);
//                    single-value TX = event*36.
//                  - FourPacked (Listener only) = p0*64 + ...; single-value
//                    TX = param*64.
//                  - All multi-byte fields network/big-endian on the wire.
//                Deviation from the reference (doc-normative, Milan-correct):
//                the reference ignores the four-packed listener declaration
//                when activating the talker; we gate on Ready/ReadyFailed.
//---------------------------------------------------------------------------//

package lwsrp_pkg;

  // ---- Ethernet encapsulation (802.1Q §35/§11; link-local, never bridged) --
  localparam [47:0] MSRP_MCAST_MAC_C  = 48'h0180_C200_000E;
  localparam [47:0] MVRP_MCAST_MAC_C  = 48'h0180_C200_0021;
  localparam [15:0] MSRP_ETHERTYPE_C  = 16'h22EA;
  localparam [15:0] MVRP_ETHERTYPE_C  = 16'h88F5;
  localparam [7:0]  MRP_PROTO_VER_C   = 8'h00;

  // ---- MSRP attribute types + FirstValue lengths (802.1Q §35.2.2.4) -------
  localparam [7:0] MSRP_ATTR_TALKER_ADV_C    = 8'd1;   //! 25 B FirstValue
  localparam [7:0] MSRP_ATTR_TALKER_FAILED_C = 8'd2;   //! 34 B (RX-only)
  localparam [7:0] MSRP_ATTR_LISTENER_C      = 8'd3;   //! 8 B + FourPacked
  localparam [7:0] MSRP_ATTR_DOMAIN_C        = 8'd4;   //! 4 B
  localparam [7:0] MVRP_ATTR_VID_C           = 8'd1;   //! 2 B

  localparam [7:0] MSRP_LEN_TALKER_ADV_C    = 8'd25;
  localparam [7:0] MSRP_LEN_TALKER_FAILED_C = 8'd34;
  localparam [7:0] MSRP_LEN_LISTENER_C      = 8'd8;
  localparam [7:0] MSRP_LEN_DOMAIN_C        = 8'd4;
  localparam [7:0] MVRP_LEN_VID_C           = 8'd2;

  //! AttributeListLength for our single-value TX vectors
  //! (= 2 vector hdr + FirstValue + 1 event byte + 2 vector EndMark)
  localparam [15:0] MSRP_ALL_DOMAIN_C     = 16'd9;    //! 2+4+1+2
  localparam [15:0] MSRP_ALL_TALKER_ADV_C = 16'd30;   //! 2+25+1+2
  localparam [15:0] MSRP_ALL_LISTENER_C   = 16'd14;   //! 2+8+1+1+2

  // ---- MRP AttributeEvent (three-packed, radix 6, e0 most significant) ----
  localparam [2:0] MRP_EVT_NEW_C    = 3'd0;
  localparam [2:0] MRP_EVT_JOININ_C = 3'd1;
  localparam [2:0] MRP_EVT_IN_C     = 3'd2;
  localparam [2:0] MRP_EVT_JOINMT_C = 3'd3;
  localparam [2:0] MRP_EVT_MT_C     = 3'd4;
  localparam [2:0] MRP_EVT_LV_C     = 3'd5;

  // ---- MSRP Listener declaration (four-packed, radix 4) -------------------
  localparam [1:0] LSTN_DECL_IGNORE_C       = 2'd0;
  localparam [1:0] LSTN_DECL_ASKING_FAIL_C  = 2'd1;
  localparam [1:0] LSTN_DECL_READY_C        = 2'd2;
  localparam [1:0] LSTN_DECL_READY_FAIL_C   = 2'd3;

  // ---- SR class A constants (Milan v1.2 §5.6: class A only) ---------------
  localparam [7:0] SR_CLASS_A_ID_C   = 8'd6;
  localparam [7:0] SR_CLASS_A_PRIO_C = 8'd3;
  localparam       SR_RANK_C         = 1'b1;
  //! PriorityAndRank byte: priority[7:5]=3, rank[4]=1, reserved[3:0]=0
  localparam [7:0] SR_PRIO_RANK_C    = {SR_CLASS_A_PRIO_C[2:0], SR_RANK_C, 4'h0};

  // ---- MRP timers (802.1Q Table 10-7 defaults; doc-normative values) ------
  //! Reference (pipewire mrp.c) runs 100/1000/10000-15000 ms; both conform.
  localparam int unsigned JOIN_TIME_MS_C     = 200;
  localparam int unsigned LEAVE_TIME_MS_C    = 600;
  localparam int unsigned LEAVEALL_TIME_MS_C = 10_000;

  // ---- Class-A bandwidth math (LWSRP_FPGA_ARCHITECTURE.md §2) -------------
  //! idleSlope[bps] = MaxIntervalFrames * (MaxFrameSize + 42) * 8 * 8000
  //! 42 = preamble 8 + eth hdr 14 + VLAN 4 + FCS 4 + IPG 12
  localparam int unsigned MSRP_FRAME_OVERHEAD_C   = 42;
  localparam int unsigned CLASS_A_INTERVALS_PS_C  = 8000;   //! per second

  //! 75 % reservation ceiling (Milan §5.6 / 802.1Q §34.3.1)
  localparam int unsigned SRP_BW_LIMIT_PCT_C = 75;

endpackage
