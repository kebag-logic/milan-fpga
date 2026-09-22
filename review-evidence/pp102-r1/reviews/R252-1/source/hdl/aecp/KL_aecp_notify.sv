/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_notify.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/06 SS6.7 notifications, SS6.4 lock;
//                 Milan v1.2 SS5.3.4.1/SS5.3.4.2 dynamic state,
//                 SS5.4.2.1/SS5.4.2.2/SS5.4.2.21/SS5.4.2.22, SS5.4.5,
//                 IEEE 1722.1-2021 SS7.4.1/SS7.4.2/SS7.4.37/SS7.4.38, SS9.3.5)
//
//  Description : The registered-controller list, the ENTITY lock, and the
//                unsolicited-notification scheduler, in ONE block so the
//                three things that must agree live behind one wall:
//                  - Milan SS5.3.4.2's list ("at least 16 controllers per AVB
//                    Interface", entry = {Entity ID, MAC address, port,
//                    Sequence ID of the next unsolicited notification}) -
//                    P-N-AVB-INTERFACES is 1 here, so the port field is
//                    constant and not stored;
//                  - Milan SS5.3.4.1's locked state ("At a given time, a
//                    PAAD-AE may be either locked by a controller or not";
//                    the one thing kept is "The Entity ID of the locking
//                    controller") with IEEE SS7.4.2's 60 s expiry ("The lock
//                    times out after one (1) minute. The LOCK_ENTITY command
//                    may be repeated by the current owner of the lock to
//                    keep the lock alive");
//                  - Milan SS5.4.5.1's emission duty ("the PAAD-AE sends one
//                    unsolicited notification message to each registered
//                    controller except the requesting controller", with
//                    destination_mac_address, controller_entity_id and
//                    sequence id "populated with the unique parameters
//                    associated with each registered controller", and
//                    "After sending ... the PAAD-AE increments by 1 the
//                    Sequence ID variable associated with the entry ... no
//                    matter whether the packet is actually sent").
//
//                THE TABLE IS ONE LUTRAM, WALKED - NEVER A COMPARATOR BANK.
//                Every duty here is slow-path (an AECP command in flight, a
//                once-per-event emission round), so entries are visited one
//                per cycle through ONE read port and mutated through ONE
//                write port, and the whole match logic is a single
//                {eid, mac} equality. Milan's minimum count (16) is the
//                depth; nothing is sized past it.
//
//                REGISTER/DEREGISTER/LOCK/UNLOCK arrive as OPS on the rgy
//                face, driven by KL_aecp_engine's gather bus while the
//                corresponding microprogram is in flight (the engine's gxf
//                watchdog bounds the wait, so a wedge here degrades to
//                ENTITY_MISBEHAVING, never a hang). Results are one 64-bit
//                word; the ops encode:
//                  op 0 REGISTER   -> walk; refresh a duplicate {eid, mac}
//                     (Sequence ID PRESERVED - Milan SS5.4.2.21 initializes
//                     it to zero only "If a new entry is created") or claim
//                     a free row (seq = 0); no row free -> result 1, which
//                     the microprogram turns into NO_RESOURCES (Milan
//                     SS5.4.2.21 "it shall return the NO_RESOURCES error
//                     code" - the CONTROLLER_AVAILABLE eviction probe of the
//                     same clause is a MAY and is not attempted).
//                     TIME_LIMITED (IEEE SS7.4.37.2) arms this row's timer
//                     slot for 300 s; a refresh WITHOUT the flag cancels it.
//                  op 1 DEREGISTER -> walk; clear the matching row; always
//                     result 0 (removing an absent registration is
//                     idempotent - neither IEEE SS7.4.38 nor Milan SS5.4.2.22
//                     defines an error arm for it).
//                  op 2 LOCK, op 3 UNLOCK -> no walk. The lock is one held
//                     bit + one 64-bit eid + one shared-timer slot, per the
//                     texts above. Result codes: 0 = SUCCESS (locked /
//                     re-armed / unlocked / already-unlocked query), 1 =
//                     ENTITY_LOCKED (held by another controller - both the
//                     foreign LOCK and the foreign UNLOCK land here, because
//                     IEEE SS7.4.2 admits state changes only from the
//                     holder, and the denial carrying locked_id IS the
//                     query answer Milan SS5.4.2.2's UNLOCK note wants).
//                     Result bit 1 = "the lock STATE CHANGED", the emission
//                     trigger (Milan SS5.4.5.2 sends only for a command
//                     that "modifies the state", so a keep-alive re-lock
//                     and an already-unlocked query emit nothing).
//                  rgy_state_i = 1 -> no op: answer the holder's eid
//                     (locked_id for the response; 0 = not locked).
//                THE OP RUNS ONCE PER REQUEST EDGE. A microprogram that
//                issues two rgy gathers back-to-back would leave rgy_req
//                high across both; every rgy program therefore separates
//                its gathers with a non-gather microop (the COMPARE that
//                tests the result does it naturally) - recorded in
//                gen_ucode.py where the programs live.
//
//                EXPIRY RIDES THE SHARED TIMER SERVICE, never a private
//                millisecond counter: row i owns slot TMR_REGMON_BASE_P + i
//                for TIME_LIMITED registration and the second half owns the
//                Milan SS5.4.5.3 CONTROLLER_AVAILABLE monitor. Each valid
//                command from a registered tuple requests a new independent
//                PRNG draw in the 30 to 60 second range. A monitor expiry
//                starts one CONTROLLER_AVAILABLE transaction through the
//                shared originator. Any matching response, regardless of
//                status, requests a new draw; one failed retry removes the
//                row and queues its targeted DEREGISTER notification. The
//                lock owns singleton slot TMR_LOCK_SLOT_P. A fired
//                registration slot parks in pend_r exactly like
//                KL_pp_originator parks expiries, because the walk engine
//                is single-threaded; ANY successful re-register of the row
//                clears the parked fire (the refresh wins the race - a
//                controller that re-registered must never be expired on the
//                deadline it just replaced). Lock expiry clears the lock
//                and queues the Milan Table 5.22 LOCK_ENTITY notification
//                ("Sent when the entity automatically unlocks itself after
//                the one (1) minute timeout").
//
//                EMISSION is a walk of the same table: pick the highest
//                pending event class, then for each valid row (skipping the
//                excluded requester, if any) hand KL_aecp_engine ONE job
//                {kind, descriptor, eid, mac, seq} and wait for uns_done_i.
//                The engine rebuilds the response from CURRENT state for
//                every controller - same builder, same microprogram, same
//                gather faces as the solicited answer, per the one-builder
//                rule. Sequence ID writes back +1 per completed job. An
//                event re-firing mid-walk simply re-pends its class (the
//                pending bit clears at PICK), so every controller sees the
//                final state at least once; re-fires are coalesced by
//                class, which Milan permits because the notification body
//                is not queued history but current state. The automatic
//                DEREGISTER notification is a single-shot job to the
//                expired controller only (Milan Table 5.22: "sent only to
//                this controller"), latched at drain time because its row
//                is gone by emission time.
//
//                COMMAND TRIGGERS retain the opcode-specific response kind,
//                descriptor tuple, command arguments, and requester EID in a
//                bounded FIFO. Successful no-op setters do not enqueue. The
//                requester is excluded from the table walk. GET_COUNTERS
//                changes use one dirty and pending bit per served descriptor;
//                their one-second limit is measured when emission begins.
//
//                DEADLOCK IS BROKEN BY WITHDRAWAL: while a presented job
//                waits for the engine, a rising rgy_req_i proves the engine
//                is busy running a solicited registry/lock command (an
//                unsolicited job's own microprogram never touches the rgy
//                face), so the un-accepted job is withdrawn, the op served,
//                and the job re-presented. Without this, engine-waits-on-
//                gather and notify-waits-on-done form a cycle.
//
//                WHAT THIS BLOCK DOES NOT DO, on purpose: the optional
//                CONTROLLER_AVAILABLE eviction sweep on registry overflow.
//                A full registry returns the mandatory NO_RESOURCES status
//                without evicting a controller that may still be alive.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_notify
  import pp_pkg::*;
#(
    //! P-N-CONTROLLERS (Milan SS5.3.4.2: at least 16 per AVB Interface)
    parameter int unsigned N_CTRL_P          = 16,
    //! P-N-STREAM-IN / P-N-STREAM-OUT - width of the stream-info event sets
    parameter int unsigned N_STREAM_IN_P     = 8,
    parameter int unsigned N_STREAM_OUT_P    = 8,
    //! IEEE SS7.4.37.2: "a timeout of 300 seconds for the registration"
    parameter int unsigned TL_TIMEOUT_MS_P   = 300_000,
    //! IEEE SS7.4.2: "The lock times out after one (1) minute"
    parameter int unsigned LOCK_TIMEOUT_MS_P = 60_000,
    //! timer-service geometry + this block's slot allocation (F08.4)
    parameter int unsigned TMR_SLOTS_P       = 89,
    parameter int unsigned TMR_REGMON_BASE_P = 25,
    parameter int unsigned TMR_LOCK_SLOT_P   = 61,
    //! derived - do not override
    localparam int unsigned TMR_AW_C = (TMR_SLOTS_P > 1) ? $clog2(TMR_SLOTS_P) : 1,
    localparam int unsigned CIX_W_C  = (N_CTRL_P > 1) ? $clog2(N_CTRL_P) : 1,
    //! stream-index widths, CLAMPED exactly as protocol_processor_top clamps
    //! its own (a 1-stream shape must not declare [-1:0])
    localparam int unsigned SIX_W_C  = (N_STREAM_IN_P  > 1) ? $clog2(N_STREAM_IN_P)  : 1,
    localparam int unsigned SOX_W_C  = (N_STREAM_OUT_P > 1) ? $clog2(N_STREAM_OUT_P) : 1
) (
    input  wire         clk_i,               //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,               //! synchronous active-low reset

    //! ---- registry/lock op face (KL_aecp_engine gather bus client) ----
    input  wire         rgy_req_i,           //! op/state query presented (held)
    input  wire         rgy_state_i,         //! 1 = read the lock holder, no op
    input  wire  [1:0]  rgy_op_i,            //! 0 REG / 1 DEREG / 2 LOCK / 3 UNLOCK
    input  wire  [63:0] rgy_eid_i,           //! requesting controller entity_id
    input  wire  [47:0] rgy_mac_i,           //! its source MAC (the registry tuple)
    input  wire         rgy_tl_i,            //! REGISTER: TIME_LIMITED flag
    output logic [63:0] rgy_data_o,          //! result word (see banner)
    output logic        rgy_wait_o,          //! HOLD the gather beat (not a ready)

    //! ---- Table 5.22 event strobes (one-cycle; coalesced by class) ----
    input  wire  [N_STREAM_IN_P-1:0]  ev_stri_in_i,  //! per-sink GET_STREAM_INFO change
    input  wire  [N_STREAM_OUT_P-1:0] ev_stri_out_i, //! per-source GET_STREAM_INFO change
    input  wire         ev_avb_i,            //! GET_AVB_INFO state change
    input  wire         ev_asp_i,            //! GET_AS_PATH state change
    input  wire         ev_amap_i,           //! successful state-changing map edit
    input  wire         ev_amap_remove_i,    //! 0 ADD, 1 REMOVE
    input  wire  [15:0] ev_amap_type_i,
    input  wire  [15:0] ev_amap_index_i,
    input  wire  [15:0] ev_amap_count_i,
    input  wire  [63:0] ev_amap_excl_eid_i,
    input  wire         ev_ctr_i,            //! one descriptor counter changed
    input  wire  [15:0] ev_ctr_type_i,
    input  wire  [15:0] ev_ctr_index_i,
    input  wire         ev_cmd_i,            //! successful state-changing command
    input  wire  [3:0]  ev_cmd_class_i,
    input  wire  [15:0] ev_cmd_type_i,
    input  wire  [15:0] ev_cmd_index_i,
    input  wire  [15:0] ev_cmd_arg0_i,
    input  wire  [15:0] ev_cmd_arg1_i,
    input  wire  [63:0] ev_cmd_excl_eid_i,

    //! ---- registered-controller availability monitor --------------------
    input  wire         rx_cmd_valid_i,      //! valid AECP command at the RX validator
    input  wire  [63:0] rx_cmd_eid_i,
    input  wire  [47:0] rx_cmd_mac_i,
    output logic        prng_draw_req_o,
    output logic [2:0]  prng_draw_kind_o,
    input  wire         prng_draw_busy_i,
    input  wire         prng_draw_valid_i,
    input  wire  [15:0] prng_draw_ms_i,
    output logic        ca_valid_o,
    output logic [3:0]  ca_owner_o,
    output logic [63:0] ca_ctlr_eid_o,
    output logic [47:0] ca_mac_o,
    input  wire         ca_ready_i,
    output logic        ca_cancel_valid_o,
    output logic [3:0]  ca_cancel_owner_o,
    input  wire         ca_rsp_valid_i,
    input  wire  [3:0]  ca_rsp_owner_i,
    input  wire         ca_fail_valid_i,
    input  wire  [3:0]  ca_fail_owner_i,

    //! ---- unsolicited job face toward KL_aecp_engine ----
    output logic        uns_valid_o,         //! job presented, held until done
    output logic [3:0]  uns_kind_o,          //! pp_pkg PP_UNS_* response kind
    output logic [15:0] uns_desc_type_o,     //! response descriptor_type
    output logic [15:0] uns_desc_index_o,    //! response descriptor_index
    output logic [63:0] uns_ctlr_eid_o,      //! target controller entity_id
    output logic [47:0] uns_mac_o,           //! target unicast MAC
    output logic [15:0] uns_seq_o,           //! this entry's sequence_id
    output logic        uns_amap_remove_o,
    output logic [15:0] uns_amap_count_o,
    output logic [15:0] uns_arg0_o,
    output logic [15:0] uns_arg1_o,
    input  wire         uns_done_i,          //! engine retired the job (sent or voided)
    output logic        amap_busy_o,         //! preserve the engine staging RAM

    //! ---- lock state, published (06 SS6.4 consumers: engine + listener A1) ----
    output logic        lock_held_o,         //! ENTITY lock held
    output logic [63:0] lock_ctlr_o,         //! holder's controller entity_id

    //! ---- shared timer service (one arm client; expiry bus listener) ----
    output logic                 tmr_arm_valid_o,       //! one-cycle arm/cancel
    output logic                 tmr_arm_cancel_o,      //! 1 = cancel the slot
    output logic [TMR_AW_C-1:0]  tmr_arm_slot_o,        //! slot to arm/cancel
    output logic [PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_o, //! PP_OWN_NTFY/LOCK tag
    output logic [31:0]          tmr_arm_deadline_ms_o, //! absolute ms deadline
    input  wire  [31:0]          now_ms_i,              //! timer service now_ms_o
    input  wire                  tmr_exp_valid_i,       //! expiry event strobe
    input  wire  [TMR_AW_C-1:0]  tmr_exp_slot_i,        //! expired slot
    input  wire  [PP_TIMER_OWNER_W_C-1:0] tmr_exp_owner_i, //! owner tag as armed

    output logic                 mon_arm_valid_o,
    output logic                 mon_arm_cancel_o,
    output logic [TMR_AW_C-1:0]  mon_arm_slot_o,
    output logic [PP_TIMER_OWNER_W_C-1:0] mon_arm_owner_o,
    output logic [31:0]          mon_arm_deadline_ms_o,

    //! ---- observability ----
    output logic [7:0]  dbg_reg_cnt_o,       //! live registrations
    output logic [15:0] dbg_uns_cnt_o,       //! unsolicited jobs completed
    output logic [7:0]  dbg_coalesce_o       //! lock events merged losing their exclusion
);

  // ---- registry rows: ONE LUTRAM, one read + one write port ---------------
  //! {eid, mac, seq} = 128 bits x N_CTRL_P. valid/tl/pend stay in flops -
  //! the expiry intake and the walk touch them in the same cycle.
  (* ram_style = "distributed" *) logic [127:0] rows_r [0:N_CTRL_P-1];
  logic [N_CTRL_P-1:0] valid_r, tl_r, pend_r;

  logic [CIX_W_C-1:0] rd_ix_w;
  logic [127:0]       row_w;
  logic [63:0]        row_eid_w;
  logic [47:0]        row_mac_w;
  logic [15:0]        row_seq_w;
  assign row_w     = rows_r[rd_ix_w];
  assign row_eid_w = row_w[127:64];
  assign row_mac_w = row_w[63:16];
  assign row_seq_w = row_w[15:0];

  //! registered write strobes: the row write lands one cycle after the
  //! state that decided it - no reader touches that row that soon
  logic               wr_en_r;
  logic [CIX_W_C-1:0] wr_ix_r;
  logic [127:0]       wr_row_r;
  always_ff @(posedge clk_i) begin : row_write
    if (wr_en_r) rows_r[wr_ix_r] <= wr_row_r;
  end

  // ---- the ENTITY lock (Milan SS5.3.4.1: one holder eid + one held bit) ---
  logic        lk_held_r;
  logic [63:0] lk_ctlr_r;
  assign lock_held_o = lk_held_r;
  assign lock_ctlr_o = lk_ctlr_r;

  // ---- pending event classes + the lock notification's exclusion ----------
  logic [N_STREAM_IN_P-1:0]  pe_sin_r;
  logic [N_STREAM_OUT_P-1:0] pe_sout_r;
  logic        pe_avb_r, pe_asp_r, pe_lock_r, pe_amap_r;
  logic        amap_remove_r;
  logic [15:0] amap_type_r, amap_index_r, amap_count_r;
  logic [63:0] amap_excl_r;
  logic [63:0] lockx_eid_r;    //! requester excluded from the lock emission
  logic        lockx_v_r;      //! 0 = no exclusion (timeout, or coalesced)

  // Command-driven notifications are losslessly parked behind the registry
  // walk. Sixteen entries match the dispatcher depth and keep a slow fan-out
  // from overwriting the identity of a later state change.
  localparam int unsigned CMDQ_N_C = 16;
  logic [3:0]  cmdq_class_r [0:CMDQ_N_C-1];
  logic [15:0] cmdq_type_r  [0:CMDQ_N_C-1];
  logic [15:0] cmdq_index_r [0:CMDQ_N_C-1];
  logic [15:0] cmdq_arg0_r  [0:CMDQ_N_C-1];
  logic [15:0] cmdq_arg1_r  [0:CMDQ_N_C-1];
  logic [63:0] cmdq_excl_r  [0:CMDQ_N_C-1];
  logic [3:0]  cmdq_wr_r, cmdq_rd_r;
  logic [4:0]  cmdq_count_r;
  logic [15:0] cmdq_drop_r;
  logic        cmd_class_ok_w, cmd_push_w;

  // Counter notifications have one independent one-second throttle per
  // descriptor. This build serves every stream row plus AVB_INTERFACE[0]
  // and CLOCK_DOMAIN[0], the same set accepted by GET_COUNTERS.
  localparam int unsigned N_CTR_DESC_C = N_STREAM_IN_P + N_STREAM_OUT_P + 2;
  localparam int unsigned CTX_W_C = (N_CTR_DESC_C > 1) ? $clog2(N_CTR_DESC_C) : 1;
  localparam logic [15:0] DT_STREAM_INPUT_C  = 16'h0005;
  localparam logic [15:0] DT_STREAM_OUTPUT_C = 16'h0006;
  localparam logic [15:0] DT_AVB_INTERFACE_C = 16'h0009;
  localparam logic [15:0] DT_CLOCK_DOMAIN_C  = 16'h0024;
  logic [N_CTR_DESC_C-1:0] ctr_dirty_r, ctr_pend_r, ctr_sent_r;
  logic [31:0] ctr_last_r [0:N_CTR_DESC_C-1];
  logic        ctr_ev_ok_w;
  logic [CTX_W_C-1:0] ctr_ev_ix_w;

  // Availability monitor state. A command hit only sets a bit; the single
  // PRNG draw port drains those bits and arms the second half of regmon.
  logic [N_CTRL_P-1:0] mon_draw_pend_r, ca_pend_r, ca_probe_r;
  logic                 mon_draw_wait_r;
  logic [CIX_W_C-1:0]   mon_draw_ix_r;
  logic                 mon_pick_ok_w, ca_pick_ok_w, ca_cancel_ok_w;
  logic [CIX_W_C-1:0]   mon_pick_ix_w, ca_pick_ix_w, ca_cancel_ix_w;
  logic [N_CTRL_P-1:0]  rx_cmd_hit_w;

  //! the auto-DEREGISTER single-shot holder: its row is cleared at drain, so
  //! the addressing tuple must be latched before it goes
  logic        dh_v_r;
  logic [63:0] dh_eid_r;
  logic [47:0] dh_mac_r;
  logic [15:0] dh_seq_r;

  // ---- FSM ----------------------------------------------------------------
  typedef enum logic [3:0] {
    N_IDLE, N_WALK, N_APPLY, N_ANS, N_DRAIN, N_EMIT_RD, N_EMIT_WAIT, N_EMIT_WB
  } n_st_e;
  n_st_e n_st_r;

  //! once-per-request latch, NOT an edge detector: a request withdrawn-from
  //! in N_EMIT_WAIT must still be serviceable when the FSM reaches N_IDLE a
  //! cycle later, and a plain edge detector consumed the edge on the way -
  //! the engine's gather then starved into its watchdog (found by the
  //! pp_top L2b check: the lock notification answered ENTITY_MISBEHAVING)
  logic               req_done_r;
  logic [CIX_W_C-1:0] wk_ix_r;          // walk index (op + emit + drain)
  logic               wk_match_r;
  logic [CIX_W_C-1:0] wk_match_ix_r;
  logic [15:0]        wk_match_seq_r;
  logic               wk_free_r;
  logic [CIX_W_C-1:0] wk_free_ix_r;
  //! ONE holding set for BOTH walks (op arguments; presented-job identity).
  //! The FSM serializes the two duties, and a job interrupted by an op is
  //! re-latched from its row (or the dh_ holder) on resume - so sharing the
  //! 128 flops and, more to the point, the 128-bit write-back mux they feed
  //! is free.
  logic [63:0]        hold_eid_r;
  logic [47:0]        hold_mac_r;
  logic [15:0]        hold_seq_r;
  logic               op_tl_r, op_dereg_r;
  //! result: 2 bits (bit 0 = refused/denied, bit 1 = state changed) plus a
  //! flag routing the state query's 64-bit holder eid - never a 64-bit
  //! result register whose D-mux costs more than the data it ever carries
  logic [1:0]         result_r;
  logic               result_q_r;

  // emit walk context
  logic        em_active_r;
  logic [3:0]  em_kind_r;
  logic [15:0] em_dt_r, em_di_r;
  logic [15:0] em_arg0_r, em_arg1_r;
  logic [63:0] em_excl_r;
  logic        em_excl_v_r;
  logic        em_amap_remove_r;
  logic [15:0] em_amap_count_r;
  logic        em_dh_r;                 // this job is the DEREG single-shot
  logic        em_cmd_r;
  logic [CIX_W_C-1:0] em_ix_r;

  logic [15:0] uns_cnt_r;
  logic [7:0]  coalesce_r;

  //! ONE shared deadline adder: every arm site adds `now + constant`, so the
  //! constant is muxed (2 LUT/bit) instead of duplicating a 32-bit adder per
  //! site. Lock ops pick the 60 s constant; everything else the 300 s one.
  logic [31:0] deadline_w;
  assign deadline_w = now_ms_i + ((rgy_req_i && rgy_op_i[1])
                                  ? 32'(LOCK_TIMEOUT_MS_P)
                                  : 32'(TL_TIMEOUT_MS_P));

  //! rgy op decode: a new op starts on the request's rising edge only (see
  //! the banner's once-per-edge rule)
  logic rgy_new_w;
  assign rgy_new_w = rgy_req_i && !req_done_r;

  //! lock op outcomes, combinational from current state
  logic lk_is_holder_w;
  assign lk_is_holder_w = lk_held_r && (lk_ctlr_r == rgy_eid_i);
  logic lk_denied_w;
  assign lk_denied_w = lk_held_r && !lk_is_holder_w;

  //! walk-row comparisons (one comparator each; the walk is serial)
  logic wk_hit_w;
  assign wk_hit_w = valid_r[wk_ix_r] && (row_eid_w == hold_eid_r)
                    && (row_mac_w == hold_mac_r);
  logic em_skip_w;
  assign em_skip_w = !valid_r[wk_ix_r]
                     || (em_excl_v_r && (row_eid_w == em_excl_r));

  always_comb begin : counter_event_map
    ctr_ev_ok_w = 1'b0;
    ctr_ev_ix_w = '0;
    if ((ev_ctr_type_i == DT_STREAM_INPUT_C)
        && (32'(ev_ctr_index_i) < N_STREAM_IN_P)) begin
      ctr_ev_ok_w = 1'b1;
      ctr_ev_ix_w = CTX_W_C'(ev_ctr_index_i);
    end else if ((ev_ctr_type_i == DT_STREAM_OUTPUT_C)
                 && (32'(ev_ctr_index_i) < N_STREAM_OUT_P)) begin
      ctr_ev_ok_w = 1'b1;
      ctr_ev_ix_w = CTX_W_C'(N_STREAM_IN_P + 32'(ev_ctr_index_i));
    end else if ((ev_ctr_type_i == DT_AVB_INTERFACE_C)
                 && (ev_ctr_index_i == 16'd0)) begin
      ctr_ev_ok_w = 1'b1;
      ctr_ev_ix_w = CTX_W_C'(N_STREAM_IN_P + N_STREAM_OUT_P);
    end else if ((ev_ctr_type_i == DT_CLOCK_DOMAIN_C)
                 && (ev_ctr_index_i == 16'd0)) begin
      ctr_ev_ok_w = 1'b1;
      ctr_ev_ix_w = CTX_W_C'(N_STREAM_IN_P + N_STREAM_OUT_P + 1);
    end
  end

  assign cmd_class_ok_w = ev_cmd_class_i inside {4'd1, 4'd2, 4'd3, 4'd4,
                                                  4'd5, 4'd7, 4'd8, 4'd9};
  assign cmd_push_w = ev_cmd_i && cmd_class_ok_w
                      && (cmdq_count_r < 5'(CMDQ_N_C));

  always_comb begin : monitor_pick
    mon_pick_ok_w = 1'b0;
    mon_pick_ix_w = '0;
    ca_pick_ok_w  = 1'b0;
    ca_pick_ix_w  = '0;
    ca_cancel_ok_w = 1'b0;
    ca_cancel_ix_w = '0;
    for (int i = int'(N_CTRL_P) - 1; i >= 0; i--) begin
      if (mon_draw_pend_r[i] && valid_r[i] && !ca_probe_r[i]) begin
        mon_pick_ok_w = 1'b1;
        mon_pick_ix_w = CIX_W_C'(i);
      end
      if (ca_pend_r[i] && valid_r[i] && !ca_probe_r[i]
          && !rx_cmd_hit_w[i]) begin
        ca_pick_ok_w = 1'b1;
        ca_pick_ix_w = CIX_W_C'(i);
      end
      if (rx_cmd_hit_w[i] && ca_probe_r[i]) begin
        ca_cancel_ok_w = 1'b1;
        ca_cancel_ix_w = CIX_W_C'(i);
      end
    end
  end

  always_comb begin : command_registry_hit
    rx_cmd_hit_w = '0;
    for (int unsigned i = 0; i < N_CTRL_P; i++) begin
      rx_cmd_hit_w[i] = rx_cmd_valid_i && valid_r[i]
                        && (rows_r[i][127:64] == rx_cmd_eid_i)
                        && (rows_r[i][63:16] == rx_cmd_mac_i);
    end
  end

  always_comb begin : ca_request
    ca_valid_o    = ca_pick_ok_w;
    ca_owner_o    = 4'(ca_pick_ix_w);
    ca_ctlr_eid_o = rows_r[ca_pick_ix_w][127:64];
    ca_mac_o      = rows_r[ca_pick_ix_w][63:16];
    // A TIME_LIMITED drain can remove and later reuse a row while its old
    // availability exchange is still live. Cancel before clearing the row,
    // just as an incoming command cancels a superseded probe.
    ca_cancel_valid_o = ca_cancel_ok_w
                        || ((n_st_r == N_DRAIN) && ca_probe_r[pd_ix_w]);
    ca_cancel_owner_o = ((n_st_r == N_DRAIN) && ca_probe_r[pd_ix_w])
                        ? 4'(pd_ix_w) : 4'(ca_cancel_ix_w);
  end

  //! emit pick: the class priority is fixed - the single-shot DEREGISTER
  //! first (its controller is already gone from the table), then lock, then
  //! entity-wide classes, then per-stream ones
  logic        pick_any_w;
  logic [3:0]  pick_kind_w;
  logic [15:0] pick_dt_w, pick_di_w;
  logic [15:0] pick_arg0_w, pick_arg1_w;
  logic        pick_cmd_w;
  logic [CTX_W_C-1:0] pick_ctr_ix_w;
  always_comb begin : emit_pick
    pick_any_w  = 1'b1;
    pick_kind_w = PP_UNS_LOCK_C;
    pick_dt_w   = 16'h0000;             // ENTITY
    pick_di_w   = 16'd0;
    pick_arg0_w = 16'd0;
    pick_arg1_w = 16'd0;
    pick_cmd_w  = 1'b0;
    pick_ctr_ix_w = '0;
    if (pe_lock_r) begin
      pick_kind_w = PP_UNS_LOCK_C;
    end else if (cmdq_count_r != 5'd0) begin
      pick_cmd_w = 1'b1;
      pick_dt_w  = cmdq_type_r[cmdq_rd_r];
      pick_di_w  = cmdq_index_r[cmdq_rd_r];
      pick_arg0_w = cmdq_arg0_r[cmdq_rd_r];
      pick_arg1_w = cmdq_arg1_r[cmdq_rd_r];
      unique case (cmdq_class_r[cmdq_rd_r])
        4'd1: pick_kind_w = PP_UNS_CFG_C;
        4'd2: pick_kind_w = PP_UNS_SFMT_C;
        4'd3: pick_kind_w = PP_UNS_SINFO_C;
        4'd4: pick_kind_w = PP_UNS_CTRL_C;
        4'd5: pick_kind_w = PP_UNS_SRATE_C;
        4'd7: pick_kind_w = PP_UNS_NAME_C;
        4'd8: pick_kind_w = PP_UNS_CLKS_C;
        4'd9: pick_kind_w = PP_UNS_STRM_C;
        default: pick_kind_w = PP_UNS_DEREG_C;
      endcase
    end else if (pe_amap_r) begin
      pick_kind_w = PP_UNS_AMAP_C;
      pick_dt_w   = amap_type_r;
      pick_di_w   = amap_index_r;
    end else if (pe_avb_r) begin
      pick_kind_w = PP_UNS_AVB_C;
      pick_dt_w   = 16'h0009;           // AVB_INTERFACE
    end else if (pe_asp_r) begin
      pick_kind_w = PP_UNS_ASP_C;
      pick_dt_w   = 16'h0009;
    end else begin
      pick_any_w = 1'b0;
      for (int unsigned c = 0; c < N_CTR_DESC_C; c++) begin
        if (!pick_any_w && ctr_pend_r[c]) begin
          pick_any_w    = 1'b1;
          pick_kind_w   = PP_UNS_CTRS_C;
          pick_ctr_ix_w = CTX_W_C'(c);
          if (c < N_STREAM_IN_P) begin
            pick_dt_w = DT_STREAM_INPUT_C;
            pick_di_w = 16'(c);
          end else if (c < (N_STREAM_IN_P + N_STREAM_OUT_P)) begin
            pick_dt_w = DT_STREAM_OUTPUT_C;
            pick_di_w = 16'(c - N_STREAM_IN_P);
          end else if (c == (N_STREAM_IN_P + N_STREAM_OUT_P)) begin
            pick_dt_w = DT_AVB_INTERFACE_C;
            pick_di_w = 16'd0;
          end else begin
            pick_dt_w = DT_CLOCK_DOMAIN_C;
            pick_di_w = 16'd0;
          end
        end
      end
      for (int unsigned s = 0; s < N_STREAM_IN_P; s++) begin
        if (!pick_any_w && pe_sin_r[s]) begin
          pick_any_w  = 1'b1;
          pick_kind_w = PP_UNS_STRI_C;
          pick_dt_w   = 16'h0005;       // STREAM_INPUT
          pick_di_w   = 16'(s);
        end
      end
      for (int unsigned s = 0; s < N_STREAM_OUT_P; s++) begin
        if (!pick_any_w && pe_sout_r[s]) begin
          pick_any_w  = 1'b1;
          pick_kind_w = PP_UNS_STRI_C;
          pick_dt_w   = 16'h0006;       // STREAM_OUTPUT
          pick_di_w   = 16'(s);
        end
      end
    end
  end

  //! expiry intake: registry rows own {PP_OWN_NTFY_C + i}, the lock owns
  //! PP_OWN_LOCK_C; both also match on the armed slot, like the originator
  logic        exp_row_w, exp_lock_w, exp_mon_w;
  logic [CIX_W_C-1:0] exp_ix_w;
  assign exp_ix_w  = tmr_exp_owner_i[CIX_W_C-1:0];
  assign exp_row_w = tmr_exp_valid_i
      && (tmr_exp_owner_i[7:CIX_W_C] == PP_OWN_NTFY_C[7:CIX_W_C])
      && (tmr_exp_slot_i == TMR_AW_C'(TMR_REGMON_BASE_P + 32'(exp_ix_w)));
  assign exp_lock_w = tmr_exp_valid_i && (tmr_exp_owner_i == PP_OWN_LOCK_C)
      && (tmr_exp_slot_i == TMR_AW_C'(TMR_LOCK_SLOT_P));
  assign exp_mon_w = tmr_exp_valid_i
      && (tmr_exp_owner_i[7:CIX_W_C] == PP_OWN_CMON_C[7:CIX_W_C])
      && (tmr_exp_slot_i == TMR_AW_C'(TMR_REGMON_BASE_P + N_CTRL_P
                                      + 32'(exp_ix_w)));

  //! parked-expiry drain pick (lowest index first; order is immaterial)
  logic               pd_any_w;
  logic [CIX_W_C-1:0] pd_ix_w;
  always_comb begin : pend_pick
    pd_any_w = 1'b0;
    pd_ix_w  = '0;
    for (int i = int'(N_CTRL_P) - 1; i >= 0; i--) begin
      if (pend_r[i]) begin
        pd_any_w = 1'b1;
        pd_ix_w  = CIX_W_C'(i);
      end
    end
  end

  // ---- read index: whichever duty the FSM is on ---------------------------
  always_comb begin : read_mux
    unique case (n_st_r)
      N_DRAIN:  rd_ix_w = pd_ix_w;
      default:  rd_ix_w = wk_ix_r;
    endcase
  end

  //! the gather beat is held while an op is unfinished; a state query
  //! answers in the N_ANS cycle like an op does
  assign rgy_wait_o = (n_st_r != N_ANS);
  assign rgy_data_o = result_q_r ? (lk_held_r ? lk_ctlr_r : 64'd0)
                                 : {62'd0, result_r};

  assign uns_valid_o      = (n_st_r == N_EMIT_WAIT);
  assign uns_kind_o       = em_kind_r;
  assign uns_desc_type_o  = em_dt_r;
  assign uns_desc_index_o = em_di_r;
  assign uns_ctlr_eid_o   = hold_eid_r;
  assign uns_mac_o        = hold_mac_r;
  assign uns_seq_o        = hold_seq_r;
  assign uns_amap_remove_o = em_amap_remove_r;
  assign uns_amap_count_o  = em_amap_count_r;
  assign uns_arg0_o        = em_arg0_r;
  assign uns_arg1_o        = em_arg1_r;
  // Holding the command path while a class is draining makes the finite
  // event queue lossless under sustained controller traffic. It also keeps
  // the mapping staging RAM intact until its unsolicited body is consumed.
  assign amap_busy_o = dh_v_r || em_active_r || pe_lock_r || pe_amap_r
                       || pe_avb_r || pe_asp_r || (|pe_sin_r) || (|pe_sout_r)
                       || (cmdq_count_r != 5'd0) || (|ctr_pend_r);
  assign prng_draw_kind_o = 3'd4;       // KL_pp_prng: uniform 30..60 seconds

  assign dbg_uns_cnt_o  = uns_cnt_r;
  assign dbg_coalesce_o = coalesce_r;

  always_comb begin : reg_count
    dbg_reg_cnt_o = 8'd0;
    for (int unsigned i = 0; i < N_CTRL_P; i++) begin
      dbg_reg_cnt_o = dbg_reg_cnt_o + {7'd0, valid_r[i]};
    end
  end

  // ---- the machine --------------------------------------------------------
  always_ff @(posedge clk_i) begin : notify_core
    if (!rst_n) begin
      n_st_r      <= N_IDLE;
      valid_r     <= '0;
      tl_r        <= '0;
      pend_r      <= '0;
      lk_held_r   <= 1'b0;
      lk_ctlr_r   <= 64'd0;
      pe_sin_r    <= '0;
      pe_sout_r   <= '0;
      pe_avb_r    <= 1'b0;
      pe_asp_r    <= 1'b0;
      pe_lock_r   <= 1'b0;
      pe_amap_r   <= 1'b0;
      cmdq_wr_r   <= 4'd0;
      cmdq_rd_r   <= 4'd0;
      cmdq_count_r <= 5'd0;
      cmdq_drop_r <= 16'd0;
      ctr_dirty_r <= '0;
      ctr_pend_r  <= '0;
      ctr_sent_r  <= '0;
      for (int unsigned c = 0; c < N_CTR_DESC_C; c++) ctr_last_r[c] <= 32'd0;
      mon_draw_pend_r <= '0;
      ca_pend_r       <= '0;
      ca_probe_r      <= '0;
      mon_draw_wait_r <= 1'b0;
      mon_draw_ix_r   <= '0;
      prng_draw_req_o <= 1'b0;
      mon_arm_valid_o <= 1'b0;
      mon_arm_cancel_o <= 1'b0;
      mon_arm_slot_o <= '0;
      mon_arm_owner_o <= '0;
      mon_arm_deadline_ms_o <= 32'd0;
      amap_remove_r <= 1'b0;
      amap_type_r <= 16'd0;
      amap_index_r <= 16'd0;
      amap_count_r <= 16'd0;
      amap_excl_r <= 64'd0;
      lockx_eid_r <= 64'd0;
      lockx_v_r   <= 1'b0;
      dh_v_r      <= 1'b0;
      dh_eid_r    <= 64'd0;
      dh_mac_r    <= 48'd0;
      dh_seq_r    <= 16'd0;
      req_done_r  <= 1'b0;
      wk_ix_r     <= '0;
      wk_match_r  <= 1'b0;
      wk_match_ix_r  <= '0;
      wk_match_seq_r <= 16'd0;
      wk_free_r   <= 1'b0;
      wk_free_ix_r   <= '0;
      hold_eid_r  <= 64'd0;
      hold_mac_r  <= 48'd0;
      hold_seq_r  <= 16'd0;
      op_tl_r     <= 1'b0;
      op_dereg_r  <= 1'b0;
      result_r    <= 2'd0;
      result_q_r  <= 1'b0;
      em_active_r <= 1'b0;
      em_kind_r   <= 4'd0;
      em_dt_r     <= 16'd0;
      em_di_r     <= 16'd0;
      em_arg0_r   <= 16'd0;
      em_arg1_r   <= 16'd0;
      em_excl_r   <= 64'd0;
      em_excl_v_r <= 1'b0;
      em_amap_remove_r <= 1'b0;
      em_amap_count_r <= 16'd0;
      em_dh_r     <= 1'b0;
      em_cmd_r    <= 1'b0;
      em_ix_r     <= '0;
      uns_cnt_r   <= 16'd0;
      coalesce_r  <= 8'd0;
      wr_en_r     <= 1'b0;
      wr_ix_r     <= '0;
      wr_row_r    <= '0;
      tmr_arm_valid_o       <= 1'b0;
      tmr_arm_cancel_o      <= 1'b0;
      tmr_arm_slot_o        <= '0;
      tmr_arm_owner_o       <= '0;
      tmr_arm_deadline_ms_o <= 32'd0;
    end else begin
      wr_en_r         <= 1'b0;
      tmr_arm_valid_o <= 1'b0;
      prng_draw_req_o <= 1'b0;
      mon_arm_valid_o <= 1'b0;
      if (!rgy_req_i) req_done_r <= 1'b0;

      // ---- event intake (independent of the FSM) -------------------------
      for (int unsigned s = 0; s < N_STREAM_IN_P; s++) begin
        if (ev_stri_in_i[s]) pe_sin_r[s] <= 1'b1;
      end
      for (int unsigned s = 0; s < N_STREAM_OUT_P; s++) begin
        if (ev_stri_out_i[s]) pe_sout_r[s] <= 1'b1;
      end
      if (ev_avb_i) pe_avb_r <= 1'b1;
      if (ev_asp_i) pe_asp_r <= 1'b1;
      if (ev_amap_i) begin
        pe_amap_r <= 1'b1;
        amap_remove_r <= ev_amap_remove_i;
        amap_type_r <= ev_amap_type_i;
        amap_index_r <= ev_amap_index_i;
        amap_count_r <= ev_amap_count_i;
        amap_excl_r <= ev_amap_excl_eid_i;
      end
      if (ev_cmd_i && cmd_class_ok_w) begin
        if (cmd_push_w) begin
          cmdq_class_r[cmdq_wr_r] <= ev_cmd_class_i;
          cmdq_type_r[cmdq_wr_r]  <= ev_cmd_type_i;
          cmdq_index_r[cmdq_wr_r] <= ev_cmd_index_i;
          cmdq_arg0_r[cmdq_wr_r]  <= ev_cmd_arg0_i;
          cmdq_arg1_r[cmdq_wr_r]  <= ev_cmd_arg1_i;
          cmdq_excl_r[cmdq_wr_r]  <= ev_cmd_excl_eid_i;
          cmdq_wr_r    <= cmdq_wr_r + 4'd1;
          cmdq_count_r <= cmdq_count_r + 5'd1;
        end else if (cmdq_drop_r != 16'hFFFF) begin
          cmdq_drop_r <= cmdq_drop_r + 16'd1;
        end
      end

      if (ev_ctr_i && ctr_ev_ok_w) ctr_dirty_r[ctr_ev_ix_w] <= 1'b1;
      for (int unsigned c = 0; c < N_CTR_DESC_C; c++) begin
        if (ctr_dirty_r[c] && !ctr_pend_r[c]
            && (!ctr_sent_r[c]
                || ((now_ms_i - ctr_last_r[c]) >= 32'd1000))) begin
          ctr_dirty_r[c] <= 1'b0;
          ctr_pend_r[c]  <= 1'b1;
        end
      end

      // Any valid command from a registered controller supersedes an old
      // monitor deadline and asks for a fresh independent random interval.
      for (int unsigned i = 0; i < N_CTRL_P; i++) begin
        if (rx_cmd_hit_w[i]) begin
          mon_draw_pend_r[i] <= 1'b1;
          ca_pend_r[i]       <= 1'b0;
          ca_probe_r[i]      <= 1'b0;
        end
      end

      if (exp_mon_w && valid_r[exp_ix_w] && !ca_probe_r[exp_ix_w]
          && !mon_draw_pend_r[exp_ix_w] && !rx_cmd_hit_w[exp_ix_w]
          && !(mon_draw_wait_r && (mon_draw_ix_r == exp_ix_w))) begin
        ca_pend_r[exp_ix_w] <= 1'b1;
      end
      if (ca_valid_o && ca_ready_i) begin
        ca_pend_r[ca_pick_ix_w]  <= 1'b0;
        ca_probe_r[ca_pick_ix_w] <= 1'b1;
      end
      if (ca_rsp_valid_i && (32'(ca_rsp_owner_i) < N_CTRL_P)
          && !rx_cmd_hit_w[ca_rsp_owner_i]
          && valid_r[ca_rsp_owner_i]) begin
        ca_probe_r[ca_rsp_owner_i]      <= 1'b0;
        mon_draw_pend_r[ca_rsp_owner_i] <= 1'b1;
      end
      if (ca_fail_valid_i && (32'(ca_fail_owner_i) < N_CTRL_P)
          && !rx_cmd_hit_w[ca_fail_owner_i]
          && valid_r[ca_fail_owner_i]) begin
        ca_probe_r[ca_fail_owner_i] <= 1'b0;
        pend_r[ca_fail_owner_i]     <= 1'b1;
      end

      if (!mon_draw_wait_r && mon_pick_ok_w && !prng_draw_busy_i) begin
        prng_draw_req_o <= 1'b1;
        mon_draw_wait_r <= 1'b1;
        mon_draw_ix_r   <= mon_pick_ix_w;
        mon_draw_pend_r[mon_pick_ix_w] <= 1'b0;
      end
      if (mon_draw_wait_r && prng_draw_valid_i) begin
        mon_draw_wait_r       <= 1'b0;
        mon_arm_valid_o       <= 1'b1;
        mon_arm_cancel_o      <= 1'b0;
        mon_arm_slot_o        <= TMR_AW_C'(TMR_REGMON_BASE_P + N_CTRL_P
                                           + 32'(mon_draw_ix_r));
        mon_arm_owner_o       <= PP_OWN_CMON_C
                                 | {{(PP_TIMER_OWNER_W_C-CIX_W_C){1'b0}},
                                    mon_draw_ix_r};
        mon_arm_deadline_ms_o <= now_ms_i + 32'(prng_draw_ms_i);
      end

      // ---- registry TL expiry: park; the drain state removes + latches ---
      if (exp_row_w && valid_r[exp_ix_w] && tl_r[exp_ix_w]) begin
        pend_r[exp_ix_w] <= 1'b1;
      end

      // ---- lock expiry: auto-unlock + Table 5.22 notification ------------
      if (exp_lock_w && lk_held_r) begin
        lk_held_r <= 1'b0;
        lk_ctlr_r <= 64'd0;
        if (pe_lock_r) begin
          //! The final coalesced change is caused by timeout, not by the
          //! earlier requester. Clear that command exclusion so every
          //! registered controller observes the resulting unlocked state.
          lockx_v_r <= 1'b0;
          if (coalesce_r != 8'hFF) coalesce_r <= coalesce_r + 8'd1;
        end else begin
          pe_lock_r <= 1'b1;
          lockx_v_r <= 1'b0;            // a timeout excludes nobody
        end
      end

      unique case (n_st_r)
        // ------------------------------------------------------------------
        N_IDLE: begin
          wk_ix_r    <= '0;
          wk_match_r <= 1'b0;
          wk_free_r  <= 1'b0;
          if (rgy_new_w) begin
            req_done_r <= 1'b1;
            result_q_r <= rgy_state_i;
            if (rgy_state_i) begin
              //! lock-holder query: no op, no walk (rgy_data_o routes the
              //! holder eid combinationally off result_q_r)
              n_st_r   <= N_ANS;
            end else if (rgy_op_i[1]) begin
              // ---- LOCK / UNLOCK: no walk, one cycle -----------------
              if (lk_denied_w) begin
                result_r <= 2'd1;                   // ENTITY_LOCKED
              end else if (!rgy_op_i[0]) begin
                // LOCK by the holder (re-arm) or when free (take)
                result_r  <= {!lk_held_r, 1'b0};    // bit1 = changed
                lk_held_r <= 1'b1;
                lk_ctlr_r <= rgy_eid_i;
                tmr_arm_valid_o       <= 1'b1;
                tmr_arm_cancel_o      <= 1'b0;
                tmr_arm_slot_o        <= TMR_AW_C'(TMR_LOCK_SLOT_P);
                tmr_arm_owner_o       <= PP_OWN_LOCK_C;
                tmr_arm_deadline_ms_o <= deadline_w;
                if (!lk_held_r) begin
                  //! took the lock: notify everyone but the taker
                  pe_lock_r   <= 1'b1;
                  lockx_eid_r <= rgy_eid_i;
                  lockx_v_r   <= 1'b1;
                end
              end else begin
                // UNLOCK by the holder, or the already-unlocked query
                result_r <= {lk_held_r, 1'b0};      // bit1 = changed
                if (lk_held_r) begin
                  lk_held_r <= 1'b0;
                  lk_ctlr_r <= 64'd0;
                  tmr_arm_valid_o  <= 1'b1;
                  tmr_arm_cancel_o <= 1'b1;
                  tmr_arm_slot_o   <= TMR_AW_C'(TMR_LOCK_SLOT_P);
                  tmr_arm_owner_o  <= PP_OWN_LOCK_C;
                  tmr_arm_deadline_ms_o <= 32'd0;
                  pe_lock_r   <= 1'b1;
                  lockx_eid_r <= rgy_eid_i;
                  lockx_v_r   <= 1'b1;
                end
              end
              n_st_r <= N_ANS;
            end else begin
              // ---- REGISTER / DEREGISTER: latch + walk -----------------
              hold_eid_r <= rgy_eid_i;
              hold_mac_r <= rgy_mac_i;
              op_tl_r    <= rgy_tl_i;
              op_dereg_r <= rgy_op_i[0];
              n_st_r     <= N_WALK;
            end
          end else if (pd_any_w && !dh_v_r) begin
            //! the drain waits for the previous auto-DEREGISTER to emit -
            //! its row must stay live until the holder frees (the expiry
            //! lands a little late, never lost)
            n_st_r <= N_DRAIN;
          end else if (dh_v_r || em_active_r || pick_any_w) begin
            if (dh_v_r) begin
              //! the single-shot auto-DEREGISTER, from the holder
              em_kind_r <= PP_UNS_DEREG_C;
              em_dt_r   <= 16'd0;
              em_di_r   <= 16'd0;
              em_arg0_r <= 16'd0;
              em_arg1_r <= 16'd0;
              em_dh_r    <= 1'b1;
              em_cmd_r   <= 1'b0;
              hold_eid_r <= dh_eid_r;
              hold_mac_r <= dh_mac_r;
              hold_seq_r <= dh_seq_r;
              n_st_r     <= N_EMIT_WAIT;
            end else begin
              if (!em_active_r) begin
                //! claim the class: pending clears NOW so a mid-walk
                //! re-fire re-queues the class for a second, final round
                em_active_r <= 1'b1;
                em_kind_r   <= pick_kind_w;
                em_dt_r     <= pick_dt_w;
                em_di_r     <= pick_di_w;
                em_arg0_r   <= pick_arg0_w;
                em_arg1_r   <= pick_arg1_w;
                em_cmd_r    <= pick_cmd_w;
                em_ix_r     <= '0;
                if (pick_kind_w == PP_UNS_LOCK_C) begin
                  em_excl_r   <= lockx_eid_r;
                  em_excl_v_r <= lockx_v_r;
                  pe_lock_r   <= 1'b0;
                end else if (pick_kind_w == PP_UNS_AMAP_C) begin
                  em_excl_r <= amap_excl_r;
                  em_excl_v_r <= 1'b1;
                  em_amap_remove_r <= amap_remove_r;
                  em_amap_count_r <= amap_count_r;
                  pe_amap_r <= 1'b0;
                end else if (pick_cmd_w) begin
                  em_excl_r   <= cmdq_excl_r[cmdq_rd_r];
                  em_excl_v_r <= 1'b1;
                  cmdq_rd_r   <= cmdq_rd_r + 4'd1;
                  if (cmd_push_w)
                    cmdq_count_r <= cmdq_count_r;
                  else
                    cmdq_count_r <= cmdq_count_r - 5'd1;
                end else if (pick_kind_w == PP_UNS_CTRS_C) begin
                  em_excl_v_r <= 1'b0;
                  ctr_pend_r[pick_ctr_ix_w] <= 1'b0;
                  // Measure the one-second limit from emission selection,
                  // not from the possibly much earlier pending instant.
                  ctr_sent_r[pick_ctr_ix_w] <= 1'b1;
                  ctr_last_r[pick_ctr_ix_w] <= now_ms_i;
                end else begin
                  em_excl_v_r <= 1'b0;
                  if (pick_kind_w == PP_UNS_AVB_C)      pe_avb_r <= 1'b0;
                  else if (pick_kind_w == PP_UNS_ASP_C) pe_asp_r <= 1'b0;
                  else if (pick_dt_w == 16'h0005) pe_sin_r[pick_di_w[SIX_W_C-1:0]]  <= 1'b0;
                  else                            pe_sout_r[pick_di_w[SOX_W_C-1:0]] <= 1'b0;
                end
                wk_ix_r <= '0;
              end else begin
                wk_ix_r <= em_ix_r;
              end
              em_dh_r <= 1'b0;
              n_st_r  <= N_EMIT_RD;
            end
          end
        end

        // ------------------------------------------------------------------
        N_WALK: begin
          if (wk_hit_w && !wk_match_r) begin
            wk_match_r     <= 1'b1;
            wk_match_ix_r  <= wk_ix_r;
            wk_match_seq_r <= row_seq_w;
          end
          if (!valid_r[wk_ix_r] && !wk_free_r) begin
            wk_free_r    <= 1'b1;
            wk_free_ix_r <= wk_ix_r;
          end
          if (wk_ix_r == CIX_W_C'(N_CTRL_P - 1)) n_st_r <= N_APPLY;
          else                                   wk_ix_r <= wk_ix_r + CIX_W_C'(1);
        end

        // ------------------------------------------------------------------
        N_APPLY: begin
          if (op_dereg_r) begin
            //! idempotent removal (see banner); cancel the row's timer
            result_r <= 2'd0;
            if (wk_match_r) begin
              valid_r[wk_match_ix_r] <= 1'b0;
              tl_r[wk_match_ix_r]    <= 1'b0;
              pend_r[wk_match_ix_r]  <= 1'b0;
              tmr_arm_valid_o  <= 1'b1;
              tmr_arm_cancel_o <= 1'b1;
              tmr_arm_slot_o   <= TMR_AW_C'(TMR_REGMON_BASE_P + 32'(wk_match_ix_r));
              tmr_arm_owner_o  <= PP_OWN_NTFY_C | {{(PP_TIMER_OWNER_W_C-CIX_W_C){1'b0}}, wk_match_ix_r};
              tmr_arm_deadline_ms_o <= 32'd0;
              mon_draw_pend_r[wk_match_ix_r] <= 1'b0;
              ca_pend_r[wk_match_ix_r]       <= 1'b0;
              ca_probe_r[wk_match_ix_r]      <= 1'b0;
              if (mon_draw_wait_r && (mon_draw_ix_r == wk_match_ix_r))
                mon_draw_wait_r <= 1'b0;
              mon_arm_valid_o       <= 1'b1;
              mon_arm_cancel_o      <= 1'b1;
              mon_arm_slot_o        <= TMR_AW_C'(TMR_REGMON_BASE_P + N_CTRL_P
                                                  + 32'(wk_match_ix_r));
              mon_arm_owner_o       <= PP_OWN_CMON_C
                                       | {{(PP_TIMER_OWNER_W_C-CIX_W_C){1'b0}},
                                          wk_match_ix_r};
              mon_arm_deadline_ms_o <= 32'd0;
            end
          end else if (wk_match_r || wk_free_r) begin
            //! refresh keeps the row's Sequence ID; a new row starts at 0
            //! (Milan SS5.4.2.21). Either way the parked fire is stale.
            result_r <= 2'd0;
            wr_en_r  <= 1'b1;
            wr_ix_r  <= wk_match_r ? wk_match_ix_r : wk_free_ix_r;
            wr_row_r <= {hold_eid_r, hold_mac_r,
                         wk_match_r ? wk_match_seq_r : 16'd0};
            valid_r[wk_match_r ? wk_match_ix_r : wk_free_ix_r] <= 1'b1;
            tl_r[wk_match_r ? wk_match_ix_r : wk_free_ix_r]    <= op_tl_r;
            pend_r[wk_match_r ? wk_match_ix_r : wk_free_ix_r]  <= 1'b0;
            mon_draw_pend_r[wk_match_r ? wk_match_ix_r : wk_free_ix_r] <= 1'b1;
            ca_pend_r[wk_match_r ? wk_match_ix_r : wk_free_ix_r] <= 1'b0;
            ca_probe_r[wk_match_r ? wk_match_ix_r : wk_free_ix_r] <= 1'b0;
            tmr_arm_valid_o  <= 1'b1;
            tmr_arm_cancel_o <= !op_tl_r;
            tmr_arm_slot_o   <= TMR_AW_C'(TMR_REGMON_BASE_P
                                + 32'(wk_match_r ? wk_match_ix_r : wk_free_ix_r));
            tmr_arm_owner_o  <= PP_OWN_NTFY_C | {{(PP_TIMER_OWNER_W_C-CIX_W_C){1'b0}},
                                wk_match_r ? wk_match_ix_r : wk_free_ix_r};
            tmr_arm_deadline_ms_o <= deadline_w;
          end else begin
            result_r <= 2'd1;                     // full: NO_RESOURCES
          end
          n_st_r <= N_ANS;
        end

        // ------------------------------------------------------------------
        N_ANS: if (!rgy_req_i) n_st_r <= N_IDLE;

        // ------------------------------------------------------------------
        N_DRAIN: begin
          //! remove the expired row and latch its tuple for the single-shot
          //! DEREGISTER notification (Milan Table 5.22: this controller only)
          dh_v_r   <= 1'b1;
          dh_eid_r <= row_eid_w;
          dh_mac_r <= row_mac_w;
          dh_seq_r <= row_seq_w;
          valid_r[pd_ix_w] <= 1'b0;
          tl_r[pd_ix_w]    <= 1'b0;
          pend_r[pd_ix_w]  <= 1'b0;
          mon_draw_pend_r[pd_ix_w] <= 1'b0;
          ca_pend_r[pd_ix_w]       <= 1'b0;
          ca_probe_r[pd_ix_w]      <= 1'b0;
          if (mon_draw_wait_r && (mon_draw_ix_r == pd_ix_w))
            mon_draw_wait_r <= 1'b0;
          mon_arm_valid_o       <= 1'b1;
          mon_arm_cancel_o      <= 1'b1;
          mon_arm_slot_o        <= TMR_AW_C'(TMR_REGMON_BASE_P + N_CTRL_P
                                              + 32'(pd_ix_w));
          mon_arm_owner_o       <= PP_OWN_CMON_C
                                   | {{(PP_TIMER_OWNER_W_C-CIX_W_C){1'b0}},
                                      pd_ix_w};
          mon_arm_deadline_ms_o <= 32'd0;
          n_st_r <= N_IDLE;
        end

        // ------------------------------------------------------------------
        N_EMIT_RD: begin
          if (em_ix_r >= CIX_W_C'(N_CTRL_P - 1) && em_skip_w) begin
            em_active_r <= 1'b0;
            n_st_r      <= N_IDLE;
          end else if (em_skip_w) begin
            em_ix_r <= em_ix_r + CIX_W_C'(1);
            wk_ix_r <= em_ix_r + CIX_W_C'(1);
          end else begin
            hold_eid_r <= row_eid_w;
            hold_mac_r <= row_mac_w;
            hold_seq_r <= row_seq_w;
            n_st_r     <= N_EMIT_WAIT;
          end
        end

        // ------------------------------------------------------------------
        N_EMIT_WAIT: begin
          if (uns_done_i) begin
            n_st_r <= N_EMIT_WB;
          end else if (rgy_new_w) begin
            //! withdrawal (see banner): the engine is provably running a
            //! solicited registry/lock command, so this job was not taken
            n_st_r <= N_IDLE;
          end
        end

        // ------------------------------------------------------------------
        N_EMIT_WB: begin
          //! Milan SS5.4.5.1: increment the entry's Sequence ID after every
          //! send, whether or not the frame made it out
          if (uns_cnt_r != 16'hFFFF) uns_cnt_r <= uns_cnt_r + 16'd1;
          if (em_dh_r) begin
            dh_v_r <= 1'b0;
          end else begin
            wr_en_r  <= 1'b1;
            wr_ix_r  <= em_ix_r;
            wr_row_r <= {hold_eid_r, hold_mac_r, hold_seq_r + 16'd1};
            if (em_ix_r == CIX_W_C'(N_CTRL_P - 1)) em_active_r <= 1'b0;
            else                                   em_ix_r <= em_ix_r + CIX_W_C'(1);
          end
          n_st_r <= N_IDLE;
        end

        default: n_st_r <= N_IDLE;
      endcase
    end
  end

endmodule : KL_aecp_notify
`default_nettype wire
