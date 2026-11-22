// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for KL_tdm_render_master's lane width (#584): a lane
// of SLOTS_P rendered slots on a bus frame of BUS_SLOTS_P slots.
//
// The harness is the bus's timing owner: it drives bclk_rise_i, bclk_fall_i
// and frame_pos_i as KL_tdm_capture_master exports them, writes known samples
// into the bank on clk_i, commits frames, and decodes tdm_dout_o at the pins'
// own schedule (slot k bit b in bit period 1 + SLOT_BITS*k + b, launched on
// the fall inside it, so the rise that ENDS bit period p samples it). Every
// decoded frame is graded whole: each rendered slot carries its sample,
// 24-in-32 MSB first with zero padding, and every slot past the lane carries
// zero. The 8x8's lane is the first leg (one slot of a TDM32 bus, the first
// TDM render channel only); the shipping 1x1's full TDM8 lane is the
// regression leg, elaborated through the default BUS_SLOTS_P.
#include "Vtdm_render_master.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdint>
#include <cstdio>
#include <vector>

#ifndef LANE_SLOTS
#error "LANE_SLOTS (the lane's rendered slots) is set by the Makefile"
#endif
#ifndef LANE_BUS_SLOTS
#error "LANE_BUS_SLOTS (the bus frame's slots) is set by the Makefile"
#endif

namespace {

constexpr int kSlots     = LANE_SLOTS;
constexpr int kBusSlots  = LANE_BUS_SLOTS;
constexpr int kSlotBits  = 32;
constexpr int kFrame     = kBusSlots * kSlotBits;  // bit periods per frame
constexpr int kHalf      = 2;                      // clk_tdm cycles per bclk half
constexpr int kSettle    = 6;                      // frames to open the epoch
constexpr int kGraded    = 4;                      // decoded frames graded
constexpr std::uint32_t kMask24 = 0xFFFFFFu;

Vtdm_render_master* dut = nullptr;
int phase = 0;     // clk_tdm cycle within a bclk period
int pos   = 0;     // the timing owner's pre-edge frame position

// One clk_tdm cycle, with clk_i ticking twice as fast so the producer side
// runs as it does on the shipping divider plan (clk_i faster than clk_tdm).
// Returns the decoded bit when this cycle is a bclk rise, else -1.
int tdm_cycle() {
    const bool rise = (phase == 0);
    const bool fall = (phase == kHalf);
    dut->bclk_rise_i = rise;
    dut->bclk_fall_i = fall;
    dut->frame_pos_i = pos;
    const int sampled = rise ? dut->tdm_dout_o : -1;
    for (int k = 0; k < 2; ++k) {
        dut->clk_i = 0; dut->eval();
        dut->clk_i = 1; dut->eval();
    }
    dut->clk_tdm_i = 0; dut->eval();
    dut->clk_tdm_i = 1; dut->eval();
    if (rise) pos = (pos + 1) % kFrame;
    phase = (phase + 1) % (2 * kHalf);
    return sampled;
}

// One producer frame: every rendered slot written, then the commit.
void commit(const std::vector<std::uint32_t>& smp) {
    for (int s = 0; s < kSlots; ++s) {
        dut->smp_wr_en_i = 1;
        dut->smp_wr_slot_i = s;
        dut->smp_wr_data_i = smp[s] & kMask24;
        dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval();
    }
    dut->smp_wr_en_i = 0;
    dut->tick_i = 1;
    dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval();
    dut->tick_i = 0;
}

// Run whole bit periods until a complete frame has been decoded; returns the
// frame's slots as 32-bit words (MSB first, as the pins carry them).
std::vector<std::uint32_t> decode_frame() {
    // align: the rise whose pre-edge position is 1 samples bit period 1
    while (!(phase == 0 && pos == 1)) tdm_cycle();
    std::vector<std::uint32_t> slot(kBusSlots, 0);
    for (int n = 0; n < kFrame; ++n) {
        int bit = -1;
        while (bit < 0) bit = tdm_cycle();
        const int idx = n;  // bit period 1 + n
        slot[idx / kSlotBits] = (slot[idx / kSlotBits] << 1) | (bit & 1);
    }
    return slot;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vtdm_render_master> model;
    dut = model.get();
    char label[64];
    std::snprintf(label, sizeof label, "tdm_render_master %dof%d", kSlots, kBusSlots);
    milan::tb::Checker check{label};

    dut->rst_n = 0; dut->fresh_i = 1; dut->epoch_evt_i = 0;
    dut->smp_wr_en_i = 0; dut->tick_i = 0;
    for (int n = 0; n < 4 * kFrame; ++n) tdm_cycle();
    dut->rst_n = 1;
    for (int f = 0; f < kSettle; ++f)
        for (int n = 0; n < kFrame * 2 * kHalf; ++n) tdm_cycle();
    check.that("the render epoch opened (commit_en_o)", dut->commit_en_o);

    for (int g = 0; g < kGraded; ++g) {
        std::vector<std::uint32_t> smp(kSlots);
        for (int s = 0; s < kSlots; ++s)
            smp[s] = (0x800001u + 0x010203u * (g + 1) + 0x111111u * s) & kMask24;
        commit(smp);
        // the commit is adopted at the next frame start; the frame after it
        // is the first decoded whole from the new commit
        decode_frame();
        const std::vector<std::uint32_t> got = decode_frame();
        for (int s = 0; s < kBusSlots; ++s) {
            char what[96];
            const std::uint32_t want = (s < kSlots) ? (smp[s] << 8) : 0u;
            std::snprintf(what, sizeof what, "frame %d slot %d (%s)", g, s,
                          s < kSlots ? "rendered: sample, 24-in-32 MSB first" : "past the lane: zero");
            check.hex(what, got[s], want);
        }
    }
    check.dec("no commit overrun", dut->overruns_o, 0);
    check.that("frames serialized", dut->frames_o > kGraded);
    return check.report();
}
