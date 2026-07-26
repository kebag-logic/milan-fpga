/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for traffic_classifier.sv AFTER the
 * xpm_fifo_axis -> axis_fifo (Forencich verilog-axis) swap (Track 1.2 of
 * docs/integration/OPEN_SOURCE_MIGRATION.md). That this builds+runs at all proves the module
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
static void run_frames(const std::vector<std::vector<Beat>>& frames, int bp, const char* tag,
                       const std::vector<int>* exp_dest = nullptr,
                       const std::vector<int>* exp_de = nullptr) {
    // flatten expected input
    std::vector<Beat> expect;
    for (auto& f : frames) for (auto& b : f) expect.push_back(b);

    std::vector<Beat> got;
    std::vector<int>  got_dest;      // tdest per collected beat
    std::vector<int>  got_de;        // tuser[0] = drop_eligible per collected beat
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
            got_de.push_back(dut->m_tuser & 1);
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

    // ---- tdest CORRECTNESS per frame (the check the 2026-07-05 bug slipped past:
    // stability alone passes a classifier that consistently reports the PREVIOUS
    // frame's class — see docs/findings/CBS_DATAPATH_BUG.md) ----
    if (exp_dest) {
        bool dest_ok = got.size() == total;
        size_t fidx = 0;
        for (size_t i = 0; dest_ok && i < got.size(); i++) {
            if (fidx < exp_dest->size() && got_dest[i] != (*exp_dest)[fidx]) dest_ok = false;
            if (got[i].last) fidx++;
        }
        ck((std::string(tag) + ": tdest CORRECT per frame").c_str(), dest_ok ? 1 : 0, 1);
    }

    // ---- REQ-CLS-05: drop_eligible (DEI) sideband on tuser[0] ----
    // Same contract as tdest: correct AND stable from the frame's FIRST beat.
    if (exp_de) {
        bool de_stable = true; int fde = -1;
        for (size_t i = 0; i < got_de.size(); i++) {
            if (fde < 0) fde = got_de[i];
            else if (got_de[i] != fde) de_stable = false;
            if (got[i].last) fde = -1;
        }
        ck((std::string(tag) + ": DEI stable per frame").c_str(), de_stable ? 1 : 0, 1);

        bool de_ok = got.size() == total;
        size_t fidx = 0;
        for (size_t i = 0; de_ok && i < got_de.size(); i++) {
            if (fidx < exp_de->size() && got_de[i] != (*exp_de)[fidx]) de_ok = false;
            if (got[i].last) fidx++;
        }
        ck((std::string(tag) + ": DEI CORRECT per frame").c_str(), de_ok ? 1 : 0, 1);
    }
}


// Drive `frames` at LINE RATE (s_tvalid never deasserts between frames, m_tready
// pinned high) and return the per-frame tdest actually observed on the FIRST
// beat of each output frame. Used by the REQ-CLS-06 checks, which need the raw
// vector so the harness can also prove its own comparison has teeth.
static std::vector<int> collect_dest_line_rate(const std::vector<std::vector<Beat>>& frames) {
    std::vector<int> per_frame;
    size_t fi = 0, bi = 0, nbeats = 0;
    for (auto& f : frames) nbeats += f.size();
    size_t seen = 0;
    bool first_of_frame = true;
    dut->m_tready = 1;
    for (int c = 0; c < 60000 && seen < nbeats; c++) {
        bool have_in = (fi < frames.size());
        if (have_in) {
            const Beat& b = frames[fi][bi];
            dut->s_tdata = b.data; dut->s_tkeep = b.keep;
            dut->s_tlast = b.last; dut->s_tvalid = 1;    // NEVER deasserted mid-burst
        } else {
            dut->s_tvalid = 0;
        }
        lo();
        if (dut->m_tvalid) {
            if (first_of_frame) { per_frame.push_back(dut->m_tdest); first_of_frame = false; }
            seen++;
            if (dut->m_tlast) first_of_frame = true;
        }
        bool in_acc = have_in && dut->s_tvalid && dut->s_tready;
        hi();
        if (in_acc) { if (++bi >= frames[fi].size()) { bi = 0; fi++; } }
    }
    dut->s_tvalid = 0;
    return per_frame;
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

    // ---- REAL headers, BACK-TO-BACK, alternating queues (regression for
    // docs/findings/CBS_DATAPATH_BUG.md: first beats must carry THIS frame's class) ----
    // expected-queue model == traffic_class_map with the configured tables
    auto expq = [&](bool tagged, int pcp) {
        int eff   = tagged ? pcp : (int)dut->default_pcp_i;
        int regen = (dut->prio_regen_i  >> (3 * eff))   & 7;
        int tc    = (dut->pcp_tc_map_i  >> (3 * regen)) & 7;
        return (int)((dut->tc_queue_map_i >> (2 * tc)) & 3);
    };
    // little-endian beats (BIG_ENDIAN=0 instance): wire byte n = beat[n%8] lane n%8
    auto mkhdr = [](bool tagged, int pcp, int nbeats, int dei = 0) {
        std::vector<uint8_t> f(nbeats * 8, 0xA5);
        for (int i = 0; i < 6; i++) { f[i] = 0x68; f[6 + i] = 0x02; }
        if (tagged) {
            f[12] = 0x81; f[13] = 0x00;
            f[14] = (uint8_t)((pcp << 5) | (dei << 4)); f[15] = 0x02;   // TCI: PCP, DEI, VID 2
            f[16] = 0x08; f[17] = 0x00;
        } else { f[12] = 0x08; f[13] = 0x00; }
        std::vector<Beat> fr;
        for (int b = 0; b < nbeats; b++) {
            uint64_t d = 0;
            for (int k = 0; k < 8; k++) d |= (uint64_t)f[b * 8 + k] << (8 * k);
            fr.push_back({ d, 0xFF, b == nbeats - 1 });
        }
        return fr;
    };
    std::vector<std::vector<Beat>> real;
    std::vector<int> expd;
    for (int r = 0; r < 4; r++)                    // tagged PCP1 / untagged, alternating
        for (int pcp = 0; pcp < 8; pcp += 2) {
            real.push_back(mkhdr(true,  pcp, 4 + (pcp & 3))); expd.push_back(expq(true,  pcp));
            real.push_back(mkhdr(false, 0,   3 + (pcp & 1))); expd.push_back(expq(false, 0));
        }
    run_frames(real, /*bp=*/0, "real-hdr b2b",       &expd);
    run_frames(real, /*bp=*/1, "real-hdr b2b bp",    &expd);

    // ---- gPTP FAST-PATH (2026-07-13): untagged 0x88F7 must classify to
    // GPTP_CLASS (q1) even in PCP mode (untagged default_pcp would otherwise
    // send it wherever the tables point), sandwiched between bulk frames ----
    {
        auto mkgptp = [](int nbeats) {
            std::vector<uint8_t> f(nbeats * 8, 0x00);
            const uint8_t hdr[14] = {0x01,0x80,0xC2,0,0,0x0E, 2,0,0,0,0,2, 0x88,0xF7};
            for (int i = 0; i < 14; i++) f[i] = hdr[i];
            f[14] = 0x12; f[15] = 0x02;
            std::vector<Beat> fr;
            for (int b = 0; b < nbeats; b++) {
                uint64_t d = 0;
                for (int k = 0; k < 8; k++) d |= (uint64_t)f[b * 8 + k] << (8 * k);
                fr.push_back({ d, (uint8_t)(b == nbeats - 1 ? 0x0F : 0xFF), b == nbeats - 1 });
            }
            return fr;
        };
        std::vector<std::vector<Beat>> gm;
        std::vector<int> gexp;
        gm.push_back(mkhdr(false, 0, 5)); gexp.push_back(expq(false, 0));   // bulk before
        gm.push_back(mkgptp(9));          gexp.push_back(1);                // GPTP_CLASS
        gm.push_back(mkhdr(true, 3, 4));  gexp.push_back(expq(true, 3));    // tagged after
        gm.push_back(mkgptp(9));          gexp.push_back(1);                // again
        run_frames(gm, /*bp=*/0, "gptp fast-path (pcp mode)", &gexp);
        // and legacy mode lands on the same class
        dut->use_pcp_i = 0;
        std::vector<std::vector<Beat>> gl = { mkgptp(9) };
        std::vector<int> glexp = { 1 };
        run_frames(gl, /*bp=*/0, "gptp fast-path (legacy mode)", &glexp);
        dut->use_pcp_i = 1;
    }

    // ---- REQ-CLS-07: reserved-DMAC validation of the gPTP fast path ----
    // 802.1AS-2020 s10.5 gPTP rides 01-80-C2-00-00-0E. The DUT parses the DMAC
    // off the WIRE (byte 0 first), so this exercises the parse as well as the
    // gate. Negative leg: the same 0x88F7 frame sent to a foreign DMAC must
    // LOSE the priority queue once CLS_CTRL[1] is set - and must keep it while
    // the bit is clear (reset behaviour is bit-identical to today's silicon).
    {
        // gPTP frame with a settable destination MAC
        auto mkgptp_dmac = [](const uint8_t dm[6], int nbeats) {
            std::vector<uint8_t> f(nbeats * 8, 0x00);
            for (int i = 0; i < 6; i++) f[i] = dm[i];
            const uint8_t rest[8] = {2,0,0,0,0,2, 0x88,0xF7};
            for (int i = 0; i < 8; i++) f[6 + i] = rest[i];
            f[14] = 0x12; f[15] = 0x02;
            std::vector<Beat> fr;
            for (int b = 0; b < nbeats; b++) {
                uint64_t d = 0;
                for (int k = 0; k < 8; k++) d |= (uint64_t)f[b * 8 + k] << (8 * k);
                fr.push_back({ d, (uint8_t)(b == nbeats - 1 ? 0x0F : 0xFF), b == nbeats - 1 });
            }
            return fr;
        };
        const uint8_t good[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};   // reserved gPTP mcast
        const uint8_t spoof[6]= {0x01,0x80,0xC2,0x00,0x00,0x0F};   // one bit off - not gPTP
        const uint8_t uni[6]  = {0x02,0x00,0x00,0x00,0x00,0x68};   // plain unicast

        // default port priority 2 -> identity tables -> queue 2 (NOT q1=GPTP)
        uint32_t ident24 = 0; for (int i = 0; i < 8; i++) ident24 |= (uint32_t)i << (3 * i);
        dut->default_pcp_i = 2; dut->pcp_tc_map_i = ident24; dut->prio_regen_i = ident24;

        // (a) check OFF: every DMAC still takes the fast path
        dut->dmac_check_i = 0;
        std::vector<std::vector<Beat>> off = { mkgptp_dmac(good, 9), mkgptp_dmac(spoof, 9),
                                               mkgptp_dmac(uni, 9) };
        std::vector<int> offexp = { 1, 1, 1 };
        run_frames(off, /*bp=*/0, "cls07 check-off keeps fast path", &offexp);

        // (b) check ON: only the reserved DMAC keeps q1; the others fall to q2
        dut->dmac_check_i = 1;
        std::vector<std::vector<Beat>> on = { mkgptp_dmac(good, 9), mkgptp_dmac(spoof, 9),
                                              mkgptp_dmac(uni, 9), mkgptp_dmac(good, 9) };
        std::vector<int> onexp = { 1, 2, 2, 1 };
        run_frames(on, /*bp=*/0, "cls07 reserved DMAC gates gPTP", &onexp);
        run_frames(on, /*bp=*/1, "cls07 reserved DMAC gates gPTP bp", &onexp);

        // (c) legacy mode: the spoof must land on BEST_EFFORT (q3), not q1
        dut->use_pcp_i = 0;
        std::vector<std::vector<Beat>> lg = { mkgptp_dmac(good, 9), mkgptp_dmac(spoof, 9) };
        std::vector<int> lgexp = { 1, 3 };
        run_frames(lg, /*bp=*/0, "cls07 legacy spoof -> BEST_EFFORT", &lgexp);

        // restore the harness defaults for anything that follows
        dut->use_pcp_i = 1; dut->dmac_check_i = 0; dut->default_pcp_i = 0;
        dut->pcp_tc_map_i = 0x00FAC688; dut->prio_regen_i = 0x00FAC688;
    }

    // ---- REQ-CLS-05: DEI (drop_eligible) sideband on m_axis.tuser[0] ----
    // 802.1Q §6.9.4: the drop-eligibility indicator is carried WITH the frame.
    // Contract mirrors tdest - correct and stable from the frame's first beat,
    // and it must NOT be inferred for untagged frames.
    {
        std::vector<std::vector<Beat>> de;
        std::vector<int> dedest, deexp;
        // tagged DEI=1 and DEI=0 at every PCP, back-to-back, so a stale-by-one
        // sideband (the tdest bug class of 2026-07-05) shows up immediately
        for (int pcp = 0; pcp < 8; pcp++) {
            de.push_back(mkhdr(true, pcp, 4, 1)); dedest.push_back(expq(true, pcp)); deexp.push_back(1);
            de.push_back(mkhdr(true, pcp, 5, 0)); dedest.push_back(expq(true, pcp)); deexp.push_back(0);
        }
        run_frames(de, /*bp=*/0, "cls05 DEI tagged", &dedest, &deexp);
        run_frames(de, /*bp=*/1, "cls05 DEI tagged bp", &dedest, &deexp);

        // DEI must not change the queue: same PCP, both DEI values -> same tdest
        // (802.1Q: drop_eligible is a policer input, not a priority input)
        {
            bool same = true;
            for (size_t i = 0; i + 1 < dedest.size(); i += 2) same &= dedest[i] == dedest[i + 1];
            ck("cls05: DEI does not move the queue", same ? 1 : 0, 1);
        }

        // NEGATIVE: untagged frames have NO drop-eligibility indication. mkhdr
        // fills the payload with 0xA5 - bit 4 of byte 14 is 0xA5 & 0x10 = SET -
        // so a classifier that sliced the TCI unconditionally would report 1.
        // It must report 0. A gPTP frame (untagged, 0x88F7) must likewise be 0.
        {
            std::vector<std::vector<Beat>> un = { mkhdr(false, 0, 4), mkhdr(false, 0, 6),
                                                 mkhdr(true, 5, 4, 1), mkhdr(false, 0, 3) };
            std::vector<int> undest = { expq(false, 0), expq(false, 0), expq(true, 5), expq(false, 0) };
            std::vector<int> unexp  = { 0, 0, 1, 0 };
            run_frames(un, /*bp=*/0, "cls05 untagged DEI=0 (negative)", &undest, &unexp);
        }
    }

    // ---- REQ-CLS-06: back-to-back parsing at line rate ----
    // The header FSM must re-arm on tlast SAME-CYCLE: no inter-frame idle beat
    // exists at line rate, and the 18-byte header spans 3 of the 64-bit beats,
    // so a 3-beat frame completes its header ON its tlast beat - the tightest
    // re-arm case there is. (The module's original note claimed "there should
    // be at least one clock cycle delay incoming packets"; the 2026-07-05
    // sideband redesign removed that constraint, this pins it.)
    {
        std::vector<std::vector<Beat>> burst;
        std::vector<int> exp;
        auto mkgptp_min = [](int nbeats) {          // untagged 0x88F7, reserved DMAC
            std::vector<uint8_t> f(nbeats * 8, 0x00);
            const uint8_t hdr[14] = {0x01,0x80,0xC2,0,0,0x0E, 2,0,0,0,0,2, 0x88,0xF7};
            for (int i = 0; i < 14; i++) f[i] = hdr[i];
            std::vector<Beat> fr;
            for (int b = 0; b < nbeats; b++) {
                uint64_t d = 0;
                for (int k = 0; k < 8; k++) d |= (uint64_t)f[b * 8 + k] << (8 * k);
                fr.push_back({ d, (uint8_t)(b == nbeats - 1 ? 0x0F : 0xFF), b == nbeats - 1 });
            }
            return fr;
        };
        // 3-beat frames dominate: header completes exactly on tlast
        for (int r = 0; r < 6; r++) {
            burst.push_back(mkhdr(true, 6, 3));  exp.push_back(expq(true, 6));   // SR-ish
            burst.push_back(mkhdr(false, 0, 3)); exp.push_back(expq(false, 0));  // best effort
            burst.push_back(mkgptp_min(3));      exp.push_back(1);               // gPTP
            burst.push_back(mkhdr(true, 2, 4));  exp.push_back(expq(true, 2));
            burst.push_back(mkhdr(true, 6, 3));  exp.push_back(expq(true, 6));
            burst.push_back(mkgptp_min(4));      exp.push_back(1);
        }
        std::vector<int> got = collect_dest_line_rate(burst);
        ck("cls06: line-rate frame count", (long)got.size(), (long)exp.size());
        bool ok = got.size() == exp.size();
        for (size_t i = 0; ok && i < got.size(); i++)
            if (got[i] != exp[i]) {
                printf("  [FAIL] cls06 frame %zu: tdest=%d expect %d\n", i, got[i], exp[i]);
                ok = false;
            }
        ck("cls06: zero-idle burst classifies every frame correctly", ok ? 1 : 0, 1);

        // NEGATIVE / teeth: a classifier that reports the PREVIOUS frame's class
        // (the pre-2026-07-05 failure mode, and exactly what a missing tlast
        // re-arm produces) would match this ROTATED expectation. It must not.
        if (got.size() == exp.size() && got.size() > 1) {
            bool rot_match = true;
            for (size_t i = 1; i < got.size(); i++) if (got[i] != exp[i - 1]) rot_match = false;
            ck("cls06: NOT stale-by-one-frame (rotated model must mismatch)",
               rot_match ? 1 : 0, 0);
            // and the expectation vector must actually vary, or the above is vacuous
            bool varies = false;
            for (size_t i = 1; i < exp.size(); i++) if (exp[i] != exp[0]) varies = true;
            ck("cls06: burst spans multiple queues (negative is not vacuous)", varies ? 1 : 0, 1);
        }

        // and the same burst still passes the full integrity model
        run_frames(burst, /*bp=*/0, "cls06 zero-idle burst", &exp);
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
