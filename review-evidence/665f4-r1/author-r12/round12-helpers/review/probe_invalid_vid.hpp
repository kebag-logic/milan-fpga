// Reviewer probe (R532-9): appended to srp_binding.hpp in a disposable copy.
// One PROBE_TX_RESPONSE whose stream_vlan_id is 0 (outside 1..4094): count how
// long the composed loop refuses to sleep with no further input, and what
// ACMP and SRP each report meanwhile.
namespace {
class SrpBindingVidProbe : public SrpBinding {};
TEST_F(SrpBindingVidProbe, InvalidVidKeepsTheLoopAwakeWithoutInput) {
    bind(0);
    auto invalid=answer(0); invalid.vlan=0;
    ASSERT_TRUE(offer(invalid,spec::MULTICAST_MAC,acfg.sink_interface[0]));
    settle();
    unsigned awake=0, first_sleep=0;
    for (unsigned ms=0; ms<12000u; ++ms) {
        mbx_model_advance_ms(&model,1u);
        for (unsigned n=0;n<4u;++n) {
            if (ctrl_loop_service(&app.loop)!=0u) { ++awake; } else { if (!first_sleep) first_sleep=ms+1u; break; }
        }
        if (ms==5000u) {
            std::printf("  probe: t=5 s acmp state %d (6=SETTLED_NO_RSV) srp bound %d request pending %d\n",
                        static_cast<int>(core()->sinks[0].state),sink(0).bound,app.srp_requests[0].pending);
        }
    }
    std::printf("  probe: 12 s without input: %u non-idle passes, first idle pass at %u ms, owed passes %u\n",
                awake,first_sleep,static_cast<unsigned>(app.loop.stats.owed_passes));
    EXPECT_LT(first_sleep,100u) << "PROBE-VID the loop sleeps soon after a permanently refused binding";
}
} // namespace
