#include "srp_fixture.hpp"
FW_TALLY_LABEL("R533 shared binding rebind");
namespace {
TEST_F(Srp, RebindingRepresentativeMustWithdrawLastEligibleRequest) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    uint8_t good[6]={0x91,0xe0,0xf0,0,0,9};
    uint8_t miss[6]={0x91,0xe0,0xf0,0,0,10};
    std::vector<uint8_t> talker(25);
    std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(good,good+6,talker.begin()+8);
    wire_put_be(talker.data()+14,2,2);
    wire_put_be(talker.data()+16,224,2);
    wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,good,2));
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,miss,2));
    offer(frame(1,talker,1)); advance(400);
    ASSERT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    ASSERT_EQ(adapter.ifs[0].sinks[1].declared,2u);
    // Only the first binding matched; its replacement also misses.
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,miss,2));
    model.tx_sent=0; settle(); advance(1200); capture();
    EXPECT_EQ(adapter.ifs[0].sinks[0].desired,0u);
    EXPECT_EQ(adapter.ifs[0].sinks[1].desired,0u);
    bool withdrew=false, renewed=false;
    for (const auto &d:declarations) if(d.ethertype==0x22ea && d.type==3 &&
        std::equal(d.value.begin(),d.value.end(),sid.bytes)) {
        std::cout << "listener event=" << d.event << " subtype=" << d.subtype
                  << " time_ms=" << d.time_ms << "\n";
        withdrew |= d.event==5;
        renewed |= d.event!=5 && d.subtype==2;
    }
    EXPECT_TRUE(withdrew) << "no eligible binding remains; Listener withdrawal is required";
    EXPECT_FALSE(renewed) << "Ready must not renew after every binding becomes ineligible";
}
}
