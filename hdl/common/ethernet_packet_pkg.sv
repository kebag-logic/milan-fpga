/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : ethernet_packet_pkg.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-06-28
  Description : Ethernet packet definitions for VLAN-aware traffic classification.

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper

------------------------------------------------------------------------------
*/

`include "parameters.svh"

`ifndef ETHERNET_PACKET_PKG_SV
`define ETHERNET_PACKET_PKG_SV

package ethernet_packet_pkg;

// -----------------------------------------------------------------------------
// Constants and Parameters
// -----------------------------------------------------------------------------


//! Number of bits in a byte.
parameter int BYTE_TO_BIT     = 8;

//! Default data width for AXI-Stream (can be overridden).
parameter int TDATA_WIDTH = `AXIS_DATA_WIDTH;

//! MAC address width in bytes and bits.
parameter int MAC_ADDR_WIDTH  = 6;
parameter int MAC_ADDR_BIT_WIDTH  = MAC_ADDR_WIDTH * BYTE_TO_BIT;

//! Ethertype field width in bytes and bits.
parameter int ETH_TYPE_WIDTH  = 2;
parameter int ETH_TYPE_BIT_WIDTH  = ETH_TYPE_WIDTH * BYTE_TO_BIT;

//! VLAN TPID and TCI widths.
parameter int VLAN_TPID_WIDTH = 2;
parameter int VLAN_TPID_BIT_WIDTH = VLAN_TPID_WIDTH * BYTE_TO_BIT;
parameter int VLAN_TCI_WIDTH  = 2;
parameter int VLAN_TCI_BIT_WIDTH  = VLAN_TCI_WIDTH * BYTE_TO_BIT;

//! Total VLAN tag size (TPID + TCI) in bytes.
parameter int VLAN_TAG_WIDTH  = VLAN_TPID_WIDTH + VLAN_TCI_WIDTH;

//! Total Ethernet header width (with VLAN) in bytes and bits.
parameter int ETH_HEADER_WIDTH = (MAC_ADDR_WIDTH * 2) + ETH_TYPE_WIDTH + VLAN_TAG_WIDTH;
parameter int ETH_HEADER_BIT_WIDTH = ETH_HEADER_WIDTH * BYTE_TO_BIT;

//! Number of chunks needed to capture entire header using TDATA_WIDTH granularity.
parameter int ETH_HEADER_CHUNKS = (ETH_HEADER_BIT_WIDTH + TDATA_WIDTH - 1) / TDATA_WIDTH;
parameter int ETH_HEADER_BUFFER_WIDTH = ETH_HEADER_CHUNKS * TDATA_WIDTH;

//! PCP field width (IEEE 802.1Q: 3 bits)
parameter int PCP_BIT_WIDTH = 3;

//! Number of egress queues (traffic classes), q0 .. q5.
//! 802.1Q ORDER: the HIGHER index is the HIGHER priority, so q5 (SR class A)
//! wins arbitration over q0 (best effort). See `network_priority_t` and
//! docs/reference/EGRESS_QUEUE_MAP.md for the full map and the reasoning.
parameter int NUMBER_OF_QUEUES = 6;

//! Priority Queues Bit field
parameter int PRIORITY_QUEUES_BIT_WIDTH = $clog2(NUMBER_OF_QUEUES);

// -----------------------------------------------------------------------------
// Ethernet Header Structs
// -----------------------------------------------------------------------------

//! Basic Ethernet header (Dst MAC, Src MAC, Ethertype)
typedef struct packed {
  logic [MAC_ADDR_BIT_WIDTH-1:0] dst_mac;
  logic [MAC_ADDR_BIT_WIDTH-1:0] src_mac;
  logic [ETH_TYPE_BIT_WIDTH-1:0] eth_type;
} ethernet_hdr_t;

//! VLAN-tagged Ethernet header (includes TCI and TPID)
typedef struct packed {
  ethernet_hdr_t eth_common_hdr;
  logic [VLAN_TPID_BIT_WIDTH-1:0] vlan_tpid;
  logic [VLAN_TCI_BIT_WIDTH-1:0] vlan_tci;
} ethernet_vlan_hdr_t;

// -----------------------------------------------------------------------------
// Ethernet Ethertype Constants
// -----------------------------------------------------------------------------

//! VLAN-tagged Ethernet frame
parameter logic [ETH_TYPE_BIT_WIDTH-1:0] ETH_TYPE_VLAN = 16'h8100;
//! Precision Time Protocol (PTP) Ethernet type
parameter logic [ETH_TYPE_BIT_WIDTH-1:0] ETH_TYPE_PTP = 16'h88F7;
//! 1722 IEEE Audio Video Transport Protocol (AVTP) Ethernet type
parameter logic [ETH_TYPE_BIT_WIDTH-1:0] ETH_TYPE_AVTP = 16'h22F0;

// -----------------------------------------------------------------------------
// Endianness Conversion Function
// -----------------------------------------------------------------------------

//! Reorder bytes in a word from little-endian to big-endian.
//! @param data_in Input data word.
//! @param width Bit-width of the data (must be multiple of 8).
//! @return Reordered data word.
function automatic logic [TDATA_WIDTH-1:0] reorder_endian_func(
  input logic [TDATA_WIDTH-1:0] data_in,
  input int width
);
  logic [TDATA_WIDTH-1:0] data_out;
  for(int i=0; i < width/BYTE_TO_BIT; i++)begin
    data_out[i*BYTE_TO_BIT+:BYTE_TO_BIT] = data_in[(width - BYTE_TO_BIT*(i+1))+: BYTE_TO_BIT];
  end
  return data_out;
endfunction

// -----------------------------------------------------------------------------
// Simplified Network Priority Classes
// -----------------------------------------------------------------------------

/**
 * @typedef network_priority_t
 * @brief Enumerated priority classes based on IEEE 802.1Q standard.
 *
 * These classes are used to categorize incoming Ethernet traffic for
 * queue-based scheduling. Each class is mapped to a distinct output queue,
 * and the ENUM VALUE *IS* THE QUEUE INDEX: higher index = higher priority
 * (802.1Q order), so the arbiter in traffic_shaping_core grants q5 first and
 * q0 last.
 *
 *   q5  SRA_CLASS       CBS-shaped SR class A - every MSRP-reserved AVB stream
 *   q4  SRB_CLASS       CBS-shaped SR class B (provisioned, unused today)
 *   q3  GPTP_CLASS      802.1AS / gPTP (CPU path)
 *   q2  CONTROL_CLASS   MAAP, MSRP, MVRP, 1722.1 ADP / ACMP / AECP
 *   q1  RESERVED_CLASS  spare, deliberately unmapped
 *   q0  BEST_EFFORT     everything else, to/from the CPU
 *
 * WHY gPTP SITS *BELOW* THE SHAPED CLASSES (correctness, not preference):
 * 802.1Q-2018 8.6.8.2 credit-based shaping assumes the shaped queues are the
 * top of the strict-priority order. A strict-priority queue ABOVE them can
 * preempt a class-A frame whose credit has already been earned, so the credit
 * accounting no longer bounds the class-A latency it is supposed to bound -
 * the shaper's guarantee is void. gPTP tolerates the demotion because every
 * event message is hardware-timestamped at the egress SFD (ptp_ts_top), so a
 * queueing delay changes only *when* the message leaves, never the timestamp
 * it carries - the residence time lands in the correction field where the
 * protocol already accounts for it. Do NOT "fix" this by promoting gPTP.
 */

typedef enum logic [PRIORITY_QUEUES_BIT_WIDTH-1:0] {
  BEST_EFFORT    = 3'd0, //!< q0: default for non-prioritized traffic (lowest)
  RESERVED_CLASS = 3'd1, //!< q1: spare slot, nothing is mapped here
  CONTROL_CLASS  = 3'd2, //!< q2: MAAP/MSRP/MVRP + 1722.1 ADP/ACMP/AECP
  GPTP_CLASS     = 3'd3, //!< q3: gPTP (Generalized Precision Time Protocol)
  SRB_CLASS      = 3'd4, //!< q4: Stream Reservation Class B (CBS shaped)
  SRA_CLASS      = 3'd5  //!< q5: Stream Reservation Class A (highest priority)
} network_priority_t;

// -----------------------------------------------------------------------------
// CBS Algorithm parameters and priority encoding function
// -----------------------------------------------------------------------------

/**
 * @brief Priority encoder function for queue arbitration.
 *
 * @param req Request vector. Each bit corresponds to a queue.
 * @return Index of the HIGHEST-NUMBERED active request
 *         (NUMBER_OF_QUEUES-1 = highest priority, 0 = lowest).
 *         Returns -1 if no request is active.
 *
 * 802.1Q ORDER (changed with the 6-queue map): the scan runs from the top
 * index DOWN, so q5 (SR class A) beats q4 (class B) beats q3 (gPTP) ...
 * beats q0 (best effort). It used to scan upward with q0 as the winner; the
 * enum `network_priority_t` was renumbered in the same commit so every
 * symbolic user (SRA_CLASS, GPTP_CLASS, ...) keeps its relative rank.
 *
 * This function is synthesizable since it uses a single return
 * statement and a deterministic loop.
 */
function automatic int priority_encode(input logic [NUMBER_OF_QUEUES-1:0] req);
  int sel;
  sel = -1;
  for (int i = NUMBER_OF_QUEUES - 1; i >= 0; i--) begin
    if (req[i] && sel == -1) begin
      sel = i;
    end
  end
  return sel;
endfunction

//! Array of idle slopes (bps) for each traffic class for 1GBps.
//! The idle slope defines the rate at which credit increases when the queue is idle and has data.
//! It is proportional to the guaranteed bandwidth for that traffic class.
//!
//! INDEXED BY QUEUE, so entry 0 is q0 = BEST_EFFORT and entry 5 is q5 =
//! SR class A. (Before the 6-queue map this array ran the other way round -
//! entry 0 was class A - because q0 used to be the highest priority.)
//!
//! These are the *reset defaults* only: at runtime the shaper is reprogrammed
//! per queue from the milan_csr CBS registers (REQ-CBS-01). The sum across all
//! six classes is 750 Mb/s = 75 % of the 1 Gb/s port rate, honouring the
//! 802.1Qav deltaBandwidth <= 75 % guidance (REQ-CBS-03); the shaped pair
//! alone (q5 + q4 = 600 Mb/s = 60 %) is likewise inside that ceiling, which is
//! the number 802.1Q-2018 34.3.1 actually constrains. The milan_csr reset
//! defaults mirror these values.
parameter int IDLE_SLOPE_1G [0:NUMBER_OF_QUEUES-1] = '{
   25_000_000,  //!< q0 Best Effort  (2.5 %)
   25_000_000,  //!< q1 Reserved     (2.5 %, spare slot)
   50_000_000,  //!< q2 Control      (5 %)
   50_000_000,  //!< q3 gPTP         (5 %)
  150_000_000,  //!< q4 SR Class B   (15 %, CBS)
  450_000_000   //!< q5 SR Class A   (45 %, CBS - the AVB streams)
};

//! Array of idle slopes (bps) for each traffic class for 100MBps.
//! The idle slope defines the rate at which credit increases when the queue is idle and has data.
//! It is proportional to the guaranteed bandwidth for that traffic class.
//! Same queue order as IDLE_SLOPE_1G; sum is 75 Mb/s = 75 % of the 100 Mb/s
//! port rate (REQ-CBS-03).
parameter int IDLE_SLOPE_100M [0:NUMBER_OF_QUEUES-1] = '{
   2_500_000,  //!< q0 Best Effort
   2_500_000,  //!< q1 Reserved
   5_000_000,  //!< q2 Control
   5_000_000,  //!< q3 gPTP
  15_000_000,  //!< q4 SR Class B
  45_000_000   //!< q5 SR Class A
};

//! Maximum  frame length for MTU1500
parameter int MAX_FRAME_SIZE = 1522;

//! Function that calculates high credit given idle_slope and port_rate
function automatic int calc_hi_credit(
  input int idle_slope,
  input int port_rate
);
  longint tmp;
  tmp = (longint'(MAX_FRAME_SIZE) * longint'(idle_slope)) / longint'(port_rate);
  return int'(tmp);
endfunction

//! Function that calculates low credit given idle_slope and port_rate
function automatic int calc_lo_credit(
  input int idle_slope,
  input int port_rate
);
  longint tmp;
  tmp = (longint'(MAX_FRAME_SIZE) * (longint'(idle_slope) - longint'(port_rate))) / longint'(port_rate);
  return int'(tmp);
endfunction

//! Maksimum credit threshold (in bytes).
//! A queue can accumulate credit up to this value during idle periods. Beyond this, credit
//! accumulation stops.
parameter int HI_CREDIT [0:NUMBER_OF_QUEUES-1] = '{
  calc_hi_credit(IDLE_SLOPE_1G[0], 1_000_000_000),
  calc_hi_credit(IDLE_SLOPE_1G[1], 1_000_000_000),
  calc_hi_credit(IDLE_SLOPE_1G[2], 1_000_000_000),
  calc_hi_credit(IDLE_SLOPE_1G[3], 1_000_000_000),
  calc_hi_credit(IDLE_SLOPE_1G[4], 1_000_000_000),
  calc_hi_credit(IDLE_SLOPE_1G[5], 1_000_000_000)
};

//! Minimum credit threshold (in bytes).
//! A queue can lose credit up to this value during send periods. Beyond this, credit
//! decrement stops.
parameter int LO_CREDIT [0:NUMBER_OF_QUEUES-1] = '{
  calc_lo_credit(IDLE_SLOPE_1G[0], 1_000_000_000),
  calc_lo_credit(IDLE_SLOPE_1G[1], 1_000_000_000),
  calc_lo_credit(IDLE_SLOPE_1G[2], 1_000_000_000),
  calc_lo_credit(IDLE_SLOPE_1G[3], 1_000_000_000),
  calc_lo_credit(IDLE_SLOPE_1G[4], 1_000_000_000),
  calc_lo_credit(IDLE_SLOPE_1G[5], 1_000_000_000)
};

//! Clock frequency used for credit slope calculations.
//! Unit: Hertz (Hz). Determines the slope-per-cycle resolution.
parameter int CLK_FREQ_HZ = 100_000_000;

//! Fixed-point scaling factor (Q16 format).
//! Used to convert slope values from integer to fixed-point representation.
parameter int FP_DECIMAL_POINT = 16;

// -----------------------------------------------------------------------------
// PTP packet parameters
// -----------------------------------------------------------------------------

//! Timestamp info bit width
parameter int TIMESTAMP_BIT_WIDTH          = 64;

//! gPTP/IEEE 1588v2 PTP Header Field Widths (in bytes)
parameter int PTP_MSG_TYPE_WIDTH           = 1;
parameter int PTP_VERSION_WIDTH            = 1;
parameter int PTP_MSG_LENGTH_WIDTH         = 2;
parameter int PTP_DOMAIN_NUM_WIDTH         = 1;
parameter int PTP_RESERVED1_WIDTH          = 1;
parameter int PTP_FLAGS_WIDTH              = 2;
parameter int PTP_CORRECTION_FIELD_WIDTH   = 8;
parameter int PTP_RESERVED2_WIDTH          = 4;
parameter int PTP_CLK_IDENTITY_WIDTH       = 8;
parameter int PTP_SOURCE_PORT_ID_WIDTH     = 2;
parameter int PTP_SEQ_ID_WIDTH             = 2;
parameter int PTP_CONTROL_FIELD_WIDTH      = 1;
parameter int PTP_LOG_MSG_INTERVAL_WIDTH   = 1;

//! Offset of sequenceId within the PTP message
parameter int PTP_SEQ_ID_OFFSET_IN_PTP = 
  PTP_MSG_TYPE_WIDTH +
  PTP_VERSION_WIDTH +
  PTP_MSG_LENGTH_WIDTH +
  PTP_DOMAIN_NUM_WIDTH +
  PTP_RESERVED1_WIDTH +
  PTP_FLAGS_WIDTH +
  PTP_CORRECTION_FIELD_WIDTH +
  PTP_RESERVED2_WIDTH +
  PTP_CLK_IDENTITY_WIDTH +
  PTP_SOURCE_PORT_ID_WIDTH;

//! Offset of Ethernet header (Dst MAC + Src MAC + Ethertype)
parameter int ETH_HEADER_NO_VLAN_WIDTH = (MAC_ADDR_WIDTH * 2) + ETH_TYPE_WIDTH;
parameter int ETH_HEADER_NO_VLAN_OFFSET = (MAC_ADDR_WIDTH * 2);

//! Absolute byte offset of sequence ID from Ethernet frame start (gPTP)
parameter int PTP_SEQ_ID_OFFSET = ETH_HEADER_NO_VLAN_WIDTH + PTP_SEQ_ID_OFFSET_IN_PTP;

//! PTP message sequence ID bit width
parameter int PTP_SEQ_ID_BIT_WIDTH = PTP_SEQ_ID_WIDTH * BYTE_TO_BIT;

//! Timestamp metadata structure to be sent to PS
typedef struct packed {
  bit direction; //! 0 for rx packets, 1 for tx packets
  logic [PTP_SEQ_ID_BIT_WIDTH-1:0] seq_id; // sequence id of ptp message
  logic [TIMESTAMP_BIT_WIDTH-1:0] timestamp; // timestamp value of the packet
} ts_metadata;

endpackage

`endif // ETHERNET_PACKET_PKG_SV
