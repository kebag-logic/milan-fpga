/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for rx_mac_filter.sv — the TCAM-driven RX
 * destination-MAC filter (REQ-MAC-02).
 *
 * Programs the TCAM via the write port, then streams frames whose destination
 * MAC sits in beat 0, and checks:
 *   - whitelist mode (default_pass=0): only frames whose dest MAC matches an
 *     accept entry are forwarded; misses are dropped (no output beats)
 *   - ternary/range accept (01-80-C2-00-00-0x)
 *   - blacklist mode (default_pass=1): a drop entry (action[0]=1) drops its MAC,
 *     everything else passes
 *   - passed frames come out byte-exact (cut-through, no corruption)
 *   - REQ-MAC-02 station address filter: promiscuous, exact-match unicast,
 *     broadcast, allmulti, the 64-bucket multicast hash, and the interaction
 *     with the TCAM (hit wins over the address filter, promisc wins over both)
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vrx_mac_filter.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vrx_mac_filter* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-32s got=%ld exp=%ld\n", what, got, exp); }
}

static void lo() { dut->clk_i = 0; dut->eval(); }
static void hi() { dut->clk_i = 1; dut->eval(); }
static void step() { lo(); hi(); }

static void wr_tcam(int idx, int valid, uint64_t key, uint64_t mask, int action) {
    dut->tcam_wr_en_i = 1; dut->tcam_wr_index_i = idx; dut->tcam_wr_valid_i = valid;
    dut->tcam_wr_key_i = key; dut->tcam_wr_mask_i = mask; dut->tcam_wr_action_i = action;
    step();
    dut->tcam_wr_en_i = 0; step();
}

// build beat 0 with dest MAC (MSB-first) in byte lanes 0..5 + a marker in 6..7
static uint64_t beat0(uint64_t mac, uint8_t marker) {
    uint64_t v = 0;
    for (int i = 0; i < 6; i++) v |= (uint64_t)((mac >> (40 - 8 * i)) & 0xFF) << (8 * i);
    v |= (uint64_t)marker << 48;
    return v;
}

// send a frame to `mac`; return the collected output beats (empty = dropped)
static std::vector<uint64_t> send_frame(uint64_t mac, int len) {
    std::vector<uint64_t> beats, got;
    beats.push_back(beat0(mac, 0xAB));
    for (int b = 1; b < len; b++) beats.push_back(0xC0FFEE0000000000ULL | (uint64_t)b);
    size_t bi = 0;
    for (int c = 0; c < 3000 && bi < beats.size(); c++) {
        dut->s_tdata = beats[bi];
        dut->s_tkeep = (bi == beats.size() - 1) ? 0x3F : 0xFF;
        dut->s_tlast = (bi == beats.size() - 1);
        dut->s_tvalid = 1; dut->m_tready = 1;
        lo();
        if (dut->m_tvalid && dut->m_tready) got.push_back(dut->m_tdata);
        bool acc = dut->s_tvalid && dut->s_tready;
        hi();
        if (acc) bi++;
    }
    dut->s_tvalid = 0; step();
    // integrity: a forwarded frame must match the input beats exactly
    if (!got.empty()) {
        bool eq = got.size() == beats.size();
        for (size_t i = 0; eq && i < got.size(); i++) eq = (got[i] == beats[i]);
        ck("forwarded frame byte-exact", eq ? 1 : 0, 1);
    }
    return got;
}

static const uint64_t MAC_GPTP   = 0x0180C200000EULL;
static const uint64_t MAC_AVDECC = 0x91E0F0010000ULL;
static const uint64_t MAC_RESVK  = 0x0180C2000000ULL, MAC_RESVM = 0xFFFFFFFFFFF0ULL;
static const uint64_t MAC_BCAST  = 0xFFFFFFFFFFFFULL, MASK_ALL  = 0xFFFFFFFFFFFFULL;
static const uint64_t MAC_UNI    = 0xAABBCCDDEEFFULL;

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vrx_mac_filter;

    dut->rst_n = 0; dut->s_tvalid = 0; dut->s_tlast = 0; dut->m_tready = 1;
    dut->tcam_wr_en_i = 0; dut->default_pass_i = 0;
    dut->addr_filter_en_i = 0; dut->promisc_i = 0; dut->allmulti_i = 0;
    dut->station_mac_i = 0; dut->mc_hash_i = 0;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1; step();

    printf("== rx_mac_filter harness ==\n");

    // ---- whitelist mode: default_pass=0, accept only listed groups ----
    dut->default_pass_i = 0;
    wr_tcam(0, 1, MAC_GPTP,   MASK_ALL,  0x00);   // accept gPTP
    wr_tcam(1, 1, MAC_AVDECC, MASK_ALL,  0x00);   // accept AVDECC
    wr_tcam(2, 1, MAC_RESVK,  MAC_RESVM, 0x00);   // accept reserved range

    ck("whitelist: gPTP passes",       (long)send_frame(MAC_GPTP, 4).size(),   4);
    ck("whitelist: AVDECC passes",     (long)send_frame(MAC_AVDECC, 5).size(), 5);
    ck("whitelist: range 0x passes",   (long)send_frame(0x0180C2000007ULL, 4).size(), 4); // 01-80-C2-00-00-07 in range
    ck("whitelist: out-of-range drop", (long)send_frame(0x0180C20000A3ULL, 4).size(), 0); // high nibble A -> mask F0 excludes it
    ck("whitelist: unicast dropped",   (long)send_frame(MAC_UNI, 4).size(),    0);
    ck("whitelist: bcast dropped",     (long)send_frame(MAC_BCAST, 4).size(),  0);

    // ---- blacklist mode: default_pass=1, drop a specific group ----
    wr_tcam(0, 0, 0, 0, 0);            // remove gPTP accept
    wr_tcam(1, 0, 0, 0, 0);            // remove AVDECC accept
    wr_tcam(2, 0, 0, 0, 0);            // remove range accept
    dut->default_pass_i = 1;
    wr_tcam(0, 1, MAC_BCAST, MASK_ALL, 0x01);   // action[0]=1 => drop broadcast

    ck("blacklist: bcast dropped",  (long)send_frame(MAC_BCAST, 4).size(), 0);
    ck("blacklist: unicast passes", (long)send_frame(MAC_UNI, 4).size(),   4);
    ck("blacklist: gPTP passes",    (long)send_frame(MAC_GPTP, 4).size(),  4);

    printf("--------------------------------------------------------------\n");
    // runt guard (2026-07-19): a 1-beat frame (tlast at SOF, <=8 bytes) is
    // never a legal Ethernet frame - swallowed even in default-pass mode
    dut->default_pass_i = 1;
    ck("runt 1-beat frame swallowed", (long)send_frame(MAC_UNI, 1).size(), 0);
    ck("normal frame after runt passes", send_frame(MAC_UNI, 8).size() == 8 ? 1 : 0, 1);


    // ======================================================================
    //  REQ-MAC-02 - 802.3 station address filter (the CSR ABI has advertised
    //  promisc/allmulti/MAC_ADDR/MC_HASH since 2026-07-01; nothing in fabric
    //  consumed them, so non-matching unicast was NEVER dropped in hardware).
    // ======================================================================
    // reference hash: 6-bit XOR fold of the 48-bit address, MSB-aligned
    auto mc_bucket = [](uint64_t mac) {
        int h = 0;
        for (int g = 0; g < 8; g++) h ^= (int)((mac >> (42 - 6 * g)) & 0x3F);
        return h;
    };
    const uint64_t MAC_STATION = 0x001BC50AC100ULL;   // our unicast
    const uint64_t MAC_OTHER   = 0x001BC50AC101ULL;   // one bit off - foreign
    const uint64_t MAC_MAAP    = 0x91E0F000FE00ULL;   // a MAAP-allocated group

    // clear the blacklist entry left over above, back to a bare table
    wr_tcam(0, 0, 0, 0, 0);
    dut->default_pass_i = 1;    // legacy blanket accept still the miss policy
    dut->station_mac_i  = MAC_STATION;

    // ---- disarmed: reset behaviour must be bit-identical to before ----
    dut->addr_filter_en_i = 0;
    ck("mac02 disarmed: foreign unicast passes", (long)send_frame(MAC_OTHER, 4).size(), 4);

    // ---- armed: exact-match unicast, everything else off ----
    dut->addr_filter_en_i = 1;
    ck("mac02 station unicast passes",   (long)send_frame(MAC_STATION, 4).size(), 4);
    ck("mac02 foreign unicast DROPPED",  (long)send_frame(MAC_OTHER, 4).size(),   0);
    ck("mac02 broadcast passes",         (long)send_frame(MAC_BCAST, 4).size(),   4);
    ck("mac02 multicast dropped (no hash, no allmulti)",
                                         (long)send_frame(MAC_GPTP, 4).size(),    0);

    // ---- allmulti: every group address, station unicast still exact ----
    dut->allmulti_i = 1;
    ck("mac02 allmulti: gPTP mcast passes",   (long)send_frame(MAC_GPTP, 4).size(),   4);
    ck("mac02 allmulti: MAAP group passes",   (long)send_frame(MAC_MAAP, 4).size(),   4);
    ck("mac02 allmulti: foreign unicast STILL dropped",
                                              (long)send_frame(MAC_OTHER, 4).size(),  0);
    dut->allmulti_i = 0;

    // ---- multicast hash: only the programmed buckets pass ----
    {
        int bg = mc_bucket(MAC_GPTP);
        // pins the worked example in docs/reference/REGISTER_MAP.md 0x114 so the
        // documented fold and the driver's copy of it cannot drift apart
        ck("mac02 hash: 01-80-C2-00-00-0E -> bucket 23 (REGISTER_MAP)", bg, 23);
        dut->mc_hash_i = 1ULL << bg;
        ck("mac02 hash: programmed bucket passes", (long)send_frame(MAC_GPTP, 4).size(), 4);
        // a group whose bucket is NOT set must drop (pick one that differs)
        uint64_t other_grp = MAC_MAAP;
        if (mc_bucket(other_grp) == bg) other_grp = 0x91E0F000FE01ULL;
        ck("mac02 hash: unprogrammed bucket DROPPED",
           (long)send_frame(other_grp, 4).size(), 0);
        // and setting its bucket lets it through - proves the index is the
        // documented fold and not an accident of one address
        dut->mc_hash_i = (1ULL << bg) | (1ULL << mc_bucket(other_grp));
        ck("mac02 hash: second bucket added passes",
           (long)send_frame(other_grp, 4).size(), 4);
        ck("mac02 hash: unicast unaffected by hash bits",
           (long)send_frame(MAC_OTHER, 4).size(), 0);
        dut->mc_hash_i = 0;
    }

    // ---- TCAM still overrides the address filter both ways ----
    wr_tcam(3, 1, MAC_OTHER, MASK_ALL, 0x00);       // accept a foreign unicast
    ck("mac02 TCAM accept beats the address filter",
       (long)send_frame(MAC_OTHER, 4).size(), 4);
    wr_tcam(4, 1, MAC_STATION, MASK_ALL, 0x01);     // drop OUR OWN address
    ck("mac02 TCAM drop beats the address filter",
       (long)send_frame(MAC_STATION, 4).size(), 0);

    // ---- promiscuous outranks everything except the runt guard ----
    dut->promisc_i = 1;
    ck("mac02 promisc: foreign unicast passes",  (long)send_frame(MAC_OTHER, 4).size(),   4);
    ck("mac02 promisc: TCAM-dropped MAC passes", (long)send_frame(MAC_STATION, 4).size(), 4);
    ck("mac02 promisc: random group passes",     (long)send_frame(MAC_MAAP, 4).size(),    4);
    ck("mac02 promisc: runt STILL swallowed",    (long)send_frame(MAC_OTHER, 1).size(),   0);
    dut->promisc_i = 0;

    // ---- disarming restores the legacy miss policy exactly ----
    wr_tcam(3, 0, 0, 0, 0); wr_tcam(4, 0, 0, 0, 0);
    dut->addr_filter_en_i = 0;
    ck("mac02 re-disarmed: foreign unicast passes again",
       (long)send_frame(MAC_OTHER, 4).size(), 4);
    dut->default_pass_i = 0;
    ck("mac02 re-disarmed + whitelist: foreign unicast dropped",
       (long)send_frame(MAC_OTHER, 4).size(), 0);
    dut->default_pass_i = 1;

    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
