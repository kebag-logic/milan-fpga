/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_scoreboard.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/03 §6
//                F03.7 hazard classes + ordering rules (a)/(e); 06 §8
//                FAIL_SAFE pairing)
//
//  Description : Cross-engine admission control over the NINE hazard classes
//                of pp_pkg (03 §6). A transaction presents {class, key};
//                the grant is combinational against the registered hold set
//                and allocates one entry of a MAX_HOLDS_P-deep table. The
//                F03.7 matrix, as encoded here (symmetric, precedence top
//                to bottom):
//                  1. CFG_BARRIER conflicts with EVERYTHING, itself
//                     included (global drain). A refused CFG_BARRIER
//                     request latches barrier_pend_r: all non-barrier
//                     admission is then refused until the barrier grants
//                     on an empty table ("drain all in-flight, block
//                     admission, then execute").
//                  2. RO_SNAPSHOT admits in parallel with itself (any
//                     key); vs any other class (all are writes) it
//                     conflicts only on the same key.
//                  3. LOCK_OP is global vs every lock-protected member
//                     (CFG_BARRIER, STREAM_CFG, MAP_CFG, CLOCK_CFG,
//                     NAME_WR, IDENTIFY — the F06.14 lock column) and
//                     itself; REGISTRY_OP is not lock-protected.
//                  4. Same class: REGISTRY_OP and IDENTIFY serialize
//                     key-independently (single resource); STREAM_CFG,
//                     MAP_CFG, CLOCK_CFG, NAME_WR serialize per key.
//                  5. MAP_CFG and STREAM_CFG cross-lock (the
//                     format<->mapping validation pair).
//                  6. Every other cross pair touches disjoint resources:
//                     no conflict.
//                Releases: the normal release (rule (a): after the
//                solicited-response enqueue) frees by hold id. The rule (e)
//                deadline-kill release is honored ONLY while the paired
//                response-queued flag is asserted — the key is released
//                only after the FAIL_SAFE response is queued (06 §8), never
//                on the kill alone. Releases land on the clock edge; a
//                grant in the same cycle is evaluated against the
//                PRE-release hold set (race-free, one cycle of latency to
//                reuse a freed key).
//
//                The one design decision that matters: the doc's MAP_CFG
//                row cross-locks "with STREAM_CFG of referenced streams",
//                but this port carries ONE {class, key} per transaction —
//                a mapping op referencing several streams cannot present a
//                key set. The cross-lock is therefore CLASS-WIDE
//                (MAP_CFG vs any STREAM_CFG holder, key ignored): a strict
//                superset of the doc's serialization — conservative, never
//                admits a forbidden pair, only over-serializes the
//                format<->mapping path.
//
//                Storage note: the holds table is deliberately FLOPS
//                (MAX_HOLDS_P x 20 b) with parallel conflict comparators —
//                it is CAM-shaped (every admission compares against every
//                live hold in the same cycle), so the RAM-inference rule
//                does not apply; there is no wide read mux, only the
//                per-entry match term.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_scoreboard #(
    //! holds-table depth — bounds concurrently-admitted transactions
    //! (in-flight <= P-RX-SLOTS + queue depths, 03 §4)
    parameter int unsigned MAX_HOLDS_P = 8,
    //! derived hold-id width — do not override
    localparam int unsigned ID_W_C = (MAX_HOLDS_P > 32'd1) ? $clog2(MAX_HOLDS_P)
                                                           : 32'd1
) (
    input  wire                    clk_i,              //! core clock (P-CLK-HZ domain)
    input  wire                    rst_n,              //! synchronous active-low reset

    //! ---- admission port (dispatch side) ----
    input  wire                    adm_req_i,          //! admission request
    input  wire             [3:0]  adm_class_i,        //! pp_pkg::pp_hazard_e of the transaction
    input  wire             [15:0] adm_key_i,          //! serialization key within the class
    output logic                   adm_gnt_o,          //! combinational grant (same cycle)
    output logic      [ID_W_C-1:0] adm_id_o,           //! hold id (valid with gnt; quote it to release)

    //! ---- normal release (rule (a): after solicited-response enqueue) ----
    input  wire                    rel_valid_i,        //! release strobe
    input  wire       [ID_W_C-1:0] rel_id_i,           //! hold id from the grant (non-held id = no-op)

    //! ---- rule (e) deadline-kill release (06 §8 forced respond) ----
    input  wire                    kill_valid_i,       //! deadline-kill release strobe
    input  wire       [ID_W_C-1:0] kill_id_i,          //! hold id to kill
    input  wire                    kill_resp_queued_i, //! FAIL_SAFE response is queued — kill honored only with this
    output logic                   kill_ack_o,         //! kill honored this cycle (combinational)

    //! ---- observability ----
    output logic [MAX_HOLDS_P-1:0] holds_o,            //! live-hold mask
    output logic                   full_o,             //! table full (grant impossible)
    output logic                   barrier_pend_o      //! CFG_BARRIER drain in progress
);

  // ---- hazard-class codes, from the single source (pp_pkg, 03 §6) --------
  localparam logic [3:0] HZ_RO_SNAPSHOT_C = pp_pkg::PP_HZ_RO_SNAPSHOT;
  localparam logic [3:0] HZ_CFG_BARRIER_C = pp_pkg::PP_HZ_CFG_BARRIER;
  localparam logic [3:0] HZ_STREAM_CFG_C  = pp_pkg::PP_HZ_STREAM_CFG;
  localparam logic [3:0] HZ_MAP_CFG_C     = pp_pkg::PP_HZ_MAP_CFG;
  localparam logic [3:0] HZ_CLOCK_CFG_C   = pp_pkg::PP_HZ_CLOCK_CFG;
  localparam logic [3:0] HZ_NAME_WR_C     = pp_pkg::PP_HZ_NAME_WR;
  localparam logic [3:0] HZ_LOCK_OP_C     = pp_pkg::PP_HZ_LOCK_OP;
  localparam logic [3:0] HZ_REGISTRY_OP_C = pp_pkg::PP_HZ_REGISTRY_OP;
  localparam logic [3:0] HZ_IDENTIFY_C    = pp_pkg::PP_HZ_IDENTIFY;

  // ---- the F06.14 lock-protected set (LOCK_OP row of F03.7) --------------
  function automatic logic hz_is_lockprot(input logic [3:0] c);
    return (c == HZ_CFG_BARRIER_C) || (c == HZ_STREAM_CFG_C)
        || (c == HZ_MAP_CFG_C)     || (c == HZ_CLOCK_CFG_C)
        || (c == HZ_NAME_WR_C)     || (c == HZ_IDENTIFY_C);
  endfunction

  // ---- the F03.7 conflict matrix (symmetric; precedence = banner order) --
  function automatic logic hz_conflict(
      input logic [3:0]  a_cls,
      input logic [15:0] a_key,
      input logic [3:0]  b_cls,
      input logic [15:0] b_key
  );
    logic       same_key_v;
    logic [3:0] other_v;
    same_key_v = (a_key == b_key);
    other_v    = (a_cls == HZ_LOCK_OP_C) ? b_cls : a_cls;
    // (1) CFG_BARRIER excludes everything, itself included (global drain)
    if ((a_cls == HZ_CFG_BARRIER_C) || (b_cls == HZ_CFG_BARRIER_C)) begin
      return 1'b1;
    end
    // (2) RO_SNAPSHOT: reads parallel; blocked only vs same-key write
    if ((a_cls == HZ_RO_SNAPSHOT_C) && (b_cls == HZ_RO_SNAPSHOT_C)) begin
      return 1'b0;
    end
    if ((a_cls == HZ_RO_SNAPSHOT_C) || (b_cls == HZ_RO_SNAPSHOT_C)) begin
      return same_key_v;
    end
    // (3) LOCK_OP: global vs every lock-protected member + itself
    if ((a_cls == HZ_LOCK_OP_C) || (b_cls == HZ_LOCK_OP_C)) begin
      return (other_v == HZ_LOCK_OP_C) || hz_is_lockprot(other_v);
    end
    // (4) same class: registry/identify are single resources, rest per key
    if (a_cls == b_cls) begin
      if ((a_cls == HZ_REGISTRY_OP_C) || (a_cls == HZ_IDENTIFY_C)) begin
        return 1'b1;
      end
      return same_key_v;
    end
    // (5) MAP_CFG cross-locked with STREAM_CFG (class-wide, see banner)
    if (((a_cls == HZ_STREAM_CFG_C) && (b_cls == HZ_MAP_CFG_C))
     || ((a_cls == HZ_MAP_CFG_C)   && (b_cls == HZ_STREAM_CFG_C))) begin
      return 1'b1;  // format<->mapping validation pair
    end
    // (6) disjoint resources
    return 1'b0;
  endfunction

  // ------------------------------------------------------------ hold table
  // CAM-shaped: flops + parallel comparators (see banner storage note).
  logic [MAX_HOLDS_P-1:0] valid_r;
  logic [3:0]             cls_r [0:MAX_HOLDS_P-1];
  logic [15:0]            key_r [0:MAX_HOLDS_P-1];
  logic                   barrier_pend_r;

  // ------------------------------------------------------- conflict scan
  logic conflict_any_w;

  always_comb begin : conflict_scan
    conflict_any_w = 1'b0;
    for (int unsigned i = 0; i < MAX_HOLDS_P; i++) begin
      if (valid_r[i]
          && hz_conflict(adm_class_i, adm_key_i, cls_r[i], key_r[i])) begin
        conflict_any_w = 1'b1;
      end
    end
  end

  // ---------------------------------------------------- lowest-free entry
  logic              ff_valid_w;
  logic [ID_W_C-1:0] ff_id_w;

  always_comb begin : first_free
    ff_valid_w = 1'b0;
    ff_id_w    = '0;
    for (int unsigned i = 0; i < MAX_HOLDS_P; i++) begin
      if (!ff_valid_w && !valid_r[i]) begin
        ff_valid_w = 1'b1;
        ff_id_w    = ID_W_C'(i);
      end
    end
  end

  // ------------------------------------------------------------ admission
  logic adm_is_barrier_w;

  assign adm_is_barrier_w = (adm_class_i == HZ_CFG_BARRIER_C);
  assign adm_gnt_o = adm_req_i && ff_valid_w && !conflict_any_w
                     && (adm_is_barrier_w || !barrier_pend_r);
  assign adm_id_o  = ff_id_w;

  // rule (e): the kill is honored ONLY once the FAIL_SAFE response is queued
  assign kill_ack_o = kill_valid_i && kill_resp_queued_i && valid_r[kill_id_i];

  assign holds_o        = valid_r;
  assign full_o         = !ff_valid_w;
  assign barrier_pend_o = barrier_pend_r;

  // ------------------------------------------------------- state update
  // Grant targets a free entry, releases target valid entries: the write
  // sets are disjoint by construction, so one process needs no priority.
  always_ff @(posedge clk_i) begin : holds_table
    if (!rst_n) begin
      valid_r        <= '0;
      barrier_pend_r <= 1'b0;
      for (int unsigned i = 0; i < MAX_HOLDS_P; i++) begin
        cls_r[i] <= 4'd0;
        key_r[i] <= 16'd0;
      end
    end else begin
      if (rel_valid_i && valid_r[rel_id_i]) begin
        valid_r[rel_id_i] <= 1'b0;
      end
      if (kill_ack_o) begin
        valid_r[kill_id_i] <= 1'b0;
      end
      if (adm_gnt_o) begin
        valid_r[ff_id_w] <= 1'b1;
        cls_r[ff_id_w]   <= adm_class_i;
        key_r[ff_id_w]   <= adm_key_i;
      end
      // a refused CFG_BARRIER latches the drain; the grant clears it
      if (adm_req_i && adm_is_barrier_w) begin
        barrier_pend_r <= !adm_gnt_o;
      end
    end
  end

endmodule : KL_pp_scoreboard
`default_nettype wire
