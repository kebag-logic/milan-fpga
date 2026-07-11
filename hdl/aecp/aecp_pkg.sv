/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : aecp_pkg.sv
  Description : Package for AECP (IEEE 1722.1-2021) — AEM listener.
                Constants, typedefs and status-bus structure shared by all
                KL_aecp_* modules.

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §9; Milan v1.2 §5.4
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

package aecp_pkg;

  // ------------------------------------------------------------------ //
  // AVTP / AECP framing constants                                        //
  // ------------------------------------------------------------------ //
  //! EtherType shared with ADP
  localparam [15:0] AVTP_ETYPE_C        = 16'h22F0;
  //! AECP AVTP subtype (IEEE 1722.1-2021 §9.1)
  localparam [7:0]  AECP_SUBTYPE_C      = 8'hFB;
  //! Milan Vendor-Unique protocol_id (OUI 00-1B-C5-0A-C1-00)
  localparam [47:0] MILAN_PROTOCOL_ID_C = 48'h001BC50AC100;

  // ------------------------------------------------------------------ //
  // AECP message_type field (4 bits, IEEE 1722.1-2021 Table 9.1)         //
  // ------------------------------------------------------------------ //
  localparam [3:0] MSG_AEM_COMMAND               = 4'd0;
  localparam [3:0] MSG_AEM_RESPONSE              = 4'd1;
  localparam [3:0] MSG_ADDRESS_ACCESS_COMMAND    = 4'd2;
  localparam [3:0] MSG_ADDRESS_ACCESS_RESPONSE   = 4'd3;
  localparam [3:0] MSG_AEM_IDENTIFY_NOTIFICATION = 4'd4;
  localparam [3:0] MSG_VENDOR_UNIQUE_COMMAND     = 4'd6;
  localparam [3:0] MSG_VENDOR_UNIQUE_RESPONSE    = 4'd7;

  // ------------------------------------------------------------------ //
  // AECP AEM command_type values (15 bits, IEEE 1722.1-2021 Table 7.128) //
  // ------------------------------------------------------------------ //
  localparam [14:0] CMD_ACQUIRE_ENTITY                     = 15'd0;
  localparam [14:0] CMD_LOCK_ENTITY                        = 15'd1;
  localparam [14:0] CMD_ENTITY_AVAILABLE                   = 15'd2;
  localparam [14:0] CMD_CONTROLLER_AVAILABLE               = 15'd3;
  localparam [14:0] CMD_READ_DESCRIPTOR                    = 15'd4;
  localparam [14:0] CMD_WRITE_DESCRIPTOR                   = 15'd5;
  localparam [14:0] CMD_SET_CONFIGURATION                  = 15'd6;
  localparam [14:0] CMD_GET_CONFIGURATION                  = 15'd7;
  localparam [14:0] CMD_SET_STREAM_FORMAT                  = 15'd8;
  localparam [14:0] CMD_GET_STREAM_FORMAT                  = 15'd9;
  localparam [14:0] CMD_SET_STREAM_INFO                    = 15'd14;
  localparam [14:0] CMD_GET_STREAM_INFO                    = 15'd15;
  localparam [14:0] CMD_SET_NAME                           = 15'd16;
  localparam [14:0] CMD_GET_NAME                           = 15'd17;
  localparam [14:0] CMD_SET_SAMPLING_RATE                  = 15'd20;
  localparam [14:0] CMD_GET_SAMPLING_RATE                  = 15'd21;
  localparam [14:0] CMD_SET_CLOCK_SOURCE                   = 15'd22;
  localparam [14:0] CMD_GET_CLOCK_SOURCE                   = 15'd23;
  localparam [14:0] CMD_SET_CONTROL                        = 15'd24;
  localparam [14:0] CMD_GET_CONTROL                        = 15'd25;
  localparam [14:0] CMD_START_STREAMING                    = 15'd34;
  localparam [14:0] CMD_STOP_STREAMING                     = 15'd35;
  localparam [14:0] CMD_REGISTER_UNSOLICITED_NOTIFICATION  = 15'd36;
  localparam [14:0] CMD_DEREGISTER_UNSOLICITED_NOTIFICATION= 15'd37;
  localparam [14:0] CMD_GET_AVB_INFO                       = 15'd39;
  localparam [14:0] CMD_GET_COUNTERS                       = 15'd41;
  localparam [14:0] CMD_GET_AUDIO_MAP                      = 15'd43;
  localparam [14:0] CMD_ADD_AUDIO_MAPPINGS                 = 15'd44;
  localparam [14:0] CMD_REMOVE_AUDIO_MAPPINGS              = 15'd45;

  // ------------------------------------------------------------------ //
  // AECP status codes (5 bits, IEEE 1722.1-2021 Table 7.126)             //
  // ------------------------------------------------------------------ //
  localparam [4:0] STATUS_SUCCESS            = 5'd0;
  localparam [4:0] STATUS_NOT_IMPLEMENTED    = 5'd1;
  localparam [4:0] STATUS_NO_SUCH_DESCRIPTOR = 5'd2;
  localparam [4:0] STATUS_ENTITY_LOCKED      = 5'd3;
  localparam [4:0] STATUS_ENTITY_ACQUIRED    = 5'd4;
  localparam [4:0] STATUS_NOT_AUTHENTICATED  = 5'd5;
  localparam [4:0] STATUS_AUTHENTICATION_DISABLED = 5'd6;
  localparam [4:0] STATUS_BAD_ARGUMENTS      = 5'd7;
  localparam [4:0] STATUS_NO_RESOURCES       = 5'd8;
  localparam [4:0] STATUS_IN_PROGRESS        = 5'd9;
  localparam [4:0] STATUS_ENTITY_MISBEHAVING = 5'd10;
  localparam [4:0] STATUS_NOT_SUPPORTED      = 5'd11;
  localparam [4:0] STATUS_STREAM_IS_RUNNING  = 5'd12;

  // ------------------------------------------------------------------ //
  // AEM descriptor_type constants (IEEE 1722.1-2021 Table 7.1)           //
  // ------------------------------------------------------------------ //
  localparam [15:0] DESC_ENTITY             = 16'h0000;
  localparam [15:0] DESC_CONFIGURATION      = 16'h0001;
  localparam [15:0] DESC_AUDIO_UNIT         = 16'h0002;
  localparam [15:0] DESC_VIDEO_UNIT         = 16'h0003;
  localparam [15:0] DESC_SENSOR_UNIT        = 16'h0004;
  localparam [15:0] DESC_STREAM_INPUT       = 16'h0005;
  localparam [15:0] DESC_STREAM_OUTPUT      = 16'h0006;
  localparam [15:0] DESC_JACK_INPUT         = 16'h0007;
  localparam [15:0] DESC_JACK_OUTPUT        = 16'h0008;
  localparam [15:0] DESC_AVB_INTERFACE      = 16'h0009;
  localparam [15:0] DESC_CLOCK_SOURCE       = 16'h000A;
  localparam [15:0] DESC_MEMORY_OBJECT      = 16'h000B;
  localparam [15:0] DESC_LOCALE             = 16'h000C;
  localparam [15:0] DESC_STRINGS            = 16'h000D;
  localparam [15:0] DESC_STREAM_PORT_INPUT  = 16'h000E;
  localparam [15:0] DESC_STREAM_PORT_OUTPUT = 16'h000F;
  localparam [15:0] DESC_EXTERNAL_PORT_INPUT  = 16'h0010;
  localparam [15:0] DESC_EXTERNAL_PORT_OUTPUT = 16'h0011;
  localparam [15:0] DESC_INTERNAL_PORT_INPUT  = 16'h0012;
  localparam [15:0] DESC_INTERNAL_PORT_OUTPUT = 16'h0013;
  localparam [15:0] DESC_AUDIO_CLUSTER      = 16'h0014;
  localparam [15:0] DESC_VIDEO_CLUSTER      = 16'h0015;
  localparam [15:0] DESC_SENSOR_CLUSTER     = 16'h0016;
  localparam [15:0] DESC_AUDIO_MAP          = 16'h0017;
  localparam [15:0] DESC_VIDEO_MAP          = 16'h0018;
  localparam [15:0] DESC_SENSOR_MAP         = 16'h0019;
  localparam [15:0] DESC_CONTROL            = 16'h001A;
  localparam [15:0] DESC_SIGNAL_SELECTOR    = 16'h001B;
  localparam [15:0] DESC_MIXER             = 16'h001C;
  localparam [15:0] DESC_MATRIX            = 16'h001D;
  localparam [15:0] DESC_MATRIX_SIGNAL     = 16'h001E;
  localparam [15:0] DESC_SIGNAL_SPLITTER   = 16'h001F;
  localparam [15:0] DESC_SIGNAL_COMBINER   = 16'h0020;
  localparam [15:0] DESC_SIGNAL_DEMULTIPLEXER = 16'h0021;
  localparam [15:0] DESC_SIGNAL_MULTIPLEXER   = 16'h0022;
  localparam [15:0] DESC_SIGNAL_TRANSCODER    = 16'h0023;
  localparam [15:0] DESC_CLOCK_DOMAIN      = 16'h0024;
  localparam [15:0] DESC_CONTROL_BLOCK     = 16'h0025;
  localparam [15:0] DESC_INVALID           = 16'hFFFF;

  // ------------------------------------------------------------------ //
  // Milan Vendor-Unique command codes (Milan v1.2 Table 5.18; the         //
  // reference header aecp-vendor-unique-milan-v12.h confirms 0x0000)      //
  // ------------------------------------------------------------------ //
  localparam [14:0] VU_GET_MILAN_INFO                   = 15'h0000;

  // ------------------------------------------------------------------ //
  // Sizing constants                                                     //
  // ------------------------------------------------------------------ //
  //! Max bounded controllers for unsolicited table
  localparam int unsigned MAX_UNSOLICITED_CTLR_C = 16;
  //! Single configuration (48/96/192 kHz handled via SET_SAMPLING_RATE
  //! within it — matches milan-v12-entity.json configurations_count=1)
  localparam int unsigned NUM_CONFIGURATIONS_C   = 1;
  //! Lock timer: 60 s × 1 kHz = 60 000 ticks
  localparam [16:0] LOCK_TIMER_TICKS_C = 17'd60_000;
  //! Controller staleness: 30 s × 1 kHz = 30 000 ticks
  localparam [15:0] STALE_TIMER_TICKS_C = 16'd30_000;
  //! GET_COUNTERS throttle: 1 s × 1 kHz = 1 000 ticks
  localparam [9:0]  COUNTER_THROTTLE_TICKS_C = 10'd1_000;

  // ------------------------------------------------------------------ //
  // AECP common parsed-header bus                                        //
  // Passed between all pipeline stages after KL_aecp_common_parser.     //
  // Modelled on adp_pkg::entity_info_t.                                  //
  // ------------------------------------------------------------------ //
  typedef struct packed {
    logic [3:0]  message_type;
    logic [4:0]  status;
    logic [10:0] control_data_length;
    logic [63:0] target_entity_id;
    logic [63:0] controller_entity_id;
    logic [15:0] sequence_id;
    logic        u_flag;               //!< unsolicited notification requested
    logic [14:0] command_type;
    //! bit0 of the ACQUIRE/LOCK 32-bit flags field (payload bytes 26-29):
    //! RELEASE / UNLOCK. Valid with hdr_valid for those two commands.
    logic        flags_lsb;
    //! following fields valid only for descriptor commands
    logic [15:0] configuration_index;  //!< SET_CONFIGURATION layout (bytes 28-29)
    logic [15:0] descriptor_type;      //!< READ_DESCRIPTOR layout (bytes 30-31)
    logic [15:0] descriptor_index;
    logic        hdr_valid;            //!< strobe: header fully parsed
  } aecp_hdr_t;

  // ------------------------------------------------------------------ //
  // L0 state output — used by response_builder & cmd_specific_extract   //
  // ------------------------------------------------------------------ //
  typedef struct packed {
    logic [63:0] entity_id;
    logic [15:0] current_configuration_index;
    logic        locked;
    logic        acquired;
    logic [63:0] acquiring_controller_id;
    logic [63:0] locking_controller_id;
  } aecp_l0_state_t;

  // ------------------------------------------------------------------ //
  // Accessor request/response bus                                        //
  // ------------------------------------------------------------------ //
  typedef struct packed {
    logic [3:0]  level;        //! 0=entity, 1=config, 2=desc_type, 3=descriptor
    logic [15:0] config_idx;
    logic [15:0] desc_type;
    logic [15:0] desc_idx;
    logic        valid;
  } aecp_acc_req_t;

  typedef struct packed {
    logic [15:0] bram_addr;    //! byte address in KL_aecp_aem_store
    logic [15:0] payload_size; //! bytes in this descriptor
    logic        dynamic_flag; //! one or more fields from dyn_mux
    logic [4:0]  status;       //! NO_SUCH_DESCRIPTOR if out of range
    logic        valid;
  } aecp_acc_resp_t;

endpackage
