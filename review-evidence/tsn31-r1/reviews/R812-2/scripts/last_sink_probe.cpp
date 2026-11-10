// SPDX-License-Identifier: MIT
// Reviewer probe (issue 31): at ACMP_MAX_SINKS = N, the last sink's BIND_RX with no transmit room owes its response
// and a probe whose probe_of is N (one plus index N - 1); both leave, the probe's sink is found, and no sink is held.
#include <gtest/gtest.h>
#include "acmp.h"
#include "acmp_fake.hpp"
using namespace acmp_test;
extern "C" void ctrl_reentry_assert(const char*) {}
static acmp a;
static acmp_config cfg;
TEST(LastSink, ProbeOfTheLastSinkIsNamedAndLeaves) {
    fk = Fake{}; cfg = acmp_config{};
    cfg.entity_id = kOwn; cfg.n_interfaces = 2; cfg.mac[0] = kMac0; cfg.mac[1] = kMac1; cfg.n_sinks = ACMP_MAX_SINKS;
    for (unsigned k = 0; k < cfg.n_sinks; ++k) cfg.sink_interface[k] = static_cast<std::uint8_t>(k % 2u);
    cfg.n_sources = 2; cfg.source_interface[0] = 0; cfg.source_interface[1] = 1;
    for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) fk.source[i] = acmp_source_state{true, {kSid + i, kDa + i, 2u}, false};
    ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
    const unsigned last = ACMP_MAX_SINKS - 1u;
    Pdu p; p.msg = spec::MSG_BIND_RX_COMMAND; p.controller = kCtl1; p.talker = kTkA; p.listener = kOwn;
    p.talker_uid = 1; p.listener_uid = static_cast<std::uint16_t>(last); p.seq = 0x4100;
    auto f = acmpdu(p);
    fk.room = false;
    acmp_rx(&a, last % 2u, f.data(), f.size());
    ASSERT_EQ(a.owed_count, 2u);
    EXPECT_EQ(unsigned(a.owed[(a.owed_head + 1u) % ACMP_OWED_MAX].probe_of), ACMP_MAX_SINKS) << "probe_of names the last sink";
    EXPECT_EQ(unsigned(a.sinks[last].change_owed), 1u);
    fk.room = true; fk.clear();
    while (acmp_poll(&a)) {}
    EXPECT_EQ(a.owed_count, 0u);
    unsigned held = 0; for (unsigned k = 0; k < ACMP_MAX_SINKS; ++k) held += a.sinks[k].change_owed;
    EXPECT_EQ(held, 0u);
    EXPECT_EQ(fk.count(Call::CHANGED), 1u);
    EXPECT_EQ(fk.calls[static_cast<std::size_t>(fk.position(Call::CHANGED, 0))].index, last);
}
