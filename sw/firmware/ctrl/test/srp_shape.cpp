// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "srp_fixture.hpp"
#include <cstdio>
FW_TALLY_LABEL("ctrl SRP generated entity shape");
namespace {
TEST_F(Srp, EveryGeneratedOutputIsDeclaredAndEverySinkFits) {
    EXPECT_EQ(CTRL_SRP_SOURCES,SRP_EXPECT_SOURCES);
    EXPECT_EQ(CTRL_SRP_SINKS,SRP_EXPECT_SINKS);
    settle(); capture();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        unsigned outputs=0;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && (d.type==1 || d.type==2)) ++outputs;
        EXPECT_EQ(outputs,CTRL_SRP_SOURCES)<<"every generated output has a startup declaration";
        for(unsigned n=0;n<CTRL_SRP_SINKS;++n) {
            msrp_stream_id sid{{2,1,2,3,4,5,0,static_cast<uint8_t>(n)}};
            uint8_t da[]={0x91,0xe0,0xf0,0,0,static_cast<uint8_t>(n)};
            ASSERT_TRUE(srp_mbx_bind(&adapter,i,n,&sid,da,2));
            std::vector<uint8_t> value(25); std::copy(sid.bytes,sid.bytes+8,value.begin());
            std::copy(da,da+6,value.begin()+8); wire_put_be(value.data()+14,2,2);
            wire_put_be(value.data()+16,224,2); wire_put_be(value.data()+18,1,2); value[20]=0x60;
            offer(frame(1,value,0),i);
            EXPECT_EQ(adapter.ifs[i].sinks[n].declared,2u)<<"last bound sink fits static storage";
        }
    }
    advance(200); EXPECT_EQ(pool.refused,0u)<<"entity-derived pool covers all bound sinks";
    std::printf("SRP shape: interfaces=%u sources=%u sinks=%u arena=%zu adapter=%zu pool_used=%u\n",
        MBX_N_IF,CTRL_SRP_SOURCES,CTRL_SRP_SINKS,sizeof(arena),sizeof(adapter),ctrl_pool_in_use(&pool));
}
}
