// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#include <gtest/gtest.h>
#include <csignal>
#include <cstdlib>
#include "fw_gtest.hpp"
#include "maap.h"

FW_TALLY_LABEL("ctrl MAAP debug port contract");

TEST(MaapDebug, SynchronousExpiryAsserts) {
    maap core{};
    maap_ports ports{};
    ports.ctx = &core;
    ports.clock = [](void*) -> std::uint32_t { return 1; };
    ports.range = [](void*, unsigned, std::uint64_t, std::uint16_t, bool) {};
    ports.timer_start = [](void* ctx, unsigned, std::uint32_t) { maap_timer_expired(static_cast<maap*>(ctx)); };
    ports.timer_stop = [](void*, unsigned) {};
    ports.send = [](void*, unsigned, const std::uint8_t*, std::size_t) { return true; };
    ASSERT_TRUE(maap_init(&core, &ports, 0, 0x020000000001ULL, 8));
    EXPECT_EXIT({
        // The expected child abort must not invoke the tally's crash reporter.
        std::signal(SIGABRT, SIG_DFL);
        (void)maap_begin(&core, MAAP_POOL_BASE);
        std::_Exit(0);
    }, ::testing::KilledBySignal(SIGABRT), "in_call") << "debug reentry assertion";
}
