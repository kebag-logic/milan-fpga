/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_maap.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/11_maap_engine.md in full; 02 §4.2 the
//                 allocator seam it answers; 08 §5 the two F08.4 MAAP slots;
//                 08 §3 PRNG kinds 5/6/7)
//
//  Description : MAAP, IEEE Std 1722-2016 Annex B, as a processor-class
//                engine: ONE state machine instance (B.3.2) claiming ONE
//                contiguous block of cfg_count_i addresses out of the
//                dynamic allocation pool 91:E0:F0:00:00:00..91:E0:F0:00:FD:FF
//                (Table B.9) for the whole entity — source s uses base + s,
//                the same convention the integrating fabric already applies
//                (KL_pp_maap_shim: milan_datapath's `eff_aaf_dmac + j`).
//                The Table B.7 walk, byte-exact PDUs (Figure B.1, cdl 16 per
//                B.2.1), the B.3.4 randomized timers and the B.3.6.4
//                compare_MAC tie-break are implemented against the standard
//                text, NOT against the pipewire reference contract the
//                fabric's KL_maap transcribed — the deviations between the
//                two are listed at the bottom of this banner.
//
//                THE WALK (Table B.7, executed literally):
//                  Begin!/PortOperational! = the rise of (cfg_en_i AND
//                  link_up_i AND cfg_count_i != 0): generate_address (the
//                  seed on the first attempt if provisioned — footnote a —
//                  else a PRNG kind-7 draw, rejection-clamped so the whole
//                  block fits the pool) then ReserveAddress!:
//                  maap_probe_count := 3 (MAAP_PROBE_RETRANSMITS, Table
//                  B.8), Start probe_timer (kind-5 draw: 500 < T < 600 ms,
//                  B.3.4.2), sProbe, -> PROBE. Each probetimer! restarts
//                  the timer with a FRESH draw, sends another PROBE and
//                  decrements; the decrement that reaches zero is
//                  probeCount! (B.3.5.8): Stop probe_timer, Start
//                  announce_timer (kind-6 draw: 30 s < T < 32 s, B.3.4.1),
//                  sAnnounce, -> DEFEND. Four PROBEs total leave the wire
//                  (the initial transmit plus three RE-transmits), the
//                  first ANNOUNCE back-to-back with the fourth, and the
//                  claim is valid (addr_valid_o) from that instant —
//                  exactly the <= 3 probe-interval acquisition
//                  KL_acmp_talker's P-MAAP-RSP-MS bound is derived from.
//
//                THE CONFLICT MATRIX (Table B.7 rows rProbe!/rDefend!/
//                rAnnounce!; only PDUs whose range overlaps ours generate
//                events at all — footnote b):
//                                PROBE state          DEFEND state
//                  rProbe!    compare_MAC, else     sDefend (echo the
//                             yield+re-randomize    probe's requested_*,
//                                                   conflict_* = the
//                                                   overlap, B.3.6.6;
//                                                   NO compare_MAC here)
//                  rDefend!   yield+re-randomize    compare_MAC, else
//                  rAnnounce! (no compare_MAC)      yield+re-randomize
//                  Release!/engage-fall = Stop timers, INITIAL, NO PDU
//                  (B.3.5.2 + footnote c: a local event; nothing is sent).
//                compare_MAC (B.3.6.4): octet-wise REVERSED unsigned
//                compare; TRUE (we are lower) = no further processing.
//                A yield re-enters through INITIAL/Restart!: a FRESH
//                random address (the seed is deliberately not reused on a
//                conflict — the range is known-bad), a fresh probe walk,
//                and the falling addr_valid_o fans out one per-source
//                conflict event through the embedded seam logic below.
//
//                WHICH RANGE a received PDU "contains" (B.3.5.5-7): a PROBE
//                is judged on its requested_* fields (its conflict_* are 0
//                by B.2.7/B.2.8); a DEFEND or ANNOUNCE is judged on
//                requested_* OR conflict_* (the inclusive reading of "an
//                address range that conflicts" — a DEFEND carries both, and
//                the fabric peers fill conflict_* per the reference). An
//                all-zero count is an EMPTY range and never conflicts, so
//                an ANNOUNCE's zero conflict fields contribute nothing.
//
//                THE SEAM, answered internally: the alloc_* / conflict_*
//                group below is the exact 10-pin face KL_pp_maap_shim
//                presents to the talker, inheriting its five recorded
//                decisions verbatim: (1) accept-and-answer-next-cycle,
//                never ready-stuck-low — the answer is a combinational
//                function of the claim sampled at the accepting cycle, so
//                an accepted request cannot fail to complete; (2) ok only
//                when the claim is VALID (DEFEND state) and src <
//                cfg_count_i; (3) RELEASE_DA is a no-op acknowledgement (one
//                block per entity, Annex B has no partial release); (4) a
//                block identity change away from a granting state raises a
//                conflict for EVERY source, lowest pending first, sticky
//                until acked; (5) not-engaged and still-probing share the
//                refuse path. Decision 1's grant arithmetic adds on the
//                16-bit offset half only, so a granted DA structurally
//                cannot leave the pool.
//
//                RX arrives as dispatched pp_txn_t records only — the
//                validator captures requested_* into the controller_eid
//                lane and conflict_* into the operands lane (F03.4 MAAP
//                columns), so this engine never reads the RX slot pool: it
//                frees the record's slot on classify and works from the
//                record. maap_version is NOT checked (B.2.3.2: higher
//                versions with a known message_type are interpreted as the
//                implemented version); reserved message_types are ignored
//                (B.2.2); a version-0 PDU is likewise processed (B.2.3.4 —
//                fields of the current version are a superset).
//
//                TX: whole 60-byte wire frames (42 real bytes zero-padded
//                to the Ethernet minimum, the fabric convention) through
//                the shared KL_pp_tx_slots pool and one dedicated
//                KL_pp_tx_arbiter lane; txreq is HELD until granted, so
//                back-to-back sends (the 4th PROBE + 1st ANNOUNCE) simply
//                serialize.
//
//                Deviations from the fabric's KL_maap (the reference-
//                contract engine this one can mechanically replace via
//                addr_o/addr_valid_o/state_o/conflicts_o/defends_o):
//                  - control_data_length 16 (B.2.1 "shall be set to 16")
//                    not the reference's 28; KL_maap's RX parser checks
//                    only ethertype+subtype, so the strict frame still
//                    interoperates;
//                  - 4 probes (1 + MAAP_PROBE_RETRANSMITS) not 3, and the
//                    first ANNOUNCE immediately at probeCount!;
//                  - announce cadence 30..32 s (Table B.8) not 3 s;
//                  - probe interval strictly inside (500, 600) ms via PRNG
//                    kind 5, announce strictly inside (30, 32) s via kind
//                    6 — B.3.4's bounds are exclusive;
//                  - compare_MAC tie-breaks (KL_maap has none: it always
//                    yields in PROBE and never yields checks in DEFEND);
//                  - a PROBE is judged on requested_*; KL_maap judged
//                    DEFEND/ANNOUNCE on conflict_* only (this engine
//                    checks both, see above).
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_maap
  import pp_pkg::*;
#(
    //! number of talker sources the seam fans conflicts out to
    //! (the processor's N_STREAM_OUT_P)
    parameter int unsigned N_SRC_P = 8,
    //! P-RX-SLOTS of the attached pool (bounds the free-port handle range)
    parameter int unsigned RX_SLOTS_P = 4,
    //! timer slots of the attached KL_pp_timer_service (index width only)
    parameter int unsigned TMR_SLOTS_P = pp_pkg::PP_TIMER_SLOTS_C,
    //! first of this engine's TWO F08.4 slots: +0 probe_timer,
    //! +1 announce_timer (08 §5 MAAP group)
    parameter int unsigned TMR_SLOT_BASE_P = 61,
    //! owner-tag base echoed at expiry (pp_pkg::PP_OWN_MAAP_C)
    parameter logic [7:0]  TMR_OWNER_BASE_P = 8'h90,
    //! KL_pp_tx_slots geometry — must match the instantiated pool
    parameter int unsigned TX_STD_SLOTS_P = 4,
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600,
    //! derived widths — do not override
    localparam int unsigned SRC_W_C = (N_SRC_P > 32'd1) ? $clog2(N_SRC_P)
                                                        : 32'd1,
    localparam int unsigned TMR_AW_C = (TMR_SLOTS_P > 32'd1)
                                       ? $clog2(TMR_SLOTS_P) : 32'd1,
    localparam int unsigned TXS_SLOT_W_C = $clog2(TX_STD_SLOTS_P + 1),
    localparam int unsigned TXS_LEN_W_C  = $clog2(TX_OVERSIZE_BYTES_P + 1)
) (
    input  wire                        clk_i,            //! core clock (P-CLK-HZ)
    input  wire                        rst_n,            //! sync active-low reset

    //! ---- quasi-static configuration (02 §2 rule 4) ------------------------
    input  wire                        cfg_en_i,         //! 1 = this engine owns the claim (cfg_maap_internal_i)
    input  wire  [7:0]                 cfg_count_i,      //! block size to claim (>= 1; 0 = idle)
    input  wire  [15:0]                cfg_seed_offset_i,//! provisioning: preferred pool offset (footnote a)
    input  wire                        cfg_seed_valid_i, //! 1 = first walk after engage probes the seed
    input  wire  [47:0]                own_mac_i,        //! source MAC + compare_MAC operand

    //! ---- level status -----------------------------------------------------
    input  wire                        link_up_i,        //! PortOperational! level (B.3.5.9)

    //! ---- dispatch-in (KL_pp_dispatch MAAP pop face) -----------------------
    input  wire                        txn_valid_i,      //! head record valid
    input  wire  [PP_TXN_W_C-1:0]      txn_i,            //! pp_txn_t (protocol = MAAP)
    output logic                       txn_ready_o,      //! engine consumes the head record

    //! ---- RX slot free (records are self-contained: free-only, no reads) ---
    output logic                       rxs_free_o,       //! return the record's payload slot
    output logic [2:0]                 rxs_free_slot_o,  //! which slot (pp_pkg handle space)

    //! ---- PRNG draw port (KL_pp_prng kinds 5/6/7) --------------------------
    output logic                       prng_draw_req_o,  //! one-cycle draw request
    output logic [2:0]                 prng_draw_kind_o, //! 5 probe / 6 announce / 7 address
    input  wire                        prng_draw_busy_i, //! draw in progress
    input  wire                        prng_draw_valid_i,//! one-cycle: draw_ms_i holds the result
    input  wire  [15:0]                prng_draw_ms_i,   //! drawn value (ms, or a kind-7 offset)

    //! ---- timer service (arm/expiry faces) ---------------------------------
    input  wire  [31:0]                now_ms_i,         //! absolute ms timebase
    output logic                       tmr_arm_valid_o,  //! arm/cancel strobe
    output logic                       tmr_arm_cancel_o, //! 1 = cancel the slot
    output logic [TMR_AW_C-1:0]        tmr_arm_slot_o,   //! deadline slot index
    output logic [PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_o, //! owner tag
    output logic [31:0]                tmr_arm_deadline_ms_o, //! absolute ms deadline
    input  wire                        tmr_exp_valid_i,  //! expiry event
    input  wire  [TMR_AW_C-1:0]        tmr_exp_slot_i,   //! expired slot
    input  wire  [PP_TIMER_OWNER_W_C-1:0] tmr_exp_owner_i, //! owner tag (unused: slot decodes)

    //! ---- TX slot pool (alloc/write/commit through the top's access mux) ---
    output logic                       txs_alloc_req_o,  //! one-cycle slot request
    output logic                       txs_oversize_o,   //! MAAP never needs the oversize slot (tied 0)
    input  wire                        txs_alloc_gnt_i,  //! grant, with the slot below
    input  wire  [TXS_SLOT_W_C-1:0]    txs_alloc_slot_i, //! granted slot index
    output logic [TXS_SLOT_W_C-1:0]    txs_wr_slot_o,    //! slot being written / committed
    output logic [TXS_LEN_W_C-1:0]     txs_wr_addr_o,    //! byte offset within the slot
    output logic                       txs_wr_valid_o,   //! byte-write strobe
    output logic [7:0]                 txs_wr_data_o,    //! frame byte
    output logic                       txs_wr_commit_o,  //! mark ready-to-send
    output logic [TXS_LEN_W_C-1:0]     txs_wr_len_o,     //! committed length (60)

    //! ---- TX lane request (held until granted — KL_pp_tx_arbiter lane) -----
    output logic                       txreq_valid_o,    //! committed slot wants the wire
    output logic [TXS_SLOT_W_C-1:0]    txreq_slot_o,     //! committed tx-slot handle
    input  wire                        txreq_ready_i,    //! lane grant (one-cycle)

    //! ---- the allocator seam (KL_pp_maap_shim's exact processor face) ------
    input  wire                        alloc_req_valid_i,   //! ALLOC/RELEASE offered, held until ready
    output logic                       alloc_req_ready_o,   //! this engine accepts the request
    input  wire                        alloc_req_release_i, //! 0 = ALLOC_DA, 1 = RELEASE_DA
    input  wire  [SRC_W_C-1:0]         alloc_req_src_i,     //! source index of the request
    output logic                       alloc_rsp_valid_o,   //! exactly one response per accepted request
    output logic                       alloc_rsp_ok_o,      //! ALLOC_DA granted (ignored on RELEASE_DA)
    output logic [47:0]                alloc_rsp_da_o,      //! granted DA (valid with ok)
    output logic                       conflict_valid_o,    //! per-source conflict, held until acked
    output logic [SRC_W_C-1:0]         conflict_src_o,      //! the source being told
    input  wire                        conflict_ack_i,      //! processor took the event (combinational)

    //! ---- claim publication (KL_maap-compatible: substitution face) --------
    output logic [47:0]                addr_o,           //! claimed base DMAC (source 0)
    output logic                       addr_valid_o,     //! 1 = DEFEND state (claim probed + defended)
    output logic [1:0]                 state_o,          //! 0 INITIAL / 1 PROBE / 2 DEFEND
    output logic [7:0]                 conflicts_o,      //! re-address events (saturating)
    output logic [7:0]                 defends_o         //! DEFEND frames sent (saturating)
);

  // ------------------------------------------------------------- constants
  //! Table B.9: dynamic allocation pool = 91:E0:F0:00:00:00 + 16-bit offset,
  //! 0xFE00 addresses (offsets 0x0000..0xFDFF)
  localparam logic [31:0] POOL_HI_C     = 32'h91E0_F000;
  localparam logic [15:0] POOL_SIZE_C   = 16'hFE00;
  //! Table B.10: the one reserved multicast address MAAP frames are sent to
  localparam logic [47:0] MAAP_DST_C    = 48'h91E0_F000_FF00;
  localparam logic [15:0] ETHERTYPE_C   = 16'h22F0;
  localparam logic [7:0]  SUBTYPE_C     = 8'hFE;
  //! Table B.1 message types
  localparam logic [3:0]  MSG_PROBE_C    = 4'd1;
  localparam logic [3:0]  MSG_DEFEND_C   = 4'd2;
  localparam logic [3:0]  MSG_ANNOUNCE_C = 4'd3;
  //! B.2.3: current maap_version; B.2.1: control_data_length 16 in ALL frames
  localparam logic [4:0]  MAAP_VER_C    = 5'd1;
  localparam logic [10:0] MAAP_CDL_C    = 11'd16;
  //! Table B.8: MAAP_PROBE_RETRANSMITS
  localparam logic [1:0]  PROBE_RETX_C  = 2'd3;
  //! wire frame: 42 real bytes padded to the 60-byte Ethernet minimum
  localparam int unsigned FRAME_BYTES_C = 60;
  //! 08 §3 F08.2 PRNG kinds owned by this engine
  localparam logic [2:0]  KIND_PROBE_C    = 3'd5;  // 501..599 ms
  localparam logic [2:0]  KIND_ANNOUNCE_C = 3'd6;  // 30001..31999 ms
  localparam logic [2:0]  KIND_ADDR_C     = 3'd7;  // pool offset 0..0xFDFF

  // ------------------------------------------------------------ txn unpack
  pp_txn_t txn_in_w;
  assign txn_in_w = pp_txn_t'(txn_i);

  // --------------------------------------------------------- slice helpers
  //! MSB-first byte n of a 48/16-bit field (n = 0 is the wire-first byte)
  function automatic logic [7:0] byte48_f(input logic [47:0] v,
                                          input int unsigned n);
    logic [47:0] sh;
    sh = v >> (8 * (5 - n));
    return sh[7:0];
  endfunction

  function automatic logic [7:0] byte16_f(input logic [15:0] v,
                                          input int unsigned n);
    logic [15:0] sh;
    sh = v >> (8 * (1 - n));
    return sh[7:0];
  endfunction

  //! B.3.6.4: octet-wise REVERSE order — the least-significant wire octet
  //! becomes the most significant comparison octet
  function automatic logic [47:0] rev48_f(input logic [47:0] m);
    return {m[7:0], m[15:8], m[23:16], m[31:24], m[39:32], m[47:40]};
  endfunction

  // ------------------------------------------------------- protocol state
  //! Table B.6 states, encoded to match KL_maap's state_o for the
  //! mechanical substitution (0 idle/INITIAL, 1 PROBE, 2 announce/DEFEND)
  typedef enum logic [1:0] { P_INITIAL = 2'd0, P_PROBE = 2'd1,
                             P_DEFEND  = 2'd2 } pstate_e;
  pstate_e     pstate_r;
  logic [15:0] offset_r;       //! claimed pool offset (base = POOL_HI + offset)
  logic [1:0]  probe_left_r;   //! maap_probe_count (Table B.4)
  logic        seed_used_r;    //! footnote-a seed consumed this engage — also
                               //! the no-reuse-on-conflict guard: a Restart!
                               //! can only run after the first walk consumed
                               //! the seed, and only a Release!/engage fall
                               //! re-arms it, so a conflicted seed is never
                               //! probed again within one engagement
  logic [7:0]  conflicts_r;    //! re-address events (saturating)
  logic [7:0]  defends_r;      //! DEFENDs sent (saturating)

  assign state_o      = pstate_r;
  assign addr_o       = {POOL_HI_C, offset_r};
  assign addr_valid_o = (pstate_r == P_DEFEND);
  assign conflicts_o  = conflicts_r;
  assign defends_o    = defends_r;

  //! engage level: the machine exists only while it may transmit (B.3.5.9)
  logic eng_w, eng_q_r;
  assign eng_w = cfg_en_i && link_up_i && (cfg_count_i != 8'd0);

  // ------------------------------------------------- our claim, 49-bit ends
  //! 49-bit inclusive ends so start+count-1 can never wrap the compare
  logic [48:0] our_lo_w, our_hi_w;
  assign our_lo_w = {1'b0, POOL_HI_C, offset_r};
  assign our_hi_w = our_lo_w + {41'd0, cfg_count_i} - 49'd1;

  // ------------------------------------------------------- expiry latching
  //! two F08.4 slots: +0 probe_timer, +1 announce_timer. Expiries latch as
  //! pending work; an arm or cancel of the slot clears its pending expiry
  //! (the arm supersedes it — the timer service's own arm-wins rule).
  logic exp_probe_w, exp_ann_w;
  assign exp_probe_w = tmr_exp_valid_i
                       && (32'(tmr_exp_slot_i) == TMR_SLOT_BASE_P);
  assign exp_ann_w   = tmr_exp_valid_i
                       && (32'(tmr_exp_slot_i) == TMR_SLOT_BASE_P + 32'd1);

  logic pend_probe_exp_r, pend_ann_exp_r;

  // ------------------------------------------------------------ walker FSM
  typedef enum logic [3:0] {
    W_OFF      = 4'd0,   //! not engaged (protocol INITIAL)
    W_IDLE     = 4'd1,   //! engaged, claim walk parked or DEFEND steady
    W_ADDR     = 4'd2,   //! generate_address: kind-7 draw (or the seed)
    W_IVAL     = 4'd3,   //! Start probe/announce_timer: kind-5/6 draw + arm
    W_ALLOC    = 4'd4,   //! TX slot request
    W_GWAIT    = 4'd5,   //! TX slot grant wait (retry)
    W_WRITE    = 4'd6,   //! 60 frame bytes into the slot
    W_COMMIT   = 4'd7,   //! commit the slot
    W_LANE     = 4'd8,   //! txreq held until the lane grants
    W_POST     = 4'd9,   //! post-send bookkeeping (chain / park)
    W_RX       = 4'd10,  //! record latched: evaluate the Table B.7 row
    W_TEARDOWN = 4'd11   //! engage fell: cancel both slots, -> OFF
  } wstate_e;

  wstate_e    w_st_r;
  logic       ival_ann_r;      //! W_IVAL draws/arms the announce timer
  logic [3:0] send_msg_r;      //! frame being built (Table B.1 code)
  logic       chain_ann_r;     //! after this PROBE: probeCount! -> ANNOUNCE
  logic       teardown_ph_r;   //! W_TEARDOWN phase (0 = probe, 1 = announce)

  //! draw serializer state (one draw in flight, ADP's discipline)
  logic       draw_act_r;
  logic       draw_req_r;
  logic [2:0] draw_kind_r;

  //! TX builder state
  logic [TXS_SLOT_W_C-1:0] bld_slot_r;
  logic [5:0]              bld_idx_r;

  //! latched RX record fields (the validator's MAAP lanes, F03.4)
  logic [3:0]  rxm_msg_r;
  logic [47:0] rxm_sa_r;
  logic [47:0] rxm_req_start_r;
  logic [15:0] rxm_req_cnt_r;
  logic [47:0] rxm_conf_start_r;
  logic [15:0] rxm_conf_cnt_r;

  //! DEFEND response echo + computed overlap (B.3.6.6), latched at W_RX
  logic [47:0] def_da_r;         //! unicast destination = the probe's SA
  logic [47:0] def_req_start_r;  //! echoed requested_start_address
  logic [15:0] def_req_cnt_r;    //! echoed requested_count
  logic [47:0] def_conf_start_r; //! first allocated address in conflict
  logic [15:0] def_conf_cnt_r;   //! count of allocated addresses in conflict

  // --------------------------------------------- conflict math (comb, W_RX)
  logic [48:0] req_lo_w, req_hi_w, conf_lo_w, conf_hi_w;
  logic        ovl_req_w, ovl_conf_w;

  assign req_lo_w  = {1'b0, rxm_req_start_r};
  assign req_hi_w  = req_lo_w + {33'd0, rxm_req_cnt_r} - 49'd1;
  assign conf_lo_w = {1'b0, rxm_conf_start_r};
  assign conf_hi_w = conf_lo_w + {33'd0, rxm_conf_cnt_r} - 49'd1;

  //! footnote b overlap; an empty range (count 0) never conflicts
  assign ovl_req_w  = (rxm_req_cnt_r != 16'd0)
                      && (req_lo_w <= our_hi_w) && (our_lo_w <= req_hi_w);
  assign ovl_conf_w = (rxm_conf_cnt_r != 16'd0)
                      && (conf_lo_w <= our_hi_w) && (our_lo_w <= conf_hi_w);

  //! compare_MAC returns TRUE = we are numerically lower (reversed octets)
  //! = no further processing (footnote d)
  logic cmp_mac_true_w;
  assign cmp_mac_true_w = rev48_f(own_mac_i) < rev48_f(rxm_sa_r);

  //! B.3.6.6 conflict fields: intersection of OUR block with the requested
  //! range (only evaluated when ovl_req_w holds, i.e. non-empty)
  logic [48:0] isect_lo_w, isect_hi_w;
  assign isect_lo_w = (req_lo_w > our_lo_w) ? req_lo_w : our_lo_w;
  assign isect_hi_w = (req_hi_w < our_hi_w) ? req_hi_w : our_hi_w;

  //! the Table B.7 row decode for the latched record (valid in W_RX)
  logic ev_hit_w;      //! footnote b: some contained range overlaps ours
  logic act_defend_w;  //! DEFEND-state rProbe!: sDefend
  logic act_yield_w;   //! Stop timer(s), INITIAL/Restart!

  always_comb begin : row_decode
    ev_hit_w     = 1'b0;
    act_defend_w = 1'b0;
    act_yield_w  = 1'b0;
    if (rxm_msg_r == MSG_PROBE_C) begin
      ev_hit_w = ovl_req_w;
      if (ev_hit_w && (pstate_r == P_PROBE)) begin
        act_yield_w = !cmp_mac_true_w;          // tie-break only in PROBE
      end else if (ev_hit_w && (pstate_r == P_DEFEND)) begin
        act_defend_w = 1'b1;                    // always defended (no tie-break)
      end
    end else if ((rxm_msg_r == MSG_DEFEND_C)
                 || (rxm_msg_r == MSG_ANNOUNCE_C)) begin
      ev_hit_w = ovl_req_w || ovl_conf_w;
      if (ev_hit_w && (pstate_r == P_PROBE)) begin
        act_yield_w = 1'b1;                     // no tie-break in PROBE
      end else if (ev_hit_w && (pstate_r == P_DEFEND)) begin
        act_yield_w = !cmp_mac_true_w;          // tie-break in DEFEND
      end
    end
    // reserved message_types: ignored (B.2.2)
  end : row_decode

  // ------------------------------------------------------------- TX frame
  //! Figure B.1, byte-exact; bytes 42..59 are the Ethernet minimum padding
  function automatic logic [7:0] frame_byte_f(
      input logic [5:0]  idx,
      input logic [3:0]  msg,
      input logic [15:0] off,
      input logic [7:0]  cnt,
      input logic [47:0] dda,
      input logic [47:0] ereq_s, input logic [15:0] ereq_c,
      input logic [47:0] econ_s, input logic [15:0] econ_c);
    int unsigned i;
    logic [7:0]  b;
    logic        dfd;
    logic [47:0] req_s;
    logic [15:0] req_c;
    i     = 32'(idx);
    dfd   = (msg == MSG_DEFEND_C);
    req_s = dfd ? ereq_s : {POOL_HI_C, off};
    req_c = dfd ? ereq_c : {8'd0, cnt};
    b     = 8'h00;
    if (i < 6)        b = byte48_f(dfd ? dda : MAAP_DST_C, i);   // DA @0
    else if (i < 12)  b = byte48_f(own_mac_i, i - 6);            // SA @6
    else if (i < 14)  b = byte16_f(ETHERTYPE_C, i - 12);         // @12
    else if (i == 14) b = SUBTYPE_C;                             // subtype
    else if (i == 15) b = {4'b0000, msg};                        // sv/ver/msg
    else if (i == 16) b = {MAAP_VER_C, MAAP_CDL_C[10:8]};        // 0x08
    else if (i == 17) b = MAAP_CDL_C[7:0];                       // cdl = 16
    // stream_id @18..25 = 0 (B.2.4)
    else if (i >= 26 && i < 32) b = byte48_f(req_s, i - 26);     // req start
    else if (i >= 32 && i < 34) b = byte16_f(req_c, i - 32);     // req count
    else if (dfd && i >= 34 && i < 40) b = byte48_f(econ_s, i - 34);
    else if (dfd && i >= 40 && i < 42) b = byte16_f(econ_c, i - 40);
    // conflict fields 0 in PROBE/ANNOUNCE (B.2.7/B.2.8); padding 0
    return b;
  endfunction

  assign txs_wr_slot_o  = bld_slot_r;
  assign txs_wr_addr_o  = TXS_LEN_W_C'(bld_idx_r);
  assign txs_wr_valid_o = (w_st_r == W_WRITE);
  assign txs_wr_data_o  = frame_byte_f(bld_idx_r, send_msg_r, offset_r,
                                       cfg_count_i, def_da_r,
                                       def_req_start_r, def_req_cnt_r,
                                       def_conf_start_r, def_conf_cnt_r);
  assign txs_wr_commit_o = (w_st_r == W_COMMIT);
  assign txs_wr_len_o    = TXS_LEN_W_C'(FRAME_BYTES_C);
  assign txs_alloc_req_o = (w_st_r == W_ALLOC);
  assign txs_oversize_o  = 1'b0;
  assign txreq_valid_o   = (w_st_r == W_LANE);
  assign txreq_slot_o    = bld_slot_r;

  // ------------------------------------------------------------ the walker
  //! one timer arm/cancel strobe at a time; registered outputs
  logic                 arm_v_r, arm_c_r;
  logic                 arm_ann_r;
  logic [31:0]          arm_dl_r;

  assign tmr_arm_valid_o       = arm_v_r;
  assign tmr_arm_cancel_o      = arm_c_r;
  assign tmr_arm_slot_o        = TMR_AW_C'(TMR_SLOT_BASE_P
                                           + (arm_ann_r ? 32'd1 : 32'd0));
  assign tmr_arm_owner_o       = TMR_OWNER_BASE_P
                                 + {7'd0, arm_ann_r};
  assign tmr_arm_deadline_ms_o = arm_dl_r;

  assign prng_draw_req_o  = draw_req_r;
  assign prng_draw_kind_o = draw_kind_r;

  //! the record is consumed (and its slot freed) in the accept cycle. W_OFF
  //! consumes too: a disabled engine that stopped popping would fill its
  //! dispatch queue with the network's routine ANNOUNCEs and wedge the
  //! SHARED normalizer head behind it — the record is dropped (Table B.7
  //! INITIAL ignores every rX!) but the pipeline keeps moving. A NULL or
  //! out-of-pool handle frees nothing (TIMER/SELF records).
  assign txn_ready_o     = ((w_st_r == W_IDLE) || (w_st_r == W_OFF))
                           && txn_valid_i;
  assign rxs_free_o      = txn_ready_o && (txn_in_w.rx_slot != PP_SLOT_NULL_C)
                           && (32'(txn_in_w.rx_slot) < RX_SLOTS_P);
  assign rxs_free_slot_o = txn_in_w.rx_slot;

  always_ff @(posedge clk_i) begin : walker
    if (!rst_n) begin
      pstate_r         <= P_INITIAL;
      offset_r         <= 16'd0;
      probe_left_r     <= 2'd0;
      seed_used_r      <= 1'b0;
      conflicts_r      <= 8'd0;
      defends_r        <= 8'd0;
      eng_q_r          <= 1'b0;
      pend_probe_exp_r <= 1'b0;
      pend_ann_exp_r   <= 1'b0;
      w_st_r           <= W_OFF;
      ival_ann_r       <= 1'b0;
      send_msg_r       <= 4'd0;
      chain_ann_r      <= 1'b0;
      teardown_ph_r    <= 1'b0;
      draw_act_r       <= 1'b0;
      draw_req_r       <= 1'b0;
      draw_kind_r      <= 3'd0;
      bld_slot_r       <= '0;
      bld_idx_r        <= 6'd0;
      rxm_msg_r        <= 4'd0;
      rxm_sa_r         <= 48'd0;
      rxm_req_start_r  <= 48'd0;
      rxm_req_cnt_r    <= 16'd0;
      rxm_conf_start_r <= 48'd0;
      rxm_conf_cnt_r   <= 16'd0;
      def_da_r         <= 48'd0;
      def_req_start_r  <= 48'd0;
      def_req_cnt_r    <= 16'd0;
      def_conf_start_r <= 48'd0;
      def_conf_cnt_r   <= 16'd0;
      arm_v_r          <= 1'b0;
      arm_c_r          <= 1'b0;
      arm_ann_r        <= 1'b0;
      arm_dl_r         <= 32'd0;
    end else begin
      // one-cycle pulses fall
      arm_v_r    <= 1'b0;
      draw_req_r <= 1'b0;
      eng_q_r    <= eng_w;

      // expiry latches (the walker may be mid-flow); an arm/cancel of the
      // slot below clears the matching latch in the same block
      if (exp_probe_w) pend_probe_exp_r <= 1'b1;
      if (exp_ann_w)   pend_ann_exp_r   <= 1'b1;

      unique case (w_st_r)
        // ---- not engaged: Release!/link-down parks the machine ----------
        W_OFF: begin
          pstate_r <= P_INITIAL;
          if (eng_w && !eng_q_r) begin
            // Begin!/PortOperational!: generate_address + ReserveAddress!
            w_st_r <= W_ADDR;
          end
        end

        // ---- generate_address (B.3.6.1) ---------------------------------
        W_ADDR: begin
          if (!eng_w) begin
            w_st_r <= W_OFF;                       // nothing armed yet
          end else if (cfg_seed_valid_i && !seed_used_r) begin
            // footnote a: a provisioned range skips generate_address; the
            // clamp keeps a mis-provisioned block inside the pool
            offset_r <= (cfg_seed_offset_i > (POOL_SIZE_C - {8'd0, cfg_count_i}))
                        ? (POOL_SIZE_C - {8'd0, cfg_count_i})
                        : cfg_seed_offset_i;
            seed_used_r  <= 1'b1;
            probe_left_r <= PROBE_RETX_C;          // init_maap_probe_count
            ival_ann_r   <= 1'b0;
            w_st_r       <= W_IVAL;
          end else if (draw_act_r) begin
            if (prng_draw_valid_i) begin
              draw_act_r <= 1'b0;
              // rejection keeps the draw uniform over the offsets the whole
              // block fits at (B.3.6.1 uniform-distribution rule): a raw
              // clamp would pile the top counts onto one offset
              if (prng_draw_ms_i <= (POOL_SIZE_C - {8'd0, cfg_count_i})) begin
                offset_r     <= prng_draw_ms_i;
                probe_left_r <= PROBE_RETX_C;      // init_maap_probe_count
                ival_ann_r   <= 1'b0;
                w_st_r       <= W_IVAL;
              end
              // else: redraw (stay in W_ADDR)
            end
          end else if (!prng_draw_busy_i && !draw_req_r) begin
            draw_req_r  <= 1'b1;
            draw_kind_r <= KIND_ADDR_C;
            draw_act_r  <= 1'b1;
          end
        end

        // ---- Start probe/announce_timer with a fresh random period ------
        W_IVAL: begin
          if (draw_act_r) begin
            if (prng_draw_valid_i) begin
              draw_act_r <= 1'b0;
              arm_v_r    <= 1'b1;
              arm_c_r    <= 1'b0;
              arm_ann_r  <= ival_ann_r;
              arm_dl_r   <= now_ms_i + {16'd0, prng_draw_ms_i};
              if (ival_ann_r) begin
                pend_ann_exp_r <= 1'b0;            // arm supersedes a stale expiry
                send_msg_r     <= MSG_ANNOUNCE_C;  // sAnnounce
              end else begin
                pend_probe_exp_r <= 1'b0;
                send_msg_r       <= MSG_PROBE_C;   // sProbe
              end
              w_st_r <= W_ALLOC;
            end
          end else if (!prng_draw_busy_i && !draw_req_r) begin
            draw_req_r  <= 1'b1;
            draw_kind_r <= ival_ann_r ? KIND_ANNOUNCE_C : KIND_PROBE_C;
            draw_act_r  <= 1'b1;
          end
        end

        // ---- TX: alloc -> write -> commit -> lane -----------------------
        W_ALLOC:  w_st_r <= W_GWAIT;
        W_GWAIT: begin
          if (txs_alloc_gnt_i) begin
            bld_slot_r <= txs_alloc_slot_i;
            bld_idx_r  <= 6'd0;
            w_st_r     <= W_WRITE;
          end else begin
            w_st_r <= W_ALLOC;                     // pool busy: retry
          end
        end
        W_WRITE: begin
          if (32'(bld_idx_r) == FRAME_BYTES_C - 1) begin
            w_st_r <= W_COMMIT;
          end else begin
            bld_idx_r <= bld_idx_r + 6'd1;
          end
        end
        W_COMMIT: w_st_r <= W_LANE;
        W_LANE: begin
          if (txreq_ready_i) begin
            w_st_r <= W_POST;
          end
        end

        // ---- post-send bookkeeping (the rest of the Table B.7 cell) -----
        W_POST: begin
          w_st_r <= W_IDLE;
          if (send_msg_r == MSG_PROBE_C) begin
            if (pstate_r != P_PROBE) begin
              pstate_r <= P_PROBE;                 // ReserveAddress! -> PROBE
            end
            if (chain_ann_r) begin
              // probeCount! (B.3.5.8): Stop probe_timer (never re-armed),
              // Start announce_timer, sAnnounce, -> DEFEND
              chain_ann_r <= 1'b0;
              ival_ann_r  <= 1'b1;
              w_st_r      <= W_IVAL;
            end
          end else if (send_msg_r == MSG_ANNOUNCE_C) begin
            pstate_r <= P_DEFEND;                  // (re)entered with each announce arm
          end
          // a DEFEND changes no state and no timer
        end

        // ---- engaged steady state: field work ---------------------------
        W_IDLE: begin
          if (!eng_w) begin
            // Release!/PortOperational-loss: Stop timers, INITIAL, no PDU
            pstate_r      <= P_INITIAL;
            seed_used_r   <= 1'b0;                 // re-arm the footnote-a seed
            teardown_ph_r <= 1'b0;
            w_st_r        <= W_TEARDOWN;
          end else if (txn_valid_i) begin
            // latch the record's MAAP lanes; slot freed by txn_ready_o
            rxm_msg_r        <= txn_in_w.msg_type;
            rxm_sa_r         <= txn_in_w.src_mac;
            rxm_req_start_r  <= txn_in_w.controller_eid[63:16];
            rxm_req_cnt_r    <= txn_in_w.controller_eid[15:0];
            rxm_conf_start_r <= {txn_in_w.operands.desc_type,
                                 txn_in_w.operands.desc_index,
                                 txn_in_w.operands.config_index};
            rxm_conf_cnt_r   <= txn_in_w.operands.unique_id;
            w_st_r           <= W_RX;
          end else if (pend_probe_exp_r) begin
            pend_probe_exp_r <= 1'b0;
            // probetimer! is meaningful in PROBE only (Table B.7 -x- rows)
            if (pstate_r == P_PROBE) begin
              if (probe_left_r == 2'd1) begin
                chain_ann_r <= 1'b1;               // this send exhausts the count
              end
              probe_left_r <= probe_left_r - 2'd1; // dec_maap_probe_count
              if (probe_left_r == 2'd1) begin
                // probe_timer would be started then stopped by probeCount!:
                // net stopped — skip the re-arm and send straight away
                send_msg_r <= MSG_PROBE_C;
                w_st_r     <= W_ALLOC;
              end else begin
                ival_ann_r <= 1'b0;                // Start probe_timer + sProbe
                w_st_r     <= W_IVAL;
              end
            end
          end else if (pend_ann_exp_r) begin
            pend_ann_exp_r <= 1'b0;
            // announcetimer! is meaningful in DEFEND only
            if (pstate_r == P_DEFEND) begin
              ival_ann_r <= 1'b1;                  // Start announce_timer + sAnnounce
              w_st_r     <= W_IVAL;
            end
          end else if (pstate_r == P_INITIAL) begin
            // an engage rise landed while the walker was busy elsewhere:
            // the claim walk still owes its start
            w_st_r <= W_ADDR;
          end
        end

        // ---- the Table B.7 row for one received PDU ---------------------
        W_RX: begin
          w_st_r <= W_IDLE;
          if ((pstate_r != P_INITIAL) && eng_w) begin
            if (act_defend_w) begin
              // sDefend (B.3.6.6): echo the probe's requested_*, conflict_*
              // = our overlapping sub-range, unicast to the probe's SA
              def_da_r         <= rxm_sa_r;
              def_req_start_r  <= rxm_req_start_r;
              def_req_cnt_r    <= rxm_req_cnt_r;
              def_conf_start_r <= isect_lo_w[47:0];
              def_conf_cnt_r   <= 16'(isect_hi_w - isect_lo_w) + 16'd1;
              defends_r        <= (&defends_r) ? defends_r
                                               : defends_r + 8'd1;
              send_msg_r       <= MSG_DEFEND_C;
              w_st_r           <= W_ALLOC;
            end else if (act_yield_w) begin
              // Stop the running timer, INITIAL/Restart! with a FRESH range
              arm_v_r     <= 1'b1;
              arm_c_r     <= 1'b1;
              arm_ann_r   <= (pstate_r == P_DEFEND);
              if (pstate_r == P_DEFEND) pend_ann_exp_r <= 1'b0;
              else                      pend_probe_exp_r <= 1'b0;
              pstate_r    <= P_INITIAL;
              conflicts_r <= (&conflicts_r) ? conflicts_r
                                            : conflicts_r + 8'd1;
              w_st_r      <= W_ADDR;
            end
          end
        end

        // ---- two-cycle teardown: cancel probe, then announce ------------
        W_TEARDOWN: begin
          arm_v_r       <= 1'b1;
          arm_c_r       <= 1'b1;
          arm_ann_r     <= teardown_ph_r;
          teardown_ph_r <= 1'b1;
          if (!teardown_ph_r) begin
            pend_probe_exp_r <= 1'b0;
          end else begin
            pend_ann_exp_r <= 1'b0;
            w_st_r         <= W_OFF;
          end
        end

        default: w_st_r <= W_OFF;
      endcase
    end
  end : walker

  // ======================================================================= //
  //  The allocator seam — KL_pp_maap_shim's logic, inherited verbatim       //
  //  (decisions 1..5 of its banner; see this file's banner for the list)    //
  // ======================================================================= //
  logic [7:0] src8_w;
  assign src8_w = 8'(alloc_req_src_i);

  logic in_block_w;
  assign in_block_w = addr_valid_o && (src8_w < cfg_count_i);

  //! DA = base + s on the 16-bit offset half only: the claim clamp keeps
  //! offset + s inside 0x0000..0xFDFF for every s < cfg_count_i, so a grant
  //! structurally cannot leave the pool or carry into the 91:E0:F0 prefix
  logic [15:0] grant_off_w;
  logic [47:0] grant_da_w;
  assign grant_off_w = offset_r + {{(16-SRC_W_C){1'b0}}, alloc_req_src_i};
  assign grant_da_w  = {POOL_HI_C, grant_off_w};

  assign alloc_req_ready_o = ~alloc_rsp_valid_o;

  logic        rsp_valid_r, rsp_ok_r;
  logic [47:0] rsp_da_r;
  assign alloc_rsp_valid_o = rsp_valid_r;
  assign alloc_rsp_ok_o    = rsp_ok_r;
  assign alloc_rsp_da_o    = rsp_da_r;

  logic grant_w;
  assign grant_w = ~alloc_req_release_i & in_block_w;

  always_ff @(posedge clk_i) begin : rsp_path
    if (!rst_n) begin
      rsp_valid_r <= 1'b0;
      rsp_ok_r    <= 1'b0;
      rsp_da_r    <= 48'd0;
    end else begin
      rsp_valid_r <= 1'b0;
      if (alloc_req_valid_i & alloc_req_ready_o) begin
        rsp_valid_r <= 1'b1;
        rsp_ok_r    <= grant_w;
        rsp_da_r    <= grant_w ? grant_da_w : 48'd0;
      end
    end
  end : rsp_path

  // ---- block-move detector -> per-source conflict fan-out ----------------
  logic        blk_valid_q_r;
  logic [15:0] blk_off_q_r;
  logic [7:0]  blk_cnt_q_r;

  logic moved_w;
  assign moved_w = blk_valid_q_r
                   && (!addr_valid_o
                       || (offset_r    != blk_off_q_r)
                       || (cfg_count_i != blk_cnt_q_r));

  logic [N_SRC_P-1:0] confl_pend_r;
  assign conflict_valid_o = |confl_pend_r;

  //! lowest pending source first (descending sweep, last write wins)
  always_comb begin : confl_pick
    conflict_src_o = '0;
    for (int unsigned i = N_SRC_P; i > 0; i--) begin
      if (confl_pend_r[i-1]) conflict_src_o = SRC_W_C'(i - 1);
    end
  end : confl_pick

  always_ff @(posedge clk_i) begin : confl_path
    if (!rst_n) begin
      blk_valid_q_r <= 1'b0;
      blk_off_q_r   <= 16'd0;
      blk_cnt_q_r   <= 8'd0;
      confl_pend_r  <= '0;
    end else begin
      blk_valid_q_r <= addr_valid_o;
      blk_off_q_r   <= offset_r;
      blk_cnt_q_r   <= cfg_count_i;
      //! a fresh move supersedes an in-flight sweep: every source must hear
      //! about the LATEST move, including one already acked for the previous
      if (moved_w) begin
        confl_pend_r <= '1;
      end else if (conflict_valid_o & conflict_ack_i) begin
        confl_pend_r[conflict_src_o] <= 1'b0;
      end
    end
  end : confl_path

  //! the expiry owner tag is decoded by slot in this engine; referenced so
  //! the port is not dangling in lint
  logic unused_owner_w;
  assign unused_owner_w = ^tmr_exp_owner_i;

endmodule : KL_pp_maap
`default_nettype wire
