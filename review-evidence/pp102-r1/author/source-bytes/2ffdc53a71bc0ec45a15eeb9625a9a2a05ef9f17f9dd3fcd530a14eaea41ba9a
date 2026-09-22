/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : pp_pkg.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/03, 08)
//
//  Description : Shared protocol-processor types — the normalized-transaction
//                record of 03 §4 as ONE packed struct, the nine scoreboard
//                hazard classes of 03 §6, the origin/protocol/disposition
//                enums, and the P-TIMER-SLOTS allocation formula of 08 §5.
//
//                The one design decision that matters: the slot handles are
//                FIXED narrow indices with an explicit null code
//                (PP_SLOT_NULL_C), sized from the F01.5 defaults
//                (P-RX-SLOTS = 4, P-TX-STD-SLOTS = 4 + 1 oversize), not
//                parameterized widths — the record must be one packed shape
//                every dispatch FIFO and queue of 03 §2 can carry unchanged.
//
//                Field-width notes against 03 §4:
//                  - interface_index is fixed at 2 bits (covers
//                    P-N-AVB-INTERFACES up to 4; the F01.5 default is 1).
//                  - operands is the 03 §4 "struct" row, folded to a 64-bit
//                    packed quartet {desc_type, desc_index, config_index,
//                    unique_id} — the same 64-bit opd lane KL_aecp_ucpu
//                    preloads at dispatch (06 §8).
//---------------------------------------------------------------------------//
`default_nettype none

package pp_pkg;

  // ---- origins (03 §5: the four producers into dispatch) -----------------
  typedef enum logic [1:0] {
    PP_ORIGIN_RX    = 2'd0,
    PP_ORIGIN_TIMER = 2'd1,
    PP_ORIGIN_SELF  = 2'd2,
    PP_ORIGIN_MGMT  = 2'd3
  } pp_origin_e;

  // ---- protocols (03 §4: ADP / ACMP / AEM / MVU / AA / MAAP) -------------
  typedef enum logic [2:0] {
    PP_PROTO_ADP  = 3'd0,
    PP_PROTO_ACMP = 3'd1,
    PP_PROTO_AEM  = 3'd2,
    PP_PROTO_MVU  = 3'd3,
    PP_PROTO_AA   = 3'd4,
    PP_PROTO_MAAP = 3'd5   // IEEE 1722-2016 Annex B, subtype 0xFE (11)
  } pp_protocol_e;

  // ---- the NINE hazard classes of 03 §6 (F03.7 row order) ----------------
  typedef enum logic [3:0] {
    PP_HZ_RO_SNAPSHOT = 4'd0,  // parallel reads; blocked only vs same-key write
    PP_HZ_CFG_BARRIER = 4'd1,  // SET_CONFIGURATION: global drain
    PP_HZ_STREAM_CFG  = 4'd2,  // per stream index; doubles as sink-SM serial
    PP_HZ_MAP_CFG     = 4'd3,  // per stream port; cross-locked w/ STREAM_CFG
    PP_HZ_CLOCK_CFG   = 4'd4,  // per audio unit / clock domain
    PP_HZ_NAME_WR     = 4'd5,  // per descriptor
    PP_HZ_LOCK_OP     = 4'd6,  // global vs every lock-protected member
    PP_HZ_REGISTRY_OP = 4'd7,  // serialized on the registry
    PP_HZ_IDENTIFY    = 4'd8   // identify bursts serialized
  } pp_hazard_e;

  // ---- response disposition (03 §4 / §8 addressing) ----------------------
  typedef enum logic [1:0] {
    PP_RESP_UNICAST     = 2'd0,  // AECP: back to src_mac / registry MAC
    PP_RESP_ACMP_MCAST  = 2'd1,  // ACMP: always 91-E0-F0-01-00-00
    PP_RESP_IDENT_MCAST = 2'd2   // identify: 91-E0-F0-01-00-01 (Annex B)
  } pp_resp_disp_e;

  // ---- slot handles ------------------------------------------------------
  // 3 bits: rx encodes 0..P-RX-SLOTS-1 (F01.5: 4); tx encodes
  // 0..P-TX-STD-SLOTS-1 (F01.5: 4) plus PP_TX_OVERSIZE_C for the one
  // full-frame slot (03 §7). PP_SLOT_NULL_C = no payload (TIMER/SELF).
  localparam logic [2:0] PP_SLOT_NULL_C   = 3'd7;
  localparam logic [2:0] PP_TX_OVERSIZE_C = 3'd4;

  // ---- operands sub-struct (03 §4 "operands" row) ------------------------
  typedef struct packed {
    logic [15:0] desc_type;     // addressed descriptor_type
    logic [15:0] desc_index;    // addressed descriptor_index
    logic [15:0] config_index;  // configuration index where applicable
    logic [15:0] unique_id;     // talker/listener unique_id (ACMP)
  } pp_operands_t;

  // ---- the normalized-transaction record (03 §4, one shape for all) ------
  typedef struct packed {
    pp_origin_e    origin;            // RX / TIMER / SELF / MGMT
    logic [1:0]    interface_index;   // ingress port (target port for SELF)
    logic [31:0]   arrival_ts;        // ms; deadline base = end of reception
    pp_protocol_e  protocol;          // ADP / ACMP / AEM / MVU / AA
    logic [3:0]    msg_type;          // header message_type
    logic [4:0]    status_in;         // header status / valid_time
    logic [10:0]   cdl;               // validated control_data_length (V1/V2)
    logic [47:0]   src_mac;           // response addressing + registry tuple
    logic [63:0]   controller_eid;    // as applicable
    logic [63:0]   target_eid;        // as applicable
    logic [15:0]   sequence_id;       // echoed in responses
    logic          u_flag;            // AECP header u bit
    logic          cr;                // AECP header cr bit
    logic [15:0]   opcode;            // AEM/MVU command_type, ACMP/ADP msg_type
    pp_operands_t  operands;          // 03 §4 operands struct (64 b)
    logic [2:0]    rx_slot;           // payload handle; PP_SLOT_NULL_C = none
    pp_hazard_e    hazard_class;      // from the dispatch ROM (03 §6)
    logic [15:0]   hazard_key;        // serialization key within the class
    logic [2:0]    tx_slot;           // allocated at response build
    logic [31:0]   deadline;          // ms absolute: arrival + class budget
    pp_resp_disp_e resp_disposition;  // unicast / ACMP mcast / identify mcast
  } pp_txn_t;

  localparam int unsigned PP_TXN_W_C = $bits(pp_txn_t);  // 393 bits

  // ---- timer geometry (08 §5) --------------------------------------------
  // Deadline RAM record is {owner[7:0], deadline_ms[31:0]} = 40 bits — the
  // 89 x 40 b sizing of 08 §5. The armed bit lives OUTSIDE the RAM (see
  // KL_pp_timer_service.sv).
  localparam int unsigned PP_TIMER_OWNER_W_C = 8;
  localparam int unsigned PP_TIMER_SLOT_DW_C = PP_TIMER_OWNER_W_C + 32;

  // P-TIMER-SLOTS allocation formula (08 §5, F08.4):
  //
  //   slots = IF                       (ADP advertise/delay, shared SM slot)
  //         + SI                       (T-ADP-NOADP, per sink)
  //         + SI                       (ACMP shared SM slot, per sink)
  //         + SO                       (T-SRP-DAFRESH/LEAVEALL2, per source)
  //         + 2*CTRL*IF                (registry monitor + TIME_LIMITED)
  //         + CA_POOL                  (T-AECP-TIMEOUT inflight pool)
  //         + 5                        (LOCK, IDENT-BURST, IDENT-REARM,
  //                                     CTR-OBSERVE, NVM-DEBOUNCE singletons)
  //         + 2                        (MAAP probe_timer + announce_timer,
  //                                     11 / IEEE 1722-2016 B.3.4)
  //         [+ (7 + SI + SO)*IF with the SRP engine: T-MRP-{JOIN,LEAVEALL}
  //            x 2 participants + T-MRP-PERIODIC + registrar-leave pool
  //            (SI + SO streams + Domain + MVRP VID)]
  //
  //   baseline (IF=1, SI=SO=8, CTRL=16, CA=4): 1+8+8+8+32+4+5+2    = 68
  //   with the SRP engine:                      68 + (7 + 8 + 8)    = 91
  //
  // F01.5 shape defaults, named once so nothing below restates them. Every
  // consumer of the map derives from these or from its own shape — a copied
  // literal is exactly the defect the map function exists to prevent.
  localparam int unsigned PP_N_IF_C         = 1;   // P-N-AVB-INTERFACES
  localparam int unsigned PP_N_STREAM_IN_C  = 8;   // P-N-STREAM-IN
  localparam int unsigned PP_N_STREAM_OUT_C = 8;   // P-N-STREAM-OUT
  localparam int unsigned PP_N_CTRL_C       = 16;  // P-N-CONTROLLERS
  localparam int unsigned PP_CA_POOL_C      = 4;   // P-CA-POOL

  // ---- F08.4 SLOT MAP, derived — never literals --------------------------
  // The 08 §5 order above is a CONTRACT: the groups appear in exactly that
  // sequence. Their SIZES are shape-dependent (SI/SO/IF/CTRL/CA), so every
  // base is the running sum of the group extents before it. This struct is
  // the single place that arithmetic exists; protocol_processor_top reads
  // its bases and KL_pp_timer_service is sized from `srp_end`.
  //
  // Why this is not a style preference: the ACMP listener and talker filter
  // timer expiries BY OWNER TAG while ADP and SRP filter BY SLOT, so an
  // aliased slot fails two different silent ways — a lost deadline where the
  // owners differ, and a MISDELIVERED expiry (one engine acting on another's
  // deadline) where they do not. Neither raises an error or moves a counter.
  typedef struct packed {
    int unsigned adp_adv;    // T-ADP-ADV / T-ADP-DELAY, IF slots
    int unsigned adp_noadp;  // T-ADP-NOADP, SI slots
    int unsigned lstn;       // ACMP listener shared SM slot, SI slots
    int unsigned tkr;        // T-SRP-DAFRESH / LEAVEALL2, SO slots
    int unsigned regmon;     // registry monitors, 2*CTRL*IF slots (P4)
    int unsigned capool;     // T-AECP-TIMEOUT inflight pool, CA slots (P4)
    int unsigned single;     // 5 singleton timers (P4)
    int unsigned maap;       // MAAP probe + announce timers, 2 slots (11)
    int unsigned base_end;   // total WITHOUT the SRP engine
    int unsigned srp_cad;    // MRP cadence, 5 + the 2 fixed registrar-leave
    int unsigned srp_tk;     // SRP talker registrar-leave, SO slots
    int unsigned srp_ls;     // SRP listener registrar-leave, SI slots
    int unsigned srp_end;    // total WITH the SRP engine
  } pp_timer_map_t;

  //! The SRP block's fixed head: T-MRP-{JOIN,LEAVEALL} x 2 participants +
  //! T-MRP-PERIODIC (5 cadence slots) followed by the Domain and MVRP VID
  //! registrar-leave slots (2) — the "7" of the (7 + SI + SO) term.
  localparam int unsigned PP_SRP_CAD_SLOTS_C = 7;
  //! LOCK-UNLOCK, IDENT-BURST, IDENT-REARM, CTR-OBSERVE, NVM-DEBOUNCE.
  localparam int unsigned PP_SINGLETON_SLOTS_C = 5;
  //! MAAP probe_timer (+0) and announce_timer (+1) — IEEE 1722-2016 B.3.4.
  //! One SM instance per entity (one block claim), so the group is fixed at
  //! two slots regardless of shape. Appended AFTER the singletons so every
  //! pre-MAAP base above stays where landed engines' defaults already point.
  localparam int unsigned PP_MAAP_SLOTS_C = 2;

  function automatic pp_timer_map_t pp_timer_map(
      input int unsigned n_if,     // P-N-AVB-INTERFACES
      input int unsigned si,       // P-N-STREAM-IN
      input int unsigned so,       // P-N-STREAM-OUT
      input int unsigned n_ctrl,   // P-N-CONTROLLERS
      input int unsigned ca_pool   // P-CA-POOL
  );
    pp_timer_map_t m;
    m.adp_adv   = 32'd0;
    m.adp_noadp = m.adp_adv   + n_if;
    m.lstn      = m.adp_noadp + si;
    m.tkr       = m.lstn      + si;
    m.regmon    = m.tkr       + so;
    m.capool    = m.regmon    + (32'd2 * n_ctrl * n_if);
    m.single    = m.capool    + ca_pool;
    m.maap      = m.single    + PP_SINGLETON_SLOTS_C;
    m.base_end  = m.maap      + PP_MAAP_SLOTS_C;
    // the SRP block, replicated per interface by F08.4; the bases below are
    // interface 0's (the RTL instantiates exactly one KL_srp_top today).
    m.srp_cad   = m.base_end;
    m.srp_tk    = m.srp_cad + PP_SRP_CAD_SLOTS_C;
    m.srp_ls    = m.srp_tk  + so;
    m.srp_end   = m.srp_cad + ((PP_SRP_CAD_SLOTS_C + si + so) * n_if);
    return m;
  endfunction

  function automatic int unsigned pp_timer_slots(
      input int unsigned n_if,     // P-N-AVB-INTERFACES
      input int unsigned si,       // P-N-STREAM-IN
      input int unsigned so,       // P-N-STREAM-OUT
      input int unsigned n_ctrl,   // P-N-CONTROLLERS
      input int unsigned ca_pool,  // P-CA-POOL
      input bit          en_srp    // P-EN-SRP-ENGINE
  );
    pp_timer_map_t m;
    m = pp_timer_map(n_if, si, so, n_ctrl, ca_pool);
    return en_srp ? m.srp_end : m.base_end;
  endfunction

  // F01.5 defaults through the formula — never restated as literals.
  localparam int unsigned PP_TIMER_SLOTS_BASE_C =
      pp_timer_slots(PP_N_IF_C, PP_N_STREAM_IN_C, PP_N_STREAM_OUT_C,
                     PP_N_CTRL_C, PP_CA_POOL_C, 1'b0);         // = 68
  localparam int unsigned PP_TIMER_SLOTS_C =
      pp_timer_slots(PP_N_IF_C, PP_N_STREAM_IN_C, PP_N_STREAM_OUT_C,
                     PP_N_CTRL_C, PP_CA_POOL_C, 1'b1);         // = 91

  // ---- owner-tag space (08 §5; the shared expiry bus is 8 bits) ----------
  // The expiry bus carries {slot, owner}. ADP and SRP filter by SLOT; the
  // ACMP listener and talker filter by OWNER TAG, so their per-index owner
  // ranges must not overlap ANY other engine's. Unlike the slot map these
  // bases are a FIXED allocation of a fixed 8-bit space, so they are stated
  // once here and BOUNDED by an elaboration guard in the top rather than
  // re-spaced per shape (re-spacing them would silently move the tags a
  // landed engine's default parameters already publish).
  localparam logic [7:0] PP_OWN_LSTN_C    = 8'h20;  // + sink   (KL_pp_acmp_listener)
  localparam logic [7:0] PP_OWN_SRP_TK_C  = 8'h40;  // + source (KL_srp_talker_fsm)
  localparam logic [7:0] PP_OWN_TKR_C     = 8'h50;  // + source (KL_acmp_talker)
  localparam logic [7:0] PP_OWN_SRP_LS_C  = 8'h60;  // + sink   (KL_srp_listener_fsm)
  localparam logic [7:0] PP_OWN_SRP_CAD_C = 8'h80;  // + 0..6   (KL_srp_top cadence)
  localparam logic [7:0] PP_OWN_MAAP_C    = 8'h90;  // + 0 probe / 1 announce (KL_pp_maap)
  localparam logic [7:0] PP_OWN_NTFY_C    = 8'hA0;  // + entry  (KL_aecp_notify TL registry)
  localparam logic [7:0] PP_OWN_LOCK_C    = 8'hB0;  // the ENTITY lock singleton (KL_aecp_notify)
  // 0xC0..0xCF is KL_pp_originator's TMR_TAG_P nibble - see its parameter
  localparam logic [7:0] PP_OWN_CMON_C    = 8'hD0;  // + entry  (Milan controller monitor)

  // ---- unsolicited-notification job kinds (06 SS6.7) ---------------------
  // KL_aecp_notify names the RESPONSE TYPE of a job; KL_aecp_engine maps the
  // kind onto {command_type, uPC entry}. A kind whose microprogram has not
  // landed maps to the no-send program - never a well-formed frame with an
  // empty body.
  localparam logic [3:0] PP_UNS_DEREG_C = 4'd0;  // DEREGISTER_UNSOLICITED_NOTIFICATION
  localparam logic [3:0] PP_UNS_LOCK_C  = 4'd1;  // LOCK_ENTITY
  localparam logic [3:0] PP_UNS_STRI_C  = 4'd2;  // GET_STREAM_INFO
  localparam logic [3:0] PP_UNS_AVB_C   = 4'd3;  // GET_AVB_INFO
  localparam logic [3:0] PP_UNS_ASP_C   = 4'd4;  // GET_AS_PATH
  localparam logic [3:0] PP_UNS_AMAP_C  = 4'd5;  // ADD/REMOVE_AUDIO_MAPPINGS
  localparam logic [3:0] PP_UNS_CTRS_C  = 4'd6;  // GET_COUNTERS
  localparam logic [3:0] PP_UNS_SRATE_C = 4'd7;  // SET_SAMPLING_RATE body from current state
  localparam logic [3:0] PP_UNS_NAME_C  = 4'd8;  // SET_NAME body from current state
  localparam logic [3:0] PP_UNS_CFG_C   = 4'd9;  // SET_CONFIGURATION body from current state
  localparam logic [3:0] PP_UNS_SFMT_C  = 4'd10; // SET_STREAM_FORMAT body from current state
  localparam logic [3:0] PP_UNS_SINFO_C = 4'd11; // SET_STREAM_INFO body from current state
  localparam logic [3:0] PP_UNS_CTRL_C  = 4'd12; // SET_CONTROL body from current state
  localparam logic [3:0] PP_UNS_CLKS_C  = 4'd13; // SET_CLOCK_SOURCE body from current state
  localparam logic [3:0] PP_UNS_STRM_C  = 4'd14; // START/STOP_STREAMING response body

  // ---- 02 §5 event-router SOURCE MAP, derived — never literals -----------
  // The router presents ONE source index per event and carries no owner tag,
  // so two groups landing on the same index are indistinguishable at the
  // consumer: the ACMP listener's kind decode is a pure range compare on the
  // index. Same failure shape as the timer map, same cure — the ORDER is the
  // contract, the SIZES are the shape.
  typedef struct packed {
    int unsigned tk_reg;    // SRP TK_ATTR_REGISTERED{sink},   SI sources
    int unsigned tk_unreg;  // SRP TK_ATTR_UNREGISTERED{sink}, SI sources
    int unsigned adp_disc;  // ADP EVT_TK_DISCOVERED{sink}
    int unsigned adp_dep;   // ADP EVT_TK_DEPARTED{sink}
    int unsigned domain;    // SRP DOMAIN_CHANGE
    int unsigned lsn_chg;   // SRP LISTENER_REG_CHANGE{source}, SO sources
    int unsigned gm_chg;    // gPTP GM_CHANGE
    int unsigned link;      // interface LINK edge
    int unsigned n_src;     // total sources (= 29 at the 8x8 default)
  } pp_evr_map_t;

  function automatic pp_evr_map_t pp_evr_map(
      input int unsigned si,   // P-N-STREAM-IN
      input int unsigned so    // P-N-STREAM-OUT
  );
    pp_evr_map_t m;
    m.tk_reg   = 32'd0;
    m.tk_unreg = m.tk_reg   + si;
    m.adp_disc = m.tk_unreg + si;
    m.adp_dep  = m.adp_disc + 32'd1;
    m.domain   = m.adp_dep  + 32'd1;
    m.lsn_chg  = m.domain   + 32'd1;
    m.gm_chg   = m.lsn_chg  + so;
    m.link     = m.gm_chg   + 32'd1;
    m.n_src    = m.link     + 32'd1;
    return m;
  endfunction

endpackage : pp_pkg
`default_nettype wire
