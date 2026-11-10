// SPDX-License-Identifier: MIT
// Review probe: at ACMP_MAX_SINKS = N, a BIND_RX for each sink k with no transmit room must hold sink k's change
// and no other sink's; the poll that sends k's response must release k's change alone (issue 31, ACMP-09).
#include <gtest/gtest.h>
#include "acmp.h"
#include "acmp_fake.hpp"
using namespace acmp_test;
extern "C" void ctrl_reentry_assert(const char*) {}
static acmp a;
static acmp_config cfg;
static void setup() {
    fk = Fake{};
    cfg = acmp_config{};
    cfg.entity_id = kOwn; cfg.n_interfaces = 2; cfg.mac[0] = kMac0; cfg.mac[1] = kMac1;
    cfg.n_sinks = ACMP_MAX_SINKS;
    for (unsigned k = 0; k < cfg.n_sinks; ++k) cfg.sink_interface[k] = static_cast<std::uint8_t>(k % 2u);
    cfg.n_sources = 2; cfg.source_interface[0] = 0; cfg.source_interface[1] = 1;
    for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) fk.source[i] = acmp_source_state{true, {kSid + i, kDa + i, 2u}, false};
    ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
}
static void bind(unsigned sink, std::uint16_t seq) {
    Pdu p; p.msg = spec::MSG_BIND_RX_COMMAND; p.controller = kCtl1; p.talker = kTkA; p.listener = kOwn;
    p.talker_uid = 1; p.listener_uid = static_cast<std::uint16_t>(sink); p.seq = seq;
    auto f = acmpdu(p);
    acmp_rx(&a, sink % 2u, f.data(), f.size());
}
TEST(EverySink, EachOwedResponseHoldsOnlyItsOwnSink) {
    for (unsigned k = 0; k < ACMP_MAX_SINKS; ++k) {
        setup();
        fk.room = false;
        bind(k, 0x4100);
        for (unsigned j = 0; j < ACMP_MAX_SINKS; ++j) {
            ASSERT_EQ(a.sinks[j].change_owed, j == k ? 1u : 0u) << "bind of sink " << k << ": change_owed of sink " << j;
        }
        fk.room = true;
        fk.clear();
        acmp_poll(&a);
        ASSERT_EQ(fk.count(Call::CHANGED), 1u) << "sink " << k;
        ASSERT_EQ(fk.calls[static_cast<std::size_t>(fk.position(Call::CHANGED, 0))].index, k) << "sink " << k;
        for (unsigned j = 0; j < ACMP_MAX_SINKS; ++j) {
            ASSERT_EQ(a.sinks[j].change_owed, 0u) << "after release of sink " << k << ": sink " << j;
        }
    }
}
// Slot reuse: fill the owed set with responses of high sinks, drain it, then owe a low sink's response in the same
// slots; no stale bit of an earlier frame may hold another sink.
TEST(EverySink, ReusedSlotsCarryNoStaleBits) {
    setup();
    fk.room = false;
    unsigned hi = ACMP_MAX_SINKS - 1u;
    for (unsigned r = 0; r < 4u; ++r) bind(hi - r, static_cast<std::uint16_t>(0x4200 + r));
    fk.room = true;
    while (acmp_poll(&a)) {}
    for (unsigned j = 0; j < ACMP_MAX_SINKS; ++j) ASSERT_EQ(a.sinks[j].change_owed, 0u) << "drained: sink " << j;
    fk.room = false;
    for (unsigned r = 0; r < 4u; ++r) bind(r, static_cast<std::uint16_t>(0x4300 + r));
    for (unsigned j = 0; j < ACMP_MAX_SINKS; ++j)
        ASSERT_EQ(a.sinks[j].change_owed, j < 4u ? 1u : 0u) << "reused slots: sink " << j;
}
