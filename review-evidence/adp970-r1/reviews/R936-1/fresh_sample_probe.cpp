
namespace {
unsigned sample_calls;
uint32_t sample_value;
uint32_t counted_sample(void*) {
    ++sample_calls;
    return sample_value;
}

TEST(IndependentDraw, QualifiedLinkUpTakesFreshSample) {
    sample_calls = 0;
    sample_value = 41000;
    adp_mbx_set_clock(counted_sample, nullptr);
    Wire w;
    boot_down(w, 3u);
    const unsigned at_enable = sample_calls;
    for (unsigned k = 0; k < 3; ++k) {
        sample_value += 1234567;
        const unsigned before = sample_calls;
        mbx_model_set_link(&model, 0, true);
        settle();
        const unsigned after = sample_calls;
        std::printf("qualified LINK_UP %u: samples before=%u after=%u; delay=%u ms\n",
                    k, before, after, adp0()->last_draw_ms);
        EXPECT_EQ(after, before + 1u) << "qualified LINK_UP consumes one fresh clock sample";
        const auto draws = adp0()->draws;
        adp_link_change(adp0(), true);
        EXPECT_EQ(adp0()->draws, draws) << "duplicate up does not draw";
        EXPECT_EQ(sample_calls, after) << "duplicate up does not sample";
        mbx_model_set_link(&model, 0, false);
        settle();
    }
    std::printf("samples at enable=%u after three rises=%u\n", at_enable, sample_calls);
    adp_mbx_set_clock(nullptr, nullptr);
}

TEST(IndependentDraw, LinkTimeChangesTheFirstDraw) {
    std::set<uint32_t> draws;
    for (unsigned k = 0; k < 32; ++k) {
        sample_value = 41000;
        adp_mbx_set_clock(counted_sample, nullptr);
        Wire w;
        boot_down(w, 3u);
        sample_value = 1234567u * k;
        mbx_model_set_link(&model, 0, true);
        settle();
        draws.insert(adp0()->last_draw_ms);
    }
    std::printf("32 distinct LINK_UP-time samples, identical enable sample: %zu distinct delays\n", draws.size());
    EXPECT_GT(draws.size(), 1u) << "the first LINK_UP draw depends on its fresh sample";
    adp_mbx_set_clock(nullptr, nullptr);
}
}
