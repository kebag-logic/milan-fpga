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
#ifdef AECP_TEST_MAILBOX
#include "aecp_mbx.h"
#include "mbx_model.h"
#endif
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
    MOCK_METHOD(bool,Send,(unsigned,const uint8_t *,size_t,uint32_t));
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
    std::vector<uint32_t> completions;
    std::array<aecp_mapping,64> input{},output{};
    std::array<aecp_map,2> maps{};
    aecp_ports ports{};
    aecp_config cfg{};
    void SetUp() override {
        ASSERT_TRUE(aecp_image_load(&model,aecp_entity_image,sizeof aecp_entity_image,AECP_ENTITY_CRC,
                                  descriptors.data(),descriptors.size(),values.data(),values.size()));
        ports={&mock,
          [](void*p,unsigned i,const uint8_t*b,size_t n,uint32_t c){return static_cast<Ports*>(p)->Send(i,b,n,c);},
          [](void*p){return static_cast<Ports*>(p)->Now();},
          [](void*p){return static_cast<Ports*>(p)->Random();},
          [](void*p,bool b,uint32_t n){static_cast<Ports*>(p)->Timer(b,n);},
          [](void*p,unsigned i,uint16_t t,uint16_t d,aecp_stream_info*v){return static_cast<Ports*>(p)->Stream(i,t,d,v);},
          [](void*p,unsigned i,uint16_t d,aecp_avb_info*v){return static_cast<Ports*>(p)->Avb(i,d,v);},
          [](void*p,unsigned i,uint16_t d,uint64_t*v,size_t n,size_t*c){return static_cast<Ports*>(p)->Path(i,d,v,n,c);},
          [](void*p,unsigned i,uint16_t t,uint16_t d,aecp_counters*v){return static_cast<Ports*>(p)->Counters(i,t,d,v);},
          [](void*p,aecp_change k,uint16_t t,uint16_t d){static_cast<Ports*>(p)->Changed(k,t,d);},
          [](void*p,uint16_t d,bool b){static_cast<Ports*>(p)->Start(d,b);}};
        ON_CALL(mock,Send).WillByDefault([this](unsigned i,const uint8_t*p,size_t n,uint32_t c){
            if(room) { sent.emplace_back(i,Bytes(p,p+n)); completions.push_back(c); } return room;});
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
    void drain() { for(unsigned n=0;n<150;++n){
        bool busy=aecp_poll(&a);
        for(auto c:completions)aecp_tx_complete(&a,c,ms);
        completions.clear();if(!busy)break;
    } }
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
            unsigned offset=d.type==0?(name==0?48:180):4; // IEEE Table 7-2
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

TEST_F(Core, ConfigurationAndLockedSetRefusals)
{
    auto out=ask(7);EXPECT_EQ(get(out,40,2),0u);
    ask(6,Bytes(3),7);auto b=Bytes(4);put(b,2,1,2);ask(6,b,7);
    bound=true;ask(6,b,12);bound=false;streaming=true;ask(6,b,12);streaming=false;
    ask(1,Bytes(16));ask(6,b,3,CTLR+1);
    for(auto [cmd,type,size]:std::vector<std::array<unsigned,3>>{{8,5,12},{20,2,8},{22,36,6},{14,6,84},{24,26,5},{34,5,4}})
        ask(cmd,target(type,0,size),3,CTLR+1);
    auto name=target(5,0,72);ask(16,name,3,CTLR+1);
    a.locked=false;model.configurations=2;ask(6,b);out=ask(7);EXPECT_EQ(get(out,40,2),1u);
    EXPECT_EQ(get(desc(0).value+310,2),1u)<<"configuration agrees with ENTITY descriptor";
    ask(6,b); // identical accepted value creates no additional state change
}

TEST_F(Core, NameRefusalsAndNoOp)
{
    ask(16,Bytes(71),7);ask(17,Bytes(7),7);
    auto b=target(5,0,72);put(b,6,1,2);ask(16,b,7);put(b,6,0,2);
    put(b,2,65535,2);ask(16,b,2);put(b,2,0,2);put(b,4,1,2);ask(16,b,7);
    put(b,0,0,2);put(b,4,2,2);ask(16,b,7);put(b,0,14,2);put(b,4,0,2);ask(16,b,7);
    put(b,0,5,2);ask(16,b);ask(16,b);
    desc(5).length=60;ask(16,b,7);
}

TEST_F(Core, IdentifyCurrentValueAndRefusals)
{
    auto b=target(26,0,5);b[4]=255;
    EXPECT_CALL(mock,Changed(AECP_CHANGE_IDENTIFY,26,0)).Times(2);
    auto out=ask(24,b);EXPECT_EQ(out[42],255);EXPECT_EQ(desc(26).value[108],255);
    ask(24,b);out=ask(25,target(26,0));EXPECT_EQ(out[42],255);
    b[4]=1;out=ask(24,b,7);EXPECT_EQ(out[42],255);b[4]=0;ask(24,b);
    ask(24,Bytes(4),7);ask(25,Bytes(3),7);ask(25,target(0,0),11);ask(25,target(26,65535),2);
    desc(26).value[82]^=1;ask(25,target(26,0),11);desc(26).length=108;ask(25,target(26,0),11);
}

TEST_F(Core, ChangedScalarValuesAndDamagedLists)
{
    auto b=target(5,0,12);auto&d=desc(5);size_t off=get(d.value+82,2);
    std::copy(d.value+off+8,d.value+off+16,b.begin()+4);ask(8,b);EXPECT_EQ(get(d.value+74,8),get(b,4,8));
    auto clock=target(36,0,6);put(clock,4,1,2);ask(22,clock);EXPECT_EQ(get(desc(36).value+70,2),1u);
    auto rate=target(2,0,8);put(rate,4,48000,4);put(desc(2).value+136,44100,4);ask(20,rate);
    for(unsigned type:{5,2,36}){
        auto&row=desc(type);unsigned cmd=type==5?8:type==2?20:22, width=type==5?8:type==2?4:2;
        auto input=target(type,0,4+width);size_t original=row.length;row.length=4;ask(cmd,input,10);row.length=original;
        unsigned at=type==5?82:type==2?140:72;uint64_t old=get(row.value+at,4);
        put(row.value+at,65535,2);ask(cmd,input,10);put(row.value+at,old,4);
        put(row.value+at+2,65535,2);ask(cmd,input,10);put(row.value+at,old,4);
    }
}

TEST_F(Core, DynamicInfoSkipsOverflowAndKeepsLaterRecords)
{
    Bytes b;
    for(unsigned cmd:{41,41,41,41,7,11,13,19,21,23,29,72,74}){
        size_t at=b.size();b.resize(at+12);put(b,at,4,2);put(b,at+6,cmd,2);put(b,at+8,9,2);
    }
    auto out=ask(75,b);EXPECT_LE(out.size(),550u); // cdl <= 524
    bool configuration=false;for(size_t at=38;at<out.size();at+=8+get(out,at,2))configuration|=get(out,at+6,2)==7;
    EXPECT_TRUE(configuration)<<"oversized element is omitted while later smaller element is returned";
    b=Bytes(12);put(b,0,4,2);put(b,6,9,2);put(b,8,5,2);b[4]=1;
    out=ask(75,b);EXPECT_EQ(out[42],7u)<<"non-success command status is an element error";
}

TEST_F(Core, MapsAreAtomicAndPaginated)
{
    auto map=[](unsigned type,std::initializer_list<aecp_mapping> rows){
        Bytes b=target(type,0,8+8*rows.size());put(b,4,rows.size(),2);size_t at=8;
        for(auto&r:rows){put(b,at,r.stream,2);put(b,at+2,r.channel,2);put(b,at+4,r.cluster,2);put(b,at+6,r.cluster_channel,2);at+=8;}return b;
    };
    for(unsigned type:{14,15}){
        auto b=map(type,{{0,1,1,0},{0,2,2,0}});ask(44,b);ask(44,b);
        auto out=ask(43,target(type,0,8));EXPECT_EQ(get(out,46,2),2u)<<"GET returns the complete current page";
        EXPECT_EQ(Bytes(out.begin()+50,out.end()),Bytes(b.begin()+8,b.end()));
        auto bad=map(type,{{0,3,3,0},{0,8,4,0}});ask(44,bad,7);
        out=ask(43,target(type,0,8));EXPECT_EQ(get(out,46,2),2u)<<"invalid final mapping leaves the entire old set";
        auto conflict=type==14?map(type,{{0,4,4,0},{0,5,4,0}}):map(type,{{0,4,4,0},{0,4,5,0}});
        ask(44,conflict,7);
        auto oldconflict=type==14?map(type,{{0,7,1,0}}):map(type,{{0,1,7,0}});ask(44,oldconflict,7);
        auto remove=map(type,{{0,1,1,0},{0,1,1,0}});ask(45,remove);ask(45,remove,7);
        out=ask(43,target(type,0,8));EXPECT_EQ(get(out,46,2),1u)<<"duplicate removes affect the live set once";
        auto page=target(type,0,8);put(page,4,65535,2);ask(43,page,7);
        ask(45,map(type,{{0,2,2,0}}));
    }
    ask(44,map(14,{{0,7,7,0}}));
    auto format=target(5,0,12);put(format,4,0x0205022000806000ull,8);
    ask(8,format,7);EXPECT_EQ(input[0].channel,7u)<<"format refusal leaves every mapped channel";
    streaming=true;ask(44,map(15,{{0,1,1,0}}),7);streaming=false;
    for(auto r:std::vector<aecp_mapping>{{65535,0,0,0},{0,0,65535,0},{0,0,0,1}})ask(44,map(14,{r}),7);
    maps[0].capacity=maps[0].count;ask(44,map(14,{{0,2,2,0}}),8);
    ask(43,Bytes(7),7);ask(43,target(0,0,8),11);ask(43,target(14,65535,8),2);
    auto b=target(14,0,8);put(b,4,177,2);ask(44,b,7);put(b,4,1,2);ask(44,b,7);
    desc(14).value[17]=1;ask(43,target(14,0,8),11);desc(14).length=19;ask(43,target(14,0,8),10);
}

TEST_F(Core, CounterNoticesCoalesceAndWaitForEligibility)
{
    register_controller();sent.clear();aecp_changed(&a,5,0,8);drain();ASSERT_EQ(sent.size(),1u);
    EXPECT_EQ(get(sent[0].second,36,2),0x8029u);EXPECT_EQ(get(sent[0].second,42,4),0xf3fu);
    for(unsigned n=0;n<10;++n)aecp_changed(&a,5,0,8);
    sent.clear();ms=999;drain();EXPECT_TRUE(sent.empty());ms=1000;drain();ASSERT_EQ(sent.size(),1u);
    EXPECT_EQ(get(sent[0].second,34,2),1u)<<"sequence advances for emitted notices only";
    aecp_changed(&a,5,0,1);aecp_changed(&a,9,0,6);aecp_changed(&a,0xffff,0,15);
    sent.clear();drain();ASSERT_EQ(sent.size(),3u);
    for(auto&v:sent)EXPECT_TRUE(get(v.second,36,2)&0x8000u);
    aecp_changed(&a,5,0,1);observations=false;drain(); // failed snapshots never claim SUCCESS
}

TEST_F(Core, ProbeRepliesResetOnlyTheirOwnInterface)
{
    register_controller();sent.clear();ms=42345;drain();ASSERT_EQ(sent.size(),1u);
    auto p=sent[0].second;uint64_t targetid=get(p,18,8),controller=get(p,26,8);
    put(p,0,MAC,6);put(p,6,CMAC,6);p[15]=1;put(p,18,targetid,8);put(p,26,controller,8);
    p[16]|=0x58; // any status counts as controller availability
    aecp_rx(&a,0,p.data(),p.size());EXPECT_EQ(a.registry[0][0].probing,0u);
    EXPECT_EQ(a.registry[0][0].deadline,84690u);
    aecp_rx(&a,0,p.data(),p.size());EXPECT_EQ(a.ignored,1u);
    put(p,26,1,8);aecp_rx(&a,0,p.data(),p.size());EXPECT_EQ(a.ignored,2u);
}

TEST_F(Core, FramingRejectsInvalidIdentityAndTruncation)
{
    auto original=command(2);
    for(size_t len=0;len<38;++len)aecp_rx(&a,0,original.data(),len);
    for(auto [at,value]:std::vector<std::array<unsigned,2>>{{0,0xff},{12,0},{14,0xfa},{15,0x10},{16,0x07},{17,1}}){
        auto p=original;p[at]=value;aecp_rx(&a,0,p.data(),p.size());
    }
    auto p=original;p[18]^=1;aecp_rx(&a,0,p.data(),p.size());p=original;p[15]=2;aecp_rx(&a,0,p.data(),p.size());
    aecp_rx(&a,2,original.data(),original.size());p.resize(AECP_FRAME_BYTES+1);aecp_rx(&a,0,p.data(),p.size());
    EXPECT_TRUE(sent.empty());EXPECT_EQ(a.ignored,2u);EXPECT_EQ(a.malformed,46u);
}

TEST_F(Core, ReentrantPortsCannotMutateState)
{
    auto p=command(2);
    EXPECT_CALL(mock,Send).WillOnce([this,&p](unsigned,const uint8_t*,size_t,uint32_t){
        aecp_open(&a);aecp_rx(&a,0,p.data(),p.size());EXPECT_FALSE(aecp_poll(&a));
        aecp_start_done(&a,true,true);aecp_changed(&a,5,0,8);return true;});
    aecp_rx(&a,0,p.data(),p.size());drain();EXPECT_EQ(a.reentries,5u);
    EXPECT_EQ(aecp_ready(&a),true);
}

TEST_F(Core, InitRefusalsAndClosedService)
{
    auto original=cfg;
    for(unsigned n:{0,3}){cfg.interfaces=n;EXPECT_FALSE(aecp_init(&a,&cfg,&ports));}cfg=original;
    model.count=0;EXPECT_FALSE(aecp_init(&a,&cfg,&ports));model.count=descriptors.size();
    model.configurations=0;EXPECT_FALSE(aecp_init(&a,&cfg,&ports));model.configurations=1;
    auto&d=desc(0);d.type=65535;EXPECT_FALSE(aecp_init(&a,&cfg,&ports));d.type=0;
    d.length=311;EXPECT_FALSE(aecp_init(&a,&cfg,&ports));d.length=312;
    put(d.value+310,1,2);EXPECT_FALSE(aecp_init(&a,&cfg,&ports));put(d.value+310,0,2);
    maps[0].default_count=65;EXPECT_FALSE(aecp_init(&a,&cfg,&ports));maps[0].default_count=0;
    EXPECT_TRUE(aecp_init(&a,&cfg,&ports));EXPECT_FALSE(aecp_ready(&a));EXPECT_FALSE(aecp_poll(&a));
    auto p=command(2);aecp_rx(&a,0,p.data(),p.size());EXPECT_TRUE(sent.empty());
}

TEST_F(Core, MilanVendorCommandsAndRefusals)
{
    auto mvu=[this](unsigned cmd,Bytes value={},bool protocol=true,unsigned status=0){
        Bytes body={0xc5,0x0a,0xc1,0,0,0,0,0};put(body,4,cmd,2);body.insert(body.end(),value.begin(),value.end());
        auto p=command(protocol?0x001b:0x001c,body,CTLR,0,6);sent.clear();aecp_rx(&a,0,p.data(),p.size());drain();
        EXPECT_EQ(sent.size(),1u);auto out=sent.front().second;
        EXPECT_EQ(out[15],7u);EXPECT_EQ(get(out,16,2)>>11,status);EXPECT_EQ(get(out,16,2)&0x7ff,out.size()-26);
        return out;
    };
    auto out=mvu(0);ASSERT_EQ(out.size(),58u);EXPECT_EQ(get(out,46,4),1u);
    EXPECT_EQ(get(out,50,4),0u);EXPECT_EQ(get(out,54,4),0u);
    out=mvu(2);ASSERT_EQ(out.size(),54u);EXPECT_EQ(get(out,46,8),0u);
    Bytes value={1,2,3,4,5,6,7,8};out=mvu(1,value);EXPECT_EQ(get(out,46,8),0x0102030405060708u);
    mvu(1,value);out=mvu(2);EXPECT_EQ(get(out,46,8),0x0102030405060708u);
    mvu(1,Bytes(8),true,1);mvu(1,{},true,1);mvu(3,{},true,1);mvu(0,{},false,1);
    a.locked=true;a.lock_owner=CTLR+1;mvu(1,value,true,1);a.locked=false;
    for(Bytes body:std::vector<Bytes>{{},{0xc5,0x0a,0xc2,0,0,0,0,0}}){
        auto p=command(0x001b,body,CTLR,0,6);sent.clear();aecp_rx(&a,0,p.data(),p.size());drain();
        ASSERT_EQ(sent.size(),1u);EXPECT_EQ(get(sent[0].second,16,2)>>11,1u);
    }
}

TEST_F(Core, GroupNameDoesNotOverwriteFirmwareVersion)
{
    auto before=Bytes(desc(0).value,desc(0).value+312);
    auto b=target(0,0,72);put(b,4,1,2);std::fill(b.begin()+8,b.end(),0x55);ask(16,b);
    auto expected=before;std::fill(expected.begin()+180,expected.begin()+244,0x55);
    auto out=ask(4,Bytes(8));
    EXPECT_EQ(Bytes(out.begin()+42,out.end()),expected)<<"IEEE Table 7-2 group_name changes only bytes 180 through 243";
}

TEST_F(Core, NotificationBackpressureAndLatestCompletion)
{
    register_controller(CTLR);register_controller(CTLR+1);sent.clear();
    unsigned accepted=0;
    ON_CALL(mock,Send).WillByDefault([this,&accepted](unsigned i,const uint8_t*p,size_t n,uint32_t c){
        if(accepted++==1)return false;
        sent.emplace_back(i,Bytes(p,p+n));completions.push_back(c);return true;
    });
    auto p=command(1,Bytes(16));aecp_rx(&a,0,p.data(),p.size());
    EXPECT_TRUE(aecp_poll(&a));EXPECT_FALSE(aecp_ready(&a));EXPECT_EQ(sent.size(),1u);drain();
    ASSERT_EQ(sent.size(),2u);EXPECT_EQ(get(sent[1].second,26,8),CTLR+1)<<"requester is excluded";
    auto s=command(34,target(5,0));aecp_rx(&a,0,s.data(),s.size());aecp_start_done(&a,true,false);drain();
    aecp_changed(&a,5,0,8);aecp_poll(&a);aecp_poll(&a);auto old=completions.front(),latest=completions.back();
    completions.clear();aecp_changed(&a,5,0,8);ms=5000;aecp_tx_complete(&a,old,0);
    size_t count=sent.size();aecp_poll(&a);EXPECT_EQ(sent.size(),count)<<"an old completion cannot release a newer copy";
    aecp_tx_complete(&a,latest,5000);ms=5999;drain();EXPECT_EQ(sent.size(),count);
    ms=6000;drain();EXPECT_EQ(sent.size(),count+2);
}

TEST_F(Core, DescriptorAndObservationBoundaryFailures)
{
    auto&d=desc(5);d.length=AECP_FRAME_BYTES;auto b=Bytes(8);put(b,4,5,2);ask(4,b,8);d.length=154;
    put(d.value+126,2,2);ask(15,target(5,0),10);put(d.value+126,0,2);
    d.length=127;ask(15,target(5,0),10);ask(41,target(5,0));d.length=154;
    auto&av=desc(9);av.index=AECP_TEST_INTERFACES;
    ask(39,target(9,av.index),10);av.index=0;
    ON_CALL(mock,Path).WillByDefault([](unsigned,uint16_t,uint64_t*,size_t,size_t*n){*n=65;return true;});
    ask(40,Bytes(4),10);
    auto p=command(4,Bytes(8));p[15]=1;put(p,26,ENTITY,8);aecp_rx(&a,0,p.data(),p.size());
    EXPECT_GT(a.ignored,0u);
}

#ifdef AECP_TEST_MAILBOX
namespace {
struct Mailbox : Core {
    mbx_model fabric{};
    aecp_mbx adapter{};
    ctrl_loop loop{};
    void SetUp() override {
        Core::SetUp();mbx_model_reset(&fabric);mbx_model_bind(&fabric,nullptr,nullptr);
        ctrl_loop_init(&loop);
        ASSERT_TRUE(aecp_mbx_init(&adapter,&cfg,&ports,6));
        ASSERT_TRUE(aecp_mbx_attach(&adapter,&loop));
        uint64_t mac[MBX_N_IF];for(unsigned i=0;i<MBX_N_IF;++i)mac[i]=MAC+i;
        ASSERT_TRUE(ctrl_loop_open(&loop,ENTITY,mac));aecp_mbx_open(&adapter);
    }
    void service(unsigned count=10){for(unsigned n=0;n<count;++n)(void)ctrl_loop_service(&loop);}
    void receive(unsigned cmd,Bytes body={},uint64_t id=CTLR,unsigned interface=0) {
        auto p=command(cmd,body,id,interface);
        ASSERT_TRUE(mbx_model_rx(&fabric,p.data(),p.size(),interface));service();
    }
};
}

TEST_F(Mailbox, EveryInterfaceAndObservationPort)
{
    for(unsigned i=0;i<MBX_N_IF;++i){
        for(auto [cmd,type]:std::vector<std::array<unsigned,2>>{{15,5},{39,9},{40,0},{41,5},{24,26}}){
            auto b=target(type,0,cmd==24?5:4);uint32_t before=fabric.tx_sent;
            receive(cmd,b,CTLR,i);ASSERT_EQ(fabric.tx_sent,before+1);
            auto p=mbx_model_tx_frame(&fabric,before);ASSERT_NE(p,nullptr);EXPECT_EQ(p->interface,i);
            EXPECT_EQ(get(p->bytes+16,2)>>11,0u);
            mbx_model_advance_ms(&fabric,5);
        }
        receive(36,{},CTLR+i,i);mbx_model_advance_ms(&fabric,5);
    }
    EXPECT_EQ(fabric.ch[MBX_CH_AECP].tx_err,0u);EXPECT_EQ(fabric.bus_err,0u);
    EXPECT_EQ(adapter.completion_count,0u);
}

TEST_F(Mailbox, OutputTailStartsCounterSpacingAfterAStall)
{
    receive(36);uint32_t before=fabric.tx_sent;
    mbx_model_tx_pause(&fabric,true);aecp_changed(&adapter.core,5,0,8);service();
    EXPECT_EQ(fabric.tx_sent,before);EXPECT_GT(adapter.completion_count,0u);
    mbx_model_advance_ms(&fabric,5000);aecp_changed(&adapter.core,5,0,8);service();
    EXPECT_EQ(fabric.tx_sent,before)<<"queued counters do not count as departed frames";
    mbx_model_tx_pause(&fabric,false);service();ASSERT_EQ(fabric.tx_sent,before+1);
    uint32_t departure=mbx_model_tx_frame(&fabric,before)->now_ms;
    mbx_model_advance_ms(&fabric,999);service();EXPECT_EQ(fabric.tx_sent,before+1);
    mbx_model_advance_ms(&fabric,1);service();ASSERT_EQ(fabric.tx_sent,before+2);
    EXPECT_GE(mbx_model_tx_frame(&fabric,before+1)->now_ms-departure,1000u);
    EXPECT_EQ(adapter.completion_count,0u);
}

TEST_F(Mailbox, TimerIdentityAndAttachRefusals)
{
    receive(1,Bytes(16));uint16_t tag=adapter.tag;
    mbx_event e{};e.type=MBX_EV_TYPE_TIMER;e.timer_slot=6;e.timer_tag=tag-1;
    loop.sinks[0].fn(loop.sinks[0].ctx,&e);EXPECT_EQ(adapter.stale_expiries,1u);
    e.timer_tag=tag;e.timer_slot=7;loop.sinks[0].fn(loop.sinks[0].ctx,&e);
    e.type=MBX_EV_TYPE_GM;loop.sinks[0].fn(loop.sinks[0].ctx,&e);
    mbx_model_advance_ms(&fabric,60000);service();EXPECT_FALSE(adapter.core.locked);
    EXPECT_FALSE(aecp_mbx_attach(&adapter,&loop));
    ctrl_loop full{};ctrl_loop_init(&full);full.n_sinks=CTRL_LOOP_MAX_SINKS;
    EXPECT_FALSE(aecp_mbx_attach(&adapter,&full));full.n_sinks=0;full.n_polls=CTRL_LOOP_MAX_POLLS;
    EXPECT_FALSE(aecp_mbx_attach(&adapter,&full));
    aecp_mbx other{};EXPECT_FALSE(aecp_mbx_init(&other,&cfg,&ports,MBX_N_TIMERS));
    auto bad=cfg;bad.interfaces=MBX_N_IF+1;EXPECT_FALSE(aecp_mbx_init(&other,&bad,&ports,0));
    bad=cfg;bad.interfaces=0;EXPECT_FALSE(aecp_mbx_init(&other,&bad,&ports,0));
}
#endif
