// Reviewer probe (R532-9): appended to srp_binding.hpp in a disposable copy.
// After a real bind and PROBE_TX_RESPONSE, a matching MSRP Talker Advertise is
// received on the sink's interface and refreshed every second. Milan v1.2
// 5.5.3.5.42 moves the sink to SETTLED_RSV_OK once the Talker attribute is
// registered; 5.5.3.5.36 withdraws SRP only when TMR_NO_TK (10 s) expires
// without one.
namespace {
class SrpBindingProbe : public SrpBinding {};
std::vector<uint8_t> probe_talker_frame(unsigned event) {
    std::vector<uint8_t> v(25);
    wire_put_be(v.data(),kSid,8); wire_put_be(v.data()+8,kDa,6); wire_put_be(v.data()+14,2,2);
    wire_put_be(v.data()+16,224,2); wire_put_be(v.data()+18,1,2); v[20]=0x60;
    const unsigned list=2+v.size()+1+2;
    std::vector<uint8_t> f(14+1+4+list+2);
    wire_put_be(f.data(),0x0180c200000eull,6);
    wire_put_be(f.data()+6,0x020304010203ull,6);
    wire_put_be(f.data()+12,0x22ea,2);
    auto *p=f.data()+14; p[1]=1; p[2]=v.size();
    wire_put_be(p+3,list,2); wire_put_be(p+5,1,2);
    std::memcpy(p+7,v.data(),v.size()); p[7+v.size()]=event*36;
    return f;
}
TEST_F(SrpBindingProbe, RegisteredTalkerReachesAcmpAndBindingSurvivesNoTk) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k); expect_stream(k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_NO_RSV);
    }
    bool withdrawn[2]{};
    for (unsigned second=0; second<12u; ++second) {
        for (unsigned k=0;k<2u;++k) {
            const auto f=probe_talker_frame(second==0 ? 0u : 1u);
            ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),acfg.sink_interface[k]));
        }
        settle();
        if (second==0) {
            for (unsigned k=0;k<2u;++k) {
                EXPECT_NE(sink(k).desired,0u) << "PROBE-TK0 SRP registered the matching Talker, sink " << k;
                EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK)
                    << "PROBE-TK1 ACMP learns the registered Talker (Milan 5.5.3.5.42), sink " << k;
            }
        }
        for (unsigned ms=0; ms<1000u; ms+=10u) {
            mbx_model_advance_ms(&model,10u); settle();
            for (unsigned k=0;k<2u;++k) {
                if (!sink(k).bound && !withdrawn[k]) {
                    withdrawn[k]=true;
                    std::printf("  probe: sink %u SRP binding withdrawn at t=%u ms after the first Talker Advertise (acmp state %d, probes sent so far)\n",
                                k,second*1000u+ms+10u,static_cast<int>(core()->sinks[k].state));
                }
            }
        }
    }
    for (unsigned k=0;k<2u;++k) {
        EXPECT_NE(sink(k).desired,0u) << "PROBE-TK0 Talker still registered after 12 s, sink " << k;
        EXPECT_TRUE(sink(k).bound) << "PROBE-TK2 a healthy registered binding survives TMR_NO_TK, sink " << k;
        EXPECT_NE(core()->sinks[k].state,ACMP_PRB_W_RESP) << "PROBE-TK3 no reprobe of a registered binding, sink " << k;
        std::printf("  probe: sink %u acmp state %d srp bound %d desired %u\n",k,
                    static_cast<int>(core()->sinks[k].state),sink(k).bound,sink(k).desired);
    }
}
} // namespace
