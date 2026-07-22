/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_acmp_tlkr_ctx at N_SRC_P=4 — the talker-
 * activation side of the N-context ACMP engine: per-uid probe windows on
 * ONE shared 1 s sweep (timer wheel), per-source stream params, and the
 * Milan near-stateless response tables per source context.
 *
 * Traceability (IEEE 1722.1-2021 / AVnu Milan v1.2):
 *   ACMP-2   8.2.1.4   talker command dispatch per talker_unique_id
 *   ACMP-3   8.2.1.5   TALKER_UNKNOWN_ID for uid >= N
 *   ACMP-5   8.2.1.7   stream_id = {station MAC, uid} per source; dest_mac
 *                      per-source config slice
 *   M-ACMP-6 5.5.4.1   PROBE_TX per uid: SUCCESS + LIVE params + 15 s arm
 *   M-ACMP-7 5.5.4.2/3 DISCONNECT_TX no-state-change; GET_TX_STATE live
 *   M-ACMP-8 5.5.4.4   GET_TX_CONNECTION -> NOT_SUPPORTED
 */

#include "VKL_acmp_tlkr_ctx.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static VKL_acmp_tlkr_ctx* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-46s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    } else {
        printf("  [ ok ] %-46s = 0x%llx\n", what, (unsigned long long)got);
    }
}

static const uint64_t ENTITY_ID  = 0x020000FFFE000001ULL;
static const uint64_t CTRL_ID    = 0x6805CA95B2D10055ULL;
static const uint64_t STATION    = 0x020000FFFE01ULL;      // 48-bit
static const uint16_t VID_BASE   = 2;                      // src k -> 2+k
static uint64_t src_dmac(int k) { return 0x91E0F000FE00ULL + k; }

static void lo() { dut->clk_i = 0; dut->eval(); }
static void hi() { dut->clk_i = 1; dut->eval(); }
static void step() { lo(); hi(); }
//! 1 s strobe + room for the N-context sweep pass (real spacing is 1 s;
//! the wheel finishes a pass in N+1 cycles)
static void tick() {
    dut->tick_1s_i = 1; step();
    dut->tick_1s_i = 0;
    for (int i = 0; i < 8; i++) step();
}

static void put_be(std::vector<uint8_t>& b, uint64_t v, int n) {
    for (int i = n - 1; i >= 0; i--) b.push_back((v >> (8 * i)) & 0xFF);
}

static std::vector<uint8_t> acmp_cmd(int msg, uint64_t talker, uint16_t tuid,
                                     uint16_t seq, uint16_t flags = 0) {
    std::vector<uint8_t> b;
    put_be(b, 0x91E0F0010000ULL, 6);
    put_be(b, CTRL_ID >> 16, 6);
    put_be(b, 0x22F0, 2);
    b.push_back(0xFC);
    b.push_back(msg & 0x0F);
    put_be(b, 44, 2);
    put_be(b, 0x1122334455667788ULL, 8);      // stream_id (controller junk)
    put_be(b, CTRL_ID, 8);
    put_be(b, talker, 8);
    put_be(b, 0xAABBCCDDEEFF0011ULL, 8);
    put_be(b, tuid, 2);
    put_be(b, 7, 2);
    put_be(b, 0x0EDC10000001ULL, 6);          // stream_dest_mac (junk)
    put_be(b, 3, 2);                          // connection_count (junk)
    put_be(b, seq, 2);
    put_be(b, flags, 2);
    put_be(b, 42, 2);                         // stream_vlan_id (junk)
    put_be(b, 0xBEEF, 2);
    return b;
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

static std::vector<uint8_t> collect(int maxc = 300) {
    std::vector<uint8_t> b;
    for (int c = 0; c < maxc; c++) {
        dut->m_axis_tready = 1;
        lo();
        if (dut->m_axis_tvalid) {
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_tkeep >> l) & 1)
                    b.push_back((dut->m_axis_tdata >> (8 * l)) & 0xFF);
            bool last = dut->m_axis_tlast;
            hi();
            if (last) return b;
        } else {
            hi();
        }
    }
    return b;
}

static uint64_t be(const std::vector<uint8_t>& b, int off, int n) {
    uint64_t v = 0; for (int i = 0; i < n; i++) v = (v << 8) | b[off + i];
    return v;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_acmp_tlkr_ctx;

    dut->rst_n = 0; dut->enable_i = 0; dut->m_axis_tready = 1;
    dut->station_mac_i = STATION; dut->entity_id_i = ENTITY_ID;
    // per-source stream params: dmac slices (192-bit wide port), vid (48-bit)
    for (int w = 0; w < 6; w++) dut->src_dmac_i[w] = 0;
    for (int k = 0; k < 4; k++) {
        uint64_t d = src_dmac(k);
        for (int i = 0; i < 48; i++) {
            int b = 48 * k + i;
            if ((d >> i) & 1) dut->src_dmac_i[b >> 5] |= (1u << (b & 31));
        }
    }
    { uint64_t v = 0;
      for (int k = 0; k < 4; k++) v |= (uint64_t)(VID_BASE + k) << (12 * k);
      dut->src_vid_i = v; }
    dut->tick_1s_i = 0; dut->listener_observed_i = 0;
    dut->rx_tvalid_i = 0; dut->rx_tdata_i = 0; dut->rx_tkeep_i = 0; dut->rx_tlast_i = 0;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1; dut->enable_i = 1;
    for (int i = 0; i < 2; i++) step();

    printf("== KL_acmp_tlkr_ctx N=4 (per-uid probe windows, one wheel) ==\n");

    // 1) GET_TX_STATE per uid: LIVE per-source stream params
    for (int uid = 0; uid < 4; uid++) {
        feed(acmp_cmd(4, ENTITY_ID, uid, 0x0100 + uid, 0x004A));
        auto r = collect();
        ck("[T1] frame length 70", r.size(), 70);
        if (r.size() == 70) {
            ck("[T1] status SUCCESS", r[16] >> 3, 0);
            ck("[T1] stream_id {mac,uid}", be(r, 18, 8), (STATION << 16) | uid);
            ck("[T1] dest_mac per source", be(r, 54, 6), src_dmac(uid));
            ck("[T1] vlan per source", be(r, 66, 2), VID_BASE + uid);
            ck("[T1] count 0", be(r, 60, 2), 0);
            ck("[T1] flags cleared", be(r, 64, 2), 0);
        }
    }
    ck("[T1] GET_TX_STATE arms nothing", dut->probe_armed_o, 0);

    // 2) uid 4 -> TALKER_UNKNOWN_ID, echo
    feed(acmp_cmd(4, ENTITY_ID, 4, 0x0200));
    auto r = collect();
    ck("[T2] uid4 TALKER_UNKNOWN_ID", r.size() == 70 ? (r[16] >> 3) : 0, 2);
    ck("[T2] uid4 stream_id echoed", be(r, 18, 8), 0x1122334455667788ULL);

    // 3) PROBE uid1 arms ONLY context 1
    feed(acmp_cmd(0, ENTITY_ID, 1, 0x0300));
    r = collect();
    ck("[T3] probe resp SUCCESS", r[16] >> 3, 0);
    ck("[T3] probe stream_id {mac,1}", be(r, 18, 8), (STATION << 16) | 1);
    ck("[T3] armed == bit1", dut->probe_armed_o, 0x2);
    ck("[T3] active == bit1", dut->talker_active_o, 0x2);

    // 4) staggered windows on ONE sweep: uid0 now, uid2 five ticks later
    feed(acmp_cmd(0, ENTITY_ID, 0, 0x0400));
    (void)collect();
    ck("[T4] armed bits {1,0}", dut->probe_armed_o, 0x3);
    for (int t = 0; t < 5; t++) tick();
    feed(acmp_cmd(0, ENTITY_ID, 2, 0x0401));
    (void)collect();
    ck("[T4] armed bits {2,1,0}", dut->probe_armed_o, 0x7);
    for (int t = 0; t < 10; t++) tick();       // uid0/1 at 15 ticks -> drop
    ck("[T4] uid0/uid1 expired, uid2 alive", dut->probe_armed_o, 0x4);
    for (int t = 0; t < 5; t++) tick();        // uid2 reaches 15
    ck("[T4] uid2 expired", dut->probe_armed_o, 0x0);
    ck("[T4] inactive", dut->talker_active_o, 0x0);

    // 5) listener_observed pins ONE context past expiry
    feed(acmp_cmd(0, ENTITY_ID, 2, 0x0500));
    (void)collect();
    dut->listener_observed_i = (1 << 2);
    for (int t = 0; t < 20; t++) tick();
    ck("[T5] ctx2 held by its listener", dut->probe_armed_o, 0x4);
    ck("[T5] active held", dut->talker_active_o, 0x4);
    dut->listener_observed_i = 0;
    tick();
    ck("[T5] released after the listener leaves", dut->probe_armed_o, 0x0);

    // 6) DISCONNECT_TX: SUCCESS, zeroed fields, NO state change (5.5.4.2)
    feed(acmp_cmd(0, ENTITY_ID, 3, 0x0600));
    (void)collect();
    feed(acmp_cmd(2, ENTITY_ID, 3, 0x0601, 0x004A));
    r = collect();
    ck("[T6] disc SUCCESS", r[16] >> 3, 0);
    ck("[T6] disc stream_id zeroed", be(r, 18, 8), 0);
    ck("[T6] disc does NOT disarm ctx3", dut->probe_armed_o, 0x8);

    // 7) GET_TX_CONNECTION -> NOT_SUPPORTED (5.5.4.4)
    feed(acmp_cmd(12, ENTITY_ID, 0, 0x0700));
    r = collect();
    ck("[T7] gtc NOT_SUPPORTED", r[16] >> 3, 31);

    printf("\nKL_acmp_tlkr_ctx N=4: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
