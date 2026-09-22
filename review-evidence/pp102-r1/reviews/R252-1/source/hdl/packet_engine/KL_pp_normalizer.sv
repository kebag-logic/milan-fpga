/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_normalizer.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/03 §4 normalized transaction + F03.3
//                 ALLOC->DECODED arc, 03 §5 the four producers, 08 §4 budgets)
//
//  Description : Transaction normalizer — ONE record shape for all work
//                items, regardless of origin (03 §4). The RX producer is the
//                validator's parsed-header beat: the normalizer stamps
//                origin = RX, arrival_ts = now_ms_i (deadline base = end of
//                reception), deadline = arrival + per-protocol class budget
//                (08 §4: T-BUDGET-ACMP-RESP / T-BUDGET-AECP-WC per 03 §6
//                rule (e); ADP budget = the integrator's delay-window bound),
//                tx_slot = PP_SLOT_NULL_C, and the 03 §8 response
//                disposition (ADP/ACMP -> 91-E0-F0-01-00-00 multicast, AECP
//                -> unicast). hazard_class/hazard_key come back over the
//                dispatch-ROM seam: hz_protocol_o/hz_opcode_o present the
//                query combinationally with the beat, hz_class_i/hz_key_i
//                answer in the same cycle (the ROM itself lands in P4,
//                06 §8 — here it stays a port).
//
//                The TIMER / SELF / MGMT producers of 03 §5 inject
//                ALREADY-FORMED pp_txn_t records (their owners stamp every
//                field, including deadline) and pass through bit-exact.
//                Fixed producer priority in the 03 §5 listed order:
//                RX > TIMER > SELF > MGMT. Producers are never dropped —
//                a full downstream queue backpressures through txn_ready_i
//                and the per-producer ready outputs (F03.3 has no drop arc
//                after the RX-slot gate; 03 §6 (e): never a silent drop).
//
//                The one design decision that matters: the normalizer is a
//                single 1-deep output register behind a purely combinational
//                assemble+arbitrate stage — ready_o is an ACCEPT strobe
//                (qualified by the producer's valid), so exactly one
//                producer wins per cycle and a record is never duplicated
//                or reordered on a stall. Deadline arithmetic is mod-2^32
//                ms by construction: consumers compare signed differences,
//                so arrival 0xFFFF_FFF0 + 0x20 = 0x10 is correct, not a bug.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_normalizer
  import pp_pkg::*;
(
    input  wire                    clk_i,               //! core clock (P-CLK-HZ domain)
    input  wire                    rst_n,               //! synchronous active-low reset

    //! ---- timebase + class budgets (08 §4) ----
    input  wire  [31:0]            now_ms_i,            //! absolute ms (KL_pp_timer_service now_ms_o)
    input  wire  [15:0]            budget_adp_ms_i,     //! ADP class budget in ms (delay-window bound)
    input  wire  [15:0]            budget_acmp_ms_i,    //! ACMP class budget in ms (T-BUDGET-ACMP-RESP)
    input  wire  [15:0]            budget_aecp_ms_i,    //! AEM/MVU/AA class budget in ms (T-BUDGET-AECP-WC)

    //! ---- RX producer: the validator's parsed-header beat (F03.2 extract) ----
    input  wire                    rx_valid_i,          //! parsed beat presented (held until accepted)
    output logic                   rx_ready_o,          //! accept strobe (this cycle the beat is taken)
    input  wire  [1:0]             rx_if_index_i,       //! ingress interface index
    input  wire  [2:0]             rx_protocol_i,       //! pp_protocol_e code from subtype/msg_type
    input  wire  [3:0]             rx_msg_type_i,       //! header message_type
    input  wire  [4:0]             rx_status_i,         //! header status / valid_time
    input  wire  [10:0]            rx_cdl_i,            //! validated control_data_length (V1/V2)
    input  wire  [47:0]            rx_src_mac_i,        //! frame SA (response addressing)
    input  wire  [63:0]            rx_controller_eid_i, //! controller_entity_id as applicable
    input  wire  [63:0]            rx_target_eid_i,     //! target/entity/stream id as applicable
    input  wire  [15:0]            rx_sequence_id_i,    //! echoed in responses
    input  wire                    rx_u_i,              //! AECP header u bit
    input  wire                    rx_cr_i,             //! AECP header cr bit
    input  wire  [15:0]            rx_opcode_i,         //! AEM/MVU command_type, ACMP/ADP msg_type
    input  wire  [63:0]            rx_operands_i,       //! packed pp_operands_t quartet
    input  wire  [2:0]             rx_slot_i,           //! RX payload slot handle (KL_pp_rx_slots)

    //! ---- dispatch-ROM seam (06 §8; the ROM lands in P4) ----
    output logic                   hz_valid_o,          //! query lines valid (mirrors rx_valid_i)
    output logic [2:0]             hz_protocol_o,       //! query: protocol of the beat
    output logic [15:0]            hz_opcode_o,         //! query: opcode of the beat
    input  wire  [3:0]             hz_class_i,          //! answer: hazard class (03 §6, same cycle)
    input  wire  [15:0]            hz_key_i,            //! answer: serialization key (same cycle)

    //! ---- TIMER producer (03 §5 #2): already-formed record ----
    input  wire                    tmr_valid_i,         //! record presented (held until accepted)
    input  wire  [PP_TXN_W_C-1:0]  tmr_txn_i,           //! formed pp_txn_t, passes bit-exact
    output logic                   tmr_ready_o,         //! accept strobe

    //! ---- SELF producer (03 §5 #3, the originator): already-formed record ----
    input  wire                    self_valid_i,        //! record presented (held until accepted)
    input  wire  [PP_TXN_W_C-1:0]  self_txn_i,          //! formed pp_txn_t, passes bit-exact
    output logic                   self_ready_o,        //! accept strobe

    //! ---- MGMT producer (03 §5 #4, the side port): already-formed record ----
    input  wire                    mgmt_valid_i,        //! record presented (held until accepted)
    input  wire  [PP_TXN_W_C-1:0]  mgmt_txn_i,          //! formed pp_txn_t, passes bit-exact
    output logic                   mgmt_ready_o,        //! accept strobe

    //! ---- normalized stream to KL_pp_dispatch ----
    output logic                   txn_valid_o,         //! record valid (held through a stall)
    output logic [PP_TXN_W_C-1:0]  txn_o,               //! the 03 §4 record
    input  wire                    txn_ready_i          //! dispatch consumes the record this cycle
);

  // -------------------------------------------------- RX record assembly
  pp_protocol_e proto_w;
  logic [15:0]  budget_sel_w;
  pp_txn_t      rx_txn_w;

  assign proto_w = pp_protocol_e'(rx_protocol_i);

  always_comb begin : budget_sel
    case (proto_w)
      PP_PROTO_ADP:  budget_sel_w = budget_adp_ms_i;
      PP_PROTO_ACMP: budget_sel_w = budget_acmp_ms_i;
      default:       budget_sel_w = budget_aecp_ms_i;  // AEM / MVU / AA
    endcase
  end

  always_comb begin : rx_assemble
    rx_txn_w.origin          = PP_ORIGIN_RX;
    rx_txn_w.interface_index = rx_if_index_i;
    rx_txn_w.arrival_ts      = now_ms_i;
    rx_txn_w.protocol        = proto_w;
    rx_txn_w.msg_type        = rx_msg_type_i;
    rx_txn_w.status_in       = rx_status_i;
    rx_txn_w.cdl             = rx_cdl_i;
    rx_txn_w.src_mac         = rx_src_mac_i;
    rx_txn_w.controller_eid  = rx_controller_eid_i;
    rx_txn_w.target_eid      = rx_target_eid_i;
    rx_txn_w.sequence_id     = rx_sequence_id_i;
    rx_txn_w.u_flag          = rx_u_i;
    rx_txn_w.cr              = rx_cr_i;
    rx_txn_w.opcode          = rx_opcode_i;
    rx_txn_w.operands        = pp_operands_t'(rx_operands_i);
    rx_txn_w.rx_slot         = rx_slot_i;
    rx_txn_w.hazard_class    = pp_hazard_e'(hz_class_i);
    rx_txn_w.hazard_key      = hz_key_i;
    rx_txn_w.tx_slot         = PP_SLOT_NULL_C;          // allocated at response build
    rx_txn_w.deadline        = now_ms_i + {16'h0, budget_sel_w};  // mod-2^32 ms
    // 03 §8 destination addressing: ADP and ACMP responses both multicast
    // 91-E0-F0-01-00-00 (one disposition code); AECP unicasts to src_mac
    rx_txn_w.resp_disposition =
        ((proto_w == PP_PROTO_ADP) || (proto_w == PP_PROTO_ACMP))
        ? PP_RESP_ACMP_MCAST : PP_RESP_UNICAST;
  end

  // the dispatch-ROM seam mirrors the presented beat, answers same-cycle
  assign hz_valid_o    = rx_valid_i;
  assign hz_protocol_o = rx_protocol_i;
  assign hz_opcode_o   = rx_opcode_i;

  // ------------------------------------- fixed-priority producer arbiter
  // 03 §5 listed order: RX (1) > TIMER (2) > SELF (3) > MGMT (4)
  logic    sel_valid_w;
  pp_txn_t sel_txn_w;

  always_comb begin : producer_pick
    sel_valid_w = 1'b1;
    if (rx_valid_i)        sel_txn_w = rx_txn_w;
    else if (tmr_valid_i)  sel_txn_w = pp_txn_t'(tmr_txn_i);
    else if (self_valid_i) sel_txn_w = pp_txn_t'(self_txn_i);
    else if (mgmt_valid_i) sel_txn_w = pp_txn_t'(mgmt_txn_i);
    else begin
      sel_valid_w = 1'b0;
      sel_txn_w   = pp_txn_t'({PP_TXN_W_C{1'b0}});
    end
  end

  // -------------------------------------------------- 1-deep output stage
  pp_txn_t txn_r;
  logic    txn_valid_r;
  logic    can_load_w;
  logic    accept_w;

  assign can_load_w = !txn_valid_r || txn_ready_i;
  assign accept_w   = sel_valid_w && can_load_w;

  // accept strobes — exactly one producer wins per cycle (backpressure,
  // never a drop: an unselected or stalled producer simply holds its valid)
  assign rx_ready_o   = can_load_w && rx_valid_i;
  assign tmr_ready_o  = can_load_w && !rx_valid_i && tmr_valid_i;
  assign self_ready_o = can_load_w && !rx_valid_i && !tmr_valid_i
                        && self_valid_i;
  assign mgmt_ready_o = can_load_w && !rx_valid_i && !tmr_valid_i
                        && !self_valid_i && mgmt_valid_i;

  always_ff @(posedge clk_i) begin : out_stage
    if (!rst_n) begin
      txn_valid_r <= 1'b0;
      txn_r       <= pp_txn_t'({PP_TXN_W_C{1'b0}});
    end else begin
      if (accept_w) begin
        txn_r       <= sel_txn_w;
        txn_valid_r <= 1'b1;
      end else if (txn_valid_r && txn_ready_i) begin
        txn_valid_r <= 1'b0;
      end
    end
  end

  assign txn_valid_o = txn_valid_r;
  assign txn_o       = txn_r;

endmodule : KL_pp_normalizer
`default_nettype wire
