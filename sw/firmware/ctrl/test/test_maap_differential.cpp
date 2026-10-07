// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Shared stimulus, separate Annex B and legacy-fabric expectations (#686).
#include <gtest/gtest.h>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

#include "VKL_maap.h"
#include "verilator_harness.hpp"
#include "fw_gtest.hpp"
#include "maap.h"

FW_TALLY_LABEL("MAAP core and parent wire differential");

namespace {
using Frame = std::array<std::uint8_t, 60>;
constexpr std::uint64_t kMac = 0x020000000080ULL;
constexpr std::uint64_t kBase = 0x91e0f0000100ULL;

void put(Frame& f, unsigned at, unsigned bytes, std::uint64_t value) {
    for (unsigned k = 0; k < bytes; ++k) f[at + bytes - 1 - k] = static_cast<std::uint8_t>(value >> (8 * k));
}

Frame input(unsigned type, std::uint64_t peer, unsigned offset = 0x100) {
    Frame f{}; put(f, 0, 6, type == 2 ? kMac : MAAP_MULTICAST); put(f, 6, 6, peer);
    f[12] = 0x22; f[13] = 0xf0; f[14] = 0xfe; f[15] = static_cast<std::uint8_t>(type);
    f[16] = 8; f[17] = 16; put(f, 26, 6, MAAP_POOL_BASE + offset); f[33] = 8;
    if (type == 2) { put(f, 34, 6, MAAP_POOL_BASE + offset); f[41] = 8; }
    return f;
}

struct Software {
    maap core{};
    maap_ports ports{};
    std::vector<Frame> frames;
    Software() {
        ports.ctx = this;
        ports.send = [](void* ctx, unsigned, const std::uint8_t* data, std::size_t n) {
            auto& r = *static_cast<Software*>(ctx); Frame f{};
            std::memcpy(f.data(), data, n); r.frames.push_back(f); return true;
        };
        ports.timer_start = [](void*, unsigned, std::uint32_t) {};
        ports.timer_stop = [](void*, unsigned) {};
        ports.range = [](void*, unsigned, std::uint64_t, std::uint16_t, bool) {};
        ports.clock = [](void*) -> std::uint32_t { return 17; };
        EXPECT_TRUE(maap_init(&core, &ports, 0, kMac, 8));
    }
    void begin() { EXPECT_TRUE(maap_begin(&core, kBase)); }
    void acquire() { begin(); for (unsigned k = 0; k < 3; ++k) maap_timer_expired(&core); }
    void receive(const Frame& f) { maap_rx(&core, f.data(), f.size()); }
};

struct Fabric {
    const milan::tb::Model<VKL_maap> model;
    std::vector<Frame> frames;
    Frame pending{};
    unsigned bytes = 0;
    unsigned cycles = 0;
    Fabric() {
        model->station_mac_i = kMac; model->count_i = 8;
        model->seed_offset_i = 0x100; model->seed_valid_i = 1;
        model->enable_i = 0; model->rx_tvalid_i = 0; model->rx_tready_i = 1;
        model->m_axis_tready = 1; model->rst_n = 0; step(6); model->rst_n = 1; step(3);
    }
    void step(unsigned n = 1) {
        for (unsigned k = 0; k < n; ++k) {
            model->clk_i = 0; model->eval();
            if (model->m_axis_tvalid && model->m_axis_tready) {
                for (unsigned j = 0; j < 8; ++j) {
                    if (model->m_axis_tkeep & (1u << j)) {
                        if (bytes < pending.size()) pending[bytes] = static_cast<std::uint8_t>(model->m_axis_tdata >> (j * 8));
                        ++bytes;
                    }
                }
                if (model->m_axis_tlast) {
                    EXPECT_EQ(bytes, 60u); frames.push_back(pending); pending = {}; bytes = 0;
                }
            }
            model->clk_i = 1; model->eval(); ++cycles;
        }
    }
    void begin() { model->enable_i = 1; step(3); }
    void frames_until(unsigned n, unsigned budget = 80000) {
        for (unsigned k = 0; k < budget && frames.size() < n; ++k) step();
        ASSERT_GE(frames.size(), n) << "parent produces expected output";
    }
    void acquire() { begin(); frames_until(4); ASSERT_EQ(model->state_o, 2u); }
    void receive(const Frame& f) {
        for (unsigned at = 0; at < 60; at += 8) {
            std::uint64_t word = 0;
            for (unsigned k = 0; k < 8 && at + k < 60; ++k) word |= static_cast<std::uint64_t>(f[at + k]) << (8 * k);
            model->rx_tdata_i = word; model->rx_tkeep_i = at == 56 ? 15 : 255;
            model->rx_tvalid_i = 1; model->rx_tlast_i = at == 56; step();
        }
        model->rx_tvalid_i = 0; model->rx_tlast_i = 0; step(50);
    }
};

TEST(MaapDifferential, ProbeSequenceWireAndCadence) {
    Software s; Fabric f; s.acquire(); f.acquire();
    ASSERT_EQ(s.frames.size(), 5u); ASSERT_EQ(f.frames.size(), 4u);
    for (unsigned k = 0; k < 5; ++k) {
        EXPECT_EQ(s.frames[k], input(k == 4 ? 3u : 1u, kMac)) << "Annex B core wire";
    }
    for (unsigned k = 0; k < 3; ++k) {
        Frame legacy = s.frames[k]; legacy[17] = 28;
        EXPECT_EQ(f.frames[k], legacy) << "raw PROBE differs only in known parent length";
    }
    Frame legacy = s.frames.back(); legacy[17] = 28;
    EXPECT_EQ(f.frames.back(), legacy) << "raw ANNOUNCE differs only in known parent length";
    EXPECT_EQ(s.frames[3][15], 1u); EXPECT_EQ(f.frames[3][15], 3u);
    EXPECT_GT(s.core.last_delay_ms, 30000u);
    auto start = f.cycles; f.frames_until(5);
    EXPECT_LT(f.cycles - start, 51000u) << "parent 3 second announcement deviation retained";
    std::puts("DIFF #686: core initial+3 retransmissions, parent 3 total; CDL 16/28; announce 30-32 s/3-5.047 s");
}

class DifferentialCell : public ::testing::TestWithParam<int> {};
TEST_P(DifferentialCell, SharedConflict) {
    const auto key = GetParam(); const unsigned state = key / 3, type = key % 3 + 1;
    Software s; Fabric f;
    if (state == 1) { s.begin(); f.begin(); }
    if (state == 2) { s.acquire(); f.acquire(); }
    auto stimulus = input(type, 0x060000000040ULL);
    auto before = s.frames.size(); auto parent_before = f.frames.size();
    s.receive(stimulus); f.receive(stimulus);
    if (state == 0) {
        EXPECT_EQ(s.frames.size(), before); EXPECT_EQ(f.frames.size(), parent_before);
        return;
    }
    if (state == 2 && type == 1) {
        ASSERT_EQ(s.frames.size(), before + 1); ASSERT_EQ(f.frames.size(), parent_before + 1);
        Frame legacy = s.frames.back(); put(legacy, 0, 6, MAAP_MULTICAST); legacy[17] = 28;
        EXPECT_EQ(f.frames.back(), legacy) << "raw DEFEND known destination and length differences";
    } else {
        EXPECT_EQ(s.core.state, MAAP_PROBE); EXPECT_EQ(s.core.conflicts, 1u);
        EXPECT_FALSE(s.core.valid); EXPECT_EQ(s.frames.back()[15], 1u);
        if (type == 3) {
            EXPECT_EQ(f.model->conflicts_o, 0u) << "parent ignores ANNOUNCE requested range";
        } else {
            EXPECT_EQ(f.model->state_o, 1u); EXPECT_EQ(f.model->conflicts_o, 1u);
            f.frames_until(parent_before + 1);
            const auto& a = s.frames.back(); const auto& b = f.frames.back();
            for (unsigned byte = 0; byte < 60; ++byte) {
                if (byte == 17 || (byte >= 26 && byte < 32)) continue;
                EXPECT_EQ(a[byte], b[byte]) << "retry wire, excluding CDL and independent random allocation";
            }
        }
    }
    std::printf("DIFF state=%u input=%u core-conflicts=%u parent-conflicts=%u\n",
                state, type, s.core.conflicts, f.model->conflicts_o);
}
INSTANTIATE_TEST_SUITE_P(AllStates, DifferentialCell, ::testing::Range(0, 9));

TEST(MaapDifferential, ReleaseAndRetry) {
    Software s; Fabric f; s.acquire(); f.acquire();
    maap_release(&s.core); f.model->enable_i = 0; f.step(20);
    EXPECT_EQ(s.core.state, MAAP_INITIAL); EXPECT_EQ(f.model->state_o, 0u);
    EXPECT_FALSE(s.core.valid); EXPECT_FALSE(f.model->addr_valid_o);
    s.begin(); f.begin();
    EXPECT_EQ(s.core.base, kBase); EXPECT_EQ(f.model->offset_o, 0x100u);
    EXPECT_EQ(s.core.state, MAAP_PROBE); EXPECT_EQ(f.model->state_o, 1u);
}
} // namespace
