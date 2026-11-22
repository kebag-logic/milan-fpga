// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// #584: the 8x8's render lane - the first slot of a TDM32 bus - on its REAL
// timing owner, KL_tdm_capture_master, decoded at the pins alone. The owner's
// fsync is high at the bclk rise E(0) and slot 0's MSB is sampled one rise
// later, E(1) (dsp_a, one-bit data delay), so the rise n + 1 after the fsync
// rise samples bit n of the frame. Every decoded frame is graded whole: slot
// 0 carries the committed sample 24-in-32 MSB first, slots 1..31 carry zero.
#include "Vbus_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdint>
#include <cstdio>
#include <vector>

namespace {
constexpr int kBusSlots = 32;
constexpr int kFrame = kBusSlots * 32;
constexpr std::uint32_t kMask24 = 0xFFFFFFu;
Vbus_wrap* dut = nullptr;
int last_bclk = 0;
int bit_n = -1;                   // the frame bit the next rise samples, -1 = before the frame
std::vector<std::uint32_t> cur(kBusSlots, 0);
std::vector<std::vector<std::uint32_t>> frames;

// one clk_audio cycle, clk_i twice inside it; each bclk rise is decoded
void cycle() {
    for (int k = 0; k < 2; ++k) { dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); }
    dut->clk_audio_i = 0; dut->eval();
    dut->clk_audio_i = 1; dut->eval();
    const int b = dut->tdm_bclk_o;
    if (b && !last_bclk) {                 // a rise of the pin
        // bit n of a frame is sampled at E(1 + n), so its last bit, n = 1023,
        // is sampled at the next frame's E(0), the rise its fsync is high at
        if (bit_n >= 0 && bit_n < kFrame) {
            cur[bit_n / 32] = (cur[bit_n / 32] << 1) | (dut->tdm_dout_o & 1);
            ++bit_n;
        }
        if (dut->tdm_fsync_o) {            // E(0): the next rise samples bit 0
            if (bit_n == kFrame) frames.push_back(cur);
            bit_n = 0;
            cur.assign(kBusSlots, 0);
        }
    }
    last_bclk = b;
}

void commit(std::uint32_t smp) {
    dut->smp_wr_en_i = 1; dut->smp_wr_slot_i = 0; dut->smp_wr_data_i = smp & kMask24;
    dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval();
    dut->smp_wr_en_i = 0; dut->tick_i = 1;
    dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval();
    dut->tick_i = 0;
}
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vbus_wrap> model;
    dut = model.get();
    milan::tb::Checker check{"tdm_render_master 1of32 on the capture master"};
    dut->rst_n = 0;
    for (int n = 0; n < 64; ++n) cycle();
    dut->rst_n = 1;
    for (int n = 0; n < 8 * 2 * kFrame; ++n) cycle();
    check.that("the render epoch opened on the owner's frames (commit_en_o)", dut->commit_en_o);
    const std::uint32_t samples[3] = {0x800001u, 0x7FFFFEu, 0x123456u};
    for (std::uint32_t smp : samples) {
        commit(smp);
        frames.clear();
        for (int n = 0; n < 4 * 2 * kFrame; ++n) cycle();
        if (!check.that("whole frames decoded at the pins", frames.size() >= 3)) continue;
        const auto& f = frames.back();
        char what[96];
        std::snprintf(what, sizeof what, "slot 0 carries 0x%06X, 24-in-32 MSB first", smp);
        check.hex(what, f[0], smp << 8);
        unsigned nonzero = 0;
        for (int s = 1; s < kBusSlots; ++s) nonzero += f[s] != 0;
        check.dec("slots 1..31 past the lane carry zero", nonzero, 0);
    }
    check.that("frames serialized", dut->frames_o > 8);
    return check.report();
}
