/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <info@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

package avtp_aecp_pkg;
  import avtp_pkt_common_pkg::*;

  // AECP message_type constants
  localparam bit8 AECP_MSG_AEM_COMMAND    = 8'h00; // only lower 4 bits matter
  localparam bit8 AECP_MSG_AEM_RESPONSE   = 8'h01;
  localparam bit8 AECP_MSG_VU_COMMAND     = 8'h06;
  localparam bit8 AECP_MSG_VU_RESPONSE    = 8'h07;

  // AECP status codes
  localparam bit8 AECP_STATUS_SUCCESS     = 8'h00;
  localparam bit8 AECP_STATUS_NOT_IMPL    = 8'h01;
  localparam bit8 AECP_STATUS_NO_DESC     = 8'h02;
  localparam bit8 AECP_STATUS_LOCKED      = 8'h03;
  localparam bit8 AECP_STATUS_ACQUIRED    = 8'h04;
  localparam bit8 AECP_STATUS_BAD_ARGS    = 8'h07;
  localparam bit8 AECP_STATUS_INVALID_CMD = 8'h0A;
  localparam bit8 AECP_STATUS_PROTO_ERR   = 8'h0B;

  // AEM command types
  localparam bit16 AEM_CMD_ACQUIRE_ENTITY   = 16'h0000;
  localparam bit16 AEM_CMD_LOCK_ENTITY      = 16'h0001;
  localparam bit16 AEM_CMD_ENTITY_AVAILABLE = 16'h0002;
  localparam bit16 AEM_CMD_READ_DESCRIPTOR  = 16'h0004;
  localparam bit16 AEM_CMD_WRITE_DESCRIPTOR = 16'h0005;
  localparam bit16 AEM_CMD_SET_CONFIGURATION= 16'h0006;
  localparam bit16 AEM_CMD_GET_CONFIGURATION= 16'h0007;
  localparam bit16 AEM_CMD_SET_NAME         = 16'h0010;
  localparam bit16 AEM_CMD_GET_NAME         = 16'h0011;
  localparam bit16 AEM_CMD_REG_UNSOLICITED  = 16'h0024;
  localparam bit16 AEM_CMD_DEREG_UNSOLICITED= 16'h0025;
  localparam bit16 AEM_CMD_GET_COUNTERS     = 16'h0027;
  localparam bit16 AEM_CMD_GET_AUDIO_MAP    = 16'h0029;
  localparam bit16 AEM_CMD_ADD_AUDIO_MAP    = 16'h002A;
  localparam bit16 AEM_CMD_REM_AUDIO_MAP    = 16'h002B;

  // ACQUIRE_ENTITY flags
  localparam bit32 ACQUIRE_FLAG_RELEASE    = 32'h8000_0000;
  localparam bit32 ACQUIRE_FLAG_PERSISTENT = 32'h4000_0000;
  // LOCK_ENTITY flags
  localparam bit32 LOCK_FLAG_UNLOCK        = 32'h8000_0000;

  // AECP AEM common header struct
  typedef struct {
    bit [3:0]  message_type;          // AEM_COMMAND=0, AEM_RESPONSE=1
    bit [4:0]  status;                // 0=SUCCESS
    bit [10:0] control_data_length;
    bit64      target_entity_id;
    bit64      controller_entity_id;
    bit16      sequence_id;
    bit        u_flag;                // unsolicited flag
    bit [14:0] command_type;
  } avtp_aecp_common_hdr_t;

  // ACQUIRE_ENTITY payload
  typedef struct {
    avtp_aecp_common_hdr_t common;
    bit32  acquire_flags;
    bit64  owner_id;
    bit16  descriptor_type;
    bit16  descriptor_index;
  } avtp_aecp_acquire_t;

  // LOCK_ENTITY payload
  typedef struct {
    avtp_aecp_common_hdr_t common;
    bit32  lock_flags;
    bit64  locked_id;
    bit16  descriptor_type;
    bit16  descriptor_index;
  } avtp_aecp_lock_t;

  // READ_DESCRIPTOR payload
  typedef struct {
    avtp_aecp_common_hdr_t common;
    bit16  configuration_index;
    bit16  reserved;
    bit16  descriptor_type;
    bit16  descriptor_index;
  } avtp_aecp_read_desc_t;

  // No-payload commands (GET_CONFIGURATION, REGISTER/DEREGISTER_UNSOLICITED)
  typedef struct {
    avtp_aecp_common_hdr_t common;
  } avtp_aecp_no_payload_t;

  // SET_NAME payload (64 bytes name)
  typedef struct {
    avtp_aecp_common_hdr_t common;
    bit16  descriptor_type;
    bit16  descriptor_index;
    bit16  name_index;
    bit16  configuration_index;
    bit [511:0] name; // 64-byte UTF-8 string
  } avtp_aecp_set_name_t;

endpackage
