// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R302-1, #546): false-positive safety of the KL_crf_rx
// discontinuity detector. Expected rate is the stimulus's own 256-interval
// timestamp sum; nothing is read from DUT internals.
#include "VKL_crf_rx.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdint>
#include <cstdio>
#include <deque>

namespace {
constexpr uint64_t kSid = 0x0200000000010001ULL;
constexpr int64_t kNom = 2'000'000;

class JitterProbe {
 public:
    int run() {
        for (const int drift : {-601, 0, 601})
            for (const int jit : {384, 640})
                jitter_run(drift, jit, false);
        jitter_run(601, 640, true);   // tu held high the whole time
        tu_only_edges();
        return check.report();
    }
 private:
    milan::tb::Model<VKL_crf_rx> dut;
    milan::tb::Checker check{"r302 jitter probe"};
    uint64_t base = 10'000'000'000ULL;   // ideal (jitter-free) source time
    uint8_t seq = 0;
    uint32_t rng = 0x12345678u;
    std::deque<uint64_t> hist;

    int32_t rnd(int span) {             // uniform in [-span, +span]
        rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5;
        return static_cast<int32_t>(rng % (2u * span + 1u)) - span;
    }
    void tick() { dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); }
    void reset() {
        dut->rst_n = 0; dut->en_i = 0; dut->stop_i = 0; dut->frame_p_i = 0;
        dut->sid_i = kSid; dut->sid_frame_i = kSid; dut->subtype_i = 4;
        dut->type_i = 1; dut->pullbase_i = 48000; dut->mr_i = 0; dut->tu_i = 0;
        tick(); tick(); dut->rst_n = 1; dut->en_i = 1; tick();
        hist.clear();
    }
    void send(uint64_t ts) {
        dut->seq_i = seq++;
        dut->fsh_i = (uint64_t{8} << 48) | (uint64_t{96} << 32) | (ts >> 32);
        dut->fsh2_i = ts << 32;
        dut->ptp_now_i = ts - 500'000;
        dut->frame_p_i = 1; tick(); dut->frame_p_i = 0; tick(); tick();
        hist.push_back(ts);
        if (hist.size() > 257) hist.pop_front();
    }
    int32_t expected_rate() const {
        return static_cast<int32_t>(hist.back() - hist.front() - 256 * kNom);
    }
    void jitter_run(int drift, int jit, bool tu_high) {
        reset(); dut->tu_i = tu_high;
        bool valid_ok = true, rate_ok = true;
        for (int n = 0; n < 12000; ++n) {
            base += static_cast<uint64_t>(kNom + drift);
            send(base + static_cast<uint64_t>(static_cast<int64_t>(rnd(jit))));
            if (n >= 256) {
                valid_ok &= dut->rate_valid_o;
                rate_ok &= static_cast<int32_t>(dut->rate_o) == expected_rate();
            }
        }
        char what[160];
        std::snprintf(what, sizeof what,
                      "drift %d ns/interval, +/-%d ns per-timestamp jitter%s: never invalid",
                      drift, jit, tu_high ? ", tu held high" : "");
        check.that(what, valid_ok);
        std::snprintf(what, sizeof what,
                      "drift %d, jitter +/-%d%s: rate equals source interval sum",
                      drift, jit, tu_high ? ", tu high" : "");
        check.that(what, rate_ok);
    }
    // A legitimate tu edge with NO timestamp step: one full refill of 256
    // intervals is withheld, then validity and an exact rate return.
    void tu_only_edges() {
        reset();
        for (int n = 0; n < 300; ++n) { base += kNom + 100; send(base); }
        check.that("tu-only: valid before edge", dut->rate_valid_o);
        for (const bool level : {true, false, true, false}) {
            dut->tu_i = level;
            base += kNom + 100; send(base);
            int invalid = !dut->rate_valid_o;
            for (int n = 0; n < 400; ++n) {
                base += kNom + 100; send(base);
                if (!dut->rate_valid_o) ++invalid;
            }
            check.dec("tu-only edge withholds exactly 256 accepted PDUs", invalid, 256);
            check.that("tu-only edge: valid again", dut->rate_valid_o);
            check.dec("tu-only edge: exact rate after refill",
                      static_cast<uint32_t>(dut->rate_o), 256u * 100u);
            check.dec("tu-only edge: no unlock", dut->cnt_unlocked_o, 0);
        }
    }
};
}  // namespace
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    JitterProbe probe;
    return probe.run();
}
