namespace {
TEST_F(SrpFeedback, ReviewNewAndDomainExposeDifferentWireViews) {
    const unsigned k=0;
    bind(k); response(k); registration(k,true,1);
    for (unsigned n=0;n<1400;++n) { mbx_model_advance_ms(&model,1); settle(); }
    ASSERT_EQ(sink(k).declared,1u);
    current_kind(k,true);
    auto f=talker(0,false,0);
    // Type 4, width 4, list 9, one JoinIn of Domain {6,3,2}, then Message and PDU EndMarks.
    const std::vector<uint8_t> domain={4,4,0,9,0,1,6,3,0,2,36,0,0,0,0};
    f.resize(f.size()-2); f.insert(f.end(),domain.begin(),domain.end());
    const auto start=model.now_ms;
    queue(k,f); settle();
    for (unsigned n=0;n<CTRL_LOOP_JOIN_CS*10u;++n) { mbx_model_advance_ms(&model,1); settle(); }
    current_kind(k,false); // This queries GET_RX_STATE and asserts REGISTERING_FAILED is clear.
    std::cout << "OBS start_ms=" << start << " now_ms=" << model.now_ms
              << " ACMP_REGISTERING_FAILED=" << core()->sinks[k].tk_failed
              << " desired=" << unsigned(sink(k).desired)
              << " declared=" << unsigned(sink(k).declared) << '\n';
    EXPECT_EQ(sink(k).declared,2u) << "ACMP Advertise view must have Ready declaration within a JoinTime";
}
}
