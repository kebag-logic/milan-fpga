/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_adp_engine.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/04 in
//                full: §3 PDU/F04.5/F04.6, §5 state, §6.1 advertise SM
//                F04.2, §6.2 talker-discovery SM F04.3, §8/08 §2 timing)
//
//  Description : The ADP engine — pure hardwired FSMs, no microcode:
//                  * one Milan §5.6.3 advertise SM per AVB interface
//                    (DOWN/DELAY/WAITING; ENTITY_DEPARTING only on
//                    entity-disable, never on link-down; GM_CHANGE
//                    re-advertises through DELAY; held in DOWN until
//                    entity_enable_i — Milan §5.6.1 boot gate);
//                  * the available_index manager of 04 §5;
//                  * the 82-byte wire-frame ADPDU builder (14 B Ethernet
//                    header + 68 B ADPDU, cdl 56, entity_id at wire byte
//                    18 per F04.5) writing a KL_pp_tx_slots slot;
//                  * one Milan §5.6.4 talker-discovery SM per Stream
//                    Input, fed by registered remote ENTITY_AVAILABLE /
//                    DEPARTING observations from dispatch, emitting
//                    EVT_TK_DISCOVERED / EVT_TK_DEPARTED class-C strobes
//                    to the ACMP listener SMs.
//
//                The delay draws use KL_pp_prng's draw port with TWO
//                DISTINCT kinds: kind 1 = T-ADP-DELAY-START (0..2 s,
//                enable-with-link-up entry only) and kind 2 = T-ADP-DELAY
//                (0..4 s, every later DELAY entry) — review §8 item 5
//                calls a merged draw a hiding conformance defect.
//
//                The one decision that matters: available_index follows
//                the DOC rule (04 §5 / IEEE §6.2.2.15) — 0 at power-up,
//                incremented AFTER each transmitted ENTITY_AVAILABLE,
//                reset to 0 after ENTITY_DEPARTING (whose wire field
//                carries the pre-reset value, per the F04.2 action order
//                "send ENTITY_DEPARTING, available_index = 0"). This
//                DIVERGES from the reference platform's adp_advertiser,
//                which increments on EVERY transmitted ADPDU; the doc rule
//                is subject to live-controller adjudication (Hive /
//                la_avdecc) before cutover.
//
//                The discovery SM builds the full Milan §5.6.4.5.1 gm/
//                domain guard: an ENTITY_AVAILABLE is matched only when
//                its gptp_grandmaster_id AND gptp_domain_number equal the
//                ingress port's class-D values. On a conformant Milan net
//                this guard NEVER fires: Milan §2 pins 802.1AS-2011
//                domain 0, so both peers report domain 0 and, once
//                converged, the same grandmaster — a mismatch exists only
//                mid-GM-handover or across a misplumbed boundary; it is
//                built because §5.6.4.5.1 is a shall and the handover
//                window is real.
//
//                Storage: the per-sink saved {interface_index,
//                available_index} record (04 §5 / F07.6 fields) is a
//                1W1R sync-read RAM, iterated one sink per step — never a
//                flop mirror behind a wide mux.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_adp_engine
  import pp_pkg::*;
  import pp_adp_pkg::*;
#(
    //! P-N-AVB-INTERFACES (F01.5 default 1) — advertise SM instances
    parameter int unsigned N_IF_P = 1,
    //! P-N-STREAM-IN (F01.5 default 8) — talker-discovery SM instances
    parameter int unsigned N_SINK_P = 8,
    //! timer-service slot of interface 0's shared advertise/delay timer
    //! (08 §5 F08.4: slots [ADV_BASE .. ADV_BASE+IF-1])
    parameter int unsigned TMR_SLOT_ADV_BASE_P = 0,
    //! timer-service slot of sink 0's T-ADP-NOADP (08 §5: the SI block)
    parameter int unsigned TMR_SLOT_NOADP_BASE_P = TMR_SLOT_ADV_BASE_P + N_IF_P,
    //! KL_pp_rx_slots geometry — must match the instantiated pool
    parameter int unsigned RX_SLOTS_P = 4,
    parameter int unsigned RX_BYTES_P = 576,
    //! KL_pp_tx_slots geometry — must match the instantiated pool
    parameter int unsigned TX_STD_SLOTS_P = 4,
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600,
    //! P-TIMER-SLOTS of the attached KL_pp_timer_service (index width only).
    //! Parameterized, not read from pp_pkg: the F08.4 slot map is derived
    //! from the SHAPE (08 §5), so a top elaborated at more than the F01.5
    //! default streams sizes a larger timer and this width must follow it.
    parameter int unsigned TMR_SLOTS_P = pp_pkg::PP_TIMER_SLOTS_C,
    //! derived widths — do not override
    localparam int unsigned IF_W_C  = (N_IF_P > 1) ? $clog2(N_IF_P) : 1,
    localparam int unsigned SNK_W_C = (N_SINK_P > 1) ? $clog2(N_SINK_P) : 1,
    localparam int unsigned TMR_AW_C = (TMR_SLOTS_P > 32'd1)
                                       ? $clog2(TMR_SLOTS_P) : 32'd1,
    localparam int unsigned RXS_SLOT_W_C = (RX_SLOTS_P > 1) ? $clog2(RX_SLOTS_P) : 1,
    localparam int unsigned RXS_ADDR_W_C = $clog2(RX_BYTES_P),
    localparam int unsigned TXS_SLOT_W_C = $clog2(TX_STD_SLOTS_P + 1),
    localparam int unsigned TXS_LEN_W_C  = $clog2(TX_OVERSIZE_BYTES_P + 1)
) (
    input  wire                        clk_i,              //! core clock (P-CLK-HZ)
    input  wire                        rst_n,              //! synchronous active-low reset

    // ---- level controls + class-C events in (02 §5/§6) --------------------
    input  wire                        entity_enable_i,    //! Milan §5.6.1 boot gate (level); falling edge = SHUTDOWN
    input  wire  [N_IF_P-1:0]          link_up_i,          //! per-interface link status (level, 2FF-synced upstream)
    input  wire  [N_IF_P-1:0]          gm_change_i,        //! per-interface GM_CHANGE strobe (event router face)

    // ---- class-D status dictionary (F02.10) -------------------------------
    input  wire  [N_IF_P*64-1:0]       gm_id_i,            //! gm_id[if] — sampled at PDU build + discovery guard
    input  wire  [N_IF_P*8-1:0]        gptp_domain_i,      //! gptp_domain[if] — idem

    // ---- identity/model registers (04 §3 field-sourcing table) ------------
    input  wire  [63:0]                entity_id_i,        //! own entity_id (config/ID register)
    input  wire  [63:0]                entity_model_id_i,  //! entity_model_id (=/= 0, =/= all-1s)
    input  wire  [47:0]                own_mac_i,          //! source MAC of the built wire frame
    input  wire  [15:0]                talker_sources_i,   //! talker_stream_sources (max across configs)
    input  wire  [15:0]                talker_caps_i,      //! talker_capabilities (review §8 item 6)
    input  wire  [15:0]                listener_sinks_i,   //! listener_stream_sinks (max across configs)
    input  wire  [15:0]                listener_caps_i,    //! listener_capabilities (review §8 item 6)
    input  wire  [15:0]                current_cfg_i,      //! current_configuration_index (dynamic overlay)
    input  wire  [15:0]                identify_index_i,   //! identify_control_index (model metadata)

    // ---- dispatch-in (KL_pp_dispatch ADP pop face) ------------------------
    input  wire                        txn_valid_i,        //! head record valid
    input  wire  [PP_TXN_W_C-1:0]      txn_i,              //! pp_txn_t record (protocol = ADP)
    output logic                       txn_ready_o,        //! engine consumes the head record

    // ---- RX slot pool read/free (KL_pp_rx_slots read side) ----------------
    output logic [RXS_SLOT_W_C-1:0]    rxs_rd_slot_o,      //! payload slot handle being read
    output logic [RXS_ADDR_W_C-1:0]    rxs_rd_addr_o,      //! PDU byte address within the slot
    output logic                       rxs_rd_en_o,        //! sync-read enable (data next cycle)
    input  wire  [7:0]                 rxs_rd_data_i,      //! slot byte, one cycle after rd_en
    output logic                       rxs_free_o,         //! return the consumed slot
    output logic [RXS_SLOT_W_C-1:0]    rxs_free_slot_o,    //! which slot to return

    // ---- PRNG draw port (KL_pp_prng, exact) -------------------------------
    output logic                       prng_draw_req_o,    //! one-cycle draw request
    output logic [2:0]                 prng_draw_kind_o,   //! kind 1 = DELAY-START, kind 2 = DELAY
    input  wire                        prng_draw_busy_i,   //! draw in progress
    input  wire                        prng_draw_valid_i,  //! one-cycle: draw_ms_i holds the result
    input  wire  [15:0]                prng_draw_ms_i,     //! drawn delay in ms

    // ---- timer service (KL_pp_timer_service arm/expiry faces) -------------
    input  wire  [31:0]                now_ms_i,           //! absolute ms timebase (now_ms_o)
    output logic                       tmr_arm_valid_o,    //! arm/cancel strobe
    output logic                       tmr_arm_cancel_o,   //! 1 = cancel the slot
    output logic [TMR_AW_C-1:0]        tmr_arm_slot_o,     //! deadline slot index
    output logic [PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_o, //! owner tag (= slot index)
    output logic [31:0]                tmr_arm_deadline_ms_o, //! absolute ms deadline
    input  wire                        tmr_exp_valid_i,    //! expiry event
    input  wire  [TMR_AW_C-1:0]        tmr_exp_slot_i,     //! expired slot
    input  wire  [PP_TIMER_OWNER_W_C-1:0] tmr_exp_owner_i, //! owner tag (unused: slot decodes)

    // ---- TX slot pool (KL_pp_tx_slots alloc/write/commit faces) -----------
    output logic                       txs_alloc_req_o,    //! one-cycle slot request
    output logic                       txs_oversize_o,     //! ADP never needs the oversize slot (tied 0)
    input  wire                        txs_alloc_gnt_i,    //! one-cycle grant, cycle after the request
    input  wire  [TXS_SLOT_W_C-1:0]    txs_alloc_slot_i,   //! granted slot index
    output logic [TXS_SLOT_W_C-1:0]    txs_wr_slot_o,      //! slot being written / committed
    output logic [TXS_LEN_W_C-1:0]     txs_wr_addr_o,      //! byte offset within the slot
    output logic                       txs_wr_valid_o,     //! byte-write strobe
    output logic [7:0]                 txs_wr_data_o,      //! frame byte
    output logic                       txs_wr_commit_o,    //! mark ready-to-send
    output logic [TXS_LEN_W_C-1:0]     txs_wr_len_o,       //! committed length (82)

    // ---- TX request face (TX arbiter not landed: plain port) --------------
    output logic                       txreq_valid_o,      //! one-cycle: committed slot queued for TX
    output logic [TXS_SLOT_W_C-1:0]    txreq_slot_o,       //! committed tx-slot handle
    output logic [IF_W_C-1:0]          txreq_if_o,         //! egress AVB interface

    // ---- ACMP binding view (07 §4 sink records; plain face) ---------------
    input  wire  [N_SINK_P-1:0]        bound_i,            //! sink is bound (discovery SM armed)
    input  wire  [N_SINK_P*64-1:0]     bound_talker_eid_i, //! bound talker entity_id per sink

    // ---- class-C events out (ACMP listener SMs; plain port) ---------------
    output logic                       evt_valid_o,        //! one-cycle event strobe
    output logic                       evt_departed_o,     //! 1 = EVT_TK_DEPARTED, 0 = EVT_TK_DISCOVERED
    output logic [SNK_W_C-1:0]         evt_sink_o,         //! sink index payload

    // ---- GPTP_GM_CHANGED counter ticks (04 §2) ----------------------------
    output logic [N_IF_P-1:0]          gm_changed_tick_o,  //! per-interface counter tick

    // ---- observability ----------------------------------------------------
    output logic [N_IF_P*2-1:0]        dbg_adv_state_o,    //! advertise SM state per interface
    output logic [N_IF_P*32-1:0]       dbg_avail_index_o,  //! available_index manager per interface
    output logic [N_SINK_P-1:0]        dbg_tk_discovered_o //! discovery SM state per sink
);

  // ------------------------------------------------------------ txn unpack
  pp_txn_t txn_in_w;
  assign txn_in_w = pp_txn_t'(txn_i);

  // --------------------------------------------------------- slice helpers
  //! MSB-first byte n of a 64/48/32/16-bit field (n = 0 is the wire-first byte)
  function automatic logic [7:0] byte64_f(input logic [63:0] v, input int unsigned n);
    logic [63:0] sh;
    sh = v >> (8 * (7 - n));
    return sh[7:0];
  endfunction

  function automatic logic [7:0] byte48_f(input logic [47:0] v, input int unsigned n);
    logic [47:0] sh;
    sh = v >> (8 * (5 - n));
    return sh[7:0];
  endfunction

  function automatic logic [7:0] byte32_f(input logic [31:0] v, input int unsigned n);
    logic [31:0] sh;
    sh = v >> (8 * (3 - n));
    return sh[7:0];
  endfunction

  function automatic logic [7:0] byte16_f(input logic [15:0] v, input int unsigned n);
    logic [15:0] sh;
    sh = v >> (8 * (1 - n));
    return sh[7:0];
  endfunction

  //! clamped per-interface class-D slices
  function automatic logic [63:0] gm_slice_f(input logic [IF_W_C-1:0] ifx);
    int unsigned i;
    i = (32'(ifx) < N_IF_P) ? 32'(ifx) : 32'd0;
    return gm_id_i[64*i +: 64];
  endfunction

  function automatic logic [7:0] dom_slice_f(input logic [IF_W_C-1:0] ifx);
    int unsigned i;
    i = (32'(ifx) < N_IF_P) ? 32'(ifx) : 32'd0;
    return gptp_domain_i[8*i +: 8];
  endfunction

  // ------------------------------------------------------ edge synchronizers
  logic [N_IF_P-1:0]   link_q_r;
  logic                enable_q_r;
  logic [N_SINK_P-1:0] bound_q_r;
  logic [N_IF_P-1:0]   gm_tick_r;

  logic [N_IF_P-1:0]   link_fall_w;
  logic [N_IF_P-1:0]   link_rise_w;
  logic                enable_rise_w;
  logic                enable_fall_w;
  logic [N_SINK_P-1:0] bound_fall_w;

  assign link_fall_w   = link_q_r & ~link_up_i;
  assign link_rise_w   = ~link_q_r & link_up_i;
  assign enable_rise_w = entity_enable_i && !enable_q_r;
  assign enable_fall_w = !entity_enable_i && enable_q_r;
  assign bound_fall_w  = bound_q_r & ~bound_i;

  always_ff @(posedge clk_i) begin : edge_sync
    if (!rst_n) begin
      link_q_r   <= '0;
      enable_q_r <= 1'b0;
      bound_q_r  <= '0;
      gm_tick_r  <= '0;
    end else begin
      link_q_r   <= link_up_i;
      enable_q_r <= entity_enable_i;
      bound_q_r  <= bound_i;
      gm_tick_r  <= gm_change_i;   // GPTP_GM_CHANGED ticks on every GM_CHANGE
    end
  end

  assign gm_changed_tick_o = gm_tick_r;

  // ============================================================ RX pipeline
  // One transaction at a time: classify, fetch the payload fields the
  // record does not carry (available_index @36, gm @40, domain @48,
  // interface_index @54 — PDU offsets; the RX pool stores the validated
  // PDU from the subtype byte, its 536-byte minimum = max command PDU),
  // then step every matched discovery SM, then free the slot.
  typedef enum logic [3:0] {
    RX_IDLE     = 4'd0,
    RX_CLASSIFY = 4'd1,
    RX_READ     = 4'd2,
    RX_SINK_RD  = 4'd3,
    RX_SINK_EX  = 4'd4,
    RX_SINK_EV2 = 4'd5,
    RX_NEXT     = 4'd6,
    RX_FREE     = 4'd7
  } rx_st_e;

  localparam int unsigned PDU_FLD_FIRST_C = 36;  // available_index MSB
  localparam int unsigned PDU_FLD_LAST_C  = 55;  // interface_index LSB

  rx_st_e            rx_st_r;
  logic [3:0]        rxq_msg_r;       // ADP message_type
  logic [63:0]       rxq_eid_r;       // remote entity_id (header @4)
  logic [4:0]        rxq_vt_r;        // remote valid_time (status lane)
  logic [IF_W_C-1:0] rxq_if_r;        // ingress interface
  logic [2:0]        rxq_slot_r;      // RX slot handle (PP_SLOT_NULL_C = none)
  logic [5:0]        rd_ptr_r;        // slot byte address being issued
  logic              cap_vld_r;       // a read is landing this cycle
  logic [5:0]        cap_idx_r;       // its byte address
  logic [31:0]       rx_aidx_r;       // remote available_index
  logic [63:0]       rx_gm_r;         // remote gptp_grandmaster_id
  logic [7:0]        rx_dom_r;        // remote gptp_domain_number
  logic [15:0]       rx_ifx_r;        // remote interface_index
  logic [SNK_W_C-1:0] sink_r;         // discovery iteration cursor

  logic rx_have_slot_w;
  assign rx_have_slot_w = (rxq_slot_r != PP_SLOT_NULL_C)
                          && (32'(rxq_slot_r) < RX_SLOTS_P);

  // sink match vector: the F04.1 compare array over sink bindings
  logic [N_SINK_P-1:0] match_w;
  always_comb begin : sink_match
    for (int unsigned s = 0; s < N_SINK_P; s++) begin
      match_w[s] = bound_i[s] && (bound_talker_eid_i[64*s +: 64] == rxq_eid_r);
    end
  end

  // ---------------------------------------------- discovery SM evaluation
  // Per-sink saved record {interface_index[15:0], available_index[31:0]}:
  // 1W1R sync-read RAM (04 §5 sink-record fields), read in RX_SINK_RD,
  // written in RX_SINK_EX. State bit per sink: 1 = TK_DISCOVERED.
  logic [47:0] disc_rec_r [0:N_SINK_P-1];
  logic [47:0] disc_rec_q_r;
  logic        rec_rd_en_w;
  logic        rec_wr_en_w;
  logic [47:0] rec_wr_data_w;

  logic [N_SINK_P-1:0] disc_st_r;

  logic [15:0] rec_ifx_w;
  logic [31:0] rec_aidx_w;
  assign {rec_ifx_w, rec_aidx_w} = disc_rec_q_r;

  logic gm_dom_ok_w;    // Milan §5.6.4.5.1 guard (never fires conformant, see banner)
  assign gm_dom_ok_w = (rx_gm_r == gm_slice_f(rxq_if_r))
                    && (rx_dom_r == dom_slice_f(rxq_if_r));

  // evaluation results (combinational, valid in RX_SINK_EX)
  logic ev_dep_w;       // fire EVT_TK_DEPARTED for sink_r
  logic ev_disc_w;      // fire EVT_TK_DISCOVERED for sink_r
  logic st_set_w;       // disc_st_r[sink_r] <= 1
  logic st_clr_w;       // disc_st_r[sink_r] <= 0
  logic iter_arm_w;     // arm T-ADP-NOADP for sink_r
  logic iter_cancel_w;  // cancel T-ADP-NOADP for sink_r

  always_comb begin : disc_eval
    ev_dep_w      = 1'b0;
    ev_disc_w     = 1'b0;
    st_set_w      = 1'b0;
    st_clr_w      = 1'b0;
    iter_arm_w    = 1'b0;
    iter_cancel_w = 1'b0;
    rec_wr_en_w   = 1'b0;
    rec_wr_data_w = {rx_ifx_r, rx_aidx_r};
    if (rx_st_r == RX_SINK_EX) begin
      if (rxq_msg_r == ADP_MSG_AVAILABLE_C) begin
        if (!disc_st_r[sink_r]) begin
          // TK_NOT_DISCOVERED: accept only on gm+domain match (F04.3)
          if (gm_dom_ok_w) begin
            ev_disc_w   = 1'b1;
            st_set_w    = 1'b1;
            rec_wr_en_w = 1'b1;
            iter_arm_w  = 1'b1;
          end
        end else if (rx_ifx_r == rec_ifx_w) begin
          // TK_DISCOVERED: interface_index must equal the saved value
          if (rx_aidx_r > rec_aidx_w) begin
            rec_wr_en_w = 1'b1;               // fresh cycle: store + re-arm
            iter_arm_w  = 1'b1;
          end else if (gm_dom_ok_w) begin
            // talker-restart detector: departed + rediscovered pair
            ev_dep_w    = 1'b1;
            ev_disc_w   = 1'b1;
            rec_wr_en_w = 1'b1;
            iter_arm_w  = 1'b1;
          end else begin
            ev_dep_w      = 1'b1;             // stale index + foreign GM
            st_clr_w      = 1'b1;
            iter_cancel_w = 1'b1;
          end
        end
      end else if (rxq_msg_r == ADP_MSG_DEPARTING_C) begin
        if (disc_st_r[sink_r] && (rx_ifx_r == rec_ifx_w)) begin
          ev_dep_w      = 1'b1;
          st_clr_w      = 1'b1;
          iter_cancel_w = 1'b1;
        end
      end
    end
  end

  assign rec_rd_en_w = (rx_st_r == RX_SINK_RD);

  always_ff @(posedge clk_i) begin : disc_rec_ram
    if (rec_rd_en_w) begin
      disc_rec_q_r <= disc_rec_r[sink_r];
    end
    if (rec_wr_en_w) begin
      disc_rec_r[sink_r] <= rec_wr_data_w;
    end
  end

  // ---------------------------------------------- NOADP expiry + unbind
  logic        noadp_exp_w;
  logic [31:0] exp_slot_ext_w;
  logic [31:0] noadp_rel_w;       // wrap-safe: below-base wraps huge
  logic [SNK_W_C-1:0] noadp_exp_sink_w;

  assign exp_slot_ext_w = {{(32-TMR_AW_C){1'b0}}, tmr_exp_slot_i};
  assign noadp_rel_w    = exp_slot_ext_w - TMR_SLOT_NOADP_BASE_P;
  assign noadp_exp_w    = tmr_exp_valid_i && (noadp_rel_w < N_SINK_P);
  assign noadp_exp_sink_w = SNK_W_C'(noadp_rel_w);

  always_ff @(posedge clk_i) begin : disc_state
    if (!rst_n) begin
      disc_st_r <= '0;
    end else begin
      // NOADP aging: expiry in TK_DISCOVERED departs the talker (F04.3)
      if (noadp_exp_w) begin
        disc_st_r[noadp_exp_sink_w] <= 1'b0;
      end
      // unbind disarms the SM silently (active-while-bound, 04 §6.2)
      for (int unsigned s = 0; s < N_SINK_P; s++) begin
        if (bound_fall_w[s]) disc_st_r[s] <= 1'b0;
      end
      // iteration outcome wins any same-cycle collision
      if (st_set_w) disc_st_r[sink_r] <= 1'b1;
      if (st_clr_w) disc_st_r[sink_r] <= 1'b0;
    end
  end

  assign dbg_tk_discovered_o = disc_st_r;

  // ---------------------------------------------------------- RX pipe FSM
  // txn accepted marker (classify runs on registered fields)
  logic txn_in_valid_q_r;

  logic disc_hit_w;                   // ENTITY_DISCOVER accepted this cycle
  logic [IF_W_C-1:0] disc_hit_if_w;

  assign disc_hit_w = (rx_st_r == RX_CLASSIFY)
                      && (txn_in_valid_q_r)
                      && (rxq_msg_r == ADP_MSG_DISCOVER_C)
                      && ((rxq_eid_r == 64'd0) || (rxq_eid_r == entity_id_i));
  assign disc_hit_if_w = rxq_if_r;

  always_ff @(posedge clk_i) begin : rx_pipe
    if (!rst_n) begin
      rx_st_r          <= RX_IDLE;
      rxq_msg_r        <= 4'd0;
      rxq_eid_r        <= 64'd0;
      rxq_vt_r         <= 5'd0;
      rxq_if_r         <= '0;
      rxq_slot_r       <= PP_SLOT_NULL_C;
      rd_ptr_r         <= 6'd0;
      cap_vld_r        <= 1'b0;
      cap_idx_r        <= 6'd0;
      rx_aidx_r        <= 32'd0;
      rx_gm_r          <= 64'd0;
      rx_dom_r         <= 8'd0;
      rx_ifx_r         <= 16'd0;
      sink_r           <= '0;
      txn_in_valid_q_r <= 1'b0;
    end else begin
      cap_vld_r <= 1'b0;
      unique case (rx_st_r)
        RX_IDLE: begin
          if (txn_valid_i) begin
            rxq_msg_r        <= txn_in_w.msg_type;
            rxq_eid_r        <= txn_in_w.target_eid;
            rxq_vt_r         <= txn_in_w.status_in;
            rxq_if_r         <= IF_W_C'(txn_in_w.interface_index);
            rxq_slot_r       <= txn_in_w.rx_slot;
            txn_in_valid_q_r <= (txn_in_w.protocol == PP_PROTO_ADP);
            rx_st_r          <= RX_CLASSIFY;
          end
        end
        RX_CLASSIFY: begin
          if (txn_in_valid_q_r
              && ((rxq_msg_r == ADP_MSG_AVAILABLE_C)
                  || (rxq_msg_r == ADP_MSG_DEPARTING_C))
              && rx_have_slot_w) begin
            rd_ptr_r <= 6'(PDU_FLD_FIRST_C);
            rx_st_r  <= RX_READ;
          end else begin
            // DISCOVER is consumed by disc_hit_w; everything else drops
            rx_st_r <= RX_FREE;
          end
        end
        RX_READ: begin
          // issue one byte read per cycle; capture lands one cycle later
          cap_vld_r <= 1'b1;
          cap_idx_r <= rd_ptr_r;
          if (rd_ptr_r != 6'(PDU_FLD_LAST_C)) begin
            rd_ptr_r <= rd_ptr_r + 6'd1;
          end
          if (cap_vld_r) begin
            if (cap_idx_r <= 6'd39) begin
              rx_aidx_r <= {rx_aidx_r[23:0], rxs_rd_data_i};
            end else if (cap_idx_r <= 6'd47) begin
              rx_gm_r <= {rx_gm_r[55:0], rxs_rd_data_i};
            end else if (cap_idx_r == 6'd48) begin
              rx_dom_r <= rxs_rd_data_i;
            end else if (cap_idx_r >= 6'd54) begin
              rx_ifx_r <= {rx_ifx_r[7:0], rxs_rd_data_i};
            end
            if (cap_idx_r == 6'(PDU_FLD_LAST_C)) begin
              sink_r  <= '0;
              rx_st_r <= RX_SINK_RD;
            end
          end
        end
        RX_SINK_RD: begin
          // record read issued (rec_rd_en_w); skip unmatched sinks fast
          if (match_w[sink_r]) begin
            rx_st_r <= RX_SINK_EX;
          end else begin
            rx_st_r <= RX_NEXT;
          end
        end
        RX_SINK_EX: begin
          // disc_eval fires events/arms this cycle; pairs need one more
          if (ev_dep_w && ev_disc_w) begin
            rx_st_r <= RX_SINK_EV2;
          end else begin
            rx_st_r <= RX_NEXT;
          end
        end
        RX_SINK_EV2: begin
          rx_st_r <= RX_NEXT;
        end
        RX_NEXT: begin
          if (32'(sink_r) == N_SINK_P - 1) begin
            rx_st_r <= RX_FREE;
          end else begin
            sink_r  <= sink_r + SNK_W_C'(1);
            rx_st_r <= RX_SINK_RD;
          end
        end
        RX_FREE: begin
          rx_st_r <= RX_IDLE;
        end
        default: rx_st_r <= RX_IDLE;
      endcase
    end
  end

  assign txn_ready_o = (rx_st_r == RX_IDLE);

  assign rxs_rd_slot_o  = rxq_slot_r[RXS_SLOT_W_C-1:0];
  assign rxs_rd_addr_o  = RXS_ADDR_W_C'(rd_ptr_r);
  assign rxs_rd_en_o    = (rx_st_r == RX_READ);
  assign rxs_free_o     = (rx_st_r == RX_FREE) && rx_have_slot_w;
  assign rxs_free_slot_o = rxq_slot_r[RXS_SLOT_W_C-1:0];

  // ======================================================== advertise SMs
  // Per interface: F04.2 state, the startup-draw marker, the shared-slot
  // timer pending request (last-writer-wins), and the send-queue bits.
  typedef enum logic [1:0] {
    TPEND_NONE   = 2'd0,
    TPEND_ARM    = 2'd1,
    TPEND_CANCEL = 2'd2
  } tpend_e;

  adp_adv_st_e adv_st_r [N_IF_P];
  logic [N_IF_P-1:0] adv_startup_r;      // next draw uses kind 1 (DELAY-START)
  tpend_e            tpend_r [N_IF_P];
  logic [31:0]       tpend_deadline_r [N_IF_P];
  logic [N_IF_P-1:0] pend_avail_r;       // ENTITY_AVAILABLE queued to build
  logic [N_IF_P-1:0] pend_dep_r;         // ENTITY_DEPARTING queued to build

  // advertise shared-slot expiry decode (wrap-safe relative index)
  logic       adv_exp_w;
  logic [31:0] adv_rel_w;
  logic [IF_W_C-1:0] adv_exp_if_w;
  assign adv_rel_w    = exp_slot_ext_w - TMR_SLOT_ADV_BASE_P;
  assign adv_exp_w    = tmr_exp_valid_i && (adv_rel_w < N_IF_P);
  assign adv_exp_if_w = IF_W_C'(adv_rel_w);

  // draw delivery (from the PRNG serializer below)
  logic              draw_del_w;
  logic [IF_W_C-1:0] draw_del_if_w;
  logic [15:0]       draw_del_ms_w;

  // builder completion (from the builder below; B_REQ cycle)
  logic              bld_done_avail_w;
  logic              bld_done_dep_w;
  logic [IF_W_C-1:0] bld_done_if_w;

  // timer-port issue grant for the pending shared-slot request
  logic              tpend_issue_w;
  logic [IF_W_C-1:0] tpend_issue_if_w;

  always_ff @(posedge clk_i) begin : adv_sm
    if (!rst_n) begin
      for (int unsigned i = 0; i < N_IF_P; i++) begin
        adv_st_r[i]         <= ADP_ADV_DOWN;
        tpend_r[i]          <= TPEND_NONE;
        tpend_deadline_r[i] <= 32'd0;
      end
      adv_startup_r <= '0;
    end else begin
      // issued pending request retires (may be overwritten below)
      if (tpend_issue_w) begin
        tpend_r[tpend_issue_if_w] <= TPEND_NONE;
      end

      for (int unsigned i = 0; i < N_IF_P; i++) begin
        // 1) shared-slot expiry: DELAY -> WAITING (send), WAITING -> DELAY
        if (adv_exp_w && (32'(adv_exp_if_w) == i)) begin
          if (adv_st_r[i] == ADP_ADV_DELAY) begin
            adv_st_r[i] <= ADP_ADV_WAITING;   // pend_avail set below
          end else if (adv_st_r[i] == ADP_ADV_WAITING) begin
            adv_st_r[i]      <= ADP_ADV_DRAW; // T-ADP-ADV cadence restart
            adv_startup_r[i] <= 1'b0;
          end
        end

        // 2) RCV_ADP_DISCOVER: WAITING only (Table 5.51: DELAY/DOWN ignore)
        if (disc_hit_w && (32'(disc_hit_if_w) == i)
            && (adv_st_r[i] == ADP_ADV_WAITING)) begin
          adv_st_r[i]      <= ADP_ADV_DRAW;
          adv_startup_r[i] <= 1'b0;
          tpend_r[i]       <= TPEND_CANCEL;   // stop T-ADP-ADV
        end

        // 3) GM_CHANGE: WAITING only (Milan §5.6.3.5.7)
        if (gm_change_i[i] && (adv_st_r[i] == ADP_ADV_WAITING)) begin
          adv_st_r[i]      <= ADP_ADV_DRAW;
          adv_startup_r[i] <= 1'b0;
          tpend_r[i]       <= TPEND_CANCEL;
        end

        // 4) draw delivered: DRAW -> DELAY, arm T-ADP-DELAY(-START)
        if (draw_del_w && (32'(draw_del_if_w) == i)
            && (adv_st_r[i] == ADP_ADV_DRAW)) begin
          adv_st_r[i]         <= ADP_ADV_DELAY;
          tpend_r[i]          <= TPEND_ARM;
          tpend_deadline_r[i] <= now_ms_i + {16'd0, draw_del_ms_w};
        end

        // 5) ENTITY_AVAILABLE committed: arm T-ADP-ADV (still WAITING)
        if (bld_done_avail_w && (32'(bld_done_if_w) == i)
            && (adv_st_r[i] == ADP_ADV_WAITING)) begin
          tpend_r[i]          <= TPEND_ARM;
          tpend_deadline_r[i] <= now_ms_i + ADP_T_ADV_MS_C;
        end

        // 6) LINK_DOWN: -> DOWN, stop timers, NO departing (Milan §5.6.3.5.6)
        if (link_fall_w[i] && (adv_st_r[i] != ADP_ADV_DOWN)) begin
          adv_st_r[i] <= ADP_ADV_DOWN;
          tpend_r[i]  <= TPEND_CANCEL;
        end

        // 7) entity disable = SHUTDOWN: departing from any advertising state
        if (enable_fall_w && (adv_st_r[i] != ADP_ADV_DOWN)) begin
          adv_st_r[i] <= ADP_ADV_DOWN;        // pend_dep set below
          tpend_r[i]  <= TPEND_CANCEL;
        end

        // 8) begin/resume operation (Milan §5.6.1 gate):
        //    enable rise with link already up -> DELAY via T-ADP-DELAY-START;
        //    LINK_UP while enabled -> DELAY via T-ADP-DELAY (F04.2 arcs)
        if (entity_enable_i && !enable_fall_w
            && (adv_st_r[i] == ADP_ADV_DOWN)) begin
          if (enable_rise_w && link_up_i[i]) begin
            adv_st_r[i]      <= ADP_ADV_DRAW;
            adv_startup_r[i] <= 1'b1;
          end else if (link_rise_w[i] && !enable_rise_w) begin
            adv_st_r[i]      <= ADP_ADV_DRAW;
            adv_startup_r[i] <= 1'b0;
          end
        end
      end
    end
  end

  // ----------------------------------------------------- send-queue bits
  logic              bld_take_w;        // builder consumes a pend bit
  logic              bld_take_dep_w;
  logic [IF_W_C-1:0] bld_take_if_w;

  always_ff @(posedge clk_i) begin : send_queue
    if (!rst_n) begin
      pend_avail_r <= '0;
      pend_dep_r   <= '0;
    end else begin
      for (int unsigned i = 0; i < N_IF_P; i++) begin
        // set: delay expiry sends AVAILABLE; disable sends DEPARTING
        if (adv_exp_w && (32'(adv_exp_if_w) == i)
            && (adv_st_r[i] == ADP_ADV_DELAY)) begin
          pend_avail_r[i] <= 1'b1;
        end
        if (enable_fall_w && (adv_st_r[i] != ADP_ADV_DOWN)) begin
          pend_dep_r[i]   <= 1'b1;
          pend_avail_r[i] <= 1'b0;    // departing supersedes a queued advert
        end
        // link loss abandons a queued advert (never a queued departing)
        if (link_fall_w[i]) begin
          pend_avail_r[i] <= 1'b0;
        end
        // builder pick
        if (bld_take_w && (32'(bld_take_if_w) == i)) begin
          if (bld_take_dep_w) pend_dep_r[i]   <= 1'b0;
          else                pend_avail_r[i] <= 1'b0;
        end
      end
    end
  end

  // ------------------------------------------------- available_index mgr
  // DOC RULE (04 §5, IEEE §6.2.2.15): 0 at power-up; ++ AFTER each
  // transmitted ENTITY_AVAILABLE; reset to 0 after ENTITY_DEPARTING (the
  // departing frame carries the pre-reset value). See banner: diverges
  // from the reference platform's every-ADPDU increment; adjudication
  // against live controllers is required before cutover.
  logic [31:0] aidx_r [N_IF_P];

  always_ff @(posedge clk_i) begin : avail_index_mgr
    if (!rst_n) begin
      for (int unsigned i = 0; i < N_IF_P; i++) aidx_r[i] <= 32'd0;
    end else begin
      if (bld_done_avail_w) begin
        aidx_r[bld_done_if_w] <= aidx_r[bld_done_if_w] + 32'd1;
      end
      if (bld_done_dep_w) begin
        aidx_r[bld_done_if_w] <= 32'd0;
      end
    end
  end

  // ======================================================= PRNG serializer
  // One draw in flight; requests scan the interfaces in DRAW state. The
  // captured kind must still match the SM's current wish at delivery —
  // a stale draw (link bounced mid-draw) is discarded, never mis-kinded.
  logic              draw_act_r;
  logic [IF_W_C-1:0] draw_if_r;
  logic [2:0]        draw_kind_r;
  logic              draw_req_r;
  logic [2:0]        draw_req_kind_r;

  logic              draw_need_w;
  logic [IF_W_C-1:0] draw_need_if_w;
  logic [2:0]        draw_need_kind_w;

  always_comb begin : draw_pick
    draw_need_w      = 1'b0;
    draw_need_if_w   = '0;
    draw_need_kind_w = ADP_DRAW_KIND_DELAY_C;
    for (int unsigned i = 0; i < N_IF_P; i++) begin
      if (!draw_need_w && (adv_st_r[i] == ADP_ADV_DRAW)) begin
        draw_need_w      = 1'b1;
        draw_need_if_w   = IF_W_C'(i);
        draw_need_kind_w = adv_startup_r[i] ? ADP_DRAW_KIND_START_C
                                            : ADP_DRAW_KIND_DELAY_C;
      end
    end
  end

  //! wanted kind of the in-flight draw's interface, re-derived at delivery
  logic [2:0] draw_want_now_w;
  assign draw_want_now_w = adv_startup_r[draw_if_r] ? ADP_DRAW_KIND_START_C
                                                    : ADP_DRAW_KIND_DELAY_C;

  assign draw_del_w    = prng_draw_valid_i && draw_act_r
                         && (adv_st_r[draw_if_r] == ADP_ADV_DRAW)
                         && (draw_want_now_w == draw_kind_r);
  assign draw_del_if_w = draw_if_r;
  assign draw_del_ms_w = prng_draw_ms_i;

  always_ff @(posedge clk_i) begin : prng_serializer
    if (!rst_n) begin
      draw_act_r      <= 1'b0;
      draw_if_r       <= '0;
      draw_kind_r     <= 3'd0;
      draw_req_r      <= 1'b0;
      draw_req_kind_r <= 3'd0;
    end else begin
      draw_req_r <= 1'b0;
      if (draw_act_r) begin
        if (prng_draw_valid_i) begin
          draw_act_r <= 1'b0;      // delivered or discarded either way
        end
      end else if (draw_need_w && !prng_draw_busy_i && !draw_req_r) begin
        draw_req_r      <= 1'b1;   // one-cycle request pulse
        draw_req_kind_r <= draw_need_kind_w;
        draw_if_r       <= draw_need_if_w;
        draw_kind_r     <= draw_need_kind_w;
        draw_act_r      <= 1'b1;
      end
    end
  end

  assign prng_draw_req_o  = draw_req_r;
  assign prng_draw_kind_o = draw_req_kind_r;

  // ========================================================= ADPDU builder
  typedef enum logic [2:0] {
    B_IDLE   = 3'd0,
    B_SAMPLE = 3'd1,
    B_ALLOC  = 3'd2,
    B_GWAIT  = 3'd3,
    B_WRITE  = 3'd4,
    B_COMMIT = 3'd5,
    B_REQ    = 3'd6
  } bld_st_e;

  bld_st_e           bld_st_r;
  logic              bld_dep_r;      // building ENTITY_DEPARTING
  logic [IF_W_C-1:0] bld_if_r;
  logic [TXS_SLOT_W_C-1:0] bld_slot_r;
  logic [6:0]        bld_idx_r;      // wire byte 0..81
  logic [63:0]       bld_gm_r;       // gm_id sampled at PDU build (04 §3)
  logic [7:0]        bld_dom_r;
  logic [31:0]       bld_aidx_r;

  // builder pick (departing outranks a queued advert)
  logic              pick_vld_w;
  logic              pick_dep_w;
  logic [IF_W_C-1:0] pick_if_w;

  always_comb begin : bld_pick
    pick_vld_w = 1'b0;
    pick_dep_w = 1'b0;
    pick_if_w  = '0;
    for (int unsigned i = 0; i < N_IF_P; i++) begin
      if (!pick_vld_w && pend_dep_r[i]) begin
        pick_vld_w = 1'b1;
        pick_dep_w = 1'b1;
        pick_if_w  = IF_W_C'(i);
      end
    end
    for (int unsigned i = 0; i < N_IF_P; i++) begin
      if (!pick_vld_w && pend_avail_r[i]) begin
        pick_vld_w = 1'b1;
        pick_dep_w = 1'b0;
        pick_if_w  = IF_W_C'(i);
      end
    end
  end

  assign bld_take_w     = (bld_st_r == B_IDLE) && pick_vld_w;
  assign bld_take_dep_w = pick_dep_w;
  assign bld_take_if_w  = pick_if_w;

  //! F04.5 wire frame, byte-exact (i = wire byte offset; 82 bytes total)
  function automatic logic [7:0] frame_byte_f(
      input logic [6:0]        idx,
      input logic              dep,
      input logic [IF_W_C-1:0] ifx,
      input logic [63:0]       gm,
      input logic [7:0]        dom,
      input logic [31:0]       aidx);
    int unsigned i;
    logic [7:0] b;
    i = 32'(idx);
    b = 8'h00;
    if (i < 6)        b = byte48_f(ADP_MCAST_DA_C, i);            // DA @0
    else if (i < 12)  b = byte48_f(own_mac_i, i - 6);             // SA @6
    else if (i < 14)  b = byte16_f(ADP_ETHERTYPE_C, i - 12);      // @12
    else if (i == 14) b = ADP_SUBTYPE_C;                          // subtype
    else if (i == 15) b = {4'b0000,                               // h+version
                           dep ? ADP_MSG_DEPARTING_C : ADP_MSG_AVAILABLE_C};
    else if (i == 16) b = {dep ? 5'd0 : ADP_VALID_TIME_C,         // valid_time
                           ADP_CDL_C[10:8]};
    else if (i == 17) b = ADP_CDL_C[7:0];                         // cdl = 56
    else if (i < 26)  b = byte64_f(entity_id_i, i - 18);          // eid @18
    else if (i < 34)  b = byte64_f(entity_model_id_i, i - 26);
    else if (i < 38)  b = byte32_f(ADP_ENTITY_CAPS_C, i - 34);
    else if (i < 40)  b = byte16_f(talker_sources_i, i - 38);
    else if (i < 42)  b = byte16_f(talker_caps_i, i - 40);
    else if (i < 44)  b = byte16_f(listener_sinks_i, i - 42);
    else if (i < 46)  b = byte16_f(listener_caps_i, i - 44);
    else if (i < 50)  b = 8'h00;                                  // ctrl caps
    else if (i < 54)  b = byte32_f(aidx, i - 50);                 // avail idx
    else if (i < 62)  b = byte64_f(gm, i - 54);                   // gm @54
    else if (i == 62) b = dom;                                    // domain
    else if (i == 63) b = 8'h00;                                  // reserved
    else if (i < 66)  b = byte16_f(current_cfg_i, i - 64);
    else if (i < 68)  b = byte16_f(identify_index_i, i - 66);
    else if (i < 70)  b = byte16_f({{(16-IF_W_C){1'b0}}, ifx}, i - 68);
    else              b = 8'h00;               // association_id + reserved
    return b;
  endfunction

  always_ff @(posedge clk_i) begin : builder
    if (!rst_n) begin
      bld_st_r   <= B_IDLE;
      bld_dep_r  <= 1'b0;
      bld_if_r   <= '0;
      bld_slot_r <= '0;
      bld_idx_r  <= 7'd0;
      bld_gm_r   <= 64'd0;
      bld_dom_r  <= 8'd0;
      bld_aidx_r <= 32'd0;
    end else begin
      unique case (bld_st_r)
        B_IDLE: begin
          if (pick_vld_w) begin
            bld_dep_r <= pick_dep_w;
            bld_if_r  <= pick_if_w;
            bld_st_r  <= B_SAMPLE;
          end
        end
        B_SAMPLE: begin
          bld_gm_r   <= gm_slice_f(bld_if_r);       // sampled at PDU build
          bld_dom_r  <= dom_slice_f(bld_if_r);
          bld_aidx_r <= aidx_r[bld_if_r];           // pre-increment value
          bld_st_r   <= B_ALLOC;
        end
        B_ALLOC: begin
          bld_st_r <= B_GWAIT;                      // one-cycle alloc pulse
        end
        B_GWAIT: begin
          if (txs_alloc_gnt_i) begin
            bld_slot_r <= txs_alloc_slot_i;
            bld_idx_r  <= 7'd0;
            bld_st_r   <= B_WRITE;
          end else begin
            bld_st_r <= B_ALLOC;                    // pool full: retry
          end
        end
        B_WRITE: begin
          if (32'(bld_idx_r) == ADP_FRAME_BYTES_C - 1) begin
            bld_st_r <= B_COMMIT;
          end else begin
            bld_idx_r <= bld_idx_r + 7'd1;
          end
        end
        B_COMMIT: begin
          bld_st_r <= B_REQ;
        end
        B_REQ: begin
          bld_st_r <= B_IDLE;
        end
        default: bld_st_r <= B_IDLE;
      endcase
    end
  end

  assign txs_alloc_req_o = (bld_st_r == B_ALLOC);
  assign txs_oversize_o  = 1'b0;
  assign txs_wr_slot_o   = bld_slot_r;
  assign txs_wr_addr_o   = TXS_LEN_W_C'(bld_idx_r);
  assign txs_wr_valid_o  = (bld_st_r == B_WRITE);
  assign txs_wr_data_o   = frame_byte_f(bld_idx_r, bld_dep_r, bld_if_r,
                                        bld_gm_r, bld_dom_r, bld_aidx_r);
  assign txs_wr_commit_o = (bld_st_r == B_COMMIT);
  assign txs_wr_len_o    = TXS_LEN_W_C'(ADP_FRAME_BYTES_C);

  assign txreq_valid_o = (bld_st_r == B_REQ);
  assign txreq_slot_o  = bld_slot_r;
  assign txreq_if_o    = bld_if_r;

  assign bld_done_avail_w = (bld_st_r == B_REQ) && !bld_dep_r;
  assign bld_done_dep_w   = (bld_st_r == B_REQ) && bld_dep_r;
  assign bld_done_if_w    = bld_if_r;

  // ==================================================== timer-port muxing
  // Single arm/cancel port toward KL_pp_timer_service. Priority: the
  // discovery iteration (must never stall) > unbind NOADP cancels >
  // per-interface shared-slot pending requests.
  logic [N_SINK_P-1:0] ucancel_pend_r;
  logic                ucancel_issue_w;
  logic [SNK_W_C-1:0]  ucancel_sink_w;

  always_comb begin : ucancel_pick
    ucancel_issue_w = 1'b0;
    ucancel_sink_w  = '0;
    for (int unsigned s = 0; s < N_SINK_P; s++) begin
      if (!ucancel_issue_w && ucancel_pend_r[s]) begin
        ucancel_issue_w = 1'b1;
        ucancel_sink_w  = SNK_W_C'(s);
      end
    end
  end

  logic              tpend_any_w;
  logic [IF_W_C-1:0] tpend_if_w;

  always_comb begin : tpend_pick
    tpend_any_w = 1'b0;
    tpend_if_w  = '0;
    for (int unsigned i = 0; i < N_IF_P; i++) begin
      if (!tpend_any_w && (tpend_r[i] != TPEND_NONE)) begin
        tpend_any_w = 1'b1;
        tpend_if_w  = IF_W_C'(i);
      end
    end
  end

  logic iter_port_w;
  assign iter_port_w = iter_arm_w || iter_cancel_w;

  assign tpend_issue_w    = tpend_any_w && !iter_port_w && !ucancel_issue_w;
  assign tpend_issue_if_w = tpend_if_w;

  logic ucancel_grant_w;
  assign ucancel_grant_w = ucancel_issue_w && !iter_port_w;

  always_ff @(posedge clk_i) begin : ucancel_pend
    if (!rst_n) begin
      ucancel_pend_r <= '0;
    end else begin
      for (int unsigned s = 0; s < N_SINK_P; s++) begin
        if (bound_fall_w[s] && disc_st_r[s]) begin
          ucancel_pend_r[s] <= 1'b1;
        end
      end
      if (ucancel_grant_w) begin
        ucancel_pend_r[ucancel_sink_w] <= 1'b0;
      end
    end
  end

  always_comb begin : tmr_port_mux
    tmr_arm_valid_o       = 1'b0;
    tmr_arm_cancel_o      = 1'b0;
    tmr_arm_slot_o        = '0;
    tmr_arm_deadline_ms_o = 32'd0;
    if (iter_port_w) begin
      tmr_arm_valid_o       = 1'b1;
      tmr_arm_cancel_o      = iter_cancel_w;
      tmr_arm_slot_o        = TMR_AW_C'(TMR_SLOT_NOADP_BASE_P + 32'(sink_r));
      tmr_arm_deadline_ms_o = now_ms_i + adp_vt_to_ms_f(rxq_vt_r);
    end else if (ucancel_issue_w) begin
      tmr_arm_valid_o  = 1'b1;
      tmr_arm_cancel_o = 1'b1;
      tmr_arm_slot_o   = TMR_AW_C'(TMR_SLOT_NOADP_BASE_P + 32'(ucancel_sink_w));
    end else if (tpend_any_w) begin
      tmr_arm_valid_o       = 1'b1;
      tmr_arm_cancel_o      = (tpend_r[tpend_if_w] == TPEND_CANCEL);
      tmr_arm_slot_o        = TMR_AW_C'(TMR_SLOT_ADV_BASE_P + 32'(tpend_if_w));
      tmr_arm_deadline_ms_o = tpend_deadline_r[tpend_if_w];
    end
  end

  assign tmr_arm_owner_o = {{(PP_TIMER_OWNER_W_C-TMR_AW_C){1'b0}}, tmr_arm_slot_o};

  // ======================================================== event emitter
  // Iterator events take the port (DEPARTED first on a restart pair);
  // NOADP-expiry DEPARTED events queue per sink and drain when idle.
  logic [N_SINK_P-1:0] pend_dep_evt_r;
  logic                drain_any_w;
  logic [SNK_W_C-1:0]  drain_sink_w;

  always_comb begin : drain_pick
    drain_any_w  = 1'b0;
    drain_sink_w = '0;
    for (int unsigned s = 0; s < N_SINK_P; s++) begin
      if (!drain_any_w && pend_dep_evt_r[s]) begin
        drain_any_w  = 1'b1;
        drain_sink_w = SNK_W_C'(s);
      end
    end
  end

  logic iter_evt_w;
  assign iter_evt_w = (rx_st_r == RX_SINK_EX) && (ev_dep_w || ev_disc_w);

  always_ff @(posedge clk_i) begin : event_emitter
    if (!rst_n) begin
      evt_valid_o    <= 1'b0;
      evt_departed_o <= 1'b0;
      evt_sink_o     <= '0;
      pend_dep_evt_r <= '0;
    end else begin
      evt_valid_o <= 1'b0;
      // NOADP expiry in TK_DISCOVERED queues a DEPARTED event
      if (noadp_exp_w && disc_st_r[noadp_exp_sink_w]) begin
        pend_dep_evt_r[noadp_exp_sink_w] <= 1'b1;
      end
      if (iter_evt_w) begin
        evt_valid_o    <= 1'b1;
        evt_departed_o <= ev_dep_w;       // pair order: DEPARTED first
        evt_sink_o     <= sink_r;
      end else if (rx_st_r == RX_SINK_EV2) begin
        evt_valid_o    <= 1'b1;
        evt_departed_o <= 1'b0;           // then DISCOVERED
        evt_sink_o     <= sink_r;
      end else if (drain_any_w) begin
        evt_valid_o    <= 1'b1;
        evt_departed_o <= 1'b1;
        evt_sink_o     <= drain_sink_w;
        pend_dep_evt_r[drain_sink_w] <= 1'b0;
      end
    end
  end

  // -------------------------------------------------------- observability
  always_comb begin : dbg_flatten
    for (int unsigned i = 0; i < N_IF_P; i++) begin
      dbg_adv_state_o[2*i +: 2]    = adv_st_r[i];
      dbg_avail_index_o[32*i +: 32] = aidx_r[i];
    end
  end

endmodule : KL_adp_engine
`default_nettype wire
