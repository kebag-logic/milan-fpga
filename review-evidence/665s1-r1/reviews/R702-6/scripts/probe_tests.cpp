
// ---- external review probes, appended to a scratch copy of test_aecp.cpp only ----
// P1: the owner's unlock waits for the face across the lock's sixty-second
// deadline and is then acknowledged: exactly one unlock notification, the lock
// released with no owner, no second (expiry) notification.
TEST_F(Core, ReviewProbeOwnerUnlockWaitsAcrossExpiryThenTaken)
{
    bool face=true;
    bool late=false;
    ON_CALL(mock,Applied).WillByDefault([&]{return face;});
    ON_CALL(mock,Changed).WillByDefault([&](aecp_change,uint16_t,uint16_t){face=face&&!late;});
    register_controller(CTLR+1);ask(1,Bytes(16));ASSERT_TRUE(a.locked);
    auto unlocks=[&]{return std::count_if(sent.begin(),sent.end(),[](auto&v){return get(v.second,36,2)==0x8001;});};
    ms=59990;drain();
    late=true;Bytes unlock(16);put(unlock,0,1,4);ask(1,unlock,AECP_IN_PROGRESS);
    ASSERT_TRUE(a.waiting);
    ms=60020;sent.clear();drain();
    EXPECT_TRUE(a.waiting)<<"PROBE the wait still holds past the old deadline";
    EXPECT_EQ(unlocks(),0)<<"PROBE nothing notified while waiting";
    late=false;face=true;sent.clear();drain();
    EXPECT_FALSE(a.waiting);
    EXPECT_EQ(unlocks(),1)<<"PROBE one unlock notification once taken";
    EXPECT_FALSE(a.locked);EXPECT_FALSE(a.unlocked);EXPECT_EQ(a.lock_owner,0u)<<"PROBE released, no owner";
    sent.clear();ms=60200;drain();EXPECT_EQ(unlocks(),0)<<"PROBE no second notification";
    auto available=ask(2,{},0,CTLR+1);
    EXPECT_EQ(get(available,38,4),0u)<<"PROBE ENTITY_AVAILABLE unlocked";EXPECT_EQ(get(available,50,8),0u);
}

// P2: as P1, but the wait fails: the unlock is refused ENTITY_MISBEHAVING, the
// lock then expires and holds by its owner until applied, then exactly one
// expiry notification and the owner dropped.
TEST_F(Core, ReviewProbeOwnerUnlockWaitsAcrossExpiryThenFails)
{
    bool face=true;
    bool late=false;
    ON_CALL(mock,Applied).WillByDefault([&]{return face;});
    ON_CALL(mock,Changed).WillByDefault([&](aecp_change,uint16_t,uint16_t){face=face&&!late;});
    register_controller(CTLR+1);ask(1,Bytes(16));ASSERT_TRUE(a.locked);
    auto unlocks=[&]{return std::count_if(sent.begin(),sent.end(),[](auto&v){return get(v.second,36,2)==0x8001;});};
    ms=59990;drain();
    late=true;Bytes unlock(16);put(unlock,0,1,4);ask(1,unlock,AECP_IN_PROGRESS);
    ASSERT_TRUE(a.waiting);
    ms=59990+AECP_WAIT_MS;sent.clear();drain();
    EXPECT_FALSE(a.waiting)<<"PROBE the wait failed";
    bool misbehaving=std::any_of(sent.begin(),sent.end(),[](auto&v){return get(v.second,36,2)==1u&&(get(v.second,16,2)>>11)==AECP_ENTITY_MISBEHAVING;});
    EXPECT_TRUE(misbehaving)<<"PROBE the unlock answered ENTITY_MISBEHAVING";
    sent.clear();drain();
    EXPECT_FALSE(a.locked)<<"PROBE released to the platform after the wait";
    EXPECT_EQ(a.lock_owner,CTLR)<<"PROBE held by its owner until applied";
    EXPECT_EQ(unlocks(),0)<<"PROBE not notified unapplied";
    auto available=ask(2,{},0,CTLR+1);
    EXPECT_EQ(get(available,38,4),2u)<<"PROBE ENTITY_AVAILABLE locked";EXPECT_EQ(get(available,50,8),CTLR);
    EXPECT_EQ(get(ask(1,Bytes(16),AECP_ENTITY_LOCKED,CTLR+1),42,8),CTLR)<<"PROBE other refused naming owner";
    late=false;face=true;sent.clear();drain();
    EXPECT_EQ(unlocks(),1)<<"PROBE one expiry notification once applied";
    EXPECT_EQ(a.lock_owner,0u);EXPECT_FALSE(a.unlocked);
    sent.clear();ms+=60000;drain();EXPECT_EQ(unlocks(),0)<<"PROBE once";
    EXPECT_EQ(get(ask(1,Bytes(16),0,CTLR+1),42,8),CTLR+1)<<"PROBE another controller takes it";
}

// P3: GET_SYSTEM_UNIQUE_ID while a change waits answers SUCCESS with the value
// in force; a SET with the value already in force is still refused.
TEST_F(Core, ReviewProbeSystemIdReadWhileWaiting)
{
    bool face=true;
    bool late=false;
    ON_CALL(mock,Applied).WillByDefault([&]{return face;});
    ON_CALL(mock,Changed).WillByDefault([&](aecp_change,uint16_t,uint16_t){face=face&&!late;});
    constexpr uint64_t IN_FORCE=0x0102030405060708;
    EXPECT_EQ(get(set_system_id(IN_FORCE),16,2)>>11,0u);
    late=true;Bytes identify=target(26,0,5);identify[4]=255;ask(24,identify,AECP_IN_PROGRESS);
    ASSERT_TRUE(a.waiting);
    Bytes body={0xc5,0x0a,0xc1,0,0,0,0,0};put(body,4,2,2);body.resize(16);
    auto p=command(0x001b,body,CTLR,0,6);sent.clear();aecp_rx(&a,0,p.data(),p.size());drain();
    ASSERT_FALSE(sent.empty());
    EXPECT_EQ(get(sent.front().second,16,2)>>11,0u)<<"PROBE GET answered";
    EXPECT_EQ(get(sent.front().second,46,8),IN_FORCE)<<"PROBE GET value in force";
    EXPECT_EQ(get(set_system_id(IN_FORCE),16,2)>>11,AECP_ENTITY_MISBEHAVING)<<"PROBE same-value SET refused while waiting";
}
