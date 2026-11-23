// Review probes for issue #969 (not part of the PR). Compiled beside the tree's own srp_mbx.cpp, whose fixtures they use.
// 1. The external round's probes, verbatim (r886_1_probes.inc).
// 2. The internal round's stale-count probes, verbatim (r885_1_stale_count_probe.inc).
// 3. This round's own probes (RvProbe*), below.
#include "srp_mbx.cpp"
#include "r886_1_probes.inc"
namespace {
#include "r885_1_stale_count_probe.inc"
}

namespace {
class RvProbe : public SrpEarlyTalker {
protected:
    // one legal vector of `count` Talker Advertise JoinIn values from stream `first` on (35.2.2.8.4)
    std::vector<uint8_t> vec(unsigned first, unsigned count) {
        auto f = talker(first, kAdvertise, kJoinIn);
        f.resize(46u);
        wire_put_be(f.data() + 19, count, 2);
        wire_put_be(f.data() + 17, 29u + (count + 2u) / 3u, 2);
        for (unsigned k = 0; k < count; k += 3u) {
            f.push_back(static_cast<uint8_t>(36u + (k + 1u < count ? 6u : 0u) + (k + 2u < count ? 1u : 0u)));
        }
        f.insert(f.end(), {0, 0, 0, 0});
        return f;
    }
    void every_input_declares(const std::string &words) {
        for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) expect_bound_declares(k, k, kAdvertise, words);
    }
};

// At the bound (every place taken by unrelated Talkers, then refreshed so nothing is pending), a reset, then one
// vector of every input: the reset's zeroing alone must free every place.
TEST_F(RvProbe, AtTheBoundRefreshedThenResetThenFullVector) {
    settle(); advance(400);
    offer(vec(0x80u, CTRL_SRP_SINKS)); quiet(400);
    offer(vec(0x80u, CTRL_SRP_SINKS)); quiet(400);
    ASSERT_EQ(adapter.kept_count[0], CTRL_SRP_SINKS);
    mbx_model_set_link(&model, 0, false); settle(); mbx_model_set_link(&model, 0, true); settle(); advance(400);
    offer(vec(0u, CTRL_SRP_SINKS)); quiet(400);
    every_input_declares("at the bound, refreshed, reset: one vector of every input is kept");
}

// A kept Talker ages out through the participant's own LeaveAll with the talker silent (Registrar IN -> LV -> MT, an
// indication), its block is reclaimed, then one vector of every input: every place must be free again.
TEST_F(RvProbe, KeptAgedOutByLeaveAllThenFullVector) {
    settle(); advance(400);
    offer(talker(0xe0u, kAdvertise, kJoinIn)); quiet(400);
    offer(talker(0xe0u, kAdvertise, kJoinIn)); quiet(400);   // refreshed: nothing pending
    ASSERT_EQ(adapter.kept_count[0], 1u);
    quiet(22000);                                              // past a LeaveAll period and the leave timer
    offer(vec(0u, CTRL_SRP_SINKS)); quiet(400);
    every_input_declares("aged out by LeaveAll, reclaimed: one vector of every input is kept");
}

// A reset of the other interface leaves this interface's kept count as it was (2 interfaces only).
TEST_F(RvProbe, OtherInterfaceResetKeepsThisCount) {
    if (MBX_N_IF < 2) GTEST_SKIP() << "one interface";
    settle(); advance(400);
    offer(talker(0xe0u, kAdvertise, kJoinIn)); quiet(400);
    ASSERT_EQ(adapter.kept_count[0], 1u);
    mbx_model_set_link(&model, MBX_N_IF - 1, false); settle();
    mbx_model_set_link(&model, MBX_N_IF - 1, true); settle(); advance(400);
    EXPECT_EQ(adapter.kept_count[0], 1u) << "interface 0's kept count after interface 1's reset";
    EXPECT_EQ(adapter.kept_count[MBX_N_IF - 1], 0u) << "interface 1's count zeroed";
    offer(vec(0u, CTRL_SRP_SINKS - 1u)); quiet(400);
    for (unsigned k = 0; k + 1u < CTRL_SRP_SINKS; ++k) expect_bound_declares(k, k, kAdvertise, "beside the one kept");
}
}
