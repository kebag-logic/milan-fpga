/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_pair_blend + KL_pair_zero_fill (HANDOVER 8.3b
 * / Milan v1.2 5.3.7.3).
 *
 * BLEND: the I2S pair rides OUT slot 0 ("channels 1/2 stay the I2S Pmod",
 * USER 2026-07-28) and TDM pair k rides out slot 1+k; a same-cycle collision
 * passes the TDM strobe and emits the held I2S pair on the next free cycle,
 * freshest sample winning; pairs_merged_o counts every output strobe.
 *
 * ZERO-FILL: per media-tick period, every pair slot that neither of the two
 * preceding periods fed gets ONE zero-sample strobe - so a bound talker with
 * no physical source frames silence (the clause's "shall be streaming"), a
 * live slot is NEVER filled regardless of its phase against the tick, and a
 * slot whose source dies starts filling from the second tick after death.
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vpair_fill_tb_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static Vpair_fill_tb_top* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-52s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    } else {
        printf("  [ok]   %-52s = 0x%llx\n", what, (unsigned long long)got);
    }
}

// one full clk cycle; sample-and-record blend/fill outputs on the rising edge
struct Strobe { int slot; uint32_t l, r; };
static Strobe b_log[64]; static int b_n = 0;
static Strobe z_log[512]; static int z_n = 0;

// Sample BEFORE the rising edge: that is the value a same-clock consumer
// (the packetizer) latches AT the edge - sampling after it reads the
// post-update register state and eats one-cycle strobes the edge itself
// consumed (measured here first: pairs_merged_o said 7 while a post-edge
// probe logged 5).
//
// ZERO-FILL OUTPUT IS REGISTERED (AX 100 MHz timing closure): a strobe
// DECIDED in cycle N - live pass-through or fill - is on z_pv_o/z_slot_o
// during cycle N+1, so this harness always steps once past the driving
// cycle before reading. Z7 pins that contract explicitly. The blend
// outputs remain combinational.
static void step() {
    dut->clk_i = 0; dut->eval();
    if (dut->b_pv_o && b_n < 64)
        b_log[b_n++] = { (int)dut->b_slot_o, dut->b_l_o, dut->b_r_o };
    if (dut->z_pv_o && z_n < 512)
        z_log[z_n++] = { (int)dut->z_slot_o, dut->z_l_o, dut->z_r_o };
    dut->clk_i = 1; dut->eval();
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vpair_fill_tb_top;

    dut->rst_n = 0;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) step();

    // =====================================================================
    //  BLEND
    // =====================================================================
    printf("[blend] slot map + collision hold\n");

    // B1: lone I2S strobe -> out slot 0, data passes
    b_n = 0;
    dut->b_i2s_pv_i = 1; dut->b_i2s_l_i = 0x111111; dut->b_i2s_r_i = 0x222222;
    step();
    dut->b_i2s_pv_i = 0;
    step();
    ck("B1 lone I2S: one strobe", b_n, 1);
    ck("B1 out slot", b_log[0].slot, 0);
    ck("B1 L", b_log[0].l, 0x111111);
    ck("B1 R", b_log[0].r, 0x222222);

    // B2: lone TDM strobe slot 2 -> out slot 3
    b_n = 0;
    dut->b_tdm_pv_i = 1; dut->b_tdm_slot_i = 2;
    dut->b_tdm_l_i = 0x333333; dut->b_tdm_r_i = 0x444444;
    step();
    dut->b_tdm_pv_i = 0;
    step();
    ck("B2 lone TDM slot 2: one strobe", b_n, 1);
    ck("B2 out slot == 1 + tdm slot", b_log[0].slot, 3);
    ck("B2 L", b_log[0].l, 0x333333);

    // B3: same-cycle collision -> TDM this cycle, held I2S the next
    b_n = 0;
    dut->b_i2s_pv_i = 1; dut->b_i2s_l_i = 0xAAAAAA; dut->b_i2s_r_i = 0xBBBBBB;
    dut->b_tdm_pv_i = 1; dut->b_tdm_slot_i = 0;
    dut->b_tdm_l_i = 0xCCCCCC; dut->b_tdm_r_i = 0xDDDDDD;
    step();
    dut->b_i2s_pv_i = 0; dut->b_tdm_pv_i = 0;
    step(); step();
    ck("B3 collision: two strobes total", b_n, 2);
    ck("B3 first is TDM (slot 1)", b_log[0].slot, 1);
    ck("B3 first L is TDM data", b_log[0].l, 0xCCCCCC);
    ck("B3 second is held I2S (slot 0)", b_log[1].slot, 0);
    ck("B3 second L is held I2S data", b_log[1].l, 0xAAAAAA);

    // B4: freshest-wins - collide, then collide again with new I2S data
    // before the hold drains; the LATER sample must be the one emitted
    b_n = 0;
    dut->b_i2s_pv_i = 1; dut->b_i2s_l_i = 0x0A0A0A; dut->b_i2s_r_i = 0;
    dut->b_tdm_pv_i = 1; dut->b_tdm_slot_i = 1;
    dut->b_tdm_l_i = 0x1; dut->b_tdm_r_i = 0;
    step();                                     // hold <- 0x0A0A0A
    dut->b_i2s_l_i = 0x0B0B0B;                  // fresh sample, same collision
    dut->b_tdm_slot_i = 2; dut->b_tdm_l_i = 0x2;
    step();                                     // hold <- 0x0B0B0B (fresh wins)
    dut->b_i2s_pv_i = 0; dut->b_tdm_pv_i = 0;
    step(); step();
    ck("B4 three strobes (2 TDM + 1 I2S)", b_n, 3);
    ck("B4 drained I2S is the FRESH sample", b_log[2].l, 0x0B0B0B);

    // B5: pairs_merged_o counted every output strobe above (1+1+2+3)
    ck("B5 pairs_merged_o == output strobes", dut->b_merged_o, 7);

    // =====================================================================
    //  ZERO-FILL  (TOTAL_P = 8; the harness owns the tick)
    // =====================================================================
    printf("[fill] 5.3.7.3 silence fill, fed-tracked\n");
    auto tick = [&]() { dut->z_tick_i = 1; step(); dut->z_tick_i = 0; };
    auto quiet_cycles = [&](int n) { for (int i = 0; i < n; i++) step(); };

    // Z1: reset grace - the first tick fills nothing (fed_prev resets
    // all-fed), the second declares every slot dead and fills all 8
    z_n = 0;
    tick(); quiet_cycles(20);
    ck("Z1 no fills after the first tick", z_n, 0);
    tick(); quiet_cycles(20);
    ck("Z1 second tick fills every slot", z_n, 8);
    bool all_zero = true, slots_ok = true;
    for (int i = 0; i < z_n; i++) {
        if (z_log[i].l || z_log[i].r) all_zero = false;
        if (z_log[i].slot != i) slots_ok = false;   // lowest-first walk
    }
    ck("Z1 fills carry zero samples", all_zero ? 1 : 0, 1);
    ck("Z1 fills walk slots 0..7 in order", slots_ok ? 1 : 0, 1);
    ck("Z1 fill_cnt_o", dut->z_fill_cnt_o, 8);

    // Z2: a live slot is never filled - feed slot 3 once per period at a
    // phase that lands JUST AFTER each tick (the worst case the two-period
    // rule exists for), 10 periods; slot 3 must appear only as passthrough.
    // PRIME it first: one strobe in the period before the loop, so the
    // loop's first tick already sees it live (a fill decided before a slot
    // has ever strobed is correct, not a false positive).
    dut->z_pv_i = 1; dut->z_slot_i = 3;
    dut->z_l_i = 0x654321; dut->z_r_i = 0x123456;
    step();
    dut->z_pv_i = 0;
    quiet_cycles(4);
    int fills_slot3 = 0, passes_slot3 = 0;
    for (int p = 0; p < 10; p++) {
        tick();
        // just after the tick: the live strobe (decision cycle N; the
        // registered output presents it during N+1)
        dut->z_pv_i = 1; dut->z_slot_i = 3;
        dut->z_l_i = 0x654321; dut->z_r_i = 0x123456;
        z_n = 0; step();
        dut->z_pv_i = 0; step();
        if (z_n == 1 && z_log[0].slot == 3 && z_log[0].l == 0x654321)
            passes_slot3++;
        z_n = 0; quiet_cycles(20);
        for (int i = 0; i < z_n; i++) if (z_log[i].slot == 3) fills_slot3++;
    }
    ck("Z2 live slot passes through every period", passes_slot3, 10);
    ck("Z2 live slot NEVER filled (any phase)", fills_slot3, 0);

    // Z3: the other 7 slots filled once per period while slot 3 lived
    // (10 periods x 7) + Z1's 8 = fill_cnt total
    ck("Z3 fill_cnt_o == 8 + 10*7", dut->z_fill_cnt_o, 8 + 70);

    // Z4: death - stop feeding slot 3; the two-period rule holds it back
    // while EITHER window still saw it (grace is up to two periods,
    // ~41.7 us - the price of never doubling a live slot), then fills
    // resume every period
    z_n = 0; tick(); quiet_cycles(20);
    int f3 = 0; for (int i = 0; i < z_n; i++) if (z_log[i].slot == 3) f3++;
    ck("Z4 grace window 1 after death", f3, 0);
    z_n = 0; tick(); quiet_cycles(20);
    f3 = 0; for (int i = 0; i < z_n; i++) if (z_log[i].slot == 3) f3++;
    ck("Z4 grace window 2 after death", f3, 0);
    z_n = 0; tick(); quiet_cycles(20);
    f3 = 0; for (int i = 0; i < z_n; i++) if (z_log[i].slot == 3) f3++;
    ck("Z4 dead slot fills once both windows empty", f3, 1);
    ck("Z4 all 8 filled once that period", z_n, 8);

    // Z5: input priority - a passthrough strobe during the fill walk defers
    // the fill but loses none of it
    tick();
    dut->z_pv_i = 1; dut->z_slot_i = 6; dut->z_l_i = 0x777777; dut->z_r_i = 0;
    z_n = 0; step();                     // passthrough competes with the walk
    dut->z_pv_i = 0;
    quiet_cycles(25);
    // that period: slot 6 passed through live, 7 others filled (slot 6 was
    // fed THIS period but its fill decision came from the two BEFORE it, so
    // it is also still in the pending walk - assert total strobes = 1 live +
    // 8 pending fills)
    ck("Z5 live strobe + full pending walk", z_n, 9);
    bool live_first = (z_log[0].slot == 6 && z_log[0].l == 0x777777);
    ck("Z5 the live strobe leads the walk out", live_first ? 1 : 0, 1);

    // Z6: an out-of-span slot passes through and is never tracked or filled
    // (settle TWO periods first so Z5's live slot 6 ages out of both windows)
    tick(); quiet_cycles(20);
    tick(); quiet_cycles(20);
    z_n = 0;
    dut->z_pv_i = 1; dut->z_slot_i = 12; dut->z_l_i = 0x999999; dut->z_r_i = 0;
    step();
    dut->z_pv_i = 0;
    step();                              // registered output: read at N+1
    ck("Z6 out-of-span slot passes through", z_n, 1);
    ck("Z6 slot preserved", z_log[0].slot, 12);
    int before = dut->z_fill_cnt_o;
    tick(); quiet_cycles(20);
    tick(); quiet_cycles(20);
    ck("Z6 fill span stays 8/period", (dut->z_fill_cnt_o - before) % 8, 0);

    // Z7: REGISTERED-OUTPUT CONTRACT (the AX 100 MHz re-time). A strobe
    // decided in cycle N is ABSENT from the outputs during N and present
    // exactly during N+1; two back-to-back decisions leave back-to-back,
    // none lost, and nothing trails. A combinational output (the old
    // shape), a skipped valid delay, or a doubled register all fail here.
    // No tick since Z6, so the pending walk is empty and cannot interleave.
    quiet_cycles(4);
    z_n = 0;
    dut->z_pv_i = 1; dut->z_slot_i = 2;
    dut->z_l_i = 0xABC123; dut->z_r_i = 0x00CAFE;
    step();                              // N: decision only
    ck("Z7 output silent in the decision cycle", z_n, 0);
    dut->z_slot_i = 4; dut->z_l_i = 0x0DEF45; dut->z_r_i = 0x00BEEF;
    step();                              // N+1: strobe N visible, N+1 decides
    ck("Z7 strobe N sampled at N+1", z_n, 1);
    ck("Z7 slot intact", z_log[0].slot, 2);
    ck("Z7 L intact", z_log[0].l, 0xABC123);
    ck("Z7 R intact", z_log[0].r, 0x00CAFE);
    dut->z_pv_i = 0;
    step();                              // N+2: strobe N+1 visible
    ck("Z7 back-to-back: strobe N+1 at N+2", z_n, 2);
    ck("Z7 second slot intact", z_log[1].slot, 4);
    ck("Z7 second L intact", z_log[1].l, 0x0DEF45);
    step();
    ck("Z7 no trailing strobe", z_n, 2);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
