// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// [NC] NETLIST-level pin of KL_chan_map_capture's index decodes.
//
// WHY THIS LEG EXISTS (t532 silicon, 2026-08-09): the runtime dynamic-
// output-map path misbehaved ON SILICON while every RTL simulation of the
// same sequences was green - the same divergence class as the VERSION
// 0x002D +1-key seeder shift that VERSION 0x0030 fixed by hoisting
// always_ff-local `automatic` temporaries to module-scope wires (see
// KL_aecp_response_builder w_odsd_* and the matching lb_a0_w/lb_a1_w/
// lb_nxt_w hoist in KL_chan_map_capture). RTL sims cannot see that class:
// Verilator agrees with the RTL intent, synthesis is what diverges. This
// leg therefore simulates a SYNTHESIZED form of the module: yosys
// (proc; opt; memory; opt -full) lowers the always_ff processes, inlines
// the functions/automatic temporaries, and decomposes both RAMs
// (map_r, lb_hold_r) into explicit write-enable decode and read-mux
// trees - the exact structures a shifted binding would land in - and the
// checks below then pin the decode BY VALUE:
//
//   * one runtime-style map write per channel key {stream 0, channel k,
//     source LOOP rx j}: the readback must return it at key k (and the
//     NEIGHBOUR keys must be untouched - a +1/-1 write shift cannot hide);
//   * the walker output must select channel k carrying rx stream j's
//     samples EXACTLY - not k+1, not j+1 (the two silicon signatures:
//     "wire[n] = store[n-1], channel 0 unreachable" and "loop-of-rx0
//     taps rx1").
//
// The netlist is yosys's, not Vivado's, so this is a pin of the hazard
// CLASS (post-synthesis index decode), not a bit-level Vivado repro - it
// is the strongest desk-side gate available for it.
#include "VKL_chan_map_capture.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <map>

static VKL_chan_map_capture* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, unsigned long got, unsigned long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=0x%lx exp=0x%lx\n", what, got, exp); }
    else            printf("  [ ok ] %-52s = 0x%lx\n", what, got);
}

static void step() { dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); }
static void cyc(int n = 1) { for (int i = 0; i < n; i++) step(); }

// one-cycle map write (the runtime AECP-mirror port shape: addr = CHANNEL key)
static void map_wr(int addr, uint16_t word) {
    dut->map_wr_en_i = 1; dut->map_wr_addr_i = addr; dut->map_wr_data_i = word;
    cyc(); dut->map_wr_en_i = 0; cyc();
}
// registered readback (1-cycle latency), returns the 13-bit entry
static uint32_t map_rd(int addr) {
    dut->map_rd_en_i = 1; dut->map_rd_addr_i = addr;
    for (int g = 0; g < 8; g++) { cyc();
        if (dut->map_rd_valid_o) { dut->map_rd_en_i = 0; uint32_t v = dut->map_rd_data_o; cyc(); return v; } }
    dut->map_rd_en_i = 0; return 0xFFFFFFFFu;
}

// one loopback payload beat: two S32BE samples (2-channel stream = one
// {ch0, ch1} pair per beat), tuser = rx stream index
static void lb_beat(int stream, uint32_t s0, uint32_t s1, int last) {
    uint64_t d = 0;
    d |= (uint64_t)((s0 >> 16) & 0xFF) << 0;
    d |= (uint64_t)((s0 >>  8) & 0xFF) << 8;
    d |= (uint64_t)( s0        & 0xFF) << 16;
    d |= (uint64_t)((s1 >> 16) & 0xFF) << 32;
    d |= (uint64_t)((s1 >>  8) & 0xFF) << 40;
    d |= (uint64_t)( s1        & 0xFF) << 48;
    dut->lb_tdata_i = d; dut->lb_tuser_i = stream;
    dut->lb_tvalid_i = 1; dut->lb_tlast_i = last;
    cyc();
    dut->lb_tvalid_i = 0; dut->lb_tlast_i = 0;
}

// map entry {en[12], half[11], src[10:8], idxh[7:4], idx[3:0]}
static uint16_t ent(int en, int half, int src, int idxh, int idx) {
    return (uint16_t)((en << 12) | (half << 11) | (src << 8) | (idxh << 4) | idx);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_chan_map_capture;

    printf("== [NC] KL_chan_map_capture NETLIST decode pin (yosys proc/memory lowering) ==\n");
    dut->rst_n = 0; dut->tick_i = 0; dut->map_wr_en_i = 0; dut->map_rd_en_i = 0;
    dut->i2s_pair_valid_i = 0; dut->tdm_pair_valid_i = 0; dut->ring_pair_valid_i = 0;
    dut->lb_tvalid_i = 0; dut->lb_tlast_i = 0; dut->tone_smp_i = 0;
    dut->lb_wire_chans_i = 0; dut->lb_flush_i = 0;
    cyc(4); dut->rst_n = 1; cyc(4);

    // rx streams 1 and 2 are 2-channel (fields 4b each; 0 would mean "2"
    // too, but say it explicitly - the decode under test must USE stream 1's
    // field for stream 1)
    dut->lb_wire_chans_i = (2u << (1*4)) | (2u << (2*4));

    // ---- plant DISTINCT audio in rx1 pair0 and rx2 pair0 ------------------
    // (values chosen so any +-1 stream/pair shift changes every check)
    lb_beat(1, 0x111AA0, 0x111BB1, 1);       // rx1: ch0/ch1
    lb_beat(2, 0x222AA0, 0x222BB1, 1);       // rx2: ch0/ch1
    cyc(4);

    // ---- runtime-style map writes: talker 0's four channel keys ----------
    // {stream 0, channel k, source LOOP rx j} - k and j both matter below.
    map_wr(0, ent(1, 0, 5, 2, 0));           // ch0 <- LOOP rx2 pair0 L
    map_wr(1, ent(1, 1, 5, 2, 0));           // ch1 <- LOOP rx2 pair0 R
    map_wr(2, ent(1, 0, 5, 1, 0));           // ch2 <- LOOP rx1 pair0 L
    map_wr(3, ent(1, 1, 5, 1, 0));           // ch3 <- LOOP rx1 pair0 R

    // ---- readback: every write at ITS key, neighbours untouched ----------
    ck("NC readback key 0 (channel 0 IS reachable)", map_rd(0) & 0x1FFF, ent(1,0,5,2,0));
    ck("NC readback key 1", map_rd(1) & 0x1FFF, ent(1,1,5,2,0));
    ck("NC readback key 2", map_rd(2) & 0x1FFF, ent(1,0,5,1,0));
    ck("NC readback key 3", map_rd(3) & 0x1FFF, ent(1,1,5,1,0));
    ck("NC neighbour key 4 untouched (no +1 write shift)", map_rd(4) & 0x1FFF, 0);
    ck("NC neighbour key 63 untouched (no -1 wrap shift)", map_rd(63) & 0x1FFF, 0);

    // an isolated key far from the cluster: +1-shift detector with empty
    // neighbours on BOTH sides
    map_wr(9, ent(1, 0, 5, 1, 1));           // t2 ch1... key 9 <- rx1 pair1
    ck("NC isolated key 9 lands at 9", map_rd(9) & 0x1FFF, ent(1,0,5,1,1));
    ck("NC key 8 still empty",  map_rd(8)  & 0x1FFF, 0);
    ck("NC key 10 still empty", map_rd(10) & 0x1FFF, 0);
    map_wr(9, 0);                            // clear it again (walk stays clean)

    // ---- the walk: one tick, capture every injected pair ------------------
    std::map<int, std::pair<uint32_t,uint32_t>> got;   // slot -> {L, R}
    dut->tick_i = 1; step(); dut->tick_i = 0;
    for (int c = 0; c < 1200; c++) {
        step();
        if (dut->pair_valid_o)
            got[dut->pair_slot_o] = { dut->pair_l_o, dut->pair_r_o };
    }
    ck("NC walk covered all 32 slots", got.size(), 32);

    // slot 0 = channels {0,1}: rx2's pair EXACTLY (loop-of-rx2 taps rx2)
    ck("NC slot 0 L = rx2 ch0 (not rx1's, not silence)", got[0].first,  0x222AA0);
    ck("NC slot 0 R = rx2 ch1", got[0].second, 0x222BB1);
    // slot 1 = channels {2,3}: rx1's pair EXACTLY (loop-of-rx1 taps rx1,
    // NOT rx2 - the "loop-of-rx0 taps rx1" silicon signature detector)
    ck("NC slot 1 L = rx1 ch0 (not rx2's: no +1 stream shift)", got[1].first, 0x111AA0);
    ck("NC slot 1 R = rx1 ch1", got[1].second, 0x111BB1);
    // every unmapped slot injects digital silence (never skipped)
    { int quiet = 1;
      for (int s = 2; s < 32; s++)
          if (got.count(s) && (got[s].first || got[s].second)) quiet = 0;
      ck("NC slots 2..31 carry digital silence", quiet, 1); }

    // ---- fresh rx data must move the SAME channels (hold-write decode) ----
    lb_beat(1, 0x111AA2, 0x111BB3, 1);
    lb_beat(2, 0x222AA2, 0x222BB3, 1);
    cyc(4);
    got.clear();
    dut->tick_i = 1; step(); dut->tick_i = 0;
    for (int c = 0; c < 1200; c++) {
        step();
        if (dut->pair_valid_o)
            got[dut->pair_slot_o] = { dut->pair_l_o, dut->pair_r_o };
    }
    ck("NC beat 2: slot 0 tracks rx2", got[0].first == 0x222AA2 && got[0].second == 0x222BB3, 1);
    ck("NC beat 2: slot 1 tracks rx1", got[1].first == 0x111AA2 && got[1].second == 0x111BB3, 1);

    // ---- REMOVE-style write (0x0000) silences ONLY its channel -----------
    map_wr(2, 0);                            // ch2 dark, ch3 stays
    got.clear();
    dut->tick_i = 1; step(); dut->tick_i = 0;
    for (int c = 0; c < 1200; c++) {
        step();
        if (dut->pair_valid_o)
            got[dut->pair_slot_o] = { dut->pair_l_o, dut->pair_r_o };
    }
    ck("NC removed ch2 goes silent", got[1].first, 0);
    ck("NC sibling ch3 keeps its cluster", got[1].second, 0x111BB3);
    ck("NC untouched slot 0 unaffected by the remove", got[0].first, 0x222AA2);

    printf("----------------------------------------------------------------------\n");
    printf("[NC] netlist decode pin: %ld checks, %ld failures\nRESULT: %s\n",
           checks, fails, fails ? "FAIL" : "PASS");
    delete dut;
    return fails ? 1 : 0;
}
