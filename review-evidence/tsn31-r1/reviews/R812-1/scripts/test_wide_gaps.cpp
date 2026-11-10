// SPDX-License-Identifier: MIT
// Disposable reviewer probe (not proposed source): two 33-sink behaviours of the owed-release mask
// that the PR's acmp_wide tests do not exercise. Built like acmp_wide: ACMP_MAX_SINKS=33u,
// -fsanitize=shift,undefined with no recovery. Fixture copied from tests/test_acmp_wide.cpp.
#include <gtest/gtest.h>

#include <cstdint>

#include "acmp.h"
#include "acmp_fake.hpp"

using namespace acmp_test;

extern "C" void ctrl_reentry_assert(const char* module) { static_cast<void>(module); }

namespace {

class WideGaps : public ::testing::Test {
 protected:
    void SetUp() override {
        ASSERT_EQ(ACMP_MAX_SINKS, 33u);
        fk = Fake{};
        cfg = acmp_config{};
        cfg.entity_id = kOwn;
        cfg.n_interfaces = 2;
        cfg.mac[0] = kMac0;
        cfg.mac[1] = kMac1;
        cfg.n_sinks = ACMP_MAX_SINKS;
        for (unsigned k = 0; k < ACMP_MAX_SINKS; ++k) cfg.sink_interface[k] = static_cast<std::uint8_t>(k % 2u);
        cfg.n_sources = 2;
        cfg.source_interface[0] = 0;
        cfg.source_interface[1] = 1;
        for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) fk.source[i] = acmp_source_state{true, {kSid + i, kDa + i, 2u}, false};
        ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
    }
    bool command(std::uint8_t msg, unsigned sink, std::uint16_t seq) {
        Pdu p;
        p.msg = msg;
        p.controller = kCtl1;
        p.talker = kTkA;
        p.listener = kOwn;
        p.talker_uid = 1;
        p.listener_uid = static_cast<std::uint16_t>(sink);
        p.seq = seq;
        auto f = acmpdu(p);
        return acmp_rx(&a, a.sinks[sink].interface, f.data(), f.size());
    }
    acmp a{};
    acmp_config cfg{};
};

// A frame that releases nothing, owed in a slot that earlier held sink 32's response, must not hold sink 32.
TEST_F(WideGaps, ReusedSlotCarriesNoStaleReleaseBit) {
    fk.room = false;
    command(spec::MSG_BIND_RX_COMMAND, 32u, 0x4100);
    ASSERT_TRUE(a.owed_count == 2u && a.sinks[32].change_owed == 1u);
    fk.room = true;
    acmp_poll(&a);
    acmp_poll(&a);
    ASSERT_TRUE(a.owed_count == 0u && a.sinks[32].change_owed == 0u);
    fk.room = false;
    for (unsigned i = 0; i < ACMP_OWED_MAX - 1u; ++i) {
        ASSERT_TRUE(command(spec::MSG_GET_RX_STATE_COMMAND, 5u, static_cast<std::uint16_t>(0x4200 + i)));
    }
    ASSERT_EQ(a.owed_count, ACMP_OWED_MAX - 1u);
    EXPECT_EQ(a.sinks[32].change_owed, 0u) << "GAP1 sink 32 held by a GET_RX_STATE response in its old slot";
    EXPECT_FALSE(acmp_change_pending(&a, 32u)) << "GAP1 no change of sink 32 is pending";
}

// Sink 31 is the last bit of word 0: its change waits behind its own owed response and is released by it.
TEST_F(WideGaps, SinkThirtyOneIsHeldByItsOwnResponse) {
    fk.room = false;
    command(spec::MSG_BIND_RX_COMMAND, 31u, 0x4300);
    EXPECT_TRUE(acmp_change_pending(&a, 31u) && a.sinks[31].change_owed == 1u) << "GAP2 sink 31 waits behind its response";
    EXPECT_FALSE(acmp_change_pending(&a, 32u)) << "GAP2 sink 32 is not held by sink 31's response";
    fk.room = true;
    acmp_poll(&a);
    EXPECT_TRUE(!acmp_change_pending(&a, 31u) && a.sinks[31].change_owed == 0u) << "GAP2 sink 31 released by its response";
}

}  // namespace
