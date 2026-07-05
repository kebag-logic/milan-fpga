/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for traffic_class_map.sv — the runtime
 * 802.1Q priority-to-queue classification (REQ-CLS-01..04, REQ-VER-03).
 *
 * An independent C++ model of the PCP -> regen -> traffic-class -> queue
 * pipeline (and the legacy EtherType fallback) must match the DUT for a large
 * random sweep of configs and frames, plus directed checks for the Table-8-5
 * default map, the untagged default-priority path, and legacy classification.
 *
 * traffic_class_map is pure combinational (no FIFO/primitive), so it Verilates
 * with no Xilinx tools. Exit 0 = pass, non-zero = fail.
 */

#include "Vtraffic_class_map.h"
#include "verilated.h"

#include <cstdio>
#include <cstdint>
#include <random>

static const int NQ = 4;
static const int TDEST_MASK = NQ - 1;
static const int TDEST_W = 2;   // ceil(log2 NQ); CLS_TC_QUEUE_MAP packs TDEST_W bits/entry

// EtherType constants (match ethernet_packet_pkg.sv)
static const uint16_t ETH_TYPE_PTP  = 0x88F7;
static const uint16_t ETH_TYPE_AVTP = 0x22F0;

// Legacy enum ordering (ethernet_packet_pkg.sv network_priority_t)
enum { SRA_CLASS = 0, GPTP_CLASS = 1, CONTROL_CLASS = 2, BEST_EFFORT = 3 };

struct Frame {
    bool     use_pcp;
    uint8_t  default_pcp;   // 3 bits
    uint32_t pcp_tc_map;    // 24 bits
    uint32_t prio_regen;    // 24 bits
    uint32_t tc_queue_map;  // 32 bits
    bool     vlan_valid;
    uint8_t  pcp;           // 3 bits
    bool     dei;
    uint16_t eth_type;
};

// Reference classification (independent of the RTL).
static uint32_t ref_tdest(const Frame& f) {
    if (f.use_pcp) {
        uint8_t eff_pcp = f.vlan_valid ? f.pcp : f.default_pcp;
        uint8_t regen   = (f.prio_regen   >> (eff_pcp * 3)) & 0x7;
        uint8_t tc      = (f.pcp_tc_map   >> (regen   * 3)) & 0x7;
        // TC->queue: TDEST_W bits per entry (matches the ABI / RTL bit-slice)
        uint8_t queue   = (f.tc_queue_map >> (tc * TDEST_W)) & TDEST_MASK;
        return queue;
    } else {
        int p;
        if (f.eth_type == ETH_TYPE_PTP)                        p = GPTP_CLASS;
        else if (f.vlan_valid && f.eth_type == ETH_TYPE_AVTP)  p = SRA_CLASS;
        else if (!f.vlan_valid && f.eth_type == ETH_TYPE_AVTP) p = CONTROL_CLASS;
        else                                                   p = BEST_EFFORT;
        return p & TDEST_MASK;
    }
}

struct Harness {
    Vtraffic_class_map* dut;
    long checks = 0, fails = 0;
    explicit Harness(Vtraffic_class_map* d) : dut(d) {}

    uint32_t eval(const Frame& f) {
        dut->use_pcp_i      = f.use_pcp;
        dut->default_pcp_i  = f.default_pcp;
        dut->pcp_tc_map_i   = f.pcp_tc_map;
        dut->prio_regen_i   = f.prio_regen;
        dut->tc_queue_map_i = f.tc_queue_map;
        dut->vlan_valid_i   = f.vlan_valid;
        dut->pcp_i          = f.pcp;
        dut->dei_i          = f.dei;
        dut->eth_type_i     = f.eth_type;
        dut->eval();
        return dut->tdest_o & 0xFF;
    }

    void check(const Frame& f, const char* tag) {
        uint32_t got = eval(f);
        uint32_t exp = ref_tdest(f);
        checks++;
        if (got != exp) {
            if (fails < 20)
                printf("  [FAIL] %-14s got=%u exp=%u (use_pcp=%d vlan=%d pcp=%u eth=%04X)\n",
                       tag, got, exp, f.use_pcp, f.vlan_valid, f.pcp, f.eth_type);
            fails++;
        }
    }
};

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Vtraffic_class_map* dut = new Vtraffic_class_map;
    Harness h(dut);

    printf("== traffic_class_map classification harness (NQ=%d) ==\n", NQ);

    // milan_csr reset defaults (docs/REGISTER_MAP.md)
    const uint32_t DEF_PCP_TC = 0x00FAC688;
    const uint32_t DEF_REGEN  = 0x00FAC688;   // identity (reset fixed 2026-07-05)
    const uint32_t DEF_TCQ    = 0x000000E4;   // identity 3,2,1,0

    // ---- Directed 1: tagged frames through the default Table-8-5 map ----
    {
        long f0 = h.fails;
        for (int pcp = 0; pcp < 8; pcp++) {
            Frame f{true, 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, true, (uint8_t)pcp, false, 0x0800};
            h.check(f, "tagged_default");
        }
        printf("  [%s] tagged frames PCP 0..7 classify per default table\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 1b: default CLS_TC_QUEUE_MAP (0xE4) is the identity 3,2,1,0 ----
    // Locks the ABI intent (TDEST_W bits/entry) so a wrong field width regresses.
    {
        long f0 = h.fails;
        // identity PCP->TC (DEF via prio_regen+pcp_tc), so route a tagged frame
        // whose regenerated TC is exactly t, and confirm queue == t.
        // Build a config: use_pcp, regen=identity, pcp_tc=identity, tcq=0xE4.
        uint32_t ident24 = 0; for (int i=0;i<8;i++) ident24 |= (uint32_t)i << (3*i);
        for (int tc = 0; tc < 4; tc++) {
            Frame f{true, 0, ident24, ident24, DEF_TCQ, true, (uint8_t)tc, false, 0x0800};
            uint32_t q = h.eval(f);
            if (q != (uint32_t)tc) { printf("  [FAIL] default TCQ identity: TC%d -> q%u (expect %d)\n", tc, q, tc); h.fails++; }
            h.check(f, "tcq_identity");
        }
        printf("  [%s] default CLS_TC_QUEUE_MAP 0xE4 = identity 3,2,1,0\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 2: untagged frame uses the default port priority ----
    {
        long f0 = h.fails;
        for (int dp = 0; dp < 8; dp++) {
            Frame tagged  {true, (uint8_t)dp, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, true,  (uint8_t)dp, false, 0x0800};
            Frame untagged{true, (uint8_t)dp, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, false, 0,           false, 0x0800};
            uint32_t qt = h.eval(tagged);
            uint32_t qu = h.eval(untagged);
            h.check(untagged, "untagged_default");
            if (qt != qu) { printf("  [FAIL] untagged(default_pcp=%d)=%u != tagged(pcp=%d)=%u\n", dp, qu, dp, qt); h.fails++; }
        }
        printf("  [%s] untagged frame classified by default port priority (REQ-CLS-03)\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 3: legacy EtherType fallback (use_pcp=0) ----
    {
        long f0 = h.fails;
        Frame ptp   {false, 0, 0, 0, 0, false, 0, false, ETH_TYPE_PTP};
        Frame avtp_v{false, 0, 0, 0, 0, true,  0, false, ETH_TYPE_AVTP};
        Frame avtp_u{false, 0, 0, 0, 0, false, 0, false, ETH_TYPE_AVTP};
        Frame be    {false, 0, 0, 0, 0, false, 0, false, 0x0800};
        h.check(ptp, "legacy_ptp");
        h.check(avtp_v, "legacy_avtp_vlan");
        h.check(avtp_u, "legacy_avtp_novlan");
        h.check(be, "legacy_be");
        bool ok = (h.eval(ptp)==(GPTP_CLASS&TDEST_MASK)) &&
                  (h.eval(avtp_v)==(SRA_CLASS&TDEST_MASK)) &&
                  (h.eval(avtp_u)==(CONTROL_CLASS&TDEST_MASK)) &&
                  (h.eval(be)==(BEST_EFFORT&TDEST_MASK));
        printf("  [%s] legacy EtherType fallback (gPTP/SR-A/control/BE) preserved\n",
               (ok && h.fails == f0) ? "PASS" : "FAIL");
        if (!ok) h.fails++;
    }

    // ---- Randomized sweep: DUT must match the reference for any config ----
    {
        long f0 = h.fails;
        std::mt19937 rng(0xC1A551F1);
        std::uniform_int_distribution<uint32_t> u24(0, 0xFFFFFF);
        std::uniform_int_distribution<uint32_t> u32(0, 0xFFFFFFFF);
        std::uniform_int_distribution<int> b(0, 1);
        std::uniform_int_distribution<int> p3(0, 7);
        const uint16_t etypes[] = {ETH_TYPE_PTP, ETH_TYPE_AVTP, 0x0800, 0x86DD, 0x8100};
        std::uniform_int_distribution<int> ei(0, 4);
        for (int i = 0; i < 200000; i++) {
            Frame f;
            f.use_pcp      = b(rng);
            f.default_pcp  = p3(rng);
            f.pcp_tc_map   = u24(rng);
            f.prio_regen   = u24(rng);
            f.tc_queue_map = u32(rng);
            f.vlan_valid   = b(rng);
            f.pcp          = p3(rng);
            f.dei          = b(rng);
            f.eth_type     = etypes[ei(rng)];
            h.check(f, "random");
        }
        printf("  [%s] randomized 200000 configs/frames match reference\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", h.checks, h.fails);
    printf("RESULT: %s\n", (h.fails == 0) ? "PASS" : "FAIL");

    dut->final();
    delete dut;
    return (h.fails == 0) ? 0 : 1;
}
