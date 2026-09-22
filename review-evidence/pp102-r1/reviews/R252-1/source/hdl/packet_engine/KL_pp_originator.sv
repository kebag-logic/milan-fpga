/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_originator.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/03 §5 originator + inflight table,
//                 03 §3 rules V6/V7 response routing, 05 §6.4 A13
//                 exact-duplicate retry, 08 §2 T-ACMP-CMD / T-AECP-TIMEOUT
//                 owners, 09 §3 F09.4 mismatched-response tolerance row)
//
//  Description : Single service point for entity-initiated command PDUs
//                (ACMP PROBE_TX, AECP CONTROLLER_AVAILABLE). The issuing
//                engine serializes the PDU into a KL_pp_tx_slots slot and
//                hands the handle here; the originator assigns sequence_id
//                from a per-owner counter (iss_seq_o previews the value so
//                the engine writes it into the PDU bytes before issuing),
//                HOLDS the slot across the exchange (hold/release pair
//                toward the pool — the pool must not auto-free it on eof),
//                requests the send, and arms the owner-provided timer slot
//                only after the serializer accepts that slot. Responses
//                are matched on {key, seq} against the inflight table
//                {owner, key, seq, timer-slot, timeout, tx-slot, retried}:
//                hit -> route to owner + timer disarm + slot release; no
//                match -> SILENTLY ignored but counted (8-bit, F09.4).
//                First expiry -> ONE re-send request of the SAME held slot
//                (bytes unchanged: Milan's exact duplicate, same seq); the
//                timer re-arms only when that retry reaches the serializer.
//                Second expiry -> fail to owner + release. IEEE's
//                one-retry rule is thereby central, never per-engine
//                (IEEE §9.3.6.1.2, §8.2.2.1.5). Timeout values arrive on
//                the issue port — 08 F08.1 stays the single source, no
//                T-constant is restated here.
//
//  Decision    : the design decision that matters — the inflight table is
//                a small flop CAM (INFLIGHT_P <= 16), never a RAM: the
//                response match must compare {key, seq} against every
//                live entry in one cycle, which a sync-read RAM cannot do
//                without a multi-cycle search FSM; at <= 16 x ~60 b the
//                flops are cheaper than that FSM. The timer owner tag
//                encodes {TMR_TAG_P, entry index} so expiry routing back
//                into the table is O(1), and every shared one-op-per-cycle
//                resource (timer arm port, hold/release, send lanes) is
//                serialized to ONE event per cycle. Non-backpressurable
//                cancellation, serializer acceptance, and expiry inputs are
//                parked per entry before the priority chain; issue is the only
//                backpressurable input. The pending masks are overflow-free
//                because each bit names its live inflight entry.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_originator #(
    //! P-CA-POOL (F01.5 default 4): CONTROLLER_AVAILABLE inflight share
    parameter int unsigned CA_POOL_P     = 4,
    //! probe share: one inflight per sink SM (F01.5 P-N-STREAM-IN, 8)
    parameter int unsigned PROBE_SLOTS_P = 8,
    //! inflight entries (03 §5): default = CA pool + probe slots
    parameter int unsigned INFLIGHT_P    = CA_POOL_P + PROBE_SLOTS_P,
    //! response identity width; 16 preserves the generic folded-key shape,
    //! while AECP CONTROLLER_AVAILABLE uses the full {Entity ID, MAC} tuple
    parameter int unsigned KEY_W_P       = 16,
    //! timer-service depth — sizes the arm/expiry slot index width
    parameter int unsigned TMR_SLOTS_P   = pp_pkg::PP_TIMER_SLOTS_C,
    //! fixed entry-index field width inside the 8-bit timer owner tag
    localparam int unsigned IFL_AW_C = 4,
    //! tag field width — the rest of the timer owner byte
    localparam int unsigned TAG_W_C  = pp_pkg::PP_TIMER_OWNER_W_C - IFL_AW_C,
    //! originator's tag nibble in arm_owner — unique among timer users
    parameter logic [TAG_W_C-1:0] TMR_TAG_P = 4'hC,
    //! derived timer slot index width — matches KL_pp_timer_service
    localparam int unsigned TMR_AW_C = (TMR_SLOTS_P > 32'd1)
                                     ? $clog2(TMR_SLOTS_P) : 32'd1
) (
    input  wire                  clk_i,        //! core clock (P-CLK-HZ domain)
    input  wire                  rst_n,        //! synchronous active-low reset

    // ---- issue port (engines request an originated command) --------------
    input  wire                  iss_valid_i,  //! issue request, held until granted
    input  wire  [IFL_AW_C-1:0]  iss_owner_i,  //! owner id (engine/sink) — seq counter + routing tag
    input  wire  [2:0]           iss_tx_slot_i, //! KL_pp_tx_slots handle of the serialized PDU
    input  wire  [KEY_W_P-1:0]   iss_key_i,    //! exact owner-selected response identity
    input  wire  [TMR_AW_C-1:0]  iss_tmr_slot_i, //! timer slot to arm (sink SM slot / CA-pool slot, F08.4)
    input  wire  [15:0]          iss_timeout_ms_i, //! T-ACMP-CMD / T-AECP-TIMEOUT value, from the owner
    output logic                 iss_ready_o,  //! can accept this cycle (low = table full or busy)
    output logic                 iss_gnt_o,    //! acceptance strobe (valid && ready)
    output logic [15:0]          iss_seq_o,    //! next seq for iss_owner_i — assigned on grant
    output logic [IFL_AW_C-1:0]  iss_id_o,     //! inflight id allocated on grant

    // ---- owner cancellation ----------------------------------------------
    // A controller monitor has at most one exchange live per owner. A valid
    // command from that controller supersedes its availability probe, so the
    // owner can cancel the live exchange without manufacturing a response.
    input  wire                  cancel_valid_i,
    input  wire  [IFL_AW_C-1:0]  cancel_owner_i,

    // ---- response match (RX pipeline, rules V6/V7) ------------------------
    input  wire                  rsp_valid_i,  //! a response PDU arrived
    input  wire  [15:0]          rsp_seq_i,    //! its sequence_id
    input  wire  [KEY_W_P-1:0]   rsp_key_i,    //! same identity shape as iss_key_i

    // ---- routing back to the owner ----------------------------------------
    output logic                 rt_valid_o,   //! response matched an inflight entry
    output logic [IFL_AW_C-1:0]  rt_owner_o,   //! owner of the completed exchange
    output logic [IFL_AW_C-1:0]  rt_id_o,      //! its inflight id
    output logic                 fail_valid_o, //! both attempts timed out
    output logic [IFL_AW_C-1:0]  fail_owner_o, //! owner of the failed exchange
    output logic [IFL_AW_C-1:0]  fail_id_o,    //! its inflight id

    // ---- send lanes toward the TX arbiter ---------------------------------
    output logic                 send_valid_o,   //! first transmission request
    output logic [2:0]           send_slot_o,    //! tx slot to serialize
    output logic                 resend_valid_o, //! retry: EXACT duplicate (same held slot, same seq)
    output logic [2:0]           resend_slot_o,  //! tx slot to re-serialize
    input  wire                  send_accept_valid_i, //! serializer accepted initial/retry slot
    input  wire  [2:0]           send_accept_slot_i,

    // ---- hold/release pair toward KL_pp_tx_slots --------------------------
    output logic                 hold_valid_o,    //! pin the slot: suppress auto-free on eof
    output logic [2:0]           hold_slot_o,     //! slot being pinned
    output logic                 release_valid_o, //! exchange over: pool may free the slot
    output logic [2:0]           release_slot_o,  //! slot being released
    output logic [7:0]           withdraw_slot_mask_o, //! slots canceled before serializer acceptance

    // ---- timer arm port (exact KL_pp_timer_service shape) -----------------
    output logic                 tmr_arm_valid_o,       //! arm/cancel strobe
    output logic                 tmr_arm_cancel_o,      //! 1 = cancel the slot, 0 = arm it
    output logic [TMR_AW_C-1:0]  tmr_arm_slot_o,        //! slot index to arm/cancel
    output logic [pp_pkg::PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_o, //! {TMR_TAG_P, inflight id}
    output logic [31:0]          tmr_arm_deadline_ms_o, //! absolute ms: now + timeout
    input  wire  [31:0]          now_ms_i,              //! timer service now_ms_o

    // ---- timer expiry bus (owner-tagged, shared fan-out) -------------------
    input  wire                  exp_valid_i,  //! expiry event strobe
    input  wire  [TMR_AW_C-1:0]  exp_slot_i,   //! expired slot
    input  wire  [pp_pkg::PP_TIMER_OWNER_W_C-1:0] exp_owner_i, //! owner tag as armed

    // ---- observability -----------------------------------------------------
    output logic [7:0]           rsp_ign_cnt_o,   //! unmatched responses, wraps (F09.4)
    output logic [INFLIGHT_P-1:0] inflight_busy_o //! live inflight entries
);

  // ------------------------------------------------------------- geometry
  // entries are addressed by the low nibble of the timer owner tag, so the
  // table can never exceed the tag's index space
  localparam int unsigned IFL_N_C = 32'd1 << IFL_AW_C;                  // 16

  if (INFLIGHT_P < 32'd1 || INFLIGHT_P > IFL_N_C) begin : g_inflight_check
    $error("KL_pp_originator: INFLIGHT_P must be 1..16 (owner-tag nibble)");
  end

  // ------------------------------------------------------- inflight table
  // Flop CAM (see Decision). Vectors and arrays are sized to the full
  // 16-entry index space so a rogue tag index reads a hard invalid and can
  // never alias a live entry; only 0..INFLIGHT_P-1 are ever allocated.
  // Data arrays are unreset — every read is qualified by valid_r.
  logic [IFL_N_C-1:0]  valid_r;
  logic [IFL_N_C-1:0]  retried_r;
  logic [IFL_N_C-1:0]  exp_pend_r;
  logic [IFL_N_C-1:0]  await_tx_r;
  logic [IFL_N_C-1:0]  accept_pend_r;
  logic [IFL_N_C-1:0]  cancel_pend_r;
  logic [IFL_AW_C-1:0] owner_r [0:IFL_N_C-1];
  logic [KEY_W_P-1:0]  key_r   [0:IFL_N_C-1];
  logic [15:0]         seq_r   [0:IFL_N_C-1];
  logic [TMR_AW_C-1:0] tslot_r [0:IFL_N_C-1];
  logic [15:0]         tout_r  [0:IFL_N_C-1];
  logic [2:0]          txs_r   [0:IFL_N_C-1];

  // per-owner sequence_id counters (03 §5: seq from the owner's counter)
  logic [15:0] seq_ctr_r [0:IFL_N_C-1];

  // --------------------------------------------------- allocation picker
  logic                free_ok_w;
  logic [IFL_AW_C-1:0] free_ix_w;

  always_comb begin : alloc_pick
    free_ok_w = 1'b0;
    free_ix_w = '0;
    for (int i = int'(INFLIGHT_P) - 1; i >= 0; i--) begin
      if (!valid_r[i]) begin
        free_ok_w = 1'b1;
        free_ix_w = IFL_AW_C'(i);
      end
    end
  end

  logic [IFL_N_C-1:0]  cancel_work_w;
  logic                cancel_pend_ok_w;
  logic [IFL_AW_C-1:0] cancel_pend_ix_w;

  always_comb begin : cancel_pending_pick
    cancel_work_w = cancel_pend_r;
    if (cancel_valid_i && cancel_hit_w)
      cancel_work_w[cancel_ix_w] = 1'b1;
    cancel_pend_ok_w = 1'b0;
    cancel_pend_ix_w = '0;
    for (int i = int'(INFLIGHT_P) - 1; i >= 0; i--) begin
      if (cancel_work_w[i]) begin
        cancel_pend_ok_w = 1'b1;
        cancel_pend_ix_w = IFL_AW_C'(i);
      end
    end
  end

  logic                accept_ok_w;
  logic [IFL_AW_C-1:0] accept_pend_ix_w;

  always_comb begin : accept_pending_pick
    accept_ok_w      = 1'b0;
    accept_pend_ix_w = '0;
    for (int i = int'(INFLIGHT_P) - 1; i >= 0; i--) begin
      if (accept_pend_r[i]) begin
        accept_ok_w      = 1'b1;
        accept_pend_ix_w = IFL_AW_C'(i);
      end
    end
  end

  // ------------------------------------------------------- response CAM
  logic                hit_ok_w;
  logic [IFL_AW_C-1:0] hit_ix_w;

  always_comb begin : cam_pick
    hit_ok_w = 1'b0;
    hit_ix_w = '0;
    for (int i = int'(INFLIGHT_P) - 1; i >= 0; i--) begin
      if (valid_r[i] && (key_r[i] == rsp_key_i)
                     && (seq_r[i] == rsp_seq_i)) begin
        hit_ok_w = 1'b1;
        hit_ix_w = IFL_AW_C'(i);
      end
    end
  end

  logic                cancel_hit_w;
  logic [IFL_AW_C-1:0] cancel_ix_w;

  always_comb begin : cancel_pick
    cancel_hit_w = 1'b0;
    cancel_ix_w  = '0;
    for (int i = int'(INFLIGHT_P) - 1; i >= 0; i--) begin
      if (valid_r[i] && (owner_r[i] == cancel_owner_i)) begin
        cancel_hit_w = 1'b1;
        cancel_ix_w  = IFL_AW_C'(i);
      end
    end
  end

  // ------------------------------------------ serializer-acceptance CAM
  // A held TX slot belongs to exactly one live exchange. Match the handle
  // granted by the TX arbiter back to the entry whose initial send or retry
  // is waiting in the originator lane queue. Until this grant arrives there
  // is no wire attempt, so no response timeout may run.
  logic                accept_hit_w;
  logic [IFL_AW_C-1:0] accept_ix_w;

  always_comb begin : accept_pick
    accept_hit_w = 1'b0;
    accept_ix_w  = '0;
    for (int i = int'(INFLIGHT_P) - 1; i >= 0; i--) begin
      if (valid_r[i] && await_tx_r[i]
                     && (txs_r[i] == send_accept_slot_i)) begin
        accept_hit_w = 1'b1;
        accept_ix_w  = IFL_AW_C'(i);
      end
    end
  end

  // -------------------------------------------------- expiry acceptance
  // Filter the shared expiry bus down to genuine hits on a live entry of
  // ours (tag match + index in range + armed slot matches the stored one);
  // a stale fire — the entry completed while its expiry was in the sweep
  // pipeline — is dropped here or, if already parked, cleared by the
  // response path below (the response always wins the race).
  logic                exp_ours_w;
  logic [IFL_AW_C-1:0] exp_ix_w;
  logic                exp_genuine_w;

  assign exp_ours_w = exp_valid_i
      && (exp_owner_i[pp_pkg::PP_TIMER_OWNER_W_C-1:IFL_AW_C] == TMR_TAG_P);
  assign exp_ix_w   = exp_owner_i[IFL_AW_C-1:0];
  assign exp_genuine_w = exp_ours_w && (32'(exp_ix_w) < INFLIGHT_P)
      && valid_r[exp_ix_w] && (tslot_r[exp_ix_w] == exp_slot_i);

  logic                pend_ok_w;
  logic [IFL_AW_C-1:0] pend_ix_w;

  always_comb begin : pend_pick
    pend_ok_w = 1'b0;
    pend_ix_w = '0;
    for (int i = int'(INFLIGHT_P) - 1; i >= 0; i--) begin
      if (exp_pend_r[i]) begin
        pend_ok_w = 1'b1;
        pend_ix_w = IFL_AW_C'(i);
      end
    end
  end

  // -------------------------------------------------- one event per cycle
  // Priority response > parked cancel > TX acceptance > expiry > issue: the
  // event kinds share the timer arm port and the hold/release/send pulse lanes,
  // so exactly one proceeds per cycle. Only issue can be backpressured.
  logic ev_rsp_w, ev_cancel_w, ev_accept_w, ev_exp_w, ev_iss_w;

  assign ev_rsp_w    = rsp_valid_i && hit_ok_w;
  assign ev_cancel_w = !ev_rsp_w && cancel_pend_ok_w;
  assign ev_accept_w = !ev_rsp_w && !ev_cancel_w && accept_ok_w;
  assign ev_exp_w    = !ev_rsp_w && !ev_cancel_w && !ev_accept_w && pend_ok_w;
  assign iss_ready_o = free_ok_w && !ev_rsp_w && !ev_cancel_w
                     && !ev_accept_w && !pend_ok_w;
  assign ev_iss_w    = iss_valid_i && iss_ready_o;

  // Expose every slot that must be withdrawn before serializer acceptance.
  // The mask is combinational from the current response/cancel decision so
  // the TX lane can suppress a selected request before the registered release
  // reaches the shared slot pool. Stored cancellations remain masked while a
  // response for another entry consumes the single action lane.
  always_comb begin : withdraw_mask
    withdraw_slot_mask_o = '0;
    for (int i = 0; i < int'(INFLIGHT_P); i++) begin
      if (cancel_work_w[i] && valid_r[i])
        withdraw_slot_mask_o[txs_r[i]] = 1'b1;
    end
    if (ev_rsp_w)
      withdraw_slot_mask_o[txs_r[hit_ix_w]] = 1'b1;
    if (ev_exp_w && valid_r[pend_ix_w] && retried_r[pend_ix_w])
      withdraw_slot_mask_o[txs_r[pend_ix_w]] = 1'b1;
  end

  assign iss_gnt_o = ev_iss_w;
  assign iss_id_o  = free_ix_w;
  assign iss_seq_o = seq_ctr_r[iss_owner_i];

  // ------------------------------------------------------- table update
  always_ff @(posedge clk_i) begin : inflight_state
    if (!rst_n) begin
      valid_r    <= '0;
      retried_r  <= '0;
      exp_pend_r <= '0;
      await_tx_r <= '0;
      accept_pend_r <= '0;
      cancel_pend_r <= '0;
      for (int i = 0; i < int'(IFL_N_C); i++) begin
        seq_ctr_r[i] <= 16'd0;
      end
    end else begin
      // park a genuine expiry; ordering below lets a same-cycle response
      // for the same entry clear it again (the response wins)
      if (exp_genuine_w) begin
        exp_pend_r[exp_ix_w] <= 1'b1;
      end
      // The serializer grant is not backpressurable. Park it before the
      // one-event priority chain so a simultaneous response or cancellation
      // for another entry cannot consume the grant without starting a timer.
      if (send_accept_valid_i && accept_hit_w) begin
        accept_pend_r[accept_ix_w] <= 1'b1;
      end
      // Cancellation is also a one-cycle, non-backpressurable input. Park it
      // before arbitration so a response for another entry cannot consume the
      // sole event lane and lose a TIME_LIMITED drain cancellation.
      if (cancel_valid_i && cancel_hit_w) begin
        cancel_pend_r[cancel_ix_w] <= 1'b1;
      end
      if (ev_rsp_w) begin
        valid_r[hit_ix_w]    <= 1'b0;
        exp_pend_r[hit_ix_w] <= 1'b0;
        await_tx_r[hit_ix_w] <= 1'b0;
        accept_pend_r[hit_ix_w] <= 1'b0;
        cancel_pend_r[hit_ix_w] <= 1'b0;
      end else if (ev_cancel_w) begin
        valid_r[cancel_pend_ix_w]    <= 1'b0;
        exp_pend_r[cancel_pend_ix_w] <= 1'b0;
        await_tx_r[cancel_pend_ix_w] <= 1'b0;
        accept_pend_r[cancel_pend_ix_w] <= 1'b0;
        cancel_pend_r[cancel_pend_ix_w] <= 1'b0;
      end else if (ev_accept_w) begin
        await_tx_r[accept_pend_ix_w] <= 1'b0;
        accept_pend_r[accept_pend_ix_w] <= 1'b0;
      end else if (ev_exp_w) begin
        exp_pend_r[pend_ix_w] <= 1'b0;
        if (valid_r[pend_ix_w]) begin
          if (!retried_r[pend_ix_w]) begin
            retried_r[pend_ix_w] <= 1'b1;   // one exact-duplicate retry
            await_tx_r[pend_ix_w] <= 1'b1;
          end else begin
            valid_r[pend_ix_w] <= 1'b0;     // second timeout: fail + free
            await_tx_r[pend_ix_w] <= 1'b0;
            accept_pend_r[pend_ix_w] <= 1'b0;
          end
        end
      end else if (ev_iss_w) begin
        valid_r[free_ix_w]    <= 1'b1;
        retried_r[free_ix_w]  <= 1'b0;
        exp_pend_r[free_ix_w] <= 1'b0;
        await_tx_r[free_ix_w] <= 1'b1;
        accept_pend_r[free_ix_w] <= 1'b0;
        owner_r[free_ix_w]    <= iss_owner_i;
        key_r[free_ix_w]      <= iss_key_i;
        seq_r[free_ix_w]      <= seq_ctr_r[iss_owner_i];
        tslot_r[free_ix_w]    <= iss_tmr_slot_i;
        tout_r[free_ix_w]     <= iss_timeout_ms_i;
        txs_r[free_ix_w]      <= iss_tx_slot_i;
        seq_ctr_r[iss_owner_i] <= seq_ctr_r[iss_owner_i] + 16'd1;
      end
    end
  end

  // -------------------------------------------------- registered actions
  // All externally visible pulses fire the cycle AFTER their event; the
  // one-event rule guarantees each lane carries at most one op per cycle.
  always_ff @(posedge clk_i) begin : action_regs
    if (!rst_n) begin
      rt_valid_o            <= 1'b0;
      rt_owner_o            <= '0;
      rt_id_o               <= '0;
      fail_valid_o          <= 1'b0;
      fail_owner_o          <= '0;
      fail_id_o             <= '0;
      send_valid_o          <= 1'b0;
      send_slot_o           <= '0;
      resend_valid_o        <= 1'b0;
      resend_slot_o         <= '0;
      hold_valid_o          <= 1'b0;
      hold_slot_o           <= '0;
      release_valid_o       <= 1'b0;
      release_slot_o        <= '0;
      tmr_arm_valid_o       <= 1'b0;
      tmr_arm_cancel_o      <= 1'b0;
      tmr_arm_slot_o        <= '0;
      tmr_arm_owner_o       <= '0;
      tmr_arm_deadline_ms_o <= 32'd0;
    end else begin
      rt_valid_o      <= 1'b0;
      fail_valid_o    <= 1'b0;
      send_valid_o    <= 1'b0;
      resend_valid_o  <= 1'b0;
      hold_valid_o    <= 1'b0;
      release_valid_o <= 1'b0;
      tmr_arm_valid_o <= 1'b0;
      if (ev_rsp_w) begin
        // route + disarm + release; the entry frees this edge
        rt_valid_o            <= 1'b1;
        rt_owner_o            <= owner_r[hit_ix_w];
        rt_id_o               <= hit_ix_w;
        release_valid_o       <= 1'b1;
        release_slot_o        <= txs_r[hit_ix_w];
        tmr_arm_valid_o       <= 1'b1;
        tmr_arm_cancel_o      <= 1'b1;
        tmr_arm_slot_o        <= tslot_r[hit_ix_w];
        tmr_arm_owner_o       <= {TMR_TAG_P, hit_ix_w};
        tmr_arm_deadline_ms_o <= 32'd0;
      end else if (ev_cancel_w) begin
        // A valid command from this owner proves liveness and supersedes
        // the probe. Free the immutable retry slot and disarm its timeout.
        release_valid_o       <= 1'b1;
        release_slot_o        <= txs_r[cancel_pend_ix_w];
        tmr_arm_valid_o       <= 1'b1;
        tmr_arm_cancel_o      <= 1'b1;
        tmr_arm_slot_o        <= tslot_r[cancel_pend_ix_w];
        tmr_arm_owner_o       <= {TMR_TAG_P, cancel_pend_ix_w};
        tmr_arm_deadline_ms_o <= 32'd0;
      end else if (ev_accept_w) begin
        // Start the attempt budget only after the arbiter transfers this
        // handle to the serializer. Queueing delay is outside that budget.
        tmr_arm_valid_o       <= 1'b1;
        tmr_arm_cancel_o      <= 1'b0;
        tmr_arm_slot_o        <= tslot_r[accept_pend_ix_w];
        tmr_arm_owner_o       <= {TMR_TAG_P, accept_pend_ix_w};
        tmr_arm_deadline_ms_o <= now_ms_i + 32'(tout_r[accept_pend_ix_w]);
      end else if (ev_exp_w) begin
        if (valid_r[pend_ix_w]) begin
          if (!retried_r[pend_ix_w]) begin
            // one retry: EXACT duplicate — the held slot, untouched, so
            // the wire PDU (including seq) is bit-identical (05 A13)
            resend_valid_o <= 1'b1;
            resend_slot_o  <= txs_r[pend_ix_w];
          end else begin
            // second timeout: report + release (the expired slot already
            // disarmed itself in the timer service — no cancel needed)
            fail_valid_o    <= 1'b1;
            fail_owner_o    <= owner_r[pend_ix_w];
            fail_id_o       <= pend_ix_w;
            release_valid_o <= 1'b1;
            release_slot_o  <= txs_r[pend_ix_w];
          end
        end
      end else if (ev_iss_w) begin
        send_valid_o          <= 1'b1;
        send_slot_o           <= iss_tx_slot_i;
        hold_valid_o          <= 1'b1;
        hold_slot_o           <= iss_tx_slot_i;
      end
    end
  end

  // -------------------------------------- unmatched-response counter
  // F09.4: a response with no inflight match is silently ignored — no
  // state change, no routing — but the drop is trace-visible (V8 spirit)
  always_ff @(posedge clk_i) begin : ign_count
    if (!rst_n) begin
      rsp_ign_cnt_o <= 8'd0;
    end else if (rsp_valid_i && !hit_ok_w) begin
      rsp_ign_cnt_o <= rsp_ign_cnt_o + 8'd1;
    end
  end

  assign inflight_busy_o = valid_r[INFLIGHT_P-1:0];

endmodule : KL_pp_originator
`default_nettype wire
