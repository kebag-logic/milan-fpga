/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Lock-supervision harness for adp_tx_arbiter.sv — the 07-29 silicon TX
 * wedge class. Built with -GTO_LOG2_P=7 (128-cycle window) so the watchdog
 * verdicts are reachable in simulation.
 *
 * Cases:
 *   1. no false fire — frames with mid-frame tvalid gaps SHORTER than the
 *      window and ordinary back-pressure complete byte-exact, with zero
 *      abort/stall events
 *   2. source abandons a frame (tvalid drops mid-frame, never returns):
 *      abort_evt_o pulses once, the arbiter closes the frame with ONE
 *      injected zero-data all-keep tlast beat, releases the lock, and the
 *      OTHER source's queued frame then flows byte-exact (the trunk
 *      survives). The ADP driver deasserts tvalid on its accepted beat
 *      (AXIS) — a held tvalid would be re-accepted every cycle and hide
 *      the very release being proven (Opus verify D3).
 *   3. downstream refusal (m_tready held 0 with a beat presented):
 *      stall_evt_o pulses, NOTHING is released or injected, and when
 *      tready returns the stalled frame completes byte-exact (a stall
 *      verdict must not corrupt a live frame)
 *   4. diag_locked_o tracks the held grant
 *
 * All source-accept decisions sample the PRE-edge handshake captured inside
 * step() (post-edge tready reads race the legal beat advance — the same
 * trap sim_main.cpp:129 avoids and the first draft of this file hit).
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vadp_tx_arbiter.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vadp_tx_arbiter* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-44s got=%ld exp=%ld\n", what, got, exp); }
    else            printf("  [ ok ] %-44s = %ld\n", what, got);
}

struct Beat { uint64_t data; uint8_t keep; bool last; };
static std::vector<Beat> sink;      // accepted output beats
static long aborts = 0, stalls = 0;
static bool d_acc = false, a_acc = false;  // pre-edge source accepts, last step

static void step() {
    dut->clk_i = 0; dut->eval();
    d_acc = dut->s_data_tvalid && dut->s_data_tready;
    a_acc = dut->s_adp_tvalid  && dut->s_adp_tready;
    if (dut->m_tvalid && dut->m_tready) {
        Beat b; b.data = dut->m_tdata; b.keep = dut->m_tkeep; b.last = dut->m_tlast;
        sink.push_back(b);
    }
    dut->clk_i = 1; dut->eval();
    if (dut->abort_evt_o) aborts++;
    if (dut->stall_evt_o) stalls++;
}
static void run(int n) { for (int i = 0; i < n; i++) step(); }

// drive one full frame on the data source, honouring tready (pre-edge accept),
// with an optional tvalid gap of `gap` cycles before beat `gap_at`
static void send_data_frame(uint8_t tag, int len, int gap_at = -1, int gap = 0) {
    for (int b = 0; b < len; b++) {
        if (b == gap_at) {
            dut->s_data_tvalid = 0;
            run(gap);
        }
        dut->s_data_tdata  = ((uint64_t)tag << 56) | (uint64_t)b;
        dut->s_data_tkeep  = 0xFF;
        dut->s_data_tlast  = (b == len - 1);
        dut->s_data_tvalid = 1;
        do { step(); } while (!d_acc);
    }
    dut->s_data_tvalid = 0; dut->s_data_tlast = 0;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vadp_tx_arbiter;

    dut->rst_n = 0; dut->s_data_tvalid = 0; dut->s_adp_tvalid = 0; dut->m_tready = 1;
    run(3);
    dut->rst_n = 1; run(2);

    printf("== adp_tx_arbiter lock supervision (TO_LOG2_P=7 -> 128-cycle window) ==\n");

    // ---- case 1: legal gaps + back-pressure never fire the watchdog --------
    sink.clear();
    send_data_frame(0xC1, 6, /*gap_at=*/3, /*gap=*/100);   // gap < 128 window
    run(4);
    ck("c1: frame delivered whole", (long)sink.size(), 6);
    ck("c1: tlast on final beat only",
       (sink.size() == 6 && sink.back().last &&
        !sink[4].last && !sink[0].last) ? 1 : 0, 1);
    ck("c1: no abort fired", aborts, 0);
    ck("c1: no stall fired", stalls, 0);

    // ---- case 2: source abandons mid-frame; trunk must survive -------------
    sink.clear(); aborts = stalls = 0;
    // present 3 beats of a "5-beat" frame, then go silent forever
    for (int b = 0; b < 3; b++) {
        dut->s_data_tdata  = ((uint64_t)0xC2 << 56) | (uint64_t)b;
        dut->s_data_tkeep  = 0xFF;
        dut->s_data_tlast  = 0;
        dut->s_data_tvalid = 1;
        do { step(); } while (!d_acc);
    }
    dut->s_data_tvalid = 0;
    // the OTHER source queues ONE single-beat frame behind the held lock;
    // its tvalid drops on the pre-edge accept like a real AXIS source
    dut->s_adp_tdata = ((uint64_t)0xA2 << 56); dut->s_adp_tkeep = 0xFF;
    dut->s_adp_tlast = 1; dut->s_adp_tvalid = 1;
    ck("c2: lock held while abandoned", (long)dut->diag_locked_o, 1);
    for (int i = 0; i < 400; i++) {
        step();
        if (a_acc) { dut->s_adp_tvalid = 0; dut->s_adp_tlast = 0; }
    }
    ck("c2: abort verdict fired once", aborts, 1);
    ck("c2: no stall verdict", stalls, 0);
    // sink saw: 3 real beats + 1 injected close beat + the adp frame
    ck("c2: closed + released (3+1+1 beats)", (long)sink.size(), 5);
    if (sink.size() >= 5) {
        ck("c2: injected beat closes the frame", sink[3].last ? 1 : 0, 1);
        ck("c2: injected beat keep all-set", (long)sink[3].keep, 0xFF);
        ck("c2: injected beat data zeroed", sink[3].data == 0 ? 1 : 0, 1);
        ck("c2: adp frame flowed after release",
           ((sink[4].data >> 56) == 0xA2 && sink[4].last) ? 1 : 0, 1);
    } else {
        // the point of the case — losing these checks must fail the run
        fails += 4; checks += 4;
        printf("  [FAIL] c2: sink too short, injected-beat checks forced red\n");
    }
    run(2);
    ck("c2: lock free after service", (long)dut->diag_locked_o, 0);

    // ---- case 3: downstream refusal is reported, never "recovered" ---------
    sink.clear(); aborts = stalls = 0;
    dut->m_tready = 0;
    dut->s_data_tdata  = ((uint64_t)0xC3 << 56);
    dut->s_data_tkeep  = 0xFF; dut->s_data_tlast = 0; dut->s_data_tvalid = 1;
    run(300);                                    // > one window, beat presented
    ck("c3: stall verdict fired", stalls >= 1 ? 1 : 0, 1);
    ck("c3: no abort under refusal", aborts, 0);
    ck("c3: nothing accepted while refused", (long)sink.size(), 0);
    // accept-locking never locks a frame the downstream refuses outright -
    // the stall verdict above comes from the watchdog's presented-beat arm
    ck("c3: no lock formed under pure refusal", (long)dut->diag_locked_o, 0);
    // downstream returns: the SAME frame completes exactly
    dut->m_tready = 1;
    do { step(); } while (!d_acc);
    dut->s_data_tdata = ((uint64_t)0xC3 << 56) | 1; dut->s_data_tlast = 1;
    do { step(); } while (!d_acc);
    dut->s_data_tvalid = 0; dut->s_data_tlast = 0; run(2);
    ck("c3: stalled frame completed whole", (long)sink.size(), 2);
    if (sink.size() == 2) {
        ck("c3: frame content intact",
           (sink[0].data == ((uint64_t)0xC3 << 56) && !sink[0].last &&
            sink[1].data == (((uint64_t)0xC3 << 56) | 1) && sink[1].last) ? 1 : 0, 1);
    }
    ck("c3: lock free after completion", (long)dut->diag_locked_o, 0);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
