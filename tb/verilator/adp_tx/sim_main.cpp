/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for adp_tx_arbiter.sv — the 2-input AXIS
 * packet arbiter that merges the ADP advertiser stream with the datapath into
 * the MAC TX stream.
 *
 * Two sources are offered concurrently (each a queue of multi-beat frames with
 * source-tagged, sequence-encoded data). The sink collects the merged output and
 * asserts:
 *   - no frame is ever interleaved (every beat of an output frame shares one
 *     source tag and its beat index increments 0..len-1)
 *   - each source's frames arrive in order, byte-for-byte, with correct tkeep/tlast
 *   - every offered frame is delivered exactly once
 *   - all of the above holds under toggled m_tready (back-pressure)
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vadp_tx_arbiter.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>
#include <deque>

static Vadp_tx_arbiter* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-32s got=%ld exp=%ld\n", what, got, exp); }
}

struct Beat { uint64_t data; uint8_t keep; bool last; };
typedef std::vector<Beat> Frame;

static Frame make_frame(uint8_t tag, int fidx, int len, uint8_t lastkeep) {
    Frame f;
    for (int b = 0; b < len; b++) {
        Beat bt;
        bt.data = ((uint64_t)tag << 56) | ((uint64_t)fidx << 16) | (uint64_t)b;
        bt.last = (b == len - 1);
        bt.keep = bt.last ? lastkeep : 0xFF;
        f.push_back(bt);
    }
    return f;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vadp_tx_arbiter;

    // Source frame programs (distinct tags: 0xD0 = datapath, 0xA0 = adp).
    std::deque<Frame> data_q, adp_q;
    data_q.push_back(make_frame(0xD0, 0, 4,  0xFF));
    data_q.push_back(make_frame(0xD0, 1, 7,  0x0F));
    data_q.push_back(make_frame(0xD0, 2, 1,  0x01));   // single-beat frame
    data_q.push_back(make_frame(0xD0, 3, 5,  0x3F));
    adp_q.push_back(make_frame(0xA0, 0, 11, 0x03));    // ADPDU-sized
    adp_q.push_back(make_frame(0xA0, 1, 5,  0xFF));
    adp_q.push_back(make_frame(0xA0, 2, 2,  0x7F));

    // expected FIFOs (checker consumes as frames complete)
    std::deque<Frame> exp_data = data_q, exp_adp = adp_q;
    size_t total_frames = data_q.size() + adp_q.size();

    // driver cursors
    size_t d_f = 0, d_b = 0, a_f = 0, a_b = 0;

    // sink state
    Frame cur;                 // beats collected for the in-progress output frame
    size_t got_data = 0, got_adp = 0, got_frames = 0;

    dut->rst_n = 0;
    dut->s_data_tvalid = dut->s_adp_tvalid = 0; dut->m_tready = 1;
    for (int i = 0; i < 3; i++) { dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); }
    dut->rst_n = 1;

    printf("== adp_tx_arbiter harness ==\n");

    int bp = 0;
    for (int c = 0; c < 4000; c++) {
        // ---- drive current beat of each source (hold until accepted) ----
        bool d_has = (d_f < data_q.size());
        bool a_has = (a_f < adp_q.size());
        if (d_has) { const Beat& b = data_q[d_f][d_b];
            dut->s_data_tdata = b.data; dut->s_data_tkeep = b.keep;
            dut->s_data_tlast = b.last; dut->s_data_tvalid = 1; }
        else dut->s_data_tvalid = 0;
        if (a_has) { const Beat& b = adp_q[a_f][a_b];
            dut->s_adp_tdata = b.data; dut->s_adp_tkeep = b.keep;
            dut->s_adp_tlast = b.last; dut->s_adp_tvalid = 1; }
        else dut->s_adp_tvalid = 0;

        dut->m_tready = (bp = !bp) ? 1 : 1;    // start no-bp; switched to toggling below
        if (c > 1200) dut->m_tready = (c & 1); // second half: back-pressure

        // low phase: combinational outputs settle
        dut->clk_i = 0; dut->eval();

        // sink: collect an accepted output beat
        if (dut->m_tvalid && dut->m_tready) {
            Beat ob; ob.data = dut->m_tdata; ob.keep = dut->m_tkeep; ob.last = dut->m_tlast;
            cur.push_back(ob);
            if (ob.last) {
                // ---- verify the completed output frame ----
                uint8_t tag = (cur[0].data >> 56) & 0xFF;
                bool one_source = true;
                for (auto& x : cur) if (((x.data >> 56) & 0xFF) != tag) one_source = false;
                ck("frame not interleaved (single tag)", one_source ? 1 : 0, 1);
                std::deque<Frame>& exp = (tag == 0xD0) ? exp_data : exp_adp;
                if (exp.empty()) { ck("unexpected extra frame", 0, 1); }
                else {
                    Frame want = exp.front(); exp.pop_front();
                    ck("frame length", (long)cur.size(), (long)want.size());
                    bool eq = cur.size() == want.size();
                    for (size_t i = 0; eq && i < cur.size(); i++)
                        eq = (cur[i].data == want[i].data) && (cur[i].keep == want[i].keep)
                             && (cur[i].last == want[i].last);
                    ck("frame content byte-exact", eq ? 1 : 0, 1);
                }
                if (tag == 0xD0) got_data++; else got_adp++;
                got_frames++;
                cur.clear();
            }
        }
        // advance the granted source(s) whose beat was accepted this cycle
        bool d_acc = d_has && dut->s_data_tvalid && dut->s_data_tready;
        bool a_acc = a_has && dut->s_adp_tvalid && dut->s_adp_tready;

        // high phase: registers update
        dut->clk_i = 1; dut->eval();

        if (d_acc) { if (++d_b >= data_q[d_f].size()) { d_b = 0; d_f++; } }
        if (a_acc) { if (++a_b >= adp_q[a_f].size())  { a_b = 0; a_f++; } }

        if (got_frames == total_frames) break;
    }

    ck("all data frames delivered", (long)got_data, (long)data_q.size());
    ck("all adp frames delivered",  (long)got_adp,  (long)adp_q.size());
    ck("total frames delivered",    (long)got_frames, (long)total_frames);
    ck("data FIFO drained",  (long)exp_data.size(), 0);
    ck("adp FIFO drained",   (long)exp_adp.size(),  0);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld   (data=%zu adp=%zu frames)\n",
           checks, fails, got_data, got_adp);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
