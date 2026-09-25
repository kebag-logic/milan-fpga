// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Issue #546: public-output checks of timestamp-era isolation. Expected
// rates come from the stimulus's interval sum, never from DUT internals.
#include "VKL_crf_rx.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <array>
#include <cstdint>

namespace {
class DiscontinuityHarness {
 public:
    int run() {
        check.echo_passes();
        reset();
        fill(200, false);
        marker(true);
        marker(false);
        for (const int64_t jump : std::array<int64_t, 10>{
                 21000, -21000, 150000, -150000, 1000000000, -1000000000,
                 4294967296LL, -4294967296LL, 4294968296LL, -4294968296LL})
            step(jump);
        spacing_limits();
        rejected_markers();
        pending_collision();
        lifecycle();
        return check.report();
    }
 private:
    milan::tb::Model<VKL_crf_rx> dut;
    milan::tb::Checker check{"crf_rx discontinuity"};
    uint64_t ts = 10'000'000'000ULL;
    uint8_t seq = 0;
    static constexpr uint64_t kSid = 0x0200000000010001ULL;

    void tick() {
        dut->clk_i = 0; dut->eval();
        dut->clk_i = 1; dut->eval();
    }
    void reset() {
        dut->rst_n = 0; dut->en_i = 0; dut->stop_i = 0;
        dut->frame_p_i = 0; dut->sid_i = kSid;
        dut->subtype_i = 4; dut->type_i = 1;
        dut->sid_frame_i = kSid; dut->pullbase_i = 48000;
        dut->mr_i = 0; dut->tu_i = 0;
        tick(); tick(); dut->rst_n = 1; dut->en_i = 1; tick();
    }
    void fields() {
        dut->seq_i = seq;
        dut->fsh_i = (uint64_t{8} << 48) | (uint64_t{96} << 32) | (ts >> 32);
        dut->fsh2_i = ts << 32;
        // Deliberately jitter arrival time: it cannot change source spacing.
        dut->ptp_now_i = ts - (seq % 2 ? 100 : 1'900'000);
    }
    void send(int64_t spacing = 2'000'200) {
        ts += static_cast<uint64_t>(spacing);
        fields(); dut->frame_p_i = 1; tick();
        dut->frame_p_i = 0; tick(); tick(); ++seq;
    }
    void fill(int drift, bool tu) {
        dut->tu_i = tu;
        for (int n = 0; n < 256; ++n) {
            send(2'000'000 + drift);
            check.that("initial history stays invalid for 256 timestamps", !dut->rate_valid_o);
        }
        send(2'000'000 + drift);
        check.that("257th timestamp publishes a valid sample", dut->rate_valid_o);
        check.that("rate equals 256 source intervals minus nominal",
                   static_cast<int32_t>(dut->rate_o) == 256 * drift);
    }
    void refill(int drift = 200) {
        const auto held = dut->rate_o;
        bool isolated = true;
        for (int n = 1; n < 256; ++n) {
            send(2'000'000 + drift);
            isolated &= !dut->rate_valid_o && dut->rate_o == held;
        }
        check.that("all 255 crossing intervals are withheld", isolated);
        send(2'000'000 + drift);
        check.that("exactly 256 new intervals restore validity", dut->rate_valid_o);
        check.that("first clean rate excludes the phase jump",
                   static_cast<int32_t>(dut->rate_o) == 256 * drift);
    }
    void marker(bool tu) {
        const auto held = dut->rate_o;
        dut->tu_i = tu;
        ts += 2'001'200; // 1 us phase step: below the backstop, marker alone
        fields(); dut->frame_p_i = 1; dut->clk_i = 0; dut->eval();
        check.that("tu edge invalidates before the sampling edge", !dut->rate_valid_o);
        tick(); dut->frame_p_i = 0; tick(); ++seq;
        check.that("tu edge holds the published rate", dut->rate_o == held);
        check.that("tu edge leaves receiver locked", dut->locked_o);
        refill(); // includes a whole clean window with tu held high
        check.dec("tu edges never count a media unlock", dut->cnt_unlocked_o, 0);
    }
    void step(int64_t jump) {
        const auto held = dut->rate_o;
        send(2'000'200 + jump);
        check.that("unmarked timestamp jump invalidates the rate", !dut->rate_valid_o);
        check.that("unmarked timestamp jump cannot publish", dut->rate_o == held);
        check.that("unmarked timestamp jump preserves receiver lock", dut->locked_o);
        refill();
    }
    void spacing_limits() {
        // Inclusive detector boundary, checked at nominal rate. These are
        // isolated phase offsets, so subsequent periods return to 2 ms.
        reset(); fill(0, true);
        for (const int delta : {-2048, 2048}) {
            send(2'000'000 + delta);
            check.that("2048 ns boundary remains valid", dut->rate_valid_o);
            send(2'000'000);
        }
        for (const int delta : {-2049, 2049}) {
            send(2'000'000 + delta);
            check.that("2049 ns boundary is rejected", !dut->rate_valid_o);
            refill(0);
        }
        // Legitimate extremes combine 100 ppm media and 200 ppm PHC.
        for (const int drift : {-601, 601}) {
            bool valid = true;
            for (int n = 0; n < 257; ++n) {
                send(2'000'000 + drift); valid &= dut->rate_valid_o;
            }
            check.that("combined legitimate rate extremes are never rejected", valid);
            check.that("legitimate rate changes still propagate",
                       static_cast<int32_t>(dut->rate_o) == 256 * drift);
        }
    }
    void rejected_markers() {
        const auto held = dut->rate_o;
        dut->tu_i = !dut->tu_i;
        dut->type_i = 0;
        fields(); dut->frame_p_i = 1; tick();
        dut->frame_p_i = 0; tick();
        check.that("malformed marker cannot invalidate", dut->rate_valid_o);
        dut->type_i = 1; dut->sid_frame_i = kSid + 1;
        dut->frame_p_i = 1; tick(); dut->frame_p_i = 0; tick();
        check.that("foreign marker cannot invalidate", dut->rate_valid_o);
        check.dec("rejected frames cannot change rate", dut->rate_o, held);
        dut->sid_frame_i = kSid; dut->tu_i = !dut->tu_i;
        send();
        check.that("rejected marker never seeds the reference", dut->rate_valid_o);
    }
    void pending_collision() {
        reset(); fill(200, false);
        const auto held = dut->rate_o;
        ts += 2'000'300; fields(); dut->frame_p_i = 1; tick(); ++seq;
        // A clean rate is pending in the BRAM read pipeline. The very
        // next cycle carries a sub-threshold jump and a tu transition.
        ts += 2'001'200; dut->tu_i = 1; fields(); tick(); ++seq;
        dut->frame_p_i = 0; tick(); tick();
        check.that("back-to-back marker cancels pending publication", dut->rate_o == held);
        check.that("back-to-back marker leaves invalid history", !dut->rate_valid_o);
        refill();
    }
    void lifecycle() {
        ++seq; send(4'000'400);
        check.that("lost PDU cannot poison a 256-PDU rate", !dut->rate_valid_o);
        refill();
        --seq; send();
        check.that("duplicate PDU restarts the rate history", !dut->rate_valid_o);
        refill();
        dut->stop_i = 1; dut->eval();
        check.that("STOP gates sample validity immediately", !dut->rate_valid_o);
        dut->stop_i = 0;
        for (int n = 0; n < 20005; ++n) tick();
        check.that("silence invalidates the old rate", !dut->rate_valid_o);
        fill(200, false);
        dut->en_i = 0; tick(); dut->en_i = 1; tick();
        check.that("rebind invalidates old history", !dut->rate_valid_o);
        fill(-100, true);
        reset();
        check.that("reset invalidates history", !dut->rate_valid_o);
        ts = UINT64_MAX - 10'000'000;
        fill(200, false);
        check.that("natural 64-bit rollover preserves clean spacing", dut->rate_valid_o);
    }
};
} // namespace
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    DiscontinuityHarness harness;
    return harness.run();
}
