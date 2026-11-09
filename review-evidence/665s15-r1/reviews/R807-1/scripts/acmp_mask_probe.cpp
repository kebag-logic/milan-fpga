// Probe: tsn-c-stack's ACMP owed-release mask with ACMP_MAX_SINKS = 33 (the 32x32 simulation shape's sinks).
// A BIND_RX for sink 32 whose response cannot leave (no room) must hold sink 32's change and only sink 32's.
// Build: see acmp_mask_probe.sh. Compiled with ACMP_MAX_SINKS=33u and -fsanitize=shift.
#include <gtest/gtest.h>
#include <cstdio>
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
    for (unsigned k = 0; k < cfg.n_sinks; ++k) cfg.sink_interface[k] = k % 2u;
    cfg.n_sources = 2; cfg.source_interface[0] = 0; cfg.source_interface[1] = 1;
    for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) fk.source[i] = acmp_source_state{true, {kSid + i, kDa + i, 2u}, false};
    ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
}
static void bind(unsigned sink) {
    Pdu p; p.msg = spec::MSG_BIND_RX_COMMAND; p.controller = kCtl1; p.talker = kTkA; p.listener = kOwn;
    p.talker_uid = 1; p.listener_uid = static_cast<std::uint16_t>(sink); p.flags = 0; p.seq = 0x4100;
    auto f = acmpdu(p);
    acmp_rx(&a, sink % 2u, f.data(), f.size());
}
TEST(AcmpMask33, OwedResponseHoldsOnlyItsOwnSink) {
    static_assert(ACMP_MAX_SINKS == 33u, "the probe is for 33 sinks");
    setup();
    fk.room = false;
    bind(32);
    std::printf("after BIND_RX sink 32 with no room: change_owed[32]=%u change_owed[0]=%u pending(32)=%d pending(0)=%d\n",
                a.sinks[32].change_owed, a.sinks[0].change_owed, acmp_change_pending(&a, 32), acmp_change_pending(&a, 0));
    EXPECT_TRUE(acmp_change_pending(&a, 32)) << "sink 32's change waits behind its owed response (#653)";
    EXPECT_FALSE(acmp_change_pending(&a, 0)) << "sink 0, which owes nothing, is not held";
}
TEST(AcmpMask33, Sink0OwedDoesNotHoldSink32) {
    setup();
    fk.room = false;
    bind(0);
    std::printf("after BIND_RX sink 0 with no room: change_owed[0]=%u change_owed[32]=%u\n",
                a.sinks[0].change_owed, a.sinks[32].change_owed);
    EXPECT_FALSE(acmp_change_pending(&a, 32)) << "sink 32, which owes nothing, is not held";
}
