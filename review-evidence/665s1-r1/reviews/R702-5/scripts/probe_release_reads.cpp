
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
