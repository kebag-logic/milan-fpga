#include "srp_fixture.hpp"
FW_TALLY_LABEL("R533 generic MVRP registrar");
namespace {
TEST_F(Srp, MvrpKeepsOriginalIeeeLeaveDeadline) {
    settle();
    auto state=[&]() {
        mrp_reg_state current=MRP_REG_STATE_COUNT;
        mrp_attr_visit(adapter.ifs[0].mvrp,0,[](void *ctx,const mrp_attr_status *s) {
            if(wire_be16(static_cast<const uint8_t*>(s->attr_val))==2) *static_cast<mrp_reg_state*>(ctx)=s->reg;
        },&current);
        return current;
    };
    std::vector<uint8_t> f(26);
    wire_put_be(f.data(),0x0180c2000021ull,6);wire_put_be(f.data()+12,0x88f5,2);
    const uint8_t pdu[]={0,1,2,0,1,0,2,0,0,0,0,0};
    std::copy(pdu,pdu+12,f.begin()+14);
    offer(f); ASSERT_EQ(state(),MRP_REG_STATE_IN);
    f[21]=5*36;offer(f);EXPECT_EQ(state(),MRP_REG_STATE_LV);
    advance(2000);offer(f);EXPECT_EQ(state(),MRP_REG_STATE_LV);
    advance(2990);EXPECT_EQ(state(),MRP_REG_STATE_LV);
    advance(10);EXPECT_EQ(state(),MRP_REG_STATE_MT);
}
}
