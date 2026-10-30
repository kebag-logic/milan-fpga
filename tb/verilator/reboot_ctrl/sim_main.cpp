// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_reboot_ctrl self-checking harness (issue #787): the end-station reset on
// the protocol processor's AECP REBOOT request (IEEE 1722.1-2021 7.4.43).
//
// The module is built at its SHIPPING waits, 10,000 ms of drain and 3,500 ms
// of PHY hold (docs/design/REBOOT_RESET.md), and at a MAC statement the
// Makefile names per leg, from which the module derives its egress bound.
// Only the millisecond is compressed: this harness drives ms_tick_i itself,
// one pulse every kMsCycles clocks, at a phase each scenario chooses, so the
// bounds are graded in ticks against the documented values rather than
// against the RTL's own constants.
//
// The harness is also the datapath and the MAC around the module. As the
// datapath it offers frames at the MAC port and lets a beat through only
// when mac_tx_stop_o allows it, which is the gate milan_datapath applies.
// As the MAC it flips mac_txend_tgl_i when a frame it was given reaches its
// PHY, and raises mac_flush_i for a link-guard episode.
//
// Graded, each by its own labelled checks:
//   U0  idle: no request, no PHY hold, CSIB high and the dummy word, whatever
//       the saved-state status does
//   U1  no live writer (backed 0, even with dirty and pending work), nothing
//       in the MAC: the egress wait starts two clocks after the request, the
//       PHY hold more than one tick and at most two ticks and two clocks
//       after the request, the hold lasts more than 3,500 ms and at most one
//       tick more, then exactly eight clocks of CSIB low carry the IPROG
//       words, bit-reversed per byte; the PHY hold stays up, and the
//       sequence repeats after another hold
//   U2  durable (backed 1, dirty 0, pend 0): the same
//   U3  dirty work with a live writer: no egress wait and no PHY hold while
//       it is dirty, the egress wait on the clock the dirty bit clears
//   U4  the same for pending work
//   U5  a writer that never commits: the drain ends after more than
//       10,000 ms and at most one tick more
//   U6  the writer lost during the drain: the egress wait on that clock
//   U7  a one-clock request still resets: the module latches it
//   U8  status moves after the drain end change nothing
//   U9  reset during the hold: back to idle, no IPROG
//   U10 reset in the middle of the IPROG words: CSIB high at once, no word
//       after it
//   U11 the tick phase: two other phases keep the waits inside their bounds
//   U12 frames in the MAC at the request: no PHY hold until the last one
//       reaches the PHY, then more than one tick and at most two ticks and
//       five clocks later; a frame taken on the clock another one ends is
//       counted
//   U13 a frame in progress at the port when the wait starts, held back in
//       its middle across ticks: no PHY hold while it is taken, the port
//       takes the rest of it, starts no new frame, and the hold waits for it
//   U14 the bound: a MAC that never finishes ends the wait after more than
//       the derived egress bound and at most one tick more, inside the
//       bound stated for a durable state
//   U15 a link-guard flush in the wait: what the MAC held is gone, and the
//       hold follows on the quiet tick, not at the bound
//   U16 an end with nothing counted does not wrap the count: a frame taken
//       after it is still waited for
//   U17 the stated bound from the request to the IPROG word, with a writer
//       that never commits and a MAC that never finishes

#include "VKL_reboot_ctrl.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <array>
#include <cstdint>
#include <cstdio>
#include <string>

#ifndef EGRESS_MS
#error "EGRESS_MS: the egress bound the leg's MAC statement derives, from the Makefile"
#endif

namespace {

//! clocks per harness millisecond
constexpr uint64_t kMsCycles = 8;
//! the documented waits (docs/design/REBOOT_RESET.md), independent literals
constexpr uint64_t kDrainMs = 10000;
constexpr uint64_t kHoldMs = 3500;
//! the egress bound of this leg's MAC statement, an independent literal
constexpr uint64_t kEgressMs = EGRESS_MS;
//! the stated bound beyond its milliseconds (KL_reboot_ctrl's banner)
constexpr uint64_t kBoundClocks = 8;
//! clocks the toggle needs to cross: the module's three-flop synchroniser
constexpr uint64_t kSyncClocks = 3;

//! The 7-series IPROG sequence through ICAPE2, as configuration words: dummy,
//! sync, type-1 NOOP, type-1 write of one word to WBSTAR (register 0b10000),
//! the start address 0, type-1 write of one word to CMD (register 0b00100),
//! the IPROG command (0b01111), type-1 NOOP.
constexpr std::array<uint32_t, 8> kIprogWords = {
    0xFFFFFFFFu, 0xAA995566u, 0x20000000u, 0x30020001u,
    0x00000000u, 0x30008001u, 0x0000000Fu, 0x20000000u};

//! ICAPE2's X32 data bus takes every byte with its bit order reversed
uint32_t bit_reverse_bytes(uint32_t w) {
    uint32_t out = 0;
    for (int b = 0; b < 4; ++b) {
        const uint32_t byte = (w >> (8 * b)) & 0xFFu;
        uint32_t rev = 0;
        for (int i = 0; i < 8; ++i)
            if (byte & (1u << i)) rev |= 1u << (7 - i);
        out |= rev << (8 * b);
    }
    return out;
}

class RebootBench {
 public:
    int execute(bool egress_only);

 private:
    void step();
    void run(uint64_t n) { for (uint64_t i = 0; i < n; ++i) step(); }
    void reset(unsigned phase);
    void status(bool backed, bool dirty, bool pend) {
        dut->nvm_backed_i = backed;
        dut->nvm_dirty_i = dirty;
        dut->nvm_pend_i = pend;
    }
    //! steps until the predicate holds, or limit steps; returns the count
    template <class Pred>
    uint64_t run_until(Pred pred, uint64_t limit) {
        uint64_t n = 0;
        while (n < limit && !pred()) { step(); ++n; }
        return n;
    }
    //! the datapath's gate: offer one beat, which the port takes only when
    //! mac_tx_stop_o allows it; true when it was taken
    bool offer_beat(bool last);
    //! a whole frame of `beats` beats, back to back; true when all were taken
    bool offer_frame(unsigned beats);
    //! the MAC hands a frame's last octet to its PHY, then lets the toggle
    //! settle as frames at least 84 octet times apart would
    void wire_end() {
        dut->mac_txend_tgl_i = !dut->mac_txend_tgl_i;
        run(kSyncClocks + 1);
    }
    //! raises the request and steps until the PHY hold rises, or limit
    //! steps; returns the steps
    uint64_t request_to_hold(uint64_t limit) {
        dut->reboot_req_i = 1;
        step();
        return 1 + run_until([&] { return dut->phy_hold_o == 1; }, limit);
    }
    //! grades the hold after the egress wait found nothing left: more than
    //! one tick and at most two ticks and `extra` clocks after `n`
    void grade_quiet(const std::string& tag, uint64_t n, uint64_t extra);
    //! steps until CSIB falls, then grades one burst of IPROG words; returns
    //! the steps spent before the burst
    uint64_t grade_burst(const std::string& tag, uint64_t limit);
    //! grades the clocks from the request to the IPROG command word, the
    //! seventh of a burst whose CSIB fell `to_burst` clocks after it
    void grade_bound(const std::string& tag, uint64_t to_burst, uint64_t ms);
    std::string label(const std::string& tag, const char* what) const {
        return tag + " " + what;
    }

    void prove_idle_is_inert();
    void prove_reset_without_a_writer();
    void prove_reset_of_a_durable_state();
    void prove_dirty_work_is_waited_for();
    void prove_pending_work_is_waited_for();
    void prove_the_drain_deadline();
    void prove_a_lost_writer_ends_the_drain();
    void prove_a_one_clock_request_is_latched();
    void prove_status_after_the_drain_changes_nothing();
    void prove_reset_during_the_hold();
    void prove_reset_during_the_words();
    void prove_the_tick_phase();
    void prove_frames_in_the_mac_are_waited_for();
    void prove_the_frame_in_progress_finishes();
    void prove_the_egress_bound();
    void prove_a_flush_clears_the_account();
    void prove_a_stray_end_does_not_wrap();
    void prove_the_stated_bound();

    VKL_reboot_ctrl* dut = nullptr;
    milan::tb::Checker ck{"reboot_ctrl"};
    uint64_t cyc = 0;
    unsigned tick_phase = 0;
};

void RebootBench::step() {
    dut->ms_tick_i = (cyc % kMsCycles) == tick_phase;
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    ++cyc;
}

void RebootBench::reset(unsigned phase) {
    tick_phase = phase;
    dut->rst_n = 0;
    dut->reboot_req_i = 0;
    dut->mac_tx_beat_i = 0;
    dut->mac_tx_last_i = 0;
    dut->mac_flush_i = 0;
    status(false, false, false);
    run(4);
    dut->rst_n = 1;
    run(kSyncClocks + 3);
}

bool RebootBench::offer_beat(bool last) {
    dut->clk_i = 0; dut->eval();
    const bool take = dut->mac_tx_stop_o == 0;
    dut->mac_tx_beat_i = take;
    dut->mac_tx_last_i = take && last;
    step();
    dut->mac_tx_beat_i = 0;
    dut->mac_tx_last_i = 0;
    return take;
}

bool RebootBench::offer_frame(unsigned beats) {
    bool all = true;
    for (unsigned b = 0; b < beats; ++b) all = offer_beat(b + 1 == beats) && all;
    return all;
}

void RebootBench::grade_quiet(const std::string& tag, uint64_t n, uint64_t extra) {
    std::printf("  [i] %s %llu clocks, bound (%llu, %llu]\n", tag.c_str(),
                static_cast<unsigned long long>(n),
                static_cast<unsigned long long>(kMsCycles),
                static_cast<unsigned long long>(2 * kMsCycles + extra));
    ck.that(label(tag, "the PHY hold rises more than one tick later").c_str(),
            dut->phy_hold_o == 1 && n > kMsCycles);
    ck.that(label(tag, "...and at most two ticks and the crossing later").c_str(),
            dut->phy_hold_o == 1 && n <= 2 * kMsCycles + extra);
}

uint64_t RebootBench::grade_burst(const std::string& tag, uint64_t limit) {
    const uint64_t before = run_until([&] { return dut->icap_csib_o == 0; }, limit);
    ck.that(label(tag, "CSIB falls for the IPROG words").c_str(), before < limit);
    bool words_ok = true;
    for (size_t k = 0; k < kIprogWords.size(); ++k) {
        if (dut->icap_csib_o != 0 || dut->icap_i_o != bit_reverse_bytes(kIprogWords[k])) {
            words_ok = false;
            std::printf("  [i] %s word %zu: csib %u I 0x%08X, want 0x%08X\n", tag.c_str(), k,
                        static_cast<unsigned>(dut->icap_csib_o),
                        static_cast<unsigned>(dut->icap_i_o),
                        static_cast<unsigned>(bit_reverse_bytes(kIprogWords[k])));
        }
        ck.that(label(tag, "the PHY hold stays up through the IPROG words").c_str(),
                dut->phy_hold_o == 1);
        step();
    }
    ck.that(label(tag, "eight consecutive clocks carry dummy, sync, NOOP, WBSTAR, 0, CMD, IPROG, "
                       "NOOP, bits reversed per byte").c_str(), words_ok);
    ck.dec(label(tag, "CSIB is high again after the eighth word").c_str(), dut->icap_csib_o, 1);
    ck.hex(label(tag, "the bus returns to the dummy word").c_str(), dut->icap_i_o, 0xFFFFFFFFu);
    ck.dec(label(tag, "the PHY hold stays up after the words").c_str(), dut->phy_hold_o, 1);
    return before;
}

void RebootBench::grade_bound(const std::string& tag, uint64_t to_burst, uint64_t ms) {
    const uint64_t to_iprog = to_burst + 6;
    std::printf("  [i] %s request to the IPROG word %llu clocks, bound %llu\n", tag.c_str(),
                static_cast<unsigned long long>(to_iprog),
                static_cast<unsigned long long>(ms * kMsCycles + kBoundClocks));
    ck.that(label(tag, "the IPROG word comes inside the stated bound").c_str(),
            to_iprog <= ms * kMsCycles + kBoundClocks);
}

void RebootBench::prove_idle_is_inert() {
    reset(0);
    bool inert = true;
    for (uint64_t i = 0; i < (kDrainMs + kHoldMs + kEgressMs + 4) * kMsCycles; ++i) {
        status((i >> 5) & 1, (i >> 7) & 1, (i >> 9) & 1);
        if ((i & 63) == 0) dut->mac_txend_tgl_i = !dut->mac_txend_tgl_i;
        dut->mac_flush_i = (i >> 11) & 1;
        step();
        inert = inert && dut->phy_hold_o == 0 && dut->icap_csib_o == 1
                && dut->icap_i_o == 0xFFFFFFFFu && dut->mac_tx_stop_o == 0;
    }
    dut->mac_flush_i = 0;
    ck.that("U0 no request: no PHY hold, no stop, CSIB high and the dummy word for longer than "
            "every wait", inert);
}

void RebootBench::prove_reset_without_a_writer() {
    reset(0);
    status(false, true, true);          // a dead writer's leftover work
    dut->reboot_req_i = 1;
    step();
    ck.dec("U1 no writer: no stop on the clock the request is sampled", dut->mac_tx_stop_o, 0);
    step();
    ck.dec("U1 no writer: the egress wait starts two clocks after the request",
           dut->mac_tx_stop_o, 1);
    ck.dec("U1 no writer: ...with no PHY hold yet", dut->phy_hold_o, 0);
    const uint64_t n = 2 + run_until([&] { return dut->phy_hold_o == 1; }, 4 * kMsCycles);
    grade_quiet("U1 no writer, nothing in the MAC: from the request", n, 2);
    const uint64_t hold = grade_burst("U1", (kHoldMs + 4) * kMsCycles);
    std::printf("  [i] U1 hold %llu clocks, bound (%llu, %llu]\n",
                static_cast<unsigned long long>(hold),
                static_cast<unsigned long long>(kHoldMs * kMsCycles),
                static_cast<unsigned long long>((kHoldMs + 1) * kMsCycles));
    ck.that("U1 the hold is longer than 3,500 ms", hold > kHoldMs * kMsCycles);
    ck.that("U1 the hold is at most one tick longer than 3,500 ms",
            hold <= (kHoldMs + 1) * kMsCycles);
    const uint64_t again = grade_burst("U1 retry", (kHoldMs + 4) * kMsCycles);
    ck.that("U1 retry: the IPROG words repeat after another hold of more than 3,500 ms",
            again > kHoldMs * kMsCycles && again <= (kHoldMs + 1) * kMsCycles);
    ck.dec("U1 the stop stays up to the end", dut->mac_tx_stop_o, 1);
}

void RebootBench::prove_reset_of_a_durable_state() {
    reset(3);
    status(true, false, false);
    const uint64_t n = request_to_hold(4 * kMsCycles);
    grade_quiet("U2 durable, nothing in the MAC: from the request", n, 2);
    const uint64_t hold = grade_burst("U2", (kHoldMs + 4) * kMsCycles);
    ck.that("U2 the hold is longer than 3,500 ms and at most one tick more",
            hold > kHoldMs * kMsCycles && hold <= (kHoldMs + 1) * kMsCycles);
    grade_bound("U2 durable:", n + hold, kEgressMs + kHoldMs + 2);
}

void RebootBench::prove_dirty_work_is_waited_for() {
    reset(5);
    status(true, true, false);
    dut->reboot_req_i = 1;
    bool held_off = true;
    for (uint64_t i = 0; i < 4000 * kMsCycles; ++i) {
        step();
        held_off = held_off && dut->phy_hold_o == 0 && dut->icap_csib_o == 1
                   && dut->mac_tx_stop_o == 0;
    }
    ck.that("U3 dirty work with a live writer: no stop, no PHY hold and no IPROG for 4,000 ms",
            held_off);
    status(true, false, false);         // the commit's acknowledgement
    step();
    ck.dec("U3 the egress wait starts on the clock the dirty bit clears", dut->mac_tx_stop_o, 1);
    const uint64_t n = run_until([&] { return dut->phy_hold_o == 1; }, 4 * kMsCycles);
    grade_quiet("U3 nothing in the MAC: from the drain's end", n, 1);
    grade_burst("U3", (kHoldMs + 4) * kMsCycles);
}

void RebootBench::prove_pending_work_is_waited_for() {
    reset(1);
    status(true, false, true);
    dut->reboot_req_i = 1;
    bool held_off = true;
    for (uint64_t i = 0; i < 1500 * kMsCycles; ++i) {
        step();
        held_off = held_off && dut->phy_hold_o == 0 && dut->mac_tx_stop_o == 0;
    }
    ck.that("U4 pending work with a live writer: no stop and no PHY hold for 1,500 ms", held_off);
    status(true, true, false);          // the producer wrote it: now dirty
    run(100 * kMsCycles);
    ck.dec("U4 the work moves from pending to dirty: still no stop", dut->mac_tx_stop_o, 0);
    status(true, false, false);
    step();
    ck.dec("U4 the egress wait starts on the clock the work is durable", dut->mac_tx_stop_o, 1);
}

void RebootBench::prove_the_drain_deadline() {
    reset(7);
    status(true, true, true);           // a live writer that never commits
    dut->reboot_req_i = 1;
    step();                             // the request is sampled
    const uint64_t drain = run_until([&] { return dut->mac_tx_stop_o == 1; },
                                     (kDrainMs + 4) * kMsCycles);
    std::printf("  [i] U5 drain %llu clocks, bound (%llu, %llu]\n",
                static_cast<unsigned long long>(drain),
                static_cast<unsigned long long>(kDrainMs * kMsCycles),
                static_cast<unsigned long long>((kDrainMs + 1) * kMsCycles));
    ck.that("U5 a writer that never commits: the drain ends after more than 10,000 ms",
            drain > kDrainMs * kMsCycles);
    ck.that("U5 ...and at most one tick after 10,000 ms", drain <= (kDrainMs + 1) * kMsCycles);
    const uint64_t n = run_until([&] { return dut->phy_hold_o == 1; }, 4 * kMsCycles);
    grade_quiet("U5 nothing in the MAC: from the drain's end", n, 1);
    const uint64_t hold = grade_burst("U5", (kHoldMs + 4) * kMsCycles);
    ck.that("U5 the hold after a deadline is still longer than 3,500 ms",
            hold > kHoldMs * kMsCycles && hold <= (kHoldMs + 1) * kMsCycles);
}

void RebootBench::prove_a_lost_writer_ends_the_drain() {
    reset(2);
    status(true, true, false);
    dut->reboot_req_i = 1;
    run(2000 * kMsCycles);
    ck.dec("U6 dirty work, live writer: no stop after 2,000 ms", dut->mac_tx_stop_o, 0);
    status(false, true, false);         // T-NVM-WRITER-ALIVE expired: backed falls
    step();
    ck.dec("U6 the writer is lost: the egress wait starts on that clock", dut->mac_tx_stop_o, 1);
}

void RebootBench::prove_a_one_clock_request_is_latched() {
    reset(4);
    status(false, false, false);
    dut->reboot_req_i = 1;
    step();
    dut->reboot_req_i = 0;
    run_until([&] { return dut->phy_hold_o == 1; }, 4 * kMsCycles);
    ck.dec("U7 a one-clock request: the PHY hold still rises", dut->phy_hold_o, 1);
    grade_burst("U7", (kHoldMs + 4) * kMsCycles);
}

void RebootBench::prove_status_after_the_drain_changes_nothing() {
    reset(6);
    status(true, false, false);
    request_to_hold(4 * kMsCycles);
    bool steady = true;
    uint64_t n = 0;
    while (n < (kHoldMs + 4) * kMsCycles && dut->icap_csib_o == 1) {
        status(n & 1, (n >> 1) & 1, (n >> 2) & 1);
        step();
        ++n;
        steady = steady && dut->phy_hold_o == 1;
    }
    ck.that("U8 status moves during the hold: the PHY hold stays up", steady);
    ck.that("U8 ...and the IPROG words still start after more than 3,500 ms",
            n > kHoldMs * kMsCycles && n <= (kHoldMs + 1) * kMsCycles);
}

void RebootBench::prove_reset_during_the_hold() {
    reset(0);
    request_to_hold(4 * kMsCycles);
    run(1000 * kMsCycles);
    ck.dec("U9 the PHY hold is up 1,000 ms into the hold", dut->phy_hold_o, 1);
    dut->rst_n = 0;
    step();
    dut->reboot_req_i = 0;
    dut->rst_n = 1;
    bool idle = dut->phy_hold_o == 0 && dut->mac_tx_stop_o == 0;
    for (uint64_t i = 0; i < (kHoldMs + 4) * kMsCycles; ++i) {
        step();
        idle = idle && dut->phy_hold_o == 0 && dut->icap_csib_o == 1 && dut->mac_tx_stop_o == 0;
    }
    ck.that("U9 a reset during the hold: back to idle, the port open, and no IPROG afterwards",
            idle);
}

void RebootBench::prove_reset_during_the_words() {
    reset(0);
    dut->reboot_req_i = 1;
    run_until([&] { return dut->icap_csib_o == 0; }, (kHoldMs + 8) * kMsCycles);
    run(3);
    ck.hex("U10 the fourth IPROG word is on the bus", dut->icap_i_o,
           bit_reverse_bytes(kIprogWords[3]));
    dut->rst_n = 0;
    step();
    ck.dec("U10 a reset in the middle of the words: CSIB is high on the next clock",
           dut->icap_csib_o, 1);
    ck.hex("U10 ...and the bus carries the dummy word", dut->icap_i_o, 0xFFFFFFFFu);
    dut->reboot_req_i = 0;
    dut->rst_n = 1;
    bool quiet = true;
    for (uint64_t i = 0; i < 64; ++i) {
        step();
        quiet = quiet && dut->icap_csib_o == 1 && dut->phy_hold_o == 0;
    }
    ck.that("U10 ...and no word follows it", quiet);
}

void RebootBench::prove_the_tick_phase() {
    for (unsigned phase : {1u, static_cast<unsigned>(kMsCycles - 1)}) {
        reset(phase);
        const std::string tag = "U11 phase " + std::to_string(phase);
        const uint64_t n = request_to_hold(4 * kMsCycles);
        grade_quiet(tag + " nothing in the MAC: from the request", n, 2);
        const uint64_t hold = grade_burst(tag, (kHoldMs + 4) * kMsCycles);
        ck.that(label(tag, "the hold stays inside (3,500 ms, 3,501 ms]").c_str(),
                hold > kHoldMs * kMsCycles && hold <= (kHoldMs + 1) * kMsCycles);
        grade_bound(tag + " durable:", n + hold, kEgressMs + kHoldMs + 2);
    }
}

void RebootBench::prove_frames_in_the_mac_are_waited_for() {
    reset(2);
    //! three frames the port handed the MAC before the request
    for (int f = 0; f < 3; ++f) ck.that("U12 the port takes a frame before the request",
                                        offer_frame(4));
    status(false, false, false);
    dut->reboot_req_i = 1;
    run(20 * kMsCycles);
    ck.dec("U12 frames in the MAC at the request: the egress wait has started",
           dut->mac_tx_stop_o, 1);
    ck.dec("U12 ...and no PHY hold 20 ms later with three frames still in the MAC",
           dut->phy_hold_o, 0);
    wire_end();
    run(3 * kMsCycles);
    ck.dec("U12 two frames still in the MAC: no PHY hold", dut->phy_hold_o, 0);
    wire_end();
    run(3 * kMsCycles);
    ck.dec("U12 one frame still in the MAC: no PHY hold", dut->phy_hold_o, 0);
    wire_end();
    const uint64_t n = (kSyncClocks + 1) + run_until([&] { return dut->phy_hold_o == 1; },
                                                     4 * kMsCycles);
    grade_quiet("U12 the last frame reaches the PHY: from its end", n, kSyncClocks + 2);

    //! a frame taken on the clock another one reaches the PHY is counted
    reset(5);
    ck.that("U12 coincide: the port takes a first frame", offer_frame(3));
    run(kSyncClocks + 1);
    ck.that("U12 coincide: the port takes a second frame's first beat", offer_beat(false));
    //! its last beat is taken on the clock the first frame's end has crossed
    dut->mac_txend_tgl_i = !dut->mac_txend_tgl_i;
    run(kSyncClocks - 1);
    ck.that("U12 coincide: ...and its last beat as the first frame's end lands",
            offer_beat(true));
    dut->reboot_req_i = 1;
    run(10 * kMsCycles);
    ck.dec("U12 coincide: the second frame is still in the MAC: no PHY hold",
           dut->phy_hold_o, 0);
    wire_end();
    const uint64_t m = (kSyncClocks + 1) + run_until([&] { return dut->phy_hold_o == 1; },
                                                     4 * kMsCycles);
    grade_quiet("U12 coincide: the second frame reaches the PHY: from its end", m,
                kSyncClocks + 2);
}

void RebootBench::prove_the_frame_in_progress_finishes() {
    reset(4);
    status(true, true, false);
    dut->reboot_req_i = 1;
    run(3);
    //! a frame starts at the port while the drain still runs
    const bool first = offer_beat(false);
    ck.that("U13 the port takes a frame's first beats during the drain",
            offer_beat(false) && first);
    status(true, false, false);         // the drain ends with that frame half taken
    step();
    ck.dec("U13 the egress wait starts with a frame half taken: the port stays open for it",
           dut->mac_tx_stop_o, 0);
    //! the MAC holds the port back in the middle of the frame across ticks
    run(3 * kMsCycles);
    ck.dec("U13 a frame still being taken 3 ms into the wait: no PHY hold", dut->phy_hold_o, 0);
    ck.dec("U13 ...and the port still open for it", dut->mac_tx_stop_o, 0);
    bool rest = true;
    for (int b = 0; b < 3; ++b) rest = offer_beat(b == 2) && rest;
    ck.that("U13 the port takes the rest of the frame in progress", rest);
    ck.dec("U13 ...then starts no new frame", dut->mac_tx_stop_o, 1);
    bool refused = true;
    for (int k = 0; k < 4; ++k) refused = !offer_frame(2) && refused;
    ck.that("U13 a frame offered after it is not taken", refused);
    run(10 * kMsCycles);
    ck.dec("U13 the frame in progress is still in the MAC: no PHY hold", dut->phy_hold_o, 0);
    wire_end();
    const uint64_t n = (kSyncClocks + 1) + run_until([&] { return dut->phy_hold_o == 1; },
                                                     4 * kMsCycles);
    grade_quiet("U13 it reaches the PHY: from its end", n, kSyncClocks + 2);
    run((kHoldMs + 1) * kMsCycles);
    ck.dec("U13 the port stays stopped through the hold", dut->mac_tx_stop_o, 1);
}

void RebootBench::prove_the_egress_bound() {
    reset(6);
    ck.that("U14 the port takes a frame the MAC will never send", offer_frame(2));
    dut->reboot_req_i = 1;
    step();
    step();
    ck.dec("U14 the egress wait starts", dut->mac_tx_stop_o, 1);
    const uint64_t n = run_until([&] { return dut->phy_hold_o == 1; },
                                 (kEgressMs + 4) * kMsCycles);
    std::printf("  [i] U14 egress wait %llu clocks, bound (%llu, %llu]\n",
                static_cast<unsigned long long>(n),
                static_cast<unsigned long long>(kEgressMs * kMsCycles),
                static_cast<unsigned long long>((kEgressMs + 1) * kMsCycles));
    ck.that("U14 a MAC that never finishes: the PHY hold still rises", dut->phy_hold_o == 1);
    ck.that("U14 ...after more than the derived egress bound",
            dut->phy_hold_o == 1 && n > kEgressMs * kMsCycles);
    ck.that("U14 ...and at most one tick more", dut->phy_hold_o == 1
                                                 && n <= (kEgressMs + 1) * kMsCycles);
    const uint64_t hold = grade_burst("U14", (kHoldMs + 4) * kMsCycles);
    //! the worst case once the state is durable: the egress deadline, then the hold
    grade_bound("U14 durable, the egress deadline:", 2 + n + hold, kEgressMs + kHoldMs + 2);
}

void RebootBench::prove_a_flush_clears_the_account() {
    reset(1);
    for (int f = 0; f < 2; ++f) offer_frame(3);
    dut->reboot_req_i = 1;
    run(5 * kMsCycles);
    ck.dec("U15 two frames in the MAC: no PHY hold", dut->phy_hold_o, 0);
    dut->mac_flush_i = 1;               // the link guard holds the MAC in reset
    run(4);
    dut->mac_flush_i = 0;
    const uint64_t n = 4 + run_until([&] { return dut->phy_hold_o == 1; },
                                     (kEgressMs + 4) * kMsCycles);
    grade_quiet("U15 a flush in the wait: from the flush", n, 6);
}

void RebootBench::prove_a_stray_end_does_not_wrap() {
    reset(3);
    wire_end();                         // an end with nothing counted
    wire_end();
    ck.that("U16 the port takes a frame after two stray ends", offer_frame(2));
    dut->reboot_req_i = 1;
    run(10 * kMsCycles);
    ck.dec("U16 the frame is still in the MAC: no PHY hold", dut->phy_hold_o, 0);
    wire_end();
    const uint64_t n = (kSyncClocks + 1) + run_until([&] { return dut->phy_hold_o == 1; },
                                                     4 * kMsCycles);
    grade_quiet("U16 it reaches the PHY: from its end", n, kSyncClocks + 2);
}

void RebootBench::prove_the_stated_bound() {
    for (unsigned phase : {0u, static_cast<unsigned>(kMsCycles - 1)}) {
        reset(phase);
        const std::string tag = "U17 phase " + std::to_string(phase);
        offer_frame(2);                 // never sent
        status(true, true, true);       // never committed
        const uint64_t n = request_to_hold((kDrainMs + kEgressMs + 8) * kMsCycles);
        const uint64_t hold = grade_burst(tag, (kHoldMs + 4) * kMsCycles);
        grade_bound(tag + " deadline and bound:", n + hold, kDrainMs + kEgressMs + kHoldMs + 3);
    }
}

int RebootBench::execute(bool egress_only) {
    const milan::tb::Model<VKL_reboot_ctrl> model;
    dut = model.get();
    ck.echo_passes();
    std::printf("=== KL_reboot_ctrl: AECP REBOOT -> drain -> egress -> PHY hold -> IPROG "
                "(egress bound %llu ms) ===\n", static_cast<unsigned long long>(kEgressMs));
    //! a leg built at another MAC statement grades what that statement
    //! changes: the derived bound and the bound stated from the request
    if (egress_only) {
        prove_the_egress_bound();
        prove_the_stated_bound();
        return ck.report();
    }

    prove_idle_is_inert();
    prove_reset_without_a_writer();
    prove_reset_of_a_durable_state();
    prove_dirty_work_is_waited_for();
    prove_pending_work_is_waited_for();
    prove_the_drain_deadline();
    prove_a_lost_writer_ends_the_drain();
    prove_a_one_clock_request_is_latched();
    prove_status_after_the_drain_changes_nothing();
    prove_reset_during_the_hold();
    prove_reset_during_the_words();
    prove_the_tick_phase();
    prove_frames_in_the_mac_are_waited_for();
    prove_the_frame_in_progress_finishes();
    prove_the_egress_bound();
    prove_a_flush_clears_the_account();
    prove_a_stray_end_does_not_wrap();
    prove_the_stated_bound();

    return ck.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    RebootBench bench;
    return bench.execute(argc == 2 && std::string(argv[1]) == "--egress-only");
}
