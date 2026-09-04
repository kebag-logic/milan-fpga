// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Item-4 AES3 / S-PDIF ser/des harness (KL_aes3_tx + KL_aes3_rx, four
// receivers on ONE transmitted biphase-mark line - see aes3_wrap.sv):
//   [LOCK]  cold start: the receiver acquires the unit interval from the
//           wire alone, finds the X/Y/Z preambles, counts 192-frame blocks
//           and only asserts locked_o after LOCK_BLOCKS_P clean blocks - no
//           pair is emitted before that;
//   [PAIR]  sample-exact pair stream: every {pair 0, L, R} the receiver
//           emits equals the pair the transmitter was handed, in order,
//           with pair_slot_o = 0 and pairs_captured_o counting them;
//   [WORD]  the same wire decoded at WORD_BITS_P 20 and 16 truncates
//           exactly where the standard says (top bits of the aux+sample
//           field, MSB-justified into the 24-bit pipeline width);
//   [CS]    channel status round-trips: the block the transmitter sends is
//           the block the receiver publishes, and CONSUMER_P re-reads the
//           SAME bits as AES3 professional vs IEC 60958-3 consumer
//           (emphasis/fs at different offsets, pro/consumer mismatch flag);
//   [VBIT]  V=1 counts in invalid_o and does NOT drop lock or suppress the
//           pair (the wire-truth rule the front-end family follows);
//   [ERR]   a real biphase violation injected on the line (flip_i inserts
//           two extra transitions) drops lock, counts sync_loss_o, stops
//           the pair stream, and the link re-locks by itself afterwards;
//   [UNDER] transmitter underrun: with no fresh pair the line stays LEGAL
//           (the far end keeps lock, zero parity errors) and the repeat is
//           confessed in underrun_o.
#include "Vaes3_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <cstdint>
#include <vector>

// ---------------------------------------------------------------- stimulus --
struct Pair {
    uint32_t l;
    uint32_t r;
};

// The aux+sample field is MSB-justified into the harness's 24-bit pipeline
// width, so a WORD_BITS_P=20 receiver clears the low 4 bits of it and a
// WORD_BITS_P=16 receiver the low 8.
constexpr uint32_t kSampleMask24 = 0xFFFFFFu;
constexpr uint32_t kWord20Mask = 0xFFFFF0u;
constexpr uint32_t kWord16Mask = 0xFFFF00u;
constexpr uint32_t kWord20LowBits = 0xFu;
constexpr uint32_t kWord16LowBits = 0xFFu;

// frame = 128 UI x 4 clk; block = 192 frames
constexpr long FRAME_CLK = 128 * 4;
constexpr long BLOCK_CLK = 192 * FRAME_CLK;

// how long a cold acquisition or a re-lock is given before we call it stuck
constexpr long kLockBudgetClk = 6 * BLOCK_CLK;

namespace {

uint32_t smp(long n) {
    return static_cast<uint32_t>((n * 0x9E37u + 0x5AA5u) & kSampleMask24);
}

//! The ser/des harness: it owns the Verilated model, the transmitted-pair
//! log, the three receivers' capture buffers, the capture arming flags and
//! the tally, so each phase below reads state that belongs to the same object
//! rather than to the file (Core Guidelines I.2).
class Aes3SerdesHarness {
 public:
    int run() {
        reset_dut();
        cold_acquisition_from_the_wire_alone();
        pair_stream_is_sample_exact();
        the_same_wire_at_20_and_16_bits();
        channel_status_round_trips_in_both_dialects();
        v_bit_counts_and_never_gags_the_wire_truth();
        a_biphase_violation_costs_lock_then_relocks();
        starving_the_transmitter_keeps_the_line_legal();
        return report();
    }

 private:
    void ck(const char* t, long got, long exp) {
        checks++;
        if (got != exp) {
            fails++;
            printf("  [FAIL] %-54s got=%ld exp=%ld\n", t, got, exp);
        } else {
            printf("  [ ok ] %-54s = %ld\n", t, got);
        }
    }
    void ck_hex(const char* t, uint32_t got, uint32_t exp) {
        checks++;
        if (got != exp) {
            fails++;
            printf("  [FAIL] %-54s got=0x%06X exp=0x%06X\n", t, got, exp);
        } else {
            printf("  [ ok ] %-54s = 0x%06X\n", t, got);
        }
    }

    void sample_outputs() {
        if (collect) {
            if (dut->r24_pv_o) got24.push_back({dut->r24_l_o, dut->r24_r_o});
            if (dut->r20_pv_o) got20.push_back({dut->r20_l_o, dut->r20_r_o});
            if (dut->r16_pv_o) got16.push_back({dut->r16_l_o, dut->r16_r_o});
        }
        if (watch_unlocked && !dut->r24_lock_o && dut->r24_pv_o) pairs_seen_unlocked++;
    }

    // One cycle of the (single-rate) clock pair. The datapath clock and the serial
    // clock run together here on purpose: the CDC FIFOs are exercised for their
    // protocol, not for their metastability, which is the cdc/ suite's job.
    void step() {
        // present a pair whenever the transmitter has room and we still owe some
        if (feed_left > 0 && dut->pair_ready_o) {
            Pair p{smp(2 * static_cast<long>(pushed.size())),
                   smp(2 * static_cast<long>(pushed.size()) + 1)};
            dut->pair_valid_i = 1;
            dut->pair_l_i = p.l;
            dut->pair_r_i = p.r;
            pushed.push_back(p);
            feed_left--;
        } else {
            dut->pair_valid_i = 0;
        }
        dut->clk = 0;
        dut->clk_audio = 0;
        dut->eval();
        dut->clk = 1;
        dut->clk_audio = 1;
        dut->eval();
        sample_outputs();
    }
    void cyc(long n) { for (long i = 0; i < n; i++) step(); }

    // run until pred() or the budget expires; returns cycles actually run
    template <typename F> long run_until(F pred, long budget) {
        long n = 0;
        while (n < budget && !pred()) {
            step();
            n++;
        }
        return n;
    }

    // find `want` in pushed[] (samples are distinct, so the match is unique)
    long index_of(const Pair& want) {
        for (size_t i = 0; i < pushed.size(); i++)
            if (pushed[i].l == want.l && pushed[i].r == want.r) return static_cast<long>(i);
        return -1;
    }

    void reset_dut() {
        dut->rst_n = 0;
        dut->clk = 0;
        dut->clk_audio = 0;
        dut->pair_valid_i = 0;
        dut->pair_l_i = 0;
        dut->pair_r_i = 0;
        dut->smp_invalid_i = 0;
        dut->flip_i = 0;
        // AES3 professional byte 0 = 0x55: bit0 professional, emphasis [4:2] = 5,
        // fs [7:6] = 1; byte 3 = 0x02 so the consumer dialect reads fs = 2 off
        // the SAME bits. One word, two legal readings - that is the whole point.
        dut->cs_bits_i = 0x02000055u;
        cyc(8);
        dut->rst_n = 1;
        cyc(8);
    }

    // ================================================================ LOCK ==
    void cold_acquisition_from_the_wire_alone() {
        printf("== [LOCK] cold acquisition from the wire alone ==\n");
        feed_left = 4000;
        watch_unlocked = true;
        long n = run_until([this] { return dut->r24_lock_o != 0; }, kLockBudgetClk);
        // locked_o crosses on a 2-FF sync, the census on cdc_pulse: let the
        // slower path land before reading the counters against it
        cyc(32);
        ck("r24 locked_o asserted", dut->r24_lock_o, 1);
        ck("no pair emitted before lock", pairs_seen_unlocked, 0);
        ck("lock took >= 2 blocks (LOCK_BLOCKS_P=2)", n >= 2 * BLOCK_CLK, 1);
        ck("r24 parity errors during acquisition", dut->r24_par_o, 0);
        ck("r24 sync losses during acquisition", dut->r24_loss_o, 0);
        ck("transmitter emitted blocks", dut->tx_blocks_o >= 3, 1);
        ck("r24 saw the same block count", dut->r24_blocks_o >= 3, 1);
        ck("r20 locked too", dut->r20_lock_o, 1);
        ck("r16 locked too", dut->r16_lock_o, 1);
        watch_unlocked = false;
    }

    // ================================================================ PAIR ==
    void pair_stream_is_sample_exact() {
        printf("== [PAIR] sample-exact pair stream ==\n");
        collect = true;
        cyc(40 * FRAME_CLK);
        collect = false;
        ck("pairs received", static_cast<long>(got24.size()) >= 30, 1);
        long base = index_of(got24[0]);
        ck("first received pair is a pair we handed over", base >= 0, 1);
        long bad = 0;
        for (size_t i = 0; i < got24.size(); i++) {
            const Pair& e = pushed[static_cast<size_t>(base) + i];
            if (got24[i].l != e.l || got24[i].r != e.r) bad++;
        }
        ck("every pair sample-exact and in order", bad, 0);
        ck("pair_slot_o is 0 (stereo members own pair 0)", dut->r24_slot_o, 0);
        ck("pairs_captured_o counted them",
           dut->r24_pairs_o >= static_cast<uint32_t>(got24.size()), 1);
    }

    // ================================================================ WORD ==
    void the_same_wire_at_20_and_16_bits() {
        printf("== [WORD] the same wire at 20 and 16 bits ==\n");
        long n20 = static_cast<long>(got20.size()) < static_cast<long>(got24.size())
                       ? static_cast<long>(got20.size())
                       : static_cast<long>(got24.size());
        long b20 = 0;
        long b16 = 0;
        for (long i = 0; i < n20 - 2; i++) {
            long j = index_of(got24[0]) + i;
            uint32_t l = pushed[static_cast<size_t>(j)].l;
            uint32_t r = pushed[static_cast<size_t>(j)].r;
            if (got20[i].l != (l & kWord20Mask) || got20[i].r != (r & kWord20Mask)) b20++;
            if (got16[i].l != (l & kWord16Mask) || got16[i].r != (r & kWord16Mask)) b16++;
        }
        ck("WORD_BITS_P=20 truncates to the top 20 bits", b20, 0);
        ck("WORD_BITS_P=16 truncates to the top 16 bits", b16, 0);
        ck_hex("r20 sample MSB-justified (low 4 bits clear)", got20[1].l & kWord20LowBits, 0);
        ck_hex("r16 sample MSB-justified (low 8 bits clear)", got16[1].l & kWord16LowBits, 0);
    }

    // ================================================================== CS ==
    void channel_status_round_trips_in_both_dialects() {
        printf("== [CS] channel status round-trip, both dialects ==\n");
        ck("r24 cs_valid_o", dut->r24_csv_o, 1);
        ck_hex("channel-status word round-tripped", dut->r24_cs_o, 0x02000055u);
        ck("professional: cs_pro_o", dut->r24_pro_o, 1);
        ck("professional: emphasis byte0[4:2]", dut->r24_emph_o, 5);
        ck("professional: fs byte0[7:6]", dut->r24_fs_o, 1);
        ck("professional: no dialect mismatch", dut->r24_mism_o, 0);
        ck("consumer: cs_valid_o", dut->rc_csv_o, 1);
        ck("consumer: emphasis byte0[5:3] of the same word", dut->rc_emph_o, 2);
        ck("consumer: fs byte3[3:0] of the same word", dut->rc_fs_o, 2);
        ck("consumer: dialect MISMATCH flagged (bit0 says pro)", dut->rc_mism_o, 1);
    }

    // ================================================================ VBIT ==
    void v_bit_counts_and_never_gags_the_wire_truth() {
        printf("== [VBIT] V=1 counts, never gags the wire truth ==\n");
        uint32_t inv0 = dut->r24_inv_o;
        uint32_t pc0 = dut->r24_pairs_o;
        uint32_t par0 = dut->r24_par_o;
        uint32_t los0 = dut->r24_loss_o;
        dut->smp_invalid_i = 1;
        cyc(12 * FRAME_CLK);
        dut->smp_invalid_i = 0;
        cyc(4 * FRAME_CLK);
        ck("invalid_o counted the V=1 subframes", dut->r24_inv_o > inv0, 1);
        ck("pairs kept flowing while V was set", dut->r24_pairs_o > pc0 + 8, 1);
        ck("V=1 did not drop lock", dut->r24_lock_o, 1);
        ck("V=1 is not a parity error", dut->r24_par_o, par0);
        ck("V=1 is not a sync loss", dut->r24_loss_o, los0);
    }

    // ================================================================= ERR ==
    void a_biphase_violation_costs_lock_then_relocks() {
        printf("== [ERR] a real biphase violation costs lock, then re-locks ==\n");
        uint32_t loss1 = dut->r24_loss_o;
        for (int attempt = 0; attempt < 8 && dut->r24_lock_o; attempt++) {
            // two extra transitions
            dut->flip_i = 1;
            cyc(2);
            dut->flip_i = 0;
            run_until([this] { return dut->r24_lock_o == 0; }, 4 * FRAME_CLK);
        }
        cyc(32);                             // let the census pulse land too
        ck("locked_o dropped on the injected violation", dut->r24_lock_o, 0);
        ck("sync_loss_o counted it", dut->r24_loss_o > loss1, 1);
        // no pair may appear once the drop has settled through the CSR domain
        cyc(64);
        uint32_t pc1 = dut->r24_pairs_o;
        run_until([this] { return dut->r24_lock_o != 0; }, 1 * BLOCK_CLK / 2);
        ck("no pair emitted while unlocked", dut->r24_pairs_o, pc1);
        ck("still unlocked half a block later", dut->r24_lock_o, 0);
        long n = run_until([this] { return dut->r24_lock_o != 0; }, kLockBudgetClk);
        ck("re-locked by itself", dut->r24_lock_o, 1);
        ck("re-lock cost >= 2 clean blocks", n >= 2 * BLOCK_CLK - FRAME_CLK, 1);
        got24.clear();
        collect = true;
        cyc(16 * FRAME_CLK);
        collect = false;
        ck("pairs resumed after re-lock", static_cast<long>(got24.size()) >= 10, 1);
        long base2 = index_of(got24[0]);
        ck("resumed pairs are still ours", base2 >= 0, 1);
        long bad2 = 0;
        for (size_t i = 0; i < got24.size(); i++) {
            const Pair& e = pushed[static_cast<size_t>(base2) + i];
            if (got24[i].l != e.l || got24[i].r != e.r) bad2++;
        }
        ck("resumed pairs sample-exact and in order", bad2, 0);
    }

    // =============================================================== UNDER ==
    void starving_the_transmitter_keeps_the_line_legal() {
        printf("== [UNDER] starving the transmitter keeps the line legal ==\n");
        uint32_t und0 = dut->tx_under_o;
        uint32_t par1 = dut->r24_par_o;
        uint32_t los2 = dut->r24_loss_o;
        feed_left = 0;                       // stop handing pairs over
        cyc(20 * FRAME_CLK);                 // FIFO (depth 8) drains, then repeats
        got24.clear();
        collect = true;
        cyc(8 * FRAME_CLK);
        collect = false;
        ck("underrun_o confessed the repeats", dut->tx_under_o > und0, 1);
        ck("the far end kept lock through the underrun", dut->r24_lock_o, 1);
        ck("underrun is not a parity error", dut->r24_par_o, par1);
        ck("underrun is not a sync loss", dut->r24_loss_o, los2);
        long same = 0;
        for (size_t i = 1; i < got24.size(); i++)
            if (got24[i].l == got24[0].l && got24[i].r == got24[0].r) same++;
        ck("the starved link repeats the LAST pair", same >= 2, 1);
        ck("pairs still flow while starved", static_cast<long>(got24.size()) >= 4, 1);
        // RECOVERY. This check used to read `dut->pair_ready_o >= 0`, and
        // `pair_ready_o` is an unsigned Verilator word, so `>= 0` was always true
        // and the recovery it names was never tested. `-Wtype-limits` found it the
        // moment this suite was built with `-Wall -Wextra`.
        //
        // The instantaneous level is the WRONG thing to assert here even once the
        // comparison is fixed: `pair_ready_o` is `!src_full_w` (KL_aes3_tx.sv:147),
        // step() hands over a pair on every cycle the FIFO has room, and 8 frames
        // is far longer than the depth-8 FIFO takes to refill - so a healthy,
        // fully recovered transmitter reads back 0 here, and `== 1` fails. Proven,
        // not assumed: `== 1` was run against this DUT and reported
        // `got=0 exp=1`.
        //
        // What "accepting pairs again" means is that pairs were TAKEN during the
        // window, which is exactly what the feed counter records.
        constexpr long kRecoveryPairsOffered = 400;
        feed_left = kRecoveryPairsOffered;
        cyc(8 * FRAME_CLK);
        const long accepted_after_starve = kRecoveryPairsOffered - feed_left;
        ck("recovered: transmitter accepting pairs again", accepted_after_starve > 0, 1);
        ck("no parity error over the whole run", dut->r24_par_o, 0);
    }

    // ================================================================= end ==
    int report() {
        printf("--------------------------------------------------------------\n");
        printf("checks: %ld   failures: %ld\n", checks, fails);
        printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }

    const milan::tb::Model<Vaes3_wrap> model;
    Vaes3_wrap* dut = model.get();

    long checks = 0;
    long fails = 0;

    std::vector<Pair> pushed;          // pairs handed to the transmitter
    std::vector<Pair> got24;
    std::vector<Pair> got20;
    std::vector<Pair> got16;
    bool   collect = false;
    long   pairs_seen_unlocked = 0;
    bool   watch_unlocked = false;
    long feed_left = 0;                // pairs still to hand the transmitter
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Aes3SerdesHarness harness;
    return harness.run();
}
