namespace {
TEST_F(SrpTalkerKinds, ReviewQuiescentReplacementWithTrailingMessage) {
    for (unsigned latest : {kAdvertise,kFailed}) {
        for (unsigned phase=0; phase<1000; phase+=10) {
            SCOPED_TRACE(::testing::Message() << "latest=" << latest << " phase=" << phase);
            settle(); advance(400); bind(0);
            offer(record(3u-latest,kJoinIn)); advance(1000+phase);
            auto f=record(latest,kNew);
            const auto suffix=frame(4,{6,3,0,2},1);
            f.resize(f.size()-2);
            f.insert(f.end(),suffix.begin()+15,suffix.end());
            expect_declared(f,0,latest,"replacement followed by Domain must declare within a JoinTime");
            TearDown(); SetUp();
        }
    }
}

TEST_F(SrpTalkerKinds, ReviewAllThreeEventOrders) {
    // Six inputs: New and Leave of either kind; JoinIn of either kind.
    // The independent model retains a set and the latest registering event.
    for (unsigned code=0; code<216; ++code) {
        SCOPED_TRACE(::testing::Message() << "trace=" << code);
        settle(); advance(400); bind(0);
        unsigned mask=0, latest=0, trace=code;
        std::vector<uint8_t> f;
        bool had=false, withdrawn=false;
        for (unsigned pos=0;pos<3;++pos) {
            const unsigned x=trace%6; trace/=6;
            const unsigned kind=(x%2)+1;
            const unsigned event=x<2 ? kNew : x<4 ? kLv : kJoinIn;
            if (event==kLv) mask &= ~kind;
            else if (event==kNew) { mask |= kind; latest=kind; }
            else { mask=kind; latest=kind; }
            if (had && !mask) withdrawn=true;
            had=mask!=0;
            auto next=record(kind,event);
            if (f.empty()) f=next;
            else { f.resize(f.size()-2); f.insert(f.end(),next.begin()+15,next.end()); }
        }
        const unsigned expected=(mask & latest) ? latest : mask;
        const auto start=model.tx_sent;
        offer(f); advance(kJoinMs);
        EXPECT_EQ(sink(0).desired,expected) << "ordered registration model";
        EXPECT_EQ(sink(0).declared,expected) << "ordered declaration model";
        EXPECT_EQ(sink(0).withdrawn,withdrawn) << "only a real registration gap withdraws";
        for (const auto &d:listeners(start)) {
            if (expected) {
                EXPECT_NE(d.event,kLv) << "no transient withdrawal on wire";
                EXPECT_EQ(d.subtype,expected) << "only final kind on wire";
            }
        }
        TearDown(); SetUp();
    }
}
}
