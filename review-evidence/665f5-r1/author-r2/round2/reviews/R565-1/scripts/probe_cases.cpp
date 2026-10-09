// R565-1 independent clause and failure-path probes. Included after the exact-head fixture.
TEST_F(Core, R565ReadDescriptorIgnoresConfigurationForRootDescriptors)
{
    for (unsigned type : {0u, 1u}) {
        for (unsigned configuration : {1u, 65535u}) {
            auto body = Bytes(8);
            put(body, 0, configuration, 2); put(body, 4, type, 2);
            auto response = ask(4, body, AECP_SUCCESS);
            EXPECT_EQ(get(response, 38, 2), 0u) << "IEEE 7.4.5.1/.2 root descriptor configuration is ignored and returned as zero";
            EXPECT_EQ(response.size(), 42u + desc(type).length);
        }
    }
}

TEST_F(Core, R565SetStreamInfoReturnsCurrentObservationFields)
{
    auto body = target(6, 0, 84);
    put(body, 4, 0x20000000, 4); put(body, 24, 123456, 4);
    auto response = ask(14, body);
    EXPECT_EQ(get(response, 46, 8), get(desc(6).value + 74, 8)) << "IEEE 7.4.15.1 current stream_format";
    EXPECT_EQ(get(response, 54, 8), 0x0102030405060708ull) << "IEEE 7.4.15.1 current stream_id";
    EXPECT_EQ(get(response, 66, 6), 0x91e0f0000101ull) << "IEEE 7.4.15.1 current destination MAC";
    EXPECT_EQ(get(response, 82, 2), 2u) << "IEEE 7.4.15.1 current VLAN";
    EXPECT_EQ(get(response, 62, 4), 123456u) << "Milan 5.4.2.9 requested latency";
}

TEST_F(Core, R565UnavailableStreamDoesNotStarveOtherNotices)
{
    register_controller(); sent.clear();
    ON_CALL(mock, Stream).WillByDefault(Return(false));
    aecp_changed(&a, 5, 0, 1); // unavailable stream observation comes first
    aecp_changed(&a, 9, 0, 2); // independent available AVB observation
    for (unsigned n=0; n<1000; ++n) { ms=n; (void)aecp_poll(&a); }
    bool avb_notice=false;
    for (const auto &p:sent) avb_notice |= get(p.second,36,2)==0x8027u;
    EXPECT_TRUE(avb_notice) << "Milan Table 5.22 independent AVB change must not starve";
    EXPECT_NE(events[&desc(5)-descriptors.data()].pending & 1u, 0u) << "failed snapshot remains pending";
}

TEST_F(Core, R565CrossInstanceCallbackIsRefused)
{
    aecp other{};
    auto other_events=events; auto other_cfg=cfg; other_cfg.events=other_events.data();
    ASSERT_TRUE(aecp_init(&other,&other_cfg,&ports));
    ON_CALL(mock, Changed).WillByDefault([&](aecp_change,uint16_t,uint16_t){aecp_open(&other);});
    auto body=target(26,0,5);body[4]=255;ask(24,body);
    EXPECT_FALSE(other.open) << "port must not synchronously enter another instance";
    EXPECT_GT(other.reentries,0u) << "cross-instance refusal is counted";
}
