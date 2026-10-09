// R564-2 reviewer probes, appended after the exact-head test_aecp.cpp. Each prints
// what it observed; EXPECTs state the outcome this round's assignment requires.
static unsigned q_status(const Bytes &o){return unsigned(get(o,16,2)>>11);}
TEST_F(Core, Q1_PersistentlyUnavailableSnapshotRetriesAtTimerPaceOnly)
{
    register_controller();sent.clear();unsigned reads=0,busy=0;
    ON_CALL(mock,Stream).WillByDefault([&](unsigned,uint16_t,uint16_t,aecp_stream_info*v){++reads;*v={};return false;});
    aecp_changed(&a,5,0,1);
    for(unsigned t=0;t<1000;++t){ms=t;for(unsigned k=0;k<5;++k)busy+=aecp_poll(&a);}
    printf("PROBE Q1 reads=%u over 1000 ms with 5 polls/ms busy_polls=%u sent=%zu\n",reads,busy,sent.size());
    EXPECT_LE(reads,1001u)<<"retry is paced by its 1 ms timer, not by poll rate";
    EXPECT_EQ(busy,0u)<<"a failed snapshot alone lets the loop sleep";
    EXPECT_NE(events[&desc(5)-descriptors.data()].pending&1u,0u)<<"event retained";
}
TEST_F(Core, Q2_SetStreamInfoWithoutSubcommandReportsCurrentLatency)
{
    auto b=target(6,0,84);put(b,4,0x20000000,4);put(b,24,111,4);ask(14,b);
    put(b,4,0,4);put(b,24,999,4);auto out=ask(14,b);
    printf("PROBE Q2 no-subcommand status=%u flags=0x%08x latency=%u stored=%u\n",q_status(out),
           unsigned(get(out,42,4)),unsigned(get(out,62,4)),unsigned(latency[0]));
    EXPECT_EQ(get(out,62,4),111u)<<"no sub-command: current latency, request ignored";
    EXPECT_EQ(latency[0],111u);
}
TEST_F(Core, Q3_RootConfigurationAbsentIndexNormalizesAndRefuses)
{
    auto b=target(1,0,8);put(b,4,1,2);put(b,6,1,2);auto out=ask(4,b,2);
    printf("PROBE Q3 CONFIGURATION idx1 cfg_in=1 status=%u cfg_out=%u\n",q_status(out),unsigned(get(out,38,2)));
    EXPECT_EQ(get(out,38,2),0u);
}
TEST_F(Core, Q4_HdcpExactFixedHeaderIsAnswered)
{
    auto request=command(0,Bytes(4),CTLR,0,8);sent.clear();
    aecp_rx(&a,0,request.data(),request.size());drain();
    printf("PROBE Q4 hdcp 28-byte pdu responses=%zu\n",sent.size());
    ASSERT_EQ(sent.size(),1u);EXPECT_EQ(sent[0].second[15],9u);EXPECT_EQ(q_status(sent[0].second),1u);
}
TEST_F(Core, Q5_LockQueryInsideOwnPortIsRefusedWithoutWriting)
{
    uint64_t owner=0x1234;bool result=true;unsigned before=a.reentries;
    ON_CALL(mock,Changed).WillByDefault([&](aecp_change,uint16_t,uint16_t){result=aecp_locked(&a,&owner);});
    auto body=target(26,0,5);body[4]=255;ask(24,body);
    printf("PROBE Q5 locked_result=%d owner=0x%llx reentries_delta=%u\n",result,(unsigned long long)owner,a.reentries-before);
    EXPECT_FALSE(result);EXPECT_EQ(owner,0x1234u);EXPECT_EQ(a.reentries-before,1u);
}
