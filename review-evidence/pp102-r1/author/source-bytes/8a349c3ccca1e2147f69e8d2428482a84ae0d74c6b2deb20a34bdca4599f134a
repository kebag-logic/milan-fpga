/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_acmp_listener.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/05 §4,
//                §5, §6, §6.7; records 07 §4 F07.6; timing 08 §2/§5 F08.1;
//                verification 09 §3 MTXW)
//
//  Description : The ROM-driven Milan listener-SM executor of 05 §4: ONE
//                event-at-a-time executor over per-sink records (the F07.6
//                384-bit record in a sync-read RAM, never a flop mirror)
//                with the full F05.3 transition matrix in a $readmemh'd
//                BRAM-shaped ROM (P-ACMP-TROM-W = 32-bit entries, addressed
//                {event[3:0], state[2:0]}, generated row-by-row from the
//                doc table by rom/gen_ltn_rom.py) and the A1..A17 action
//                primitives of the 05 §6.3 legend hardwired. Consumes the
//                dispatch-in face (BIND_RX / UNBIND_RX / GET_RX_STATE /
//                PROBE_TX_RESPONSE per the 05 §3 guards), the timer-service
//                expiry bus (one shared SM slot per sink, 08 §5 — the
//                expiring T-ID is derived from sm_state), and the EVT_TK_*
//                class-C events. Produces committed 56-byte Milan ACMPDUs
//                (Δ2) into the TX slot pool + a TX request handle, the
//                A15/A8 settle/teardown faces toward the srp+avtp adapters,
//                discovery arm/disarm toward ADP (04 §6.2), NVM mark/clear,
//                and the per-commit notification trigger. GET_RX_STATE is
//                served from the records per F05.14.
//
//                The one design decision that matters: the MATRIX lives in
//                ROM (the Milan/IEEE profile seam of 01 §7) while the
//                actions are hardwired and sequenced in ONE fixed canonical
//                order — A1 A11 A8 A9 A2 A6 A10 A12 A13 A14 A15 A16 A17 A3
//                A7 A4 A5 — which realizes every F05.3 cell's listed action
//                order, so a profile swaps behavior by swapping the ROM
//                image and never touches the datapath.
//
//                Interpretations pinned here (suite-checked):
//                - 'ign'/'note only' cells are inert at every observable
//                  face; the tk_disc/tk_reg record flags still mirror the
//                  discovery SM / srp adapter (bookkeeping, gated by the
//                  cell's VALID bit) — F05.3's dagger conditionals require
//                  it.
//                - A listener command whose listener_entity_id is not ours
//                  is consumed silently (03 §3 V7 routes by EID; answering
//                  LISTENER_UNKNOWN_ID for a foreign EID would make every
//                  listener answer every command).
//                - PROBE_TX_RESPONSE guard (05 §3): {controller EID, talker
//                  EID, talker unique_id, seq} must match the record's
//                  saved probe, else silently ignored.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_acmp_listener
  import pp_pkg::*;
  import pp_acmp_pkg::*;
#(
    //! P-N-STREAM-IN (F01.5): sink records / listener SMs
    parameter int unsigned N_SINKS_P           = 8,
    //! transition-ROM image (rom/gen_ltn_rom.py output)
    parameter string       TROM_HEX_P          = "ltn_rom.hex",
    //! P-RX-SLOTS / P-RX-SLOT-BYTES (F01.5) — must match KL_pp_rx_slots
    parameter int unsigned RX_SLOTS_P          = 4,
    parameter int unsigned RX_SLOT_BYTES_P     = 576,
    //! P-TX-STD-SLOTS / P-TX-OVERSIZE-BYTES (F01.5) — must match KL_pp_tx_slots
    parameter int unsigned TX_STD_SLOTS_P      = 4,
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600,
    //! timer-service slot index width ($clog2 of its SLOTS_P; 89 -> 7)
    parameter int unsigned TMR_SLOT_AW_P       = 7,
    //! first deadline-RAM slot of the per-sink shared ACMP SM slots
    //! (08 §5 allocation order: IF + SI noadp slots come first -> 1 + 8)
    parameter int unsigned TMR_BASE_SLOT_P     = 9,
    //! owner-tag base for the expiry bus (router-assigned range)
    parameter int unsigned TMR_OWNER_BASE_P    = 32,
    //! maximum cycles a started/stopped request may wait for the walker
    parameter int unsigned STRM_TIMEOUT_CYC_P  = 4096,
    //! derived — do not override
    localparam int unsigned SINK_W_C     = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1,
    localparam int unsigned RXS_SLOT_W_C = (RX_SLOTS_P > 1) ? $clog2(RX_SLOTS_P) : 1,
    localparam int unsigned RXS_ADDR_W_C = $clog2(RX_SLOT_BYTES_P),
    localparam int unsigned TXS_SLOT_W_C = $clog2(TX_STD_SLOTS_P + 1),
    localparam int unsigned TXS_LEN_W_C  = $clog2(TX_OVERSIZE_BYTES_P + 1)
) (
    input  wire                          clk_i,           //! core clock (P-CLK-HZ)
    input  wire                          rst_n,           //! sync active-low reset

    input  wire  [63:0]                  entity_id_i,     //! own entity_id (quasi-static)

    //! ---- dispatch-in face (03 §4; plain face, dispatch not yet landed) --
    input  wire                          txn_valid_i,     //! normalized transaction present
    input  wire  pp_txn_t                txn_i,           //! the 03 §4 record (ACMP rows)
    output logic                         txn_ready_o,     //! pop: accept on valid AND ready

    //! ---- EVT_TK_* class-C events in (04 §6.2 + srp adapter, 02 §5) ------
    input  wire                          evt_tk_valid_i,  //! event present (sticky until ack)
    input  wire  [1:0]                   evt_tk_kind_i,   //! TK_KIND_*_C
    input  wire                          evt_tk_failed_i, //! with REG: attr is Talker Failed
    input  wire  [15:0]                  evt_tk_sink_i,   //! sink index payload
    output logic                         evt_tk_ready_o,  //! ack (accept on valid AND ready)

    //! ---- boot preload face (07 §5.3: restored binding -> PRB_W_AVAIL) ---
    input  wire                          pre_valid_i,     //! preload request (boot restore)
    input  wire  [15:0]                  pre_sink_i,      //! sink index
    input  wire  [63:0]                  pre_talker_eid_i,//! restored talker EID
    input  wire  [15:0]                  pre_talker_uid_i,//! restored talker unique_id
    input  wire  [63:0]                  pre_ctlr_eid_i,  //! restored controller EID
    input  wire                          pre_sw_i,        //! restored STREAMING_WAIT
    input  wire                          pre_started_i,   //! restored started flag
    output logic                         pre_ready_o,     //! accept on valid AND ready

    //! ---- started/stopped face (Milan §5.4.2.19/.20 -> §5.3.8.7) ---------
    //! NOTE on the OTHER STREAMING_WAIT. `f_sw` is the flag the BIND carried
    //! and it is deliberately NOT re-derived from `f_started` here: Milan
    //! Table 5.37 says the ACMP GET_RX_STATE_RESPONSE reports STREAMING_WAIT
    //! as the "value copied from the saved binding parameters", so it is a
    //! record of what the binding asked for. AECP's GET_STREAM_INFO reports
    //! the LIVE state instead (Table 5.9 bit 28, "1 if the Stream Input is
    //! bound and stopped"). Two different questions with two different
    //! answers; making them agree would break the ACMP one.
    //! START/STOP_STREAMING lands here because this record is the ONE place
    //! started/stopped has a lifecycle: §5.3.8.7 calls the state "undefined
    //! when the Stream Input is not bound", A10 clears it on unbind, and the
    //! NVM shadow captures and restores it. It is a HANDSHAKE, not a pulse -
    //! the engine holds its state-port write until `strm_set_ready_o`, so a
    //! request that arrives while this walker is busy is delayed rather than
    //! dropped. Ready means the record commit or required no-op check is
    //! complete, not merely that the local holder accepted the request.
    input  wire                          strm_set_valid_i,//! request present
    input  wire  [15:0]                  strm_set_sink_i, //! Stream Input index
    input  wire                          strm_set_val_i,  //! 1 = started
    output logic                         strm_set_ready_o,//! completed this cycle
    output logic                         strm_set_error_o,//! bounded wait expired

    //! per-sink started/stopped, mirrored off the record RAM's own write bus
    output logic [N_SINKS_P-1:0]         strm_started_o,

    //! ---- timer-service face (KL_pp_timer_service arm/expiry ports) ------
    input  wire  [31:0]                  now_ms_i,        //! absolute ms timebase
    output logic                         tmr_arm_valid_o, //! arm/cancel strobe
    output logic                         tmr_arm_cancel_o,//! 1 = cancel the slot
    output logic [TMR_SLOT_AW_P-1:0]     tmr_arm_slot_o,  //! TMR_BASE_SLOT_P + sink
    output logic [PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_o,//! TMR_OWNER_BASE_P + sink
    output logic [31:0]                  tmr_arm_deadline_ms_o, //! absolute deadline
    input  wire                          tmr_exp_valid_i, //! expiry event
    input  wire  [TMR_SLOT_AW_P-1:0]     tmr_exp_slot_i,  //! expired slot (unused: owner-keyed)
    input  wire  [PP_TIMER_OWNER_W_C-1:0] tmr_exp_owner_i,//! owner tag -> sink

    //! ---- PRNG face (KL_pp_prng draw ports; T-ACMP-DELAY = kind 0) -------
    output logic                         draw_req_o,      //! one-cycle draw request
    output logic [2:0]                   draw_kind_o,     //! constant PRNG_KIND_ACMP_DELAY_C
    input  wire                          draw_busy_i,     //! draw in progress
    input  wire                          draw_valid_i,    //! draw_ms_i holds the result
    input  wire  [15:0]                  draw_ms_i,       //! drawn delay in ms

    //! ---- RX slot pool face (KL_pp_rx_slots read + free ports) -----------
    output logic [RXS_SLOT_W_C-1:0]      rxs_rd_slot_o,   //! payload slot handle
    output logic [RXS_ADDR_W_C-1:0]      rxs_rd_addr_o,   //! ACMPDU byte offset
    output logic                         rxs_rd_en_o,     //! sync-read enable
    input  wire  [7:0]                   rxs_rd_data_i,   //! byte, one cycle later
    output logic                         rxs_free_o,      //! return the slot
    output logic [RXS_SLOT_W_C-1:0]      rxs_free_slot_o, //! which slot

    //! ---- TX slot pool face (KL_pp_tx_slots alloc + write ports) ---------
    output logic                         txs_alloc_req_o, //! one-cycle slot request
    output logic                         txs_oversize_o,  //! ACMP is never Δ8: tied 0
    input  wire                          txs_alloc_gnt_i, //! grant pulse (cycle after req)
    input  wire  [TXS_SLOT_W_C-1:0]      txs_alloc_slot_i,//! granted slot
    output logic [TXS_SLOT_W_C-1:0]      txs_wr_slot_o,   //! slot being written
    output logic [TXS_LEN_W_C-1:0]       txs_wr_addr_o,   //! byte offset
    output logic                         txs_wr_valid_o,  //! byte-write strobe
    output logic [7:0]                   txs_wr_data_o,   //! ACMPDU byte
    output logic                         txs_wr_commit_o, //! commit with wr_len
    output logic [TXS_LEN_W_C-1:0]       txs_wr_len_o,    //! 56 (Milan Δ2)

    //! ---- TX request face (arbiter not yet landed: committed handle) -----
    output logic                         txreq_valid_o,   //! one-cycle request strobe
    output logic [TXS_SLOT_W_C-1:0]      txreq_slot_o,    //! committed tx-slot handle

    //! ---- lock-manager face (A1; level status, 06 §6.8 not yet landed) ---
    input  wire                          lock_held_i,     //! ENTITY lock held
    input  wire  [63:0]                  lock_ctlr_i,     //! holder's controller EID

    //! ---- action faces out (class-C strobes; A-primitives leaving 05) ----
    output logic                         act_settle_o,    //! A15: INPUT_CONFIGURE+ENABLE + SRP listen
    output logic [63:0]                  act_settle_sid_o,//! settled stream_id
    output logic [47:0]                  act_settle_da_o, //! settled stream_dest_mac
    output logic [11:0]                  act_settle_vlan_o,//! settled stream_vlan_id
    output logic                         act_teardown_o,  //! A8: WITHDRAW_LISTENER + INPUT_DISABLE
    output logic                         act_disc_arm_o,  //! A4: arm discovery SM (04 §6.2)
    output logic [63:0]                  act_disc_talker_eid_o, //! talker to watch
    output logic                         act_disc_disarm_o,//! A9: disarm discovery SM
    output logic                         act_nvm_o,       //! A2/A10: NVM binding record touch
    output logic                         act_nvm_set_o,   //! 1 = mark (A2), 0 = clear (A10)
    output logic                         act_notify_o,    //! committed-change trigger (05 §6.3 rule)
    output logic [SINK_W_C-1:0]          act_sink_o,      //! sink for every strobe above

    //! ---- observability (suite shadow of the record RAM write port) ------
    output logic                         dbg_busy_o,      //! executor not idle
    //! started/stopped requests accepted and dropped for an out-of-range
    //! sink. Should read a permanent 0; non-zero means the descriptor image
    //! and this processor's shape disagree. OBSERVABLE AT THIS PORT, and in
    //! simulation - it is deliberately NOT plumbed to a CSR, because that
    //! would be a register-map change for a counter whose only legitimate
    //! value is zero. The point of counting rather than dropping quietly is
    //! that the arm is REACHABLE in a testbench and graded there; a
    //! controller cannot read it.
    output logic [15:0]                  dbg_strq_drop_o,
    //! one pulse per COMMITTED started/stopped transition, with `act_sink_o`
    //! naming the sink. Milan Table 5.22 lists "Started/stopped state (Stream
    //! Input only)" among the changes that must push a GET_STREAM_INFO
    //! unsolicited notification, and this is that trigger.
    //!
    //! It is NOT the other obligation, and the two are easy to conflate:
    //! IEEE §7.5.2 makes START_STREAMING and STOP_STREAMING themselves
    //! unsolicited-response commands ("when an ATDECC Entity sends a response
    //! to one of the commands below with a status code of SUCCESS then it
    //! also sends an unsolicited response"), which Milan §5.4.5.2 restates.
    //! That response is NOT sent: the engine's unsolicited-kind map has no
    //! entry for these opcodes, exactly as it has none for the SET_* family.
    //! It is the same systemic gap, tracked as issue #69, and it is named
    //! here so this trigger is not mistaken for covering it.
    //!
    //! SEPARATE from `act_notify_o`, which fires for every committed record
    //! change - the bind and settle events already have their own terms
    //! upstream, and re-triggering on those would push duplicates.
    output logic                         act_strt_chg_o,
    output logic                         act_strt_cmd_chg_o,
    output logic                         dbg_recwr_o,     //! record write this cycle
    output logic [SINK_W_C-1:0]          dbg_recwr_sink_o,//! written sink
    output logic [ACMP_REC_W_C-1:0]      dbg_recwr_rec_o  //! written record image
);

  // ------------------------------------------------------------ executor SM
  typedef enum logic [4:0] {
    X_INIT       = 5'd0,   // zero-sweep the record RAM after reset
    X_IDLE       = 5'd1,
    X_PRELOAD    = 5'd2,   // boot-restore record write + A4 arm
    X_RDREC      = 5'd3,   // record RAM read issue
    X_LATCH      = 5'd4,   // record read data -> working copy
    X_FETCH      = 5'd5,   // ACMPDU field fetch from the RX slot
    X_CLASS      = 5'd6,   // event classification + ROM read issue
    X_ROM        = 5'd7,   // ROM entry latch, A1 gate, bookkeeping
    X_STEP       = 5'd8,   // canonical-order action walk
    X_DRAW       = 5'd9,   // A12: PRNG draw then arm
    X_BLD_ALLOC  = 5'd10,  // TX slot request pulse
    X_BLD_WAIT   = 5'd11,  // grant wait (retry on miss)
    X_BLD_WR     = 5'd12,  // 56 byte writes
    X_BLD_COMMIT = 5'd13,  // commit + length
    X_BLD_REQ    = 5'd14,  // TX request handle (+ probe T-ACMP-CMD arm)
    X_WB         = 5'd15,  // record write-back + notify
    X_CONSUME    = 5'd16,  // RX slot free, work item retired
    X_STRT_RD    = 5'd17,  // started/stopped request: record RAM read issue
    X_STRT_AP    = 5'd18   // ...apply to f_started if the sink is bound
  } xstate_e;

  // builder PDU kinds
  typedef enum logic [2:0] {
    B_ERR    = 3'd0,  // echo msg+1 with an error status (A1 / unknown uid)
    B_BIND   = 3'd1,  // A3
    B_UNBIND = 3'd2,  // A7
    B_GETRX  = 3'd3,  // A16 (F05.14)
    B_PROBE  = 3'd4   // A5 / A13
  } bkind_e;

  xstate_e             xs_r;
  logic [SINK_W_C:0]   init_cnt_r;

  // accepted work item
  logic                src_txn_r;      // 1 = dispatch txn, 0 = timer/TK event
  logic                src_tmr_r;
  logic                src_strq_r;
  logic [3:0]          msg_x_r;        // ACMP message_type
  logic [4:0]          status_x_r;     // header status (probe responses)
  logic [63:0]         ctlr_x_r;       // controller_entity_id
  logic [15:0]         seq_x_r;        // sequence_id (echoed)
  logic [15:0]         uid16_r;        // listener_unique_id as received
  logic [2:0]          rxslot_r;       // payload handle (PP_SLOT_NULL_C = none)
  logic [SINK_W_C-1:0] sink_r;
  logic [1:0]          tkkind_r;
  logic                tkfail_r;
  logic                errflow_r;      // respond-and-consume path (no write-back)

  // preload latches
  logic [63:0]         preL_talker_eid_r;
  logic [15:0]         preL_talker_uid_r;
  logic [63:0]         preL_ctlr_eid_r;
  logic                preL_sw_r;
  logic                preL_started_r;
  logic                strtL_val_r;    // the bit a START/STOP asked for
  //! ---- the started/stopped request holder ------------------------------
  //! One deep. Capture is internal and deliberately separate from the
  //! interface completion handshake. This lets a request wait while the
  //! walker is busy, but the AECP microprogram cannot emit SUCCESS until the
  //! record commit or no-op examination has finished. A pending request has
  //! a bounded wait. If the current walk does not retire in time, the holder
  //! is discarded before it reaches the record and completion reports an
  //! error. Once this job starts its record read, it has no resource waits.
  logic                strq_pend_r;
  logic                strq_busy_r;
  logic                strq_done_r;
  logic                strq_fail_r;
  localparam int unsigned STRQ_TMO_W_C = $clog2(STRM_TIMEOUT_CYC_P + 1);
  logic [STRQ_TMO_W_C-1:0] strq_tmo_r;
  logic [15:0]         strq_sink_r;
  logic                strq_val_r;
  logic [15:0]         dbg_strq_drop_r;
  //! `f_started` as it stood when this walk loaded the record. Milan Table
  //! 5.22 asks for a push when the started/stopped state CHANGES, and the
  //! walk that changes it is not always the AECP one: 5.5.3.5.6 step 2's
  //! re-bind short-circuit updates the binding parameters - STREAMING_WAIT
  //! among them - so a controller re-binding the same talker with the flag
  //! flipped moves the state without a START/STOP_STREAMING in sight.
  //! Comparing against the loaded value catches every cause instead of
  //! naming them, which is what a trigger keyed on the request alone missed.
  logic                strt_was_r;
  //! BELT AND BRACES, and said so rather than left to be discovered: with
  //! `bind_act_r` below covering every ROM cell that binds, and X_STRT_AP
  //! requiring `f_bound` before it changes anything, no walk today can reach
  //! X_WB with `bnd_was_r` low and the bit changed - removing this term
  //! leaves both suites green. It is kept because it states the CLAUSE's
  //! condition directly ("undefined when the Stream Input is not bound")
  //! rather than relying on the ROM's current action lists to imply it, and
  //! a future cell that binds without A2 would otherwise slip through.
  //!
  //! ...and whether it was BOUND then. Milan §5.3.8.7 calls started/stopped
  //! "undefined when the Stream Input is not bound", so a bind (undefined ->
  //! started) and an unbind (started -> undefined) are not started/stopped
  //! CHANGES and must not push Table 5.22's trigger. They also already pulse
  //! the same per-sink event level from their own terms upstream, so firing
  //! here as well put TWO unsolicited GET_STREAM_INFO frames on the wire per
  //! bind - which is not just noise: it shifted every later response in the
  //! suite by one frame. Requiring bound-before AND bound-after leaves
  //! exactly the two paths that move the bit under a live binding: the AECP
  //! request, and §5.5.3.5.6 step 2's re-bind with STREAMING_WAIT flipped.
  logic                bnd_was_r;
  //! ...and whether this walk RE-BOUND the sink. A BIND_NEW onto a sink that
  //! is already bound runs `A1 A11 A9 A2 A3 A4 A5` - no A10, so `f_bound`
  //! never drops while A2 rewrites `f_started` from the new flags. That is a
  //! third path changing the bit under a live binding, and it already pushes
  //! from A4's discovery arm, so raising the started/stopped trigger beside
  //! it puts a second GET_STREAM_INFO frame on the wire for one event - the
  //! same duplicate this trigger was narrowed to avoid on a fresh bind.
  logic                bind_act_r;

  initial begin : parameter_checks
    if (STRM_TIMEOUT_CYC_P == 0)
      $fatal(1, "STRM_TIMEOUT_CYC_P must be greater than zero");
  end

  // fetched ACMPDU fields (zeroed at accept; big-endian shift-in)
  logic [63:0]         tk_eid_f_r;     // talker_entity_id @20
  logic [15:0]         tk_uid_f_r;     // talker_unique_id @36
  logic [15:0]         flags_f_r;      // flags @50
  logic [63:0]         sid_f_r;        // stream_id @4
  logic [47:0]         da_f_r;         // stream_dest_mac @40
  logic [15:0]         vlan_f_r;       // stream_vlan_id @52
  logic [4:0]          f_idx_r;        // fetch issue index
  logic [4:0]          f_cap_idx_r;    // capture index (issue delayed 1)
  logic                f_cap_v_r;

  // working record + event + ROM entry
  acmp_rec_t           rec_r;
  lsm_event_e          evt_r;
  logic [16:0]         apend_r;        // pending action bitmap (A1 consumed)
  logic [4:0]          ord_r;          // canonical-order step 0..16
  logic                cellmut_r;      // any state-mutating action ran

  // builder
  bkind_e              bk_r;
  logic [3:0]          bmsg_r;         // B_ERR echo message_type
  logic [4:0]          bstat_r;        // B_ERR status
  logic [5:0]          bidx_r;
  logic                bwait_r;       // second grant-wait cycle used
  logic [TXS_SLOT_W_C-1:0] bslot_r;

  logic [15:0]         probe_ctr_r;    // A5 sequence_id source (03 §5)
  logic                draw_issued_r;

  // pending expiries, one per sink (an A11 in flight clears its bit)
  logic [N_SINKS_P-1:0] pendexp_r;

  // ------------------------------------------------------------ RAM: records
  // F07.6 records in a 1W1R sync-read RAM — RAM-shaped by construction,
  // never a flop mirror + wide mux. Deliberately NO reset on the array or
  // its read register (BRAM inference; the X_INIT sweep zeroes content).
  logic [ACMP_REC_W_C-1:0] rec_ram_r [0:N_SINKS_P-1];
  logic [ACMP_REC_W_C-1:0] rec_rdata_r;
  //! typed views of the record RAM's read and write buses. A field select
  //! cannot be taken off a cast expression directly, and naming them once
  //! keeps the write mirror reading the SAME bus the RAM is written from.
  acmp_rec_t               rec_rd_w;
  acmp_rec_t               recwr_rec_w;

  logic                    recwr_en_w;
  logic [SINK_W_C-1:0]     recwr_addr_w;
  logic [ACMP_REC_W_C-1:0] recwr_data_w;
  acmp_rec_t               pre_rec_w;
  acmp_rec_t               wb_rec_w;

  always_ff @(posedge clk_i) begin : rec_ram_wr
    if (recwr_en_w) begin
      rec_ram_r[recwr_addr_w] <= recwr_data_w;
    end
  end

  always_ff @(posedge clk_i) begin : rec_ram_rd
    rec_rdata_r <= rec_ram_r[sink_r];
  end

  // ------------------------------------------------------ ROM: F05.3 matrix
  // 128 x P-ACMP-TROM-W, $readmemh image from rom/gen_ltn_rom.py; sync
  // read (BRAM-shaped). No reset: ROM.
  logic [TROM_W_C-1:0] trom_r [0:TROM_DEPTH_C-1];
  logic [TROM_W_C-1:0] trom_rdata_r;
  lsm_event_e          evt_w;
  logic                probe_match_w;

  initial $readmemh(TROM_HEX_P, trom_r);

  always_ff @(posedge clk_i) begin : trom_rd
    trom_rdata_r <= trom_r[{4'(evt_w), rec_r.sm_state}];
  end

  // ------------------------------------------------- accept-time selections
  logic pend_any_w;
  logic [SINK_W_C-1:0] pend_sink_w;

  always_comb begin : pend_pick
    pend_any_w  = 1'b0;
    pend_sink_w = '0;
    for (int unsigned i = 0; i < N_SINKS_P; i++) begin
      if (!pend_any_w && pendexp_r[i]) begin
        pend_any_w  = 1'b1;
        pend_sink_w = SINK_W_C'(i);
      end
    end
  end

  logic exp_hit_w;
  logic [SINK_W_C-1:0] exp_sink_w;

  assign exp_hit_w  = tmr_exp_valid_i
                      && (32'(tmr_exp_owner_i) >= TMR_OWNER_BASE_P)
                      && (32'(tmr_exp_owner_i) <  TMR_OWNER_BASE_P + N_SINKS_P);
  assign exp_sink_w = SINK_W_C'(32'(tmr_exp_owner_i) - TMR_OWNER_BASE_P);

  // txn pre-decode
  logic txn_acmp_w, txn_msg_ok_w, txn_eid_ok_w, txn_uid_ok_w, txn_has_slot_w;

  assign txn_acmp_w     = (txn_i.protocol == PP_PROTO_ACMP);
  assign txn_msg_ok_w   = (txn_i.msg_type == AMSG_PROBE_TX_RESP_C)
                       || (txn_i.msg_type == AMSG_BIND_RX_CMD_C)
                       || (txn_i.msg_type == AMSG_UNBIND_RX_CMD_C)
                       || (txn_i.msg_type == AMSG_GET_RX_STATE_CMD_C);
  assign txn_eid_ok_w   = (txn_i.target_eid == entity_id_i);
  assign txn_uid_ok_w   = (32'(txn_i.operands.unique_id) < N_SINKS_P);
  assign txn_has_slot_w = (txn_i.rx_slot != PP_SLOT_NULL_C);

  // handshakes (05 §2 serialization: one work item at a time; priority
  // txn > pending expiry > TK event > preload)
  //! EVERY acceptor on this walker has to exclude the holder arm, not just
  //! the one that was noticed first. `strq_pend_r` went in at the TOP of the
  //! X_IDLE priority chain, so on the cycle the holder drains this state
  //! machine is leaving X_IDLE for X_STRT_RD - and any source still being
  //! told "ready" on that cycle is CONSUMED BY ITS PRODUCER and never
  //! serviced. `txn_ready_o` is the expensive one: KL_pp_dispatch feeds it
  //! straight to the pop side of the command FIFO, so an ACMP command at the
  //! head is popped and dropped, its controller times out, and its RX slot
  //! is never freed (only X_CONSUME frees, and this walk never gets there) -
  //! a permanent leak out of a four-slot pool shared with ADP, MAAP, the
  //! talker and AECP.
  assign txn_ready_o    = (xs_r == X_IDLE) && !strq_pend_r;
  assign evt_tk_ready_o = (xs_r == X_IDLE) && !strq_pend_r
                          && !txn_valid_i && !pend_any_w;
  assign strm_set_ready_o = strq_done_r;
  assign strm_set_error_o = strq_fail_r;
  //! ...and the preload face likewise. `KL_acmp_nvm_shadow` treats
  //! `pre_ready_i` as ACCEPTANCE and advances to the next sink on it, so a
  //! ready raised while the walker is about to take the started/stopped job
  //! instead loses that sink's restored binding AND its discovery arm, with
  //! nothing to say it happened - the same silent-drop class this change
  //! exists to remove. See the note on `txn_ready_o` above: all four
  //! acceptors need the term, and fixing only this one left the other three.
  assign pre_ready_o    = (xs_r == X_IDLE) && !strq_pend_r
                          && !txn_valid_i && !pend_any_w
                          && !evt_tk_valid_i;

  // ------------------------------------------------------------- slot fetch
  // ACMPDU byte offsets (F05.13): talker_entity_id @20, talker_unique_id
  // @36, flags @50, stream_id @4, stream_dest_mac @40, stream_vlan_id @52.
  // Fields land MSB-first, so a shift-in per field suffices.
  logic slot_ok_w;
  logic [4:0] f_cnt_w;

  assign slot_ok_w = (rxslot_r != PP_SLOT_NULL_C);
  assign f_cnt_w   = (msg_x_r == AMSG_PROBE_TX_RESP_C) ? 5'd28 : 5'd12;

  function automatic logic [RXS_ADDR_W_C-1:0] fofs_f(input logic [4:0] i);
    logic [9:0] o;
    if (i < 5'd8) begin
      o = 10'd20 + 10'(i);                 // talker_entity_id
    end else if (i < 5'd10) begin
      o = 10'd36 + 10'(i - 5'd8);          // talker_unique_id
    end else if (i < 5'd12) begin
      o = 10'd50 + 10'(i - 5'd10);         // flags
    end else if (i < 5'd20) begin
      o = 10'd4 + 10'(i - 5'd12);          // stream_id
    end else if (i < 5'd26) begin
      o = 10'd40 + 10'(i - 5'd20);         // stream_dest_mac
    end else begin
      o = 10'd52 + 10'(i - 5'd26);         // stream_vlan_id
    end
    return RXS_ADDR_W_C'(o);
  endfunction

  assign rxs_rd_en_o   = (xs_r == X_FETCH) && slot_ok_w && (f_idx_r < f_cnt_w);
  assign rxs_rd_addr_o = fofs_f(f_idx_r);
  assign rxs_rd_slot_o = rxslot_r[RXS_SLOT_W_C-1:0];

  // ------------------------------------------------------- classification
  assign probe_match_w = (ctlr_x_r == rec_r.bind_ctlr_eid)
                      && (tk_eid_f_r == rec_r.talker_eid)
                      && (tk_uid_f_r == rec_r.talker_uid)
                      && (seq_x_r == rec_r.probe_seq);

  always_comb begin : classify
    evt_w = LEV_TMR_CMD;  // spurious-expiry default: '-' in every such cell
    if (src_txn_r) begin
      unique case (msg_x_r)
        AMSG_BIND_RX_CMD_C: begin
          if (rec_r.f_bound && (tk_eid_f_r == rec_r.talker_eid)
              && (tk_uid_f_r == rec_r.talker_uid)) begin
            evt_w = LEV_BIND_SAME;
          end else begin
            evt_w = LEV_BIND_NEW;
          end
        end
        AMSG_UNBIND_RX_CMD_C:    evt_w = LEV_UNBIND;
        AMSG_GET_RX_STATE_CMD_C: evt_w = LEV_GETRX;
        default: begin  // AMSG_PROBE_TX_RESP_C (guard applied in X_CLASS)
          evt_w = (status_x_r == AST_SUCCESS_C) ? LEV_PROBE_OK
                                                : LEV_PROBE_FAIL;
        end
      endcase
    end else if (src_tmr_r) begin
      // one shared SM slot per sink (08 §5): the expiring T-ID is the one
      // the state armed; states without an armed timer classify to a row
      // whose cell is an F05.3 em-dash (proven inert by the suite)
      unique case (rec_r.sm_state)
        3'(LSM_PWD): evt_w = LEV_TMR_DELAY;
        3'(LSM_PWR): evt_w = LEV_TMR_CMD;
        3'(LSM_PW2): evt_w = LEV_TMR_CMD;
        3'(LSM_PWT): evt_w = LEV_TMR_RETRY;
        3'(LSM_SNR): evt_w = LEV_TMR_NOTK;
        default:     evt_w = LEV_TMR_CMD;
      endcase
    end else begin
      unique case (tkkind_r)
        TK_KIND_DISC_C: evt_w = LEV_TK_DISC;
        TK_KIND_DEP_C:  evt_w = LEV_TK_DEP;
        TK_KIND_REG_C:  evt_w = LEV_TK_REG;
        default:        evt_w = LEV_TK_UNREG;
      endcase
    end
  end

  // ROM entry field views
  logic        rom_valid_w, rom_ign_w, rom_cond_w;
  logic [16:0] rom_acts_w;
  logic [2:0]  rom_next_w;

  assign rom_valid_w = trom_rdata_r[TROM_VALID_B_C];
  assign rom_ign_w   = trom_rdata_r[TROM_IGN_B_C];
  assign rom_cond_w  = trom_rdata_r[TROM_COND_B_C];
  assign rom_acts_w  = trom_rdata_r[TROM_ACT_LSB_C +: 17];
  assign rom_next_w  = trom_rdata_r[TROM_NEXT_LSB_C +: 3];

  // dagger resolution (05 §6.3 legend: tk? PWD/A12 : PWA/A17)
  logic [16:0] res_acts_w;
  logic [2:0]  res_next_w;

  always_comb begin : dagger
    res_acts_w = rom_acts_w;
    res_next_w = rom_next_w;
    if (rom_cond_w && !rec_r.f_tk_disc) begin
      res_next_w             = 3'(LSM_PWA);
      res_acts_w[ACT_A12_C]  = 1'b0;
      res_acts_w[ACT_A17_C]  = 1'b1;
    end
  end

  // A1: lock check (05 §6.3 legend; lock manager face is level status)
  logic lock_block_w;
  assign lock_block_w = lock_held_i && (lock_ctlr_i != ctlr_x_r);

  // -------------------------------------------- canonical action execution
  // ONE total order realizing every F05.3 cell's listed order (see banner).
  function automatic logic [4:0] act_order_f(input logic [4:0] k);
    unique case (k)
      5'd0:    return 5'(ACT_A1_C);
      5'd1:    return 5'(ACT_A11_C);
      5'd2:    return 5'(ACT_A8_C);
      5'd3:    return 5'(ACT_A9_C);
      5'd4:    return 5'(ACT_A2_C);
      5'd5:    return 5'(ACT_A6_C);
      5'd6:    return 5'(ACT_A10_C);
      5'd7:    return 5'(ACT_A12_C);
      5'd8:    return 5'(ACT_A13_C);
      5'd9:    return 5'(ACT_A14_C);
      5'd10:   return 5'(ACT_A15_C);
      5'd11:   return 5'(ACT_A16_C);
      5'd12:   return 5'(ACT_A17_C);
      5'd13:   return 5'(ACT_A3_C);
      5'd14:   return 5'(ACT_A7_C);
      5'd15:   return 5'(ACT_A4_C);
      default: return 5'(ACT_A5_C);   // step 16
    endcase
  endfunction

  logic [4:0] cur_act_w;
  assign cur_act_w = act_order_f(ord_r);

  // ------------------------------------------------------------ PDU builder
  // The 56-byte Milan ACMPDU (F05.13) as one 448-bit image; byte idx k is
  // the field octet at wire offset k (big-endian fields).
  logic [3:0]   b_msg_w;
  logic [4:0]   b_status_w;
  logic [63:0]  b_sid_w, b_ctlr_w, b_tkeid_w;
  logic [15:0]  b_tkuid_w, b_luid_w, b_cc_w, b_seq_w, b_flags_w, b_vlan_w;
  logic [47:0]  b_da_w;
  logic [447:0] pdu_w;
  logic [7:0]   pdu_byte_w;
  logic         settled_w, rf_w;

  assign settled_w = (rec_r.sm_state == 3'(LSM_SNR))
                  || (rec_r.sm_state == 3'(LSM_SOK));
  assign rf_w      = (rec_r.sm_state == 3'(LSM_SOK)) && rec_r.f_srp_decl[1];

  always_comb begin : bld_fields
    b_msg_w    = AMSG_GET_RX_STATE_RESP_C;
    b_status_w = AST_SUCCESS_C;
    b_sid_w    = 64'd0;
    b_ctlr_w   = ctlr_x_r;
    b_tkeid_w  = 64'd0;
    b_tkuid_w  = 16'd0;
    b_luid_w   = uid16_r;
    b_da_w     = 48'd0;
    b_cc_w     = 16'd0;
    b_seq_w    = seq_x_r;
    b_flags_w  = 16'd0;
    b_vlan_w   = 16'd0;
    unique case (bk_r)
      B_ERR: begin
        b_msg_w    = bmsg_r;
        b_status_w = bstat_r;
        b_tkeid_w  = tk_eid_f_r;
        b_tkuid_w  = tk_uid_f_r;
      end
      B_BIND: begin
        // A3: SUCCESS {cc=1, FAST_CONNECT=0, SW echoed, RF=0, stream 0}
        b_msg_w   = AMSG_BIND_RX_RESP_C;
        b_tkeid_w = tk_eid_f_r;
        b_tkuid_w = tk_uid_f_r;
        b_cc_w    = 16'd1;
        b_flags_w = flags_f_r & AFLG_STREAMING_WAIT_C;
      end
      B_UNBIND: begin
        // A7: SUCCESS, command talker fields echoed
        b_msg_w   = AMSG_UNBIND_RX_RESP_C;
        b_tkeid_w = tk_eid_f_r;
        b_tkuid_w = tk_uid_f_r;
      end
      B_GETRX: begin
        // A16: F05.14 — SUCCESS always, content by state
        b_msg_w   = AMSG_GET_RX_STATE_RESP_C;
        b_tkeid_w = rec_r.f_bound ? rec_r.talker_eid : 64'd0;
        b_tkuid_w = rec_r.f_bound ? rec_r.talker_uid : 16'd0;
        b_cc_w    = rec_r.f_bound ? 16'd1 : 16'd0;
        b_flags_w = rec_r.f_bound
                    ? (AFLG_FAST_CONNECT_C
                       | (rec_r.f_sw ? AFLG_STREAMING_WAIT_C : 16'd0)
                       | (rf_w ? AFLG_REG_FAILED_C : 16'd0))
                    : 16'd0;
        b_sid_w   = settled_w ? rec_r.settled_stream_id : 64'd0;
        b_da_w    = settled_w ? rec_r.settled_da : 48'd0;
        b_vlan_w  = settled_w ? {4'd0, rec_r.settled_vlan} : 16'd0;
      end
      default: begin
        // B_PROBE — A5/A13: {FAST_CONNECT=1, SW=0, cc=0, stream 0},
        // regenerated from the record (Milan exact duplicate, 03 §5)
        b_msg_w   = AMSG_PROBE_TX_CMD_C;
        b_ctlr_w  = rec_r.bind_ctlr_eid;
        b_tkeid_w = rec_r.talker_eid;
        b_tkuid_w = rec_r.talker_uid;
        b_luid_w  = 16'(32'(sink_r));
        b_seq_w   = rec_r.probe_seq;
        b_flags_w = AFLG_FAST_CONNECT_C;
      end
    endcase
  end

  assign pdu_w = {8'hFC,                       // subtype @0
                  4'h0, b_msg_w,               // h=0, ver=0, message_type @1
                  b_status_w, ACMP_CDL_MILAN_C,// status @2, cdl = 44
                  b_sid_w,                     // stream_id @4
                  b_ctlr_w,                    // controller_entity_id @12
                  b_tkeid_w,                   // talker_entity_id @20
                  entity_id_i,                 // listener_entity_id @28
                  b_tkuid_w,                   // talker_unique_id @36
                  b_luid_w,                    // listener_unique_id @38
                  b_da_w,                      // stream_dest_mac @40
                  b_cc_w,                      // connection_count @46
                  b_seq_w,                     // sequence_id @48
                  b_flags_w,                   // flags @50
                  b_vlan_w,                    // stream_vlan_id @52
                  16'h0000};                   // connected_listeners_entries @54

  assign pdu_byte_w = pdu_w[(9'd440 - {bidx_r, 3'b000}) +: 8];

  // ------------------------------------------------------------ record init
  always_comb begin : pre_rec
    pre_rec_w                  = '0;
    pre_rec_w.sm_state         = 3'(LSM_PWA);
    pre_rec_w.pbsta            = PB_PASSIVE_C;
    pre_rec_w.f_bound          = 1'b1;
    pre_rec_w.f_sw             = preL_sw_r;
    pre_rec_w.f_started        = preL_started_r;
    pre_rec_w.talker_eid       = preL_talker_eid_r;
    pre_rec_w.talker_uid       = preL_talker_uid_r;
    pre_rec_w.bind_ctlr_eid    = preL_ctlr_eid_r;
    pre_rec_w.sm_tmr_handle    = 8'(TMR_BASE_SLOT_P + 32'(sink_r));
  end

  always_comb begin : wb_rec
    wb_rec_w               = rec_r;
    wb_rec_w.sm_tmr_handle = 8'(TMR_BASE_SLOT_P + 32'(sink_r));
  end

  assign recwr_en_w   = ((xs_r == X_INIT) && (init_cnt_r < (SINK_W_C+1)'(N_SINKS_P)))
                      || (xs_r == X_PRELOAD) || (xs_r == X_WB);
  assign rec_rd_w     = acmp_rec_t'(rec_rdata_r);
  assign recwr_rec_w  = acmp_rec_t'(recwr_data_w);
  assign recwr_addr_w = (xs_r == X_INIT) ? init_cnt_r[SINK_W_C-1:0] : sink_r;
  assign recwr_data_w = (xs_r == X_INIT) ? '0
                      : (xs_r == X_PRELOAD) ? ACMP_REC_W_C'(pre_rec_w)
                                            : ACMP_REC_W_C'(wb_rec_w);

  //! The per-sink view the fabric admission gate reads. It is written from
  //! the record RAM's OWN write bus, in the same cycle and from the same data,
  //! so it cannot drift from the records it reports: there is one write and
  //! two destinations, not two writers. That covers every path without naming
  //! any of them — the X_INIT zero sweep, the boot preload, A10's unbind
  //! clear and X_STRT_AP alike.
  always_ff @(posedge clk_i) begin : started_mirror
    if (!rst_n) begin
      strm_started_o <= '0;
    end else if (recwr_en_w) begin
      strm_started_o[recwr_addr_w] <= recwr_rec_w.f_started;
    end
  end

  assign dbg_busy_o       = (xs_r != X_IDLE);
  assign dbg_strq_drop_o  = dbg_strq_drop_r;
  assign dbg_recwr_o      = recwr_en_w;
  assign dbg_recwr_sink_o = recwr_addr_w;
  assign dbg_recwr_rec_o  = recwr_data_w;

  // ------------------------------------------------------------ static outs
  assign draw_kind_o     = PRNG_KIND_ACMP_DELAY_C;
  assign txs_oversize_o  = 1'b0;   // ACMP responses are never Δ8 oversize
  assign txs_wr_slot_o   = bslot_r;
  assign txreq_slot_o    = bslot_r;
  assign rxs_free_slot_o = rxslot_r[RXS_SLOT_W_C-1:0];
  assign act_sink_o      = sink_r;
  assign act_settle_sid_o  = sid_f_r;
  assign act_settle_da_o   = da_f_r;
  assign act_settle_vlan_o = vlan_f_r[11:0];

  // ------------------------------------------------------------ pendexp
  logic pend_clr_a11_w;
  logic pend_clr_pop_w;

  assign pend_clr_a11_w = (xs_r == X_STEP) && (cur_act_w == 5'(ACT_A11_C))
                          && apend_r[ACT_A11_C];
  //! ...and the timer-expiry pop, for the same reason: clearing the pendexp
  //! bit on a cycle the walker spends going to X_STRT_RD loses the expiry,
  //! and a lost T-ACMP-CMD leaves the sink in PB_ACTIVE with no retry.
  assign pend_clr_pop_w = (xs_r == X_IDLE) && !strq_pend_r
                          && !txn_valid_i && pend_any_w;

  always_ff @(posedge clk_i) begin : pendexp
    if (!rst_n) begin
      pendexp_r <= '0;
    end else begin
      // set from the expiry bus; a same-cycle A11 clear wins (the cancel
      // must swallow an expiry launched just before it — 05 §6.3 A11)
      if (exp_hit_w) begin
        pendexp_r[exp_sink_w] <= 1'b1;
      end
      if (pend_clr_a11_w) begin
        pendexp_r[sink_r] <= 1'b0;
      end
      if (pend_clr_pop_w) begin
        pendexp_r[pend_sink_w] <= 1'b0;
      end
    end
  end

  // ------------------------------------------------------------ the engine
  always_ff @(posedge clk_i) begin : engine
    if (!rst_n) begin
      xs_r          <= X_INIT;
      init_cnt_r    <= '0;
      src_txn_r     <= 1'b0;
      src_tmr_r     <= 1'b0;
      src_strq_r    <= 1'b0;
      msg_x_r       <= 4'd0;
      status_x_r    <= 5'd0;
      ctlr_x_r      <= 64'd0;
      seq_x_r       <= 16'd0;
      uid16_r       <= 16'd0;
      rxslot_r      <= PP_SLOT_NULL_C;
      sink_r        <= '0;
      tkkind_r      <= 2'd0;
      tkfail_r      <= 1'b0;
      errflow_r     <= 1'b0;
      preL_talker_eid_r <= 64'd0;
      preL_talker_uid_r <= 16'd0;
      preL_ctlr_eid_r   <= 64'd0;
      preL_sw_r         <= 1'b0;
      preL_started_r    <= 1'b0;
      strtL_val_r       <= 1'b0;
      strq_pend_r       <= 1'b0;
      strq_busy_r       <= 1'b0;
      strq_done_r       <= 1'b0;
      strq_fail_r       <= 1'b0;
      strq_tmo_r        <= '0;
      strq_sink_r       <= 16'd0;
      strq_val_r        <= 1'b0;
      dbg_strq_drop_r   <= 16'd0;
      strt_was_r        <= 1'b0;
      bnd_was_r         <= 1'b0;
      bind_act_r        <= 1'b0;
      act_strt_chg_o    <= 1'b0;
      act_strt_cmd_chg_o <= 1'b0;
      tk_eid_f_r    <= 64'd0;
      tk_uid_f_r    <= 16'd0;
      flags_f_r     <= 16'd0;
      sid_f_r       <= 64'd0;
      da_f_r        <= 48'd0;
      vlan_f_r      <= 16'd0;
      f_idx_r       <= 5'd0;
      f_cap_idx_r   <= 5'd0;
      f_cap_v_r     <= 1'b0;
      rec_r         <= '0;
      evt_r         <= LEV_BIND_SAME;
      apend_r       <= 17'd0;
      ord_r         <= 5'd0;
      cellmut_r     <= 1'b0;
      bk_r          <= B_ERR;
      bmsg_r        <= 4'd0;
      bstat_r       <= 5'd0;
      bidx_r        <= 6'd0;
      bslot_r       <= '0;
      probe_ctr_r   <= 16'd0;
      draw_issued_r <= 1'b0;
      // registered output strobes
      tmr_arm_valid_o       <= 1'b0;
      tmr_arm_cancel_o      <= 1'b0;
      tmr_arm_slot_o        <= '0;
      tmr_arm_owner_o       <= '0;
      tmr_arm_deadline_ms_o <= 32'd0;
      draw_req_o            <= 1'b0;
      txs_alloc_req_o       <= 1'b0;
      txs_wr_addr_o         <= '0;
      txs_wr_valid_o        <= 1'b0;
      txs_wr_data_o         <= 8'd0;
      txs_wr_commit_o       <= 1'b0;
      txs_wr_len_o          <= '0;
      txreq_valid_o         <= 1'b0;
      rxs_free_o            <= 1'b0;
      act_settle_o          <= 1'b0;
      act_teardown_o        <= 1'b0;
      act_disc_arm_o        <= 1'b0;
      act_disc_talker_eid_o <= 64'd0;
      act_disc_disarm_o     <= 1'b0;
      act_nvm_o             <= 1'b0;
      act_nvm_set_o         <= 1'b0;
      act_notify_o          <= 1'b0;
    end else begin
      // one-cycle strobes default low
      tmr_arm_valid_o   <= 1'b0;
      tmr_arm_cancel_o  <= 1'b0;
      draw_req_o        <= 1'b0;
      txs_alloc_req_o   <= 1'b0;
      txs_wr_valid_o    <= 1'b0;
      txs_wr_commit_o   <= 1'b0;
      txreq_valid_o     <= 1'b0;
      rxs_free_o        <= 1'b0;
      act_settle_o      <= 1'b0;
      act_teardown_o    <= 1'b0;
      act_disc_arm_o    <= 1'b0;
      act_disc_disarm_o <= 1'b0;
      act_nvm_o         <= 1'b0;
      act_notify_o      <= 1'b0;
      act_strt_chg_o    <= 1'b0;
      act_strt_cmd_chg_o <= 1'b0;
      f_cap_v_r         <= 1'b0;

      unique case (xs_r)
        // ---------------------------------------------------------- X_INIT
        X_INIT: begin
          if (init_cnt_r < (SINK_W_C+1)'(N_SINKS_P)) begin
            init_cnt_r <= init_cnt_r + (SINK_W_C+1)'(1);
          end else begin
            xs_r <= X_IDLE;
          end
        end

        // ---------------------------------------------------------- X_IDLE
        X_IDLE: begin
          bind_act_r <= 1'b0;
          errflow_r <= 1'b0;
          cellmut_r <= 1'b0;
          apend_r   <= 17'd0;
          ord_r     <= 5'd0;
          f_idx_r   <= 5'd0;
          tk_eid_f_r <= 64'd0;
          tk_uid_f_r <= 16'd0;
          flags_f_r  <= 16'd0;
          sid_f_r    <= 64'd0;
          da_f_r     <= 48'd0;
          vlan_f_r   <= 16'd0;
          //! The holder drains FIRST, ahead of ACMP RX and the timer queue.
          //! It is a two-state job, so it delays an ACMP command by a handful
          //! of cycles; in exchange a sustained ACMP burst can no longer
          //! starve a START/STOP the AECP µCPU is already stalled on.
          //! §5.4.2.19/.20 carry no RX slot of their own - the AECP command
          //! that caused this owns its slot and answers from the µprogram -
          //! so this walk is told there is none to free.
          if (strq_pend_r) begin
            src_txn_r   <= 1'b0;
            src_tmr_r   <= 1'b0;
            src_strq_r  <= 1'b1;
            rxslot_r    <= PP_SLOT_NULL_C;
            sink_r      <= SINK_W_C'(strq_sink_r);
            strtL_val_r <= strq_val_r;
            strq_pend_r <= 1'b0;
            if (32'(strq_sink_r) < N_SINKS_P) begin
              xs_r <= X_STRT_RD;
            end else begin
              //! accepted and dropped - COUNTED, never silent. A stale
              //! descriptor image shipped beside the bitstream is how this
              //! arm stops being unreachable, and then the command would
              //! answer SUCCESS and land nowhere.
              dbg_strq_drop_r <= dbg_strq_drop_r + 16'd1;
              strq_done_r     <= 1'b1;
              strq_fail_r     <= 1'b1;
            end
          end else if (txn_valid_i) begin
            src_txn_r  <= 1'b1;
            src_tmr_r  <= 1'b0;
            src_strq_r <= 1'b0;
            msg_x_r    <= txn_i.msg_type;
            status_x_r <= txn_i.status_in;
            ctlr_x_r   <= txn_i.controller_eid;
            seq_x_r    <= txn_i.sequence_id;
            uid16_r    <= txn_i.operands.unique_id;
            rxslot_r   <= txn_i.rx_slot;
            sink_r     <= SINK_W_C'(txn_i.operands.unique_id);
            if (!txn_acmp_w || !txn_msg_ok_w || !txn_eid_ok_w) begin
              xs_r <= X_CONSUME;         // not ours: consume silently (V7)
            end else if (!txn_uid_ok_w) begin
              if (txn_i.msg_type == AMSG_PROBE_TX_RESP_C) begin
                xs_r <= X_CONSUME;       // invalid uid response: ignore
              end else begin
                // LISTENER_UNKNOWN_ID, state fields undefined (05 §3)
                errflow_r <= 1'b1;
                bk_r      <= B_ERR;
                bstat_r   <= AST_LISTENER_UNKNOWN_ID_C;
                bmsg_r    <= txn_i.msg_type + 4'd1;
                xs_r      <= (txn_i.rx_slot != PP_SLOT_NULL_C) ? X_FETCH
                                                               : X_BLD_ALLOC;
              end
            end else begin
              xs_r <= X_RDREC;
            end
          end else if (pend_any_w) begin
            src_txn_r <= 1'b0;
            src_tmr_r <= 1'b1;
            src_strq_r <= 1'b0;
            rxslot_r  <= PP_SLOT_NULL_C;
            sink_r    <= pend_sink_w;    // pendexp bit cleared alongside
            xs_r      <= X_RDREC;
          end else if (evt_tk_valid_i) begin
            src_txn_r <= 1'b0;
            src_tmr_r <= 1'b0;
            src_strq_r <= 1'b0;
            rxslot_r  <= PP_SLOT_NULL_C;
            tkkind_r  <= evt_tk_kind_i;
            tkfail_r  <= evt_tk_failed_i;
            sink_r    <= SINK_W_C'(evt_tk_sink_i);
            if (32'(evt_tk_sink_i) < N_SINKS_P) begin
              xs_r <= X_RDREC;
            end
            // else: acked and dropped, stay idle
          end else if (pre_valid_i) begin
            src_strq_r         <= 1'b0;
            sink_r            <= SINK_W_C'(pre_sink_i);
            preL_talker_eid_r <= pre_talker_eid_i;
            preL_talker_uid_r <= pre_talker_uid_i;
            preL_ctlr_eid_r   <= pre_ctlr_eid_i;
            preL_sw_r         <= pre_sw_i;
            preL_started_r    <= pre_started_i;
            if (32'(pre_sink_i) < N_SINKS_P) begin
              xs_r <= X_PRELOAD;
            end
          end
        end

        // ------------------------------------------------------- X_PRELOAD
        X_PRELOAD: begin
          // 07 §5.3: restored binding enters PRB_W_AVAIL; A4 arms discovery
          act_disc_arm_o        <= 1'b1;
          act_disc_talker_eid_o <= preL_talker_eid_r;
          xs_r                  <= X_IDLE;
        end

        // ------------------------------------------------------- X_STRT_RD
        X_STRT_RD: begin
          xs_r <= X_STRT_AP;             // rec_rdata_r valid next cycle
        end

        // ------------------------------------------------------- X_STRT_AP
        //! Milan §5.4.2.19: "this command has no effect on a Stream Input
        //! that is not already bound or already started" — so an unbound sink
        //! is left alone entirely (no write-back, no notification), and a
        //! request for the state the record is already in commits nothing.
        //! `cellmut_r` gates BOTH the generic record-change `act_notify_o`
        //! and the started/stopped `act_strt_chg_o` this change adds, and the
        //! second is the one Milan Table 5.22 asks for ("Started/stopped
        //! state (Stream Input only)") and IEEE §7.4.35 restates from the
        //! command's side. Gating on a REAL transition is what keeps a repeat
        //! from pushing a notification that says nothing changed. Issue #69
        //! owns the rest of the trigger SET; this one is here because it did
        //! not exist to be triggered until this command landed.
        X_STRT_AP: begin
          rec_r      <= rec_rd_w;
          strt_was_r <= rec_rd_w.f_started;
          bnd_was_r  <= rec_rd_w.f_bound;
          if (rec_rd_w.f_bound && (rec_rd_w.f_started != strtL_val_r)) begin
            rec_r.f_started <= strtL_val_r;
            cellmut_r       <= 1'b1;
            xs_r            <= X_WB;
          end else begin
            strq_done_r <= 1'b1;
            strq_fail_r <= 1'b0;
            xs_r        <= X_IDLE;
          end
        end

        // --------------------------------------------------------- X_RDREC
        X_RDREC: begin
          xs_r <= X_LATCH;               // rec_rdata_r valid next cycle
        end

        // --------------------------------------------------------- X_LATCH
        X_LATCH: begin
          rec_r      <= acmp_rec_t'(rec_rdata_r);
          strt_was_r <= rec_rd_w.f_started;
          bnd_was_r  <= rec_rd_w.f_bound;
          if (src_txn_r && (msg_x_r != AMSG_GET_RX_STATE_CMD_C)
              && slot_ok_w) begin
            xs_r <= X_FETCH;
          end else begin
            xs_r <= X_CLASS;
          end
        end

        // --------------------------------------------------------- X_FETCH
        X_FETCH: begin
          if (slot_ok_w && (f_idx_r < f_cnt_w)) begin
            f_idx_r <= f_idx_r + 5'd1;
          end
          f_cap_v_r   <= rxs_rd_en_o;
          f_cap_idx_r <= f_idx_r;
          if (f_cap_v_r) begin
            if (f_cap_idx_r < 5'd8) begin
              tk_eid_f_r <= {tk_eid_f_r[55:0], rxs_rd_data_i};
            end else if (f_cap_idx_r < 5'd10) begin
              tk_uid_f_r <= {tk_uid_f_r[7:0], rxs_rd_data_i};
            end else if (f_cap_idx_r < 5'd12) begin
              flags_f_r <= {flags_f_r[7:0], rxs_rd_data_i};
            end else if (f_cap_idx_r < 5'd20) begin
              sid_f_r <= {sid_f_r[55:0], rxs_rd_data_i};
            end else if (f_cap_idx_r < 5'd26) begin
              da_f_r <= {da_f_r[39:0], rxs_rd_data_i};
            end else begin
              vlan_f_r <= {vlan_f_r[7:0], rxs_rd_data_i};
            end
            if (f_cap_idx_r == f_cnt_w - 5'd1) begin
              xs_r <= errflow_r ? X_BLD_ALLOC : X_CLASS;
            end
          end else if (!slot_ok_w) begin
            xs_r <= errflow_r ? X_BLD_ALLOC : X_CLASS;  // no payload: zeros
          end
        end

        // --------------------------------------------------------- X_CLASS
        X_CLASS: begin
          evt_r <= evt_w;                // trom_rdata_r valid next cycle
          if (src_txn_r && (msg_x_r == AMSG_PROBE_TX_RESP_C)
              && !probe_match_w) begin
            xs_r <= X_CONSUME;           // 05 §3: silently ignore
          end else begin
            xs_r <= X_ROM;
          end
        end

        // ----------------------------------------------------------- X_ROM
        X_ROM: begin
          // event bookkeeping (VALID-gated; see banner interpretation)
          if ((evt_r == LEV_TK_DISC) && rom_valid_w) begin
            rec_r.f_tk_disc <= 1'b1;
          end
          if ((evt_r == LEV_TK_DEP) && rom_valid_w) begin
            rec_r.f_tk_disc <= 1'b0;
          end
          if ((evt_r == LEV_TK_REG) && rom_valid_w && !rom_ign_w) begin
            rec_r.f_tk_reg     <= 1'b1;
            rec_r.f_srp_decl[1] <= tkfail_r;
          end
          if (!rom_valid_w || rom_ign_w) begin
            xs_r <= X_WB;                // inert cell: bookkeeping-only WB
          end else if (res_acts_w[ACT_A1_C] && lock_block_w) begin
            // A1 fails: respond CONTROLLER_NOT_AUTHORIZED, abort the cell
            errflow_r <= 1'b1;
            bk_r      <= B_ERR;
            bstat_r   <= AST_CONTROLLER_NOT_AUTH_C;
            bmsg_r    <= msg_x_r + 4'd1;
            xs_r      <= X_BLD_ALLOC;
          end else begin
            rec_r.sm_state <= res_next_w;
            apend_r        <= res_acts_w & ~(17'd1 << ACT_A1_C);
            ord_r          <= 5'd0;
            xs_r           <= X_STEP;
          end
        end

        // ---------------------------------------------------------- X_STEP
        X_STEP: begin
          if (ord_r == 5'd17) begin
            xs_r <= X_WB;
          end else if (!apend_r[cur_act_w]) begin
            ord_r <= ord_r + 5'd1;
          end else begin
            ord_r <= ord_r + 5'd1;       // sub-flows rewind via their exits
            unique case (cur_act_w)
              5'(ACT_A11_C): begin       // stop the active SM timer
                tmr_arm_valid_o  <= 1'b1;
                tmr_arm_cancel_o <= 1'b1;
                tmr_arm_slot_o   <= TMR_SLOT_AW_P'(TMR_BASE_SLOT_P + 32'(sink_r));
                tmr_arm_owner_o  <= PP_TIMER_OWNER_W_C'(TMR_OWNER_BASE_P + 32'(sink_r));
              end
              5'(ACT_A8_C): begin        // teardown SRP + AVTP, clear settled
                act_teardown_o        <= 1'b1;
                rec_r.settled_stream_id <= 64'd0;
                rec_r.settled_da      <= 48'd0;
                rec_r.settled_vlan    <= 12'd0;
                rec_r.f_tk_reg        <= 1'b0;
                rec_r.f_srp_decl      <= 2'd0;
                cellmut_r             <= 1'b1;
              end
              5'(ACT_A9_C): begin        // disarm discovery SM
                act_disc_disarm_o <= 1'b1;
                rec_r.f_tk_disc   <= 1'b0;
                cellmut_r         <= 1'b1;
              end
              5'(ACT_A2_C): begin        // store binding + NVM mark
                bind_act_r          <= 1'b1;
                rec_r.talker_eid    <= tk_eid_f_r;
                rec_r.talker_uid    <= tk_uid_f_r;
                rec_r.bind_ctlr_eid <= ctlr_x_r;
                rec_r.f_sw          <= |(flags_f_r & AFLG_STREAMING_WAIT_C);
                //! Milan §5.3.8.7 leaves started/stopped "undefined when the
                //! Stream Input is not bound", so BINDING is what defines it,
                //! and the BIND_RX_COMMAND says which: IEEE §7.4.35 describes
                //! START_STREAMING as starting "an already connected stream
                //! that was connected via ACMP with the STREAMING_WAIT flag
                //! set", i.e. a bind carrying the flag lands STOPPED and a
                //! bind without it lands STARTED. Deriving it here rather
                //! than leaving f_started at its reset 0 is what keeps the
                //! ordinary bind streaming: the fabric admission gate reads
                //! this bit, so a bind that never set it would connect a
                //! stream that discards every frame.
                rec_r.f_started     <= ~|(flags_f_r & AFLG_STREAMING_WAIT_C);
                rec_r.f_bound       <= 1'b1;
                act_nvm_o           <= 1'b1;
                act_nvm_set_o       <= 1'b1;
                cellmut_r           <= 1'b1;
              end
              5'(ACT_A6_C): begin        // v1.2 re-bind short-circuit
                rec_r.bind_ctlr_eid <= ctlr_x_r;
                rec_r.f_sw          <= |(flags_f_r & AFLG_STREAMING_WAIT_C);
                //! §5.5.3.5.6 step 2 (and its twins in .12/.26/.33/.39/.45):
                //! on a re-bind naming the SAME talker, "update the binding
                //! parameters with the controller entity_id and
                //! STREAMING_WAIT fields". Leaving the started state alone
                //! would let a re-bind asking for stopped be answered SUCCESS
                //! while the stream kept flowing.
                //!
                //! INFERENCE, stated as one: the clause says the saved
                //! PARAMETERS are updated; it does not say the live state
                //! follows. It is read that way here because §5.3.8.7 makes
                //! the state a property of the binding, so a binding whose
                //! STREAMING_WAIT now reads 1 describing a started sink would
                //! be self-contradictory - and Table 5.9 bit 28 would then
                //! disagree with the ACMP answer. The consequence worth
                //! knowing: a controller re-binding to take ownership with
                //! the flag clear RESTARTS a sink another controller had
                //! stopped. That transition does raise Table 5.22's push.
                rec_r.f_started     <= ~|(flags_f_r & AFLG_STREAMING_WAIT_C);
                cellmut_r           <= 1'b1;
              end
              5'(ACT_A10_C): begin       // clear binding + NVM clear
                rec_r.talker_eid    <= 64'd0;
                rec_r.talker_uid    <= 16'd0;
                rec_r.bind_ctlr_eid <= 64'd0;
                rec_r.probe_seq     <= 16'd0;
                rec_r.f_bound       <= 1'b0;
                rec_r.f_sw          <= 1'b0;
                rec_r.f_started     <= 1'b0;
                rec_r.f_retried     <= 1'b0;
                rec_r.pbsta         <= PB_DISABLED_C;
                rec_r.acmpsta       <= 5'd0;
                act_nvm_o           <= 1'b1;
                act_nvm_set_o       <= 1'b0;
                cellmut_r           <= 1'b1;
              end
              5'(ACT_A12_C): begin       // arm T-ACMP-DELAY via PRNG draw
                rec_r.pbsta   <= PB_ACTIVE_C;
                rec_r.acmpsta <= 5'd0;
                cellmut_r     <= 1'b1;
                draw_issued_r <= 1'b0;
                ord_r         <= ord_r;  // hold: X_DRAW advances on return
                xs_r          <= X_DRAW;
              end
              5'(ACT_A13_C): begin       // exact-duplicate probe (same seq)
                rec_r.f_retried <= 1'b1;
                cellmut_r       <= 1'b1;
                bk_r            <= B_PROBE;
                ord_r           <= ord_r;
                xs_r            <= X_BLD_ALLOC;
              end
              5'(ACT_A14_C): begin       // backoff + capture acmpsta
                tmr_arm_valid_o       <= 1'b1;
                tmr_arm_cancel_o      <= 1'b0;
                tmr_arm_slot_o        <= TMR_SLOT_AW_P'(TMR_BASE_SLOT_P + 32'(sink_r));
                tmr_arm_owner_o       <= PP_TIMER_OWNER_W_C'(TMR_OWNER_BASE_P + 32'(sink_r));
                tmr_arm_deadline_ms_o <= now_ms_i + T_ACMP_RETRY_MS_C;
                rec_r.acmpsta         <= (evt_r == LEV_PROBE_FAIL)
                                         ? status_x_r
                                         : AST_LISTENER_TALKER_TIMEOUT_C;
                cellmut_r             <= 1'b1;
              end
              5'(ACT_A15_C): begin       // settle: latch params, arm NOTK
                rec_r.settled_stream_id <= sid_f_r;
                rec_r.settled_da        <= da_f_r;
                rec_r.settled_vlan      <= vlan_f_r[11:0];
                rec_r.f_srp_decl[0]     <= 1'b1;
                rec_r.pbsta             <= PB_COMPLETED_C;
                rec_r.acmpsta           <= 5'd0;
                act_settle_o            <= 1'b1;
                tmr_arm_valid_o         <= 1'b1;
                tmr_arm_cancel_o        <= 1'b0;
                tmr_arm_slot_o          <= TMR_SLOT_AW_P'(TMR_BASE_SLOT_P + 32'(sink_r));
                tmr_arm_owner_o         <= PP_TIMER_OWNER_W_C'(TMR_OWNER_BASE_P + 32'(sink_r));
                tmr_arm_deadline_ms_o   <= now_ms_i + T_ACMP_NOTK_MS_C;
                cellmut_r               <= 1'b1;
              end
              5'(ACT_A16_C): begin       // GET_RX_STATE from the record
                bk_r  <= B_GETRX;
                ord_r <= ord_r;
                xs_r  <= X_BLD_ALLOC;
              end
              5'(ACT_A17_C): begin
                rec_r.pbsta   <= PB_PASSIVE_C;
                rec_r.acmpsta <= 5'd0;
                cellmut_r     <= 1'b1;
              end
              5'(ACT_A3_C): begin        // BIND_RX_RESPONSE SUCCESS
                bk_r  <= B_BIND;
                ord_r <= ord_r;
                xs_r  <= X_BLD_ALLOC;
              end
              5'(ACT_A7_C): begin        // UNBIND_RX_RESPONSE SUCCESS
                bk_r  <= B_UNBIND;
                ord_r <= ord_r;
                xs_r  <= X_BLD_ALLOC;
              end
              5'(ACT_A4_C): begin        // arm discovery SM
                act_disc_arm_o        <= 1'b1;
                act_disc_talker_eid_o <= rec_r.talker_eid;
                rec_r.pbsta           <= PB_PASSIVE_C;
                cellmut_r             <= 1'b1;
              end
              default: begin             // ACT_A5_C: probe #1, fresh seq
                rec_r.probe_seq <= probe_ctr_r;
                probe_ctr_r     <= probe_ctr_r + 16'd1;
                rec_r.f_retried <= 1'b0;
                rec_r.pbsta     <= PB_ACTIVE_C;
                rec_r.acmpsta   <= 5'd0;
                cellmut_r       <= 1'b1;
                bk_r            <= B_PROBE;
                ord_r           <= ord_r;
                xs_r            <= X_BLD_ALLOC;
              end
            endcase
          end
        end

        // ---------------------------------------------------------- X_DRAW
        X_DRAW: begin
          if (draw_valid_i) begin
            tmr_arm_valid_o       <= 1'b1;
            tmr_arm_cancel_o      <= 1'b0;
            tmr_arm_slot_o        <= TMR_SLOT_AW_P'(TMR_BASE_SLOT_P + 32'(sink_r));
            tmr_arm_owner_o       <= PP_TIMER_OWNER_W_C'(TMR_OWNER_BASE_P + 32'(sink_r));
            tmr_arm_deadline_ms_o <= now_ms_i + 32'(draw_ms_i);
            draw_issued_r         <= 1'b0;
            ord_r                 <= ord_r + 5'd1;
            xs_r                  <= X_STEP;
          end else if (!draw_issued_r && !draw_busy_i) begin
            draw_req_o    <= 1'b1;
            draw_issued_r <= 1'b1;
          end
        end

        // ----------------------------------------------------- X_BLD_ALLOC
        X_BLD_ALLOC: begin
          txs_alloc_req_o <= 1'b1;       // one-cycle pulse: one grant max
          bwait_r         <= 1'b0;
          xs_r            <= X_BLD_WAIT;
        end

        // ------------------------------------------------------ X_BLD_WAIT
        // the registered request is visible one cycle after X_BLD_ALLOC and
        // KL_pp_tx_slots pulses its grant the cycle after sampling it, so
        // the grant lands two cycles out: wait both before a retry pulse
        X_BLD_WAIT: begin
          if (txs_alloc_gnt_i) begin
            bslot_r <= txs_alloc_slot_i;
            bidx_r  <= 6'd0;
            xs_r    <= X_BLD_WR;
          end else if (!bwait_r) begin
            bwait_r <= 1'b1;
          end else begin
            xs_r <= X_BLD_ALLOC;         // pool busy: retry
          end
        end

        // -------------------------------------------------------- X_BLD_WR
        X_BLD_WR: begin
          txs_wr_valid_o <= 1'b1;
          txs_wr_addr_o  <= TXS_LEN_W_C'(32'(bidx_r));
          txs_wr_data_o  <= pdu_byte_w;
          if (bidx_r == 6'(ACMP_PDU_BYTES_C - 1)) begin
            xs_r <= X_BLD_COMMIT;
          end else begin
            bidx_r <= bidx_r + 6'd1;
          end
        end

        // ---------------------------------------------------- X_BLD_COMMIT
        X_BLD_COMMIT: begin
          txs_wr_commit_o <= 1'b1;
          txs_wr_len_o    <= TXS_LEN_W_C'(ACMP_PDU_BYTES_C);
          xs_r            <= X_BLD_REQ;
        end

        // ------------------------------------------------------- X_BLD_REQ
        X_BLD_REQ: begin
          txreq_valid_o <= 1'b1;         // committed handle to the arbiter
          if (bk_r == B_PROBE) begin     // A5/A13: arm T-ACMP-CMD
            tmr_arm_valid_o       <= 1'b1;
            tmr_arm_cancel_o      <= 1'b0;
            tmr_arm_slot_o        <= TMR_SLOT_AW_P'(TMR_BASE_SLOT_P + 32'(sink_r));
            tmr_arm_owner_o       <= PP_TIMER_OWNER_W_C'(TMR_OWNER_BASE_P + 32'(sink_r));
            tmr_arm_deadline_ms_o <= now_ms_i + T_ACMP_CMD_MS_C;
          end
          if (errflow_r) begin
            xs_r <= X_CONSUME;           // aborted cell: no write-back
          end else begin
            ord_r <= ord_r + 5'd1;
            xs_r  <= X_STEP;
          end
        end

        // ------------------------------------------------------------ X_WB
        X_WB: begin
          act_notify_o <= cellmut_r;     // committed change -> trigger
          //! WHY `strt_was_r`/`bnd_was_r` are never stale here. X_WB has three
          //! entries: the inert-cell arm and the action-walk exit, both of
          //! which come through X_LATCH, and X_STRT_AP, which loads them
          //! itself. Every one of the thirteen `cellmut_r <= 1'b1` sites is
          //! inside X_STEP's action handlers or X_STRT_AP, so a walk that
          //! reaches X_WB without loading them (the error/builder flow)
          //! necessarily arrives with `cellmut_r` clear and cannot raise the
          //! pulse on a stale comparison. A future path into X_WB that can
          //! set `cellmut_r` must load them too.
          //!
          //! ...and the Table 5.22 started/stopped trigger, on a REAL change
          //! of the bit rather than on the kind of walk that made it. A
          //! repeat START on an already started input leaves the value equal
          //! and pushes nothing, which is what the clause asks ("when one of
          //! these pieces of information CHANGES"); a re-bind that flips
          //! STREAMING_WAIT pushes, which keying on the AECP request alone
          //! did not. `bind_act_r` excludes the walks that RE-BIND, because
          //! those already push from their own discovery/teardown terms; the
          //! paths left are the AECP request and §5.5.3.5.6 step 2's
          //! short-circuit, which runs A6 and no A2.
          act_strt_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound
                            && !bind_act_r
                            && (rec_r.f_started != strt_was_r);
          act_strt_cmd_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound
                                && !bind_act_r && src_strq_r
                                && (rec_r.f_started != strt_was_r);
          if (src_strq_r) begin
            strq_done_r <= 1'b1;
            strq_fail_r <= 1'b0;
          end
          xs_r         <= X_CONSUME;
        end

        // ------------------------------------------------------- X_CONSUME
        X_CONSUME: begin
          if (src_txn_r && slot_ok_w) begin
            rxs_free_o <= 1'b1;          // zero-copy handle returned
          end
          xs_r <= X_IDLE;
        end

        default: xs_r <= X_IDLE;
      endcase

      //! Internal capture runs in every state. `strq_busy_r` remains set
      //! through the external completion handshake, so the valid held by the
      //! microprocessor cannot be mistaken for a second request.
      if (strm_set_valid_i && strm_set_ready_o) begin
        strq_busy_r <= 1'b0;
        strq_done_r <= 1'b0;
        strq_fail_r <= 1'b0;
      end else if (strm_set_valid_i && !strq_busy_r) begin
        strq_pend_r <= 1'b1;
        strq_busy_r <= 1'b1;
        strq_done_r <= 1'b0;
        strq_fail_r <= 1'b0;
        strq_tmo_r  <= '0;
        strq_sink_r <= strm_set_sink_i;
        strq_val_r  <= strm_set_val_i;
      end

      //! Only the pending phase can wait on another walker job. Once the
      //! holder drains, X_STRT_RD, X_STRT_AP and X_WB have no resource wait.
      //! Timeout therefore discards a request before any record side effect.
      if (strq_pend_r && (xs_r != X_IDLE)) begin
        if (strq_tmo_r == STRQ_TMO_W_C'(STRM_TIMEOUT_CYC_P - 1)) begin
          strq_pend_r <= 1'b0;
          strq_done_r <= 1'b1;
          strq_fail_r <= 1'b1;
        end else begin
          strq_tmo_r <= strq_tmo_r + STRQ_TMO_W_C'(1);
        end
      end else if (!strq_pend_r) begin
        strq_tmo_r <= '0;
      end
    end
  end

endmodule : KL_pp_acmp_listener
`default_nettype wire
