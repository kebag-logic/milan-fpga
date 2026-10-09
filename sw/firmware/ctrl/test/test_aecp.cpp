// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "fw_gtest.hpp"
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <array>
#include <vector>
#include <algorithm>
extern "C" {
#include "aecp.h"
#include "aecp_image.h"
#include "aecp_entity_gen.h"
}

FW_TALLY_LABEL("AECP core");
using Bytes = std::vector<uint8_t>;
using testing::_;
using testing::Return;
using testing::NiceMock;
namespace {
constexpr uint64_t ENTITY=0x020000fffe000001, MAC=0x020000000001, CTLR=0x1020304050607080, CMAC=0x020000000081;
uint64_t get(const uint8_t *b,unsigned n) { uint64_t v=0;while(n--) v=(v<<8)|*b++;return v; }
uint64_t get(const Bytes& b,size_t at,unsigned n) { return get(b.data()+at,n); }
void put(uint8_t *b,uint64_t v,unsigned n) { for(unsigned k=0;k<n;++k) b[k]=v>>(8*(n-k-1)); }
void put(Bytes& b,size_t at,uint64_t v,unsigned n) { put(b.data()+at,v,n); }
Bytes target(unsigned type,unsigned index,size_t size=4) { Bytes v(size);put(v,0,type,2);put(v,2,index,2);return v; }
Bytes command(unsigned cmd,Bytes body={},uint64_t controller=CTLR,unsigned interface=0,unsigned msg=0) {
    Bytes b(38+body.size());
    put(b,0,MAC+interface,6);put(b,6,CMAC,6);put(b,12,0x22f0,2);
    b[14]=0xfb;b[15]=msg;put(b,16,12+body.size(),2);put(b,18,ENTITY,8);
    put(b,26,controller,8);put(b,34,0x1234,2);put(b,36,cmd,2);
    std::copy(body.begin(),body.end(),b.begin()+38);return b;
}
struct Ports {
    MOCK_METHOD(bool,Send,(unsigned,const uint8_t *,size_t));
    MOCK_METHOD(uint32_t,Now,());
    MOCK_METHOD(uint32_t,Random,());
    MOCK_METHOD(void,Timer,(bool,uint32_t));
    MOCK_METHOD(bool,Stream,(unsigned,uint16_t,uint16_t,aecp_stream_info *));
    MOCK_METHOD(bool,Avb,(unsigned,uint16_t,aecp_avb_info *));
    MOCK_METHOD(bool,Path,(unsigned,uint16_t,uint64_t *,size_t,size_t *));
    MOCK_METHOD(bool,Counters,(unsigned,uint16_t,uint16_t,aecp_counters *));
    MOCK_METHOD(void,Changed,(aecp_change,uint16_t,uint16_t));
    MOCK_METHOD(void,Start,(uint16_t,bool));
};
struct Core : testing::Test {
    aecp a{};
    std::array<aecp_descriptor,AECP_ENTITY_DESCRIPTORS> descriptors{};
    std::array<uint8_t,AECP_ENTITY_VALUE_BYTES> values{};
    std::array<aecp_event,AECP_ENTITY_DESCRIPTORS> events{};
    std::array<uint32_t,32> latency{};
    aecp_model model{};
    NiceMock<Ports> mock;
    uint32_t ms=0;
    bool room=true,bound=false,streaming=false,observations=true;
    std::vector<std::pair<unsigned,Bytes>> sent;
    std::array<aecp_mapping,64> input{},output{};
    std::array<aecp_map,2> maps{};
    aecp_ports ports{};
    aecp_config cfg{};
    void SetUp() override {
        ASSERT_TRUE(aecp_image_load(&model,aecp_entity_image,sizeof aecp_entity_image,AECP_ENTITY_CRC,
                                  descriptors.data(),descriptors.size(),values.data(),values.size()));
        ports={&mock,
          [](void*p,unsigned i,const uint8_t*b,size_t n){return static_cast<Ports*>(p)->Send(i,b,n);},
          [](void*p){return static_cast<Ports*>(p)->Now();},
          [](void*p){return static_cast<Ports*>(p)->Random();},
          [](void*p,bool b,uint32_t n){static_cast<Ports*>(p)->Timer(b,n);},
          [](void*p,unsigned i,uint16_t t,uint16_t d,aecp_stream_info*v){return static_cast<Ports*>(p)->Stream(i,t,d,v);},
          [](void*p,unsigned i,uint16_t d,aecp_avb_info*v){return static_cast<Ports*>(p)->Avb(i,d,v);},
          [](void*p,unsigned i,uint16_t d,uint64_t*v,size_t n,size_t*c){return static_cast<Ports*>(p)->Path(i,d,v,n,c);},
          [](void*p,unsigned i,uint16_t t,uint16_t d,aecp_counters*v){return static_cast<Ports*>(p)->Counters(i,t,d,v);},
          [](void*p,aecp_change k,uint16_t t,uint16_t d){static_cast<Ports*>(p)->Changed(k,t,d);},
          [](void*p,uint16_t d,bool b){static_cast<Ports*>(p)->Start(d,b);}};
        ON_CALL(mock,Send).WillByDefault([this](unsigned i,const uint8_t*p,size_t n){
            if(room) { sent.emplace_back(i,Bytes(p,p+n)); } return room;});
        ON_CALL(mock,Now).WillByDefault([this]{return ms;});
        ON_CALL(mock,Random).WillByDefault(Return(12345));
        ON_CALL(mock,Stream).WillByDefault([this](unsigned,uint16_t,uint16_t,aecp_stream_info*v){
            *v={0x0102030405060708,0x91e0f0000101,0x8877665544332211,0xff000000,12345,7,2,9,3,4,bound,streaming};
            return observations;});
        ON_CALL(mock,Avb).WillByDefault([this](unsigned,uint16_t,aecp_avb_info*v){
            *v={0x0123456789abcdef,123456,0,7,3,2};return observations;});
        ON_CALL(mock,Path).WillByDefault([this](unsigned,uint16_t,uint64_t*v,size_t,size_t*n){
            *n=2;v[0]=0x0123456789abcdef;v[1]=0xfedcba9876543210;return observations;});
        ON_CALL(mock,Counters).WillByDefault([this](unsigned,uint16_t,uint16_t,aecp_counters*v){
            v->valid=0xf3f;for(unsigned n=0;n<32;++n)v->value[n]=0x10203000+n;return observations;});
        maps[0]={14,0,0,8,input.data(),0,input.size(),nullptr,0};
        maps[1]={15,0,0,8,output.data(),0,output.size(),nullptr,0};
        cfg={ENTITY,{MAC,MAC+1},AECP_TEST_INTERFACES,&model,maps.data(),maps.size(),events.data(),latency.data()};
        ASSERT_TRUE(aecp_init(&a,&cfg,&ports));aecp_open(&a);
    }
    aecp_descriptor& desc(unsigned type,unsigned index=0) {
        auto it=std::find_if(descriptors.begin(),descriptors.end(),[=](auto&d){return d.type==type&&d.index==index;});
        if(it==descriptors.end()) { throw std::runtime_error("fixture descriptor absent"); } return *it;
    }
    void drain() { for(unsigned n=0;n<150&&aecp_poll(&a);++n){} }
    Bytes ask(unsigned cmd,Bytes body={},unsigned status=0,uint64_t controller=CTLR,unsigned interface=0) {
        sent.clear();auto b=command(cmd,body,controller,interface);aecp_rx(&a,interface,b.data(),b.size());drain();
        if(sent.empty()){ADD_FAILURE()<<"command produces a response: "<<cmd;return Bytes(200);}
        auto out=sent.front().second;
        EXPECT_EQ(get(out,16,2)>>11,status)<<"status for command "<<cmd;
        EXPECT_EQ(get(out,16,2)&0x7ff,out.size()-26)<<"response length describes all emitted bytes";
        EXPECT_EQ(get(out,0,6),CMAC)<<"response addresses the requesting MAC";
        EXPECT_EQ(get(out,6,6),MAC+interface)<<"response uses the ingress interface MAC";
        EXPECT_EQ(get(out,26,8),controller)<<"response retains controller identity";
        EXPECT_EQ(get(out,34,2),0x1234u)<<"response retains transaction sequence";
        return out;
    }
    void register_controller(uint64_t id=CTLR,unsigned interface=0){ask(36,{},0,id,interface);}
};
}

TEST_F(Core, EveryDescriptorAndReadFailures)
{
    for(const auto&d:descriptors){
        auto b=target(d.configuration,0,8);put(b,4,d.type,2);put(b,6,d.index,2);
        auto out=ask(4,b);ASSERT_EQ(out.size(),42u+d.length);
        EXPECT_EQ(Bytes(out.begin()+42,out.end()),Bytes(d.value,d.value+d.length))<<"every READ_DESCRIPTOR is byte exact";
    }
    ask(4,Bytes(7),7);auto b=Bytes(8);put(b,0,1,2);ask(4,b,7);
    put(b,0,0,2);put(b,4,0xffff,2);ask(4,b,2);
}

TEST_F(Core, UnsupportedAndAcquire)
{
    for(unsigned cmd:{3,5,11,13,19,29,72,74,0x3fff}){
        Bytes body={1,2,3,4,5};auto out=ask(cmd,body,1);
        EXPECT_EQ(Bytes(out.begin()+38,out.end()),body)<<"unsupported command echoes its exact body";
    }
    auto out=ask(0,Bytes(16,0xff),11);EXPECT_EQ(get(out,42,8),0u)<<"ACQUIRE never grants ownership";
    ask(0,Bytes(15),7);ask(38,Bytes(4),7);
}

TEST_F(Core, LockQueriesAndExpiry)
{
    Bytes b(16);auto out=ask(1,b);EXPECT_EQ(get(out,42,8),CTLR);
    uint64_t owner=0;EXPECT_TRUE(aecp_locked(&a,&owner));EXPECT_EQ(owner,CTLR);
    ask(1,b,3,CTLR+1);ask(1,b);
    out=ask(2);EXPECT_EQ(get(out,38,4),2u);EXPECT_EQ(get(out,50,8),CTLR);
    put(b,0,1,4);ask(1,b);EXPECT_FALSE(aecp_locked(&a,&owner));EXPECT_EQ(owner,0u);
    ask(1,b);put(b,12,5,4);ask(1,b,11);ask(1,Bytes(15),7);
    register_controller(CTLR+1);ask(1,Bytes(16));sent.clear();
    ms=59999;drain();EXPECT_TRUE(a.locked);sent.clear();ms=60000;drain();
    EXPECT_FALSE(a.locked)<<"lock expires at exactly sixty seconds";
    auto it=std::find_if(sent.begin(),sent.end(),[](auto&v){return get(v.second,36,2)==0x8001;});
    ASSERT_NE(it,sent.end());EXPECT_EQ(get(it->second,42,8),0u);
}

TEST_F(Core, NamesAndDescriptorOverlay)
{
    for(auto&d:descriptors){
        if(!(d.type==0||d.type==1||d.type==2||d.type==5||d.type==6||d.type==9||d.type==10||d.type==20||d.type==26||d.type==36))continue;
        for(unsigned name=0;name<(d.type==0?2u:1u);++name){
            auto b=target(d.type,d.index,72);put(b,4,name,2);
            std::fill(b.begin()+8,b.end(),uint8_t(0x41+name));
            auto out=ask(16,b);EXPECT_EQ(Bytes(out.begin()+46,out.end()),Bytes(b.begin()+8,b.end()));
            auto getbody=Bytes(b.begin(),b.begin()+8);out=ask(17,getbody);
            EXPECT_EQ(Bytes(out.begin()+46,out.end()),Bytes(b.begin()+8,b.end()))<<"GET_NAME returns the accepted name";
            unsigned offset=d.type==0?48+128*name:4;
            EXPECT_EQ(Bytes(d.value+offset,d.value+offset+64),Bytes(b.begin()+8,b.end()))<<"READ_DESCRIPTOR uses the same name";
        }
    }
}

TEST_F(Core, ScalarGetSetAndCurrentValueRefusals)
{
    for(auto [set,type,offset,width,listoff]:std::vector<std::array<unsigned,5>>{{8,5,74,8,82},{8,6,74,8,82},{20,2,136,4,140},{22,36,70,2,72}}){
        auto&d=desc(type);auto b=target(type,0,4+width);size_t list=get(d.value+listoff,2);
        std::copy(d.value+list,d.value+list+width,b.begin()+4);
        auto out=ask(set,b);EXPECT_EQ(get(out,42,width),get(b,4,width));
        out=ask(set+1,target(type,0));EXPECT_EQ(get(out,42,width),get(b,4,width));
        auto bad=b;std::fill(bad.begin()+4,bad.end(),0xff);out=ask(set,bad,7);
        EXPECT_EQ(get(out,42,width),get(b,4,width))<<"refused SET reports current value";
        ask(set,Bytes(3),7);ask(set+1,Bytes(3),7);ask(set,target(0,0,4+width),11);
        ask(set,target(type,0xffff,4+width),2);ask(set+1,target(type,0xffff),2);
    }
    bound=true;ask(8,target(5,0,12),12);bound=false;streaming=true;ask(8,target(6,0,12),12);
}

TEST_F(Core, ObservationsHaveFullWireForms)
{
    for(unsigned type:{5,6}){
        auto out=ask(15,target(type,0));ASSERT_EQ(out.size(),94u);
        EXPECT_EQ(get(out,42,4),0xff000000u);EXPECT_EQ(get(out,54,8),0x0102030405060708u);
        EXPECT_EQ(get(out,66,6),0x91e0f0000101u);EXPECT_EQ(get(out,74,8),0x8877665544332211u);
        EXPECT_EQ(get(out,82,2),2u);EXPECT_EQ(get(out,86,4),7u);EXPECT_EQ(out[90],100u);
    }
    auto out=ask(39,target(9,0));EXPECT_EQ(out.size(),62u);EXPECT_EQ(get(out,42,8),0x0123456789abcdefu);
    EXPECT_EQ(get(out,50,4),123456u);EXPECT_EQ(get(out,56,2),1u);EXPECT_EQ(get(out,58,4),0x06030002u);
    out=ask(40,Bytes(4));ASSERT_EQ(out.size(),58u);EXPECT_EQ(get(out,40,2),2u);
    EXPECT_EQ(get(out,42,8),0x0123456789abcdefu);EXPECT_EQ(get(out,50,8),0xfedcba9876543210u);
    for(unsigned type:{5,6,9,36}){
        out=ask(41,target(type,0));ASSERT_EQ(out.size(),174u);EXPECT_EQ(get(out,42,4),0xf3fu);
        for(unsigned n=0;n<32;++n)EXPECT_EQ(get(out,46+4*n,4),0x10203000u+n)<<"coherent bank includes every counter";
    }
}

TEST_F(Core, ObservationRefusals)
{
    for(unsigned cmd:{15,39,40,41})ask(cmd,Bytes(3),7);
    for(unsigned cmd:{15,39,41}){ask(cmd,target(0,0),11);ask(cmd,target(cmd==15?5:9,0xffff),2);}
    ask(40,target(0xffff,0),2);
    observations=false;
    for(auto [cmd,type]:std::vector<std::array<unsigned,2>>{{15,5},{39,9},{41,9}})ask(cmd,target(type,0),10);
    ask(40,Bytes(4),10);
}

TEST_F(Core, StreamInfoDirectionFlagsAndLatency)
{
    auto b=target(6,0,84);put(b,4,0x20000000,4);put(b,24,123456,4);
    EXPECT_CALL(mock,Changed(AECP_CHANGE_LATENCY,6,0)).Times(1);
    ask(14,b);ask(14,b);auto out=ask(15,target(6,0));EXPECT_EQ(get(out,62,4),123456u);
    put(b,0,5,2);ask(14,b,11);put(b,0,6,2);put(b,4,0,4);ask(14,b,11);
    put(b,4,0x20000000,4);put(b,24,0x80000000,4);ask(14,b,7);
    streaming=true;ask(14,b,12);streaming=false;ask(14,Bytes(83),7);put(b,2,65535,2);ask(14,b,2);
}

TEST_F(Core, BackpressureOrdersResponseBeforeNotice)
{
    register_controller(CTLR+1,AECP_TEST_INTERFACES-1);
    room=false;auto b=command(1,Bytes(16));aecp_rx(&a,0,b.data(),b.size());
    sent.clear();EXPECT_TRUE(aecp_poll(&a));EXPECT_TRUE(sent.empty());EXPECT_FALSE(aecp_ready(&a));
    aecp_rx(&a,0,b.data(),b.size());EXPECT_EQ(a.busy_drops,1u);
    room=true;drain();ASSERT_EQ(sent.size(),2u);
    EXPECT_EQ(get(sent[0].second,36,2),1u);EXPECT_EQ(get(sent[1].second,36,2),0x8001u);
    EXPECT_EQ(get(sent[1].second,34,2),0u);EXPECT_EQ(sent[1].first,AECP_TEST_INTERFACES-1u);
    EXPECT_TRUE(aecp_ready(&a));
}

TEST_F(Core, StartIsDeferredAndHasFailureDeadline)
{
    auto b=command(34,target(5,0));
    EXPECT_CALL(mock,Start(0,true)).Times(1);
    EXPECT_CALL(mock,Start(0,false)).Times(1);
    aecp_rx(&a,0,b.data(),b.size());EXPECT_TRUE(aecp_poll(&a));EXPECT_TRUE(sent.empty());
    aecp_start_done(&a,true,true);drain();ASSERT_EQ(sent.size(),1u);EXPECT_EQ(get(sent[0].second,16,2)>>11,0u);
    b=command(35,target(5,0));sent.clear();aecp_rx(&a,0,b.data(),b.size());ms=10;drain();
    ASSERT_EQ(sent.size(),1u);EXPECT_EQ(get(sent[0].second,16,2)>>11,10u);
    aecp_start_done(&a,true,true);EXPECT_FALSE(a.start_pending);
    ask(34,target(6,0),11);ask(35,Bytes(3),7);ask(34,target(5,0xffff),2);
}

TEST_F(Core, DynamicInfoWhitelistAndIndependentResults)
{
    Bytes b;for(auto [cmd,type]:std::vector<std::array<unsigned,2>>{{9,5},{41,9},{11,0}}){
        size_t at=b.size();b.resize(at+12);put(b,at,4,2);put(b,at+6,cmd,2);put(b,at+8,type,2);
    }
    auto out=ask(75,b);EXPECT_EQ(get(out,38,2),12u);EXPECT_EQ(get(out,58,2),136u);
    EXPECT_EQ(out[206],11u)<<"allowed but unsupported member gets per-record NOT_SUPPORTED";
    auto bad=b;put(bad,6,39,2);ask(75,bad,7);ask(75,Bytes(7),7);ask(75,Bytes(513),7);
    bad=b;put(bad,0,65535,2);ask(75,bad,7);
}

TEST_F(Core, RegistryCapacityInterfaceKeysAndLiveness)
{
    for(unsigned i=0;i<AECP_TEST_INTERFACES;++i)
        for(unsigned n=0;n<16;++n)register_controller(CTLR+n,i);
    ask(36,{},8,CTLR+16);ask(36,{},0,CTLR);ask(37,{},0,CTLR);ask(37,{},0,CTLR);
    register_controller(CTLR+16);sent.clear();ms=42345;drain();
    EXPECT_EQ(sent.size(),16u*AECP_TEST_INTERFACES)<<"each registered interface entry gets a probe";
    for(auto&[i,p]:sent){EXPECT_EQ(get(p,36,2),3u);EXPECT_EQ(p[15],0u);EXPECT_EQ(get(p,26,8),ENTITY);}
    sent.clear();ms+=250;drain();EXPECT_EQ(sent.size(),16u*AECP_TEST_INTERFACES);
    sent.clear();ms+=250;drain();EXPECT_EQ(sent.size(),16u*AECP_TEST_INTERFACES);
    for(auto&[i,p]:sent){(void)i;EXPECT_EQ(get(p,36,2),0x8025u);}
}
