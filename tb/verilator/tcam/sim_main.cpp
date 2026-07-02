/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for tcam.sv — the register-based ternary CAM
 * used as a destination-MAC steering database.
 *
 * Checks: exact match, ternary (wildcard/range) match, priority among
 * overlapping entries (lowest index wins), the multi-hit vector, add / remove /
 * update of entries, and a clean miss. Exit 0 = pass.
 */

#include "Vtcam.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static Vtcam* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-30s got=0x%llx exp=0x%llx\n", what,
                                       (unsigned long long)got, (unsigned long long)exp); }
}

static void tick() { dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); }

// add/update (valid=1) or remove (valid=0) one entry
static void wr(int idx, int valid, uint64_t key, uint64_t mask, int action) {
    dut->wr_en_i = 1; dut->wr_index_i = idx; dut->wr_valid_i = valid;
    dut->wr_key_i = key; dut->wr_mask_i = mask; dut->wr_action_i = action;
    tick();
    dut->wr_en_i = 0; tick();
}

// combinational lookup
static void look(uint64_t key, int& m, int& idx, int& act, int& vec) {
    dut->lookup_key_i = key; dut->eval();
    m = dut->match_o; idx = dut->match_index_o; act = dut->match_action_o; vec = dut->match_vec_o;
}

// Well-known destination MACs
static const uint64_t MAC_GPTP   = 0x0180C200000EULL; // gPTP peer-delay multicast
static const uint64_t MAC_AVDECC = 0x91E0F0010000ULL; // AVDECC/ADP multicast
static const uint64_t MAC_RESVK  = 0x0180C2000000ULL; // reserved multicast 01-80-C2-00-00-0x
static const uint64_t MAC_RESVM  = 0xFFFFFFFFFFF0ULL; // ...low nibble wildcard
static const uint64_t MAC_BCAST  = 0xFFFFFFFFFFFFULL;
static const uint64_t MASK_ALL   = 0xFFFFFFFFFFFFULL;
static const uint64_t MAC_UNI    = 0xAABBCCDDEEFFULL; // random unicast (miss)
static const uint64_t MAC_STREAM = 0x91E0F0001234ULL; // a MAAP-style stream dest

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vtcam;

    dut->rst_n = 0;
    dut->wr_en_i = 0; dut->lookup_key_i = 0;
    for (int i = 0; i < 4; i++) tick();
    dut->rst_n = 1; tick();

    printf("== tcam (ternary MAC CAM) harness ==\n");

    // after reset, table is empty -> everything misses
    int m, idx, act, vec;
    look(MAC_GPTP, m, idx, act, vec);
    ck("empty table misses", m, 0);

    // program the database
    wr(0, 1, MAC_GPTP,   MASK_ALL,  0x01);   // exact gPTP           -> action 1
    wr(1, 1, MAC_AVDECC, MASK_ALL,  0x02);   // exact AVDECC         -> action 2
    wr(2, 1, MAC_RESVK,  MAC_RESVM, 0x03);   // ternary 01-80-C2-..-0x -> action 3
    wr(3, 1, MAC_BCAST,  MASK_ALL,  0x04);   // exact broadcast      -> action 4

    // exact hit; gPTP also falls in the reserved range (entry2) -> priority = entry0
    look(MAC_GPTP, m, idx, act, vec);
    ck("gPTP match",        m, 1);
    ck("gPTP index (prio 0)", idx, 0);
    ck("gPTP action",       act, 0x01);
    ck("gPTP multi-hit vec", vec, 0x5);      // entries 0 and 2 both match

    // ternary-only hit: 01-80-C2-00-00-03 matches the range entry but not exact gPTP
    look(0x0180C2000003ULL, m, idx, act, vec);
    ck("range match",   m, 1);
    ck("range index",   idx, 2);
    ck("range action",  act, 0x03);

    // other exact entries
    look(MAC_AVDECC, m, idx, act, vec);
    ck("avdecc index", idx, 1); ck("avdecc action", act, 0x02);
    look(MAC_BCAST, m, idx, act, vec);
    ck("bcast index", idx, 3); ck("bcast action", act, 0x04);

    // clean miss
    look(MAC_UNI, m, idx, act, vec);
    ck("unicast miss", m, 0); ck("miss vec", vec, 0x0);

    // remove the AVDECC entry -> now misses
    wr(1, 0, 0, 0, 0);
    look(MAC_AVDECC, m, idx, act, vec);
    ck("removed avdecc misses", m, 0);

    // reuse slot 1 for a stream multicast (update)
    wr(1, 1, MAC_STREAM, MASK_ALL, 0x05);
    look(MAC_STREAM, m, idx, act, vec);
    ck("updated entry match", m, 1);
    ck("updated index", idx, 1); ck("updated action", act, 0x05);
    // and the old AVDECC address stays gone
    look(MAC_AVDECC, m, idx, act, vec);
    ck("old key still gone", m, 0);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
