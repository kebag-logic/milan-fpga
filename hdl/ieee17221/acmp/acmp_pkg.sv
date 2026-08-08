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
  localparam [3:0] ACMP_CONNECT_RX_COMMAND_C        = 4'd6;   //! Milan BIND_RX
  localparam [3:0] ACMP_CONNECT_RX_RESPONSE_C       = 4'd7;
  localparam [3:0] ACMP_DISCONNECT_RX_COMMAND_C     = 4'd8;   //! Milan UNBIND_RX
  localparam [3:0] ACMP_DISCONNECT_RX_RESPONSE_C    = 4'd9;
  localparam [3:0] ACMP_GET_RX_STATE_COMMAND_C      = 4'd10;
  localparam [3:0] ACMP_GET_RX_STATE_RESPONSE_C     = 4'd11;
  localparam [3:0] ACMP_GET_TX_CONNECTION_COMMAND_C = 4'd12;
  localparam [3:0] ACMP_GET_TX_CONNECTION_RESPONSE_C= 4'd13;

  // status (IEEE 1722.1-2021 Table 8-2)
  localparam [4:0] ACMP_STATUS_SUCCESS_C            = 5'd0;
  localparam [4:0] ACMP_STATUS_LISTENER_UNKNOWN_ID_C= 5'd1;
  localparam [4:0] ACMP_STATUS_TALKER_UNKNOWN_ID_C  = 5'd2;
  //! Milan 5.5.4.1 step 3 / Table 5.42: PROBE_TX while no valid stream
  //! DMAC is available (4.3.3.1 condition 1: MAAP claim live + unconflicted)
  localparam [4:0] ACMP_STATUS_TALKER_DEST_MAC_FAILED_C = 5'd3;
  localparam [4:0] ACMP_STATUS_LSTN_TALKER_TIMEOUT_C= 5'd7;
  localparam [4:0] ACMP_STATUS_CTLR_NOT_AUTHORIZED_C= 5'd16;
  localparam [4:0] ACMP_STATUS_NOT_SUPPORTED_C      = 5'd31;

  // flags cleared in a talker state response (pipewire reference behaviour)
  localparam [15:0] ACMP_FLAG_FAST_CONNECT_C        = 16'h0002;
  localparam [15:0] ACMP_FLAG_STREAMING_WAIT_C      = 16'h0008;
  localparam [15:0] ACMP_FLAG_SRP_REG_FAILED_C      = 16'h0040;

  //! Talker SUCCESS-response flag-clear masks, one per Milan v1.2 5.5.4
  //! response table (response flags = echo AND-NOT mask). The pipewire
  //! module-avb reference INVERTED the probe law (cleared FAST_CONNECT/
  //! STREAMING_WAIT, kept REGISTERING_FAILED) and echoed the DISCONNECT
  //! flags - the spec tables win. Error rows keep the full echo (mask 0).
  //! PROBE_TX Table 5.43: FAST_CONNECT/STREAMING_WAIT echoed,
  //! REGISTERING_FAILED forced 0 (16'h0040).
  localparam [15:0] ACMP_FLAG_CLR_PROBE_C = ACMP_FLAG_SRP_REG_FAILED_C;
  //! DISCONNECT_TX Table 5.45: all three named flags 0 (16'h004A).
  localparam [15:0] ACMP_FLAG_CLR_DISC_C  = ACMP_FLAG_FAST_CONNECT_C |
                                            ACMP_FLAG_STREAMING_WAIT_C |
                                            ACMP_FLAG_SRP_REG_FAILED_C;
  //! GET_TX_STATE Table 5.47: clear all three, then the flag_set lane ORs
  //! REGISTERING_FAILED back in (1 iff registering a Listener Asking
  //! Failed attribute — KL_acmp_tlkr_ctx lstn_ask_fail_i, gh #56 A2).
  localparam [15:0] ACMP_FLAG_CLR_GTS_C   = ACMP_FLAG_CLR_DISC_C;

  // ------------------------------------------------------------------ //
  // Milan v1.2 listener SM (pipewire acmp-milan-v12.h/.c contract)       //
  // ------------------------------------------------------------------ //
  typedef enum logic [2:0] {
    LSM_UNBOUND_S        = 3'd0,
    LSM_PRB_W_AVAIL_S    = 3'd1,   //! bound, talker not ADP-visible
    LSM_PRB_W_DELAY_S    = 3'd2,   //! random 0..~1 s backoff before probing
    LSM_PRB_W_RESP_S     = 3'd3,   //! probe #1 outstanding (200 ms)
    LSM_PRB_W_RESP2_S    = 3'd4,   //! probe #2 outstanding (200 ms)
    LSM_PRB_W_RETRY_S    = 3'd5,   //! probing failed, 4 s back-off
    LSM_SETTLED_NO_RSV_S = 3'd6,   //! probed OK, SRP reservation not up
    LSM_SETTLED_RSV_OK_S = 3'd7    //! connected + reservation active
  } acmp_lsm_t;

  //! listener timer durations in ms (reference acmp-milan-v12.c:22-25;
  //! DELAY is randomized — RTL draws 0..1023 ms from an LFSR, the point
  //! is desynchronization, both conform)
  localparam [13:0] LSM_TMR_NO_RESP_MS_C = 14'd200;
  localparam [13:0] LSM_TMR_RETRY_MS_C   = 14'd4000;
  localparam [13:0] LSM_TMR_NO_TK_MS_C   = 14'd10000;
  //! ADP availability aging FLOOR for a zero-valid_time ADPDU (1722.1
  //! 6.2.2.5 makes the horizon per-talker: valid_time x 2 s, latched into
  //! the record as adp_vt — see the aging law in KL_acmp_lstn_ctx). A
  //! vt = 0 ADPDU must make the talker neither immortal nor instantly
  //! dead: the clamp grants two 2 s advertise periods to refresh.
  localparam [6:0]  LSM_ADP_AGE_MIN_S_C  = 7'd4;

  // ------------------------------------------------------------------ //
  // Listener BIND CONTEXT record (KL_acmp_lstn_ctx table entry).         //
  // One record per listener sink (listener_unique_id); the whole SM      //
  // state of a sink lives here so N sinks share one machine + one RAM.   //
  // An all-zero record is a valid UNBOUND context (post-reset init).     //
  // ------------------------------------------------------------------ //
  //! NOTE the two newest fields sit ABOVE state (the packed MSBs): every
  //! pre-existing field keeps its historical LSB offset, which is what the
  //! package-free consumers of the flattened record (milan_csr's literal
  //! ACMP_CTX_*_LO_C map, the persist/csr harness cbits() maps) key on.
  typedef struct packed {
    logic [15:0] seq;       //! sequence_id of the OUTSTANDING probe: latched
                            //! at launch, REUSED by the RESP2 resend
                            //! (5.5.3.5.16 "duplicate"), matched against the
                            //! PROBE_TX_RESPONSE (5.5.3.5.18 step 1)
    logic [4:0]  adp_vt;    //! bound talker's ADPDU valid_time (2 s units);
                            //! aging horizon = adp_vt x 2 s (1722.1 6.2.2.5)
    acmp_lsm_t   state;     //! Milan 5.5.3 binding-SM state
    logic        active;    //! sink open (drives lstn_declare/stream_active)
    logic        tk_avail;  //! bound talker ADP-visible
    logic [1:0]  probing;   //! 0 dis / 1 passive / 2 active / 3 done
    logic [4:0]  status;    //! last probe status / timeout
    logic [6:0]  adp_age;   //! seconds since the talker's last ADPDU
    logic [13:0] tmr;       //! shared-wheel countdown, ms; 0 = disarmed
    logic [15:0] tuid;      //! bound talker_unique_id
    logic [15:0] flags;     //! stored binding flags (STREAMING_WAIT etc.)
    logic [11:0] vlan;      //! stream_vlan_id from the probe response
    logic [47:0] dmac;      //! stream_dest_mac (probe response / bind cmd)
    logic [63:0] sid;       //! stream_id (policy: derived or explicit)
    logic [63:0] talker;    //! bound talker_entity_id
    logic [63:0] ctlr;      //! binding controller_entity_id
  } acmp_lstn_ctx_t;

  localparam int ACMP_LSTN_CTX_W_C = $bits(acmp_lstn_ctx_t);   //! 338

endpackage

`default_nettype wire
