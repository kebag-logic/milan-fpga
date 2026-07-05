/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for traffic_classifier.sv AFTER the
 * xpm_fifo_axis -> axis_fifo (Forencich verilog-axis) swap (Track 1.2 of
 * docs/OPEN_SOURCE_MIGRATION.md). That this builds+runs at all proves the module
 * is now Verilator-simulatable (it could not be with XPM).
 *
 * Functional checks (independent of the exact header byte layout — the PCP->queue
 * VALUE is covered by tb/verilator/cls):
 *   - lossless, in-order passthrough: every input beat emerges once, in order,
 *     with tdata/tkeep/tlast byte-exact (the FIFO swap must not corrupt/drop data)
 *   - tdest is stable within each output frame (classification doesn't glitch)
 *   - holds under output back-pressure (toggled m_tready)
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vclassifier_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>
#include <string>

static Vclassifier_wrap* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-34s got=%ld exp=%ld\n", what, got, exp); }
}

struct Beat { uint64_t data; uint8_t keep; bool last; };

static void lo() { dut->clk = 0; dut->eval(); }
static void hi() { dut->clk = 1; dut->eval(); }

// Drive `frames` through the DUT and collect the output; check integrity.
// bp!=0 toggles m_tready to exercise back-pressure.
static void run_frames(const std::vector<std::vector<Beat>>& frames, int bp, const char* tag) {
    // flatten expected input
    std::vector<Beat> expect;
    for (auto& f : frames) for (auto& b : f) expect.push_back(b);

    std::vector<Beat> got;
    std::vector<int>  got_dest;      // tdest per collected beat
    size_t fi = 0, bi = 0;           // input cursor
    size_t total = expect.size();
    int phase = 0;

    for (int c = 0; c < 20000 && got.size() < total; c++) {
        bool have_in = (fi < frames.size());
        if (have_in) {
            const Beat& b = frames[fi][bi];
            dut->s_tdata = b.data; dut->s_tkeep = b.keep;
            dut->s_tlast = b.last; dut->s_tvalid = 1;
        } else {
            dut->s_tvalid = 0;
        }
        int ready = bp ? (phase = !phase) : 1;
        dut->m_tready = ready;

        lo();
        // sink
        if (dut->m_tvalid && ready) {
            got.push_back({ (uint64_t)dut->m_tdata, (uint8_t)dut->m_tkeep, (bool)dut->m_tlast });
            got_dest.push_back(dut->m_tdest);
        }
        bool in_acc = have_in && dut->s_tvalid && dut->s_tready;
        hi();
        if (in_acc) { if (++bi >= frames[fi].size()) { bi = 0; fi++; } }
    }

    // ---- integrity: output == input, in order, byte-exact ----
    ck((std::string(tag) + ": beat count").c_str(), (long)got.size(), (long)total);
    bool eq = got.size() == total;
    for (size_t i = 0; eq && i < total; i++)
        eq = (got[i].data == expect[i].data) && (got[i].keep == expect[i].keep)
             && (got[i].last == expect[i].last);
    ck((std::string(tag) + ": passthrough byte-exact").c_str(), eq ? 1 : 0, 1);

    // ---- tdest stable within each output frame ----
    bool dest_stable = true; int frame_dest = -1;
    for (size_t i = 0; i < got.size(); i++) {
        if (frame_dest < 0) frame_dest = got_dest[i];
        else if (got_dest[i] != frame_dest) dest_stable = false;
        if (got[i].last) frame_dest = -1;   // next frame may differ
    }
    ck((std::string(tag) + ": tdest stable per frame").c_str(), dest_stable ? 1 : 0, 1);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vclassifier_wrap;

    // reset
    dut->resetn = 0;
    dut->s_tvalid = dut->s_tlast = 0; dut->m_tready = 1;
    dut->use_pcp_i = 1; dut->dmac_check_i = 0; dut->default_pcp_i = 0;
    dut->pcp_tc_map_i = 0x00FAC688; dut->prio_regen_i = 0x00FAC688; dut->tc_queue_map_i = 0x000000E4;
    for (int i = 0; i < 6; i++) { lo(); hi(); }
    dut->resetn = 1;
    for (int i = 0; i < 2; i++) { lo(); hi(); }

    printf("== traffic_classifier harness (axis_fifo / Forencich) ==\n");

    // frames long enough for the header parse to complete (>= a few beats)
    auto mk = [](int f, int len) {
        std::vector<Beat> fr;
        for (int b = 0; b < len; b++)
            fr.push_back({ ((uint64_t)0xE0 << 56) | ((uint64_t)f << 32) | (uint64_t)b,
                           (uint8_t)(b == len - 1 ? 0x0F : 0xFF), b == len - 1 });
        return fr;
    };
    std::vector<std::vector<Beat>> frames = { mk(0,4), mk(1,6), mk(2,3), mk(3,5) };

    run_frames(frames, /*bp=*/0, "no-bp");
    run_frames(frames, /*bp=*/1, "backpressure");

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
