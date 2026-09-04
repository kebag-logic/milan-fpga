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
#include "VKL_crf_rx___024root.h"   // [G1] preload: the public flop names
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <cstdint>

#ifndef IVAL_CYC_C
#error "IVAL_CYC_C must come from the Makefile (the -GIVAL_CYC_P twin)"
#endif
#if !defined(MAXTT_NS_C) || !defined(EARLY_M_NS_C)
#error "MAXTT_NS_C / EARLY_M_NS_C must come from the Makefile (RTL twins)"
#endif
// The Makefile's three -D twins are the transport; these are what the
// harness reads. A macro has no type and no scope, a constexpr has both.
constexpr uint32_t kIvalCyc       = IVAL_CYC_C;
constexpr uint32_t kMaxttNs       = MAXTT_NS_C;
constexpr uint32_t kEarlyMarginNs = EARLY_M_NS_C;
// derived here exactly as the RTL derives EARLY_LIMIT_C from its two
// parameters — the sum is never written down as a literal on either side
constexpr uint32_t EARLY_LIMIT_C = kMaxttNs + kEarlyMarginNs;

namespace {

//---------------------------------------------------------------------------
// Independent replica of the measurement engine (Milan v1.2 7.3.2-7.3.4 +
// Table 5.6): 256-deep ts ring, 512 ms window rate, 8-PDU settle lock,
// 100 ms drop, observation-interval counter commit.
//---------------------------------------------------------------------------
struct Model {
    static constexpr int      DEPTH = 256;
    // the 512 ms rate window in ns: DEPTH entries of the 2 ms PDU grid
    static constexpr uint64_t RATE_WINDOW_NS = 512000000ULL;
    // zero-initialised because the replica is a member of a stack-allocated
    // harness now, not a file-scope static: the ring must start where the
    // static-storage one did, even though no read reaches an unwritten slot
    // (a slot is only read once hfill has counted DEPTH pushes into it)
    uint64_t hist[DEPTH] = {};
    int      hidx = 0;
    int      hfill = 0;
    uint8_t  exp_seq = 0;
    bool     have_seq = false;
    int      settle = 0;                 // 0..7
    bool     locked = false;
    uint32_t cnt_l = 0;
    uint32_t cnt_u = 0;
    uint32_t cnt_i = 0;                  // STREAM_INTERRUPTED (per-event)
    int32_t  delta = 0;
    int32_t  rate = 0;
    // gh #61 G1: all seven interval tallies are 32-bit WRAPPING - the old
    // 8-bit fmt/seq SATURATION violated 5.3.8.10's "wraps back to zero"
    // (a pegged instrument is frozen), and 16 bits wrapped at the
    // 65536 s = 18 h 12 min soak mark
    uint32_t pdu = 0;                    // FRAMES_RX interval commits
    uint32_t fmt_e = 0;                  // UF interval commits
    uint32_t seq_e = 0;                  // SM interval commits
    uint32_t mr_c = 0;                   // MR interval commits
    uint32_t tu_c = 0;                   // TU interval commits
    uint32_t lt_c = 0;                   // LATE interval commits
    uint32_t et_c = 0;                   // EARLY interval commits
    // mr reference for the current binding era: seeded, not counted, by
    // the era's first accepted PDU
    bool     prev_mr = false;
    bool     mr_seeded = false;
    // Milan 5.3.8.7 stopped state (issue #97): observation continues,
    // consumption stops - only the settle/lock arms below read it
    bool     stop = false;

    // Table 5.6 interval machinery, cycle-exact mirror of iv_tick_gen +
    // the engine's commit/fold: iv_tick is REGISTERED (pulses the cycle
    // after the divider wraps); an event in the commit cycle itself is
    // harvested into the closing interval.
    uint32_t iv_div = 0;
    bool     iv_tick = false;
    bool     f_frx = false;
    bool     f_uf = false;
    bool     f_sm = false;
    bool     f_mr = false;
    bool     f_tu = false;
    bool     f_lt = false;
    bool     f_et = false;

    void cycle(bool frx_ev, bool uf_ev, bool sm_ev,
               bool mr_ev, bool tu_ev, bool lt_ev, bool et_ev) {
        if (iv_tick) {
            if (f_frx || frx_ev) pdu++;
            if (f_uf  || uf_ev)  fmt_e++;  // no peg: 32-bit wrap is the law
            if (f_sm  || sm_ev)  seq_e++;
            if (f_mr  || mr_ev)  mr_c++;
            if (f_tu  || tu_ev)  tu_c++;
            if (f_lt  || lt_ev)  lt_c++;
            if (f_et  || et_ev)  et_c++;
            f_frx = f_uf = f_sm = false;
            f_mr = f_tu = f_lt = f_et = false;
        } else {
            f_frx |= frx_ev; f_uf |= uf_ev; f_sm |= sm_ev;
            f_mr  |= mr_ev;  f_tu |= tu_ev; f_lt |= lt_ev; f_et |= et_ev;
        }
        if (iv_div >= kIvalCyc - 1) { iv_div = 0; iv_tick = true;  }
        else                        { iv_div++;   iv_tick = false; }
    }

    void good_pdu(uint64_t ts, uint8_t seq, uint64_t ptp, bool mr) {
        if (have_seq && seq != exp_seq) {
            settle = 0;                  // discontinuity breaks the settle run
            // STREAM_INTERRUPTED: "the loss of several AVTPDUs", per-event
            if (static_cast<uint8_t>(seq - exp_seq) >= 2) cnt_i++;
        } else if (stop) {
            // a stopped sink's accepts advance nothing toward lock
        } else if (settle != 7) {
            settle++;
        } else if (!locked) {
            locked = true; cnt_l++;
        }
        exp_seq  = static_cast<uint8_t>(seq + 1);
        have_seq = true;
        prev_mr  = mr;                   // seed/track the mr level
        mr_seeded = true;
        delta = static_cast<int32_t>(static_cast<uint32_t>(ts - ptp));
        if (hfill == DEPTH) {
            rate = static_cast<int32_t>(
                static_cast<uint32_t>((ts - hist[hidx]) - RATE_WINDOW_NS));
        } else {
            hfill++;
        }
        hist[hidx] = ts;
        hidx = (hidx + 1) & (DEPTH - 1);
    }
    void bad_pdu() {                     // format-invalid, matched stream
        settle = 0;                      // the UF count commits via cycle()
    }
    void timeout() {                     // 100 ms without a CONSUMED PDU
        if (locked) { locked = false; cnt_u++; }
        settle = 0;
        // stopped, the frames may still be arriving and counted: the
        // sequence cursor, ring fill and mr reference stay live (a reset
        // here would fake SEQ_NUM_MISMATCH and MEDIA_RESET on restart)
        if (!stop) {
            have_seq = false; hfill = 0;
            mr_seeded = false;           // the mr level died with the stream
        }
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

constexpr uint64_t SID_C = 0x0200000000010001ULL;
constexpr int SETTLE_TICKS_C = 4;        // sample point after each pulse
// the 100 ms lock timeout drilled in sim time: TOUT_CYC_C is 20 000 cycles
// at the Makefile's 200 kHz, and the harness drives a few cycles past it
constexpr int kSilenceCyc = 20005;

//---------------------------------------------------------------------------
// The measurement-engine harness. The DUT handle, the replica, the observed
// strobe tallies and the two timelines are members, so no phase below can be
// read without its state in view (Core Guidelines I.2), and each phase is a
// named function saying what it PROVES (F.3).
//---------------------------------------------------------------------------
class CrfRxHarness {
 public:
    //! Every phase in order, then the tally line the sweep parses.
    int run() {
        const milan::tb::Model<VKL_crf_rx> model;
        dut = model.get();                   // this file's observing pointer

        apply_reset();
        pin_reset_and_selection_gating();
        pin_format_validation();
        pin_plus_100ppm_trajectory();
        pin_minus_50ppm_slope_change();
        pin_sequence_discontinuity();
        pin_silence_unlock_and_refill();
        pin_interval_burst_semantics();
        pin_five_formerly_constant_counters();
        pin_milan_era_wipe();
        pin_dirty_push_source_law();
        pin_restart_echo();
        pin_wrap_backing_and_slice_abi();
        pin_stopped_sink();

        printf("======================================================================\n");
        printf("KL_crf_rx: %ld checks, %ld failures (%ld accepted PDUs pinned)\n",
               checks, fails, g_pdu_no);
        return fails ? 1 : 0;
    }

 private:
    VKL_crf_rx* dut = nullptr;
    long checks = 0;
    long fails = 0;

    Model m;
    long g_pdu_no = 0;                       // global accepted-PDU ordinal

    // this-cycle Table 5.6 events, consumed by the next tick()
    bool g_ev_frx = false;
    bool g_ev_uf = false;
    bool g_ev_sm = false;
    bool g_ev_mr = false;
    bool g_ev_tu = false;
    bool g_ev_lt = false;
    bool g_ev_et = false;
    bool g_in_reset = true;
    // gh #60 F2 push-source pulses observed (dirty_p_o is a 1-cycle strobe)
    long g_dirty_cnt = 0;
    // gh #62 H2a: 10.4.3 restart echoes observed (mr_toggle_p_o, 1-cycle strobe).
    // g_mrtog_wide counts consecutive-high cycles so a level masquerading as a
    // pulse cannot pass the count checks below.
    long g_mrtog_cnt = 0;
    long g_mrtog_wide = 0;
    long g_mrtog_run = 0;

    // header-flag levels held across PDUs, exactly as the wire holds them:
    // mr is a LEVEL the talker toggles (1722-2016 10.4.3), tu a per-PDU flag
    bool g_mr = false;
    bool g_tu = false;

    // the pair of timelines every phase advances together, and the AVTPDU
    // sequence cursor that rides them: talker CRF ts, observer gPTP now
    uint64_t ts = 0;
    uint64_t ptp = 0;
    uint8_t seq = 0;

    void ck(const char* what, long long got, long long exp) {
        checks++;
        bool ok = (got == exp);
        if (!ok) fails++;
        printf("  [%s] %-46s got=%lld exp=%lld\n", ok ? "PASS" : "FAIL", what, got, exp);
    }

    // quiet per-PDU compare: prints only on FAIL (thousands of these)
    void ckq(const char* what, long pdu_no, long long got, long long exp) {
        checks++;
        if (got != exp) {
            fails++;
            printf("  [FAIL] pdu#%-5ld %-38s got=%lld exp=%lld\n", pdu_no, what, got, exp);
        }
    }

    void tick() {
        dut->clk_i = 0; dut->eval();
        dut->clk_i = 1; dut->eval();
        if (dut->dirty_p_o) g_dirty_cnt++;
        if (dut->mr_toggle_p_o) {
            g_mrtog_cnt++;
            if (++g_mrtog_run > 1) g_mrtog_wide++;
        } else {
            g_mrtog_run = 0;
        }
        if (!g_in_reset) m.cycle(g_ev_frx, g_ev_uf, g_ev_sm,
                                 g_ev_mr, g_ev_tu, g_ev_lt, g_ev_et);
        g_ev_frx = g_ev_uf = g_ev_sm = false;
        g_ev_mr = g_ev_tu = g_ev_lt = g_ev_et = false;
    }

    // run to the first cycle of a FRESH observation interval (model divider 1 =
    // the cycle right after a commit edge): a burst launched here has a full
    // tick-free window of kIvalCyc-1 cycles ahead of it
    void align_interval() {
        while (m.iv_div != 1) tick();
    }

    void drive_fields(uint64_t ts, uint8_t seq) {
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
    bool ts_late (uint64_t ts, uint64_t ptp) {
        return static_cast<int32_t>(static_cast<uint32_t>(ts - ptp)) < 0;
    }
    bool ts_early(uint64_t ts, uint64_t ptp) {
        int32_t d = static_cast<int32_t>(static_cast<uint32_t>(ts - ptp));
        return d >= 0 && static_cast<uint32_t>(d) > EARLY_LIMIT_C;
    }

    void pulse() {
        dut->frame_p_i = 1; tick();
        dut->frame_p_i = 0;
    }

    void compare(long no) {
        ckq("delta_o",        no, static_cast<int32_t>(dut->delta_o), m.delta);
        ckq("rate_o",         no, static_cast<int32_t>(dut->rate_o),  m.rate);
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
    void feed_good(uint64_t ts, uint8_t seq, uint64_t ptp) {
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
    }
    void good_pdu(uint64_t ts, uint8_t seq, uint64_t ptp) {
        feed_good(ts, seq, ptp);
        compare(++g_pdu_no);
    }

    //! Hold the DUT in reset with a quiet, deselected wire, then release it:
    //! the model's interval divider and the replica's start on the same cycle.
    void apply_reset() {
        dut->rst_n = 0; dut->en_i = 0; dut->frame_p_i = 0;
        dut->sid_i = SID_C; dut->ptp_now_i = 0;
        drive_fields(0, 0);
        for (int i = 0; i < 8; i++) tick();
        dut->rst_n = 1;
        g_in_reset = false;                  // divider runs from here, both sides
        for (int i = 0; i < 8; i++) tick();
    }

    //! Reset values, and the two gates in front of the engine: a disabled
    //! sink and a foreign frame are both invisible to every counter.
    void pin_reset_and_selection_gating() {
        printf("[crf_rx] reset + selection gating\n");
        ck("reset: delta 0",  static_cast<int32_t>(dut->delta_o), 0);
        ck("reset: rate 0",   static_cast<int32_t>(dut->rate_o), 0);
        ck("reset: unlocked", dut->locked_o, 0);

        // disabled: matching PDUs must be ignored.
        // The nominal timelines put crf_ts AHEAD of ptp_now by 1 ms, which is
        // what IEEE 1722-2016 10.7 mandates (T_CRF = source + Max Transit
        // Time) and is inside the Table 5.6 window: a healthy CRF stream must
        // tick NEITHER LATE_TIMESTAMP nor EARLY_TIMESTAMP.
        ts  = 1000000000ULL;             // talker CRF timeline
        ptp =  999000000ULL;             // observer gPTP timeline
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
    }

    //! The Milan 7.3.2 profile gate: five malformed variants, one interval.
    void pin_format_validation() {
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
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("5 malformed: ONE interval tick, not 5", dut->fmt_err_o, 1);
        ck("5 malformed: pdu_count still 0", dut->pdu_count_o, 0);
        ck("5 malformed: unlocked", dut->locked_o, 0);
    }

    //-----------------------------------------------------------------------
    // Pinned trajectory 1: talker at +100 ppm (period 2 000 200 ns),
    // observer nominal. 300 PDUs: delta drifts +200/PDU; rate_o must stay 0
    // until the ring fills (256 PDUs) then read +100 ppm exactly:
    // 256 * 200 = 51 200 ns / 512 ms window. Lock on the 8th clean PDU.
    // FRAMES_RX counts the INTERVALS containing PDUs (replica-pinned per
    // PDU), never the 300 frames.
    //-----------------------------------------------------------------------
    void pin_plus_100ppm_trajectory() {
        printf("[crf_rx] +100 ppm trajectory (300 PDUs, per-PDU pinned)\n");
        seq = 0;
        long rate_first_pdu = -1;
        for (int n = 0; n < 300; n++) {
            ts  += 2000200;                  // +100 ppm of the 2 ms grid
            ptp += 2000000;                  // nominal observer
            good_pdu(ts, seq++, ptp);
            if (rate_first_pdu < 0 && static_cast<int32_t>(dut->rate_o) != 0)
                rate_first_pdu = g_pdu_no;
        }
        ck("lock latched", dut->locked_o, 1);
        ck("cnt_locked 1", dut->cnt_locked_o, 1);
        ck("rate first nonzero on PDU 257 (ring full)", rate_first_pdu, 257);
        ck("rate == +100 ppm exactly (51200 ns/512 ms)",
           static_cast<int32_t>(dut->rate_o), 51200);
        ck("FRAMES_RX == replica interval count", dut->pdu_count_o, m.pdu);
        ck("300 PDUs commit as intervals, NOT frames", dut->pdu_count_o < 300, 1);
    }

    //-----------------------------------------------------------------------
    // Pinned trajectory 2: slope change to -50 ppm (period 1 999 900 ns).
    // rate ramps -300/PDU across the mixed window, settling at
    // 256 * (-100) = -25 600. Every intermediate value pinned vs the replica.
    //-----------------------------------------------------------------------
    void pin_minus_50ppm_slope_change() {
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
            int32_t old_rate = static_cast<int32_t>(dut->rate_o);
            g_ev_frx = true;                 // accepted sequential PDU
            g_ev_mr  = (m.mr_seeded && g_mr != m.prev_mr);
            g_ev_tu  = g_tu;
            g_ev_lt  = ts_late(ts, ptp);
            g_ev_et  = ts_early(ts, ptp);
            pulse();
            int lat = 0;
            while (static_cast<int32_t>(dut->rate_o) == old_rate && lat <= 3) {
                tick();
                lat++;
            }
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
        ck("rate == -50 ppm exactly (-25600 ns/512 ms)",
           static_cast<int32_t>(dut->rate_o), -25600);
    }

    //-----------------------------------------------------------------------
    // Sequence discontinuity: settle broken, lock RETAINED (Milan drops
    // lock only on the 100 ms silence / validation contract); the
    // SEQ_NUM_MISMATCH tally commits at the next interval tick.
    //-----------------------------------------------------------------------
    void pin_sequence_discontinuity() {
        printf("[crf_rx] sequence discontinuity\n");
        ts += 1999900; ptp += 2000000;
        seq++;                               // skip one sequence number
        good_pdu(ts, seq++, ptp);
        ck("seq skip: still locked", dut->locked_o, 1);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("seq skip: ONE interval tick", dut->seq_err_o, 1);
        for (int n = 0; n < 10; n++) {       // clean run rebuilds settle
            ts += 1999900; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        ck("clean resume: no extra lock event", dut->cnt_locked_o, 1);
        ck("clean resume: seq_err holds at 1", dut->seq_err_o, 1);
    }

    //-----------------------------------------------------------------------
    // 100 ms silence: unlock event, ring restarts (hfill=0) but hidx and
    // rate_o hold; after resume rate stays frozen for 256 PDUs, then
    // updates again; re-lock on the 8th clean PDU (cnt_locked -> 2).
    // ~100 empty observation intervals pass: no event, no counter motion.
    //-----------------------------------------------------------------------
    void pin_silence_unlock_and_refill() {
        printf("[crf_rx] 100 ms silence -> unlock -> refill\n");
        int32_t rate_frozen = static_cast<int32_t>(dut->rate_o);
        // close the still-open interval first (its pending FRX flag rightly
        // commits one more tick); THEN the ~100 empty intervals must not move
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        uint32_t pdu_frozen = dut->pdu_count_o;
        for (int i = 0; i < kSilenceCyc; i++) tick();  // TOUT_CYC_C = 20 000 @ 200 kHz
        m.timeout();
        ck("silence: unlocked", dut->locked_o, 0);
        ck("silence: cnt_unlocked 1", dut->cnt_unlocked_o, 1);
        ck("silence: rate holds last value",
           static_cast<int32_t>(dut->rate_o), rate_frozen);
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
            if (rate_change_pdu < 0 &&
                static_cast<int32_t>(dut->rate_o) != rate_frozen)
                rate_change_pdu = g_pdu_no - resume_base;
        }
        ck("re-lock: cnt_locked 2", dut->cnt_locked_o, 2);
        ck("refill: rate frozen for 256 PDUs, moves on 257",
           rate_change_pdu, 257);
        ck("refill: rate == +100 ppm again",
           static_cast<int32_t>(dut->rate_o), 51200);
    }

    //-----------------------------------------------------------------------
    // Table 5.6 interval semantics, the mutation anchor. A burst of N
    // events inside ONE aligned observation interval moves the counter by
    // exactly 1 at the tick ("incremented at the end of every observation
    // interval during which ..."), never by N (the 1722.1 Table 7-153
    // per-frame reading — ~500x high at the CRF 500 PDU/s cadence).
    //-----------------------------------------------------------------------
    void pin_interval_burst_semantics() {
        printf("[crf_rx] Milan Table 5.6 interval semantics (burst -> ONE tick)\n");
        align_interval();
        uint32_t p0 = dut->pdu_count_o;
        for (int n = 0; n < 10; n++) {       // 10 PDUs = 50 cycles < kIvalCyc-1
            ts  += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        ck("burst of 10 accepted: no commit before the tick", dut->pdu_count_o, p0);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("burst of 10 accepted: FRAMES_RX +1, not +10",
           dut->pdu_count_o, (p0 + 1));

        // mixed burst in ONE interval: 3 discontinuities (accepted) + 2 format
        // rejects -> SM +1, UF +1, FRX +1 (the accepted PDUs ride the same
        // interval), all committed together at the tick
        align_interval();
        p0 = dut->pdu_count_o;
        uint32_t f0 = dut->fmt_err_o;
        uint32_t s0 = dut->seq_err_o;
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
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("3 discontinuities: SEQ_NUM_MISMATCH +1", dut->seq_err_o,
           (s0 + 1));
        ck("2 rejects: UNSUPPORTED_FORMAT +1", dut->fmt_err_o, (f0 + 1));
        ck("same interval's accepted PDUs: FRAMES_RX +1", dut->pdu_count_o,
           (p0 + 1));
    }

    //-----------------------------------------------------------------------
    // [AVTP-5t] The five Table 5.16 counters this engine used to advertise
    // in the 0xF3F mask and serve as CONSTANT ZERO. Each gets its own law
    // check, mirroring the AAF audit's [30a1-30g]/[IV8]/[IV9] pattern.
    //-----------------------------------------------------------------------
    void pin_five_formerly_constant_counters() {
        printf("\n[AVTP-5t] the five formerly-constant Table 5.16 counters\n");

        pin_clean_stream_moves_none_of_them();
        pin_media_reset_counts_only_toggles();
        pin_timestamp_uncertain_folds_per_interval();
        pin_late_and_early_against_gptp_now();
        pin_stream_interrupted_is_per_event();
        pin_unbind_is_not_an_interruption();
    }

// -- a) baseline: a healthy stream moves NONE of them ------------------
    void pin_clean_stream_moves_none_of_them() {
        align_interval();
        uint32_t mr0 = dut->mr_cnt_o;
        uint32_t tu0 = dut->tu_cnt_o;
        uint32_t lt0 = dut->late_cnt_o;
        uint32_t et0 = dut->early_cnt_o;
        uint32_t si0 = dut->cnt_intr_o;
        for (int n = 0; n < 6; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
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
           static_cast<long>(dut->pdu_count_o > 0), 1);
    }

// -- b) MEDIA_RESET: the TOGGLE counts, a HELD mr counts nothing -------
    void pin_media_reset_counts_only_toggles() {
        align_interval();
        uint32_t mr0 = dut->mr_cnt_o;
        g_mr = true;                     // toggle 0 -> 1 on this PDU
        ts += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ptp);
        ck("[5t-b1] mr toggle: uncommitted before the tick",
           dut->mr_cnt_o, mr0);
        for (int n = 0; n < 8; n++) {    // HELD at 1 (>= 8 PDUs, 10.4.3)
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-b2] one toggle + 8 held PDUs: MEDIA_RESET +1, not +9",
           dut->mr_cnt_o, (mr0 + 1));

        align_interval();
        for (int n = 0; n < 5; n++) {    // still held: nothing more
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-b3] a HELD mr counts nothing at all",
           dut->mr_cnt_o, (mr0 + 1));

        // two toggles inside ONE interval fold to a single commit
        align_interval();
        g_mr = false; ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        g_mr = true;  ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-b4] two toggles in one interval: +1, not +2",
           dut->mr_cnt_o, (mr0 + 2));

        // a REJECTED PDU carrying a toggle counts NOTHING (not even UF's
        // sibling): the accept gate is upstream of every Table 5.6 verdict
        align_interval();
        uint32_t mrb = dut->mr_cnt_o;
        uint32_t ufb = dut->fmt_err_o;
        g_mr = false;                    // would be a toggle if accepted
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);  // bad ival
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-b5] rejected PDU: MEDIA_RESET untouched", dut->mr_cnt_o, mrb);
        ck("[5t-b6] rejected PDU: UNSUPPORTED_FORMAT +1 (and only it)",
           dut->fmt_err_o, (ufb + 1));
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
        uint32_t tub = dut->tu_cnt_o;
        uint32_t ltb = dut->late_cnt_o;
        uint32_t etb = dut->early_cnt_o;
        uint32_t ufc = dut->fmt_err_o;
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
        dut->ptp_now_i =
            ts - static_cast<uint64_t>(EARLY_LIMIT_C) - 5000000ULL;
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        g_tu = false;
        dut->ptp_now_i = ptp;
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-b7] rejected PDU: TIMESTAMP_UNCERTAIN untouched",
           dut->tu_cnt_o, tub);
        ck("[5t-b8] rejected PDU: LATE_TIMESTAMP untouched",
           dut->late_cnt_o, ltb);
        ck("[5t-b9] rejected PDU: EARLY_TIMESTAMP untouched",
           dut->early_cnt_o, etb);
        ck("[5t-b10] the two rejects fold to ONE UNSUPPORTED_FORMAT",
           dut->fmt_err_o, (ufc + 1));
    }

// -- c) TIMESTAMP_UNCERTAIN: per-interval, N tu PDUs -> +1 -------------
    void pin_timestamp_uncertain_folds_per_interval() {
        align_interval();
        uint32_t tu0 = dut->tu_cnt_o;
        g_tu = true;
        for (int n = 0; n < 7; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ptp);
        }
        ck("[5t-c1] tu burst: uncommitted before the tick",
           dut->tu_cnt_o, tu0);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-c2] 7 tu PDUs in one interval: +1, not +7",
           dut->tu_cnt_o, (tu0 + 1));
        // second interval with tu set = a second commit
        align_interval();
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-c3] a second tu interval: +1 more",
           dut->tu_cnt_o, (tu0 + 2));
        g_tu = false;
        align_interval();
        for (int n = 0; n < 4; n++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-c4] tu clear: TIMESTAMP_UNCERTAIN stops",
           dut->tu_cnt_o, (tu0 + 2));
    }

// -- d) LATE / EARLY: the CRF reference timestamp vs gPTP now ----------
    void pin_late_and_early_against_gptp_now() {
        align_interval();
        uint32_t lt0 = dut->late_cnt_o;
        uint32_t et0 = dut->early_cnt_o;
        // 5 PDUs whose reference instant already passed (10.6's
        // unreserved-stream case; Milan 7.3.3 says this must not happen).
        // The gPTP observation instant is derived FROM the PDU's own
        // timestamp, so the verdict does not ride the trajectory's drift.
        for (int n = 0; n < 5; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ts + 4000000);    // gPTP 4 ms past the ts
        }
        ck("[5t-d1] LATE uncommitted before the tick", dut->late_cnt_o, lt0);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-d2] 5 late PDUs in one interval: LATE +1",
           dut->late_cnt_o, (lt0 + 1));
        ck("[5t-d3] EARLY untouched by LATE PDUs", dut->early_cnt_o, et0);

        // two more late intervals -> +2 (per-interval, not per-frame)
        for (int k = 0; k < 2; k++) {
            align_interval();
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++, ts + 4000000);
            for (int i = 0; i < kIvalCyc + 2; i++) tick();
        }
        ck("[5t-d4] LATE +2 across two more intervals",
           dut->late_cnt_o, (lt0 + 3));

        // 4 PDUs further ahead than MAXTT + margin
        align_interval();
        for (int n = 0; n < 4; n++) {
            ts += 2000200; ptp += 2000000;
            good_pdu(ts, seq++,
                     ts - static_cast<uint64_t>(EARLY_LIMIT_C) - 5000000ULL);
        }
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-d5] 4 early PDUs in one interval: EARLY +1",
           dut->early_cnt_o, (et0 + 1));
        ck("[5t-d6] LATE untouched by EARLY PDUs",
           dut->late_cnt_o, (lt0 + 3));

        // exactly at the limit is still on time (strict >)
        align_interval();
        ts += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ts - static_cast<uint64_t>(EARLY_LIMIT_C));
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-d7] delta == the limit is NOT early",
           dut->early_cnt_o, (et0 + 1));

        // the other boundary: crf_ts EXACTLY at gPTP now is not "in the
        // past" - LATE is a strictly-negative delta
        align_interval();
        ts += 2000200; ptp += 2000000;
        good_pdu(ts, seq++, ts);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-d7b] delta == 0 is NOT late",
           dut->late_cnt_o, (lt0 + 3));

        align_interval();
        for (int n = 0; n < 4; n++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-d8] on-time PDUs move neither",
           static_cast<long>(dut->late_cnt_o == (lt0 + 3) &&
                             dut->early_cnt_o == (et0 + 1)), 1);
    }

// -- e) STREAM_INTERRUPTED is PER-EVENT, never interval-folded ---------
    void pin_stream_interrupted_is_per_event() {
        align_interval();
        uint32_t si0 = dut->cnt_intr_o;
        uint32_t s0  = dut->seq_err_o;
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
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-e3] the interval tick adds nothing to it",
           dut->cnt_intr_o, si0 + 3);
        ck("[5t-e4] the same 4 gaps fold to ONE SEQ_NUM_MISMATCH",
           dut->seq_err_o, (s0 + 1));
    }

// -- f) an unbind cannot be an interruption (clause exclusion) ---------
    void pin_unbind_is_not_an_interruption() {
        uint32_t si0 = dut->cnt_intr_o;
        dut->en_i = 0;                   // Controller Unbind
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        align_interval();
        ts += 2000200; ptp += 2000000;   // frames keep arriving, unbound
        seq += 9;
        drive_fields(ts, seq);
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
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
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-f2] rebind re-seeds mr: no phantom MEDIA_RESET",
           dut->mr_cnt_o, 0);
        ck("[5t-f3] the unbind's own sequence jump is not an interruption",
           dut->cnt_intr_o, 0);
        ck("[5t-f4] and the new era IS counting (FRAMES_RX moved off 0)",
           static_cast<long>(dut->pdu_count_o > 0), 1);
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
    void pin_milan_era_wipe() {
        printf("\n[5t-g] Milan 5.3.8.10 era wipe (not bound -> bound)\n");

        drive_every_table_5_6_counter_off_zero();
        pin_unbind_keeps_and_bind_zeroes_every_counter();
        pin_pre_bind_interval_flag_dies_with_the_era();
    }

    // ---- build a NON-ZERO value into all ten -------------------------
    // lock (cnt_locked), then 100 ms silence (cnt_unlocked), then re-lock
    void drive_every_table_5_6_counter_off_zero() {
        for (int n = 0; n < 10; n++) {   // clean run -> MEDIA_LOCKED
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        for (int i = 0; i < kSilenceCyc; i++) tick();  // TOUT_CYC_C @ 200 kHz
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
        good_pdu(ts, seq++,                                    // EARLY
                 ts - static_cast<uint64_t>(EARLY_LIMIT_C) - 5000000ULL);
        // a format reject -> UNSUPPORTED_FORMAT
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
    }

    //! The asymmetric clause, both edges: the unbind keeps all ten totals,
    //! the bind that follows zeroes them and drops the lock with them.
    void pin_unbind_keeps_and_bind_zeroes_every_counter() {
        struct { const char* n; long v; } all10[] = {
            {"MEDIA_LOCKED",        static_cast<long>(dut->cnt_locked_o)},
            {"MEDIA_UNLOCKED",      static_cast<long>(dut->cnt_unlocked_o)},
            {"STREAM_INTERRUPTED",  static_cast<long>(dut->cnt_intr_o)},
            {"SEQ_NUM_MISMATCH",    static_cast<long>(dut->seq_err_o)},
            {"MEDIA_RESET",         static_cast<long>(dut->mr_cnt_o)},
            {"TIMESTAMP_UNCERTAIN", static_cast<long>(dut->tu_cnt_o)},
            {"UNSUPPORTED_FORMAT",  static_cast<long>(dut->fmt_err_o)},
            {"LATE_TIMESTAMP",      static_cast<long>(dut->late_cnt_o)},
            {"EARLY_TIMESTAMP",     static_cast<long>(dut->early_cnt_o)},
            {"FRAMES_RX",           static_cast<long>(dut->pdu_count_o)},
        };
        for (auto& c : all10) {
            char b[96];
            snprintf(b, sizeof b, "[5t-g1] pre-unbind %s is NON-ZERO", c.n);
            ck(b, static_cast<long>(c.v > 0), 1);
        }
        // Table 5.6's own invariant on the pair, in its synchronized state
        ck("[5t-g2] bound+locked: MEDIA_LOCKED == MEDIA_UNLOCKED + 1",
           static_cast<long>(dut->cnt_locked_o),
           static_cast<long>(dut->cnt_unlocked_o) + 1);

        // ---- bound -> NOT bound: the clause says do NOT reset ------------
        long keep[10];
        for (int k = 0; k < 10; k++) keep[k] = all10[k].v;
        dut->en_i = 0;
        for (int i = 0; i < 3 * (kIvalCyc + 2); i++) tick();
        long after_unbind[10] = {
            static_cast<long>(dut->cnt_locked_o),
            static_cast<long>(dut->cnt_unlocked_o),
            static_cast<long>(dut->cnt_intr_o),
            static_cast<long>(dut->seq_err_o),
            static_cast<long>(dut->mr_cnt_o),
            static_cast<long>(dut->tu_cnt_o),
            static_cast<long>(dut->fmt_err_o),
            static_cast<long>(dut->late_cnt_o),
            static_cast<long>(dut->early_cnt_o),
            static_cast<long>(dut->pdu_count_o) };
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
            static_cast<long>(dut->cnt_locked_o),
            static_cast<long>(dut->cnt_unlocked_o),
            static_cast<long>(dut->cnt_intr_o),
            static_cast<long>(dut->seq_err_o),
            static_cast<long>(dut->mr_cnt_o),
            static_cast<long>(dut->tu_cnt_o),
            static_cast<long>(dut->fmt_err_o),
            static_cast<long>(dut->late_cnt_o),
            static_cast<long>(dut->early_cnt_o),
            static_cast<long>(dut->pdu_count_o) };
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
           static_cast<long>(dut->cnt_locked_o == 0 &&
                             dut->cnt_unlocked_o == 0), 1);

        // ---- the new era counts from zero, on the same instrument --------
        align_interval();
        for (int n = 0; n < 10; n++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[5t-g7] new era re-locks from zero: MEDIA_LOCKED 1",
           dut->cnt_locked_o, 1);
        ck("[5t-g8] new era counts FRAMES_RX from zero",
           static_cast<long>(dut->pdu_count_o > 0), 1);
    }

    // ---- a seen flag raised before the bind must die with the era ----
    // tu is set on an accepted PDU, then the bind lands BEFORE the
    // interval tick: the flag must not commit +1 into the zeroed counter
    void pin_pre_bind_interval_flag_dies_with_the_era() {
        align_interval();
        g_tu = true;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        g_tu = false;
        ck("[5t-g9] tu flag raised, not yet committed", dut->tu_cnt_o, 0);
        dut->en_i = 0; tick(); tick();
        dut->en_i = 1;
        m.bind_zero();
        for (int i = 0; i < 2 * (kIvalCyc + 2); i++) tick();
        ck("[5t-g10] a pre-bind interval flag cannot commit after the wipe",
           dut->tu_cnt_o, 0);
    }

    //-----------------------------------------------------------------------
    // [dirty] gh #60 F2: the Table 5.22 push-source law. dirty_p_o pulses
    // on lock/unlock events, STREAM_INTERRUPTED events, the SIX anomaly
    // interval commits and the bind-rise wipe - NEVER on a healthy
    // FRAMES_RX interval (the task-21 exclusion: a healthy stream closes
    // an interval every second forever and must not push forever).
    //-----------------------------------------------------------------------
    void pin_dirty_push_source_law() {
        printf("\n[dirty] gh #60 F2 push-source law\n");

        // (a) the lock event pulses once; the healthy intervals after stay
        // silent even as FRAMES_RX keeps committing
        align_interval();
        g_dirty_cnt = 0;
        for (int n = 0; n < 8; n++) {                 // clean run -> lock
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        ck("[dirty-a1] the lock event pulses dirty once", g_dirty_cnt, 1);
        g_dirty_cnt = 0;
        for (int n = 0; n < 6; n++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        for (int i = 0; i < 2 * (kIvalCyc + 2); i++) tick();
        ck("[dirty-a2] healthy FRAMES_RX intervals NEVER pulse",
           g_dirty_cnt, 0);

        // (b) an anomaly interval commit pulses - at the COMMIT, not the PDU
        align_interval();
        g_dirty_cnt = 0;
        g_tu = true;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        g_tu = false;
        ck("[dirty-b1] no pulse before the interval commit", g_dirty_cnt, 0);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[dirty-b2] the TU interval commit pulses dirty", g_dirty_cnt, 1);

        // (c) STREAM_INTERRUPTED is per-event: its pulse lands with the PDU,
        // and the gap's SEQ_NUM_MISMATCH commit pulses again at the tick
        align_interval();
        g_dirty_cnt = 0;
        ts += 2000200; ptp += 2000000; seq += 4;      // >= 2 lost
        good_pdu(ts, seq++, ptp);
        ck("[dirty-c1] the SI event pulses immediately", g_dirty_cnt, 1);
        g_dirty_cnt = 0;
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[dirty-c2] its SM interval commit pulses too", g_dirty_cnt, 1);

        // (d) the 100 ms silence unlock pulses
        g_dirty_cnt = 0;
        for (int i = 0; i < kSilenceCyc; i++) tick();  // TOUT_CYC_C @ 200 kHz
        m.timeout();
        ck("[dirty-d1] the silence unlock pulses dirty", g_dirty_cnt, 1);

        // (e) the bind-rise wipe pulses (the zeroed slate is itself a
        // wire-visible change)
        g_dirty_cnt = 0;
        dut->en_i = 0; for (int i = 0; i < 4; i++) tick();
        dut->en_i = 1; m.bind_zero();
        for (int i = 0; i < 4; i++) tick();
        ck("[dirty-e1] the bind-rise wipe pulses dirty", g_dirty_cnt, 1);
    }

    //-----------------------------------------------------------------------
    // [H2a] gh #62: mr_toggle_p_o, the IEEE 1722-2016 10.4.3 restart ECHO.
    //
    // 10.4.3 gives the received mr bit TWO duties. One is Milan Table 5.6
    // MEDIA_RESET, pinned in [5t-b] above. The other is a shall on the
    // Listener: "Toggle the mr bit in any outgoing media streams that are
    // deriving timestamps from the CRF stream" - PICS Table F.16 CRF-4, and
    // a counter cannot serve it (the observation-interval fold collapses N
    // toggles into one increment and delays it by up to a second, and a
    // counter value is a total, not an edge). This port is that edge.
    //
    // What must NOT produce one is the whole point. The seeding rules that
    // keep MEDIA_RESET honest are the same rules that keep this pulse
    // honest, and each is checked here as an independent law:
    //   * the era's FIRST accepted PDU seeds the reference silently - a new
    //     talker's arbitrary starting level is not this stream's restart
    //   * a REJECTED PDU is never accepted, so a malformed frame carrying a
    //     flipped bit cannot restart anybody's media clock
    //   * a 100 ms silence re-seeds, so a resuming stream's first PDU is
    //     silent too
    // A phantom here is not a cosmetic defect: it restarts the media clock
    // of every listener bound to this device's outgoing streams.
    //-----------------------------------------------------------------------
    void pin_restart_echo() {
        printf("\n[H2a] mr_toggle_p_o: the 10.4.3 restart echo (gh #62)\n");

        pin_restart_echo_seeds_then_reports_real_toggles();
        pin_restart_echo_ignores_rejects_and_reseeds_on_silence();
        pin_restart_echo_survives_rebind_and_foreign_frames();
    }

    //! (a) the era's first PDU seeds, (b) an accepted toggle is one pulse.
    void pin_restart_echo_seeds_then_reports_real_toggles() {
        // clean slate: rebind, then settle the era with a few accepted PDUs
        dut->en_i = 0; for (int i = 0; i < 4; i++) tick();
        dut->en_i = 1; m.bind_zero();
        for (int i = 0; i < 4; i++) tick();

        // (a) the era's FIRST accepted PDU seeds - and it deliberately
        // carries the OPPOSITE level to the one the previous era ended on,
        // which is exactly the shape a phantom would take
        g_mrtog_cnt = 0; g_mrtog_wide = 0;
        g_mr = !g_mr;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        ck("[H2a-a1] era-first PDU SEEDS, never pulses", g_mrtog_cnt, 0);
        for (int n = 0; n < 4; n++) {          // held level: still nothing
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        ck("[H2a-a2] a HELD mr level never pulses", g_mrtog_cnt, 0);

        // (b) an accepted TOGGLE pulses exactly once, one cycle wide, and
        // the >= 8 PDUs 10.4.3 makes the talker hold it for add nothing
        g_mrtog_cnt = 0; g_mrtog_wide = 0;
        g_mr = !g_mr;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        ck("[H2a-b1] an accepted toggle pulses ONCE", g_mrtog_cnt, 1);
        ck("[H2a-b2] ... and the pulse is one cycle wide", g_mrtog_wide, 0);
        for (int n = 0; n < 8; n++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        ck("[H2a-b3] the 8-PDU hold that follows adds nothing",
           g_mrtog_cnt, 1);
        // ... and back again: the OTHER direction is equally a toggle
        g_mrtog_cnt = 0;
        g_mr = !g_mr;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        ck("[H2a-b4] the return toggle pulses once too", g_mrtog_cnt, 1);
    }

    //! (c) a format-rejected flip never pulses, (d) the 100 ms silence
    //! re-seeds - and the re-seeded era still reports a real toggle.
    void pin_restart_echo_ignores_rejects_and_reseeds_on_silence() {
        // (c) a REJECTED PDU carrying a flipped bit never pulses. Same
        // profile violation [5t-b5] uses (timestamp_interval 160): the
        // accept gate is upstream of every verdict this engine forms.
        g_mrtog_cnt = 0;
        {
            bool flipped = !g_mr;
            drive_fields(ts, seq);
            dut->mr_i = flipped;                    // would be a toggle
            dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);
            g_ev_uf = true;
            pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
            m.bad_pdu();
            ck("[H2a-c1] a format-rejected flip NEVER pulses", g_mrtog_cnt, 0);
            // and the level it carried left no trace: the next ACCEPTED PDU
            // at the era's real level is still a no-op
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
            ck("[H2a-c2] ... and did not move the reference either",
               g_mrtog_cnt, 0);
        }

        // (d) the 100 ms silence re-seed. The level that goes silent belongs
        // to the stream that died; a resuming (or brand new) talker's first
        // PDU must seed, not restart. Resume on the OPPOSITE level so a
        // missing re-seed shows up as a pulse.
        g_mrtog_cnt = 0;
        for (int i = 0; i < kSilenceCyc; i++) tick();  // TOUT_CYC_C @ 200 kHz
        m.timeout();
        ck("[H2a-d1] the silence itself pulses nothing", g_mrtog_cnt, 0);
        g_mr = !g_mr;
        ts += 100000000; ptp += 100000000;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        ck("[H2a-d2] the resuming PDU re-seeds, it does not restart",
           g_mrtog_cnt, 0);
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        ck("[H2a-d3] ... and the one after it is quiet as well",
           g_mrtog_cnt, 0);
        // the re-seeded era still DETECTS a real toggle
        g_mr = !g_mr;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        ck("[H2a-d4] the re-seeded era still reports a real toggle",
           g_mrtog_cnt, 1);
    }

    //! (e) the bind edge re-seeds too, (f) a foreign stream's flip is not
    //! this sink's restart - and the next section is handed a clean slate.
    void pin_restart_echo_survives_rebind_and_foreign_frames() {
        // (e) the BIND edge re-seeds the same way, and its wipe is not a
        // restart: a Controller rebinding this sink to a different talker
        // must not restart the media clock of every stream we emit
        g_mrtog_cnt = 0;
        dut->en_i = 0; for (int i = 0; i < 4; i++) tick();
        dut->en_i = 1; m.bind_zero();
        for (int i = 0; i < 4; i++) tick();
        ck("[H2a-e1] the bind edge itself pulses nothing", g_mrtog_cnt, 0);
        g_mr = !g_mr;                                // new talker, new level
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        ck("[H2a-e2] the new era's first PDU seeds silently", g_mrtog_cnt, 0);

        // (f) a foreign frame (wrong stream_id) carrying the opposite level
        // is not this sink's stream at all - 10.4.3 scopes the bit to "the
        // stream being used by the Listener for recovering the media clock"
        g_mrtog_cnt = 0;
        {
            bool save_sid_flip = true;
            (void)save_sid_flip;
            drive_fields(ts, seq);
            dut->sid_frame_i = SID_C ^ 1;
            dut->mr_i = !g_mr;
            pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
            dut->sid_frame_i = SID_C;
            ck("[H2a-f1] a FOREIGN stream's mr flip never pulses",
               g_mrtog_cnt, 0);
        }

        // hand the next section a CLEAN slate: this one closes on accepted
        // PDUs, so an observation interval is still open with its FRAMES_RX
        // flag raised, and [G1] below preloads counter flops and counts the
        // commits that follow exactly. The bind-rise wipe clears the flags
        // on both sides (the same edge [dirty-e1] used to leave behind).
        dut->en_i = 0; for (int i = 0; i < 4; i++) tick();
        dut->en_i = 1; m.bind_zero();
        for (int i = 0; i < 4; i++) tick();
    }

    //-----------------------------------------------------------------------
    // [G1] gh #61: 32-bit wrapping backing behind the byte-identical
    // CRF_STATUS 0x74C slices. Preload the counter flops near their OLD
    // wrap/peg points (--public-flat-rw keeps every signal writable), walk
    // them across, and read the truth on both faces: the full-width value
    // (what the AECP wire serves) and the documented truncated slice (what
    // 0x74C packs - {pdu[15:0], fmt[7:0], seq[7:0]}).
    //-----------------------------------------------------------------------
    void pin_wrap_backing_and_slice_abi() {
        printf("\n[G1] 32-bit wrap backing + 0x74C truncated-slice ABI\n");

        // FRAMES_RX at 65534: a 16-bit backing wraps to 0 at 65536; the
        // 32-bit law reads 0x00010000 while the 0x74C slice truncates to 0.
        // The preload writes the FLOP (the rootp name --public-flat-rw
        // exposes) - the dut-> port member is a copy refreshed FROM it.
        dut->rootp->KL_crf_rx__DOT__pdu_count_o = 65534; m.pdu = 65534;
        tick();
        ck("[G1-a0] preload holds through a quiet cycle",
           dut->pdu_count_o, 65534);
        align_interval();
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        align_interval();
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[G1-a1] FRAMES_RX backing reads 65536 (0x00010000 on the wire)",
           dut->pdu_count_o, 65536);
        ck("[G1-a2] the 0x74C pdu[15:0] slice truncates to 0 (documented)",
           static_cast<long>(static_cast<uint16_t>(dut->pdu_count_o)), 0);

        // UNSUPPORTED_FORMAT at 254: the old 8-bit backing PEGGED at 255
        // (a frozen instrument after 4 min 15 s of persistent fault); the
        // 32-bit law passes straight through
        dut->rootp->KL_crf_rx__DOT__fmt_err_o = 254; m.fmt_e = 254;
        align_interval();
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);  // bad ival
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[G1-b1] 254 + 1 = 255 (still counting)", dut->fmt_err_o, 255);
        align_interval();
        drive_fields(ts, seq);
        dut->fsh_i = (8ULL << 48) | (160ULL << 32) | (ts >> 32);
        g_ev_uf = true;
        pulse(); for (int i = 0; i < SETTLE_TICKS_C; i++) tick();
        m.bad_pdu();
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ck("[G1-b2] UNSUPPORTED_FORMAT passes 255 - peg dropped (256)",
           dut->fmt_err_o, 256);
        ck("[G1-b3] the 0x74C fmt[7:0] slice truncates to 0 (documented)",
           static_cast<long>(static_cast<uint8_t>(dut->fmt_err_o)), 0);
    }

    //-----------------------------------------------------------------------
    // [STOP] Milan v1.2 5.3.8.7 + 5.3.8.10 (issue #97): a stopped, bound
    // sink OBSERVES - matches, validates and counts every Table 5.6 event,
    // with the per-PDU replica compare pinning all thirteen outputs - and
    // CONSUMES nothing: no settle/lock progress, no 10.4.3 restart echo,
    // and the lock machinery times out exactly as if the wire were silent.
    // Mutation anchor: re-gate frame_p_i on the stopped state (the pre-#97
    // wiring) and every stopped-counter compare below goes red.
    //-----------------------------------------------------------------------
    void pin_stopped_sink() {
        printf("\n[STOP] stopped sink: observation ungated, consumption gated\n");

        // precondition: a started, locked sink on a clean cadence
        for (int i = 0; i < 10; i++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        ck("[ST-a0] precondition: locked while started", dut->locked_o, 1);

        // (a) STOP. Accepted PDUs keep counting - the compare inside each
        // good_pdu pins counters, delta and rate against the replica - and
        // the lock HOLDS until the ordinary timeout, because nothing here
        // has silenced the consumption clock yet for 100 ms.
        dut->stop_i = 1; m.stop = true;
        for (int i = 0; i < 4; i++) tick();
        for (int i = 0; i < 6; i++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        ck("[ST-a1] the lock holds before the timeout expires",
           dut->locked_o, 1);

        // (b) a toggle while stopped: counted (MEDIA_RESET), never echoed
        g_mrtog_cnt = 0;
        g_mr = !g_mr;
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        ck("[ST-b1] the stopped toggle never reaches mr_toggle_p_o",
           g_mrtog_cnt, 0);
        for (int i = 0; i < kIvalCyc + 2; i++) tick();
        ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);

        // (c) the lock falls at the ordinary 100 ms timeout even though
        // matching frames keep arriving and keep being counted the whole
        // way through (11 bursts x ~2100 cycles > TOUT_CYC_C)
        for (int burst = 0; burst < 11; burst++) {
            ts += 2000200; ptp += 2000000;
            feed_good(ts, seq++, ptp);
            for (int i = 0; i < 2100; i++) tick();
        }
        m.timeout();              // stop=true: observation state survives
        ck("[ST-c1] the lock timed out under live, observed traffic",
           dut->locked_o, 0);
        ck("[ST-c2] ...scored as one ordinary unlock",
           dut->cnt_unlocked_o, m.cnt_u);
        ck("[ST-c3] no phantom STREAM_INTERRUPTED: the cursor survived",
           dut->cnt_intr_o, m.cnt_i);

        // (d) START again: consumption resumes, the settle run re-earns
        // the lock, and every counter CONTINUES - stop/start is not a bind
        // edge and resets nothing (Table 5.6's reset is bound-edge only)
        dut->stop_i = 0; m.stop = false;
        for (int i = 0; i < 4; i++) tick();
        ck("[ST-d0] restart is not a bind edge: FRAMES_RX kept its value",
           dut->pdu_count_o, static_cast<long long>(m.pdu));
        for (int i = 0; i < 9; i++) {
            ts += 2000200; ptp += 2000000; good_pdu(ts, seq++, ptp);
        }
        ck("[ST-d1] the started sink re-earns the lock through settle",
           dut->locked_o, 1);
        ck("[ST-d2] relock scored one MEDIA_LOCKED event",
           dut->cnt_locked_o, m.cnt_l);
        ck("[ST-d3] no phantom restart echo on START: the mr reference "
           "survived the stopped era", g_mrtog_cnt, 0);
    }
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    CrfRxHarness harness;
    return harness.run();
}
