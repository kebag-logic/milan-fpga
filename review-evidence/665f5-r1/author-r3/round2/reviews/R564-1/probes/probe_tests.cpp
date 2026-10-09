// Reviewer probes (R564-1). Each EXPECT states the clause-required outcome;
// a failing EXPECT is the observed deviation. Appended after the suite fixture.
static unsigned st(const Bytes &o){return unsigned(get(o,16,2)>>11);}
static Bytes once(aecp &a,Core &c,const Bytes &frame){
    c.sent.clear();aecp_rx(&a,0,frame.data(),frame.size());c.drain();
    return c.sent.empty()?Bytes():c.sent.front().second;
}
TEST_F(Core, P1_ReadDescriptorIgnoresConfigurationIndexForEntityAndConfiguration)
{
    for(unsigned type:{0u,1u})for(unsigned ci:{0u,1u,0xffffu}){
        auto b=target(ci,0,8);put(b,4,type,2);put(b,6,0,2);
        auto out=once(a,*this,command(4,b));ASSERT_FALSE(out.empty());
        printf("PROBE P1 type=%u cfg_in=0x%04x status=%u bytes=%zu cfg_out=0x%04x\n",type,ci,st(out),out.size(),unsigned(get(out,38,2)));
        EXPECT_EQ(st(out),0u)<<"IEEE 7.4.5.1: configuration_index ignored on receipt for ENTITY/CONFIGURATION";
        EXPECT_EQ(get(out,38,2),0u)<<"IEEE 7.4.5.2: configuration_index set to zero on transmit";
    }
}
TEST_F(Core, P2_SetStreamInfoIgnoresUnsettableFlagsAndAcceptsNoSubcommand)
{
    for(uint32_t flags:{0x20000000u,0x00000000u,0x20000004u,0x20000008u}){
        auto b=target(6,0,84);put(b,4,flags,4);put(b,24,flags?4321:0,4);
        auto out=once(a,*this,command(14,b));ASSERT_FALSE(out.empty());
        printf("PROBE P2 flags=0x%08x status=%u\n",flags,st(out));
        EXPECT_EQ(st(out),0u)<<"IEEE 7.4.15.1: SAVED_STATE/STREAMING_WAIT ignored in a command; Milan 5.4.2.9 refuses only unsupported sub-commands";
    }
}
TEST_F(Core, P3_HdcpApmCommandIsAcknowledgedNotImplemented)
{
    for(unsigned msg:{2u,4u,8u,14u}){
        auto f=command(0,Bytes(8),CTLR,0,msg);
        unsigned before=a.ignored;auto out=once(a,*this,f);
        printf("PROBE P3 message_type=%u responses=%zu ignored_delta=%u",msg,sent.size(),a.ignored-before);
        if(!out.empty())printf(" reply_type=%u status=%u",unsigned(out[15]&15),st(out));
        printf("\n");
        if(msg==8){EXPECT_FALSE(out.empty())<<"IEEE 9.7.4: each HDCP_APM_COMMAND shall be acknowledged (NOT_IMPLEMENTED)";}
    }
}
TEST_F(Core, P4_NotImplementedResponseSizes)
{
    for(unsigned cmd:{0x13u,0x0bu,0x2eu,0x3fffu}){
        auto out=ask(cmd,{},1);
        printf("PROBE P4 command=0x%04x status=%u control_data_length=%u\n",cmd,st(out),unsigned(get(out,16,2)&0x7ff));
    }
}
TEST_F(Core, P5_EntityAvailableIndexIsStatic)
{
    auto b=target(0,0,8);auto out=ask(4,b);
    printf("PROBE P5 entity available_index=%u (image constant; no ADP port exists)\n",unsigned(get(out,42+36,4)));
    SUCCEED();
}
