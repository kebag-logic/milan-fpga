/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : acmp_pkg.sv
//  Project     : Milan ACMP  (IEEE 1722.1-2021 Clause 8, AVnu Milan v1.2 §5.5)
//
//  Description : Shared constants for the ACMP (connection management)
//                responder. Mirrors the pipewire module-avb reference
//                (acmp.h) and IEEE 1722.1-2021 Table 8-1/8-2.
//
//  ACMPDU      : 56 B after the Ethernet header (frame = 70 B):
//                subtype(1) sv/ver/message_type(1) status/cdl(2) stream_id(8)
//                controller_entity_id(8) talker_entity_id(8)
//                listener_entity_id(8) talker_unique_id(2)
//                listener_unique_id(2) stream_dest_mac(6) connection_count(2)
//                sequence_id(2) flags(2) stream_vlan_id(2) reserved(2).
//                control_data_length = 44 (octets after stream_id).
//---------------------------------------------------------------------------//

`default_nettype none

package acmp_pkg;

  localparam [7:0]  ACMP_SUBTYPE_C   = 8'hFC;
  localparam [10:0] ACMP_CDL_C       = 11'd44;
  localparam int    ACMP_FRAME_BYTES_C = 70;   //! 14 Eth + 56 ACMPDU

  // message_type (IEEE 1722.1-2021 Table 8-1)
  localparam [3:0] ACMP_CONNECT_TX_COMMAND_C        = 4'd0;
  localparam [3:0] ACMP_CONNECT_TX_RESPONSE_C       = 4'd1;
  localparam [3:0] ACMP_DISCONNECT_TX_COMMAND_C     = 4'd2;
  localparam [3:0] ACMP_DISCONNECT_TX_RESPONSE_C    = 4'd3;
  localparam [3:0] ACMP_GET_TX_STATE_COMMAND_C      = 4'd4;
  localparam [3:0] ACMP_GET_TX_STATE_RESPONSE_C     = 4'd5;
  localparam [3:0] ACMP_GET_TX_CONNECTION_COMMAND_C = 4'd12;
  localparam [3:0] ACMP_GET_TX_CONNECTION_RESPONSE_C= 4'd13;

  // status (IEEE 1722.1-2021 Table 8-2)
  localparam [4:0] ACMP_STATUS_SUCCESS_C            = 5'd0;
  localparam [4:0] ACMP_STATUS_TALKER_UNKNOWN_ID_C  = 5'd2;
  localparam [4:0] ACMP_STATUS_NOT_SUPPORTED_C      = 5'd31;

  // flags cleared in a talker state response (pipewire reference behaviour)
  localparam [15:0] ACMP_FLAG_FAST_CONNECT_C        = 16'h0002;
  localparam [15:0] ACMP_FLAG_STREAMING_WAIT_C      = 16'h0008;
  localparam [15:0] ACMP_FLAG_SRP_REG_FAILED_C      = 16'h0040;

endpackage

`default_nettype wire
