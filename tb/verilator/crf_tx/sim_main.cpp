// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_crf_tx module harness: event grid cadence, frame bytes, skip-on-busy,
// enable gating, the SR class A 802.1Q C-TAG shape, the IEEE 1722-2016
// 10.4.3 mr bit, and the 10.7 Equation 14 Max Transit Time rounding.
// clk_audio == clk here (the dp TB does the same); the CDC structure is the
// library cdc_pulse.

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
// decimal form, for the Equation 14 nanosecond quantities (hex would make a
// rounding-by-one defect unreadable)
static void ckd(const char* what, long long got, long long exp) {
    checks++;
    bool ok = (got == exp);
    if (!ok) fails++;
    printf("  [%s] %-40s got=%lld exp=%lld\n", ok ? "PASS" : "FAIL", what, got, exp);
}

static uint64_t ptp_ns = 1000000000ULL;
static long g_step = 0;                 // free-running harness cycle count
static void step() {
    dut->clk_i = 0; dut->clk_audio_i = 0; dut->eval();
    dut->clk_i = 1; dut->clk_audio_i = 1;
    ptp_ns += 10;                       // 10 ns/cycle "PHC"
    dut->ptp_ns_i = ptp_ns;
    dut->eval();
    g_step++;
}

// ---------------------------------------------------------------------------
// Frame capture, pre-edge sampled (the beat visible NOW is the one the coming
// posedge consumes - the documented post-edge capture trap). g_frame_start is
// the harness cycle the frame's first beat was taken on, which the Equation 14
// mid-stream case uses to land a register write a known distance before the
// NEXT launch.
// ---------------------------------------------------------------------------
static long g_frame_start = -1;
static bool next_frame(std::vector<uint8_t>& out, long max_steps = 300000) {
    out.clear();
    std::vector<uint8_t> cur;
    for (long i = 0; i < max_steps; i++) {
        bool last = false;
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            if (cur.empty()) g_frame_start = g_step;
            uint64_t d = dut->m_axis_tdata;
            for (int j = 0; j < 8; j++) cur.push_back((uint8_t)(d >> (8*j)));
            last = dut->m_axis_tlast;
        }
        step();
        if (last) { out = cur; return true; }
    }
    return false;
}
// ... and the same collection started from wherever the harness already is,
// so a case can change an input MID-FRAME and read back what the frame kept
static bool collect_from_here(std::vector<uint8_t>& out, long max_steps = 300000) {
    out.clear();
    for (long i = 0; i < max_steps; i++) {
        bool last = false;
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            uint64_t d = dut->m_axis_tdata;
            for (int j = 0; j < 8; j++) out.push_back((uint8_t)(d >> (8*j)));
            last = dut->m_axis_tlast;
        }
        step();
        if (last) return true;
    }
    out.clear();
    return false;
}
static void wait_tvalid(long max_steps = 300000) {
    for (long i = 0; i < max_steps && !dut->m_axis_tvalid; i++) step();
}

// the CRF reference timestamp of an UNTAGGED frame: AVTPDU at offset 14,
// crf_data at pdu[20..27]
static uint64_t ts_of(const std::vector<uint8_t>& f) {
    uint64_t t = 0;
    for (int j = 0; j < 8; j++) t = (t << 8) | f[34+j];
    return t;
}

// event grid: 96 sample events x /512 = 49152 harness cycles, 10 ns each
static const long     GRID_STEPS_C = 49152;
static const int64_t  GRID_NS_C    = 49152LL * 10;

// ---------------------------------------------------------------------------
// The Equation 14 ORACLE, derived independently of the RTL. 10.7:
//     T_CRF = T_S + ceil(TTmax / P) * P + T_C,   T_C = 0 here
// with P = the nominal media clock period = 1e9/48000 ns. This computes it
// from the UNREDUCED rational; the RTL reduces the same rational to 62500/3
// and runs a sequential divider over it, so agreement is agreement between
// two derivations rather than a restatement of one.
// ---------------------------------------------------------------------------
static uint64_t eq14_periods(uint64_t mtt_ns) {
    const uint64_t NS = 1000000000ULL, BASE = 48000ULL;
    return (mtt_ns * BASE + NS - 1) / NS;            // ceil(TTmax / P)
}
static uint64_t eq14_offset(uint64_t mtt_ns) {
    const uint64_t NS = 1000000000ULL, BASE = 48000ULL;
    return (eq14_periods(mtt_ns) * NS + BASE - 1) / BASE;   // ceil(periods * P)
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_crf_tx;

    dut->rst_n = 0; dut->enable_i = 0; dut->m_axis_tready = 1;
    dut->sid_i = 0x0200000000010001ULL;
    dut->dest_mac_i = 0x91E0F0002A07ULL;
    dut->station_mac_i = 0x020000000001ULL;
    dut->transit_ns_i = 2000000;        // Milan PTO on CRF ts (like any stream)
    dut->ts_uncertain_i = 0;            // synchronised clock (1722-2016 10.4.5)
    dut->mr_i = 0;                      // 10.4.3 level, reset state (no restart)
    // untagged is the RESET shape (see the module header's prune trap):
    // the tag only turns on when the integration has a declared lwSRP row
    dut->vlan_en_i = 0; dut->vlan_pcp_i = 3; dut->vlan_vid_i = 2;
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

    // ---- tu (1722-2016 10.4.5): the CRF timestamps come from the same PHC
    // as AAF's, so an uncertain clock must be declared on CRF too. Same
    // rule as AAF: the stream keeps flowing, only the bit moves.
    dut->ts_uncertain_i = 1;
    {
        std::vector<uint8_t> uf; bool ulast = false; int ugot = 0;
        long ubyte15 = -1, ubytes = 0;
        for (int i = 0; i < 300000 && ugot < 2; i++) {
            if (dut->m_axis_tvalid) {
                uint64_t d = dut->m_axis_tdata;
                for (int j = 0; j < 8; j++) uf.push_back((uint8_t)(d >> (8*j)));
                ulast = dut->m_axis_tlast;
            }
            step();
            if (ulast) { ubyte15 = uf[15]; ubytes = (long)uf.size();
                         ugot++; uf.clear(); ulast = false; }
        }
        ck("tu=1: CRF still streams", ugot, 2);
        ck("tu=1: byte 15 = 0x81 (sv|tu)", ubyte15, 0x81);
        ck("tu=1: frame size unchanged", ubytes, 64);
    }
    dut->ts_uncertain_i = 0;
    {
        std::vector<uint8_t> cf; bool clast = false; int cgot = 0; long cb15 = -1;
        for (int i = 0; i < 300000 && cgot < 2; i++) {
            if (dut->m_axis_tvalid) {
                uint64_t d = dut->m_axis_tdata;
                for (int j = 0; j < 8; j++) cf.push_back((uint8_t)(d >> (8*j)));
                clast = dut->m_axis_tlast;
            }
            step();
            if (clast) { cb15 = cf[15]; cgot++; cf.clear(); clast = false; }
        }
        ck("tu clears: byte 15 back to 0x80", cb15, 0x80);
    }

    // ---- SR class A 802.1Q C-TAG (job 1). The tagged shape must be the
    // SAME 60-octet / 8-beat frame: TPID 0x8100 + TCI at 12..15, ethertype
    // pushed to 16..17, the whole CRF AVTPDU shifted +4, and 4 fewer pad
    // octets. TCI golden = 0x6002 (PCP 3 = SR class A per 802.1Q 34.5 /
    // Table 34-1, DEI 0, VID 2 = the SR VID Milan 4.2.7.2.1 pins) - the
    // same word KL_aaf_packetizer already puts on the wire.
    dut->vlan_en_i = 1;
    {
        std::vector<uint8_t> tf; bool tlast = false; int tgot = 0;
        std::vector<uint8_t> got;
        for (int i = 0; i < 300000 && tgot < 2; i++) {
            if (dut->m_axis_tvalid) {
                uint64_t d = dut->m_axis_tdata;
                for (int j = 0; j < 8; j++) tf.push_back((uint8_t)(d >> (8*j)));
                tlast = dut->m_axis_tlast;
            }
            step();
            if (tlast) { got = tf; tgot++; tf.clear(); tlast = false; }
        }
        ck("tagged: frames still flow", tgot, 2);
        if (got.size() >= 60) {
            const uint8_t* f = got.data();
            ck("tagged: 64 lane bytes (8 beats, unchanged)", (long)got.size(), 64);
            ck("tagged: dmac[0..2] unchanged", (f[0]<<16)|(f[1]<<8)|f[2], 0x91E0F0);
            ck("tagged: smac[0..2] unchanged", (f[6]<<16)|(f[7]<<8)|f[8], 0x020000);
            ck("tagged: TPID 8100 (802.1Q 9.5)", (f[12]<<8)|f[13], 0x8100);
            ck("tagged: TCI 6002 (PCP 3 | DEI 0 | VID 2)", (f[14]<<8)|f[15], 0x6002);
            ck("tagged: ethertype 22F0 at 16", (f[16]<<8)|f[17], 0x22F0);
            ck("tagged: subtype 04 sv 80 at 18", (f[18]<<8)|f[19], 0x0480);
            ck("tagged: type 01 at 21", f[21], 1);
            ck("tagged: sid[0..3] at 22", (long)((f[22]<<24)|(f[23]<<16)|(f[24]<<8)|f[25]), 0x02000000L);
            ck("tagged: sid[4..7] at 26", (long)(((long)f[26]<<24)|(f[27]<<16)|(f[28]<<8)|f[29]), 0x00010001L);
            ck("tagged: pull|base 48000 at 30", (long)(((long)f[30]<<24)|(f[31]<<16)|(f[32]<<8)|f[33]), 0xBB80L);
            ck("tagged: dlen 8 at 34", (f[34]<<8)|f[35], 8);
            ck("tagged: interval 96 at 36", (f[36]<<8)|f[37], 96);
            long tpad_ok = 1;
            for (int p = 46; p < 60; p++) if (f[p]) tpad_ok = 0;
            ck("tagged: zero pad 46..59", tpad_ok, 1);
        }
        // a different PCP/VID must reach the wire verbatim (no hardcode)
        dut->vlan_pcp_i = 2; dut->vlan_vid_i = 0xABC;
        std::vector<uint8_t> af; bool alast = false; int agot = 0; long atci = -1;
        for (int i = 0; i < 300000 && agot < 2; i++) {
            if (dut->m_axis_tvalid) {
                uint64_t d = dut->m_axis_tdata;
                for (int j = 0; j < 8; j++) af.push_back((uint8_t)(d >> (8*j)));
                alast = dut->m_axis_tlast;
            }
            step();
            if (alast) { atci = (af[14]<<8)|af[15]; agot++; af.clear(); alast = false; }
        }
        ck("tagged: PCP/VID are wires, not constants", atci, 0x4ABC);
        dut->vlan_pcp_i = 3; dut->vlan_vid_i = 2;
    }
    // back to untagged: the byte-identical legacy shape returns
    dut->vlan_en_i = 0;
    {
        std::vector<uint8_t> uf2; bool ul2 = false; int ug2 = 0; long et = -1, sz = 0;
        for (int i = 0; i < 300000 && ug2 < 2; i++) {
            if (dut->m_axis_tvalid) {
                uint64_t d = dut->m_axis_tdata;
                for (int j = 0; j < 8; j++) uf2.push_back((uint8_t)(d >> (8*j)));
                ul2 = dut->m_axis_tlast;
            }
            step();
            if (ul2) { et = (uf2[12]<<8)|uf2[13]; sz = (long)uf2.size();
                       ug2++; uf2.clear(); ul2 = false; }
        }
        ck("untagged again: ethertype back at 12", et, 0x22F0);
        ck("untagged again: frame size unchanged", sz, 64);
    }

    // ======================================================================
    // [H2b] IEEE 1722-2016 10.4.3 - the mr (media clock restart) bit.
    //
    // mr is a LEVEL a CRF Talker toggles when the source of the media clock
    // providing the samples changes; PICS Table F.16 makes CRF-3 (the bit
    // set as described in 10.4.3) and CRF-5 (">= 8 CRF AVTPDUs") both
    // mandatory. The toggle policy and the hold belong to
    // KL_media_clock_restart (proved in tb/verilator/tkdiag). What THIS
    // module owes is two wire facts, and they are the two this section
    // pins:
    //   * the granted level reaches the alternative header byte 1, which it
    //     SHARES with tu ({sv, ver[2:0], mr, fs, res, tu}) - so both are
    //     checked together at every combination: a shift-by-one defect in
    //     either shows up as the other, and 0x88 vs 0x81 is the whole
    //     difference between "the media clock restarted" and "the clock is
    //     uncertain"
    //   * mr_last_o is the level the last COMPLETED PDU carried - not the
    //     level currently granted. The hold counts PDUs that WENT OUT, so a
    //     frame already launched when the level flips must still report the
    //     old bit, or the new state reaches the wire for seven PDUs where
    //     the clause says eight.
    // ======================================================================
    printf("[crf_tx] [H2b] 10.4.3 mr: byte 1 beside tu, mr_last_o at tlast\n");
    {
        std::vector<uint8_t> f;
        struct { int mr, tu; long b1; const char* name; } leg[] = {
            {0, 0, 0x80, "[H2b-a] mr=0 tu=0 -> byte 15 = 0x80"},
            {1, 0, 0x88, "[H2b-b] mr=1 tu=0 -> byte 15 = 0x88"},
            {1, 1, 0x89, "[H2b-c] mr=1 tu=1 -> byte 15 = 0x89"},
            {0, 1, 0x81, "[H2b-d] mr=0 tu=1 -> byte 15 = 0x81"},
        };
        for (auto& L : leg) {
            dut->mr_i = L.mr; dut->ts_uncertain_i = L.tu;
            next_frame(f);                       // may be the in-flight one
            next_frame(f);                       // ... this one carries it
            ck(L.name, f[15], L.b1);
            ck("[H2b] ... mr_last_o mirrors the wire", dut->mr_last_o,
               (f[15] >> 3) & 1);
            ck("[H2b] ... frame still 64 lane bytes", (long)f.size(), 64);
        }
        dut->mr_i = 0; dut->ts_uncertain_i = 0;
        next_frame(f); next_frame(f);
        ck("[H2b-e] back to mr=0 tu=0", f[15], 0x80);
        ck("[H2b-e] ... and mr_last_o with it", dut->mr_last_o, 0);

        // the LATCH: flip the level with a frame already on the wire. That
        // frame keeps the old bit, and so does mr_last_o until the NEXT PDU
        // completes - the eight-PDU hold may only count what went out.
        wait_tvalid();
        dut->mr_i = 1; dut->eval();              // mid-frame flip
        collect_from_here(f);
        ck("[H2b-f] mid-frame flip: the launched PDU keeps mr=0", f[15], 0x80);
        ck("[H2b-f] ... mr_last_o still reports 0", dut->mr_last_o, 0);
        next_frame(f);
        ck("[H2b-g] the NEXT PDU carries the new level", f[15], 0x88);
        ck("[H2b-g] ... and mr_last_o follows it", dut->mr_last_o, 1);

        // the tagged shape moves the AVTPDU +4: byte 1 lands at 19
        dut->vlan_en_i = 1;
        next_frame(f); next_frame(f);
        ck("[H2b-h] tagged: mr=1 at byte 19", f[19], 0x88);
        ck("[H2b-h] ... mr_last_o unchanged by the tag", dut->mr_last_o, 1);
        dut->vlan_en_i = 0;
        dut->mr_i = 0;
        next_frame(f); next_frame(f);
        ck("[H2b-i] untagged again, mr back to 0", f[15], 0x80);
        ck("[H2b-i] ... mr_last_o back to 0", dut->mr_last_o, 0);
    }

    // ======================================================================
    // [H3] IEEE 1722-2016 10.7 Equation (14) - the Max Transit Time offset,
    // rounded UP to a whole number of MEDIA CLOCK periods.
    //
    //     T_CRF = T_S + ceil(TTmax / P) * P + T_C
    //
    // P = 1e9/48000 = 20833.333... ns, so the offset a conformant talker
    // stamps is almost never the raw TTmax. PICS Table F.16 CRF-19 asks the
    // question directly.
    //
    // MEASURING IT WITHOUT AN INTERNAL PROBE. The timestamps are latched on
    // the event grid, which is exactly GRID_NS_C apart, so between two
    // consecutive PDUs
    //     ts[k+1] - ts[k] = GRID_NS_C + (offset[k+1] - offset[k])
    // and the chain is anchored at TTmax = 2 ms, where Equation 14 is a
    // no-op (96 periods = exactly 2000000 ns) and the offset is therefore
    // known outright. Each new value is written straight after a PDU
    // completes, which leaves the whole 2 ms grid interval for the
    // sequential conversion, so the next frame carries the new answer.
    // ======================================================================
    printf("[crf_tx] [H3] 10.7 Equation 14 Max Transit Time rounding\n");
    {
        std::vector<uint8_t> f;
        dut->transit_ns_i = 2000000;
        next_frame(f); next_frame(f); next_frame(f);
        uint64_t prev_ts  = ts_of(f);
        int64_t  prev_ofs = 2000000;
        ck("[H3-anchor] 2 ms is 96 whole periods: Eq 14 is a no-op",
           (long)eq14_offset(2000000), 2000000);
        ck("[H3-anchor] ... 96 of them",  (long)eq14_periods(2000000), 96);

        // the named cases from the clause work-through, then the boundaries
        // either side of one media clock period, then the extremes
        const uint32_t sweep[] = {
            2000000,        // the shipping default: byte-identical
            1000001,        // 48.000048 periods -> 49 -> 1020834
            20833,          // just under ONE period -> 1 -> 20834
            0,              // no transit at all -> 0 periods -> 0
            1,              // a single nanosecond still buys a whole period
            20834,          // just over one period -> 2 periods
            41666, 41667,   // either side of two periods (41666.67)
            62500,          // three periods exactly (62500 = 3 * 20833.33)
            125000,         // six periods exactly
            1999999,        // one ns under the default -> still 96 periods
            2000001,        // one ns over -> 97 periods
            4000000,        // class B territory: 192 periods exactly
            2000000,        // ... and back to the shipping default
        };
        for (uint32_t mtt : sweep) {
            dut->transit_ns_i = mtt;
            if (!next_frame(f)) { ck("[H3] frame timeout", 0, 1); break; }
            uint64_t ts   = ts_of(f);
            int64_t applied = prev_ofs
                            + ((int64_t)ts - (int64_t)prev_ts - GRID_NS_C);
            char nm[96];
            snprintf(nm, sizeof nm, "[H3] MTT %u -> Eq 14 offset", mtt);
            ckd(nm, (long long)applied, (long long)eq14_offset(mtt));
            // the two clause invariants, independent of the oracle's value:
            // never BELOW the Max Transit Time (10.7's own reason for
            // rounding up), and never more than one media clock period above
            snprintf(nm, sizeof nm, "[H3] MTT %u -> offset >= TTmax", mtt);
            ck(nm, (long)(applied >= (int64_t)mtt), 1);
            snprintf(nm, sizeof nm, "[H3] MTT %u -> excess < one period", mtt);
            ck(nm, (long)((applied - (int64_t)mtt) < 20834), 1);
            prev_ts = ts; prev_ofs = applied;
        }

        // ---- the rewrite lands BETWEEN frames, never inside one ----------
        // (a) mid-frame: the timestamp was latched at launch, so a write
        //     while the serialiser is running cannot reach the PDU on the
        //     wire - it stays exactly one grid step past its predecessor.
        dut->transit_ns_i = 2000000;
        next_frame(f); next_frame(f);
        prev_ts = ts_of(f);
        wait_tvalid();
        dut->transit_ns_i = 1000001; dut->eval();
        collect_from_here(f);
        ckd("[H3-mid-a] mid-frame write: this PDU keeps the old offset",
            (long long)((int64_t)ts_of(f) - (int64_t)prev_ts), (long long)GRID_NS_C);
        prev_ts = ts_of(f); prev_ofs = 2000000;
        if (next_frame(f)) {
            int64_t applied = prev_ofs
                            + ((int64_t)ts_of(f) - (int64_t)prev_ts - GRID_NS_C);
            ckd("[H3-mid-a] ... the NEXT PDU has the converted one",
                (long long)applied, (long long)eq14_offset(1000001));
            prev_ts = ts_of(f); prev_ofs = applied;
        }

        // (b) a write that lands INSIDE the conversion window, ~20 cycles
        //     before the next launch. The divider needs ~70 cycles, so that
        //     launch MUST still stamp the previous rounded value - a
        //     half-converted quotient is not a transit time - and the frame
        //     after it gets the new one.
        long target = g_frame_start + GRID_STEPS_C - 20;
        while (g_step < target) step();
        dut->transit_ns_i = 20833; dut->eval();
        if (next_frame(f)) {
            ckd("[H3-mid-b] write during the conversion: PREVIOUS value used",
                (long long)((int64_t)ts_of(f) - (int64_t)prev_ts), (long long)GRID_NS_C);
            prev_ts = ts_of(f);
        }
        if (next_frame(f)) {
            int64_t applied = prev_ofs
                            + ((int64_t)ts_of(f) - (int64_t)prev_ts - GRID_NS_C);
            ckd("[H3-mid-b] ... adopted whole on the following PDU",
                (long long)applied, (long long)eq14_offset(20833));
        }
        dut->transit_ns_i = 2000000;
        next_frame(f); next_frame(f);
    }

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
