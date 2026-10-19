// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Lockstep leg (#640 M6): KL_avtp_rx_monitor_ctx against the pre-change
// reference KL_avtp_rx_monitor_ctx_ref (reference/, the module of dev
// e8454e27 with its name changed and #762's silence interruption applied in
// the same lines as the engine), both fed the SAME inputs every cycle by
// avtp_rxmon_lockstep_wrap.
//
//   [LS] unchanged outputs match in every cycle: accept verdicts, legacy
//        counters, LCTX answers, lock and channel levels. Every historical
//        dirty pulse remains present; #726 adds healthy update pulses,
//        graded independently by DV and the parent notification fixture.
//   [GC] GET_COUNTERS: in every cycle, one sink and column of the shipping
//        module's indexed read equals that column of the reference's
//        twelve-counter row (the old interface), for every sink.
//        Each sink's counters are also seeded with a value naming the sink
//        and column through the LCTX window and read back by value.
//   [H1] same-stream back-to-back updates: bursts of PDUs on one stream at
//        every spacing from 1 to 12 cycles, each one a sequence gap that
//        increments STREAM_INTERRUPTED, so consecutive PDU walks
//        read-modify-write the same counter; STREAM_INTERRUPTED moves by
//        exactly the bursts' accepted gaps.
//   [H2] an update colliding with a read: the GET_COUNTERS read of the
//        counter being updated is held across the update, so one read lands
//        in the write cycle itself. The counter is seeded at 0x0000FFFF, so
//        the update changes both 16-bit halves; the read moves exactly once,
//        from the old value to the new, never through a torn mixture, and
//        matches the reference in every cycle.
//   [H3] wrap: counters seeded near 2^32 through the LCTX window wrap to
//        the exact low values, FRAMES_RX adds its interval frame total
//        across the wrap, and the depacketizer word's two 16-bit tallies
//        wrap separately.
//   [H4] reset during update: a reset at every offset into a PDU burst; no
//        bundle queued before the reset is served after it.
//   [SO] a seeded random soak over every input, with resets, binds, window
//        traffic and out-of-range indexes, compared as [LS] and [GC].
//   [SI] #762, STREAM_INTERRUPTED's causes (Milan v1.2 Table 5.6), each
//        graded by count, not against the reference: a 100 ms silence that
//        unlocks a bound, started stream counts once and the resume after it
//        adds nothing; a sequence gap of two lost PDUs counts once; an unbind
//        of a locked stream unlocks without counting, and so does the silence
//        after it. A stopped stream's silence unlocks it and counts nothing
//        (5.3.8.7, the #762 ruling); STOP with live traffic counts nothing;
//        after START a silence counts again.
//        The boundary sweep lands an unbind, or a STOP, at every cycle from
//        12 before to 24 after the edge the 100 ms watchdog expires on, plus
//        far points, on an idle engine and on one paused or yielding to PDU
//        traffic. The expected count is the harness's own: it owns the reset,
//        so it knows the 1 ms grid (CLK_FREQ_HZ_P / 1000 cycles from reset
//        release), and it sees the stream's last accept on pdu_accept_p_o, so
//        the expiry is the 100th grid tick after it. After that edge the
//        silence counts exactly once; on or before it, never.
//
// Scaled clock: CLK_FREQ_HZ_P=10000 makes 1 ms 10 cycles and the 100 ms
// silence unlock 1000 cycles; the Table 5.6 interval is IVAL_CYC_P=500.
#include "Vavtp_rxmon_lockstep_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

#ifndef N_TB
#define N_TB 1
#endif

namespace {

constexpr int kN = N_TB;
constexpr int kIval = 500;
constexpr int kUnlockCycles = 1000;
//! the 1 ms grid, CLK_FREQ_HZ_P / 1000, and the 100 ms silence in its ticks
constexpr int64_t kMsCycles = 10;
constexpr int64_t kUnlockTicks = 100;
//! AAF 48 kHz / INT32 / depth 32 / 8 channels (the NxN harness's format)
constexpr uint64_t kFmt = 0x0205022002006000ULL;
constexpr uint64_t kSid0 = 0x020000FFFE010000ULL;
//! LCTX words and the monitor's counter columns
constexpr int kWFmtLo = 2;
constexpr int kWFmtHi = 3;
constexpr int kWDepkt = 11;
constexpr int kWCnt0 = 16;
constexpr int kColMl = 0;
constexpr int kColMu = 1;
constexpr int kColSi = 2;
constexpr int kColFrx = 9;
constexpr int kCols = 12;
constexpr int kLctxTimeout = 256;

//! a deterministic generator (xorshift64), so a failure replays exactly
struct Rng {
    uint64_t s;
    explicit Rng(uint64_t seed) : s(seed ? seed : 1) {}
    uint64_t next() {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        return s;
    }
    uint32_t below(uint32_t n) { return static_cast<uint32_t>(next() % n); }
    bool chance(uint32_t one_in) { return below(one_in) == 0; }
};

//! the AAF format-specific header a conformant PDU carries for kFmt
uint64_t fsh_for(uint8_t chans) {
    return (0x02ULL << 56) | (0x5ULL << 52) | (static_cast<uint64_t>(chans) << 40) |
           (0x20ULL << 32);
}

class Lockstep {
 public:
    explicit Lockstep(milan::tb::Checker& c) : c_(c) {}

    void run();

 private:
    milan::tb::Checker& c_;
    milan::tb::Model<Vavtp_rxmon_lockstep_wrap> dut_;
    uint64_t cycle_ = 0;
    uint32_t now_ = 1000000;
    uint8_t seq_[kN] = {};
    uint32_t bound_ = 0;
    uint32_t stopped_ = 0;
    //! the [SI] oracle's inputs: the last edge reset was sampled low, and
    //! each stream's last accept edge, both seen from outside the modules
    int64_t reset_edge_ = 0;
    int64_t last_accept_[kN] = {};
    //! the longest expiry-to-unlock latency the idle boundary sweeps saw
    int64_t idle_latency_ = 0;
    //! [LS]/[GC] mismatch tallies, reported once each per phase
    uint64_t ls_bad_ = 0;
    uint64_t gc_bad_ = 0;
    uint64_t gc_reads_ = 0;
    std::string first_bad_;

    void eval_comb() { dut_->eval(); }
    void step();
    void compare_outputs();
    bool compare_read(int sink, int col);
    uint32_t gc_read(int sink, int col);
    void idle_inputs();
    void pdu(int s, uint8_t seq, bool tv = true, uint8_t chans = 8);
    void cycles(int n) {
        for (int i = 0; i < n; i++) step();
    }
    void reset(int len);
    void bind(int s, bool up);
    void stop(int s, bool stopped);
    int64_t silence_expiry_edge(int s) const;
    bool lctx_write(int s, int word, uint32_t data);
    bool lctx_read(int s, int word, uint32_t& data);
    void lock_and_settle(int s);
    void report_lockstep(const char* phase);

    void gc_signatures();
    void h1_back_to_back();
    void h2_update_colliding_with_read();
    void h3_wrap();
    void h4_reset_during_update();
    void si_causes();
    void si_stop_rule();
    //! one boundary trial's outcome (boundary_trial)
    struct BoundaryTrial {
        uint32_t mu = 0;
        uint32_t si = 0;
        bool late_moved = false;
        int64_t e = 0;
        int64_t ev = 0;
        int64_t mu_edge = -1;
        int64_t si_edge = -1;
        bool yielded = false;
    };
    BoundaryTrial boundary_trial(int d, int gap, bool by_stop, bool busy);
    void si_boundary(bool by_stop, bool busy);
    void soak(uint64_t seed, int n);
};

void Lockstep::idle_inputs() {
    dut_->match_valid_i = 0;
    dut_->bind_rise_i = 0;
    dut_->bind_fall_i = 0;
    dut_->depkt_pdu_p_i = 0;
    dut_->depkt_drop_p_i = 0;
}

void Lockstep::step() {
    dut_->clk_i = 0;
    dut_->eval();
    dut_->clk_i = 1;
    dut_->eval();
    ++cycle_;
    if (dut_->dut_pdu_accept_p_o && dut_->dut_pdu_accept_idx_o < kN)
        last_accept_[dut_->dut_pdu_accept_idx_o] = static_cast<int64_t>(cycle_);
    now_ += 20;
    dut_->ptp_now_i = now_;
    idle_inputs();
    dut_->eval();
    compare_outputs();
}

void Lockstep::compare_outputs() {
    auto bad = [this](const char* what) {
        if (ls_bad_++ == 0) first_bad_ = std::string(what) + " at cycle " + std::to_string(cycle_);
    };
    if (dut_->ref_lctx_wr_rdy_o != dut_->dut_lctx_wr_rdy_o) bad("lctx_wr_rdy_o");
    if (dut_->ref_lctx_rd_valid_o != dut_->dut_lctx_rd_valid_o) bad("lctx_rd_valid_o");
    if (dut_->ref_lctx_rd_data_o != dut_->dut_lctx_rd_data_o) bad("lctx_rd_data_o");
    for (int w = 0; w < 12; w++)
        if (dut_->ref_legacy_o[w] != dut_->dut_legacy_o[w]) bad("legacy counter");
    if (dut_->ref_media_locked_o != dut_->dut_media_locked_o) bad("media_locked_o");
    // #726 adds healthy counter events to the historical notification law.
    // Every historical pulse must survive; DV and the wire cadence check
    // independently require the added healthy pulses.
    if ((dut_->ref_dirty_p_o & dut_->dut_dirty_p_o) != dut_->ref_dirty_p_o)
        bad("dirty_p_o lost historical event");
    if (dut_->ref_pdu_accept_p_o != dut_->dut_pdu_accept_p_o) bad("pdu_accept_p_o");
    if (dut_->ref_pdu_accept_idx_o != dut_->dut_pdu_accept_idx_o) bad("pdu_accept_idx_o");
    if (dut_->ref_wire_chans_o != dut_->dut_wire_chans_o) bad("wire_chans_o");
    if (dut_->ref_wire_chans_all_o != dut_->dut_wire_chans_all_o) bad("wire_chans_all_o");
    if (dut_->ref_last_ts_o != dut_->dut_last_ts_o) bad("last_ts_o");
    if (dut_->ref_last_tsd_o != dut_->dut_last_tsd_o) bad("last_tsd_o");
    //! one GET_COUNTERS read per cycle, walking every sink (and an
    //! out-of-range index) and every column
    const int sink = static_cast<int>(cycle_ % (kN + 1)) == kN ? 15 : static_cast<int>(cycle_ % (kN + 1));
    compare_read(sink, static_cast<int>((cycle_ / (kN + 1)) % kCols));
}

//! one indexed read, compared against the reference's row; true when equal
bool Lockstep::compare_read(int sink, int col) {
    dut_->diag_idx_i = static_cast<uint8_t>(sink);
    dut_->diag_col_i = static_cast<uint8_t>(col);
    dut_->eval();
    ++gc_reads_;
    const bool ok = dut_->dut_diag_q_o == dut_->ref_diag_cnt_o[col];
    if (!ok && gc_bad_++ == 0 && first_bad_.empty())
        first_bad_ = "GET_COUNTERS sink " + std::to_string(sink) + " column " +
                     std::to_string(col) + " at cycle " + std::to_string(cycle_);
    return ok;
}

uint32_t Lockstep::gc_read(int sink, int col) {
    compare_read(sink, col);
    return dut_->dut_diag_q_o;
}

void Lockstep::report_lockstep(const char* phase) {
    std::string a = std::string("[LS] ") + phase + ": unchanged outputs match and historical dirty pulses remain";
    std::string b = std::string("[GC] ") + phase + ": every GET_COUNTERS read identical to the reference";
    if (ls_bad_ != 0 || gc_bad_ != 0) std::printf("  first divergence: %s\n", first_bad_.c_str());
    c_.dec(a.c_str(), ls_bad_, 0);
    c_.dec(b.c_str(), gc_bad_, 0);
    ls_bad_ = gc_bad_ = 0;
    first_bad_.clear();
}

void Lockstep::pdu(int s, uint8_t seq, bool tv, uint8_t chans) {
    dut_->match_valid_i = 1;
    dut_->match_index_i = static_cast<uint8_t>(s);
    dut_->subtype_i = 0x02;
    dut_->seq_num_i = seq;
    dut_->ts_uncertain_i = 0;
    dut_->ts_valid_i = tv ? 1 : 0;
    dut_->media_restart_i = 0;
    dut_->avtp_ts_i = now_ + 500000;
    dut_->fsh_i = fsh_for(chans);
}

void Lockstep::reset(int len) {
    dut_->rst_n = 0;
    cycles(len);
    reset_edge_ = static_cast<int64_t>(cycle_);
    dut_->rst_n = 1;
    bound_ = 0;
    dut_->bound_i = 0;
    stopped_ = 0;
    dut_->stopped_i = 0;
}

void Lockstep::bind(int s, bool up) {
    if (up) {
        bound_ |= 1u << s;
        dut_->bind_rise_i = static_cast<uint8_t>(1u << s);
    } else {
        bound_ &= ~(1u << s);
        dut_->bind_fall_i = static_cast<uint8_t>(1u << s);
    }
    dut_->bound_i = bound_;
}

//! STOP_STREAMING / START_STREAMING: a level, held until changed
void Lockstep::stop(int s, bool stopped) {
    if (stopped)
        stopped_ |= 1u << s;
    else
        stopped_ &= ~(1u << s);
    dut_->stopped_i = stopped_;
}

//! The edge stream s's 100 ms silence watchdog expires on, from what the
//! harness drives and sees: the 1 ms tick is visible to the watchdog on edges
//! reset_edge_ + kMsCycles * m + 1 (m >= 1), the accept edge restarts the
//! count, and the 100th tick after it expires.
int64_t Lockstep::silence_expiry_edge(int s) const {
    int64_t m = (last_accept_[s] - reset_edge_ - 1) / kMsCycles + 1;
    if (m < 1) m = 1;
    return reset_edge_ + kMsCycles * (m + kUnlockTicks - 1) + 1;
}

//! a window write held until the engine grants it
bool Lockstep::lctx_write(int s, int word, uint32_t data) {
    dut_->lctx_wr_en_i = 1;
    dut_->lctx_wr_addr_i = static_cast<uint8_t>((s << 5) | word);
    dut_->lctx_wr_data_i = data;
    for (int i = 0; i < kLctxTimeout; i++) {
        dut_->eval();
        const bool granted = dut_->dut_lctx_wr_rdy_o;
        step();
        if (granted) {
            dut_->lctx_wr_en_i = 0;
            return true;
        }
    }
    dut_->lctx_wr_en_i = 0;
    return false;
}

//! a window read held until valid
bool Lockstep::lctx_read(int s, int word, uint32_t& data) {
    dut_->lctx_rd_en_i = 1;
    dut_->lctx_rd_addr_i = static_cast<uint8_t>((s << 5) | word);
    for (int i = 0; i < kLctxTimeout; i++) {
        step();
        if (dut_->dut_lctx_rd_valid_o) {
            data = dut_->dut_lctx_rd_data_o;
            dut_->lctx_rd_en_i = 0;
            return true;
        }
    }
    dut_->lctx_rd_en_i = 0;
    return false;
}

//! bind stream s and send the lock PDU plus the eight settle PDUs, spaced
//! so every walk finishes; the next in-sequence PDU then counts mismatches
void Lockstep::lock_and_settle(int s) {
    bind(s, true);
    cycles(40);
    for (int k = 0; k < 9; k++) {
        pdu(s, ++seq_[s]);
        cycles(20);
    }
    cycles(20);
}

//! every sink's ten window-writable counters seeded with a value naming the
//! sink and the column, then read back through GET_COUNTERS: a read that
//! answers with another sink's row, or another column, fails here by value
void Lockstep::gc_signatures() {
    std::printf("[GC] per-sink signatures\n");
    bool ok = true;
    for (int s = 0; s < kN; s++)
        for (int col = 0; col < 10; col++)
            ok &= lctx_write(s, kWCnt0 + col, 0xA5000000u | (static_cast<uint32_t>(s) << 8) |
                                                  static_cast<uint32_t>(col));
    c_.that("[GC] the window granted every signature write", ok);
    uint64_t wrong = 0;
    for (int s = 0; s < kN; s++)
        for (int col = 0; col < 10; col++)
            if (gc_read(s, col) != (0xA5000000u | (static_cast<uint32_t>(s) << 8) |
                                    static_cast<uint32_t>(col)))
                wrong++;
    c_.dec("[GC] every sink answers its own row and column (seeded signatures)", wrong, 0);
    report_lockstep("GC");
}

void Lockstep::h1_back_to_back() {
    std::printf("[H1] same-stream back-to-back updates\n");
    const int s = kN - 1;
    lock_and_settle(s);
    const uint32_t si0 = gc_read(s, kColSi);
    //! four pulses per burst: the first is served at once, two queue and the
    //! fourth meets a full queue whenever the spacing is short; every
    //! accepted one skips two sequence numbers (lost = 2), an interrupt
    uint32_t accepted = 0;
    for (int spacing = 1; spacing <= 12; spacing++) {
        for (int k = 0; k < 4; k++) {
            seq_[s] = static_cast<uint8_t>(seq_[s] + 3);
            pdu(s, seq_[s]);
            for (int i = 0; i < spacing; i++) {
                step();
                if (dut_->ref_pdu_accept_p_o) accepted++;
            }
        }
        //! a refused fourth PDU leaves the next burst's first one five
        //! sequence numbers past the last accepted: still a gap (lost >= 2)
        for (int i = 0; i < 80; i++) {
            step();
            if (dut_->ref_pdu_accept_p_o) accepted++;
        }
    }
    const uint32_t si1 = gc_read(s, kColSi);
    c_.that("[H1] the bursts accepted PDUs on consecutive cycles (the case is live)", accepted >= 12 * 3);
    c_.dec("[H1] STREAM_INTERRUPTED moved by exactly one per accepted gap PDU", si1 - si0, accepted);
    report_lockstep("H1");
}

void Lockstep::h2_update_colliding_with_read() {
    std::printf("[H2] an update colliding with a read\n");
    const int s = 0;
    lock_and_settle(s);
    //! seed STREAM_INTERRUPTED one below a carry into its high half, so the
    //! update changes BOTH halves and a torn read would be visible
    c_.that("[H2] the window granted the seed write", lctx_write(s, kWCnt0 + kColSi, 0x0000FFFFu));
    //! hold the read on STREAM_INTERRUPTED across one interrupting PDU: the
    //! read is re-evaluated in every cycle, the write cycle included
    const uint32_t before = gc_read(s, kColSi);
    c_.hex("[H2] the held read starts at the seed", before, 0x0000FFFFu);
    uint32_t moves = 0;
    uint32_t last = before;
    uint64_t window_bad = 0;
    seq_[s] = static_cast<uint8_t>(seq_[s] + 3);
    pdu(s, seq_[s]);
    for (int i = 0; i < 40; i++) {
        dut_->clk_i = 0;
        dut_->eval();
        dut_->clk_i = 1;
        dut_->eval();
        ++cycle_;
        now_ += 20;
        dut_->ptp_now_i = now_;
        idle_inputs();
        //! the read of the very counter the walker is writing, every cycle
        if (!compare_read(s, kColSi)) window_bad++;
        const uint32_t v = dut_->dut_diag_q_o;
        if (v != last) {
            moves++;
            last = v;
        }
        compare_outputs();
    }
    c_.dec("[H2] the held read moved exactly once across the update", moves, 1);
    c_.hex("[H2] ... from the seed to the seed + 1, carry included", last, 0x00010000u);
    c_.dec("[H2] GET_COUNTERS read identical to the reference in every cycle of the update window",
           window_bad, 0);
    report_lockstep("H2");
}

void Lockstep::h3_wrap() {
    std::printf("[H3] wrap\n");
    const int s = 0;
    reset(3);
    cycles(10);
    bind(s, true);
    cycles(40);
    bool ok = true;
    //! seed through the window after the bind's counter wipe has run
    ok &= lctx_write(s, kWCnt0 + kColMl, 0xFFFFFFFFu);
    ok &= lctx_write(s, kWCnt0 + kColMu, 0xFFFFFFFFu);
    ok &= lctx_write(s, kWCnt0 + kColSi, 0xFFFFFFFEu);
    ok &= lctx_write(s, kWCnt0 + kColFrx, 0xFFFFFFFAu);
    ok &= lctx_write(s, kWDepkt, 0xFFFEFFFFu);
    c_.that("[H3] the window granted every seed write", ok);
    //! lock (MEDIA_LOCKED wraps), settle, two interrupts (SI wraps)
    for (int k = 0; k < 9; k++) {
        pdu(s, ++seq_[s]);
        cycles(20);
    }
    for (int k = 0; k < 2; k++) {
        seq_[s] = static_cast<uint8_t>(seq_[s] + 3);
        pdu(s, seq_[s]);
        cycles(20);
    }
    //! read now: the interval wait below outlasts the silence timeout, and
    //! that silence is itself an interruption (#762)
    c_.hex("[H3] STREAM_INTERRUPTED wraps 0xFFFFFFFE -> 0x00000000 after two",
           gc_read(s, kColSi), 0x00000000u);
    //! depacketizer: three PDU pulses (pdus 0xFFFF -> 0x0002) and two drops
    //! (drops 0xFFFE -> 0x0000), each half on its own
    for (int k = 0; k < 3; k++) {
        dut_->depkt_pdu_p_i = 1;
        dut_->depkt_pdu_idx_i = static_cast<uint8_t>(s);
        if (k < 2) {
            dut_->depkt_drop_p_i = 1;
            dut_->depkt_drop_idx_i = static_cast<uint8_t>(s);
        }
        cycles(12);
    }
    //! close two intervals so FRAMES_RX commits its frame total
    cycles(2 * kIval + 50);
    c_.hex("[H3] MEDIA_LOCKED wraps 0xFFFFFFFF -> 0x00000000", gc_read(s, kColMl), 0x00000000u);
    c_.hex("[H3] FRAMES_RX adds eleven packets across 32-bit wrap (0xFFFFFFFA + 11)",
           gc_read(s, kColFrx), 0x00000005u);
    uint32_t w11 = 0;
    c_.that("[H3] the window answered the depacketizer word", lctx_read(s, kWDepkt, w11));
    c_.hex("[H3] the depacketizer word's halves wrap separately ({0xFFFE+2, 0xFFFF+3})", w11,
           0x00000002u);
    //! silence unlock: MEDIA_UNLOCKED wraps
    cycles(kUnlockCycles + 200);
    c_.hex("[H3] MEDIA_UNLOCKED wraps 0xFFFFFFFF -> 0x00000000", gc_read(s, kColMu), 0x00000000u);
    c_.hex("[H3] ...and that silence counts STREAM_INTERRUPTED on from the wrap (#762)",
           gc_read(s, kColSi), 0x00000001u);
    report_lockstep("H3");
}

void Lockstep::h4_reset_during_update() {
    std::printf("[H4] reset during update\n");
    const int s = kN - 1;
    uint64_t stale_served = 0;
    for (int offset = 0; offset < 24; offset++) {
        reset(2);
        cycles(5);
        lock_and_settle(s);
        //! a burst that leaves bundles queued, then a reset `offset` cycles in
        for (int k = 0; k < 3; k++) {
            seq_[s] = static_cast<uint8_t>(seq_[s] + 3);
            pdu(s, seq_[s]);
            if (k < 2) step();
        }
        cycles(offset);
        reset(1 + offset % 3);
        //! nothing arrives after the reset, so nothing may be served
        for (int i = 0; i < 60; i++) {
            step();
            if (dut_->dut_pdu_accept_p_o) stale_served++;
        }
    }
    c_.dec("[H4] no bundle queued before a reset is served after it", stale_served, 0);
    report_lockstep("H4");
}

//! #762: each cause of STREAM_INTERRUPTED moves it by its own count
void Lockstep::si_causes() {
    std::printf("[SI] #762 silence, gap and unbind\n");
    const int s = kN - 1;
    lock_and_settle(s);
    const uint32_t mu0 = gc_read(s, kColMu);
    const uint32_t si0 = gc_read(s, kColSi);
    cycles(kUnlockCycles + 200);
    c_.dec("[SI] a silence unlocks the bound stream once (MEDIA_UNLOCKED)", gc_read(s, kColMu) - mu0, 1);
    c_.dec("[SI] a silence that unlocks a bound stream counts STREAM_INTERRUPTED once",
           gc_read(s, kColSi) - si0, 1);
    //! the talker resumes five sequence numbers on: the first PDU re-seeds
    seq_[s] = static_cast<uint8_t>(seq_[s] + 5);
    for (int k = 0; k < 9; k++) {
        pdu(s, ++seq_[s]);
        cycles(20);
    }
    cycles(20);
    c_.dec("[SI] the resume after the silence adds nothing (its first PDU re-seeds)",
           gc_read(s, kColSi) - si0, 1);
    const uint32_t si1 = gc_read(s, kColSi);
    const uint32_t mu1 = gc_read(s, kColMu);
    seq_[s] = static_cast<uint8_t>(seq_[s] + 3);
    pdu(s, seq_[s]);
    cycles(20);
    c_.dec("[SI] a sequence gap of two lost PDUs counts STREAM_INTERRUPTED once", gc_read(s, kColSi) - si1, 1);
    c_.dec("[SI] ...and unlocks nothing", gc_read(s, kColMu) - mu1, 0);
    const uint32_t si2 = gc_read(s, kColSi);
    bind(s, false);
    cycles(40);
    c_.dec("[SI] an unbind of a locked stream unlocks it once", gc_read(s, kColMu) - mu1, 1);
    c_.dec("[SI] an unbind of a locked stream counts no STREAM_INTERRUPTED", gc_read(s, kColSi) - si2, 0);
    cycles(kUnlockCycles + 200);
    c_.dec("[SI] ...nor does the silence after the unbind", gc_read(s, kColSi) - si2, 0);
    c_.dec("[SI] ...which unlocks nothing more", gc_read(s, kColMu) - mu1, 1);
    report_lockstep("SI");
}

//! #762 ruling: a stopped input has no playback, so its silence interrupts
//! nothing (Milan v1.2 5.3.8.7 and Table 5.6). Each case is graded by count:
//! stopped silence after an established lock, START recovery, STOP with live
//! traffic, and the unbind of a stopped, locked input.
void Lockstep::si_stop_rule() {
    std::printf("[SI] #762 stopped and started inputs\n");
    const int s = kN - 1;
    lock_and_settle(s);
    uint32_t ml0 = gc_read(s, kColMl);
    uint32_t mu0 = gc_read(s, kColMu);
    uint32_t si0 = gc_read(s, kColSi);
    stop(s, true);
    cycles(kUnlockCycles + 200);
    c_.dec("[SI] a stopped input's silence unlocks it (MEDIA_UNLOCKED)", gc_read(s, kColMu) - mu0, 1);
    c_.dec("[SI] a stopped input's silence unlocks it but counts no STREAM_INTERRUPTED",
           gc_read(s, kColSi) - si0, 0);
    //! START: the talker resumes five sequence numbers on and the stream
    //! relocks; the first PDU re-seeds, and a later silence counts again
    stop(s, false);
    seq_[s] = static_cast<uint8_t>(seq_[s] + 5);
    for (int k = 0; k < 9; k++) {
        pdu(s, ++seq_[s]);
        cycles(20);
    }
    cycles(20);
    c_.dec("[SI] START: the resumed stream relocks (MEDIA_LOCKED)", gc_read(s, kColMl) - ml0, 1);
    c_.dec("[SI] START: ...and the resume counts no STREAM_INTERRUPTED", gc_read(s, kColSi) - si0, 0);
    cycles(kUnlockCycles + 200);
    c_.dec("[SI] after START a silence counts STREAM_INTERRUPTED again", gc_read(s, kColSi) - si0, 1);
    bind(s, false);
    cycles(40);

    //! STOP with live traffic: the monitor still receives every PDU, so the
    //! stream neither falls silent nor unlocks, for longer than the timeout
    lock_and_settle(s);
    mu0 = gc_read(s, kColMu);
    si0 = gc_read(s, kColSi);
    stop(s, true);
    for (int k = 0; k < 30; k++) {
        pdu(s, ++seq_[s]);
        cycles(50);
    }
    c_.dec("[SI] STOP with live traffic unlocks nothing", gc_read(s, kColMu) - mu0, 0);
    c_.dec("[SI] STOP with live traffic counts no STREAM_INTERRUPTED", gc_read(s, kColSi) - si0, 0);
    stop(s, false);
    pdu(s, ++seq_[s]);
    cycles(20);
    cycles(kUnlockCycles + 200);
    c_.dec("[SI] START after stopped live traffic: the next silence counts once",
           gc_read(s, kColSi) - si0, 1);
    bind(s, false);
    cycles(40);

    lock_and_settle(s);
    mu0 = gc_read(s, kColMu);
    si0 = gc_read(s, kColSi);
    stop(s, true);
    cycles(20);
    bind(s, false);
    cycles(40);
    c_.dec("[SI] an unbind of a stopped, locked input unlocks it once", gc_read(s, kColMu) - mu0, 1);
    c_.dec("[SI] ...and counts no STREAM_INTERRUPTED", gc_read(s, kColSi) - si0, 0);
    stop(s, false);
    report_lockstep("SI stop");
}

//! One #762 boundary trial: a fresh lock, then an unbind or a STOP sampled
//! on edge E + d, where E is the silence's expiry edge (silence_expiry_edge).
//! Busy, a PDU of a second stream (N > 1) or a depacketizer pulse (N = 1)
//! arrives every `gap` cycles until 40 cycles after the event. Returns the
//! counter deltas once the walk is over, whether anything moved in a full
//! timeout after it, and the edges GET_COUNTERS showed the walk's two writes.
Lockstep::BoundaryTrial Lockstep::boundary_trial(int d, int gap, bool by_stop, bool busy) {
    const int s = kN - 1;
    const int b = 0;
    BoundaryTrial r;
    lock_and_settle(s);
    const uint32_t mu0 = gc_read(s, kColMu);
    const uint32_t si0 = gc_read(s, kColSi);
    r.e = silence_expiry_edge(s);
    r.ev = r.e + d;
    const int64_t load_end = r.ev + 40;
    const int64_t end = std::max(r.ev, r.e) + 80;
    while (static_cast<int64_t>(cycle_) < end) {
        const int64_t next = static_cast<int64_t>(cycle_) + 1;
        if (next == r.ev) {
            if (by_stop)
                stop(s, true);
            else
                bind(s, false);
        }
        if (busy && next < load_end && next % gap == 0) {
            if (kN > 1) {
                pdu(b, ++seq_[b]);
            } else {
                dut_->depkt_pdu_p_i = 1;
                dut_->depkt_pdu_idx_i = 0;
            }
        }
        step();
        if (r.mu_edge < 0 && gc_read(s, kColMu) != mu0) r.mu_edge = static_cast<int64_t>(cycle_);
        if (r.si_edge < 0 && gc_read(s, kColSi) != si0) r.si_edge = static_cast<int64_t>(cycle_);
        if (kN > 1 && r.mu_edge >= 0 && r.si_edge < 0 && dut_->dut_pdu_accept_p_o &&
            dut_->dut_pdu_accept_idx_o == b)
            r.yielded = true;
    }
    r.mu = gc_read(s, kColMu) - mu0;
    r.si = gc_read(s, kColSi) - si0;
    cycles(kUnlockCycles + 100);
    r.late_moved = (gc_read(s, kColMu) - mu0 != r.mu) || (gc_read(s, kColSi) - si0 != r.si);
    if (by_stop) stop(s, false);
    bind(s, false);
    cycles(40);
    return r;
}

//! #762's one event boundary. An unbind, or a STOP, is sampled on every edge
//! from 12 before to 24 after the silence's expiry edge E, and at far points.
//! E is the harness's own (silence_expiry_edge), never read from a module.
//! Sampled after E, the silence is already an interruption and counts
//! exactly once; on or before E it never counts; the stream unlocks once
//! either way, and a full timeout later nothing more has moved. Busy, the
//! unlock walk waits for the walker and its STREAM_INTERRUPTED write yields.
void Lockstep::si_boundary(bool by_stop, bool busy) {
    const char* what = by_stop ? "a STOP" : "an unbind";
    std::printf("[SI] boundary: %s across the silence expiry, %s engine\n", what,
                busy ? "busy" : "idle");
    const std::string tag = std::string("[SI] boundary (") + what + (busy ? ", busy)" : ", idle)");
    std::vector<int> offsets = {-200, -40};
    for (int d = -12; d <= 24; d++) offsets.push_back(d);
    offsets.push_back(40);
    offsets.push_back(80);
    uint64_t wrong_mu = 0;
    uint64_t wrong_si = 0;
    uint64_t wrong_late = 0;
    //! where the event was sampled, against the walk's two counter writes:
    //! before the expiry, while the walk was pending, between its writes, after
    uint64_t where[4] = {};
    uint64_t yielded = 0;
    int64_t max_latency = 0;
    if (busy && kN > 1) lock_and_settle(0);
    int trial = 0;
    for (const int d : offsets) {
        const int gap = 3 + 3 * (trial++ % 3);  //! 3, 6 or 9 cycles apart
        const BoundaryTrial r = boundary_trial(d, gap, by_stop, busy);
        const uint32_t want = d > 0 ? 1 : 0;
        if (r.mu != 1 || r.si != want)
            std::printf("  offset %d from the expiry: MEDIA_UNLOCKED +%u, STREAM_INTERRUPTED +%u, "
                        "expected +1 and +%u\n", d, r.mu, r.si, want);
        wrong_mu += r.mu != 1;
        wrong_si += r.si != want;
        wrong_late += r.late_moved;
        int at = 3;
        if (r.ev <= r.e)
            at = 0;
        else if (r.mu_edge < 0 || r.ev <= r.mu_edge)
            at = 1;
        else if (r.si_edge < 0 || r.ev <= r.si_edge)
            at = 2;
        where[at]++;
        //! the silence's own unlock walk: always when stopped, and after E
        //! when the unbind comes later
        if (r.mu_edge >= 0 && (by_stop || d > 0))
            max_latency = std::max(max_latency, r.mu_edge - r.e);
        yielded += r.yielded;
    }
    if (busy && kN > 1) {
        bind(0, false);
        cycles(40);
    }
    std::printf("  sampled before the expiry %llu, while the walk was pending %llu, between its two "
                "writes %llu, after it %llu; longest expiry-to-unlock %lld cycles; "
                "interruption writes that yielded to a PDU walk %llu\n",
                static_cast<unsigned long long>(where[0]), static_cast<unsigned long long>(where[1]),
                static_cast<unsigned long long>(where[2]), static_cast<unsigned long long>(where[3]),
                static_cast<long long>(max_latency), static_cast<unsigned long long>(yielded));
    c_.dec((tag + ": the stream unlocked exactly once at every offset").c_str(), wrong_mu, 0);
    c_.dec((tag + ": after the expiry the silence counts once, on or before it never").c_str(),
           wrong_si, 0);
    c_.dec((tag + ": a full timeout later nothing more has moved").c_str(), wrong_late, 0);
    if (!busy) {
        idle_latency_ = std::max(idle_latency_, max_latency);
        c_.that((tag + ": sampled before the expiry, during the walk, between its two writes and "
                       "after it (the sweep is live)").c_str(),
                where[0] > 0 && where[1] > 0 && where[2] > 0 && where[3] > 0);
    } else {
        c_.that((tag + ": the load held the unlock walk longer than an idle engine does").c_str(),
                max_latency > idle_latency_);
        c_.that((tag + ": sampled before the expiry, while the walk was held, and after it").c_str(),
                where[0] > 0 && where[1] > 0 && where[3] > 0);
        if (kN > 1)
            c_.that((tag + ": some interruption write yielded to a PDU walk").c_str(), yielded > 0);
    }
    report_lockstep(by_stop ? "SI stop boundary" : "SI unbind boundary");
}

void Lockstep::soak(uint64_t seed, int n) {
    std::printf("[SO] random soak, seed %llu, %d cycles\n", static_cast<unsigned long long>(seed), n);
    Rng r(seed);
    reset(3);
    for (int s = 1; s < kN; s++) {
        lctx_write(s, kWFmtLo, static_cast<uint32_t>(kFmt));
        lctx_write(s, kWFmtHi, static_cast<uint32_t>(kFmt >> 32));
    }
    int wr_left = 0;
    int rd_left = 0;
    //! what the soak exercised, so a vacuous run cannot pass
    uint64_t accepts = 0;
    uint64_t dirties = 0;
    uint64_t writes = 0;
    uint64_t reads = 0;
    uint64_t resets = 0;
    uint64_t live_reads = 0;
    for (int i = 0; i < n; i++) {
        if (r.chance(4000)) {
            reset(1 + static_cast<int>(r.below(3)));
            resets++;
            continue;
        }
        if (r.chance(300)) {
            const int s = static_cast<int>(r.below(kN));
            bind(s, !((bound_ >> s) & 1u));
        }
        if (r.chance(9)) {
            const int s = static_cast<int>(r.below(kN + (r.chance(8) ? 2 : 0)));
            if (s < kN) {
                seq_[s] = static_cast<uint8_t>(seq_[s] + (r.chance(10) ? 1 + r.below(4) : 1));
            }
            pdu(s, s < kN ? seq_[s] : 0, !r.chance(20), static_cast<uint8_t>(r.chance(30) ? r.below(16) : 8));
            dut_->ts_uncertain_i = r.chance(25);
            dut_->media_restart_i = r.chance(40);
            if (r.chance(15)) dut_->fsh_i ^= 1ULL << (40 + r.below(24));
            if (r.chance(8)) dut_->avtp_ts_i = now_ - r.below(100000);
            if (r.chance(12)) dut_->avtp_ts_i = now_ + 20000000u + r.below(1000000);
        }
        if (r.chance(7)) {
            dut_->depkt_pdu_p_i = 1;
            dut_->depkt_pdu_idx_i = static_cast<uint8_t>(r.below(kN + 1));
        }
        if (r.chance(40)) {
            dut_->depkt_drop_p_i = 1;
            dut_->depkt_drop_idx_i = static_cast<uint8_t>(r.below(kN + 1));
        }
        if (wr_left == 0 && rd_left == 0 && r.chance(60)) {
            if (r.chance(2)) {
                wr_left = kLctxTimeout;
                dut_->lctx_wr_en_i = 1;
                dut_->lctx_wr_addr_i = static_cast<uint8_t>((r.below(kN) << 5) | (16 + r.below(12)));
                dut_->lctx_wr_data_i = static_cast<uint32_t>(r.next());
            } else {
                rd_left = kLctxTimeout;
                dut_->lctx_rd_en_i = 1;
                dut_->lctx_rd_addr_i = static_cast<uint8_t>((r.below(kN) << 5) | r.below(32));
            }
        }
        if (r.chance(500)) dut_->render_sel_i = static_cast<uint8_t>(r.below(kN));
        dut_->eval();
        const bool granted = dut_->dut_lctx_wr_rdy_o;
        step();
        accepts += dut_->ref_pdu_accept_p_o;
        dirties += dut_->ref_dirty_p_o != 0;
        live_reads += dut_->dut_diag_q_o != 0;
        if (wr_left > 0 && (granted || --wr_left == 0)) {
            writes += granted;
            wr_left = 0;
            dut_->lctx_wr_en_i = 0;
        }
        if (rd_left > 0 && (dut_->dut_lctx_rd_valid_o || --rd_left == 0)) {
            reads += dut_->dut_lctx_rd_valid_o;
            rd_left = 0;
            dut_->lctx_rd_en_i = 0;
        }
    }
    dut_->lctx_wr_en_i = 0;
    dut_->lctx_rd_en_i = 0;
    std::printf("  soak exercised: %llu accepts, %llu dirty cycles, %llu window writes, %llu window "
                "reads, %llu resets, %llu nonzero GET_COUNTERS reads\n",
                static_cast<unsigned long long>(accepts), static_cast<unsigned long long>(dirties),
                static_cast<unsigned long long>(writes), static_cast<unsigned long long>(reads),
                static_cast<unsigned long long>(resets), static_cast<unsigned long long>(live_reads));
    c_.that("[SO] the soak accepted PDUs, raised dirty pulses, used the window and reset (live)",
            accepts > 2000 && dirties > 200 && writes > 500 && reads > 500 && resets > 20 &&
            live_reads > n / 4);
    report_lockstep("SO");
}

void Lockstep::run() {
    dut_->clk_i = 0;
    dut_->sid0_i = kSid0;
    dut_->fmt0_i = kFmt;
    dut_->pres_ofs_i = 2000000;
    dut_->render_sel_i = 0;
    dut_->lctx_wr_en_i = 0;
    dut_->lctx_rd_en_i = 0;
    dut_->ptp_now_i = now_;
    idle_inputs();
    reset(4);
    cycles(10);
    for (int s = 1; s < kN; s++) {
        lctx_write(s, kWFmtLo, static_cast<uint32_t>(kFmt));
        lctx_write(s, kWFmtHi, static_cast<uint32_t>(kFmt >> 32));
    }
    report_lockstep("setup");
    gc_signatures();
    h1_back_to_back();
    h2_update_colliding_with_read();
    h3_wrap();
    h4_reset_during_update();
    si_causes();
    si_stop_rule();
    si_boundary(false, false);
    si_boundary(true, false);
    si_boundary(false, true);
    si_boundary(true, true);
    soak(0x6406u + kN, 300000);
    soak(0x9e3779b97f4a7c15ULL, 300000);
    c_.that("[GC] the reads covered every sink and column many times", gc_reads_ > 600000);
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const std::string label = "avtp_rxmon lockstep N=" + std::to_string(kN);
    milan::tb::Checker c(label.c_str());
    c.echo_passes();
    {
        Lockstep ls(c);
        ls.run();
    }
    return c.report();
}
