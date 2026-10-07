// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <cstddef>
#include <cstring>
#include <vector>
#include "fw_gtest.hpp"
#include "srp_mbx.h"
#include "shlan_port.h"
#include "mbx_model.h"
#include "wire.h"
// The host's allocation-port fault injector forwards to the real static pool.
// Only the library call site is renamed by the host arm; firmware stays intact.
static int calloc_before_failure = -1;
extern "C" void *srp_test_calloc(size_t count, size_t size) {
    if(calloc_before_failure==0) return nullptr;
    if(calloc_before_failure>0) --calloc_before_failure;
    return shlan_calloc(count,size);
}
namespace {
using ::testing::StrictMock;
struct Licence {
    MOCK_METHOD(void, Change, (unsigned, unsigned, bool));
    static void call(void *ctx, unsigned interface, unsigned source, bool active) {
        static_cast<Licence*>(ctx)->Change(interface,source,active);
    }
};
struct Declaration {
    unsigned interface, ethertype, type, event, subtype, time_ms;
    bool leaveall;
    std::vector<uint8_t> value;
};
class Srp : public ::testing::Test {
protected:
    mbx_model model{};
    ctrl_loop loop{};
    ctrl_pool pool{};
    alignas(std::max_align_t) uint8_t arena[SRP_POOL_ARENA_BYTES]{};
    srp_mbx adapter{};
    srp_source sources[MBX_N_IF][CTRL_SRP_SOURCES]{};
    srp_mbx_config config{};
    StrictMock<Licence> licence;
    void SetUp() override {
        calloc_before_failure=-1;
        mbx_model_reset(&model); mbx_model_bind(&model,nullptr,nullptr);
        ASSERT_TRUE(ctrl_pool_init(&pool,arena,sizeof(arena),srp_pool_classes,SRP_POOL_N_CLASSES));
        shlan_port_bind_pool(&pool);
        ctrl_loop_init(&loop);
        config.licence=Licence::call; config.ctx=&licence; config.link_rate_bps=1000000000;
        for (unsigned i=0;i<MBX_N_IF;++i) {
            config.mac[i]=0x020304050600ull+i;
            config.sources[i]=sources[i];
            for (unsigned n=0;n<CTRL_SRP_SOURCES;++n) {
                auto &s=sources[i][n];
                s.allocated=n==0;
                wire_put_be(s.value.stream_id.bytes,config.mac[i],6);
                wire_put_be(s.value.stream_id.bytes+6,n,2);
                wire_put_be(s.value.dest_mac,0x91e0f0000000ull+n,6);
                s.value.vlan_id=2; s.value.priority_and_rank=0x60;
                s.value.max_frame_size=224; s.value.max_interval_frames=1;
            }
        }
        ASSERT_TRUE(srp_mbx_init(&adapter,&config));
        ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
        ASSERT_TRUE(ctrl_loop_open(&loop,0x020304fffe050600ull,config.mac));
        for (unsigned i=0;i<MBX_N_IF;++i) mbx_model_set_link(&model,i,true);
    }
    void TearDown() override {
        srp_mbx_destroy(&adapter);
        EXPECT_EQ(ctrl_pool_in_use(&pool),0u);
        EXPECT_EQ(pool.bad_frees,0u);
        shlan_port_bind_pool(nullptr);
    }
    std::vector<Declaration> declarations;
    void capture() {
        declarations.clear();
        for (unsigned k=0;k<model.tx_sent;++k) {
            const auto *f=mbx_model_tx_frame(&model,k);
            ASSERT_NE(f,nullptr);
            ASSERT_EQ(f->channel,MBX_CH_SRP);
            ASSERT_LT(f->interface,MBX_N_IF);
            const unsigned et=wire_be16(f->bytes+12);
            ASSERT_TRUE(et==0x22ea || et==0x88f5);
            EXPECT_EQ(wire_be64(f->bytes+4)&0x0000ffffffffffffull,config.mac[f->interface]);
            EXPECT_EQ(wire_be32(f->bytes),0x0180c200u);
            EXPECT_EQ(wire_be16(f->bytes+4),et==0x22ea ? 0x000eu : 0x0021u);
            const auto *p=f->bytes+14;
            unsigned off=1, len=f->len-14;
            EXPECT_EQ(p[0],0u);
            while (off+2<=len && (p[off] || p[off+1])) {
                unsigned type=p[off++], width=p[off++];
                unsigned end=len;
                if(et==0x22ea) { ASSERT_LE(off+2,len); end=off+2+wire_be16(p+off); off+=2; }
                ASSERT_LE(end,len);
                while(off+2<=end && (p[off] || p[off+1])) {
                    const unsigned vh=wire_be16(p+off), count=vh&8191;
                    const bool subtype=et==0x22ea && type==3;
                    off+=2;
                    ASSERT_LE(off+width+(count+2)/3+(subtype?(count+3)/4:0),end);
                    for(unsigned n=0;n<count;++n) {
                        unsigned packed=p[off+width+n/3];
                        ASSERT_LE(packed,215u);
                        unsigned ev=n%3==0 ? packed/36 : n%3==1 ? (packed/6)%6 : packed%6;
                        unsigned sub=subtype ? (p[off+width+(count+2)/3+n/4]>>(6-2*(n%4)))&3 : 0;
                        Declaration d{f->interface,et,type,ev,sub,f->now_ms,(vh>>13)==1,
                                      std::vector<uint8_t>(p+off,p+off+width)};
                        // 802.1Q 10.8.2 / 35.2: increment the first value by
                        // its vector offset, independently of the transmitter.
                        auto add = [&](unsigned first, unsigned bytes) {
                            unsigned carry=n;
                            for(unsigned k=first+bytes;k>first;--k) {
                                carry+=d.value[k-1]; d.value[k-1]=carry&255; carry>>=8;
                            }
                        };
                        if(et==0x88f5) add(0,2);
                        else if(type==4) { d.value[0]+=n; d.value[1]+=n; }
                        else { add(6,2); if(type==1 || type==2) add(8,6); }
                        declarations.push_back(d);
                    }
                    off+=width+(count+2)/3+(subtype?(count+3)/4:0);
                }
                ASSERT_LE(off+2,end); EXPECT_EQ(wire_be16(p+off),0u); off+=2;
                if(et==0x22ea) { EXPECT_EQ(off,end); }
            }
            ASSERT_LE(off+2,len); EXPECT_EQ(wire_be16(p+off),0u);
        }
    }
    std::vector<uint8_t> frame(unsigned type, const std::vector<uint8_t> &value,
                               unsigned event, unsigned subtype=0, bool la=false) {
        unsigned list=2+value.size()+1+(type==3)+2;
        std::vector<uint8_t> f(14+1+4+list+2);
        wire_put_be(f.data(),0x0180c200000eull,6);
        wire_put_be(f.data()+6,0x020304010203ull,6);
        wire_put_be(f.data()+12,0x22ea,2);
        auto *p=f.data()+14; p[1]=type; p[2]=value.size();
        wire_put_be(p+3,list,2); wire_put_be(p+5,(la?0x2000:0)+1,2);
        std::memcpy(p+7,value.data(),value.size()); p[7+value.size()]=event*36;
        if(type==3) p[8+value.size()]=subtype*64;
        return f;
    }
    void offer(const std::vector<uint8_t> &f,unsigned interface=0) {
        ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),interface)); settle();
    }
    std::vector<uint8_t> identity(unsigned interface=0,unsigned source=0) {
        const auto *b=sources[interface][source].value.stream_id.bytes;
        return {b,b+8};
    }
    void settle() {
        for(unsigned n=0;n<1000;++n) if(ctrl_loop_service(&loop)==0) return;
        FAIL()<<"loop did not settle";
    }
    void advance(unsigned ms) {
        for(unsigned k=0;k<ms;++k) { mbx_model_advance_ms(&model,1); settle(); }
    }
};

} // namespace
