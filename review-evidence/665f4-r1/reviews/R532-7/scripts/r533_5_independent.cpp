// Independent mailbox-boundary probes for the round-5 dependency delta.
#include "srp_fixture.hpp"
namespace fw_test { const char *tally_label() { return "independent dependency seams"; } }

TEST_F(Srp, ReviewAtomicInvalidSuffixCannotStartTalker) {
    settle();
    auto f=frame(3,identity(),0,2);
    f.resize(f.size()-2);
    f.insert(f.end(),{4,4,0,10,0,1,6});
    const auto before=adapter.malformed;
    offer(f);
    EXPECT_EQ(adapter.malformed,before+1);
    EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    EXPECT_CALL(licence,Change(0,0,false));
}

TEST_F(Srp, ReviewFutureUnknownMessageKeepsFollowingKnownListener) {
    settle();
    auto f=frame(3,identity(),0,2);
    f[14]=1;
    f.insert(f.begin()+15,{99,1,0,3,250,255,1});
    EXPECT_CALL(licence,Change(0,0,true)); offer(f);
    EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_EQ(adapter.malformed,0u);
    EXPECT_CALL(licence,Change(0,0,false));
}

TEST_F(Srp, ReviewChangedListenerInLvIndicatesBeforePoll) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    offer(frame(3,identity(),4,2,true));
    ASSERT_TRUE(adapter.ifs[0].active[0]);
    receive_before_poll(frame(3,identity(),1,1));
    EXPECT_FALSE(adapter.ifs[0].registered[0]);
    EXPECT_TRUE(adapter.ifs[0].stop_owed[0]);
    EXPECT_CALL(licence,Change(0,0,false)); settle();
    EXPECT_FALSE(adapter.ifs[0].active[0]);
}

TEST_F(Srp, ReviewWithdrawDuringExhaustionSurvivesRecovery) {
    settle(); advance(400);
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    ASSERT_TRUE(adapter.ifs[0].active[0]);
    std::vector<void*> held;
    while(void *p=ctrl_pool_alloc(&pool,1)) held.push_back(p);
    ASSERT_GT(held.size(),0u);
    EXPECT_CALL(licence,Change(0,0,false));
    offer(frame(3,identity(),5,2));
    for(void *p:held) ctrl_pool_free(&pool,p);
    advance(10);
    std::cout << "withdraw/recovery: active=" << adapter.ifs[0].active[0]
              << " received=" << adapter.received << " malformed=" << adapter.malformed
              << " stops=" << adapter.stops << std::endl;
    EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_EQ(adapter.stops,1u);
}
