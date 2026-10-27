
// Reviewer probe (appended to a disposable copy of test_aecp.cpp; never committed).
// The lock in force after an expiry, asked from the last interface, by its owner's
// refresh, held however late, then one notification to every registered controller,
// then the lock retaken by its owner; GET_SYSTEM_UNIQUE_ID still answered meanwhile.
TEST_F(Core, ReviewerProbeUnlockedEdges)
{
    bool face=true;
    ON_CALL(mock,Applied).WillByDefault([&]{return face;});
    const unsigned last=AECP_TEST_INTERFACES-1u;
    register_controller(CTLR);register_controller(CTLR+1,last);
    ask(1,Bytes(16));
    face=false;ms=60000;sent.clear();drain();
    auto unlocks=[&]{return std::count_if(sent.begin(),sent.end(),[](auto&v){return get(v.second,36,2)==0x8001;});};
    EXPECT_EQ(unlocks(),0)<<"probe: no unlock notification before applied";
    auto av=ask(2,{},0,CTLR+1,last);
    EXPECT_EQ(get(av,38,4),2u)<<"probe: locked, asked on the last interface";
    EXPECT_EQ(get(av,50,8),CTLR)<<"probe: by its owner, asked on the last interface";
    auto refresh=ask(1,Bytes(16),AECP_ENTITY_MISBEHAVING);
    EXPECT_EQ(get(refresh,42,8),CTLR)<<"probe: owner's refresh refused naming the owner";
    Bytes g={0xc5,0x0a,0xc1,0,0,0,0,0};put(g,4,2,2);g.resize(16);
    auto gp=command(0x001b,g,CTLR+1,0,6);sent.clear();aecp_rx(&a,0,gp.data(),gp.size());drain();
    ASSERT_FALSE(sent.empty());
    EXPECT_EQ(get(sent.front().second,16,2)>>11,0u)<<"probe: GET_SYSTEM_UNIQUE_ID answered while held";
    ms+=600000;sent.clear();drain();
    EXPECT_EQ(unlocks(),0)<<"probe: however late, not notified";
    av=ask(2,{},0,CTLR+1);
    EXPECT_EQ(get(av,38,4),2u)<<"probe: still locked ten minutes later";
    EXPECT_EQ(get(ask(1,Bytes(16),AECP_ENTITY_LOCKED,CTLR+1),42,8),CTLR)<<"probe: still refused to another";
    face=true;sent.clear();drain();
    ASSERT_EQ(unlocks(),2)<<"probe: one notification to each registered controller";
    for(auto&[egress,out]:sent){
        if(get(out,36,2)!=0x8001)continue;
        EXPECT_EQ(get(out,16,2)>>11,0u);EXPECT_EQ(get(out,38,4),1u)<<"probe: UNLOCK flag";
        EXPECT_EQ(get(out,42,8),0u)<<"probe: no owner in the notification";
        EXPECT_EQ(egress,get(out,26,8)==CTLR+1?last:0u)<<"probe: each on its registration's interface";
    }
    EXPECT_EQ(get(ask(1,Bytes(16)),42,8),CTLR)<<"probe: the owner retakes it";
    uint64_t owner=0;EXPECT_TRUE(aecp_locked(&a,&owner));EXPECT_EQ(owner,CTLR);
}
