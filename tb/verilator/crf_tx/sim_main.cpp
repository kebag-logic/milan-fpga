// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_crf_tx module harness: event grid cadence, frame bytes, skip-on-busy,
// enable gating. clk_audio == clk here (the dp TB does the same); the CDC
// structure is the library cdc_pulse.

#include "VKL_crf_tx.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <vector>
#include <cstdint>

static VKL_crf_tx* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, long got, long exp) {
    checks++;
    bool ok = (got == exp);
    if (!ok) fails++;
    printf("  [%s] %-40s got=0x%08lx exp=0x%08lx\n", ok ? "PASS" : "FAIL", what, got, exp);
}

static uint64_t ptp_ns = 1000000000ULL;
static void step() {
    dut->clk_i = 0; dut->clk_audio_i = 0; dut->eval();
    dut->clk_i = 1; dut->clk_audio_i = 1;
    ptp_ns += 10;                       // 10 ns/cycle "PHC"
    dut->ptp_ns_i = ptp_ns;
    dut->eval();
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_crf_tx;

    dut->rst_n = 0; dut->enable_i = 0; dut->m_axis_tready = 1;
    dut->sid_i = 0x0200000000010001ULL;
    dut->dest_mac_i = 0x91E0F0002A07ULL;
    dut->station_mac_i = 0x020000000001ULL;
    dut->transit_ns_i = 2000000;        // Milan PTO on CRF ts (like any stream)
    for (int i = 0; i < 8; i++) step();
    dut->rst_n = 1;
    for (int i = 0; i < 8; i++) step();

    printf("[crf_tx] event grid + frame bytes\n");
    ck("idle while disabled: no tvalid", dut->m_axis_tvalid, 0);

    // stay disabled across one full event period: still silent
    for (int i = 0; i < 50000; i++) step();
    ck("disabled: still silent", dut->m_axis_tvalid, 0);
    ck("disabled: count 0", dut->tx_count_o, 0);

    dut->enable_i = 1;

    // capture 3 frames; events every 49152 cycles
    std::vector<std::vector<uint8_t>> frames;
    std::vector<uint8_t> cur;
    std::vector<uint64_t> ptp_at_last;   // ptp when each frame's tlast left
    long first_gap = -1, gap = 0, prev_end = -1;
    long c;
    for (c = 0; c < 200000 && frames.size() < 3; c++) {
        step();
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            uint64_t d = dut->m_axis_tdata;
            for (int j = 0; j < 8; j++) cur.push_back((uint8_t)(d >> (8*j)));
            if (dut->m_axis_tlast) {
                if (prev_end >= 0 && first_gap < 0) first_gap = c - prev_end;
                prev_end = c;
                frames.push_back(cur); cur.clear();
                ptp_at_last.push_back(ptp_ns);
            }
        }
    }
    ck("3 frames emitted", frames.size(), 3);
    step();                             // count increments the edge after tlast
    ck("count 3", dut->tx_count_o, 3);
    if (frames.size() == 3) {
        const uint8_t* f = frames[0].data();
        ck("frame is 64 lane bytes (8 beats)", frames[0].size(), 64);
        ck("dmac[0..2]", (f[0]<<16)|(f[1]<<8)|f[2], 0x91E0F0);
        ck("dmac[3..5]", (f[3]<<16)|(f[4]<<8)|f[5], 0x002A07);
        ck("smac[0..2]", (f[6]<<16)|(f[7]<<8)|f[8], 0x020000);
        ck("ethertype 22F0", (f[12]<<8)|f[13], 0x22F0);
        ck("subtype 04 sv 80", (f[14]<<8)|f[15], 0x0480);
        ck("seq 0", f[16], 0);
        ck("type 01", f[17], 1);
        ck("sid[0..3]", (long)((f[18]<<24)|(f[19]<<16)|(f[20]<<8)|f[21]), 0x02000000L);
        ck("sid[4..7]", (long)(((long)f[22]<<24)|(f[23]<<16)|(f[24]<<8)|f[25]), 0x00010001L);
        ck("pull|base 48000", (long)(((long)f[26]<<24)|(f[27]<<16)|(f[28]<<8)|f[29]), 0xBB80L);
        ck("dlen 8", (f[30]<<8)|f[31], 8);
        ck("interval 96", (f[32]<<8)|f[33], 96);
        long pad_ok = 1;
        for (int p = 42; p < 60; p++) if (f[p]) pad_ok = 0;
        ck("zero pad", pad_ok, 1);
        ck("seq 1 on frame 2", frames[1][16], 1);
        ck("seq 2 on frame 3", frames[2][16], 2);
        // ts fields: 96*512 cycles * 10 ns = 491520 ns apart exactly
        auto ts_of = [&](int k) {
            uint64_t t = 0;
            for (int j = 0; j < 8; j++) t = (t << 8) | frames[k][34+j];
            return t;
        };
        ck("ts delta = event grid (491520 ns)", (long)(ts_of(1)-ts_of(0)), 49152*10);
        ck("ts delta stable", (long)(ts_of(2)-ts_of(1)), 49152*10);
        ck("inter-frame gap ~= 49152 cycles", (first_gap > 49000 && first_gap < 49300) ? 1 : 0, 1);
        // Milan PTO: ts is future-dated by transit_ns at the event; by the
        // time tlast leaves (CDC + 8 beats) the margin is PTO minus ~100 ns
        long lead0 = (long)(ts_of(0) - ptp_at_last[0]);
        ck("ts future-dated by ~PTO (Milan)", (lead0 > 1990000 && lead0 <= 2000000) ? 1 : 0, 1);
    }

    // skip-on-busy: hold tready low across >1 event period, then release.
    // The pending frame drains; skipped events emit nothing, and the next
    // frame's ts is a LATER grid point (grid stays truthful).
    dut->m_axis_tready = 0;
    long vhigh = 0;
    for (int i = 0; i < 110000; i++) { step(); if (dut->m_axis_tvalid) vhigh++; }
    printf("  [dbg] blocked window: tvalid high %ld cycles, count=%u\n",
           vhigh, (unsigned)dut->tx_count_o);
    // pre-edge sampling: the stuck frame's beat 0 is already presented, so
    // read BEFORE each posedge (the beat visible now is the one the coming
    // edge consumes) - the documented post-edge capture trap
    dut->m_axis_tready = 1; dut->eval();
    std::vector<uint8_t> nf; long got_n = 0; uint64_t ts3 = 0, ts4 = 0; uint8_t s3 = 0, s4 = 0;
    for (int i = 0; i < 120000 && got_n < 2; i++) {
        bool last = false;
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            uint64_t d = dut->m_axis_tdata;
            for (int j = 0; j < 8; j++) nf.push_back((uint8_t)(d >> (8*j)));
            last = dut->m_axis_tlast;
        }
        step();
        if (last) {
            uint64_t t = 0;
            for (int j = 0; j < 8; j++) t = (t << 8) | nf[34+j];
            if (got_n == 0) { ts3 = t; s3 = nf[16]; } else { ts4 = t; s4 = nf[16]; }
            got_n++; nf.clear();
        }
    }
    ck("blocked window: frames resume", got_n, 2);
    ck("seq continuous across skip", (long)(uint8_t)(s4 - s3), 1);
    ck("post-skip ts still on the grid", (long)((ts4 - ts3) % 491520ULL), 0);
    ck("blocked events skipped, not queued", s3, 3);
    step();                             // count increments the edge after tlast
    ck("no double-emit backlog", dut->tx_count_o, 5);

    // disable: silent within one event period
    dut->enable_i = 0;
    long stray = 0;
    for (int i = 0; i < 60000; i++) { step(); if (dut->m_axis_tvalid) stray++; }
    ck("disable: wire silent", stray, 0);

    printf("======================================================================\n");
    printf("KL_crf_tx: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
