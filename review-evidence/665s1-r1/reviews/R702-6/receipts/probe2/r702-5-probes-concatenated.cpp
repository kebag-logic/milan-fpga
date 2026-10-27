
// ---- review probe (appended to a scratch copy of test_aecp.cpp; not part of the tree) ----
// After an automatic lock expiry whose LOCK_HELD release the platform has not
// applied, what do ENTITY_AVAILABLE and a foreign LOCK_ENTITY report?
namespace {
Bytes probe_send(Core &t, unsigned cmd, Bytes body, uint64_t controller)
{
    t.sent.clear();auto b=command(cmd,body,controller,0);aecp_rx(&t.a,0,b.data(),b.size());t.drain();
    return t.sent.empty()?Bytes():t.sent.front().second;
}
}
TEST_F(Core, ReviewProbeReadsDuringAPendingRelease)
{
    bool face=true;
    ON_CALL(mock,Applied).WillByDefault([&]{return face;});
    register_controller(CTLR+1);ask(1,Bytes(16),0,CTLR+1);ASSERT_TRUE(a.locked);
    auto ea=probe_send(*this,2,Bytes(16),CTLR+2);ASSERT_FALSE(ea.empty());
    std::printf("PROBE control-locked ENTITY_AVAILABLE status=%u flags=%u lock_owner=%llx\n",(unsigned)(get(ea,16,2)>>11),
                (unsigned)get(ea,38,4),(unsigned long long)get(ea,50,8));
    EXPECT_EQ(get(ea,38,4),2u)<<"control: a held lock reads as locked";
    face=false;ms=60000;drain();
    std::printf("PROBE after-expiry core_locked=%d unlocked_pending=%d\n",(int)a.locked,(int)a.unlocked);
    ea=probe_send(*this,2,Bytes(16),CTLR+2);ASSERT_FALSE(ea.empty());
    std::printf("PROBE pending-release ENTITY_AVAILABLE status=%u flags=%u lock_owner=%llx\n",(unsigned)(get(ea,16,2)>>11),
                (unsigned)get(ea,38,4),(unsigned long long)get(ea,50,8));
    auto lk=probe_send(*this,1,Bytes(16),CTLR+2);ASSERT_FALSE(lk.empty());
    std::printf("PROBE pending-release foreign LOCK_ENTITY status=%u locked_id=%llx\n",(unsigned)(get(lk,16,2)>>11),
                (unsigned long long)get(lk,42,8));
    EXPECT_EQ(get(ea,38,4),2u)<<"ruling item 3: a read reports the last acknowledged LOCK_HELD (locked) while its release is pending";
    EXPECT_EQ(get(ea,50,8),CTLR+1)<<"and the acknowledged owner";
    face=true;drain();
    ea=probe_send(*this,2,Bytes(16),CTLR+2);
    std::printf("PROBE after-applied ENTITY_AVAILABLE flags=%u lock_owner=%llx\n",(unsigned)get(ea,38,4),(unsigned long long)get(ea,50,8));
    EXPECT_EQ(get(ea,38,4),0u)<<"control: released once applied";
}

// ---- review probe (appended to a scratch copy of test_aecp.cpp; not part of the tree) ----
// At two interfaces, a change asked on interface 1 that waits for the platform
// must have its final response leave on interface 1, even after a read on
// interface 0 answered meanwhile.
TEST_F(Core, ReviewProbeWaitingResponseLeavesOnItsOwnInterface)
{
    if (AECP_TEST_INTERFACES < 2) GTEST_SKIP();
    bool face=true,late=true;
    ON_CALL(mock,Applied).WillByDefault([&]{return face;});
    ON_CALL(mock,Changed).WillByDefault([&](aecp_change,uint16_t,uint16_t){face=face&&!late;});
    Bytes identify=target(26,0,5);identify[4]=255;
    ask(24,identify,AECP_IN_PROGRESS,CTLR,1);
    std::printf("PROBE in-progress egress=%u\n",sent.empty()?99u:sent.front().first);
    ask(25,target(26,0),0,CTLR+7,0);
    late=false;face=true;sent.clear();drain();
    ASSERT_FALSE(sent.empty());
    std::printf("PROBE final status=%u egress=%u src_mac=%llx\n",(unsigned)(get(sent[0].second,16,2)>>11),sent[0].first,
                (unsigned long long)get(sent[0].second,6,6));
    EXPECT_EQ(get(sent[0].second,16,2)>>11,0u);
    EXPECT_EQ(sent[0].first,1u)<<"the final response leaves on the interface the command came in on";
}
