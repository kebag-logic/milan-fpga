// SPDX-License-Identifier: MIT
// Review probe: at ACMP_MAX_SINKS sinks, the last sink's owed PROBE_TX must name that sink in probe_of.
#include <gtest/gtest.h>

#include <cstdint>

#include "acmp.h"
#include "acmp_fake.hpp"

using namespace acmp_test;

extern "C" void ctrl_reentry_assert(const char* module) {
    static_cast<void>(module);
}

TEST(ProbeOfBound, LastSinksOwedProbeNamesIt) {
    fk = Fake{};
    acmp a{};
    acmp_config cfg{};
    cfg.entity_id = kOwn;
    cfg.n_interfaces = 2;
    cfg.mac[0] = kMac0;
    cfg.mac[1] = kMac1;
    cfg.n_sinks = ACMP_MAX_SINKS;
    for (unsigned k = 0; k < ACMP_MAX_SINKS; ++k) {
        cfg.sink_interface[k] = static_cast<std::uint8_t>(k % 2u);
    }
    cfg.n_sources = 2;
    cfg.source_interface[0] = 0;
    cfg.source_interface[1] = 1;
    for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) {
        fk.source[i] = acmp_source_state{true, {kSid + i, kDa + i, 2u}, false};
    }
    ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
    const unsigned last = ACMP_MAX_SINKS - 1u;
    fk.room = false;
    Pdu p;
    p.msg = spec::MSG_BIND_RX_COMMAND;
    p.controller = kCtl1;
    p.talker = kTkA;
    p.listener = kOwn;
    p.talker_uid = 1;
    p.listener_uid = static_cast<std::uint16_t>(last);
    p.seq = 0x4100;
    auto f = acmpdu(p);
    static_cast<void>(acmp_rx(&a, a.sinks[last].interface, f.data(), f.size()));
    ASSERT_EQ(a.owed_count, 2u) << "probe: the response and the probe are owed";
    const unsigned probe_slot = (a.owed_head + 1u) % ACMP_OWED_MAX;
    EXPECT_EQ(static_cast<unsigned>(a.owed[probe_slot].probe_of), last + 1u)
        << "probe: the owed probe names sink " << last;
    EXPECT_TRUE(acmp_change_pending(&a, last) && a.sinks[last].change_owed == 1u)
        << "probe: the last sink waits behind its own response";
    fk.room = true;
    static_cast<void>(acmp_poll(&a));
    static_cast<void>(acmp_poll(&a));
    EXPECT_TRUE(a.owed_count == 0u && !acmp_change_pending(&a, last)) << "probe: drained and released";
}
