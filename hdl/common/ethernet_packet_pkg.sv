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

//! Number of Queues
parameter int NUMBER_OF_QUEUES = 4;

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
 * queue-based scheduling. Each class is mapped to a distinct output queue.
 */

typedef enum logic [PRIORITY_QUEUES_BIT_WIDTH-1:0] {
  SRA_CLASS,      //!< Stream Reservation Class A (highest priority)
  GPTP_CLASS,     //!< gPTP (Generalized Precision Time Protocol)
  CONTROL_CLASS, //!< Control traffic (ATDECC)
  BEST_EFFORT     //!< Default for non-prioritized traffic
} network_priority_t;

// -----------------------------------------------------------------------------
// CBS Algorithm parameters and priority encoding function
// -----------------------------------------------------------------------------

/**
 * @brief Priority encoder function for queue arbitration.
 *
 * @param req One-hot request vector. Each bit corresponds to a queue.
 * @return Index of the first active request (0 = highest priority).
 *         Returns -1 if no request is active.
 *
 * This function is synthesizable since it uses a single return
 * statement and a deterministic loop.
 */
function automatic int priority_encode(input logic [NUMBER_OF_QUEUES-1:0] req);
  int sel;
  sel = -1;
  for (int i = 0; i < NUMBER_OF_QUEUES; i++) begin
    if (req[i] && sel == -1) begin
      sel = i;
    end
  end
  return sel;
endfunction

//! Array of idle slopes (bps) for each traffic class for 1GBps.
//! The idle slope defines the rate at which credit increases when the queue is idle and has data.
//! It is proportional to the guaranteed bandwidth for that traffic class.
parameter int IDLE_SLOPE_1G [0:NUMBER_OF_QUEUES-1] = '{
  500_000_000,  //!< Class A (high BW)
  250_000_000,  //!< gPTP
  150_000_000,  //!< Control traffic
  100_000_000   //!< Best Effort(lowest BW)
};

//! Array of idle slopes (bps) for each traffic class for 100MBps.
//! The idle slope defines the rate at which credit increases when the queue is idle and has data.
//! It is proportional to the guaranteed bandwidth for that traffic class.
parameter int IDLE_SLOPE_100M [0:NUMBER_OF_QUEUES-1] = '{
  50_000_000,  //!< Class A (high BW)
  25_000_000,  //!< gPTP
  15_000_000,  //!< Control traffic
  10_000_000   //!< Best Effort(lowest BW)
};

//! Maksimum credit threshold (in bytes).
//! A queue can accumulate credit up to this value during idle periods. Beyond this, credit
//! accumulation stops.
parameter int HI_CREDIT   = 1536;

//! Minimum credit threshold (in bytes).
//! If credit drops below this value during transmission, the queue must wait to regain credit
//! before continuing.
parameter int LO_CREDIT   = -1536;

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