// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// The MAAP allocation's CSR output (maap_csr.c) on a host register window.
// The Annex B core's cases are the TSN stack's own (#697): the tsn-c-stack
// submodule's tests/test_maap.cpp, linked into the same binary by the maap arm
// (ctrl_arms.MAAP_BINARIES).
#include <gtest/gtest.h>
#include <array>
#include <cstdint>
#include <cstring>
#include <vector>

#include "fw_gtest.hpp"
#include "maap.h"
#include "maap_csr.h"

FW_TALLY_LABEL("ctrl MAAP Annex B");

namespace {
constexpr std::uint64_t kBase = 0x91e0f0000100ULL;

struct CsrRig {
    std::array<std::uint32_t, 1024> regs{};
    std::array<std::uint64_t, 8> streams{};
    std::vector<std::array<std::uint32_t, 3>> writes;
    maap_csr output{};
    maap_csr_port port{};
    CsrRig() {
        port.ctx = this;
        port.read32 = [](void* ctx, unsigned, std::uint32_t offset) { return static_cast<CsrRig*>(ctx)->regs.at(offset / 4); };
        port.write32 = [](void* ctx, unsigned interface, std::uint32_t offset, std::uint32_t value) {
            auto& r = *static_cast<CsrRig*>(ctx);
            r.writes.push_back({interface, offset, value});
            // REGISTER_MAP 0x800: listener DMAC words are read-only.
            if ((offset == 0x81c || offset == 0x820) && !(r.regs[0x800 / 4] & 0x100u)) return;
            r.regs.at(offset / 4) = value;
            auto k = r.regs[0x800 / 4] & 15;
            if (offset == 0x81c) r.streams.at(k) = (r.streams.at(k) & 0xffff00000000ULL) | value;
            if (offset == 0x820) r.streams.at(k) = (static_cast<std::uint64_t>(value) << 32) | (r.streams.at(k) & 0xffffffffULL);
        };
    }
};

TEST(MaapCsr, EveryStreamAddressAndLossGate) {
    CsrRig r; r.regs[0x6cc / 4] = 0x12340803; r.regs[0x800 / 4] = 0x201;
    ASSERT_TRUE(maap_csr_init(&r.output, r.port, 8, true, 0x20001, 3));
    maap_csr_allocation(&r.output, 2, kBase, 9, true);
    EXPECT_EQ(r.regs[0x658 / 4], 0xf0000100u); EXPECT_EQ(r.regs[0x65c / 4], 0x91e0u);
    for (unsigned k = 1; k < 8; ++k) EXPECT_EQ(r.streams[k], kBase + k) << "stream destination base plus index";
    EXPECT_EQ(r.regs[0x75c / 4], 0xf0000108u); EXPECT_EQ(r.regs[0x760 / 4], 0x91e0u);
    EXPECT_EQ(r.regs[0x800 / 4], 0x201u) << "selection restored";
    EXPECT_EQ(r.regs[0x6cc / 4], 0x12340802u) << "fabric MAAP disabled without touching seed";
    ASSERT_GE(r.writes.size(), 4u);
    EXPECT_EQ(r.writes[0][1], 0x654u); EXPECT_EQ(r.writes[0][2], 0x20000u);
    EXPECT_EQ(r.writes[1][1], 0x750u); EXPECT_EQ(r.writes[1][2], 2u);
    EXPECT_EQ(r.regs[0x654 / 4], 0x20001u); EXPECT_EQ(r.regs[0x750 / 4], 3u);
    for (const auto& w : r.writes) EXPECT_EQ(w[0], 2u) << "interface stays attached";
    maap_csr_allocation(&r.output, 2, kBase, 0, false);
    EXPECT_EQ(r.regs[0x654 / 4], 0x20000u); EXPECT_EQ(r.regs[0x750 / 4], 2u) << "loss closes both media gates";
}

TEST(MaapCsr, ShapesAndCountRefusal) {
    CsrRig r;
    EXPECT_FALSE(maap_csr_init(&r.output, r.port, 9, false, 1, 0));
    EXPECT_FALSE(maap_csr_init(&r.output, r.port, 0, false, 0, 0));
    ASSERT_TRUE(maap_csr_init(&r.output, r.port, 1, false, 1, 0));
    maap_csr_allocation(&r.output, 0, kBase, 2, true);
    EXPECT_EQ(r.output.refused, 1u); EXPECT_EQ(r.regs[0x654 / 4], 0u) << "wrong shape stays disabled";
    maap_csr_allocation(&r.output, 0, kBase, 1, true);
    EXPECT_EQ(r.regs[0x654 / 4], 1u); EXPECT_EQ(r.regs[0x75c / 4], 0u);
    ASSERT_TRUE(maap_csr_init(&r.output, r.port, 0, true, 0, 3));
    maap_csr_allocation(&r.output, 0, kBase + 3, 1, true);
    EXPECT_EQ(r.regs[0x75c / 4], 0xf0000103u) << "CRF only shape";
}

// R528-1-F4: inspect the whole trace, not just its final register image.
TEST(MaapCsr, AdmissionAfterEveryDestinationWrite) {
    CsrRig r;
    ASSERT_TRUE(maap_csr_init(&r.output, r.port, 8, true, 1, 1));
    maap_csr_allocation(&r.output, 0, kBase, 9, true);
    unsigned destinations = 0;
    unsigned enables = 0;
    for (unsigned k = 0; k < r.writes.size(); ++k) {
        const auto offset = r.writes[k][1];
        const auto value = r.writes[k][2];
        if (offset == 0x658 || offset == 0x65c || offset == 0x81c ||
            offset == 0x820 || offset == 0x75c || offset == 0x760) {
            EXPECT_EQ(enables, 0u) << "no destination write after admission opens";
            ++destinations;
        }
        if ((offset == 0x654 || offset == 0x750) && (value & 1u)) {
            EXPECT_EQ(destinations, 18u) << "enables follow every destination word";
            EXPECT_GE(k, r.writes.size() - 2u) << "AAF and CRF enables are last";
            ++enables;
        }
    }
    EXPECT_EQ(destinations, 18u); EXPECT_EQ(enables, 2u);
}
} // namespace
