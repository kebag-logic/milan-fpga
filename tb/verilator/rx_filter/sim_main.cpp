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
    // A one-beat frame (tlast at SOF, at most 8 bytes) is never legal Ethernet;
    // the filter must swallow it even when the miss policy would otherwise pass.
    dut->default_pass_i = 1;
    ck("runt 1-beat frame swallowed", (long)send_frame(MAC_UNI, 1).size(), 0);
    ck("normal frame after runt passes", send_frame(MAC_UNI, 8).size() == 8 ? 1 : 0, 1);


    // ---- REQ-MAC-02: 802.3 station-address filter -----------------------
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

    // ======================================================================
    //  ARP REACHABILITY UNDER THE SHIPPING SHIELD
    //
    //  Provenance: a 2026-08-03 report of "after a cold boot the board is
    //  unreachable - ping 100% loss, ARP FAILED from the peer - until the
    //  BOARD transmits first" was RETRACTED the same day (a clean boot is
    //  reachable immediately and ARP resolves even after a cache flush).
    //  These checks are kept anyway, as the permanent regression guard that
    //  the retracted report showed we did not have: they encode WHY the
    //  filter could never have been the cause, so the next reachability
    //  scare can be pointed at the network instead of re-audited here.
    //
    //  This models EXACTLY what the driver installs. kl-eth.c kl_open():
    //      kl_wr_station_mac(kl, ndev->dev_addr);   // MAC_ADDR_LO then _HI
    //      kl_rx_shield_arm(kl);                    // TCAM idx 15, then
    //                                               // TCAM_CTRL[1] = 1
    //      kl_wr(CSR_MAC_CTRL, TX_EN | RX_EN | IS_1G);
    //  and kl_rx_shield_arm() programs ONE ternary DROP over the whole IEEE
    //  1722 MAAP space 91:E0:F0:00:xx:xx. Note the station MAC is written
    //  BEFORE the arm, and MAC RX is enabled only after both.
    //
    //  The three ARP shapes below are the desk half of that diagnosis: the
    //  filter CANNOT be the cause, because a broadcast ARP REQUEST is
    //  admitted on `dmac_bcast` (rx_mac_filter.sv:117) before the station
    //  compare is even consulted - so it passes whatever the station MAC
    //  holds. The negative control then proves the kl_open ordering is
    //  genuinely load-bearing for the UNICAST leg, and, decisively, that even
    //  the broken ordering still answers a broadcast ARP request.
    // ======================================================================
    printf("--------------------------------------------------------------\n");
    {
        const uint64_t MAC_PEER = 0x001BC50AC1FFULL;   // the pinging host
        (void)MAC_PEER;
        wr_tcam(0, 0, 0, 0, 0);                        // bare table
        dut->promisc_i = 0; dut->allmulti_i = 0; dut->mc_hash_i = 0;
        dut->default_pass_i = 1;                       // TCAM_CTRL reset 0x1
        dut->station_mac_i  = MAC_STATION;
        // kl_rx_shield_arm(): MAAP drop at index 15, then arm
        wr_tcam(15, 1, 0x91E0F0000000ULL, 0xFFFFFFFF0000ULL, 0x01);
        dut->addr_filter_en_i = 1;

        ck("arp: broadcast REQUEST passes (shield armed)",
           (long)send_frame(MAC_BCAST, 6).size(), 6);
        ck("arp: unicast REPLY to station MAC passes",
           (long)send_frame(MAC_STATION, 6).size(), 6);
        ck("arp: gratuitous ARP (broadcast) passes",
           (long)send_frame(MAC_BCAST, 8).size(), 8);
        // the shield itself must not shadow ARP: MAAP is 91:E0:F0:00:xx:xx,
        // ARP rides bcast/unicast, so the drop entry can never alias it
        ck("arp: shield still drops a MAAP stream group",
           (long)send_frame(MAC_MAAP, 6).size(), 0);

        // ---- NEGATIVE CONTROL: filter armed BEFORE the station MAC ----
        // If kl_open ever armed TCAM_CTRL[1] while MAC_ADDR_LO/HI still held
        // their reset value (milan_csr.sv:1088 mac_alo/mac_ahi <= 0), every
        // unicast to us would be blackholed. That is the failure mode this
        // ordering exists to prevent - and it is NOT the reported symptom,
        // because the broadcast leg below still passes.
        dut->station_mac_i = 0;                        // "arm before write"
        ck("arp NEG: zero station MAC blackholes our unicast",
           (long)send_frame(MAC_STATION, 6).size(), 0);
        ck("arp NEG: broadcast REQUEST STILL passes (shield exonerated)",
           (long)send_frame(MAC_BCAST, 6).size(), 6);
        dut->station_mac_i = MAC_STATION;
        ck("arp: unicast restored once the station MAC lands",
           (long)send_frame(MAC_STATION, 6).size(), 6);

        wr_tcam(15, 0, 0, 0, 0);
        dut->addr_filter_en_i = 0;
    }

    // ======================================================================
    //  STALLED FIRST BEAT - the verdict is LIVE until the first beat is
    //  ACCEPTED, not latched when it is first presented (review of PR #279).
    //
    //  These checks pin the observed sequence so the `//!` contract in
    //  rx_mac_filter.sv and the RTL are graded together: a first beat stalled
    //  on m_tready is re-judged by every TCAM and policy write that lands
    //  meanwhile, and a pass->drop flip withdraws m_tvalid without a transfer,
    //  which is the AXI4-Stream bend the contract names (ARM IHI 0051A 2.2.1).
    //  Changing that behaviour is a functional ticket of its own; when it
    //  lands, the "withdrawn" and "forced high" checks below are the ones that
    //  must be rewritten with it, on purpose and visibly.
    // ======================================================================
    printf("--------------------------------------------------------------\n");
    {
        wr_tcam(0, 0, 0, 0, 0);                        // bare table
        dut->default_pass_i = 1; dut->addr_filter_en_i = 0; dut->promisc_i = 0;

        // drive the rest of a 4-beat frame at full sink rate; return the
        // number of beats the sink saw
        auto drain_tail = [&]() {
            long out = 0;
            for (int b = 1; b < 4; b++) {
                dut->s_tdata = 0xC0FFEE0000000000ULL | (uint64_t)b;
                dut->s_tkeep = (b == 3) ? 0x3F : 0xFF; dut->s_tlast = (b == 3);
                dut->s_tvalid = 1; dut->m_tready = 1;
                lo(); if (dut->m_tvalid && dut->m_tready) out++;
                hi();
            }
            dut->s_tvalid = 0; dut->s_tlast = 0; step();
            return out;
        };
        // present the first beat of a frame that passes today, sink stalled
        auto offer_stalled_sof = [&]() {
            dut->s_tdata = beat0(MAC_UNI, 0xAB); dut->s_tkeep = 0xFF; dut->s_tlast = 0;
            dut->s_tvalid = 1; dut->m_tready = 0;
            lo();
        };

        // ---- (1) a TCAM drop entry lands while the first beat is stalled ----
        offer_stalled_sof();
        ck("sof stall: passing first beat offered (m_tvalid)", dut->m_tvalid, 1);
        ck("sof stall: sink stalled with the source (s_tready)", dut->s_tready, 0);
        ck("sof stall: not dropped before the write", dut->frame_dropped_o, 0);
        hi();                                          // edge: no handshake, nothing latched
        dut->tcam_wr_en_i = 1; dut->tcam_wr_index_i = 0; dut->tcam_wr_valid_i = 1;
        dut->tcam_wr_key_i = MAC_UNI; dut->tcam_wr_mask_i = MASK_ALL; dut->tcam_wr_action_i = 0x01;
        lo(); hi();                                    // the write commits on this edge
        dut->tcam_wr_en_i = 0;
        lo();
        ck("sof stall: TCAM write re-judges the stalled beat (frame_match_o)", dut->frame_match_o, 1);
        ck("sof stall: verdict flips to drop in flight", dut->frame_dropped_o, 1);
        ck("sof stall: m_tvalid withdrawn without a transfer (AXI4-Stream bend)", dut->m_tvalid, 0);
        ck("sof stall: dropped first beat consumed (s_tready forced high)", dut->s_tready, 1);
        hi();                                          // first beat accepted as DROPPED
        ck("sof stall: whole frame squashed after the flip", drain_tail(), 0);
        wr_tcam(0, 0, 0, 0, 0);

        // ---- (2) a policy write (default_pass 1->0) while stalled ----
        offer_stalled_sof();
        ck("sof stall/policy: passing first beat offered", dut->m_tvalid, 1);
        hi();
        dut->default_pass_i = 0;                       // the miss policy flips under the beat
        lo();
        ck("sof stall/policy: miss becomes a drop in flight", dut->frame_dropped_o, 1);
        ck("sof stall/policy: m_tvalid withdrawn without a transfer", dut->m_tvalid, 0);
        ck("sof stall/policy: dropped first beat consumed", dut->s_tready, 1);
        hi();
        ck("sof stall/policy: whole frame squashed", drain_tail(), 0);
        dut->default_pass_i = 1;

        // ---- (3) once the first beat is ACCEPTED the verdict is held ----
        dut->s_tdata = beat0(MAC_UNI, 0xAB); dut->s_tkeep = 0xFF; dut->s_tlast = 0;
        dut->s_tvalid = 1; dut->m_tready = 1;
        lo();
        ck("post-accept: first beat transfers", (dut->m_tvalid && dut->m_tready) ? 1 : 0, 1);
        hi();                                          // accepted: pass latched, in_frame
        dut->s_tvalid = 0;                             // the source pauses between beats
        wr_tcam(0, 1, 0, 0, 0x01);                     // mask 0 = drop EVERYTHING, live
        ck("post-accept: a drop-all entry does not touch the in-flight frame",
           drain_tail(), 3);
        ck("post-accept: the same entry drops the NEXT frame",
           (long)send_frame(MAC_UNI, 4).size(), 0);
        wr_tcam(0, 0, 0, 0, 0);
    }

    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
