// Reviewer probe (R528-1): IEEE 1722-2016 Table B.7 note a.
// A range supplied with Begin! must be used and generate_address not called.
// maap.h line 76-77 promises the same. Begin! with a valid preferred range
// while the port is not operational, then PortOperational!.
#include <gtest/gtest.h>
#include <cstdint>
#include <vector>
#include "maap.h"

namespace {
constexpr std::uint64_t kMac = 0x020000000080ULL;
constexpr std::uint64_t kBase = 0x91e0f0000100ULL;
struct Rig {
    maap core{};
    maap_ports ports{};
    std::vector<std::uint64_t> published;
    Rig() {
        ports.ctx = this;
        ports.send = [](void*, unsigned, const std::uint8_t*, std::size_t) { return true; };
        ports.timer_start = [](void*, unsigned, std::uint32_t) {};
        ports.timer_stop = [](void*, unsigned) {};
        ports.range = [](void* c, unsigned, std::uint64_t base, std::uint16_t n, bool) {
            if (n) static_cast<Rig*>(c)->published.push_back(base);
        };
        ports.clock = [](void*) -> std::uint32_t { return 17; };
        EXPECT_TRUE(maap_init(&core, &ports, 0, kMac, 8));
    }
};
}  // namespace

TEST(ReviewerProbe, PreferredRangeUsedWhenLinkAlreadyUp) {
    Rig r;
    ASSERT_TRUE(maap_begin(&r.core, kBase));
    EXPECT_EQ(r.core.base, kBase);
}

TEST(ReviewerProbe, PreferredRangeSurvivesBeginWhileLinkDown) {
    Rig r;
    maap_port_operational(&r.core, false);
    ASSERT_TRUE(maap_begin(&r.core, kBase)) << "Begin! with a valid preferred range is accepted";
    maap_port_operational(&r.core, true);
    ASSERT_EQ(r.core.state, MAAP_PROBE);
    EXPECT_EQ(r.core.base, kBase) << "Table B.7 note a: supplied range used, generate_address not called; base="
                                  << std::hex << r.core.base;
}
