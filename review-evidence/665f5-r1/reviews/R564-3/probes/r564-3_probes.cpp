// R564-3 reviewer probes, appended to the exact-head test_aecp.cpp Core fixture.
// S1: a SET_STREAM_INFO with no XXX_VALID sub-command to a running STREAM_OUTPUT is
//     refused with STREAM_IS_RUNNING (Milan v1.2 5.4.2.9; IEEE 1722.1-2021 7.4.15.2),
//     reports the current latency, and changes no stored state.
// S2: the same command to a STREAM_INPUT is NOT_SUPPORTED (Milan v1.2 5.4.2.9).
TEST_F(Core, S1_NoSubcommandSetOnRunningOutputIsRefused)
{
    auto b=target(6,0,84);put(b,4,0x20000000,4);put(b,24,123456,4);ask(14,b);
    const auto stored=latency;
    streaming=true;
    for(uint32_t flags:{0u,4u,8u,12u}){
        SCOPED_TRACE(flags);
        put(b,4,flags,4);put(b,24,765432,4);
        auto out=ask(14,b,12);
        EXPECT_EQ(get(out,62,4),123456u)<<"refusal reports current latency";
        EXPECT_EQ(latency,stored)<<"refusal preserves stored latency";
    }
    streaming=false;
}

TEST_F(Core, S2_NoSubcommandSetOnInputIsNotSupported)
{
    auto b=target(5,0,84);
    for(uint32_t flags:{0u,4u,8u,12u}){
        SCOPED_TRACE(flags);
        put(b,4,flags,4);put(b,24,765432,4);ask(14,b,11);
    }
}
