namespace {
TEST_F(SrpTalkerKinds, ReviewRebindingDoesNotChangeTheRegisteredKind) {
    settle(); advance(400); bind(0);
    offer(record(kFailed,kJoinIn)); offer(record(kAdvertise,kNew)); advance(kJoinMs);
    ASSERT_EQ(sink(0).desired,kAdvertise);
    ASSERT_EQ(sink(0).declared,kAdvertise);
    ASSERT_EQ(sink(0).registered_kinds,3u);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); advance(kJoinMs);
    bind(0); advance(kJoinMs);
    std::cout << "OBS rebind registered=" << unsigned(sink(0).registered_kinds)
              << " latest=" << unsigned(sink(0).latest_kind)
              << " desired=" << unsigned(sink(0).desired)
              << " declared=" << unsigned(sink(0).declared) << '\n';
    EXPECT_EQ(sink(0).desired,kAdvertise) << "unchanged registrations retain their order across an unbind";
    EXPECT_EQ(sink(0).declared,kAdvertise) << "later binding follows the latest retained registration";
    EXPECT_EQ(sink(0).feedback_kind,kAdvertise) << "later ACMP binding observes the latest retained registration";
}
}
