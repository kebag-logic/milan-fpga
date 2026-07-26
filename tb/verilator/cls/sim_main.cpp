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
 * default map, the untagged default-priority path, legacy classification, and
 * the reserved-DMAC validation of the gPTP fast path (REQ-CLS-07).
 *
 * traffic_class_map is pure combinational (no FIFO/primitive), so it Verilates
 * with no Xilinx tools. Exit 0 = pass, non-zero = fail.
 */

#include "Vtraffic_class_map.h"
#include "verilated.h"

#include <cstdio>
#include <cstdint>
#include <random>

static const int NQ = 6;
static const int TDEST_W = 3;   // ceil(log2 NQ); CLS_TC_QUEUE_MAP packs TDEST_W bits/entry
static const int TDEST_MASK = (1 << TDEST_W) - 1;

// EtherType constants (match ethernet_packet_pkg.sv)
static const uint16_t ETH_TYPE_PTP  = 0x88F7;
static const uint16_t ETH_TYPE_AVTP = 0x22F0;

// Enum ordering (ethernet_packet_pkg.sv network_priority_t). 802.1Q order:
// the value IS the queue index and the HIGHER index is the HIGHER priority.
enum { BEST_EFFORT = 0, RESERVED_CLASS = 1, CONTROL_CLASS = 2,
       GPTP_CLASS = 3, SRB_CLASS = 4, SRA_CLASS = 5 };

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
    bool     dmac_check = false;  // REQ-CLS-07: validate the reserved gPTP DMAC
    bool     dmac_gptp  = true;   // frame DMAC == 01-80-C2-00-00-0E
};

// Reference classification (independent of the RTL).
static uint32_t ref_tdest(const Frame& f) {
    // REQ-CLS-07: with dmac_check on, the fast path also demands the reserved
    // 802.1AS multicast; a spoofed 0x88F7 falls through to the ordinary paths.
    const bool gptp = (f.eth_type == ETH_TYPE_PTP) && (!f.dmac_check || f.dmac_gptp);
    if (f.use_pcp) {
        // gPTP fast-path (2026-07-13): 0x88F7 short-circuits to GPTP_CLASS in
        // BOTH modes — PCP-mode tables no longer decide event-message routing
        if (gptp) return GPTP_CLASS & TDEST_MASK;
        uint8_t eff_pcp = f.vlan_valid ? f.pcp : f.default_pcp;
        uint8_t regen   = (f.prio_regen   >> (eff_pcp * 3)) & 0x7;
        uint8_t tc      = (f.pcp_tc_map   >> (regen   * 3)) & 0x7;
        // TC->queue: TDEST_W bits per entry (matches the ABI / RTL bit-slice)
        uint8_t queue   = (f.tc_queue_map >> (tc * TDEST_W)) & TDEST_MASK;
        // OUT-OF-RANGE CLAMP: at NQ=6 the 3-bit field can name q6/q7, which do
        // not exist; traffic_class_map falls back to BEST_EFFORT rather than
        // letting axis_demux silently drop the frame (`select >= M_COUNT`).
        if (queue >= NQ) queue = BEST_EFFORT;
        return queue;
    } else {
        int p;
        if (gptp)                                              p = GPTP_CLASS;
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
        dut->dmac_check_i   = f.dmac_check;
        dut->dmac_gptp_i    = f.dmac_gptp;
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
                printf("  [FAIL] %-14s got=%u exp=%u (use_pcp=%d vlan=%d pcp=%u eth=%04X "
                       "dchk=%d dgptp=%d)\n",
                       tag, got, exp, f.use_pcp, f.vlan_valid, f.pcp, f.eth_type,
                       f.dmac_check, f.dmac_gptp);
            fails++;
        }
    }
};

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Vtraffic_class_map* dut = new Vtraffic_class_map;
    Harness h(dut);

    printf("== traffic_class_map classification harness (NQ=%d) ==\n", NQ);

    // milan_csr reset defaults (docs/reference/REGISTER_MAP.md)
    const uint32_t DEF_PCP_TC = 0x00FAC688;
    const uint32_t DEF_REGEN  = 0x00FAC688;   // identity (reset fixed 2026-07-05)
    // milan_csr reset CLS_TC_QUEUE_MAP for the 6-queue map: 3 bits/entry,
    // TC0/1 -> q0, TC2 -> q4 (SR class B), TC3 -> q5 (SR class A),
    // TC4/5 -> q2 (control), TC6/7 -> q3 (gPTP). q1 is the reserved spare.
    const uint32_t DEF_TCQ    = 0x006D2B00;
    const int      DEF_TCQ_Q[8] = {0, 0, 4, 5, 2, 2, 3, 3};

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

    // ---- Directed 1b: the 6-queue reset CLS_TC_QUEUE_MAP, entry by entry ----
    // Locks the ABI intent (TDEST_W bits/entry) so a wrong field width regresses,
    // AND locks the USER's egress map: SR class A on q5, class B on q4, control
    // on q2, gPTP on q3, best effort on q0, nothing on the reserved q1.
    {
        long f0 = h.fails;
        // identity PCP->TC (DEF via prio_regen+pcp_tc), so route a tagged frame
        // whose regenerated TC is exactly t, and confirm queue == DEF_TCQ_Q[t].
        uint32_t ident24 = 0; for (int i=0;i<8;i++) ident24 |= (uint32_t)i << (3*i);
        for (int tc = 0; tc < 8; tc++) {
            Frame f{true, 0, ident24, ident24, DEF_TCQ, true, (uint8_t)tc, false, 0x0800};
            uint32_t q = h.eval(f);
            if (q != (uint32_t)DEF_TCQ_Q[tc]) {
                printf("  [FAIL] reset TCQ: TC%d -> q%u (expect q%d)\n", tc, q, DEF_TCQ_Q[tc]);
                h.fails++;
            }
            if (q == 1) { printf("  [FAIL] reset TCQ: TC%d landed on the RESERVED q1\n", tc); h.fails++; }
            h.check(f, "tcq_reset_map");
        }
        printf("  [%s] reset CLS_TC_QUEUE_MAP 0x006D2B00 = the 6-queue map "
               "(TC3->q5 class A, TC2->q4 class B, TC4/5->q2, TC6/7->q3, rest q0)\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 1c: 802.1Q ORDER - the enum value IS the queue index and a
    // higher index is a higher priority. Pins SRA above SRB above gPTP above
    // control above the spare above best effort, which is what makes the
    // arbiter in traffic_shaping_core grant audio before sync.
    {
        long f0 = h.fails;
        bool ok = (SRA_CLASS == 5) && (SRB_CLASS == 4) && (GPTP_CLASS == 3) &&
                  (CONTROL_CLASS == 2) && (RESERVED_CLASS == 1) && (BEST_EFFORT == 0);
        // and the DUT agrees: legacy-mode VLAN AVTP -> q5, gPTP -> q3, IP -> q0
        Frame avtp{false, 0, 0, 0, 0, true,  0, false, ETH_TYPE_AVTP};
        Frame ptp {false, 0, 0, 0, 0, false, 0, false, ETH_TYPE_PTP};
        Frame be  {false, 0, 0, 0, 0, false, 0, false, 0x0800};
        uint32_t qa = h.eval(avtp), qp = h.eval(ptp), qb = h.eval(be);
        if (!(qa == 5 && qp == 3 && qb == 0)) {
            printf("  [FAIL] 802.1Q order: AVTP q%u (want 5), gPTP q%u (want 3), BE q%u (want 0)\n",
                   qa, qp, qb);
            h.fails++;
        }
        if (!(qa > qp && qp > qb)) {
            printf("  [FAIL] 802.1Q order: shaped class A must outrank gPTP must outrank BE\n");
            h.fails++;
        }
        if (!ok) { printf("  [FAIL] network_priority_t values are not the queue indices\n"); h.fails++; }
        printf("  [%s] 802.1Q order: q5 SR-A > q4 SR-B > q3 gPTP > q2 control > q1 spare > q0 BE\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 1d: an out-of-range programmed queue is CLAMPED to best
    // effort, not handed to the demux (which would silently drop the frame).
    // Only reachable because 6 is not a power of two: the 3-bit field can name
    // q6/q7. NEGATIVE-by-construction - without the clamp the DUT returns 6/7.
    {
        long f0 = h.fails;
        uint32_t ident24 = 0; for (int i=0;i<8;i++) ident24 |= (uint32_t)i << (3*i);
        for (int bad = NQ; bad < 8; bad++) {
            // map every traffic class to `bad`
            uint32_t tcq = 0; for (int i=0;i<8;i++) tcq |= (uint32_t)bad << (TDEST_W*i);
            Frame f{true, 0, ident24, ident24, tcq, true, 3, false, 0x0800};
            uint32_t q = h.eval(f);
            h.check(f, "tcq_out_of_range");
            if (q != (uint32_t)BEST_EFFORT) {
                printf("  [FAIL] out-of-range queue %d not clamped: tdest=q%u\n", bad, q);
                h.fails++;
            }
        }
        printf("  [%s] CLS_TC_QUEUE_MAP entries >= NUMBER_OF_QUEUES clamp to BEST_EFFORT\n",
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

    // ---- Directed 4: reserved-DMAC validation of the gPTP fast path (REQ-CLS-07) ----
    // 802.1AS-2020 s10.5: gPTP rides the reserved multicast 01-80-C2-00-00-0E.
    // The fast path hands 0x88F7 the second-highest queue, so with dmac_check
    // on it must ALSO see that DMAC. Negative leg (the reject must be honest):
    // a spoofed 0x88F7 at a foreign DMAC must NOT reach GPTP_CLASS - it lands
    // on the ordinary table queue (PCP mode) / BEST_EFFORT (legacy mode).
    {
        long f0 = h.fails;
        uint32_t ident24 = 0; for (int i = 0; i < 8; i++) ident24 |= (uint32_t)i << (3 * i);

        // 4a: check OFF - a foreign-DMAC 0x88F7 still takes the fast path
        //     (today's silicon behaviour must be bit-identical at reset)
        Frame off{true, 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, false, 0, false, ETH_TYPE_PTP,
                  /*dmac_check=*/false, /*dmac_gptp=*/false};
        h.check(off, "cls07_off");
        if (h.eval(off) != (GPTP_CLASS & TDEST_MASK)) {
            printf("  [FAIL] cls07: dmac_check=0 must preserve the legacy fast path\n"); h.fails++;
        }

        // 4b: check ON + right DMAC -> still GPTP_CLASS, in both modes
        for (int mode = 0; mode < 2; mode++) {
            Frame ok{(bool)mode, 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, false, 0, false,
                     ETH_TYPE_PTP, true, true};
            h.check(ok, "cls07_ok");
            if (h.eval(ok) != (GPTP_CLASS & TDEST_MASK)) {
                printf("  [FAIL] cls07: reserved DMAC rejected (use_pcp=%d)\n", mode); h.fails++;
            }
        }

        // 4c: NEGATIVE - check ON + foreign DMAC -> must lose the fast path.
        //     PCP mode: untagged, so default_pcp picks the table queue. Use
        //     default_pcp 0, which the reset map sends to q0 (best effort) -
        //     provably NOT GPTP_CLASS (q3).
        {
            Frame spoof{true, 0, ident24, ident24, DEF_TCQ, false, 0, false,
                        ETH_TYPE_PTP, true, false};
            uint32_t q = h.eval(spoof);
            h.check(spoof, "cls07_spoof_pcp");
            if (q == (GPTP_CLASS & TDEST_MASK)) {
                printf("  [FAIL] cls07 NEGATIVE: spoofed 0x88F7 still took GPTP_CLASS (q%u)\n", q);
                h.fails++;
            }
            if (q != (uint32_t)DEF_TCQ_Q[0]) {
                printf("  [FAIL] cls07 NEGATIVE: spoof landed q%u, want the table queue %d\n",
                       q, DEF_TCQ_Q[0]);
                h.fails++;
            }
        }
        // 4d: NEGATIVE, legacy mode -> BEST_EFFORT, not GPTP_CLASS
        {
            Frame spoof{false, 0, 0, 0, 0, false, 0, false, ETH_TYPE_PTP, true, false};
            uint32_t q = h.eval(spoof);
            h.check(spoof, "cls07_spoof_legacy");
            if (q != (BEST_EFFORT & TDEST_MASK)) {
                printf("  [FAIL] cls07 NEGATIVE legacy: spoof landed q%u, want BEST_EFFORT\n", q);
                h.fails++;
            }
        }
        // 4e: the check must not touch non-PTP frames at all
        for (int dg = 0; dg < 2; dg++) {
            Frame avtp{false, 0, 0, 0, 0, true, 0, false, ETH_TYPE_AVTP, true, (bool)dg};
            h.check(avtp, "cls07_avtp_untouched");
            if (h.eval(avtp) != (SRA_CLASS & TDEST_MASK)) {
                printf("  [FAIL] cls07: AVTP classification moved with dmac_gptp=%d\n", dg); h.fails++;
            }
        }
        printf("  [%s] reserved-DMAC validation gates the gPTP fast path (REQ-CLS-07)\n",
               (h.fails == f0) ? "PASS" : "FAIL");
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
            f.dmac_check   = b(rng);
            f.dmac_gptp    = b(rng);
            f.eth_type     = etypes[ei(rng)];
            h.check(f, "random");
        }
        printf("  [%s] randomized 200000 configs/frames (incl. dmac_check) match reference\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", h.checks, h.fails);
    printf("RESULT: %s\n", (h.fails == 0) ? "PASS" : "FAIL");

    dut->final();
    delete dut;
    return (h.fails == 0) ? 0 : 1;
}
