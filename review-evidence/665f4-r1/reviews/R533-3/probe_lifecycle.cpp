// Reviewer-owned behavior probes; the production checkout is never edited.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("R533 independent lifecycle and binding checks");
namespace {
std::vector<uint8_t> advertisement(const msrp_stream_id &id, const uint8_t *da, unsigned vid) {
    std::vector<uint8_t> value(25);
    std::copy(id.bytes,id.bytes+8,value.begin());
    std::copy(da,da+6,value.begin()+8);
    wire_put_be(value.data()+14,vid,2);
    wire_put_be(value.data()+16,224,2);
    wire_put_be(value.data()+18,1,2);
    value[20]=0x60;
    return value;
}
TEST_F(Srp, R533ReattachThenPhysicalRestartFencesOldPermissions) {
    settle(); advance(400);
    srp_mbx_destroy(&adapter);
    ctrl_loop_init(&loop);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    ASSERT_TRUE(ctrl_loop_open(&loop,0x020304fffe050600ull,config.mac));
    settle(); advance(400);
    for(unsigned i=0;i<MBX_N_IF;++i) {
        offer(frame(4,{6,4,0,7},0),i); advance(400);
        EXPECT_CALL(licence,Change(i,0,true));
        offer(frame(3,identity(i),1,2),i);
        ASSERT_TRUE(adapter.ifs[i].active[0]);
    }
    for(unsigned i=0;i<MBX_N_IF;++i) {
        auto ready=frame(3,identity(i),1,2);
        for(unsigned j=0;j<CTRL_LOOP_RX_PER_PASS+2;++j)
            ASSERT_TRUE(mbx_model_rx(&model,ready.data(),ready.size(),i));
        EXPECT_CALL(licence,Change(i,0,false));
        mbx_model_set_link(&model,i,false);
        mbx_model_set_link(&model,i,true);
        settle(); advance(1200);
        EXPECT_EQ(adapter.ifs[i].domain.vid,2u);
        EXPECT_EQ(adapter.ifs[i].domain.priority,3u);
        EXPECT_FALSE(adapter.ifs[i].active[0]);
        for(unsigned other=i+1;other<MBX_N_IF;++other)
            EXPECT_TRUE(adapter.ifs[other].active[0]);
        EXPECT_CALL(licence,Change(i,0,true)); offer(ready,i);
        EXPECT_TRUE(adapter.ifs[i].active[0]);
    }
    for(unsigned i=0;i<MBX_N_IF;++i) EXPECT_CALL(licence,Change(i,0,false));
}
TEST_F(Srp, R533SharedReplacementWireMatchesLastEligibleUser) {
    settle(); advance(400);
    const msrp_stream_id id{{2,7,6,5,4,3,2,1}};
    const uint8_t da[2][6]={{0x91,0xe0,0xf0,0,0,9},{0x91,0xe0,0xf0,0,0,10}};
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned first : {0u,1u}) {
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&id,da[0],7));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1,&id,da[0],7));
        offer(frame(1,advertisement(id,da[0],7),1),i); advance(400);
        capture(); model.tx_sent=0;
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,&id,da[1],8));
        advance(1200); capture();
        bool ready=false;
        for(const auto &d:declarations) if(d.interface==i && d.type==3 && d.ethertype==0x22ea) {
            EXPECT_NE(d.event,5u); ready |= d.subtype==2;
        }
        EXPECT_TRUE(ready);
        model.tx_sent=0;
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,&id,da[1],8));
        advance(3200); capture();
        bool leave=false; bool stale=false;
        for(const auto &d:declarations) if(d.interface==i && d.type==3 && d.ethertype==0x22ea) {
            leave |= d.event==5;
            stale |= d.event!=5 && d.subtype==2;
        }
        EXPECT_TRUE(leave); EXPECT_FALSE(stale);
        for(unsigned slot=0;slot<2;++slot) ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,nullptr,nullptr,0));
        advance(200);
    }
}
}
