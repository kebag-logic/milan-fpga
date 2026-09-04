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
 * default map, the untagged default-priority path, legacy classification, the
 * reserved-DMAC validation of the gPTP fast path (REQ-CLS-07) and the
 * DMAC-keyed control fast path (REQ-CLS-10) that makes the q1 CONTROL_CLASS
 * row of docs/reference/EGRESS_QUEUE_MAP.md true on the wire.
 *
 * traffic_class_map is pure combinational (no FIFO/primitive), so it Verilates
 * with no Xilinx tools. Exit 0 = pass, non-zero = fail.
 */

#include "Vtraffic_class_map.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <cstdio>
#include <cstdint>
#include <random>

constexpr int NQ = 5;
constexpr int TDEST_W = 3;   // ceil(log2 NQ); CLS_TC_QUEUE_MAP packs TDEST_W bits/entry
constexpr int TDEST_MASK = (1 << TDEST_W) - 1;

// EtherType constants (match ethernet_packet_pkg.sv)
constexpr uint16_t ETH_TYPE_PTP  = 0x88F7;
constexpr uint16_t ETH_TYPE_AVTP = 0x22F0;
constexpr uint16_t ETH_TYPE_MSRP = 0x22EA;
constexpr uint16_t ETH_TYPE_MVRP = 0x88F5;

// Reserved control destination group addresses (ethernet_packet_pkg.sv), wire
// byte order with byte 0 in the MSB. 01-80-C2-00-00-0E is SHARED by gPTP and
// MSRP and the two must NOT collapse into one queue - q2 vs q1.
constexpr uint64_t MAC_NEAREST_BRIDGE = 0x0180C200000EULL;  // gPTP + MSRP
constexpr uint64_t MAC_MVRP           = 0x0180C2000021ULL;
constexpr uint64_t MAC_ATDECC         = 0x91E0F0010000ULL;  // ADP / ACMP
constexpr uint64_t MAC_MAAP           = 0x91E0F000FF00ULL;
// Not in the table: a plain unicast (an AECP peer / any ordinary station), a
// foreign multicast, and the Bridge Group Address RSTP will one day use - that
// one is here ONLY as a negative today (no row, no LLC decode, so it must
// classify exactly like any other unknown address).
constexpr uint64_t MAC_UNICAST        = 0x020000000068ULL;
constexpr uint64_t MAC_FOREIGN_MCAST  = 0x0180C2000042ULL;
constexpr uint64_t MAC_BRIDGE_GROUP   = 0x0180C2000000ULL;  // RSTP, future

// Enum ordering (ethernet_packet_pkg.sv network_priority_t). 802.1Q order:
// the value IS the queue index and the HIGHER index is the HIGHER priority.
constexpr int BEST_EFFORT   = 0;
constexpr int CONTROL_CLASS = 1;
constexpr int GPTP_CLASS    = 2;
constexpr int SRB_CLASS     = 3;
constexpr int SRA_CLASS     = 4;

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
    bool     dmac_check = false;        // REQ-CLS-07: validate the reserved gPTP DMAC
    uint64_t dmac       = MAC_UNICAST;  // frame destination MAC (wire byte order)
    bool     ctrl_class = true;         // REQ-CLS-10: CLS_CTRL[2], resets to 1
};

// At most this many per-frame [FAIL] lines are printed; the tally still
// counts every failure. Keeps a broken DUT from burying the summary.
constexpr long kMaxFailLines = 20;

// milan_csr reset defaults (docs/reference/REGISTER_MAP.md)
constexpr uint32_t DEF_PCP_TC = 0x00FAC688;
constexpr uint32_t DEF_REGEN  = 0x00FAC688;   // identity (reset fixed 2026-07-05)
// milan_csr reset CLS_TC_QUEUE_MAP for the 5-queue map: 3 bits/entry,
// TC0/1 -> q0, TC2 -> q3 (SR class B), TC3 -> q4 (SR class A),
// TC4/5 -> q1 (control), TC6/7 -> q2 (gPTP). Every queue is mapped.
constexpr uint32_t DEF_TCQ    = 0x004898C0;
constexpr int      DEF_TCQ_Q[8] = {0, 0, 3, 4,
                                   1, 1, 2, 2};

// Reference classification (independent of the RTL).
static uint32_t ref_tdest(const Frame& f) {
    // REQ-CLS-07: with dmac_check on, the fast path also demands the reserved
    // 802.1AS multicast; a spoofed 0x88F7 falls through to the ordinary paths.
    const bool hit_nb = (f.dmac == MAC_NEAREST_BRIDGE);
    const bool gptp = (f.eth_type == ETH_TYPE_PTP) && (!f.dmac_check || hit_nb);
    // REQ-CLS-10: DMAC-keyed control table. NO EtherType precondition on a row
    // hit (the next protocol through this door, RSTP, has no EtherType at all);
    // the EtherType refines only the shared 01-80-C2-00-00-0E, and that split
    // IS the gPTP arm winning the priority chain first.
    const bool dmac_ctrl = hit_nb || (f.dmac == MAC_MVRP) ||
                           (f.dmac == MAC_ATDECC) || (f.dmac == MAC_MAAP);
    const bool group     = ((f.dmac >> 40) & 1ULL) != 0;   // I/G bit, wire byte 0
    // AECP has NO group address - it is addressed to the peer entity's unicast
    // MAC - so that one arm has to be keyed on the EtherType instead.
    const bool ctrl = f.ctrl_class && !f.vlan_valid &&
                      (dmac_ctrl || (!group && f.eth_type == ETH_TYPE_AVTP));
    if (gptp) return GPTP_CLASS & TDEST_MASK;
    if (ctrl) return CONTROL_CLASS & TDEST_MASK;
    if (f.use_pcp) {
        uint8_t eff_pcp = f.vlan_valid ? f.pcp : f.default_pcp;
        uint8_t regen   = (f.prio_regen   >> (eff_pcp * 3)) & 0x7;
        uint8_t tc      = (f.pcp_tc_map   >> (regen   * 3)) & 0x7;
        // TC->queue: TDEST_W bits per entry (matches the ABI / RTL bit-slice)
        uint8_t queue   = (f.tc_queue_map >> (tc * TDEST_W)) & TDEST_MASK;
        // OUT-OF-RANGE CLAMP: at NQ=5 the 3-bit field can name q5/q6/q7, which do
        // not exist; traffic_class_map falls back to BEST_EFFORT rather than
        // letting axis_demux silently drop the frame (`select >= M_COUNT`).
        if (queue >= NQ) queue = BEST_EFFORT;
        return queue;
    } else {
        // Legacy EtherType fallback, unchanged. Its untagged-0x22F0 arm is only
        // reachable for a control frame when CLS_CTRL[2] is CLEARED.
        int p;
        if (gptp)                                              p = GPTP_CLASS;
        else if (f.vlan_valid && f.eth_type == ETH_TYPE_AVTP)  p = SRA_CLASS;
        else if (!f.vlan_valid && f.eth_type == ETH_TYPE_AVTP) p = CONTROL_CLASS;
        else                                                   p = BEST_EFFORT;
        return p & TDEST_MASK;
    }
}

namespace {

struct Proto { const char* name; uint64_t dmac; uint16_t et; int want; };
// The table of docs/reference/EGRESS_QUEUE_MAP.md, as frames.
constexpr Proto protos[] = {
    { "gPTP",      MAC_NEAREST_BRIDGE, ETH_TYPE_PTP,  GPTP_CLASS    },
    { "MSRP",      MAC_NEAREST_BRIDGE, ETH_TYPE_MSRP, CONTROL_CLASS },
    { "MVRP",      MAC_MVRP,           ETH_TYPE_MVRP, CONTROL_CLASS },
    { "ADP/ACMP",  MAC_ATDECC,         ETH_TYPE_AVTP, CONTROL_CLASS },
    { "MAAP",      MAC_MAAP,           ETH_TYPE_AVTP, CONTROL_CLASS },
    { "AECP",      MAC_UNICAST,        ETH_TYPE_AVTP, CONTROL_CLASS },
};

//! The DUT, the tally and every directed phase under one owner: each phase is
//! named for what it proves, and the counters it moves are members rather than
//! translation-unit state (Core Guidelines I.2, F.3).
class ClassificationHarness {
 public:
    int run() {
        const milan::tb::Model<Vtraffic_class_map> model;
        dut = model.get();

        printf("== traffic_class_map classification harness (NQ=%d) ==\n", NQ);

        check_tagged_frames_take_the_default_table();
        check_reset_queue_map_names_the_five_queues();
        check_priority_order_is_the_queue_index();
        check_out_of_range_queue_clamps_to_best_effort();
        check_untagged_frame_uses_default_port_priority();
        check_legacy_ethertype_fallback_preserved();
        check_reserved_dmac_gates_the_gptp_fast_path();
        check_control_fast_path_is_dmac_keyed();
        check_random_sweep_matches_reference();

        printf("--------------------------------------------------------------\n");
        printf("checks: %ld   failures: %ld\n", checks, fails);
        printf("RESULT: %s\n", (fails == 0) ? "PASS" : "FAIL");

        return (fails == 0) ? 0 : 1;
    }

 private:
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
        dut->ctrl_class_en_i = f.ctrl_class;
        dut->dmac_i         = f.dmac;
        dut->eth_type_i     = f.eth_type;
        dut->eval();
        return dut->tdest_o & 0xFF;
    }

    void check(const Frame& f, const char* tag) {
        uint32_t got = eval(f);
        uint32_t exp = ref_tdest(f);
        checks++;
        if (got != exp) {
            if (fails < kMaxFailLines)
                printf("  [FAIL] %-18s got=%u exp=%u (use_pcp=%d vlan=%d pcp=%u eth=%04X "
                       "dchk=%d cls=%d dmac=%012llX)\n",
                       tag, got, exp, f.use_pcp, f.vlan_valid, f.pcp, f.eth_type,
                       f.dmac_check, f.ctrl_class, static_cast<unsigned long long>(f.dmac));
            fails++;
        }
    }

    // The identity PCP->TC map, as the three-bits-per-entry word the RTL reads.
    static uint32_t identity24() {
        uint32_t ident24 = 0;
        for (int i = 0; i < 8; i++) ident24 |= static_cast<uint32_t>(i) << (3 * i);
        return ident24;
    }

    // ---- Directed 1: tagged frames through the default Table-8-5 map ----
    void check_tagged_frames_take_the_default_table() {
        long f0 = fails;
        for (int pcp = 0; pcp < 8; pcp++) {
            Frame f{true, 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, true, static_cast<uint8_t>(pcp), false, 0x0800};
            check(f, "tagged_default");
        }
        printf("  [%s] tagged frames PCP 0..7 classify per default table\n",
               (fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 1b: the 5-queue reset CLS_TC_QUEUE_MAP, entry by entry ----
    // Locks the ABI intent (TDEST_W bits/entry) so a wrong field width regresses,
    // AND locks the USER's egress map: SR class A on q4, class B on q3, gPTP on
    // q2, control on q1, best effort on q0. There is no spare queue any more.
    void check_reset_queue_map_names_the_five_queues() {
        long f0 = fails;
        // identity PCP->TC (DEF via prio_regen+pcp_tc), so route a tagged frame
        // whose regenerated TC is exactly t, and confirm queue == DEF_TCQ_Q[t].
        uint32_t ident24 = identity24();
        for (int tc = 0; tc < 8; tc++) {
            Frame f{true, 0, ident24, ident24, DEF_TCQ, true, static_cast<uint8_t>(tc), false, 0x0800};
            uint32_t q = eval(f);
            if (q != static_cast<uint32_t>(DEF_TCQ_Q[tc])) {
                printf("  [FAIL] reset TCQ: TC%d -> q%u (expect q%d)\n", tc, q, DEF_TCQ_Q[tc]);
                fails++;
            }
            if (q >= static_cast<uint32_t>(NQ)) {
                printf("  [FAIL] reset TCQ: TC%d named q%u, which does not exist\n", tc, q);
                fails++;
            }
            check(f, "tcq_reset_map");
        }
        printf("  [%s] reset CLS_TC_QUEUE_MAP 0x004898C0 = the 5-queue map "
               "(TC3->q4 class A, TC2->q3 class B, TC4/5->q1, TC6/7->q2, rest q0)\n",
               (fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 1c: 802.1Q ORDER - the enum value IS the queue index and a
    // higher index is a higher priority. Pins SRA above SRB above gPTP above
    // control above best effort, which is what makes the arbiter in
    // traffic_shaping_core grant audio before sync.
    void check_priority_order_is_the_queue_index() {
        long f0 = fails;
        bool ok = (SRA_CLASS == 4) && (SRB_CLASS == 3) && (GPTP_CLASS == 2) &&
                  (CONTROL_CLASS == 1) && (BEST_EFFORT == 0);
        // and the DUT agrees: legacy-mode VLAN AVTP -> q4, gPTP -> q2, IP -> q0
        Frame avtp{false, 0, 0, 0, 0, true,  0, false, ETH_TYPE_AVTP};
        Frame ptp {false, 0, 0, 0, 0, false, 0, false, ETH_TYPE_PTP};
        Frame be  {false, 0, 0, 0, 0, false, 0, false, 0x0800};
        uint32_t qa = eval(avtp);
        uint32_t qp = eval(ptp);
        uint32_t qb = eval(be);
        if (!(qa == 4 && qp == 2 && qb == 0)) {
            printf("  [FAIL] 802.1Q order: AVTP q%u (want 4), gPTP q%u (want 2), BE q%u (want 0)\n",
                   qa, qp, qb);
            fails++;
        }
        if (!(qa > qp && qp > qb)) {
            printf("  [FAIL] 802.1Q order: shaped class A must outrank gPTP must outrank BE\n");
            fails++;
        }
        if (!ok) {
            printf("  [FAIL] network_priority_t values are not the queue indices\n");
            fails++;
        }
        printf("  [%s] 802.1Q order: q4 SR-A > q3 SR-B > q2 gPTP > q1 control > q0 BE (no spare)\n",
               (fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 1d: an out-of-range programmed queue is CLAMPED to best
    // effort, not handed to the demux (which would silently drop the frame).
    // Only reachable because 5 is not a power of two: the 3-bit field can name
    // q5/q6/q7. NEGATIVE-by-construction - without the clamp the DUT returns 5/6/7.
    void check_out_of_range_queue_clamps_to_best_effort() {
        long f0 = fails;
        uint32_t ident24 = identity24();
        for (int bad = NQ; bad < 8; bad++) {
            // map every traffic class to `bad`
            uint32_t tcq = 0;
            for (int i = 0; i < 8; i++) tcq |= static_cast<uint32_t>(bad) << (TDEST_W * i);
            Frame f{true, 0, ident24, ident24, tcq, true, 3, false, 0x0800};
            uint32_t q = eval(f);
            check(f, "tcq_out_of_range");
            if (q != static_cast<uint32_t>(BEST_EFFORT)) {
                printf("  [FAIL] out-of-range queue %d not clamped: tdest=q%u\n", bad, q);
                fails++;
            }
        }
        printf("  [%s] CLS_TC_QUEUE_MAP entries >= NUMBER_OF_QUEUES clamp to BEST_EFFORT\n",
               (fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 2: untagged frame uses the default port priority ----
    void check_untagged_frame_uses_default_port_priority() {
        long f0 = fails;
        for (int dp = 0; dp < 8; dp++) {
            Frame tagged  {true, static_cast<uint8_t>(dp), DEF_PCP_TC, DEF_REGEN, DEF_TCQ,
                           true,  static_cast<uint8_t>(dp), false, 0x0800};
            Frame untagged{true, static_cast<uint8_t>(dp), DEF_PCP_TC, DEF_REGEN, DEF_TCQ,
                           false, 0,                        false, 0x0800};
            uint32_t qt = eval(tagged);
            uint32_t qu = eval(untagged);
            check(untagged, "untagged_default");
            if (qt != qu) {
                printf("  [FAIL] untagged(default_pcp=%d)=%u != tagged(pcp=%d)=%u\n", dp, qu, dp, qt);
                fails++;
            }
        }
        printf("  [%s] untagged frame classified by default port priority (REQ-CLS-03)\n",
               (fails == f0) ? "PASS" : "FAIL");
    }

    // ---- Directed 3: legacy EtherType fallback (use_pcp=0) ----
    void check_legacy_ethertype_fallback_preserved() {
        long f0 = fails;
        Frame ptp   {false, 0, 0, 0, 0, false, 0, false, ETH_TYPE_PTP};
        Frame avtp_v{false, 0, 0, 0, 0, true,  0, false, ETH_TYPE_AVTP};
        Frame avtp_u{false, 0, 0, 0, 0, false, 0, false, ETH_TYPE_AVTP};
        Frame be    {false, 0, 0, 0, 0, false, 0, false, 0x0800};
        check(ptp, "legacy_ptp");
        check(avtp_v, "legacy_avtp_vlan");
        check(avtp_u, "legacy_avtp_novlan");
        check(be, "legacy_be");
        bool ok = (eval(ptp)==(GPTP_CLASS&TDEST_MASK)) &&
                  (eval(avtp_v)==(SRA_CLASS&TDEST_MASK)) &&
                  (eval(avtp_u)==(CONTROL_CLASS&TDEST_MASK)) &&
                  (eval(be)==(BEST_EFFORT&TDEST_MASK));
        printf("  [%s] legacy EtherType fallback (gPTP/SR-A/control/BE) preserved\n",
               (ok && fails == f0) ? "PASS" : "FAIL");
        if (!ok) fails++;
    }

    // ---- Directed 4: reserved-DMAC validation of the gPTP fast path (REQ-CLS-07) ----
    // 802.1AS-2020 s10.5: gPTP rides the reserved multicast 01-80-C2-00-00-0E.
    // The fast path hands 0x88F7 the second-highest queue, so with dmac_check
    // on it must ALSO see that DMAC. Negative leg (the reject must be honest):
    // a spoofed 0x88F7 at a foreign DMAC must NOT reach GPTP_CLASS - it lands
    // on the ordinary table queue (PCP mode) / BEST_EFFORT (legacy mode).
    void check_reserved_dmac_gates_the_gptp_fast_path() {
        long f0 = fails;
        uint32_t ident24 = identity24();

        // 4a: check OFF - a foreign-DMAC 0x88F7 still takes the fast path
        //     (today's silicon behaviour must be bit-identical at reset)
        Frame off{true, 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, false, 0, false, ETH_TYPE_PTP,
                  /*dmac_check=*/false, /*dmac=*/MAC_UNICAST};
        check(off, "cls07_off");
        if (eval(off) != (GPTP_CLASS & TDEST_MASK)) {
            printf("  [FAIL] cls07: dmac_check=0 must preserve the legacy fast path\n");
            fails++;
        }

        // 4b: check ON + right DMAC -> still GPTP_CLASS, in both modes
        for (int mode = 0; mode < 2; mode++) {
            Frame ok{static_cast<bool>(mode), 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, false, 0, false,
                     ETH_TYPE_PTP, true, MAC_NEAREST_BRIDGE};
            check(ok, "cls07_ok");
            if (eval(ok) != (GPTP_CLASS & TDEST_MASK)) {
                printf("  [FAIL] cls07: reserved DMAC rejected (use_pcp=%d)\n", mode);
                fails++;
            }
        }

        // 4c: NEGATIVE - check ON + foreign DMAC -> must lose the fast path.
        //     PCP mode: untagged, so default_pcp picks the table queue. Use
        //     default_pcp 0, which the reset map sends to q0 (best effort) -
        //     provably NOT GPTP_CLASS (q2). The DMAC is a plain unicast that is
        //     in no control row, and 0x88F7 is not the AECP EtherType, so the
        //     REQ-CLS-10 fast path must not rescue it either.
        {
            Frame spoof{true, 0, ident24, ident24, DEF_TCQ, false, 0, false,
                        ETH_TYPE_PTP, true, MAC_UNICAST};
            uint32_t q = eval(spoof);
            check(spoof, "cls07_spoof_pcp");
            if (q == (GPTP_CLASS & TDEST_MASK)) {
                printf("  [FAIL] cls07 NEGATIVE: spoofed 0x88F7 still took GPTP_CLASS (q%u)\n", q);
                fails++;
            }
            if (q != static_cast<uint32_t>(DEF_TCQ_Q[0])) {
                printf("  [FAIL] cls07 NEGATIVE: spoof landed q%u, want the table queue %d\n",
                       q, DEF_TCQ_Q[0]);
                fails++;
            }
        }
        // 4d: NEGATIVE, legacy mode -> BEST_EFFORT, not GPTP_CLASS
        {
            Frame spoof{false, 0, 0, 0, 0, false, 0, false, ETH_TYPE_PTP, true, MAC_UNICAST};
            uint32_t q = eval(spoof);
            check(spoof, "cls07_spoof_legacy");
            if (q != (BEST_EFFORT & TDEST_MASK)) {
                printf("  [FAIL] cls07 NEGATIVE legacy: spoof landed q%u, want BEST_EFFORT\n", q);
                fails++;
            }
        }
        // 4e: the check must not touch TAGGED AVTP frames at all
        {
            constexpr uint64_t dm[2] = { MAC_UNICAST,
                                         MAC_NEAREST_BRIDGE };
            for (int i = 0; i < 2; i++) {
                Frame avtp{false, 0, 0, 0, 0, true, 0, false, ETH_TYPE_AVTP, true, dm[i]};
                check(avtp, "cls07_avtp_untouched");
                if (eval(avtp) != (SRA_CLASS & TDEST_MASK)) {
                    printf("  [FAIL] cls07: AVTP classification moved with dmac=%012llX\n",
                           static_cast<unsigned long long>(dm[i]));
                    fails++;
                }
            }
        }
        printf("  [%s] reserved-DMAC validation gates the gPTP fast path (REQ-CLS-07)\n",
               (fails == f0) ? "PASS" : "FAIL");
    }

    // The reset configuration, verbatim: use_pcp = 1, default_pcp = 0.
    static Frame ctl(uint64_t dmac, uint16_t et, bool tagged, uint8_t pcp,
                     bool use_pcp, bool en) {
        Frame f{use_pcp, 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, tagged, pcp, false, et,
                /*dmac_check=*/false, dmac, en};
        return f;
    }

    // ---- Directed 5: the CONTROL fast path is keyed on the DESTINATION MAC
    // (REQ-CLS-10). This is the defect this suite exists to pin: MAAP, MSRP,
    // MVRP and 1722.1 ADP/ACMP/AECP are UNTAGGED link-local PDUs. They carry no
    // C-TAG, therefore no PCP, therefore the three PCP tables could only ever
    // route them by `default_pcp_i` - and at the shipping reset configuration
    // (use_pcp = 1, default_pcp = 0) that is BEST EFFORT. The CONTROL_CLASS
    // row of EGRESS_QUEUE_MAP.md was documented but not implemented.
    void check_control_fast_path_is_dmac_keyed() {
        long f0 = fails;

        check_documented_protocols_land_on_their_queue();
        check_shared_nearest_bridge_address_does_not_collapse();
        check_tagged_avtp_stays_on_the_sr_classes();
        check_cleared_control_bit_restores_version_0x0011();
        check_address_with_no_row_gets_nothing();
        check_forged_ethertype_cannot_buy_control_class();

        printf("  [%s] control fast path is DMAC-keyed: MSRP/MVRP/ADP/ACMP/MAAP/AECP -> q1, "
               "gPTP -> q2 at the SAME shared address, tagged 0x22F0 stays on the SR classes "
               "(REQ-CLS-10)\n", (fails == f0) ? "PASS" : "FAIL");
    }

    // 5a: every protocol lands on its documented queue, in BOTH modes, at
    //     the reset configuration.
    void check_documented_protocols_land_on_their_queue() {
        for (int mode = 0; mode < 2; mode++) {
            for (const Proto& p : protos) {
                Frame f = ctl(p.dmac, p.et, false, 0, static_cast<bool>(mode), true);
                uint32_t q = eval(f);
                check(f, "ctl_map");
                if (q != static_cast<uint32_t>(p.want)) {
                    printf("  [FAIL] REQ-CLS-10: %s (dmac %012llX eth %04X, use_pcp=%d) -> q%u, want q%d\n",
                           p.name, static_cast<unsigned long long>(p.dmac), p.et, mode, q, p.want);
                    fails++;
                }
            }
        }
    }

    // 5b: THE SHARED ADDRESS. gPTP and MSRP both ride 01-80-C2-00-00-0E and
    //     they must NOT collapse: the EtherType splits that one address and
    //     nothing else does. Cross-check against the SAME address.
    void check_shared_nearest_bridge_address_does_not_collapse() {
        Frame g = ctl(MAC_NEAREST_BRIDGE, ETH_TYPE_PTP,  false, 0, true, true);
        Frame m = ctl(MAC_NEAREST_BRIDGE, ETH_TYPE_MSRP, false, 0, true, true);
        uint32_t qg = eval(g);
        uint32_t qm = eval(m);
        if (!(qg == static_cast<uint32_t>(GPTP_CLASS) &&
              qm == static_cast<uint32_t>(CONTROL_CLASS) && qg != qm)) {
            printf("  [FAIL] shared 01-80-C2-00-00-0E collapsed: gPTP q%u, MSRP q%u\n", qg, qm);
            fails++;
        }
    }

    // 5c: NEGATIVE - a TAGGED 0x22F0 is an AVTP STREAM, not control. It must
    //     keep its PCP and ride the CBS-shaped SR queues. PCP 3 (class A) ->
    //     q4 and PCP 2 (class B) -> q3 under the reset tables; legacy mode
    //     classes it SRA_CLASS. Checked at EVERY control DMAC too, so the
    //     table can never outrank the tag.
    void check_tagged_avtp_stays_on_the_sr_classes() {
        constexpr uint64_t dm[4] = { MAC_ATDECC, MAC_MAAP,
                                     MAC_NEAREST_BRIDGE, MAC_UNICAST };
        for (int i = 0; i < 4; i++) {
            Frame a{true, 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, true, 3, false,
                    ETH_TYPE_AVTP, false, dm[i], true};
            Frame b{true, 0, DEF_PCP_TC, DEF_REGEN, DEF_TCQ, true, 2, false,
                    ETH_TYPE_AVTP, false, dm[i], true};
            Frame l{false, 0, 0, 0, 0, true, 3, false, ETH_TYPE_AVTP, false, dm[i], true};
            uint32_t qa = eval(a);
            uint32_t qb = eval(b);
            uint32_t ql = eval(l);
            check(a, "stream_pcp3");
            check(b, "stream_pcp2");
            check(l, "stream_legacy");
            if (qa != static_cast<uint32_t>(SRA_CLASS) || qb != static_cast<uint32_t>(SRB_CLASS) ||
                ql != static_cast<uint32_t>(SRA_CLASS)) {
                printf("  [FAIL] tagged 0x22F0 at dmac %012llX left the SR classes: "
                       "PCP3 q%u (want %d), PCP2 q%u (want %d), legacy q%u (want %d)\n",
                       static_cast<unsigned long long>(dm[i]),
                       qa, SRA_CLASS, qb, SRB_CLASS, ql, SRA_CLASS);
                fails++;
            }
            if (qa == static_cast<uint32_t>(CONTROL_CLASS) ||
                ql == static_cast<uint32_t>(CONTROL_CLASS)) {
                printf("  [FAIL] tagged 0x22F0 was swallowed by the control fast path\n");
                fails++;
            }
        }
    }

    // 5d: NEGATIVE - CLS_CTRL[2] = 0 restores VERSION 0x0011 behaviour
    //     bit-for-bit. Every control protocol falls back to the tables
    //     (q0 at the reset config) except the historical legacy-mode
    //     untagged-0x22F0 arm, which is deliberately left alone.
    void check_cleared_control_bit_restores_version_0x0011() {
        for (const Proto& p : protos) {
            if (p.want == GPTP_CLASS) continue;         // gPTP is not gated by this bit
            Frame f = ctl(p.dmac, p.et, false, 0, /*use_pcp=*/true, /*en=*/false);
            uint32_t q = eval(f);
            check(f, "ctl_disabled");
            if (q == static_cast<uint32_t>(CONTROL_CLASS)) {
                printf("  [FAIL] REQ-CLS-10 gate: %s reached CONTROL_CLASS with CLS_CTRL[2]=0\n", p.name);
                fails++;
            }
            if (q != static_cast<uint32_t>(DEF_TCQ_Q[0])) {
                printf("  [FAIL] REQ-CLS-10 gate: %s landed q%u, want the table queue %d\n",
                       p.name, q, DEF_TCQ_Q[0]);
                fails++;
            }
        }
    }

    // 5e: NEGATIVE - an address that is NOT a row gets nothing. The Bridge
    //     Group Address 01-80-C2-00-00-00 is here on purpose: RSTP is
    //     anticipated but NOT implemented (a BPDU is an 802.3/LLC frame with
    //     no EtherType at all), so today it must classify like any other
    //     unknown multicast - table queue, never CONTROL_CLASS. Whoever adds the row
    //     will see this check flip, which is the point.
    void check_address_with_no_row_gets_nothing() {
        constexpr uint64_t dm[2]    = { MAC_FOREIGN_MCAST,
                                        MAC_BRIDGE_GROUP };
        constexpr const char* nm[2] = { "foreign mcast", "bridge group (RSTP, future)" };
        for (int i = 0; i < 2; i++) {
            // 0x0026 = a plausible BPDU length field where an EtherType would sit
            constexpr uint16_t ets[3] = { 0x0026, ETH_TYPE_MSRP,
                                          ETH_TYPE_AVTP };
            for (int e = 0; e < 3; e++) {
                Frame f = ctl(dm[i], ets[e], false, 0, true, true);
                uint32_t q = eval(f);
                check(f, "ctl_no_row");
                if (q == static_cast<uint32_t>(CONTROL_CLASS)) {
                    printf("  [FAIL] REQ-CLS-10: %s eth %04X reached CONTROL_CLASS with no table row\n",
                           nm[i], ets[e]);
                    fails++;
                }
            }
        }
    }

    // 5f: NEGATIVE - the EtherType alone must NOT buy CONTROL_CLASS at an address that
    //     is neither a control row nor a unicast. A forged 0x22F0 to a
    //     foreign multicast is exactly the spoof a DMAC-keyed rule is meant
    //     to reject, and an EtherType-keyed one would have accepted.
    void check_forged_ethertype_cannot_buy_control_class() {
        Frame f = ctl(MAC_FOREIGN_MCAST, ETH_TYPE_AVTP, false, 0, true, true);
        uint32_t q = eval(f);
        check(f, "ctl_spoof_avtp");
        if (q == static_cast<uint32_t>(CONTROL_CLASS)) {
            printf("  [FAIL] REQ-CLS-10: forged 0x22F0 to a foreign multicast stole CONTROL_CLASS\n");
            fails++;
        }
    }

    // ---- Randomized sweep: DUT must match the reference for any config ----
    void check_random_sweep_matches_reference() {
        long f0 = fails;
        std::mt19937 rng(0xC1A551F1);
        std::uniform_int_distribution<uint32_t> u24(0, 0xFFFFFF);
        std::uniform_int_distribution<uint32_t> u32(0, 0xFFFFFFFF);
        std::uniform_int_distribution<int> b(0, 1);
        std::uniform_int_distribution<int> p3(0, 7);
        constexpr uint16_t etypes[] = {ETH_TYPE_PTP, ETH_TYPE_AVTP, ETH_TYPE_MSRP,
                                   ETH_TYPE_MVRP, 0x0800, 0x86DD, 0x8100, 0x0026};
        std::uniform_int_distribution<int> ei(0, 7);
        constexpr uint64_t dmacs[] = {MAC_NEAREST_BRIDGE, MAC_MVRP, MAC_ATDECC, MAC_MAAP,
                                  MAC_UNICAST, MAC_FOREIGN_MCAST, MAC_BRIDGE_GROUP,
                                  0xFFFFFFFFFFFFULL, 0x91E0F0010001ULL};
        std::uniform_int_distribution<int> di(0, 8);
        // Sweep length. The summary line below quotes the same number.
        constexpr int kSweepFrames = 200000;
        for (int i = 0; i < kSweepFrames; i++) {
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
            f.ctrl_class   = b(rng);
            f.dmac         = dmacs[di(rng)];
            f.eth_type     = etypes[ei(rng)];
            check(f, "random");
            // INVARIANT over the whole sweep, config-independent: a TAGGED
            // 0x22F0 is an AVTP stream and must never be taken by the control
            // fast path, whatever the DMAC or the CLS_CTRL bits say.
            if (f.vlan_valid && f.eth_type == ETH_TYPE_AVTP) {
                Frame g = f;
                g.use_pcp = false;   // legacy mode names the class outright
                if (eval(g) != static_cast<uint32_t>(SRA_CLASS & TDEST_MASK)) {
                    printf("  [FAIL] tagged 0x22F0 left SRA_CLASS (dmac %012llX)\n",
                           static_cast<unsigned long long>(f.dmac));
                    fails++;
                }
            }
        }
        printf("  [%s] randomized 200000 configs/frames (incl. dmac_check, CLS_CTRL[2] and "
               "9 destination MACs) match reference\n",
               (fails == f0) ? "PASS" : "FAIL");
    }

    Vtraffic_class_map* dut = nullptr;
    long checks = 0;
    long fails = 0;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    ClassificationHarness harness;
    return harness.run();
}
