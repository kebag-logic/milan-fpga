/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * KL_lwsrp_top at the REAL NxN attribute shape: N_CTX_P = L+T-1 with
 * L = T = 4 (the arty 4x4 config), i.e. the row map the CSR 0x800 window
 * actually drives (milan_csr `srp_sel_row_w`, REGISTER_MAP 0x800):
 *
 *     listener k -> ctx row k        (k = 1..L-1)   rows 1,2,3
 *     talker   t -> ctx row (L-1)+t  (t = 1..T-1)   rows 4,5,6
 *     row 0      -> the legacy talker+listener pair
 *
 * Three defects close here, each with its negative leg:
 *
 *  [MAP]   the per-TALKER admission gate must read talker t's row, which is
 *          (L-1)+t, NOT row t. Before 2026-07-26 KL_lwsrp_top read lane t-1
 *          for talker t - correct only at L=1. At L=4 that lane is a
 *          LISTENER row, whose ~row_dir term is 0, so EVERY t>0 gate was
 *          pinned shut whenever the engine was enabled. Negative leg: three
 *          provisioned listener rows must move NO talker gate.
 *
 *  [TSPEC] the TSpec is per row. Two talker rows with different
 *          MaxFrameSize must put their OWN value in their OWN
 *          TalkerAdvertise vector and their OWN slope in the Sigma - a 2ch
 *          and an 8ch stream cannot reserve identically. Negative leg: the
 *          Sigma is the SUM of two DIFFERENT slopes, not 2x either one.
 *
 *  [OOR]   a request naming a row this build does not have is answered but
 *          no longer silent and no longer a LIE: readback = 0xDEAD (the
 *          window's "not backed" idiom) instead of row 0's live status, and
 *          ctx_oor_o latches. Negative leg: every in-range row leaves
 *          ctx_oor_o at 0 and reads its own status.
 */

#include "VKL_lwsrp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>
#include <deque>

static VKL_lwsrp_top* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-54s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    } else {
        printf("  [ok]   %-54s = 0x%llx\n", what, (unsigned long long)got);
    }
}

static const uint64_t STATION = 0x020000000002ULL;
static const uint64_t BRIDGE  = 0x3CC0C6000001ULL;
static const uint16_t VID     = 2;
static const uint16_t MAXFRM0 = 224;              // the shared LWSRP_TSPEC
static const uint32_t LATENCY = 500000;

// talker rows 4/5/6 = talker streams 1/2/3, with DIFFERENT geometries:
// 2ch, 8ch, 4ch -> MSDU 24+24*C = 72, 216, 120
static const uint64_t T1_SID = 0x0200000000020001ULL;
static const uint64_t T2_SID = 0x0200000000020002ULL;
static const uint64_t T3_SID = 0x0200000000020003ULL;
static const uint16_t T1_MF = 72, T2_MF = 216, T3_MF = 120;
// listener rows 1/2/3
static const uint64_t L1_SID = 0x0200000000110001ULL;
static const uint64_t L2_SID = 0x0200000000110002ULL;
static const uint64_t L3_SID = 0x0200000000110003ULL;

enum { EV_NEW = 0, EV_JOININ = 1, EV_IN = 2, EV_JOINMT = 3, EV_MT = 4,
       EV_LV = 5 };
enum { D_IGN = 0, D_ASKFAIL = 1, D_READY = 2, D_READYFAIL = 3 };

// ---- cycle engine + TX collector -----------------------------------------
static long cyc = 0;
static std::deque<std::vector<uint8_t>> tx_frames;
static std::vector<uint8_t> partial;

static void step() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    cyc++;
    if (dut->m_axis_tvalid && dut->m_axis_tready) {
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_tkeep >> l) & 1)
                partial.push_back((dut->m_axis_tdata >> (8 * l)) & 0xFF);
        if (dut->m_axis_tlast) { tx_frames.push_back(partial); partial.clear(); }
    }
}
static void run(long n) { for (long i = 0; i < n; i++) step(); }
static void drain_tx() { tx_frames.clear(); }

static bool is_msrp(const std::vector<uint8_t>& f) {
    return f.size() >= 16 && f[12] == 0x22 && f[13] == 0xEA;
}
static bool is_ext_ta(const std::vector<uint8_t>& f) {
    return is_msrp(f) && f[15] == 1;      // ctx serializer, TalkerAdvertise 1st
}

static void put_be(std::vector<uint8_t>& b, uint64_t v, int n) {
    for (int i = n - 1; i >= 0; i--) b.push_back((v >> (8 * i)) & 0xFF);
}

// ---- bridge PDU builders --------------------------------------------------
static std::vector<uint8_t> bridge_domain(int cls, int prio, int vid) {
    std::vector<uint8_t> f;
    put_be(f, 0x0180C200000EULL, 6); put_be(f, BRIDGE, 6); put_be(f, 0x22EA, 2);
    f.push_back(0);
    f.push_back(4); f.push_back(4); put_be(f, 9, 2);
    put_be(f, 1, 2);
    f.push_back((uint8_t)cls); f.push_back((uint8_t)prio); put_be(f, vid, 2);
    f.push_back(EV_JOININ * 36);
    put_be(f, 0, 2); put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

//! one single-value Listener attribute for `sid` (the bridge's Ready)
static std::vector<uint8_t> bridge_listener(uint64_t sid, int evt, int decl) {
    std::vector<uint8_t> f;
    put_be(f, 0x0180C200000EULL, 6); put_be(f, BRIDGE, 6); put_be(f, 0x22EA, 2);
    f.push_back(0);
    f.push_back(3); f.push_back(8); put_be(f, 14, 2);
    put_be(f, 1, 2);
    put_be(f, sid, 8);
    f.push_back((uint8_t)(evt * 36));
    f.push_back((uint8_t)(decl * 64));
    put_be(f, 0, 2); put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

//! one single-value TalkerAdvertise for `sid` (what a LISTENER row tracks)
static std::vector<uint8_t> bridge_tadv(uint64_t sid, int evt) {
    std::vector<uint8_t> f;
    put_be(f, 0x0180C200000EULL, 6); put_be(f, BRIDGE, 6); put_be(f, 0x22EA, 2);
    f.push_back(0);
    f.push_back(1); f.push_back(25); put_be(f, 28, 2);
    put_be(f, 1, 2);
    put_be(f, sid, 8);
    for (int i = 0; i < 17; i++) f.push_back(0xA0 + i);
    f.push_back((uint8_t)(evt * 36));
    put_be(f, 0, 2); put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

static void feed(const std::vector<uint8_t>& f) {
    size_t n = f.size();
    for (size_t off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t k = 0;
        for (int l = 0; l < 8 && off + l < n; l++) {
            d |= (uint64_t)f[off + l] << (8 * l);
            k |= 1 << l;
        }
        dut->rx_tvalid_i = 1; dut->rx_tdata_i = d; dut->rx_tkeep_i = k;
        dut->rx_tlast_i = (off + 8 >= n);
        step();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0;
    step();
}

// ---- provisioning port ----------------------------------------------------
static void ctx_write(int idx, int valid, int dir, uint64_t sid,
                      uint64_t dmac, uint16_t maxf, uint16_t ivf) {
    dut->ctx_req_i = 1; dut->ctx_we_i = 1; dut->ctx_idx_i = idx;
    dut->ctx_valid_i = valid; dut->ctx_dir_i = dir; dut->ctx_sid_i = sid;
    dut->ctx_dmac_i = dmac; dut->ctx_prio_rank_i = 0x70;
    dut->ctx_max_frame_i = maxf; dut->ctx_interval_i = ivf;
    dut->ctx_latency_i = LATENCY;
    int guard = 20;
    do { step(); } while (!dut->ctx_gnt_o && guard--);
    dut->ctx_req_i = 0; dut->ctx_we_i = 0;
    step();
}

static uint16_t ctx_read(int idx, uint64_t* sid = nullptr) {
    dut->ctx_req_i = 1; dut->ctx_we_i = 0; dut->ctx_idx_i = idx;
    int guard = 20;
    do { step(); } while (!dut->ctx_gnt_o && guard--);
    uint16_t stat = dut->ctx_rd_stat_o;
    if (sid) *sid = dut->ctx_rd_sid_o;
    dut->ctx_req_i = 0;
    step();
    return stat;
}

//! pull `sid`'s MaxFrameSize out of a ctx TalkerAdvertise MRPDU
//! (eth 14 + ver 1 + msg hdr 4, then 28-byte single-value vectors)
static int ta_maxframe(const std::vector<uint8_t>& f, uint64_t sid) {
    if (!is_ext_ta(f)) return -1;
    size_t listlen = ((size_t)f[17] << 8) | f[18];
    size_t base = 19;
    for (size_t o = 0; o + 28 <= listlen - 2 && base + o + 28 <= f.size();
         o += 28) {
        uint64_t s = 0;
        for (int i = 0; i < 8; i++) s = (s << 8) | f[base + o + 2 + i];
        if (s == sid)   // vector: vech2 sid8 dmac6 vid2 | maxframe2 |
            return (f[base + o + 18] << 8) | f[base + o + 19];
    }
    return -1;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_lwsrp_top;

    dut->rst_n = 0; dut->enable_i = 0; dut->talker_en_i = 0; dut->is_1g_i = 0;
    dut->station_mac_i = STATION; dut->unique_id_i = 0;
    dut->dest_mac_i = 0x91E0F000FE02ULL; dut->vid_i = VID;
    dut->max_frame_i = MAXFRM0; dut->interval_frames_i = 1;
    dut->latency_i = LATENCY;
    dut->rx_tvalid_i = 0; dut->rx_tdata_i = 0; dut->rx_tkeep_i = 0;
    dut->rx_tlast_i = 0; dut->m_axis_tready = 1;
    dut->ctx_req_i = 0; dut->ctx_we_i = 0; dut->ctx_idx_i = 0;
    dut->ctx_valid_i = 0; dut->ctx_dir_i = 0; dut->ctx_sid_i = 0;
    dut->ctx_dmac_i = 0; dut->ctx_prio_rank_i = 0;
    dut->ctx_max_frame_i = 0; dut->ctx_interval_i = 0; dut->ctx_latency_i = 0;
    dut->lstn_bound_i = 0; dut->lstn_declare_i = 0; dut->lstn_sid_i = 0;
    for (int i = 0; i < 8; i++) step();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) step();

    printf("== KL_lwsrp_top L=4 T=4 N_CTX_P=7 (0x800 window row map) ==\n");

    // the legacy row stays OUT of the way: talker_en_i = 0 so gate bit 0 and
    // the Sigma carry only the ctx rows under test
    dut->enable_i = 1;
    run(400);
    feed(bridge_domain(6, 3, VID));
    run(200);
    ck("setup: domain ok", dut->domain_ok_o, 1);
    ck("setup: no OOR yet", dut->ctx_oor_o, 0);
    ck("setup: every gate shut", dut->stream_gate_o, 0);

    // ---------------------------------------------------------------- [MAP]
    // NEGATIVE LEG FIRST: the three LISTENER rows (1..3) must move no talker
    // gate. On the pre-fix RTL these are exactly the rows the talker gates
    // read, so this leg is what made the bug invisible: the gates were shut
    // and it looked like "no reservation yet".
    printf("-- [MAP] listener rows 1..3 (the rows talker gates used to read) --\n");
    ctx_write(1, 1, 1, L1_SID, 0, 0, 0);
    ctx_write(2, 1, 1, L2_SID, 0, 0, 0);
    ctx_write(3, 1, 1, L3_SID, 0, 0, 0);
    feed(bridge_tadv(L1_SID, EV_JOININ));
    feed(bridge_tadv(L2_SID, EV_JOININ));
    feed(bridge_tadv(L3_SID, EV_JOININ));
    run(600);
    ck("[MAP-] listener rows registered", (dut->ctx_reg_o >> 1) & 7, 7);
    ck("[MAP-] listener rows ready", (dut->ctx_ready_o >> 1) & 7, 7);
    ck("[MAP-] NO talker gate opened by them", dut->stream_gate_o, 0);
    ck("[MAP-] no slope requested", dut->idle_slope_o, 0);
    drain_tx();

    // POSITIVE LEG: talker t -> ctx row (L-1)+t = 4,5,6
    printf("-- [MAP] talker rows 4/5/6 = talker streams 1/2/3 --\n");
    ctx_write(4, 1, 0, T1_SID, 0x91E0F000FE11ULL, T1_MF, 1);
    ctx_write(5, 1, 0, T2_SID, 0x91E0F000FE12ULL, T2_MF, 1);
    ctx_write(6, 1, 0, T3_SID, 0x91E0F000FE13ULL, T3_MF, 1);
    run(400);
    ck("[MAP] rows 4/5/6 declared, gates still shut (no Ready yet)",
       dut->stream_gate_o, 0);
    // the bridge declares Listener Ready for row 4's sid ONLY
    feed(bridge_listener(T1_SID, EV_JOININ, D_READY));
    run(600);
    ck("[MAP] talker 1 gate open (ctx row 4)",
       (dut->stream_gate_o >> 1) & 1, 1);
    ck("[MAP] talker 2 gate still shut", (dut->stream_gate_o >> 2) & 1, 0);
    ck("[MAP] talker 3 gate still shut", (dut->stream_gate_o >> 3) & 1, 0);
    ck("[MAP] legacy row 0 gate untouched", dut->stream_gate_o & 1, 0);
    ck("[MAP] Sigma = row 4's slope only", dut->idle_slope_o,
       (uint32_t)((T1_MF + 42) * 64000));

    // row 5 next: a DIFFERENT gate bit, and the Sigma grows by ITS slope
    feed(bridge_listener(T2_SID, EV_JOININ, D_READY));
    run(600);
    ck("[MAP] talker 2 gate open (ctx row 5)",
       (dut->stream_gate_o >> 2) & 1, 1);
    ck("[MAP] talker 3 gate STILL shut (row 6 has no Ready)",
       (dut->stream_gate_o >> 3) & 1, 0);

    // -------------------------------------------------------------- [TSPEC]
    printf("-- [TSPEC] per-row MaxFrameSize on the wire and in the Sigma --\n");
    ck("[TSPEC] Sigma = row4 + row5, two DIFFERENT slopes",
       dut->idle_slope_o,
       (uint32_t)((T1_MF + 42) * 64000 + (T2_MF + 42) * 64000));
    // negative leg: it is a sum of unequal terms, not 2x either one
    ck("[TSPEC-] Sigma != 2 x row4's slope",
       dut->idle_slope_o == (uint32_t)(2 * (T1_MF + 42) * 64000) ? 1 : 0, 0);
    ck("[TSPEC-] Sigma != 2 x row5's slope",
       dut->idle_slope_o == (uint32_t)(2 * (T2_MF + 42) * 64000) ? 1 : 0, 0);
    ck("[TSPEC-] Sigma != 2 x the shared LWSRP_TSPEC slope",
       dut->idle_slope_o == (uint32_t)(2 * (MAXFRM0 + 42) * 64000) ? 1 : 0, 0);
    ck("[TSPEC] within the 100 Mb/s 75 % ceiling", dut->over_limit_o, 0);
    // and on the wire: each row's TalkerAdvertise carries its OWN TSpec
    drain_tx();
    {
        int m1 = -1, m2 = -1, m3 = -1;
        long deadline = cyc + 40000;
        while (cyc < deadline && (m1 < 0 || m2 < 0 || m3 < 0)) {
            for (auto& f : tx_frames) {
                int a = ta_maxframe(f, T1_SID); if (a >= 0) m1 = a;
                int b = ta_maxframe(f, T2_SID); if (b >= 0) m2 = b;
                int c = ta_maxframe(f, T3_SID); if (c >= 0) m3 = c;
            }
            step();
        }
        ck("[TSPEC] row 4 TalkerAdvertise MaxFrameSize", (unsigned)m1, T1_MF);
        ck("[TSPEC] row 5 TalkerAdvertise MaxFrameSize", (unsigned)m2, T2_MF);
        ck("[TSPEC] row 6 TalkerAdvertise MaxFrameSize", (unsigned)m3, T3_MF);
        ck("[TSPEC-] rows do not share one MaxFrameSize",
           (m1 == m2 || m2 == m3 || m1 == m3) ? 1 : 0, 0);
        ck("[TSPEC-] no row fell back to the shared LWSRP_TSPEC",
           (m1 == MAXFRM0 || m2 == MAXFRM0 || m3 == MAXFRM0) ? 1 : 0, 0);
    }

    // ---------------------------------------------------------------- [OOR]
    printf("-- [OOR] rows this build does not have are LOUD, not aliased --\n");
    // negative leg: every in-range row reads ITS OWN state, oor stays clear
    {
        uint64_t s = 0;
        uint16_t st4 = ctx_read(4, &s);
        ck("[OOR-] row 4 readback: valid", (st4 >> 15) & 1, 1);
        ck("[OOR-] row 4 readback: dir = talker", (st4 >> 14) & 1, 0);
        ck("[OOR-] row 4 readback: its own sid", s, T1_SID);
        uint16_t st1 = ctx_read(1, &s);
        ck("[OOR-] row 1 readback: dir = listener", (st1 >> 14) & 1, 1);
        ck("[OOR-] row 1 readback: its own sid", s, L1_SID);
        uint16_t st0 = ctx_read(0, &s);
        ck("[OOR-] row 0 readback: the legacy pair sid", s,
           (STATION << 16));
        ck("[OOR-] row 0 is not the not-backed sentinel",
           st0 == 0xDEAD ? 1 : 0, 0);
        ck("[OOR-] no shortfall latched by any in-range row",
           dut->ctx_oor_o, 0);
    }
    // positive leg: row 7 and row 15 do not exist in an N_CTX_P = 7 build
    {
        uint64_t s = 0;
        uint16_t st7 = ctx_read(7, &s);
        ck("[OOR] row 7 readback = the not-backed sentinel", st7, 0xDEAD);
        ck("[OOR] row 7 sid reads 0, not row 0's", s, 0);
        ck("[OOR] shortfall latched", dut->ctx_oor_o, 1);
        uint16_t st15 = ctx_read(15, &s);
        ck("[OOR] row 15 too", st15, 0xDEAD);
        // a WRITE to an unbacked row changes nothing and stays latched
        ctx_write(7, 1, 0, 0xDEADBEEFCAFEULL, 0, 999, 1);
        run(200);
        ck("[OOR] a write to row 7 opened no gate",
           dut->stream_gate_o & ~0x6u, 0);
        ck("[OOR] shortfall stays latched", dut->ctx_oor_o, 1);
        // and the in-range rows are unharmed by it
        uint16_t st4 = ctx_read(4, &s);
        ck("[OOR] row 4 survived the bad write", (st4 >> 15) & 1, 1);
        ck("[OOR] row 4 sid intact", s, T1_SID);
    }

    ck("final: no RX drops", dut->rx_drops_o, 0);
    ck("final: ctx MRPDUs were sent", dut->ctx_tx_count_o > 0, 1);

    // ONE tally line per executable. This used to print the same numbers twice
    // in two different shapes - the `checks:` form was bolted on so the sweep's
    // old `grep -o 'checks: *[0-9]*'` could see them at all. Now that
    // scripts/suite_tally.py reads both shapes, printing both would DOUBLE this
    // suite's contribution to the headline total.
    printf("== %ld checks, %ld failures ==\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    delete dut;
    return fails ? 1 : 0;
}
