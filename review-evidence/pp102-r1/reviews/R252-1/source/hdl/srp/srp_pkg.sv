/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : srp_pkg.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/10 §3)
//
//  Description : Shared SRP MRPDU constants — the F10.8 attribute-type and
//                FirstValue-length table, the three-packed attribute-event
//                alphabet (802.1Q §35.2.2.7, encoded (((e1*6)+e2)*6)+e3),
//                the Listener four-packed declaration codes, the
//                VectorHeader LeaveAllEvent code (802.1Q §10.8.2.6), and
//                the class-A identity the 10 §3 vector-value-k rule keys on
//                (SRclassID 6 = SR class A, 802.1Q Table 35-7).
//
//                The one decision that matters: the F10.8 FirstValue
//                lengths are the framing truth for vector walking — the
//                on-wire AttributeLength is VALIDATED against them, and a
//                mismatch is a malformed vector attribute (tolerance
//                discard, Milan §4.2.7.1.2), never a resync hint. The MSRP
//                AttributeListLength is likewise only ever counted; the
//                dual EndMark frames the PDU.
//---------------------------------------------------------------------------//
`default_nettype none

package srp_pkg;

  // ---- MSRP attribute types (802.1Q §35.2.2.4, F10.8) --------------------
  localparam logic [7:0] SRP_MSRP_ATTR_TALKER_ADV_C    = 8'd1;
  localparam logic [7:0] SRP_MSRP_ATTR_TALKER_FAILED_C = 8'd2;
  localparam logic [7:0] SRP_MSRP_ATTR_LISTENER_C      = 8'd3;
  localparam logic [7:0] SRP_MSRP_ATTR_DOMAIN_C        = 8'd4;

  // ---- MVRP attribute types (802.1Q §11.2.3.1.6, F10.8) ------------------
  localparam logic [7:0] SRP_MVRP_ATTR_VID_C           = 8'd1;

  // ---- FirstValue lengths in octets (F10.7 / F10.8) ----------------------
  localparam logic [7:0] SRP_FV_LEN_TALKER_ADV_C    = 8'd25;
  localparam logic [7:0] SRP_FV_LEN_TALKER_FAILED_C = 8'd34;  // + system_id 8 + failure_code 1
  localparam logic [7:0] SRP_FV_LEN_LISTENER_C      = 8'd8;
  localparam logic [7:0] SRP_FV_LEN_DOMAIN_C        = 8'd4;
  localparam logic [7:0] SRP_FV_LEN_VID_C           = 8'd2;

  // ---- three-packed attribute events (10 §3: 0 New .. 5 Lv) --------------
  typedef enum logic [2:0] {
    SRP_EV_NEW    = 3'd0,
    SRP_EV_JOININ = 3'd1,
    SRP_EV_IN     = 3'd2,
    SRP_EV_JOINMT = 3'd3,
    SRP_EV_MT     = 3'd4,
    SRP_EV_LV     = 3'd5
  } srp_event_e;

  // ---- Listener four-packed declaration codes (F10.8 row 3) --------------
  typedef enum logic [1:0] {
    SRP_DECL_IGNORE        = 2'd0,
    SRP_DECL_ASKING_FAILED = 2'd1,
    SRP_DECL_READY         = 2'd2,
    SRP_DECL_READY_FAILED  = 2'd3
  } srp_decl_e;

  // ---- Domain identity (Milan §4.2.7: only SR class A exists) ------------
  localparam logic [7:0] SRP_CLASS_A_ID_C  = 8'd6;

  // ---- VectorHeader LeaveAllEvent code (802.1Q §10.8.2.6) ----------------
  localparam logic [2:0] SRP_LEAVEALL_EV_C = 3'd1;

  //! three-packed digit extract — idx 0 = first value (b / 36),
  //! idx 1 = (b / 6) % 6, idx 2 = b % 6. A digit > 5 (reachable only at
  //! idx 0, for b > 215) is outside the event alphabet and is the
  //! malformed-vector signal the decoder's tolerance path keys on.
  function automatic logic [2:0] srp_tp_digit(
      input logic [7:0] b,
      input logic [1:0] idx
  );
    logic [7:0] q;
    unique case (idx)
      2'd0:    q = b / 8'd36;
      2'd1:    q = (b / 8'd6) % 8'd6;
      default: q = b % 8'd6;
    endcase
    return q[2:0];
  endfunction

endpackage : srp_pkg
`default_nettype wire
