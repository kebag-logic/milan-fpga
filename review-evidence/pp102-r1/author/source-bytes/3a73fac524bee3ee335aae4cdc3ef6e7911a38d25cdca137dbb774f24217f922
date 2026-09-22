/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_tx_arbiter.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/03 §8 TX arbitration F03.5, 02 §2
//                 class-A stream F02.4, 08 §2 T-TX-AGING)
//
//  Description : The ONE priority merge for all control-plane TX. N_REQ_P
//                requesters (default 6: AECP-solicited, AECP-unsolicited,
//                ACMP, ADP, SRP, originator/self-CA) each present
//                req_valid_i plus tx_slot_i — a slot already committed in
//                KL_pp_tx_slots — and carry a fixed priority class from
//                PRIO_MAP_P (03 §8: ACMP > AECP solicited + originator >
//                notification/SRP > ADP periodic). A grant starts the
//                pool's serialize port and streams that one frame to
//                ser_last with NO preemption: the F02.4 rule, a grant holds
//                sof -> eof and a higher-priority arrival mid-frame waits.
//
//                Starvation guard (T-TX-AGING, 08 §2 = 10 ms): a
//                per-requester aging counter counts tick_ms_i while the
//                request is pending; at AGING_MS_P the requester outranks
//                natives of every higher class. Pacing (03 §8): after a
//                non-solicited grant, a pending solicited requester
//                (SOLICITED_MASK_P) is served before any further
//                non-solicited frame — >= 1 slot per frame-time stays
//                reserved for solicited responses, and pacing outranks
//                aging so an aged non-solicited flood can never take two
//                back-to-back frames from waiting solicited traffic.
//
//  Decision    : the design decision that matters — NO per-beat watchdog
//                and NO truncation path exist. The reference platform's
//                adp_tx_arbiter truncated on watchdog expiry and emitted
//                valid-CRC frames with lying lengths; here the slot RAM
//                always answers for a committed slot (its serializer
//                stalls, never skips, under backpressure), so a mid-frame
//                hang is structurally impossible and a watchdog could only
//                turn a healthy stall into a corrupt frame. The arbiter is
//                therefore a pure pass-through on the byte lane
//                (ser_* -> tx_*, zero added beats) and only ever decides
//                WHICH frame starts, never how far it gets.
//
//                Precondition (03 §7 lifecycle): req_valid_i implies
//                tx_slot_i is READY with a non-zero committed length; a
//                requester presenting PP_SLOT_NULL_C is ignored rather
//                than allowed to hang the plane waiting for a start.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_tx_arbiter
  import pp_pkg::*;
#(
    //! number of TX requesters (03 §8 default: the six sources of F03.5)
    parameter int unsigned N_REQ_P = 6,
    //! per-requester priority class, 2 b each at [2*i +: 2]; 0 = doc prio 1
    //! (highest) .. 3 = doc prio 4. Default index map (F03.5):
    //!   0 AECP solicited  = 1 | 1 AECP unsolicited = 2 | 2 ACMP     = 0
    //!   3 ADP periodic    = 3 | 4 SRP MRPDU        = 2 | 5 self/CA  = 1
    parameter logic [2*N_REQ_P-1:0] PRIO_MAP_P =
        {2'd1, 2'd2, 2'd3, 2'd0, 2'd2, 2'd1},
    //! bit i = requester i carries solicited responses (pacing-protected):
    //! default ACMP (2), AECP solicited (0), originator self/CA (5)
    parameter logic [N_REQ_P-1:0]   SOLICITED_MASK_P = 6'b100101,
    //! T-TX-AGING in ms ticks (08 §2: 10 ms) — starvation promotion point
    parameter int unsigned AGING_MS_P = 10,
    //! P-TX-STD-SLOTS (F01.5) — sizes ser_slot_o exactly as KL_pp_tx_slots
    parameter int unsigned TX_STD_SLOTS_P = 4,
    //! per-requester grant counter width (wrapping)
    parameter int unsigned CNT_W_P = 16,
    //! slot-handle width; 3 at the F01.5 shape = $bits(PP_SLOT_NULL_C)
    localparam int unsigned SLOT_W_C = $clog2(TX_STD_SLOTS_P + 1)
) (
    input  wire                                clk_i,        //! core clock (P-CLK-HZ domain)
    input  wire                                rst_n,        //! synchronous active-low reset
    input  wire                                tick_ms_i,    //! 1-cycle ms strobe (KL_pp_timer_service tick_ms_o)

    // ---- requesters (one lane per F03.5 source) ---------------------------
    input  wire  [N_REQ_P-1:0]                 req_valid_i,  //! request pending; hold until grant or cancellation
    input  wire  [N_REQ_P-1:0][SLOT_W_C-1:0]   tx_slot_i,    //! committed KL_pp_tx_slots slot per requester
    input  wire                                start_abort_i, //! withdraw selected slot before serializer acceptance
    output logic [N_REQ_P-1:0]                 gnt_o,        //! one-cycle grant pulse: frame accepted for TX
    output logic [N_REQ_P-1:0][CNT_W_P-1:0]    gnt_count_o,  //! per-requester grant counters (wrap at 2^CNT_W_P)

    // ---- serialize port: mirror of KL_pp_tx_slots ser_* -------------------
    output logic                               ser_req_o,    //! start streaming ser_slot_o (pool samples when idle)
    output logic [SLOT_W_C-1:0]                ser_slot_o,   //! slot to stream — the winner's tx_slot_i
    input  wire                                ser_valid_i,  //! stream byte valid (pool)
    input  wire  [7:0]                         ser_data_i,   //! stream byte (pool)
    input  wire                                ser_last_i,   //! high with the final byte of the frame
    output logic                               ser_ready_o,  //! byte consumed this cycle (= tx_ready_i)

    // ---- merged byte stream to the mac_tx async FIFO (02 §2 class A) ------
    output logic                               tx_valid_o,   //! merged stream byte valid
    output logic                               tx_sof_o,     //! high with the first byte of each frame
    output logic [7:0]                         tx_data_o,    //! merged stream byte
    output logic                               tx_eof_o,     //! high with the final byte (= ser_last)
    input  wire                                tx_ready_i    //! downstream FIFO consumes the byte
);

  // ------------------------------------------------------------- geometry
  localparam int unsigned REQ_IX_W_C = (N_REQ_P <= 1) ? 1 : $clog2(N_REQ_P);
  localparam int unsigned AGE_W_C    =
      (AGING_MS_P == 0) ? 1 : $clog2(AGING_MS_P + 1);
  localparam logic [AGE_W_C-1:0] AGE_SAT_C = AGE_W_C'(AGING_MS_P);

  // ------------------------------------------------------------ FSM state
  typedef enum logic [1:0] {
    A_IDLE   = 2'd0,   // no owner: arbitrate
    A_START  = 2'd1,   // ser_req_o asserted, waiting for the pool to stream
    A_STREAM = 2'd2    // frame in flight, ser_req_o released
  } arb_st_e;

  arb_st_e                arb_st_r;
  logic [SLOT_W_C-1:0]    slot_r;         // winner's slot, held sof -> eof
  logic [REQ_IX_W_C-1:0]  owner_r;        // selected requester until acceptance
  logic                   start_sent_r;   // pool accepted the start request
  logic                   sof_pend_r;     // first byte of the frame not yet consumed
  logic                   pace_nonsol_r;  // last granted frame was non-solicited
  logic [N_REQ_P-1:0]     gnt_r;
  logic [AGE_W_C-1:0]     age_r [N_REQ_P];
  logic [CNT_W_P-1:0]     cnt_r [N_REQ_P];

  // --------------------------------------------------------- aged flags
  logic [N_REQ_P-1:0] aged_w;

  always_comb begin : aged_flags
    for (int i = 0; i < int'(N_REQ_P); i++)
      aged_w[i] = (age_r[i] == AGE_SAT_C);
  end

  // ------------------------------------------------------------ selection
  //! REGISTERED slot-side qualification (stage-0 pipeline cut). The
  //! tx_slot_i buses arrive from engine slot registers across the whole
  //! processor, and the != NULL compare used to feed the selection loop and
  //! from there the aging/grant counter enables combinationally - measured
  //! on the reference part as a 16-level, 4-carry failing path
  //! (tx_slot_r -> cnt_r). The qualification now lands in pend_r first;
  //! requests are normally held until grant. A cancellation may withdraw a
  //! request after qualification, so selection also checks the current valid
  //! bit below. One cycle of latency changes which cycle a frame starts.
  logic [N_REQ_P-1:0]    pend_r;
  logic [N_REQ_P-1:0]    pend_w;
  logic                  sol_pend_w;
  logic [N_REQ_P-1:0]    elig_w;
  logic                  pick_ok_w;
  logic [REQ_IX_W_C-1:0] pick_w;

  always_ff @(posedge clk_i) begin : slot_qualify
    if (!rst_n) begin
      pend_r <= '0;
    end else begin
      for (int i = 0; i < int'(N_REQ_P); i++) begin
        pend_r[i] <= req_valid_i[i]
                     && (tx_slot_i[i] != SLOT_W_C'(PP_SLOT_NULL_C));
      end
    end
  end

  always_comb begin : selection
    logic [2:0] key_w, best_w;
    // a PP_SLOT_NULL_C handle means "no payload" (pp_pkg): never a grant.
    // The cast is identity at the F01.5 shape (SLOT_W_C = 3 = handle width).
    // The registered qualifier removes the long slot-compare path, but a
    // requester may withdraw while that registered bit is still high. Keep
    // the current valid bit in the decision so a cancelled queue head cannot
    // be granted one cycle after its slot was released.
    pend_w = pend_r & req_valid_i;
    sol_pend_w = |(pend_w & SOLICITED_MASK_P);
    // pacing first (03 §8): after a non-solicited frame, only solicited
    // requesters are eligible while any wait — pacing outranks aging
    elig_w = (pace_nonsol_r && sol_pend_w) ? (pend_w & SOLICITED_MASK_P)
                                           : pend_w;
    // then rank: {fresh-bit, class} — an aged requester (0_cc) outranks
    // every fresh native (1_cc); ties resolve to the lowest index
    pick_ok_w = 1'b0;
    pick_w    = '0;
    best_w    = 3'b111;
    for (int i = 0; i < int'(N_REQ_P); i++) begin
      key_w = {~aged_w[i], PRIO_MAP_P[2*i +: 2]};
      if (elig_w[i] && (!pick_ok_w || (key_w < best_w))) begin
        pick_ok_w = 1'b1;
        pick_w    = REQ_IX_W_C'(i);
        best_w    = key_w;
      end
    end
  end

  // ------------------------------------------------------- event strobes
  logic select_w, accept_w, abort_w, consume_w, eof_w;

  assign select_w  = (arb_st_r == A_IDLE) && pick_ok_w;
  assign accept_w  = (arb_st_r == A_START) && !start_sent_r
                     && !start_abort_i;
  assign abort_w   = (arb_st_r == A_START) && !start_sent_r
                     && start_abort_i;
  assign consume_w = ser_valid_i && tx_ready_i;
  assign eof_w     = consume_w && ser_last_i;

  // -------------------------------------------------------- grant + frame
  always_ff @(posedge clk_i) begin : arbiter_fsm
    if (!rst_n) begin
      arb_st_r      <= A_IDLE;
      slot_r        <= '0;
      owner_r       <= '0;
      start_sent_r  <= 1'b0;
      sof_pend_r    <= 1'b0;
      pace_nonsol_r <= 1'b0;
      gnt_r         <= '0;
    end else begin
      gnt_r <= '0;
      case (arb_st_r)
        A_IDLE: begin
          if (select_w) begin
            arb_st_r      <= A_START;
            slot_r        <= tx_slot_i[pick_w];
            owner_r       <= pick_w;
            start_sent_r  <= 1'b0;
            sof_pend_r    <= 1'b1;
          end
        end
        A_START: begin
          // A selected request remains abortable until the pool samples its
          // first start request. Only that acceptance emits the public grant.
          if (abort_w) begin
            arb_st_r     <= A_IDLE;
            start_sent_r <= 1'b0;
            sof_pend_r   <= 1'b0;
          end else begin
            if (accept_w) begin
              start_sent_r        <= 1'b1;
              gnt_r[owner_r]      <= 1'b1;
              pace_nonsol_r       <= !SOLICITED_MASK_P[owner_r];
            end
            // hold ser_req_o until the pool visibly streams, then release
            if (sof_pend_r && consume_w) sof_pend_r <= 1'b0;
            if (eof_w)                arb_st_r <= A_IDLE;   // 1-byte frame
            else if (ser_valid_i)     arb_st_r <= A_STREAM;
          end
        end
        A_STREAM: begin
          if (sof_pend_r && consume_w) sof_pend_r <= 1'b0;
          if (eof_w)                arb_st_r <= A_IDLE;
        end
        default: arb_st_r <= A_IDLE;
      endcase
    end
  end

  // ------------------------------------------------------- aging counters
  // count tick_ms_i while pending; reset on grant or request drop — a
  // regularly-served requester never ages, a starved one is promoted at
  // AGE_SAT_C and stays promoted until it is finally granted
  always_ff @(posedge clk_i) begin : aging
    if (!rst_n) begin
      for (int i = 0; i < int'(N_REQ_P); i++) age_r[i] <= '0;
    end else begin
      for (int i = 0; i < int'(N_REQ_P); i++) begin
        if (accept_w && (owner_r == REQ_IX_W_C'(i)))   age_r[i] <= '0;
        else if (!pend_w[i])                           age_r[i] <= '0;
        else if (tick_ms_i && (age_r[i] != AGE_SAT_C))
          age_r[i] <= age_r[i] + AGE_W_C'(1);
      end
    end
  end

  // ------------------------------------------------------- grant counters
  always_ff @(posedge clk_i) begin : grant_counters
    if (!rst_n) begin
      for (int i = 0; i < int'(N_REQ_P); i++) cnt_r[i] <= '0;
    end else if (accept_w) begin
      cnt_r[owner_r] <= cnt_r[owner_r] + CNT_W_P'(1);
    end
  end

  // -------------------------------------------------------------- outputs
  // byte lane is a pure pass-through: the pool's skid IS the backpressure
  assign ser_req_o   = (arb_st_r == A_START)
                       && (start_sent_r || !start_abort_i);
  assign ser_slot_o  = slot_r;
  assign ser_ready_o = tx_ready_i;
  assign tx_valid_o  = ser_valid_i;
  assign tx_data_o   = ser_data_i;
  assign tx_sof_o    = ser_valid_i && sof_pend_r;
  assign tx_eof_o    = ser_valid_i && ser_last_i;
  assign gnt_o       = gnt_r;

  always_comb begin : count_out
    for (int i = 0; i < int'(N_REQ_P); i++) gnt_count_o[i] = cnt_r[i];
  end

endmodule : KL_pp_tx_arbiter
`default_nettype wire
