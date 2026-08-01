/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_pair_zero_fill.sv
  Author      : Kebag Logic

  Date        : 2026-07-28
  Description : Silence filler for unfed capture pair slots - the fabric half
                of Milan v1.2 5.3.7.3.

                THE CLAUSE, quoted because a paraphrase of this exact
                sentence once licensed a defect (the AAF_CTRL bypass,
                VERSION 0x0018): "As long as a PAAD is declaring a Talker
                Advertise attribute and receiving a Listener Ready or
                Listener Ready Failed attribute for a Stream Output, it
                shall be streaming AVTP packets." A talker whose pair slots
                are never strobed never advances nsamp_r, so pend_r never
                sets and it emits NO FRAME AT ALL - a listener that bound it
                got ACMP SUCCESS and then silence-with-no-packets, which is
                exactly the state the clause forbids. Before this module,
                every N>1 shape in this tree had that gap (the W3 finding of
                scripts/check_wire_accountability.py): the AX7101's TDM32
                supplies 16 pair slots against the 32 its eight 8-channel
                talkers consume, so talkers 4-7 were advertised, bindable
                and structurally mute.

                WHAT IT DOES. Tracks which pair slots the physical
                front-end(s) actually strobed, per 48 kHz media-tick period,
                and emits a ZERO-sample pair strobe for every slot that no
                source fed - so every bound talker frames at the class rate,
                carrying real audio where a source exists and legal PCM
                silence where none does. That is what any shipping product
                does with an unpatched input, and silence is a sample value,
                not an error.

                WHY FED-TRACKING AND NOT "APPEND AFTER THE LAST SLOT". An
                append design keys on the front-end's own strobes, so a dead
                front-end (a wedged TDM slave bus, an MMCM that lost lock)
                kills every talker - the exact 5.3.7.3 state again, reached
                through the filler that exists to prevent it. This design
                paces on tick_i (the free-running media grid divider), so a
                slot is filled whenever its source is dead, including ALL of
                them.

                THE TWO-PERIOD RULE. A slot is filled in a tick period only
                if it was fed in NEITHER of the two preceding periods
                (~fed_now & ~fed_prev at the tick edge). A live 48 kHz
                source whose strobe phase sits just after the tick would
                otherwise read as unfed once per beat and collect an extra
                (doubled) sample; with the two-period guard a live slot is
                never filled at any phase, and a slot whose source dies
                starts filling once both windows have emptied - up to two
                periods (~41.7 us, two samples) of gap once, then steady
                silence.

                PLACEMENT. Downstream of the capture/playback pair mux and
                upstream of the packetizer bypass mux, so it covers the
                physical front-ends AND the ALSA-ring playback source. The
                output stage is REGISTERED: every strobe (live pass-through
                or fill) leaves one clk_i cycle after its decision cycle -
                a timing cut, not a semantic one; the packetizer is
                strobe-paced and the fed/pend bookkeeping keys on the
                un-delayed inputs. The
                CHMAP crossbar path (cfg_chmap_enable = 1) bypasses it: a
                software-programmed map owns its own slot coverage. Fills
                are NOT counted in A_AAF_PAIRS (that instrument reports
                captured physical pairs; a synthetic zero must not read as a
                measurement - methodology R5); fill_cnt_o is the fills' own
                honest counter.

  Spec refs   : Milan v1.2 5.3.7.3 (streaming licence, first sentence);
                IEEE 1722-2016 7.3.3 (channels_per_frame the slots feed)
  Company     : Kebag Logic
------------------------------------------------------------------------------
*/

//! Fed-tracked silence filler: every pair slot 0..TOTAL_P-1 strobes at the
//! media tick - real samples pass through, dead slots get {0, 0}.

`default_nettype none

module KL_pair_zero_fill #(
  parameter int unsigned TOTAL_P  = 4,  //! pair slots the packetizer consumes
                                        //! (N_TALKERS x WIRE_CHANS/2)
  parameter int unsigned SLOT_W_P = 5   //! pair-slot bus width downstream
)(
  input  wire                 clk_i,    //! datapath clock
  input  wire                 rst_n,    //! active-low synchronous reset
  input  wire                 tick_i,   //! one-cycle 48 kHz media-grid strobe

  // ---- physical pair stream in (capture/playback mux) ------------------
  input  wire                 pair_valid_i,
  input  wire [SLOT_W_P-1:0]  pair_slot_i,
  input  wire [23:0]          pair_l_i,
  input  wire [23:0]          pair_r_i,

  // ---- filled pair stream out (to the packetizer bypass mux) -----------
  output logic                pair_valid_o,
  output logic [SLOT_W_P-1:0] pair_slot_o,
  output logic [23:0]         pair_l_o,
  output logic [23:0]         pair_r_o,

  // ---- status ----------------------------------------------------------
  output logic [31:0]         fill_cnt_o  //! zero pairs emitted (not pairs
                                          //! captured - R5, see banner)
);

  if (TOTAL_P < 1 || TOTAL_P > (1 << SLOT_W_P))
    $error("KL_pair_zero_fill: TOTAL_P=%0d outside 1..%0d (SLOT_W_P=%0d pair-slot bus).",
           TOTAL_P, 1 << SLOT_W_P, SLOT_W_P);

  //! fed bitmaps: current tick period and the completed one before it
  logic [TOTAL_P-1:0] fed_now_r, fed_prev_r;
  //! slots still owed a zero strobe this period
  logic [TOTAL_P-1:0] pend_r;

  //! priority-encode the lowest pending slot (TOTAL_P <= 32: one scan)
  logic                pend_any_c;
  logic [SLOT_W_P-1:0] pend_slot_c;
  always_comb begin : fill_scan
    pend_any_c  = 1'b0;
    pend_slot_c = '0;
    for (int s = TOTAL_P - 1; s >= 0; s--) begin
      if (pend_r[s]) begin
        pend_any_c  = 1'b1;
        pend_slot_c = SLOT_W_P'(s);
      end
    end
  end : fill_scan

  //! live strobes pass through with priority; fills take the idle cycles.
  //! A 48 kHz period is >1000 datapath cycles and TOTAL_P <= 32, so the
  //! pending set always drains long before the next tick.
  //!
  //! OUTPUT STAGE IS REGISTERED (AX 100 MHz WNS -0.095: pend_r reached the
  //! packetizer's staging-BRAM write enables through this mux and the
  //! datapath bypass mux in one combinational cone). The DECISION stays in
  //! this cycle - live pair wins, else the lowest pending fill - and the
  //! chosen strobe leaves exactly one clk_i cycle later. One decision, one
  //! output cycle, so no strobe is ever lost or doubled; the packetizer is
  //! strobe-paced, so the whole pair stream shifting by a cycle is
  //! invisible downstream. Bookkeeping (fed fold, pend drain, fill_cnt_o)
  //! keys on the UN-delayed inputs, exactly as before.
  always_ff @(posedge clk_i) begin : fill_out
    if (!rst_n) begin
      pair_valid_o <= 1'b0;
      pair_slot_o  <= '0;
      pair_l_o     <= 24'd0;
      pair_r_o     <= 24'd0;
    end else if (pair_valid_i) begin
      pair_valid_o <= 1'b1;
      pair_slot_o  <= pair_slot_i;
      pair_l_o     <= pair_l_i;
      pair_r_o     <= pair_r_i;
    end else begin
      pair_valid_o <= pend_any_c;
      pair_slot_o  <= pend_slot_c;
      pair_l_o     <= 24'd0;
      pair_r_o     <= 24'd0;
    end
  end : fill_out

  //! this cycle's feed, folded combinationally so a strobe landing ON the
  //! tick cycle still counts for the period it closes (a nonblocking set
  //! would lose to the tick branch's fed_now_r <= '0)
  logic [TOTAL_P-1:0] fed_now_c;
  always_comb begin : fill_fold
    fed_now_c = fed_now_r;
    if (pair_valid_i && (32'(pair_slot_i) < TOTAL_P))
      fed_now_c[pair_slot_i[$clog2(TOTAL_P == 1 ? 2 : TOTAL_P)-1:0]] = 1'b1;
  end : fill_fold

  always_ff @(posedge clk_i) begin : fill_track
    if (!rst_n) begin
      fed_now_r  <= '0;
      //! prev resets ALL-FED: the first period after reset fills nothing,
      //! so a front-end gets one full period to prove itself before the
      //! filler decides a slot is dead (the same two-period rule as
      //! steady state, applied to the reset edge)
      fed_prev_r <= '1;
      pend_r     <= '0;
      fill_cnt_o <= 32'd0;
    end else if (tick_i) begin : g_tick
      //! fill what neither of the last two periods fed (see banner)
      pend_r     <= ~fed_now_c & ~fed_prev_r;
      fed_prev_r <= fed_now_c;
      fed_now_r  <= '0;
    end else begin
      fed_now_r <= fed_now_c;
      if (!pair_valid_i && pend_any_c) begin
        pend_r[pend_slot_c[$clog2(TOTAL_P == 1 ? 2 : TOTAL_P)-1:0]] <= 1'b0;
        fill_cnt_o <= fill_cnt_o + 32'd1;
      end
    end
  end : fill_track

endmodule

`default_nettype wire
