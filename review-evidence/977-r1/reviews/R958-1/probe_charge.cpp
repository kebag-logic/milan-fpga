// Review probe: include the unchanged suite and exercise a mixed bound/kept vector.
#include "srp_mbx.cpp"
#include <iostream>
#include <cstdlib>
namespace {
TEST_F(Srp, ReviewMixedBoundAndKeptVector) {
    settle(); advance(400);
    const unsigned sinks = CTRL_SRP_SINKS;
    const unsigned values = std::getenv("REVIEW_BOUND_ONLY") ? sinks : 2u * sinks;
    const msrp_stream_id first{{0x0c,0x0d,0x0e,0x0f,0x10,0x02,0,0}};
    const uint64_t destination = 0x91e0f000fd00ull;
    for (unsigned k=0;k<sinks;++k) {
        auto sid=first; sid.bytes[7]=k;
        uint8_t da[6]; wire_put_be(da,destination+k,6);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,&sid,da,2));
    }
    settle(); advance(400);
    uint8_t da[6]; wire_put_be(da,destination,6);
    const auto value=talker_value(first,da,2);
    const unsigned packed=(values+2u)/3u;
    const unsigned list=2u+25u+packed+2u;
    std::vector<uint8_t> f(15u+4u+list+2u);
    wire_put_be(f.data(),0x0180c200000eull,6);
    wire_put_be(f.data()+6,0x0c0d0e0f1002ull,6);
    wire_put_be(f.data()+12,0x22ea,2);
    f[15]=1; f[16]=25;
    wire_put_be(f.data()+17,list,2);
    wire_put_be(f.data()+19,values,2);
    std::copy(value.begin(),value.end(),f.begin()+21);
    for(unsigned k=0;k<values;++k) f[46+k/3] += k%3==0 ? 36 : k%3==1 ? 6 : 1;
    if (f.size()<60u) f.resize(60u,0); // Ethernet minimum without FCS; MRP EndMark precedes padding.
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));
    const unsigned charge=loop.drain_charge(&adapter);
    settle();
    unsigned registered=0;
    auto visit=[](void *ctx,const mrp_attr_status *s) {
        if(s->attr_type==MSRP_ATTR_TYPE_TALKER_ADV && s->reg==MRP_REG_STATE_IN)
            ++*static_cast<unsigned *>(ctx);
    };
    ASSERT_GT(mrp_attr_visit(adapter.ifs[0].msrp,0,visit,&registered),0);
    std::cout << "REVIEW sinks=" << sinks << " vector_values=" << values
              << " registered=" << registered << " charge_us=" << charge
              << " required_count_charge_us=" << CTRL_LOOP_SRP_UNIT_US+registered*CTRL_LOOP_SRP_REG_US << '\n';
    EXPECT_EQ(registered,values) << "the real receiver accepts both bound and kept registrations";
    EXPECT_GE(charge,CTRL_LOOP_SRP_UNIT_US+registered*CTRL_LOOP_SRP_REG_US)
        << "the pre-parse registration count must not undercount accepted values";
}
}
