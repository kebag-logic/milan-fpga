
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
