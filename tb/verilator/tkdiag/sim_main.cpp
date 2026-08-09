/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_talker_diag_ctx - Milan v1.2 Table 5.4, per
 * Stream Output - and for KL_media_clock_restart, the IEEE 1722-2016 4.4.4.3
 * mr level whose transmitted bit BACKS the MEDIA_RESET counter.
 *
 * The clause text these cases encode (Milan v1.2 5.3.7.7, Table 5.4):
 *
 *  - STREAM_START "Incremented each time the Talker starts streaming";
 *    STREAM_STOP likewise, with the stated invariant "either
 *    STREAM_START=STREAM_STOP+1 (in this case, the Talker is currently
 *    streaming), or STREAM_START=STREAM_STOP".  NOTE what the clause does
 *    NOT say: these two carry no "Reset to 0" sentence, so they must SURVIVE
 *    a start - see T8.
 *  - MEDIA_RESET / TIMESTAMP_UNCERTAIN / FRAMES_TX are each "Incremented at
 *    the end of every observation interval during which ...", interval
 *    "implementation-specific and shall be less than or equal to 1 second",
 *    each followed by "Reset to 0 each time the Talker starts streaming".
 *    So they are INTERVAL counts (eight PDUs in one interval move FRAMES_TX
 *    by exactly one - a raw frame total would read 8000x off at the real
 *    frame rate) and reset-on-start is MANDATED, not a bug.
 *  - TIMESTAMP_UNCERTAIN counts intervals in which tu was set "in any of the
 *    transmitted Stream Data AVTPDUs" - tu high with nothing sent counts
 *    nothing (the difference from the free-running CLKV_TUCNT).
 *  - MEDIA_RESET counts intervals in which mr "has been toggled in any of
 *    the transmitted Stream Data AVTPDUs" - so it is derived from the mr bit
 *    the PDU carried, per context, and CANNOT be a tie-off zero (T10-T12).
 *
 * TICK_CYC_P is 64 in this build; a "period" below is 64 clk cycles.
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vtkdiag_tb_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static Vtkdiag_tb_top* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-60s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    } else {
        printf("  [ok]   %-60s = 0x%llx\n", what, (unsigned long long)got);
    }
}

static void step() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}
static void cyc(int n) { for (int i = 0; i < n; i++) step(); }
// one full observation interval, with margin for the divider phase
static void interval() { cyc(70); }

// step `cycles` clocks counting dirty_p_o pulses per context (Milan 5.4.5:
// each pulse is "a Table 5.4 counter was updated" for that Stream Output)
static int dpulses[3];
static void count_dirty(int cycles) {
    dpulses[0] = dpulses[1] = dpulses[2] = 0;
    for (int i = 0; i < cycles; i++) {
        step();
        for (int b = 0; b < 3; b++)
            if ((dut->dirty_p_o >> b) & 1) dpulses[b]++;
    }
}

static void frame_mr(int idx, int tu, int mr) {
    dut->tu_i = tu; dut->frame_mr_i = mr;
    dut->frame_p_i = 1; dut->frame_idx_i = idx;
    step();
    dut->frame_p_i = 0;
}
static void frame(int idx, int tu) { frame_mr(idx, tu, 0); }
static void rd(int idx) { dut->rd_idx_i = idx; dut->eval(); }

// read every counter of one context in a single eval
struct Ctrs { uint32_t start, stop, mreset, tu, ftx; };
static Ctrs snap(int idx) {
    rd(idx);
    return Ctrs{ (uint32_t)dut->rd_start_o, (uint32_t)dut->rd_stop_o,
                 (uint32_t)dut->rd_mreset_o, (uint32_t)dut->rd_tu_o,
                 (uint32_t)dut->rd_ftx_o };
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vtkdiag_tb_top;
    dut->rst_n = 0; dut->streaming_i = 0; dut->frame_p_i = 0;
    dut->tu_i = 0; dut->frame_mr_i = 0; dut->rd_idx_i = 0;
    dut->mcr_restart_p_i = 0; dut->mcr_streaming_i = 0; dut->mcr_clk_src_i = 0;
    cyc(4); dut->rst_n = 1; cyc(4);

    printf("[T1] reset state + the START/STOP invariant at zero\n");
    rd(0);
    ck("T1 all five zero", dut->rd_start_o | dut->rd_stop_o | dut->rd_mreset_o
                         | dut->rd_tu_o | dut->rd_ftx_o, 0);

    printf("[T2] START/STOP edge counting (one level, invariant holds)\n");
    dut->streaming_i = 0b001; cyc(3); rd(0);
    ck("T2 rise -> START 1", dut->rd_start_o, 1);
    ck("T2 ... STOP still 0 (START == STOP+1 while streaming)",
       dut->rd_stop_o, 0);
    dut->streaming_i = 0b000; cyc(3); rd(0);
    ck("T2 fall -> STOP 1 (START == STOP while stopped)", dut->rd_stop_o, 1);

    printf("[T3] FRAMES_TX is an INTERVAL count, not a frame total\n");
    dut->streaming_i = 0b001; cyc(3);        // start (resets the three)
    for (int f = 0; f < 8; f++) frame(0, 0); // 8 PDUs, ONE interval
    interval(); rd(0);
    ck("T3 8 PDUs in one interval -> FRAMES_TX 1 (not 8)", dut->rd_ftx_o, 1);
    frame(0, 0); interval();
    frame(0, 0); interval(); rd(0);
    ck("T3 two more active intervals -> 3", dut->rd_ftx_o, 3);
    interval(); interval(); rd(0);
    ck("T3 idle intervals do not count", dut->rd_ftx_o, 3);

    printf("[T4] TIMESTAMP_UNCERTAIN qualifies tu BY TRANSMISSION\n");
    dut->tu_i = 1; interval(); interval(); rd(0);
    ck("T4 tu high, nothing sent -> no count", dut->rd_tu_o, 0);
    frame(0, 1); interval(); rd(0);
    ck("T4 tu on a TRANSMITTED PDU -> 1", dut->rd_tu_o, 1);
    dut->tu_i = 0;
    frame(0, 0); interval(); rd(0);
    ck("T4 clean interval leaves it", dut->rd_tu_o, 1);

    printf("[T5] reset-on-start zeroes the three interval counters\n");
    rd(0);
    { uint64_t s0 = dut->rd_start_o;
      dut->streaming_i = 0b000; cyc(3);
      dut->streaming_i = 0b001; cyc(3); rd(0);
      ck("T5 START advanced", dut->rd_start_o, s0 + 1); }
    ck("T5 FRAMES_TX reset on start (Table 5.4)", dut->rd_ftx_o, 0);
    ck("T5 TIMESTAMP_UNCERTAIN reset on start", dut->rd_tu_o, 0);
    ck("T5 MEDIA_RESET reset on start", dut->rd_mreset_o, 0);

    printf("[T6] per-context isolation + the CRF context (index 2)\n");
    frame(2, 0); interval();
    rd(0);
    ck("T6 ctx0 unmoved by ctx2 frames", dut->rd_ftx_o, 0);
    rd(2);
    ck("T6 ctx2 counted its own interval", dut->rd_ftx_o, 1);
    ck("T6 ctx2 never started (level low) -> START 0", dut->rd_start_o, 0);

    printf("[T7] the read port is combinational per index\n");
    rd(0); uint64_t a = dut->rd_start_o;
    rd(2); uint64_t b = dut->rd_start_o;
    ck("T7 idx swap changes the view same-eval", (a != b) ? 1 : 0, 1);

    // ---------------------------------------------------------------------
    //  T8: what Table 5.4 does NOT say. MEDIA_RESET / TIMESTAMP_UNCERTAIN /
    //  FRAMES_TX each carry "Reset to 0 each time the Talker starts
    //  streaming"; STREAM_START and STREAM_STOP do NOT. A start edge must
    //  therefore leave BOTH edge counters standing, or the invariant
    //  "START = STOP+1 while streaming" is unprovable from the wire and the
    //  MVRP-LeaveAll flap fingerprint (16 starts / 15 stops) becomes
    //  unreadable.
    // ---------------------------------------------------------------------
    printf("[T8] START/STOP are NOT reset by a start (no such clause)\n");
    dut->streaming_i = 0b000; cyc(3);
    { Ctrs c = snap(0);
      uint32_t s0 = c.start, p0 = c.stop;
      ck("T8 stopped: START == STOP", c.start, c.stop);
      for (int k = 0; k < 5; k++) {           // five clean flaps
          dut->streaming_i = 0b001; cyc(3);
          dut->streaming_i = 0b000; cyc(3);
      }
      c = snap(0);
      ck("T8 five flaps -> START += 5 (survived every start)", c.start, s0 + 5);
      ck("T8 five flaps -> STOP  += 5 (survived every start)", c.stop,  p0 + 5);
      ck("T8 invariant while stopped: START == STOP", c.start, c.stop);
      dut->streaming_i = 0b001; cyc(3);
      c = snap(0);
      ck("T8 invariant while streaming: START == STOP+1", c.start, c.stop + 1);
    }

    // ---------------------------------------------------------------------
    //  T9: per-index independence across ALL contexts, never index 0 only.
    //  Give each context a DIFFERENT number of active intervals and a
    //  different number of start edges, then prove every context reports its
    //  own arithmetic. This is the case that bites an index-0-only or
    //  clamped-index read port.
    // ---------------------------------------------------------------------
    printf("[T9] per-index independence across ALL THREE contexts\n");
    dut->rst_n = 0; cyc(4); dut->rst_n = 1; cyc(4);
    dut->streaming_i = 0b111; cyc(3);        // all three start together
    // ctx0: 3 active intervals, ctx1: 1, ctx2: 2
    frame(0, 0); frame(1, 0); frame(2, 0); interval();   // all three
    frame(0, 0); frame(2, 0);              interval();   // ctx0, ctx2
    frame(0, 0);                           interval();   // ctx0 only
    { Ctrs c0 = snap(0), c1 = snap(1), c2 = snap(2);
      ck("T9 ctx0 FRAMES_TX 3", c0.ftx, 3);
      ck("T9 ctx1 FRAMES_TX 1", c1.ftx, 1);
      ck("T9 ctx2 FRAMES_TX 2", c2.ftx, 2);
      ck("T9 ctx0 START 1", c0.start, 1);
      ck("T9 ctx1 START 1", c1.start, 1);
      ck("T9 ctx2 START 1", c2.start, 1);
    }
    // now restart ONLY ctx1: its three interval counters zero, the others
    // keep theirs, and only its START moves
    dut->streaming_i = 0b101; cyc(3);
    dut->streaming_i = 0b111; cyc(3);
    { Ctrs c0 = snap(0), c1 = snap(1), c2 = snap(2);
      ck("T9 ctx1 restart zeroed ONLY ctx1 FRAMES_TX", c1.ftx, 0);
      ck("T9 ... ctx0 FRAMES_TX untouched", c0.ftx, 3);
      ck("T9 ... ctx2 FRAMES_TX untouched", c2.ftx, 2);
      ck("T9 ctx1 START 2", c1.start, 2);
      ck("T9 ctx1 STOP 1",  c1.stop,  1);
      ck("T9 ... ctx0 START still 1", c0.start, 1);
      ck("T9 ... ctx0 STOP still 0",  c0.stop,  0);
      ck("T9 ... ctx2 START still 1", c2.start, 1);
    }

    // ---------------------------------------------------------------------
    //  T10: MEDIA_RESET is backed BY THE WIRE. The counter derives the
    //  toggle from the mr bit the transmitted PDU carried, compared against
    //  that context's previous transmitted PDU - which is Table 5.4's
    //  sentence verbatim. Pre-fix this took an mr_p_i event strobe that
    //  milan_datapath tied to 1'b0, so mask bit 2 was claimed over a counter
    //  with no source (the STATS_CAP 0x204 / VERSION 0x0013 RMON lesson).
    // ---------------------------------------------------------------------
    printf("[T10] MEDIA_RESET counts an mr TOGGLE on a transmitted PDU\n");
    dut->rst_n = 0; cyc(4); dut->rst_n = 1; cyc(4);
    dut->streaming_i = 0b111; cyc(3);
    frame_mr(0, 0, 0); frame_mr(0, 0, 0); interval();
    ck("T10 mr steady 0 -> MEDIA_RESET 0", snap(0).mreset, 0);
    frame_mr(0, 0, 1);                     interval();
    ck("T10 mr 0->1 on a transmitted PDU -> 1", snap(0).mreset, 1);
    // the clause counts the TOGGLE, not the level: more PDUs at the new
    // level are not new resets
    frame_mr(0, 0, 1); frame_mr(0, 0, 1);  interval();
    ck("T10 mr STAYS 1 -> still 1 (level is not an event)", snap(0).mreset, 1);
    frame_mr(0, 0, 0);                     interval();
    ck("T10 mr 1->0 is also a toggle -> 2", snap(0).mreset, 2);
    // two toggles inside ONE interval are still one interval
    frame_mr(0, 0, 1); frame_mr(0, 0, 0);  interval();
    ck("T10 two toggles in one interval -> +1 only (interval count)",
       snap(0).mreset, 3);
    // and it is per context: ctx1 never toggled
    ck("T10 ctx1 MEDIA_RESET untouched", snap(1).mreset, 0);
    printf("[T10b] a toggle with NO PDU transmitted counts nothing\n");
    dut->frame_mr_i = 1; interval(); interval();
    ck("T10b mr level high, nothing sent -> unchanged", snap(0).mreset, 3);

    // ---------------------------------------------------------------------
    //  T11: the observation-interval BOUNDARY. An event strobe landing on
    //  the tick cycle must be counted - it was transmitted during the
    //  interval the tick closes. Pre-fix the tick's whole-vector clear was a
    //  later nonblocking assignment than the per-bit fold, so it won and the
    //  one-cycle strobe was lost from BOTH intervals. Invisible for
    //  FRAMES_TX at 8 kPDU/s, fatal for a SPARSE event: a lone tu-stamped
    //  PDU or a single mr toggle vanished.
    //
    //  The tick period is 64, so sweep 160 cycles (2.5 periods) and require the
    //  lone PDU to be counted from every one of them.
    // ---------------------------------------------------------------------
    printf("[T11] an event ON the interval tick is not lost\n");
    for (int phase = 0; phase < 160; phase++) {
        dut->rst_n = 0; dut->streaming_i = 0; dut->frame_p_i = 0;
        dut->tu_i = 0; dut->frame_mr_i = 0;
        cyc(4); dut->rst_n = 1;
        dut->streaming_i = 0b001;
        // walk to the candidate cycle, emit exactly ONE tu-stamped PDU there
        cyc(phase);
        frame_mr(0, /*tu=*/1, /*mr=*/0);
        // let two whole intervals close so the event must have been harvested
        interval(); interval();
        Ctrs c = snap(0);
        if (c.ftx == 0 || c.tu == 0) {
            checks++; fails++;
            printf("  [FAIL] T11 phase %2d: the single PDU was LOST "
                   "(FRAMES_TX=%u TIMESTAMP_UNCERTAIN=%u)\n",
                   phase, c.ftx, c.tu);
        }
    }
    checks++;
    printf("  [ok]   T11 all 160 tick phases counted the lone PDU\n");

    // the same sweep for a lone mr toggle
    printf("[T11b] a lone mr TOGGLE on any phase is not lost\n");
    for (int phase = 0; phase < 160; phase++) {
        dut->rst_n = 0; dut->streaming_i = 0; dut->frame_p_i = 0;
        dut->tu_i = 0; dut->frame_mr_i = 0;
        cyc(4); dut->rst_n = 1;
        dut->streaming_i = 0b001;
        cyc(phase);
        frame_mr(0, 0, /*mr=*/1);          // the ONLY toggle, ever
        interval(); interval();
        Ctrs c = snap(0);
        if (c.mreset == 0) {
            checks++; fails++;
            printf("  [FAIL] T11b phase %2d: the lone mr toggle was LOST\n",
                   phase);
        }
    }
    checks++;
    printf("  [ok]   T11b all 160 tick phases counted the lone mr toggle\n");

    // ---------------------------------------------------------------------
    //  T12: KL_media_clock_restart - the 4.4.4.3 producer of that mr bit.
    //  "This bit is toggled by the Talker each time a media clock restart is
    //   needed, and it stays at its new value until a new media clock
    //   restart is needed. ... Once this bit toggles, it shall remain in its
    //   new state for a minimum of eight (8) AVTPDUs for a given continuous
    //   stream."
    // ---------------------------------------------------------------------
    printf("[T12] the 4.4.4.3 mr level: toggle, hold >= 8 PDUs, per stream\n");
    dut->rst_n = 0; cyc(4); dut->rst_n = 1;
    dut->mcr_streaming_i = 0b11; dut->frame_mr_i = 0; cyc(4);
    ck("T12 reset level 0", dut->mcr_mr_o & 1, 0);
    // a restart flips the level
    dut->mcr_restart_p_i = 1; step(); dut->mcr_restart_p_i = 0; cyc(2);
    ck("T12 restart -> level toggles to 1", dut->mcr_mr_o & 1, 1);
    ck("T12 ... and talker 1 toggles too (one media clock)",
       (dut->mcr_mr_o >> 1) & 1, 1);
    // a second restart before 8 PDUs have carried the new value MUST NOT
    // move the wire (the >= 8 hold) - drive PDUs carrying the current level
    dut->frame_mr_i = 1;
    for (int k = 0; k < 4; k++) frame_mr(0, 0, 1);   // only 4 PDUs so far
    dut->mcr_restart_p_i = 1; step(); dut->mcr_restart_p_i = 0; cyc(2);
    ck("T12 restart after only 4 PDUs -> level HELD at 1", dut->mcr_mr_o & 1, 1);
    // top the count up to 8 and the pending flip is adopted
    for (int k = 0; k < 4; k++) frame_mr(0, 0, 1);
    cyc(2);
    ck("T12 8th PDU carried the state -> pending flip adopted (0)",
       dut->mcr_mr_o & 1, 0);
    // the hold is PER STREAM: talker 1 sent nothing, so its hold is
    // unsatisfied and its level must still be the pre-flip value
    ck("T12 talker 1 sent no PDUs -> its own hold blocks the flip",
       (dut->mcr_mr_o >> 1) & 1, 1);

    // ---------------------------------------------------------------------
    //  T13: the 4.4.4.3 SOURCE-CHANGE trigger (PICS Table F.7 AAF-5, AAF:M
    //  MANDATORY - "Is the mr field toggled when the device's media clock
    //  source has changed?"). Until 2026-07-30 only the CRF-disruption pulse
    //  was wired, so a controller switching the media clock source produced
    //  NO mr edge. BITES the pre-fix module (no clk_src_i trigger): every
    //  source-change ck below reads the un-toggled level.
    // ---------------------------------------------------------------------
    printf("[T13] the 4.4.4.3 SOURCE-CHANGE mr trigger (PICS AAF-5)\n");
    dut->rst_n = 0; dut->mcr_clk_src_i = 0; cyc(4); dut->rst_n = 1;
    dut->mcr_streaming_i = 0b11; dut->frame_mr_i = 0; cyc(4);
    ck("T13 reset level 0, source internal(0)", dut->mcr_mr_o & 1, 0);
    for (int k = 0; k < 8; k++) frame_mr(0, 0, 0);   // hold satisfied, no change
    cyc(2);
    ck("T13 source unchanged -> no toggle", dut->mcr_mr_o & 1, 0);
    // SET_CLOCK_SOURCE internal(0) -> CRF(2): a media-clock SOURCE change
    dut->mcr_clk_src_i = 2; step(); cyc(2);
    ck("T13 source change internal->CRF toggles mr to 1", dut->mcr_mr_o & 1, 1);
    dut->frame_mr_i = 1;
    for (int k = 0; k < 8; k++) frame_mr(0, 0, 1);   // hold the new level
    cyc(2);
    // a no-op SET (same source value) must NOT toggle
    dut->mcr_clk_src_i = 2; step(); cyc(2);
    ck("T13 no-op SET (same source) does NOT toggle", dut->mcr_mr_o & 1, 1);
    // change back CRF(2) -> internal(0): toggles again
    dut->mcr_clk_src_i = 0; step(); cyc(2);
    ck("T13 source change CRF->internal toggles mr back to 0",
       dut->mcr_mr_o & 1, 0);

    // ---------------------------------------------------------------------
    //  T15: the CRF Media Clock Output is a HOLD-BEARING context of the same
    //  engine (gh #62 H2b). IEEE 1722-2016 10.4.3 gives a CRF Talker the mr
    //  duty 4.4.4.3 gives a media-stream Talker, and PICS Table F.16 makes
    //  CRF-3 (the bit set as described in 10.4.3) and CRF-5 ("a minimum of
    //  eight (8) CRF AVTPDUs") BOTH mandatory - so the CRF output cannot be
    //  a bystander that merely reads the engine's target.
    //
    //  Its hold has to be ITS OWN, and the rates are why: a CRF stream runs
    //  at 500 PDU/s against an AAF talker's 8000, so a shared hold would let
    //  the audio talkers satisfy the CRF stream's clause on its behalf and
    //  put the new state on the CRF wire for a sixteenth of eight PDUs. The
    //  TARGET stays shared - one media clock, one restart history - which is
    //  the other half of the same clause.
    //
    //  BITES the pre-round engine, which was N_TALKERS_P = N_STREAMS: with
    //  no context 2 there is no level for the CRF talker to stamp and no
    //  hold for it to satisfy.
    // ---------------------------------------------------------------------
    printf("[T15] the CRF context (2) carries its OWN 4.4.4.3 hold\n");
    dut->rst_n = 0; dut->mcr_clk_src_i = 0; cyc(4); dut->rst_n = 1;
    dut->streaming_i = 0b111; dut->mcr_streaming_i = 0b111;
    dut->frame_mr_i = 0; cyc(4);
    ck("T15 reset: all three contexts at level 0", dut->mcr_mr_o, 0);
    // SET_CLOCK_SOURCE internal(0) -> CRF(2). Nothing has streamed yet, so
    // every hold starts satisfied and all three adopt at once - a fresh
    // stream must carry the current truth, not a stale bit.
    dut->mcr_clk_src_i = 2; step(); cyc(2);
    ck("T15 a source change toggles the CRF context with the rest",
       dut->mcr_mr_o, 0b111);
    // put the new level on the wire ASYMMETRICALLY: talker 0 completes its
    // eight PDUs, the CRF output manages only three
    dut->frame_mr_i = 1;
    for (int k = 0; k < 8; k++) frame_mr(0, 0, 1);
    for (int k = 0; k < 3; k++) frame_mr(2, 0, 1);
    cyc(2);
    // a second source change: talker 0 may move, the CRF output may not
    dut->mcr_clk_src_i = 0; step(); cyc(2);
    ck("T15 talker 0 satisfied its own hold -> adopts 0",
       dut->mcr_mr_o & 1, 0);
    ck("T15 the CRF context has 3 CRF AVTPDUs -> HELD at 1",
       (dut->mcr_mr_o >> 2) & 1, 1);
    ck("T15 talker 1 transmitted nothing -> held too (per-stream hold)",
       (dut->mcr_mr_o >> 1) & 1, 1);
    for (int k = 0; k < 4; k++) frame_mr(2, 0, 1);   // 7 of the 8
    cyc(2);
    ck("T15 seven CRF AVTPDUs is not eight -> still held",
       (dut->mcr_mr_o >> 2) & 1, 1);
    ck("T15 ... and talker 0 did not un-adopt while waiting",
       dut->mcr_mr_o & 1, 0);
    frame_mr(2, 0, 1); cyc(2);                       // the eighth
    ck("T15 the EIGHTH CRF AVTPDU releases the hold -> adopts 0",
       (dut->mcr_mr_o >> 2) & 1, 0);
    // ... and the Table 5.4 counter for that Stream Output scores the bit
    // the CRF PDUs really carried. This is the milan_datapath mux this round
    // fixed: the CRF context used to be fed a CONSTANT 0 (defensible only
    // while KL_crf_tx really did stamp a constant), so its MEDIA_RESET could
    // never move whatever the wire did.
    dut->frame_mr_i = 0;
    interval(); interval();                          // drain open flags
    {
        Ctrs c2b = snap(2), c0b = snap(0);
        frame_mr(2, 0, 0);                           // the CRF PDU at level 0
        interval(); interval();
        ck("T15 the CRF context's MEDIA_RESET scored its own wire",
           snap(2).mreset, c2b.mreset + 1);
        ck("T15 ... and talker 0's counter did not move for it",
           snap(0).mreset, c0b.mreset);
    }

    printf("--------------------------------------------------------------\n");
    // ---------------------------------------------------------------------
    //  T14: dirty_p_o, the Milan 5.4.5 Table 5.22 push source. Pushes are
    //  for EVENTS: START/STOP edges and anomaly intervals (TU, MEDIA_RESET)
    //  pulse; a HEALTHY interval - FRAMES_TX ticking and nothing else -
    //  must be SILENT, or every streaming talker pushes GET_COUNTERS at
    //  exactly 1/s to every registered controller forever (the task-#21
    //  self-excitation, decoded on silicon 2026-08-06). The 1/s rate limit
    //  is the AECP builder's, NOT this module's.
    // ---------------------------------------------------------------------
    printf("[T14] dirty_p_o pulses on EVENTS, never on healthy intervals\n");
    dut->streaming_i = 0; dut->tu_i = 0; dut->frame_p_i = 0;
    dut->frame_mr_i = 0;
    cyc(200);                                // drain edges + open intervals
    count_dirty(140);                        // two-plus idle intervals
    ck("T14 idle intervals -> no pulses on any context",
       dpulses[0] + dpulses[1] + dpulses[2], 0);
    dut->streaming_i = 0b001;
    count_dirty(6);
    ck("T14 start edge -> ONE pulse on ctx0", dpulses[0], 1);
    ck("T14 ... and none on ctx1/ctx2", dpulses[1] + dpulses[2], 0);
    //! settle the mr LEVEL inherited from the earlier sections: the first
    //! frame at the new level scores a legitimate toggle - absorb it
    frame(0, 0); count_dirty(70);
    for (int f = 0; f < 3; f++) frame(0, 0); // 3 healthy PDUs, one interval
    count_dirty(70);                         // crosses exactly one close
    ck("T14 HEALTHY interval close -> SILENT (frames are not events)",
       dpulses[0], 0);
    for (int f = 0; f < 3; f++) frame(0, 1); // 3 tu PDUs: an ACTIVE anomaly
    count_dirty(70);
    ck("T14 tu interval -> ONE pulse at its close", dpulses[0], 1);
    frame_mr(0, 0, 1);                       // mr toggles inside an interval
    count_dirty(70);
    ck("T14 media-reset interval -> ONE pulse", dpulses[0], 1);
    frame(0, 0); count_dirty(70);            // absorb the mr 1->0 toggle
    for (int f = 0; f < 3; f++) frame(0, 0);
    count_dirty(70);
    ck("T14 back to healthy -> silent again", dpulses[0], 0);
    dut->streaming_i = 0b000;
    count_dirty(6);
    ck("T14 stop edge -> ONE pulse on ctx0", dpulses[0], 1);
    frame(2, 1);                             // CRF context tu activity only
    count_dirty(70);
    ck("T14 ctx2-only tu interval -> the pulse rides bit 2", dpulses[2], 1);
    ck("T14 ... and not bit 0", dpulses[0], 0);

    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
