namespace {
TEST_F(SrpTalkerKinds, ReviewMinimalTrailingDomain) {
    for (unsigned latest : {kAdvertise,kFailed}) {
        for (bool trailing : {false,true}) {
            settle(); advance(400); bind(0);
            offer(record(3u-latest,kJoinIn)); advance(1000);
            ASSERT_EQ(sink(0).declared,3u-latest);
            auto f=record(latest,kNew);
            if (trailing) {
                const auto suffix=frame(4,{6,3,0,2},1);
                f.resize(f.size()-2);
                f.insert(f.end(),suffix.begin()+15,suffix.end());
            }
            const auto from=model.tx_sent;
            const auto received=adapter.received;
            const auto malformed=adapter.malformed;
            const unsigned start=model.now_ms;
            offer(f);
            ASSERT_EQ(adapter.received,received+1);
            ASSERT_EQ(adapter.malformed,malformed);
            ASSERT_EQ(sink(0).desired,latest);
            ASSERT_EQ(sink(0).feedback_kind,latest);
            advance(kJoinMs);
            const unsigned declared_at_join=sink(0).declared;
            std::cout << "OBS latest=" << latest << " trailing=" << trailing << " start_ms=" << start
                      << " desired=" << unsigned(sink(0).desired)
                      << " feedback=" << unsigned(sink(0).feedback_kind)
                      << " declared_after_JoinTime=" << declared_at_join << '\n';
            for (unsigned elapsed=kJoinMs;elapsed<1200 && sink(0).declared!=latest;++elapsed) advance(1);
            unsigned first_wire=UINT32_MAX;
            for (const auto &d:listeners(from))
                if (d.subtype==latest && d.event!=kLv) first_wire=std::min(first_wire,d.time_ms-start);
            std::cout << "OBS first_matching_wire_ms=" << first_wire << '\n';
            EXPECT_EQ(declared_at_join,latest) << "replacement must reach wire declaration within a JoinTime";
            EXPECT_LE(first_wire,kJoinMs) << "replacement transmit latency";
            TearDown(); SetUp();
        }
    }
}
}
