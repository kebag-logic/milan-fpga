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
// (UNSUPPORTED_FORMAT), seq_err (SEQ_NUM_MISMATCH), mr_cnt (MEDIA_RESET),
// tu_cnt (TIMESTAMP_UNCERTAIN), late_cnt (LATE_TIMESTAMP) and early_cnt
// (EARLY_TIMESTAMP) are "incremented at the end of every observation
// interval during which ..." — N events inside one interval move a counter
// by exactly ONE, committed at the interval tick. cnt_locked, cnt_unlocked
// and cnt_intr (STREAM_INTERRUPTED) stay per-event ("incremented each
// time"). The replica models the interval divider cycle-exactly (registered
// tick, tick-cycle events harvested into the closing interval), so every
// per-PDU compare below also pins the interval machinery. The dedicated
// [Table 5.6] section is the mutation anchor: revert the RTL to per-frame
// counting and a 10-PDU burst reads +10 where +1 is pinned.
//
// The [AVTP-5t] section pins the five counters that used to be advertised
// in the 0xF3F mask and served as CONSTANT ZERO. Laws under test, mirroring
// the AAF audit's [30a1-30g]/[IV8]/[IV9] pattern:
//   MEDIA_RESET        the RECEIVED mr bit TOGGLING (byte O+1 bit 3); a
//                      HELD mr counts nothing, and the era's first PDU
//                      seeds without counting
//   TIMESTAMP_UNCERTAIN the received tu bit (CRF alternative header: byte
//                      O+1 bit 0, NOT the common header's byte O+3)
//   LATE/EARLY         the CRF reference timestamp vs ptp_now: in the past
//                      / further ahead than MAXTT_NS_P + 10 ms
//   STREAM_INTERRUPTED per-EVENT, >= 2 lost AVTPDUs (no interval fold)
// and in every case a REJECTED PDU counts none of them.
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
#if !defined(MAXTT_NS_C) || !defined(EARLY_M_NS_C)
#error "MAXTT_NS_C / EARLY_M_NS_C must come from the Makefile (RTL twins)"
#endif
// derived here exactly as the RTL derives EARLY_LIMIT_C from its two
// parameters — the sum is never written down as a literal on either side
static const uint32_t EARLY_LIMIT_C = MAXTT_NS_C + EARLY_M_NS_C;

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
    uint32_t cnt_i = 0;                  // STREAM_INTERRUPTED (per-event)
    int32_t  delta = 0, rate = 0;
    uint16_t pdu = 0;                    // FRAMES_RX interval commits
    uint8_t  fmt_e = 0, seq_e = 0;       // UF / SM interval commits
    uint16_t mr_c = 0, tu_c = 0;         // MR / TU interval commits
    uint16_t lt_c = 0, et_c = 0;         // LATE / EARLY interval commits
    // mr reference for the current binding era: seeded, not counted, by
    // the era's first accepted PDU
    bool     prev_mr = false, mr_seeded = false;

    // Table 5.6 interval machinery, cycle-exact mirror of iv_tick_gen +
    // the engine's commit/fold: iv_tick is REGISTERED (pulses the cycle
    // after the divider wraps); an event in the commit cycle itself is
    // harvested into the closing interval.
    uint32_t iv_div = 0;
    bool     iv_tick = false;
    bool     f_frx = false, f_uf = false, f_sm = false;
    bool     f_mr = false, f_tu = false, f_lt = false, f_et = false;

    void cycle(bool frx_ev, bool uf_ev, bool sm_ev,
               bool mr_ev, bool tu_ev, bool lt_ev, bool et_ev) {
        if (iv_tick) {
            if (f_frx || frx_ev) pdu++;
            if (f_uf  || uf_ev)  { if (fmt_e != 0xFF) fmt_e++; }
            if (f_sm  || sm_ev)  { if (seq_e != 0xFF) seq_e++; }
            if (f_mr  || mr_ev)  mr_c++;   // 16-bit, wraps (Milan 5.3.8.10)
            if (f_tu  || tu_ev)  tu_c++;
            if (f_lt  || lt_ev)  lt_c++;
            if (f_et  || et_ev)  et_c++;
            f_frx = f_uf = f_sm = false;
            f_mr = f_tu = f_lt = f_et = false;
        } else {
            f_frx |= frx_ev; f_uf |= uf_ev; f_sm |= sm_ev;
            f_mr  |= mr_ev;  f_tu |= tu_ev; f_lt |= lt_ev; f_et |= et_ev;
        }
        if (iv_div >= IVAL_CYC_C - 1) { iv_div = 0; iv_tick = true;  }
        else                          { iv_div++;   iv_tick = false; }
    }

    void good_pdu(uint64_t ts, uint8_t seq, uint64_t ptp, bool mr) {
        if (have_seq && seq != exp_seq) {
            settle = 0;                  // discontinuity breaks the settle run
            // STREAM_INTERRUPTED: "the loss of several AVTPDUs", per-event
            if ((uint8_t)(seq - exp_seq) >= 2) cnt_i++;
        } else if (settle != 7) {
            settle++;
        } else if (!locked) {
            locked = true; cnt_l++;
        }
        exp_seq  = (uint8_t)(seq + 1);
        have_seq = true;
        prev_mr  = mr;                   // seed/track the mr level
        mr_seeded = true;
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
        mr_seeded = false;               // the mr level died with the stream
    }
    // Milan v1.2 5.3.8.10, the sentence closing Table 5.6: "The PAAD-AE
    // shall reset all of these counters to zero each time the Stream Input
    // changes its state from not bound to bound" (and NOT the other way).
    // locked falls with them and does NOT score an unlock — Table 5.6 reads
    // MEDIA_LOCKED == MEDIA_UNLOCKED as "not synchronized", and a +1 into a
    // zeroed MEDIA_UNLOCKED would strand the sink at UNLOCKED = LOCKED + 1.
    void bind_zero() {
        pdu = 0; fmt_e = 0; seq_e = 0;
        mr_c = 0; tu_c = 0; lt_c = 0; et_c = 0;
        cnt_l = 0; cnt_u = 0; cnt_i = 0;
        locked = false;
        f_frx = f_uf = f_sm = false;
        f_mr = f_tu = f_lt = f_et = false;
        settle = 0; have_seq = false; mr_seeded = false;
    }
};

static Model m;
static long g_pdu_no = 0;                // global accepted-PDU ordinal

static const uint64_t SID_C  = 0x0200000000010001ULL;
static const int SETTLE_TICKS_C = 4;     // sample point after each pulse

// this-cycle Table 5.6 events, consumed by the next tick()
static bool g_ev_frx = false, g_ev_uf = false, g_ev_sm = false;
static bool g_ev_mr = false, g_ev_tu = false, g_ev_lt = false, g_ev_et = false;
static bool g_in_reset = true;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    if (!g_in_reset) m.cycle(g_ev_frx, g_ev_uf, g_ev_sm,
                             g_ev_mr, g_ev_tu, g_ev_lt, g_ev_et);
    g_ev_frx = g_ev_uf = g_ev_sm = false;
    g_ev_mr = g_ev_tu = g_ev_lt = g_ev_et = false;
}

// run to the first cycle of a FRESH observation interval (model divider 1 =
// the cycle right after a commit edge): a burst launched here has a full
// tick-free window of IVAL_CYC_C-1 cycles ahead of it
static void align_interval() {
    while (m.iv_div != 1) tick();
}

// header-flag levels held across PDUs, exactly as the wire holds them:
// mr is a LEVEL the talker toggles (1722-2016 10.4.3), tu a per-PDU flag
static bool g_mr = false, g_tu = false;

static void drive_fields(uint64_t ts, uint8_t seq) {
    dut->subtype_i   = 0x04;
    dut->type_i      = 0x01;
    dut->seq_i       = seq;
    dut->sid_frame_i = SID_C;
    dut->pullbase_i  = 48000;            // pull=0 | base 48000
    dut->fsh_i       = (8ULL << 48) | (96ULL << 32) | (ts >> 32);
    dut->fsh2_i      = (ts & 0xFFFFFFFFULL) << 32;
    dut->mr_i        = g_mr;
    dut->tu_i        = g_tu;
}

// Table 5.6 late/early verdict for a PDU, computed the way the RTL does
static bool ts_late (uint64_t ts, uint64_t ptp) {
    return (int32_t)(uint32_t)(ts - ptp) < 0;
}
static bool ts_early(uint64_t ts, uint64_t ptp) {
    int32_t d = (int32_t)(uint32_t)(ts - ptp);
    return d >= 0 && (uint32_t)d > EARLY_LIMIT_C;
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
    ckq("mr_cnt_o",       no, dut->mr_cnt_o,          m.mr_c);
    ckq("tu_cnt_o",       no, dut->tu_cnt_o,          m.tu_c);
    ckq("late_cnt_o",     no, dut->late_cnt_o,        m.lt_c);
    ckq("early_cnt_o",    no, dut->early_cnt_o,       m.et_c);
    ckq("cnt_locked_o",   no, dut->cnt_locked_o,      m.cnt_l);
    ckq("cnt_unlocked_o", no, dut->cnt_unlocked_o,    m.cnt_u);
    ckq("cnt_intr_o",     no, dut->cnt_intr_o,        m.cnt_i);
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
    g_ev_mr  = (m.mr_seeded && g_mr != m.prev_mr);
    g_ev_tu  = g_tu;
    g_ev_lt  = ts_late(ts, ptp);
    g_ev_et  = ts_early(ts, ptp);
    pulse();
    for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
    m.good_pdu(ts, seq, ptp, g_mr);
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

    // disabled: matching PDUs must be ignored.
    // The nominal timelines put crf_ts AHEAD of ptp_now by 1 ms, which is
    // what IEEE 1722-2016 10.7 mandates (T_CRF = source + Max Transit
    // Time) and is inside the Table 5.6 window: a healthy CRF stream must
    // tick NEITHER LATE_TIMESTAMP nor EARLY_TIMESTAMP.
    uint64_t ts  = 1000000000ULL;        // talker CRF timeline
    uint64_t ptp =  999000000ULL;        // observer gPTP timeline
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
        g_ev_mr  = (m.mr_seeded && g_mr != m.prev_mr);
        g_ev_tu  = g_tu;
        g_ev_lt  = ts_late(ts, ptp);
        g_ev_et  = ts_early(ts, ptp);
        pulse();
        int lat = 0;
        while ((int32_t)dut->rate_o == old_rate && lat <= 3) { tick(); lat++; }
        for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.good_pdu(ts, seq, ptp, g_mr); seq++;
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

    //-----------------------------------------------------------------------
    // [AVTP-5t] The five Table 5.16 counters this engine used to advertise
    // in the 0xF3F mask and serve as CONSTANT ZERO. Each gets its own law
    // check, mirroring the AAF audit's [30a1-30g]/[IV8]/[IV9] pattern.
    //-----------------------------------------------------------------------
    printf("\n[AVTP-5t] the five formerly-constant Table 5.16 counters\n");

    // -- a) baseline: a healthy stream moves NONE of them ------------------
    {
        align_interval();
        uint16_t mr0 = dut->mr_cnt_o, tu0 = dut->tu_cnt_o;
        uint16_t lt0 = dut->late_cnt_o, et0 = dut->early_cnt_o;
        uint32_t si0 = dut->cnt_intr_o;
        for (int n = 0; n < 6; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-a1] clean stream: MEDIA_RESET still", dut->mr_cnt_o, mr0);
        ck("[5t-a2] clean stream: TIMESTAMP_UNCERTAIN still",
           dut->tu_cnt_o, tu0);
        ck("[5t-a3] clean stream: LATE_TIMESTAMP still",
           dut->late_cnt_o, lt0);
        ck("[5t-a4] clean stream: EARLY_TIMESTAMP still",
           dut->early_cnt_o, et0);
        ck("[5t-a5] clean stream: STREAM_INTERRUPTED still",
           dut->cnt_intr_o, si0);
        ck("[5t-a6] and none of them is stuck at the old constant 0",
           (long)(dut->pdu_count_o > 0), 1);
    }

    // -- b) MEDIA_RESET: the TOGGLE counts, a HELD mr counts nothing -------
    {
        align_interval();
        uint16_t mr0 = dut->mr_cnt_o;
        g_mr = true;                     // toggle 0 -> 1 on this PDU
        ts += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ptp);
        ck("[5t-b1] mr toggle: uncommitted before the tick",
           dut->mr_cnt_o, mr0);
        for (int n = 0; n < 8; n++) {    // HELD at 1 (>= 8 PDUs, 10.4.3)
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-b2] one toggle + 8 held PDUs: MEDIA_RESET +1, not +9",
           dut->mr_cnt_o, (uint16_t)(mr0 + 1));

        align_interval();
        for (int n = 0; n < 5; n++) {    // still held: nothing more
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-b3] a HELD mr counts nothing at all",
           dut->mr_cnt_o, (uint16_t)(mr0 + 1));

        // two toggles inside ONE interval fold to a single commit
        align_interval();
        g_mr = false; ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        g_mr = true;  ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-b4] two toggles in one interval: +1, not +2",
           dut->mr_cnt_o, (uint16_t)(mr0 + 2));

        // a REJECTED PDU carrying a toggle counts NOTHING (not even UF's
        // sibling): the accept gate is upstream of every Table 5.6 verdict
        align_interval();
        uint16_t mrb = dut->mr_cnt_o;
        uint8_t  ufb = dut->fmt_err_o;
        g_mr = false;                    // would be a toggle if accepted
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);  // bad ival
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-b5] rejected PDU: MEDIA_RESET untouched", dut->mr_cnt_o, mrb);
        ck("[5t-b6] rejected PDU: UNSUPPORTED_FORMAT +1 (and only it)",
           dut->fmt_err_o, (uint8_t)(ufb + 1));
        g_mr = true;                     // the reject never moved the level

        // the same accept gate for the OTHER three PDU-derived verdicts: a
        // matched-but-malformed PDU carrying tu = 1 AND a timestamp already
        // in the past must move UNSUPPORTED_FORMAT and nothing else. Milan
        // Table 5.6 scopes tu/late/early to "the received Stream Data
        // AVTPDUs" of THIS Stream Input, and 5.4.2.25's own
        // UNSUPPORTED_FORMAT row is what a wrong-format PDU is for — reading
        // its header fields as measurements of the bound stream would let a
        // foreign profile forge this sink's diagnostics.
        align_interval();
        uint16_t tub = dut->tu_cnt_o, ltb = dut->late_cnt_o;
        uint16_t etb = dut->early_cnt_o;
        uint8_t  ufc = dut->fmt_err_o;
        g_tu = true;
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);  // bad ival
        dut->ptp_now_i = ts + 4000000;   // and a LATE reference timestamp
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        // a second reject, this one EARLY
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);
        dut->ptp_now_i = ts - (uint64_t)EARLY_LIMIT_C - 5000000ULL;
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        g_tu = false;
        dut->ptp_now_i = ptp;
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-b7] rejected PDU: TIMESTAMP_UNCERTAIN untouched",
           dut->tu_cnt_o, tub);
        ck("[5t-b8] rejected PDU: LATE_TIMESTAMP untouched",
           dut->late_cnt_o, ltb);
        ck("[5t-b9] rejected PDU: EARLY_TIMESTAMP untouched",
           dut->early_cnt_o, etb);
        ck("[5t-b10] the two rejects fold to ONE UNSUPPORTED_FORMAT",
           dut->fmt_err_o, (uint8_t)(ufc + 1));
    }

    // -- c) TIMESTAMP_UNCERTAIN: per-interval, N tu PDUs -> +1 -------------
    {
        align_interval();
        uint16_t tu0 = dut->tu_cnt_o;
        g_tu = true;
        for (int n = 0; n < 7; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        ck("[5t-c1] tu burst: uncommitted before the tick",
           dut->tu_cnt_o, tu0);
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-c2] 7 tu PDUs in one interval: +1, not +7",
           dut->tu_cnt_o, (uint16_t)(tu0 + 1));
        // second interval with tu set = a second commit
        align_interval();
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-c3] a second tu interval: +1 more",
           dut->tu_cnt_o, (uint16_t)(tu0 + 2));
        g_tu = false;
        align_interval();
        for (int n = 0; n < 4; n++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-c4] tu clear: TIMESTAMP_UNCERTAIN stops",
           dut->tu_cnt_o, (uint16_t)(tu0 + 2));
    }

    // -- d) LATE / EARLY: the CRF reference timestamp vs gPTP now ----------
    {
        align_interval();
        uint16_t lt0 = dut->late_cnt_o, et0 = dut->early_cnt_o;
        // 5 PDUs whose reference instant already passed (10.6's
        // unreserved-stream case; Milan 7.3.3 says this must not happen).
        // The gPTP observation instant is derived FROM the PDU's own
        // timestamp, so the verdict does not ride the trajectory's drift.
        for (int n = 0; n < 5; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ts + 4000000);    // gPTP 4 ms past the ts
        }
        ck("[5t-d1] LATE uncommitted before the tick", dut->late_cnt_o, lt0);
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-d2] 5 late PDUs in one interval: LATE +1",
           dut->late_cnt_o, (uint16_t)(lt0 + 1));
        ck("[5t-d3] EARLY untouched by LATE PDUs", dut->early_cnt_o, et0);

        // two more late intervals -> +2 (per-interval, not per-frame)
        for (int k = 0; k < 2; k++) {
            align_interval();
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ts + 4000000);
            for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        }
        ck("[5t-d4] LATE +2 across two more intervals",
           dut->late_cnt_o, (uint16_t)(lt0 + 3));

        // 4 PDUs further ahead than MAXTT + margin
        align_interval();
        for (int n = 0; n < 4; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ts - (uint64_t)EARLY_LIMIT_C - 5000000ULL);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-d5] 4 early PDUs in one interval: EARLY +1",
           dut->early_cnt_o, (uint16_t)(et0 + 1));
        ck("[5t-d6] LATE untouched by EARLY PDUs",
           dut->late_cnt_o, (uint16_t)(lt0 + 3));

        // exactly at the limit is still on time (strict >)
        align_interval();
        ts += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ts - (uint64_t)EARLY_LIMIT_C);
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-d7] delta == the limit is NOT early",
           dut->early_cnt_o, (uint16_t)(et0 + 1));

        // the other boundary: crf_ts EXACTLY at gPTP now is not "in the
        // past" - LATE is a strictly-negative delta
        align_interval();
        ts += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ts);
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-d7b] delta == 0 is NOT late",
           dut->late_cnt_o, (uint16_t)(lt0 + 3));

        align_interval();
        for (int n = 0; n < 4; n++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-d8] on-time PDUs move neither",
           (long)(dut->late_cnt_o == (uint16_t)(lt0 + 3) &&
                  dut->early_cnt_o == (uint16_t)(et0 + 1)), 1);
    }

    // -- e) STREAM_INTERRUPTED is PER-EVENT, never interval-folded ---------
    {
        align_interval();
        uint32_t si0 = dut->cnt_intr_o;
        uint8_t  s0  = dut->seq_err_o;
        // ONE lost PDU is not "several": SEQ_NUM_MISMATCH only
        ts += 2000200; ptp += 2000000;
        seq += 1;                        // one gap
        good_pdu(ts, seq++, ptp);
        ck("[5t-e1] 1 lost AVTPDU: STREAM_INTERRUPTED unmoved",
           dut->cnt_intr_o, si0);
        // 3 discontinuities of >= 2 lost, all inside ONE interval: a
        // per-event counter moves 3, an interval one would move 1
        for (int n = 0; n < 3; n++) {
            ts += 2000200; ptp += 2000000;
            seq += 4;                    // 4 lost each time
            good_pdu(ts, seq++, ptp);
        }
        ck("[5t-e2] 3 gaps in ONE interval: +3 immediately (per-event)",
           dut->cnt_intr_o, si0 + 3);
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-e3] the interval tick adds nothing to it",
           dut->cnt_intr_o, si0 + 3);
        ck("[5t-e4] the same 4 gaps fold to ONE SEQ_NUM_MISMATCH",
           dut->seq_err_o, (uint8_t)(s0 + 1));
    }

    // -- f) an unbind cannot be an interruption (clause exclusion) ---------
    {
        uint32_t si0 = dut->cnt_intr_o;
        dut->en_i = 0;                   // Controller Unbind
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        align_interval();
        ts += 2000200; ptp += 2000000;   // frames keep arriving, unbound
        seq += 9;
        drive_fields(ts, seq);
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-f1] unbound: STREAM_INTERRUPTED cannot move",
           dut->cnt_intr_o, si0);
        // rebind: the previous era's mr level must not score as a toggle.
        // The bind edge ALSO zeroes every Table 5.6 tally (5.3.8.10, pinned
        // in full by section g), so the post-rebind expectation is 0 — and
        // it bites both laws: a broken era wipe reads the pre-unbind total,
        // a broken mr re-seed reads exactly 1.
        dut->en_i = 1;
        g_mr = !g_mr;                    // new talker, opposite mr level
        m.bind_zero();
        align_interval();
        for (int n = 0; n < 3; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-f2] rebind re-seeds mr: no phantom MEDIA_RESET",
           dut->mr_cnt_o, 0);
        ck("[5t-f3] the unbind's own sequence jump is not an interruption",
           dut->cnt_intr_o, 0);
        ck("[5t-f4] and the new era IS counting (FRAMES_RX moved off 0)",
           (long)(dut->pdu_count_o > 0), 1);
    }

    //-----------------------------------------------------------------------
    // [5t-g] The era wipe. Milan v1.2 5.3.8.10, the sentence that closes
    // Table 5.6: "The PAAD-AE shall reset all of these counters to zero each
    // time the Stream Input changes its state from not bound to bound." The
    // clause is deliberately ASYMMETRIC — "the PAAD-AE does not reset these
    // counters when the Stream Input changes its state from bound to not
    // bound" — so both edges are pinned here. Carrying a dead era's totals
    // into a new binding is the same defect class as the five constant
    // zeros: a number a Controller cannot interpret.
    //-----------------------------------------------------------------------
    printf("\n[5t-g] Milan 5.3.8.10 era wipe (not bound -> bound)\n");
    {
        // ---- build a NON-ZERO value into all ten -------------------------
        // lock (cnt_locked), then 100 ms silence (cnt_unlocked), then re-lock
        for (int n = 0; n < 10; n++) {   // clean run -> MEDIA_LOCKED
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        for (int i = 0; i < 20005; i++) tick();      // TOUT_CYC_C @ 200 kHz
        m.timeout();                                 // -> MEDIA_UNLOCKED
        ts += 100000000; ptp += 100000000;
        for (int n = 0; n < 10; n++) {               // -> MEDIA_LOCKED again
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        align_interval();
        // one gap of >= 2 -> SEQ_NUM_MISMATCH + STREAM_INTERRUPTED
        ts += 2000200; ptp += 2000000; seq += 3;
        good_pdu(ts, seq++, ptp);
        // an mr toggle, a tu PDU, a late PDU and an early PDU
        g_mr = !g_mr;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        g_tu = true;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        g_tu = false;
        ts += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ts + 4000000);                    // LATE
        ts += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ts - (uint64_t)EARLY_LIMIT_C - 5000000ULL);  // EARLY
        // a format reject -> UNSUPPORTED_FORMAT
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();

        struct { const char* n; long v; } all10[] = {
            {"MEDIA_LOCKED",        (long)dut->cnt_locked_o},
            {"MEDIA_UNLOCKED",      (long)dut->cnt_unlocked_o},
            {"STREAM_INTERRUPTED",  (long)dut->cnt_intr_o},
            {"SEQ_NUM_MISMATCH",    (long)dut->seq_err_o},
            {"MEDIA_RESET",         (long)dut->mr_cnt_o},
            {"TIMESTAMP_UNCERTAIN", (long)dut->tu_cnt_o},
            {"UNSUPPORTED_FORMAT",  (long)dut->fmt_err_o},
            {"LATE_TIMESTAMP",      (long)dut->late_cnt_o},
            {"EARLY_TIMESTAMP",     (long)dut->early_cnt_o},
            {"FRAMES_RX",           (long)dut->pdu_count_o},
        };
        for (auto& c : all10) {
            char b[96];
            snprintf(b, sizeof b, "[5t-g1] pre-unbind %s is NON-ZERO", c.n);
            ck(b, (long)(c.v > 0), 1);
        }
        // Table 5.6's own invariant on the pair, in its synchronized state
        ck("[5t-g2] bound+locked: MEDIA_LOCKED == MEDIA_UNLOCKED + 1",
           (long)dut->cnt_locked_o, (long)dut->cnt_unlocked_o + 1);

        // ---- bound -> NOT bound: the clause says do NOT reset ------------
        long keep[10];
        for (int k = 0; k < 10; k++) keep[k] = all10[k].v;
        dut->en_i = 0;
        for (int i = 0; i < 3 * (IVAL_CYC_C + 2); i++) tick();
        long after_unbind[10] = {
            (long)dut->cnt_locked_o, (long)dut->cnt_unlocked_o,
            (long)dut->cnt_intr_o,   (long)dut->seq_err_o,
            (long)dut->mr_cnt_o,     (long)dut->tu_cnt_o,
            (long)dut->fmt_err_o,    (long)dut->late_cnt_o,
            (long)dut->early_cnt_o,  (long)dut->pdu_count_o };
        for (int k = 0; k < 10; k++) {
            char b[96];
            snprintf(b, sizeof b, "[5t-g3] unbind must NOT reset %s",
                     all10[k].n);
            ck(b, after_unbind[k], keep[k]);
        }

        // ---- NOT bound -> bound: the clause says reset ALL of them -------
        dut->en_i = 1;
        m.bind_zero();
        for (int i = 0; i < 4; i++) tick();
        long after_bind[10] = {
            (long)dut->cnt_locked_o, (long)dut->cnt_unlocked_o,
            (long)dut->cnt_intr_o,   (long)dut->seq_err_o,
            (long)dut->mr_cnt_o,     (long)dut->tu_cnt_o,
            (long)dut->fmt_err_o,    (long)dut->late_cnt_o,
            (long)dut->early_cnt_o,  (long)dut->pdu_count_o };
        for (int k = 0; k < 10; k++) {
            char b[96];
            snprintf(b, sizeof b, "[5t-g4] bind edge zeroes %s", all10[k].n);
            ck(b, after_bind[k], 0);
        }
        // the stranding rule: locked_o has to fall WITH the zeroed pair, and
        // the fall must not score an unlock — MEDIA_LOCKED = 0,
        // MEDIA_UNLOCKED = 1 would be UNLOCKED = LOCKED + 1, a state Table
        // 5.6 does not allow
        ck("[5t-g5] bind edge drops locked_o with the pair", dut->locked_o, 0);
        ck("[5t-g6] the drop scores NO unlock (LOCKED == UNLOCKED == 0)",
           (long)(dut->cnt_locked_o == 0 && dut->cnt_unlocked_o == 0), 1);

        // ---- the new era counts from zero, on the same instrument --------
        align_interval();
        for (int n = 0; n < 10; n++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < IVAL_CYC_C + 2; i++) tick();
        ck("[5t-g7] new era re-locks from zero: MEDIA_LOCKED 1",
           dut->cnt_locked_o, 1);
        ck("[5t-g8] new era counts FRAMES_RX from zero",
           (long)(dut->pdu_count_o > 0), 1);

        // ---- a seen flag raised before the bind must die with the era ----
        // tu is set on an accepted PDU, then the bind lands BEFORE the
        // interval tick: the flag must not commit +1 into the zeroed counter
        align_interval();
        g_tu = true;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        g_tu = false;
        ck("[5t-g9] tu flag raised, not yet committed", dut->tu_cnt_o, 0);
        dut->en_i = 0; tick(); tick();
        dut->en_i = 1;
        m.bind_zero();
        for (int i = 0; i < 2 * (IVAL_CYC_C + 2); i++) tick();
        ck("[5t-g10] a pre-bind interval flag cannot commit after the wipe",
           dut->tu_cnt_o, 0);
    }

    printf("======================================================================\n");
    printf("KL_crf_rx: %ld checks, %ld failures (%ld accepted PDUs pinned)\n",
           checks, fails, g_pdu_no);
    delete dut;
    return fails ? 1 : 0;
}
