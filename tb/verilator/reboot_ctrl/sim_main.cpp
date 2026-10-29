// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_reboot_ctrl self-checking harness (issue #787): the end-station reset on
// the protocol processor's AECP REBOOT request (IEEE 1722.1-2021 7.4.43).
//
// The module is built at its SHIPPING waits, 10,000 ms of drain and 3,500 ms
// of PHY hold (docs/design/REBOOT_RESET.md). Only the millisecond is
// compressed: this harness drives ms_tick_i itself, one pulse every
// kMsCycles clocks, at a phase each scenario chooses, so the bounds are
// graded in ticks against the documented values rather than against the
// RTL's own constants.
//
// Graded, each by its own labelled checks:
//   U0  idle: no request, no PHY hold, CSIB high and the dummy word, whatever
//       the saved-state status does
//   U1  no live writer (backed 0, even with dirty and pending work): the PHY
//       hold rises two clocks after the request, the hold lasts more than
//       3,500 ms and at most one tick more, then exactly eight clocks of
//       CSIB low carry the IPROG words, bit-reversed per byte; the PHY hold
//       stays up, and the sequence repeats after another hold
//   U2  durable (backed 1, dirty 0, pend 0): the same, at once
//   U3  dirty work with a live writer: no PHY hold while it is dirty, the
//       hold on the clock the dirty bit clears
//   U4  the same for pending work
//   U5  a writer that never commits: the drain ends after more than
//       10,000 ms and at most one tick more
//   U6  the writer lost during the drain: the hold on that clock
//   U7  a one-clock request still resets: the module latches it
//   U8  status moves after the drain end change nothing
//   U9  reset during the hold: back to idle, no IPROG
//   U10 reset in the middle of the IPROG words: CSIB high at once, no word
//       after it
//   U11 the tick phase: two other phases keep the hold inside its bound

#include "VKL_reboot_ctrl.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <array>
#include <cstdint>
#include <cstdio>
#include <string>

namespace {

//! clocks per harness millisecond
constexpr uint64_t kMsCycles = 8;
//! the documented waits (docs/design/REBOOT_RESET.md), independent literals
constexpr uint64_t kDrainMs = 10000;
constexpr uint64_t kHoldMs = 3500;

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
    int execute();

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
    //! steps until CSIB falls, then grades one burst of IPROG words; returns
    //! the steps spent before the burst
    uint64_t grade_burst(const std::string& tag, uint64_t limit);
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
    status(false, false, false);
    run(4);
    dut->rst_n = 1;
    run(3);
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

void RebootBench::prove_idle_is_inert() {
    reset(0);
    bool inert = true;
    for (uint64_t i = 0; i < (kDrainMs + kHoldMs + 4) * kMsCycles; ++i) {
        status((i >> 5) & 1, (i >> 7) & 1, (i >> 9) & 1);
        step();
        inert = inert && dut->phy_hold_o == 0 && dut->icap_csib_o == 1
                && dut->icap_i_o == 0xFFFFFFFFu;
    }
    ck.that("U0 no request: no PHY hold, CSIB high and the dummy word for longer than both waits",
            inert);
}

void RebootBench::prove_reset_without_a_writer() {
    reset(0);
    status(false, true, true);          // a dead writer's leftover work
    dut->reboot_req_i = 1;
    step();
    ck.dec("U1 no writer: no PHY hold on the clock the request is sampled", dut->phy_hold_o, 0);
    step();
    ck.dec("U1 no writer: the PHY hold rises two clocks after the request", dut->phy_hold_o, 1);
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
}

void RebootBench::prove_reset_of_a_durable_state() {
    reset(3);
    status(true, false, false);
    dut->reboot_req_i = 1;
    run(2);
    ck.dec("U2 durable: the PHY hold rises two clocks after the request", dut->phy_hold_o, 1);
    const uint64_t hold = grade_burst("U2", (kHoldMs + 4) * kMsCycles);
    ck.that("U2 the hold is longer than 3,500 ms and at most one tick more",
            hold > kHoldMs * kMsCycles && hold <= (kHoldMs + 1) * kMsCycles);
}

void RebootBench::prove_dirty_work_is_waited_for() {
    reset(5);
    status(true, true, false);
    dut->reboot_req_i = 1;
    bool held_off = true;
    for (uint64_t i = 0; i < 4000 * kMsCycles; ++i) {
        step();
        held_off = held_off && dut->phy_hold_o == 0 && dut->icap_csib_o == 1;
    }
    ck.that("U3 dirty work with a live writer: no PHY hold and no IPROG for 4,000 ms", held_off);
    status(true, false, false);         // the commit's acknowledgement
    step();
    ck.dec("U3 the PHY hold rises on the clock the dirty bit clears", dut->phy_hold_o, 1);
    grade_burst("U3", (kHoldMs + 4) * kMsCycles);
}

void RebootBench::prove_pending_work_is_waited_for() {
    reset(1);
    status(true, false, true);
    dut->reboot_req_i = 1;
    bool held_off = true;
    for (uint64_t i = 0; i < 1500 * kMsCycles; ++i) {
        step();
        held_off = held_off && dut->phy_hold_o == 0;
    }
    ck.that("U4 pending work with a live writer: no PHY hold for 1,500 ms", held_off);
    status(true, true, false);          // the producer wrote it: now dirty
    run(100 * kMsCycles);
    ck.dec("U4 the work moves from pending to dirty: still no PHY hold", dut->phy_hold_o, 0);
    status(true, false, false);
    step();
    ck.dec("U4 the PHY hold rises on the clock the work is durable", dut->phy_hold_o, 1);
}

void RebootBench::prove_the_drain_deadline() {
    reset(7);
    status(true, true, true);           // a live writer that never commits
    dut->reboot_req_i = 1;
    step();                             // the request is sampled
    const uint64_t drain = run_until([&] { return dut->phy_hold_o == 1; },
                                     (kDrainMs + 4) * kMsCycles);
    std::printf("  [i] U5 drain %llu clocks, bound (%llu, %llu]\n",
                static_cast<unsigned long long>(drain),
                static_cast<unsigned long long>(kDrainMs * kMsCycles),
                static_cast<unsigned long long>((kDrainMs + 1) * kMsCycles));
    ck.that("U5 a writer that never commits: the drain ends after more than 10,000 ms",
            drain > kDrainMs * kMsCycles);
    ck.that("U5 ...and at most one tick after 10,000 ms", drain <= (kDrainMs + 1) * kMsCycles);
    const uint64_t hold = grade_burst("U5", (kHoldMs + 4) * kMsCycles);
    ck.that("U5 the hold after a deadline is still longer than 3,500 ms",
            hold > kHoldMs * kMsCycles && hold <= (kHoldMs + 1) * kMsCycles);
}

void RebootBench::prove_a_lost_writer_ends_the_drain() {
    reset(2);
    status(true, true, false);
    dut->reboot_req_i = 1;
    run(2000 * kMsCycles);
    ck.dec("U6 dirty work, live writer: no PHY hold after 2,000 ms", dut->phy_hold_o, 0);
    status(false, true, false);         // T-NVM-WRITER-ALIVE expired: backed falls
    step();
    ck.dec("U6 the writer is lost: the PHY hold rises on that clock", dut->phy_hold_o, 1);
}

void RebootBench::prove_a_one_clock_request_is_latched() {
    reset(4);
    status(false, false, false);
    dut->reboot_req_i = 1;
    step();
    dut->reboot_req_i = 0;
    step();
    ck.dec("U7 a one-clock request: the PHY hold still rises", dut->phy_hold_o, 1);
    grade_burst("U7", (kHoldMs + 4) * kMsCycles);
}

void RebootBench::prove_status_after_the_drain_changes_nothing() {
    reset(6);
    status(true, false, false);
    dut->reboot_req_i = 1;
    run(2);
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
    dut->reboot_req_i = 1;
    run(2 + 1000 * kMsCycles);
    ck.dec("U9 the PHY hold is up 1,000 ms into the hold", dut->phy_hold_o, 1);
    dut->rst_n = 0;
    step();
    dut->reboot_req_i = 0;
    dut->rst_n = 1;
    bool idle = dut->phy_hold_o == 0;
    for (uint64_t i = 0; i < (kHoldMs + 4) * kMsCycles; ++i) {
        step();
        idle = idle && dut->phy_hold_o == 0 && dut->icap_csib_o == 1;
    }
    ck.that("U9 a reset during the hold: back to idle, and no IPROG afterwards", idle);
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
        dut->reboot_req_i = 1;
        run(2);
        const std::string tag = "U11 phase " + std::to_string(phase);
        const uint64_t hold = grade_burst(tag, (kHoldMs + 4) * kMsCycles);
        ck.that(label(tag, "the hold stays inside (3,500 ms, 3,501 ms]").c_str(),
                hold > kHoldMs * kMsCycles && hold <= (kHoldMs + 1) * kMsCycles);
    }
}

int RebootBench::execute() {
    const milan::tb::Model<VKL_reboot_ctrl> model;
    dut = model.get();
    ck.echo_passes();
    std::printf("=== KL_reboot_ctrl: AECP REBOOT -> drain -> PHY hold -> IPROG ===\n");

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

    return ck.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    RebootBench bench;
    return bench.execute();
}
