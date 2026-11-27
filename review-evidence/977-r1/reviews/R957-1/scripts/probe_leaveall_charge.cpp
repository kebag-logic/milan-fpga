// Reviewer probe (appended to a disposable copy of sw/firmware/ctrl/test/srp_mbx.cpp; never committed).
// IEEE 802.1Q-2018 10.8.2.8 f) and g): a VectorAttribute may carry LeaveAll with NumberOfValues 0, its FirstValue
// still present. lwSRP's parser (mrp_pdu.c parse_pass) treats only a VectorHeader of 0 as the EndMark and goes on to
// the Message's next vector. The probe compares THE DRAIN's charge of such a record with what the record registers.
namespace {
TEST_F(Srp, ReviewProbeLeaveAllAloneVectorThenTalkers) {
    settle();
    const msrp_stream_id a{{2,1,2,3,4,5,6,0x07}};
    const msrp_stream_id b{{2,1,2,3,4,5,6,0x08}};
    const uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&a,da,2));
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&b,da,2));
    settle(); advance(200);
    const auto va=talker_value(a,da,2);
    const auto vb=talker_value(b,da,2);
    std::vector<uint8_t> f(14); wire_put_be(f.data(),0x0180c200000eull,6);
    wire_put_be(f.data()+6,0x020304010203ull,6); wire_put_be(f.data()+12,0x22ea,2);
    f.push_back(0);                                   // ProtocolVersion
    std::vector<uint8_t> list;
    list.insert(list.end(),{0x20,0x00});              // LeaveAll, NumberOfValues 0 (10.8.2.8 f, g)
    list.insert(list.end(),va.begin(),va.end());      // FirstValue present, ignored
    for (const auto *v:{&va,&vb}) {
        list.insert(list.end(),{0x00,0x01}); list.insert(list.end(),v->begin(),v->end()); list.push_back(1*36); // JoinIn
    }
    list.insert(list.end(),{0,0});                    // the AttributeList's EndMark
    f.insert(f.end(),{1,25,uint8_t(list.size()>>8),uint8_t(list.size())});
    f.insert(f.end(),list.begin(),list.end());
    f.insert(f.end(),{0,0});                          // the PDU's EndMark
    if (f.size()<60u) f.resize(60u);
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));
    const unsigned charge=loop.drain_charge(&adapter);
    std::printf("PROBE unit=%u reg=%u charge=%u\n",CTRL_LOOP_SRP_UNIT_US,CTRL_LOOP_SRP_REG_US,charge);
    settle(); advance(200);
    const unsigned k0=adapter.ifs[0].sinks[0].registered_kinds, k1=adapter.ifs[0].sinks[1].registered_kinds;
    std::printf("PROBE registered_kinds sink0=%u sink1=%u\n",k0,k1);
    EXPECT_EQ(k0,2u) << "lwSRP registers a's Advertise after the LeaveAll-alone vector";
    EXPECT_EQ(k1,2u) << "and b's";
    EXPECT_GE(charge,CTRL_LOOP_SRP_UNIT_US+2u*CTRL_LOOP_SRP_REG_US)
        << "THE DRAIN's charge is never under the Talker values the record registers";
}
} // namespace
