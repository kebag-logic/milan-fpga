/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for traffic_queues.sv after the Xilinx
 * axis_switch IP + xpm_fifo_axis -> Forencich axis_demux / axis_fifo /
 * axis_arb_mux swap (Track 1.3 of docs/integration/OPEN_SOURCE_MIGRATION.md). Building+running
 * proves the module is now Verilator-simulatable (it could not be with the IP).
 *
 * Checks:
 *   - per-queue routing: a frame pushed with tdest=Q lands in queue Q and, when
 *     Q is granted, emerges intact with m_tdest==Q (never another queue's data)
 *   - grant suppression: with no grant, nothing drains; granting one queue drains
 *     only that queue
 *   - queue_has_data: asserts once a queue is buffered past the underrun margin
 *   - data integrity: byte-exact, in-order, tlast preserved across the queue
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vqueues_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>
#include <string>

static Vqueues_wrap* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-34s got=%ld exp=%ld\n", what, got, exp); }
}

struct Beat { uint64_t data; uint8_t keep; bool last; };
static void lo() { dut->clk = 0; dut->eval(); }
static void hi() { dut->clk = 1; dut->eval(); }
static void step() { lo(); hi(); }

// push one frame (tdest=q) into the queues; returns after it is fully accepted
static void push_frame(int q, const std::vector<Beat>& f) {
    size_t b = 0; int accepted = 0;
    for (int c = 0; c < 5000 && b < f.size(); c++) {
        dut->s_tdata = f[b].data; dut->s_tkeep = f[b].keep;
        dut->s_tlast = f[b].last; dut->s_tdest = q; dut->s_tvalid = 1;
        lo();
        bool acc = dut->s_tvalid && dut->s_tready;
        hi();
        if (acc) { b++; accepted++; }
    }
    dut->s_tvalid = 0; step();
    (void)accepted;
}

// grant queue q, collect the drained frame (until tlast); record tdest seen
static std::vector<Beat> drain(int q, int& out_dest) {
    std::vector<Beat> got; out_dest = -1;
    dut->queue_grant_i = (1u << q);
    for (int c = 0; c < 5000; c++) {
        dut->m_tready = 1;
        lo();
        if (dut->m_tvalid && dut->m_tready) {
            got.push_back({ (uint64_t)dut->m_tdata, (uint8_t)dut->m_tkeep, (bool)dut->m_tlast });
            out_dest = dut->m_tdest;
            bool last = dut->m_tlast;
            hi();
            if (last) break;
        } else hi();
    }
    dut->queue_grant_i = 0; step();
    return got;
}

static std::vector<Beat> mk(uint8_t tag, int len) {
    std::vector<Beat> f;
    for (int b = 0; b < len; b++)
        f.push_back({ ((uint64_t)tag << 56) | (uint64_t)b,
                      (uint8_t)(b == len - 1 ? 0x1F : 0xFF), b == len - 1 });
    return f;
}
static bool eq(const std::vector<Beat>& a, const std::vector<Beat>& b) {
    if (a.size() != b.size()) return false;
    for (size_t i = 0; i < a.size(); i++)
        if (a[i].data != b[i].data || a[i].keep != b[i].keep || a[i].last != b[i].last) return false;
    return true;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vqueues_wrap;

    dut->resetn = 0;
    dut->s_tvalid = dut->s_tlast = 0; dut->m_tready = 0; dut->queue_grant_i = 0;
    for (int i = 0; i < 8; i++) step();
    dut->resetn = 1;
    for (int i = 0; i < 4; i++) step();

    printf("== traffic_queues harness (axis_demux/axis_fifo/axis_arb_mux) ==\n");

    // distinct frames per queue (>= 8 beats so each fills past the has-data margin)
    std::vector<Beat> fq0 = mk(0xA0, 8), fq1 = mk(0xB1, 10),
                      fq2 = mk(0xC2, 8), fq3 = mk(0xD3, 9);

    // load all four queues
    push_frame(0, fq0); push_frame(1, fq1); push_frame(2, fq2); push_frame(3, fq3);
    for (int i = 0; i < 8; i++) step();

    // each queue reports data buffered
    ck("queue_has_data all set", dut->queue_has_data_o & 0xF, 0xF);

    // with no grant, nothing drains
    dut->queue_grant_i = 0;
    bool leaked = false;
    for (int c = 0; c < 40; c++) { dut->m_tready = 1; lo(); if (dut->m_tvalid) leaked = true; hi(); }
    ck("no drain without grant", leaked ? 1 : 0, 0);

    // grant queues out of order; each must emerge intact with correct tdest
    struct { int q; std::vector<Beat>* f; } order[] = { {2,&fq2}, {0,&fq0}, {3,&fq3}, {1,&fq1} };
    for (auto& o : order) {
        int d; auto got = drain(o.q, d);
        ck((std::string("q") + std::to_string(o.q) + " tdest").c_str(), d, o.q);
        ck((std::string("q") + std::to_string(o.q) + " frame byte-exact").c_str(), eq(got, *o.f) ? 1 : 0, 1);
    }

    // all queues drained -> has_data clears
    for (int i = 0; i < 8; i++) step();
    ck("queue_has_data all clear", dut->queue_has_data_o & 0xF, 0x0);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
