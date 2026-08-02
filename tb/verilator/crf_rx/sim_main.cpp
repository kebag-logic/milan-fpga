// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_crf_rx module harness: Milan 7.3.2 CRF sink measurement engine vs an
// independent C++ replica (its own 256-entry ts ring). Pins the
// ts-history-dependent outputs — delta / rate / lock trajectory / counters —
// per accepted PDU over ppm-offset timestamp patterns, so the ts_hist
// flop-file -> BRAM conversion is provably numerically identical.
//
// COUNTER SEMANTICS (Milan v1.2 Table 5.6, the 3c82068d reading applied to
// the CRF Media Clock Input): pdu_count (FRAMES_RX), fmt_err
// (UNSUPPORTED_FORMAT) and seq_err (SEQ_NUM_MISMATCH) are "incremented at
// the end of every observation interval during which ..." — N events inside
// one interval move a counter by exactly ONE, committed at the interval
// tick. cnt_locked/cnt_unlocked stay per-event ("incremented each time").
// The replica models the interval divider cycle-exactly (registered tick,
// tick-cycle events harvested into the closing interval), so every per-PDU
// compare below also pins the interval machinery. The dedicated
// [Table 5.6] section is the mutation anchor: revert the RTL to per-frame
// counting and a 10-PDU burst reads +10 where +1 is pinned.
//
// Sampling contract: outputs are compared SETTLE_TICKS_C (4) cycles after
// each frame pulse. The CSR consumers poll at ms scale (PDUs are 2 ms
// apart), so a fixed update skew of <= 2 cycles is semantically free; the
// skew itself is measured and bounded by an explicit check below.
//
// CLK_FREQ_HZ_P is overridden to 200 kHz (Makefile -G) => the 100 ms lock
// timeout TOUT_CYC_C = 20 000 cycles. IVAL_CYC_C arrives from the SAME
// Makefile variable that sets the RTL IVAL_CYC_P (derive, never mirror).

#include "VKL_crf_rx.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

#ifndef IVAL_CYC_C
#error "IVAL_CYC_C must come from the Makefile (the -GIVAL_CYC_P twin)"
#endif

static VKL_crf_rx* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, long long got, long long exp) {
    checks++;
    bool ok = (got == exp);
    if (!ok) fails++;
    printf("  [%s] %-46s got=%lld exp=%lld\n", ok ? "PASS" : "FAIL", what, got, exp);
}

// quiet per-PDU compare: prints only on FAIL (thousands of these)
static void ckq(const char* what, long pdu_no, long long got, long long exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] pdu#%-5ld %-38s got=%lld exp=%lld\n", pdu_no, what, got, exp);
    }
}

//---------------------------------------------------------------------------
// Independent replica of the measurement engine (Milan v1.2 7.3.2-7.3.4 +
// Table 5.6): 256-deep ts ring, 512 ms window rate, 8-PDU settle lock,
// 100 ms drop, observation-interval counter commit.
//---------------------------------------------------------------------------
struct Model {
    static const int  DEPTH = 256;
    uint64_t hist[DEPTH];
    int      hidx = 0, hfill = 0;
    uint8_t  exp_seq = 0;
    bool     have_seq = false;
    int      settle = 0;                 // 0..7
    bool     locked = false;
    uint32_t cnt_l = 0, cnt_u = 0;
    int32_t  delta = 0, rate = 0;
    uint16_t pdu = 0;                    // FRAMES_RX interval commits
    uint8_t  fmt_e = 0, seq_e = 0;       // UF / SM interval commits

    // Table 5.6 interval machinery, cycle-exact mirror of iv_tick_gen +
    // the engine's commit/fold: iv_tick is REGISTERED (pulses the cycle
    // after the divider wraps); an event in the commit cycle itself is
    // harvested into the closing interval.
    uint32_t iv_div = 0;
    bool     iv_tick = false;
    bool     f_frx = false, f_uf = false, f_sm = false;

    void cycle(bool frx_ev, bool uf_ev, bool sm_ev) {
        if (iv_tick) {
            if (f_frx || frx_ev) pdu++;
            if (f_uf  || uf_ev)  { if (fmt_e != 0xFF) fmt_e++; }
            if (f_sm  || sm_ev)  { if (seq_e != 0xFF) seq_e++; }
            f_frx = f_uf = f_sm = false;
        } else {
            f_frx |= frx_ev; f_uf |= uf_ev; f_sm |= sm_ev;
        }
        if (iv_div >= IVAL_CYC_C - 1) { iv_div = 0; iv_tick = true;  }
        else                          { iv_div++;   iv_tick = false; }
    }

    void good_pdu(uint64_t ts, uint8_t seq, uint64_t ptp) {
        if (have_seq && seq != exp_seq) {
            settle = 0;                  // discontinuity breaks the settle run
        } else if (settle != 7) {
            settle++;
        } else if (!locked) {
            locked = true; cnt_l++;
        }
        exp_seq  = (uint8_t)(seq + 1);
        have_seq = true;
        delta = (int32_t)(uint32_t)(ts - ptp);
        if (hfill == DEPTH) {
            rate = (int32_t)(uint32_t)((ts - hist[hidx]) - 512000000ULL);
        } else {
            hfill++;
        }
        hist[hidx] = ts;
        hidx = (hidx + 1) & (DEPTH - 1);
    }
    void bad_pdu() {                     // format-invalid, matched stream
        settle = 0;                      // the UF count commits via cycle()
    }
    void timeout() {                     // 100 ms without an accepted PDU
        if (locked) { locked = false; cnt_u++; }
        settle = 0; have_seq = false; hfill = 0;
    }
};

static Model m;
static long g_pdu_no = 0;                // global accepted-PDU ordinal

static const uint64_t SID_C  = 0x0200000000010001ULL;
static const int SETTLE_TICKS_C = 4;     // sample point after each pulse

// this-cycle Table 5.6 events, consumed by the next tick()
static bool g_ev_frx = false, g_ev_uf = false, g_ev_sm = false;
static bool g_in_reset = true;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    if (!g_in_reset) m.cycle(g_ev_frx, g_ev_uf, g_ev_sm);
    g_ev_frx = g_ev_uf = g_ev_sm = false;
}

// run to the first cycle of a FRESH observation interval (model divider 1 =
// the cycle right after a commit edge): a burst launched here has a full
// tick-free window of IVAL_CYC_C-1 cycles ahead of it
static void align_interval() {
    while (m.iv_div != 1) tick();
}

static void drive_fields(uint64_t ts, uint8_t seq) {
    dut->subtype_i   = 0x04;
    dut->type_i      = 0x01;
    dut->seq_i       = seq;
    dut->sid_frame_i = SID_C;
    dut->pullbase_i  = 48000;            // pull=0 | base 48000
    dut->fsh_i       = (8ULL << 48) | (96ULL << 32) | (ts >> 32);
    dut->fsh2_i      = (ts & 0xFFFFFFFFULL) << 32;
}

static void pulse() {
    dut->frame_p_i = 1; tick();
    dut->frame_p_i = 0;
}

static void compare(long no) {
    ckq("delta_o",        no, (int32_t)dut->delta_o,  m.delta);
    ckq("rate_o",         no, (int32_t)dut->rate_o,   m.rate);
    ckq("locked_o",       no, dut->locked_o,          m.locked);
    ckq("pdu_count_o",    no, dut->pdu_count_o,       m.pdu);
    ckq("fmt_err_o",      no, dut->fmt_err_o,         m.fmt_e);
    ckq("seq_err_o",      no, dut->seq_err_o,         m.seq_e);
    ckq("cnt_locked_o",   no, dut->cnt_locked_o,      m.cnt_l);
    ckq("cnt_unlocked_o", no, dut->cnt_unlocked_o,    m.cnt_u);
}

// one accepted-good PDU: drive, pulse, settle, compare vs replica.
// The Table 5.6 events (FRX always, SM on a discontinuity) are computed
// from the replica's PRE-update state — exactly what the RTL sees in
// have_seq_r/exp_seq_r at the pulse edge.
static void good_pdu(uint64_t ts, uint8_t seq, uint64_t ptp) {
    dut->ptp_now_i = ptp;
    drive_fields(ts, seq);
    g_ev_frx = true;
    g_ev_sm  = (m.have_seq && seq != m.exp_seq);
    pulse();
    for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
    m.good_pdu(ts, seq, ptp);
    compare(++g_pdu_no);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_crf_rx;

    dut->rst_n = 0; dut->en_i = 0; dut->frame_p_i = 0;
    dut->sid_i = SID_C; dut->ptp_now_i = 0;
    drive_fields(0, 0);
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    g_in_reset = false;                  // divider runs from here, both sides
    for (int i = 0; i < 8; i++) tick();

    printf("[crf_rx] reset + selection gating\n");
    ck("reset: delta 0",  (int32_t)dut->delta_o, 0);
    ck("reset: rate 0",   (int32_t)dut->rate_o, 0);
    ck("reset: unlocked", dut->locked_o, 0);

    // disabled: matching PDUs must be ignored
    uint64_t ts  = 1000000000ULL;        // talker CRF timeline
    uint64_t ptp = 1000500000ULL;        // observer gPTP timeline
    drive_fields(ts, 0); dut->ptp_now_i = ptp;
    pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
    ck("disabled: pdu_count 0", dut->pdu_count_o, 0);

    dut->en_i = 1;

    // wrong stream_id / wrong subtype: ignored (no count, no error)
    dut->sid_frame_i = SID_C ^ 1;
    pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
    dut->sid_frame_i = SID_C; dut->subtype_i = 0x02;    // AAF
    pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
    ck("foreign frames: pdu_count 0", dut->pdu_count_o, 0);
    ck("foreign frames: fmt_err 0",   dut->fmt_err_o, 0);

    printf("[crf_rx] format validation (Milan 7.3.2 profile)\n");
    // each malformed variant: settle broken, no pdu count; the
    // UNSUPPORTED_FORMAT tally is a Table 5.6 interval counter, so the 5
    // rejects — launched inside ONE aligned observation interval — must
    // commit as exactly ONE tick, not 5 (the old per-frame reading).
    align_interval();
    struct { const char* name; int field; } bad[] = {
        {"type != AUDIO_SAMPLE", 0}, {"pull != 0", 1}, {"base != 48000", 2},
        {"dlen != 8", 3}, {"interval != 96", 4},
    };
    for (auto& b : bad) {
        drive_fields(ts, 0);
        switch (b.field) {
            case 0: dut->type_i = 0x02; break;
            case 1: dut->pullbase_i = (1u << 29) | 48000; break;
            case 2: dut->pullbase_i = 44100; break;
            case 3: dut->fsh_i = (16ULL << 48) | (96ULL << 32) | (ts >> 32); break;
            case 4: dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32); break;
        }
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
    }
    ck("5 malformed: no commit before the tick", dut->fmt_err_o, 0);
    for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
    ck("5 malformed: ONE interval tick, not 5", dut->fmt_err_o, 1);
    ck("5 malformed: pdu_count still 0", dut->pdu_count_o, 0);
    ck("5 malformed: unlocked", dut->locked_o, 0);

    //-----------------------------------------------------------------------
    // Pinned trajectory 1: talker at +100 ppm (period 2 000 200 ns),
    // observer nominal. 300 PDUs: delta drifts +200/PDU; rate_o must stay 0
    // until the ring fills (256 PDUs) then read +100 ppm exactly:
    // 256 * 200 = 51 200 ns / 512 ms window. Lock on the 8th clean PDU.
    // FRAMES_RX counts the INTERVALS containing PDUs (replica-pinned per
    // PDU), never the 300 frames.
    //-----------------------------------------------------------------------
    printf("[crf_rx] +100 ppm trajectory (300 PDUs, per-PDU pinned)\n");
    uint8_t seq = 0;
    long rate_first_pdu = -1;
    for (int n = 0; n < 300; n++) {
        ts  += 2000200;                  // +100 ppm of the 2 ms grid
        ptp += 2000000;                  // nominal observer
        good_pdu(ts, seq++, ptp);
        if (rate_first_pdu < 0 && (int32_t)dut->rate_o != 0)
            rate_first_pdu = g_pdu_no;
    }
    ck("lock latched", dut->locked_o, 1);
    ck("cnt_locked 1", dut->cnt_locked_o, 1);
    ck("rate first nonzero on PDU 257 (ring full)", rate_first_pdu, 257);
    ck("rate == +100 ppm exactly (51200 ns/512 ms)", (int32_t)dut->rate_o, 51200);
    ck("FRAMES_RX == replica interval count", dut->pdu_count_o, m.pdu);
    ck("300 PDUs commit as intervals, NOT frames", dut->pdu_count_o < 300, 1);

    //-----------------------------------------------------------------------
    // Pinned trajectory 2: slope change to -50 ppm (period 1 999 900 ns).
    // rate ramps -300/PDU across the mixed window, settling at
    // 256 * (-100) = -25 600. Every intermediate value pinned vs the replica.
    //-----------------------------------------------------------------------
    printf("[crf_rx] -50 ppm slope change (300 PDUs, ramp pinned)\n");
    for (int n = 0; n < 100; n++) {
        ts  += 1999900;
        ptp += 2000000;
        good_pdu(ts, seq++, ptp);
    }

    // rate-update skew probe: mid-ramp (mixed 256-PDU window) rate_o still
    // changes -300 on every PDU, so the update edge is observable.
    // Measure how many cycles after the frame pulse the change lands.
    // Flop-file: 0. BRAM read pipeline: 1. Bound: <= 2 (CSR-invisible).
    {
        ts  += 1999900; ptp += 2000000;
        dut->ptp_now_i = ptp;
        drive_fields(ts, seq);
        int32_t old_rate = (int32_t)dut->rate_o;
        g_ev_frx = true;                 // accepted sequential PDU
        pulse();
        int lat = 0;
        while ((int32_t)dut->rate_o == old_rate && lat <= 3) { tick(); lat++; }
        for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.good_pdu(ts, seq, ptp); seq++;
        compare(++g_pdu_no);
        printf("  [info] rate_o update skew after pulse edge: %d cycle(s)\n", lat);
        ck("rate update skew <= 2 cycles", lat <= 2, 1);
    }
    for (int n = 0; n < 199; n++) {
        ts  += 1999900; ptp += 2000000;
        good_pdu(ts, seq++, ptp);
    }
    ck("rate == -50 ppm exactly (-25600 ns/512 ms)", (int32_t)dut->rate_o, -25600);

    //-----------------------------------------------------------------------
    // Sequence discontinuity: settle broken, lock RETAINED (Milan drops
    // lock only on the 100 ms silence / validation contract); the
    // SEQ_NUM_MISMATCH tally commits at the next interval tick.
    //-----------------------------------------------------------------------
    printf("[crf_rx] sequence discontinuity\n");
    ts += 1999900; ptp += 2000000;
    seq++;                               // skip one sequence number
    good_pdu(ts, seq++, ptp);
    ck("seq skip: still locked", dut->locked_o, 1);
    for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
    ck("seq skip: ONE interval tick", dut->seq_err_o, 1);
    for (int n = 0; n < 10; n++) {       // clean run rebuilds settle
        ts += 1999900; ptp += 2000000;
        good_pdu(ts, seq++, ptp);
    }
    ck("clean resume: no extra lock event", dut->cnt_locked_o, 1);
    ck("clean resume: seq_err holds at 1", dut->seq_err_o, 1);

    //-----------------------------------------------------------------------
    // 100 ms silence: unlock event, ring restarts (hfill=0) but hidx and
    // rate_o hold; after resume rate stays frozen for 256 PDUs, then
    // updates again; re-lock on the 8th clean PDU (cnt_locked -> 2).
    // ~100 empty observation intervals pass: no event, no counter motion.
    //-----------------------------------------------------------------------
    printf("[crf_rx] 100 ms silence -> unlock -> refill\n");
    int32_t rate_frozen = (int32_t)dut->rate_o;
    // close the still-open interval first (its pending FRX flag rightly
    // commits one more tick); THEN the ~100 empty intervals must not move
    for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
    uint16_t pdu_frozen = dut->pdu_count_o;
    for (int i = 0; i < 20005; i++) tick();      // TOUT_CYC_C = 20 000 @ 200 kHz
    m.timeout();
    ck("silence: unlocked", dut->locked_o, 0);
    ck("silence: cnt_unlocked 1", dut->cnt_unlocked_o, 1);
    ck("silence: rate holds last value", (int32_t)dut->rate_o, rate_frozen);
    ck("silence: empty intervals do NOT tick FRAMES_RX",
       dut->pdu_count_o, pdu_frozen);

    // resume at +100 ppm again; ~100 ms passed on both timelines
    ts += 100000000; ptp += 100000000;
    long rate_change_pdu = -1;
    long resume_base = g_pdu_no;
    for (int n = 0; n < 270; n++) {
        ts  += 2000200;
        ptp += 2000000;
        good_pdu(ts, seq++, ptp);
        if (rate_change_pdu < 0 && (int32_t)dut->rate_o != rate_frozen)
            rate_change_pdu = g_pdu_no - resume_base;
    }
    ck("re-lock: cnt_locked 2", dut->cnt_locked_o, 2);
    ck("refill: rate frozen for 256 PDUs, moves on 257",
       rate_change_pdu, 257);
    ck("refill: rate == +100 ppm again", (int32_t)dut->rate_o, 51200);

    //-----------------------------------------------------------------------
    // Table 5.6 interval semantics, the mutation anchor. A burst of N
    // events inside ONE aligned observation interval moves the counter by
    // exactly 1 at the tick ("incremented at the end of every observation
    // interval during which ..."), never by N (the 1722.1 Table 7-153
    // per-frame reading — ~500x high at the CRF 500 PDU/s cadence).
    //-----------------------------------------------------------------------
    printf("[crf_rx] Milan Table 5.6 interval semantics (burst -> ONE tick)\n");
    align_interval();
    uint16_t p0 = dut->pdu_count_o;
    for (int n = 0; n < 10; n++) {       // 10 PDUs = 50 cycles < IVAL_CYC_C-1
        ts  += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ptp);
    }
    ck("burst of 10 accepted: no commit before the tick", dut->pdu_count_o, p0);
    for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
    ck("burst of 10 accepted: FRAMES_RX +1, not +10",
       dut->pdu_count_o, (uint16_t)(p0 + 1));

    // mixed burst in ONE interval: 3 discontinuities (accepted) + 2 format
    // rejects -> SM +1, UF +1, FRX +1 (the accepted PDUs ride the same
    // interval), all committed together at the tick
    align_interval();
    p0 = dut->pdu_count_o;
    uint8_t f0 = dut->fmt_err_o, s0 = dut->seq_err_o;
    for (int n = 0; n < 3; n++) {
        ts  += 2000200; ptp += 2000000;
        seq += 2;                        // every one a discontinuity
        good_pdu(ts, seq++, ptp);
    }
    for (int n = 0; n < 2; n++) {        // 2 format rejects (wrong interval)
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
    }
    for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
    ck("3 discontinuities: SEQ_NUM_MISMATCH +1", dut->seq_err_o,
       (uint8_t)(s0 + 1));
    ck("2 rejects: UNSUPPORTED_FORMAT +1", dut->fmt_err_o, (uint8_t)(f0 + 1));
    ck("same interval's accepted PDUs: FRAMES_RX +1", dut->pdu_count_o,
       (uint16_t)(p0 + 1));

    printf("======================================================================\n");
    printf("KL_crf_rx: %ld checks, %ld failures (%ld accepted PDUs pinned)\n",
           checks, fails, g_pdu_no);
    delete dut;
    return fails ? 1 : 0;
}
