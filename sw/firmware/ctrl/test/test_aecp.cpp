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
#include "aecp_state.h"
#include "aecp_internal.h"
#include "aecp_entity_gen.h"
#ifdef AECP_TEST_NVM
#include "aecp_nvm.h"
#define _Static_assert static_assert
#include "nvm_store.h"
#undef _Static_assert
#include "host/nvm_fmodel.h"
#endif
#ifdef AECP_TEST_MAILBOX
#include "aecp_mbx.h"
#include "mbx_model.h"
#endif
#ifdef AECP_TEST_APP
#include "ctrl_app_aecp.h"
#include "acmp_nvm.h"
#include "srp_mbx.h"
#endif
}
#ifdef AECP_TEST_APP
#include "acmp_fake.hpp"
#endif



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
    MOCK_METHOD(bool,Format,(uint16_t,uint16_t,uint64_t));
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
          [](void*p,uint16_t d,bool b){static_cast<Ports*>(p)->Start(d,b);},
          [](void*p,uint16_t t,uint16_t d,uint64_t f){return static_cast<Ports*>(p)->Format(t,d,f);}};
        ON_CALL(mock,Format).WillByDefault([this](uint16_t type,uint16_t index,uint64_t proposed){
            auto &d=desc(type,index);uint64_t declared=get(d.defaults+74,8);
            if((declared>>56)!=2)return proposed==declared;
            constexpr uint64_t mask=(uint64_t(1023)<<22)|(uint64_t(1)<<52);
            unsigned channels=(proposed>>22)&1023;
            bool family=channels==1||channels==2||channels==4||channels==6||channels==8;
            return !(proposed&(uint64_t(1)<<52))&&(proposed&~mask)==(declared&~mask)&&
                (type==5?family:channels==((declared>>22)&1023));
        });
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

#ifdef AECP_TEST_NVM
namespace {
struct Nvm : Core {
    aecp_nvm owner{};
    aecp_value names[AECP_ENTITY_NAMES]=AECP_ENTITY_NAMES_INIT;
    aecp_mapping rows[AECP_ENTITY_MAP_ROWS]{}, scratch[AECP_ENTITY_MAP_MAX]{};
    aecp_map pools[AECP_ENTITY_MAPS]=AECP_ENTITY_MAPS_INIT(rows);
    void SetUp() override {
        Core::SetUp();cfg.maps=pools;cfg.map_count=AECP_ENTITY_MAPS;
        ASSERT_TRUE(aecp_init(&a,&cfg,&ports));
        aecp_nvm_init(&owner,&a,names,AECP_ENTITY_NAMES,scratch,AECP_ENTITY_MAP_MAX);
        nvm_fmodel_blank();nvm_fmodel_power_on();
        nvm_fmodel_window(NVM_SLOT_A,NVM_SLOT_B+NVM_SLOT_BYTES);
        nvm_fmodel_times(1000,100);
    }
    void boot() { nvm_store_boot(&nvm_fmodel_port,&owner.port); }
    Bytes latch(unsigned g,unsigned i,size_t size) {
        Bytes b(size);EXPECT_TRUE(owner.port.latch(&owner,g,i,b.data(),size));return b;
    }
    void save() {
        while(aecp_nvm_poll(&owner)){}
        ASSERT_TRUE(nvm_store_commit_now());
        for(unsigned n=0;n<10000&&nvm_store_status()->phase!=NVM_P_IDLE;++n){
            nvm_store_service();nvm_fmodel_advance_us(100);
        }
        ASSERT_EQ(nvm_store_status()->phase,NVM_P_IDLE);ASSERT_EQ(nvm_store_status()->commits_ok,1u);
    }
};
}

TEST_F(Nvm, ShapePoolsAndNameOrdinalsMatchSavedRecords)
{
    ASSERT_EQ(AECP_ENTITY_NAMES,MILAN_NVM_N_NAME);
    for(auto &m:pools){
        auto r=nvm_rec_of(m.type==14?NVM_G_MAPI:NVM_G_MAPO,m.index);
        ASSERT_TRUE(r.ok);EXPECT_EQ(r.plen,m.capacity*8);EXPECT_LE(m.count,8u);
        for(size_t k=0;k<m.count;++k){EXPECT_EQ(m.rows[k].stream,m.index);EXPECT_EQ(m.rows[k].channel,k);}
    }
    for(unsigned i=0;i<AECP_ENTITY_NAMES;++i){
        auto b=latch(NVM_G_NAME,i,64);auto &d=desc(names[i].type,names[i].index);
        unsigned offset=names[i].type==0?(names[i].name==0?48:180):4;
        EXPECT_EQ(b,Bytes(d.defaults+offset,d.defaults+offset+64));
    }
}

TEST_F(Nvm, WholeMapFramingAndEmptySetAreDistinct)
{
    auto &m=pools[0];auto initial=latch(NVM_G_MAPI,0,m.capacity*8);
    Bytes erased(initial.size(),0xff);
    for(unsigned bad: {0xff00,0xfeff,0xfffe,0xffff}){
        auto b=erased;put(b,0,bad,2);put(b,2,0,6);
        EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPI,0,b.data(),b.size()),NVM_REFUSED);
        EXPECT_EQ(latch(NVM_G_MAPI,0,b.size()),initial);
    }
    auto b=erased;std::copy(initial.begin(),initial.begin()+8,b.end()-8);
    EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPI,0,b.data(),b.size()),NVM_REFUSED);
    EXPECT_EQ(latch(NVM_G_MAPI,0,b.size()),initial)<<"a hole cannot touch the current map";
    b=erased;b.back()=0;
    EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPI,0,b.data(),b.size()),NVM_REFUSED);
    EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPI,0,erased.data(),erased.size()),NVM_APPLIED);
    EXPECT_EQ(m.count,0u)<<"all UNUSED is an intentional empty set";
    EXPECT_EQ(owner.port.rollback(&owner,NVM_W_D3),0);EXPECT_EQ(latch(NVM_G_MAPI,0,initial.size()),initial);
}

TEST_F(Nvm, AcceptedStateSurvivesTheRealStorePowerCycle)
{
    boot();ASSERT_EQ(nvm_store_status()->terminal,NVM_T_BLANK);
    EXPECT_TRUE(owner.released);EXPECT_FALSE(a.open)<<"release queues permission; no protocol input inside a port";
    ON_CALL(mock,Changed).WillByDefault([this](aecp_change k,uint16_t t,uint16_t i){aecp_nvm_changed(&owner,k,t,i);});
    aecp_open(&a);
    auto name=target(0,0,72);put(name,4,1,2);std::fill(name.begin()+8,name.end(),0x5a);ask(16,name);
    auto p=target(6,0,84);put(p,4,0x20000000,4);put(p,24,1500000,4);ask(14,p);
    auto remove=target(14,0,16);put(remove,4,1,2);put(remove,10,7,2);put(remove,12,7,2);ask(45,remove);
    EXPECT_FALSE(nvm_store_status()->dirty)<<"port callbacks only queue persistence intent";
    auto input=latch(NVM_G_MAPI,0,pools[0].capacity*8);
    save();
    a.open=false;ASSERT_TRUE(aecp_restore_defaults(&a));owner.released=false;nvm_fmodel_power_on();boot();
    ASSERT_EQ(nvm_store_status()->terminal,NVM_T_COMPLETE);EXPECT_TRUE(owner.released);
    EXPECT_EQ(latch(NVM_G_MAPI,0,input.size()),input);
    EXPECT_EQ(latch(NVM_G_NAME,1,64),Bytes(64,0x5a));
    auto latency=latch(NVM_G_PTOF,0,4);EXPECT_EQ(get(latency,0,4),1500000u);
    for(unsigned group:{NVM_G_SUID,NVM_G_MCR}){
        auto r=nvm_rec_of(group,0);ASSERT_TRUE(r.ok);
        EXPECT_TRUE(nvm_all_erased(nvm_store_stage()+NVM_KLJ2_HDR+r.off,NVM_REC_HDR+r.plen))<<"DR5 reserved span";
    }
}

TEST_F(Nvm, AbsentMapClipsButRefusedMapRevertsItsFormat)
{
    auto &m=pools[0];auto original=latch(NVM_G_MAPI,0,m.capacity*8);
    auto &d=desc(5);uint64_t format=get(d.defaults+74,8);
    Bytes narrow(8);put(narrow,0,(format&~(uint64_t(1023)<<22))|(uint64_t(4)<<22),8);
    ASSERT_EQ(owner.port.apply(&owner,NVM_G_FMTI,0,narrow.data(),8),NVM_APPLIED);
    ASSERT_EQ(owner.port.settle(&owner),NVM_APPLIED);
    EXPECT_EQ(m.count,4u);EXPECT_EQ(get(d.value+74,8),get(narrow,0,8));
    ASSERT_EQ(owner.port.rollback(&owner,NVM_W_D3),0);
    ASSERT_EQ(owner.port.apply(&owner,NVM_G_FMTI,0,narrow.data(),8),NVM_APPLIED);
    auto invalid=original;put(invalid,0,0xff00,2);
    ASSERT_EQ(owner.port.apply(&owner,NVM_G_MAPI,0,invalid.data(),invalid.size()),NVM_REFUSED);
    EXPECT_EQ(latch(NVM_G_MAPI,0,original.size()),original)<<"refusal does not partly replace the map";
    ASSERT_EQ(owner.port.settle(&owner),NVM_APPLIED);
    EXPECT_EQ(get(d.value+74,8),format)<<"a refused saved map keeps the full reset set";
    EXPECT_EQ(latch(NVM_G_MAPI,0,original.size()),original);
    Bytes out(8);EXPECT_FALSE(owner.port.latch(&owner,NVM_G_FMTI,0,out.data(),8));
}

TEST_F(Nvm, ScalarRecordsUseSharedValidationAndReserveUnknownGroups)
{
    for(auto [group,type,offset,width]:std::vector<std::array<unsigned,4>>{
        {NVM_G_CFG,0,310,2},{NVM_G_RATE,2,136,4},{NVM_G_CLKS,36,70,2},
        {NVM_G_FMTI,5,74,8},{NVM_G_FMTO,6,74,8}}){
        auto &d=desc(type);Bytes b(d.defaults+offset,d.defaults+offset+width);
        EXPECT_EQ(owner.port.apply(&owner,group,0,b.data(),width),NVM_APPLIED);
        EXPECT_EQ(latch(group,0,width),b);
        auto bad=Bytes(width,0xff);EXPECT_EQ(owner.port.apply(&owner,group,0,bad.data(),width),NVM_REFUSED);
        EXPECT_EQ(latch(group,0,width),b)<<"refused value preserves the accepted value";
    }
    Bytes b(64,0);
    for(auto [group,index]:std::vector<std::array<unsigned,2>>{
        {NVM_G_CFG,1},{NVM_G_NAME,AECP_ENTITY_NAMES},{NVM_G_SUID,0},{NVM_G_MCR,0},{255,0}}){
        EXPECT_EQ(owner.port.apply(&owner,group,index,b.data(),b.size()),NVM_REFUSED);
        EXPECT_FALSE(owner.port.latch(&owner,group,index,b.data(),b.size()));
    }
    a.open=true;EXPECT_EQ(owner.port.apply(&owner,NVM_G_CFG,0,b.data(),2),NVM_FAULT);
    EXPECT_EQ(owner.port.rollback(&owner,NVM_W_D3),-1);
    EXPECT_EQ(owner.port.rollback(&owner,NVM_W_BIND),0)<<"binding walk does not reset AECP values";
    EXPECT_EQ(owner.port.settle(&owner),NVM_FAULT);
    model.count=0;EXPECT_FALSE(owner.port.model_ready(&owner));
}

TEST_F(Nvm, MapRecordsRefuseMissingStorageAndNeverPartiallyLatch)
{
    auto &m=pools[1];auto original=latch(NVM_G_MAPO,0,m.capacity*8);
    EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPO,0,original.data(),original.size()),NVM_APPLIED);
    EXPECT_EQ(latch(NVM_G_MAPO,0,original.size()),original);
    auto b=original;EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPO,0,b.data(),b.size()-1),NVM_REFUSED);
    EXPECT_FALSE(owner.port.latch(&owner,NVM_G_MAPO,0,b.data(),b.size()-1));EXPECT_EQ(b,original);
    owner.scratch_count=0;EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPO,0,b.data(),b.size()),NVM_FAULT);
    owner.scratch_count=AECP_ENTITY_MAP_MAX;
    for(unsigned group:{NVM_G_MAPI,NVM_G_MAPO}){
        EXPECT_EQ(owner.port.apply(&owner,group,65535,b.data(),b.size()),NVM_FAULT);
        EXPECT_FALSE(owner.port.latch(&owner,group,65535,b.data(),b.size()));
    }
    m.configuration=1;EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPO,0,b.data(),b.size()),NVM_FAULT);
    m.configuration=0;a.open=true;
    EXPECT_EQ(owner.port.apply(&owner,NVM_G_MAPO,0,b.data(),b.size()),NVM_FAULT);
}

TEST_F(Nvm, EveryChangeQueuesOnlyItsOwnedRecords)
{
    boot();
    for(auto [kind,type,group]:std::vector<std::array<unsigned,3>>{
        {AECP_CHANGE_CONFIGURATION,0,NVM_G_CFG},{AECP_CHANGE_RATE,2,NVM_G_RATE},
        {AECP_CHANGE_CLOCK,36,NVM_G_CLKS},{AECP_CHANGE_FORMAT,5,NVM_G_FMTI},
        {AECP_CHANGE_FORMAT,6,NVM_G_FMTO},{AECP_CHANGE_LATENCY,6,NVM_G_PTOF},
        {AECP_CHANGE_MAP,14,NVM_G_MAPI},{AECP_CHANGE_MAP,15,NVM_G_MAPO}}){
        aecp_nvm_changed(&owner,aecp_change(kind),type,0);
        auto r=nvm_rec_of(group,0);ASSERT_TRUE(r.ok);
        for(unsigned n=0;n<8;++n)EXPECT_EQ(owner.pending[n],n==r.id/32?(1u<<(r.id%32)):0u);
        EXPECT_TRUE(aecp_nvm_poll(&owner));EXPECT_FALSE(aecp_nvm_poll(&owner));
    }
    aecp_nvm_changed(&owner,AECP_CHANGE_NAME,5,1);
    unsigned expected=0;for(unsigned n=0;n<AECP_ENTITY_NAMES;++n){
        if(names[n].type==5&&names[n].index==1)++expected;
    }
    unsigned actual=0;while(aecp_nvm_poll(&owner))++actual;EXPECT_EQ(actual,expected);EXPECT_GT(actual,0u);
    aecp_nvm_changed(&owner,AECP_CHANGE_IDENTIFY,26,0);
    aecp_nvm_changed(&owner,AECP_CHANGE_SYSTEM_ID,0,0);
    aecp_nvm_changed(&owner,AECP_CHANGE_FORMAT,6,65535);
    EXPECT_FALSE(aecp_nvm_poll(&owner))<<"reserved and absent records never enter the queue";
}
#endif

#ifdef AECP_TEST_APP
namespace {
struct App : Nvm {
    mbx_model fabric{};
    ctrl_app application{};
    ctrl_app_aecp bridge{};
    aecp_mbx adapter{};
    acmp_nvm binding_owner{};
    adp_entity entity{ENTITY,1,MAC,0xc588,2,0x4801,2,0x4801,0};
    acmp_config connection{};
    ctrl_app_config setup{};
    alignas(std::max_align_t) uint8_t arena[SRP_POOL_ARENA_BYTES]{};
    srp_mbx reservation{};
    srp_source sources[MBX_N_IF][CTRL_SRP_SOURCES]{};
    acmp_env acmp_env_ports{};
    void SetUp() override {
        Nvm::SetUp();mbx_model_reset(&fabric);mbx_model_bind(&fabric,nullptr,nullptr);
        connection.entity_id=ENTITY;connection.n_interfaces=MBX_N_IF;connection.n_sinks=2;connection.n_sources=2;
        for(unsigned i=0;i<MBX_N_IF;++i){connection.mac[i]=MAC;cfg.mac[i]=MAC;}
        acmp_env_ports={nullptr,[](void*,uint64_t*p){*p=0;return false;},
            [](void*,unsigned,acmp_source_state*p){*p={};},[](void*,unsigned,const acmp_stream*){},
            [](void*,unsigned){},[](void*,unsigned){}};
        setup.entity=&entity;setup.arena=arena;setup.arena_bytes=sizeof arena;
        setup.classes=srp_pool_classes;setup.n_classes=SRP_POOL_N_CLASSES;
        setup.maap_allocation=[](void*,unsigned,uint64_t,uint16_t,bool){};
        setup.acmp=&connection;setup.acmp_env=&acmp_env_ports;
        ASSERT_TRUE(ctrl_app_compose(&application,&setup));
        ASSERT_TRUE(ctrl_app_compose_aecp(&application,&bridge,&adapter,&cfg,&ports,&owner));
        aecp_nvm_init(&owner,&adapter.core,names,AECP_ENTITY_NAMES,scratch,AECP_ENTITY_MAP_MAX);
        acmp_nvm_init(&binding_owner,&application.acmp.acmp,NVM_G_BIND,&owner.port);
        EXPECT_FALSE(ctrl_app_open_aecp(&bridge));
        nvm_store_boot(&nvm_fmodel_port,&binding_owner.port);
        ASSERT_TRUE(ctrl_app_open(&application,&setup));
        srp_mbx_config srp{};srp.link_rate_bps=1000000000;srp.licence=[](void*,unsigned,unsigned,bool){};
        for(unsigned i=0;i<MBX_N_IF;++i){srp.mac[i]=MAC;srp.sources[i]=sources[i];}
        ASSERT_TRUE(srp_mbx_init(&reservation,&srp));ASSERT_TRUE(ctrl_app_attach_srp(&application,&reservation));
        ASSERT_TRUE(ctrl_app_open_aecp(&bridge));
    }
    void TearDown() override { srp_mbx_destroy(&reservation); }
    void service(unsigned count=20){for(unsigned i=0;i<count;++i)(void)ctrl_loop_service(&application.loop);}
    void aem(unsigned cmd,Bytes body={},uint64_t ctl=CTLR) {
        auto p=command(cmd,body,ctl);ASSERT_TRUE(mbx_model_rx(&fabric,p.data(),p.size(),0));service();
        mbx_model_advance_ms(&fabric,5);
    }
    void acmp(unsigned msg) {
        acmp_test::Pdu p{};p.msg=msg;p.controller=CTLR;p.listener=ENTITY;p.talker=0xabcdef0102030405;
        p.listener_uid=0;p.talker_uid=0;p.flags=8;p.seq=0x4567;
        auto bytes=acmp_test::acmpdu(p);ASSERT_TRUE(mbx_model_rx(&fabric,bytes.data(),bytes.size(),0));service();
    }
};
}

TEST_F(App, DeferredStartAndLockUseTheRealAcmpOwner)
{
    acmp(6);acmp_sink_view v{};ASSERT_TRUE(acmp_view(&application.acmp.acmp,0,&v));
    ASSERT_TRUE(v.bound);ASSERT_FALSE(v.started);
    aem(34,target(5,0));ASSERT_TRUE(acmp_view(&application.acmp.acmp,0,&v));EXPECT_TRUE(v.started);
    aem(34,target(5,0));ASSERT_TRUE(acmp_view(&application.acmp.acmp,0,&v));EXPECT_TRUE(v.started);
    aem(35,target(5,0));ASSERT_TRUE(acmp_view(&application.acmp.acmp,0,&v));EXPECT_FALSE(v.started);
    EXPECT_EQ(adapter.core.reentries,0u);EXPECT_EQ(application.acmp.acmp.reentries,0u);
    aem(1,Bytes(16),CTLR+1);unsigned before=fabric.tx_sent;acmp(8);
    ASSERT_TRUE(acmp_view(&application.acmp.acmp,0,&v));EXPECT_TRUE(v.bound)<<"AECP lock governs ACMP unbind";
    bool refused=false;for(unsigned i=before;i<fabric.tx_sent;++i){auto p=mbx_model_tx_frame(&fabric,i);
        if(p->bytes[14]==0xfc&&p->bytes[15]==9)refused=(get(p->bytes+16,2)>>11)==16;}
    EXPECT_TRUE(refused);
}

TEST_F(App, MediaUnlockedNoticeCannotPassAnOwedUnbindResponse)
{
    aem(36);acmp(6);service();
    mbx_model_tx_pause(&fabric,true);
    // Fill ACMP's ring, so the UNBIND response stays in the real core queue.
    Bytes filler(70);filler[14]=0xfc;
    while(mbx_tx_send(MBX_CH_ACMP,0,filler.data(),filler.size())==MBX_STATUS_OK){}
    unsigned before=fabric.tx_sent;acmp(8);
    ASSERT_TRUE(acmp_change_pending(&application.acmp.acmp,0));
    ctrl_app_aecp_changed(&bridge,5,0,8);service();
    EXPECT_EQ(adapter.core.cfg.events[&desc(5)-descriptors.data()].pending,0u);
    EXPECT_EQ(fabric.tx_sent,before);
    mbx_model_tx_pause(&fabric,false);service(100);
    unsigned response=UINT32_MAX,notice=UINT32_MAX;
    for(unsigned i=before;i<fabric.tx_sent;++i){auto p=mbx_model_tx_frame(&fabric,i);
        if(p->bytes[14]==0xfc&&p->bytes[15]==9)response=i;
        if(p->bytes[14]==0xfb&&get(p->bytes+36,2)==0x8029)notice=i;
    }
    ASSERT_NE(response,UINT32_MAX);ASSERT_NE(notice,UINT32_MAX);EXPECT_LT(response,notice);
    EXPECT_FALSE(acmp_change_pending(&application.acmp.acmp,0));
}

TEST_F(App, PhysicalObservationsAndAcceptedWritesRetainTheirOwner)
{
    for(auto [cmd,type]:std::vector<std::array<unsigned,2>>{{15,6},{39,9},{40,0},{41,36}}){
        unsigned before=fabric.tx_sent;aem(cmd,target(type,0));
        bool success=false;for(unsigned n=before;n<fabric.tx_sent;++n){auto p=mbx_model_tx_frame(&fabric,n);
            if(p->bytes[14]==0xfb&&get(p->bytes+36,2)==cmd)success=get(p->bytes+16,2)>>11==0;}
        EXPECT_TRUE(success)<<cmd;
    }
    auto format=target(5,0,12);put(format,4,get(desc(5).defaults+74,8),8);
    EXPECT_CALL(mock,Format(5,0,_)).Times(1);
    EXPECT_CALL(mock,Changed(AECP_CHANGE_FORMAT,5,0)).Times(1);
    aem(8,format);EXPECT_TRUE(nvm_store_status()->dirty);
    ctrl_app_aecp_changed(&bridge,6,0,8);service();
    ctrl_app_aecp_changed(&bridge,5,65535,8);service();
    observations=false;unsigned before=fabric.tx_sent;aem(15,target(5,0));
    bool refused=false;for(unsigned n=before;n<fabric.tx_sent;++n){auto p=mbx_model_tx_frame(&fabric,n);
        if(p->bytes[14]==0xfb)refused=(get(p->bytes+16,2)>>11)==10;}
    EXPECT_TRUE(refused)<<"an unavailable physical snapshot cannot report success";
}

TEST_F(App, InputInfoReflectsAcmpSettlementAndFailures)
{
    auto &sink=application.acmp.acmp.sinks[0];aecp_stream_info v{};
    auto read=[&]{return bridge.ports.stream(&bridge,0,5,0,&v);};
    ASSERT_TRUE(read());EXPECT_EQ(v.flags,0x80000000u);
    acmp(6);ASSERT_TRUE(read());EXPECT_TRUE(v.bound);EXPECT_FALSE(v.running);EXPECT_TRUE(v.flags&8u);
    sink.started=true;ASSERT_TRUE(read());EXPECT_TRUE(v.running);EXPECT_FALSE(v.flags&8u);
    sink.state=ACMP_SETTLED_RSV_OK;sink.tk_failed=false;
    ASSERT_TRUE(read());EXPECT_EQ(v.flags,0xf6000006u);EXPECT_EQ(v.flags_ex,1u);
    sink.tk_failed=true;ASSERT_TRUE(read());EXPECT_EQ(v.flags,0xfe000046u);
    EXPECT_FALSE(bridge.ports.stream(&bridge,0,5,ACMP_MAX_SINKS,&v));
    unsigned source_calls=0,srp_calls=0;
    acmp_env_ports.ctx=&source_calls;
    acmp_env_ports.source=[](void*p,unsigned i,acmp_source_state*v){++*static_cast<unsigned*>(p);v->stream.vlan_id=i;};
    acmp_source_state source{};bridge.acmp_ports.source(&bridge,7,&source);
    EXPECT_EQ(source_calls,1u);EXPECT_EQ(source.stream.vlan_id,7u);
    acmp_env_ports.ctx=&srp_calls;
    acmp_env_ports.srp=[](void*p,unsigned,const acmp_stream*){++*static_cast<unsigned*>(p);};
    bridge.acmp_ports.srp(&bridge,0,nullptr);EXPECT_EQ(srp_calls,1u);
}

TEST_F(App, CompositionRefusalsLeaveExistingBindingsIntact)
{
    const auto *existing=application.acmp.acmp.env;
    ctrl_app candidate{};ctrl_app_aecp next{};aecp_mbx next_mbx{};
    EXPECT_FALSE(ctrl_app_compose_aecp(&candidate,&next,&next_mbx,&cfg,&ports,&owner));
    candidate.loop.rx[MBX_CH_ACMP].fn=application.loop.rx[MBX_CH_ACMP].fn;
    candidate.loop.rx[MBX_CH_AECP].fn=application.loop.rx[MBX_CH_AECP].fn;
    EXPECT_FALSE(ctrl_app_compose_aecp(&candidate,&next,&next_mbx,&cfg,&ports,&owner));
    candidate.loop.rx[MBX_CH_AECP].fn=nullptr;candidate.loop.n_polls=CTRL_LOOP_MAX_POLLS-1;
    EXPECT_FALSE(ctrl_app_compose_aecp(&candidate,&next,&next_mbx,&cfg,&ports,&owner));
    candidate.loop.n_polls=0;auto invalid=cfg;invalid.interfaces=0;
    EXPECT_FALSE(ctrl_app_compose_aecp(&candidate,&next,&next_mbx,&invalid,&ports,&owner));
    candidate.loop.n_sinks=CTRL_LOOP_MAX_SINKS;
    EXPECT_FALSE(ctrl_app_compose_aecp(&candidate,&next,&next_mbx,&cfg,&ports,&owner));
    EXPECT_EQ(application.acmp.acmp.env,existing);
}

TEST_F(App, ExpiredAndMissingStartRequestsCannotApplyLate)
{
    auto &entry=application.loop.polls[application.loop.n_polls-2];
    // The SRP attachment follows composition; find the bridge's actual poll.
    auto deliver=entry;
    for(unsigned n=0;n<application.loop.n_polls;++n)
        if(application.loop.polls[n].ctx==&bridge)deliver=application.loop.polls[n];
    bridge.ports.start(&bridge,0,true);adapter.core.start_pending=false;
    deliver.fn(deliver.ctx);EXPECT_FALSE(bridge.start_pending);
    EXPECT_FALSE(application.acmp.acmp.sinks[0].started);
    for(unsigned index:{0u,ACMP_MAX_SINKS}){
        bridge.ports.start(&bridge,index,true);adapter.core.start_pending=true;
        deliver.fn(deliver.ctx);EXPECT_FALSE(adapter.core.start_pending);
        EXPECT_FALSE(application.acmp.acmp.sinks[0].started);
    }
    application.acmp.acmp.sinks[0].bound=true;application.acmp.acmp.in_port=true;
    bridge.ports.start(&bridge,0,true);adapter.core.start_pending=true;deliver.fn(deliver.ctx);
    application.acmp.acmp.in_port=false;
    EXPECT_EQ(get(adapter.core.response+16,2)>>11,10u);
    EXPECT_FALSE(application.acmp.acmp.sinks[0].started);
}

TEST_F(App, UnboundStartAndStopAreSuccessfulNoOps)
{
    aem(36);
    for(unsigned cmd:{34,35}){
        unsigned first=fabric.tx_sent;aem(cmd,target(5,0));
        unsigned responses=0,notices=0;
        for(unsigned n=first;n<fabric.tx_sent;++n){auto p=mbx_model_tx_frame(&fabric,n);
            if(p->bytes[14]!=0xfb)continue;
            if(get(p->bytes+36,2)&0x8000)++notices;
            else {++responses;EXPECT_EQ(get(p->bytes+16,2)>>11,0u);}
        }
        EXPECT_EQ(responses,1u);EXPECT_EQ(notices,0u);
        EXPECT_FALSE(application.acmp.acmp.sinks[0].started);
    }
    auto rx=application.loop.rx[MBX_CH_SRP];application.loop.rx[MBX_CH_SRP].fn=nullptr;
    EXPECT_TRUE(ctrl_app_open_aecp(&bridge));application.loop.rx[MBX_CH_SRP]=rx;
}
#endif

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
        auto&d=desc(type);auto b=target(type,0,std::max(8u,4+width));size_t list=get(d.value+listoff,2);
        std::copy(d.value+list,d.value+list+width,b.begin()+4);
        auto out=ask(set,b);EXPECT_EQ(get(out,42,width),get(b,4,width));
        out=ask(set+1,target(type,0));EXPECT_EQ(get(out,42,width),get(b,4,width));
        auto bad=b;std::fill(bad.begin()+4,bad.end(),0xff);out=ask(set,bad,7);
        EXPECT_EQ(get(out,42,width),get(b,4,width))<<"refused SET reports current value";
        ask(set,Bytes(3),7);ask(set+1,Bytes(3),7);ask(set,target(0,0,std::max(8u,4+width)),11);
        ask(set,target(type,0xffff,std::max(8u,4+width)),2);ask(set+1,target(type,0xffff),2);
    }
    bound=true;ask(8,target(5,0,12),12);bound=false;streaming=true;ask(8,target(6,0,12),12);
}

TEST_F(Core, AcceptedDefaultBecomesAnOverrideAndObservationFailureRefusesSet)
{
    auto &d=desc(6);Bytes p(d.value+74,d.value+82),lat(4),copy(8);
    aecp_value v{AECP_CHANGE_FORMAT,6,0,0};
    EXPECT_FALSE(aecp_value_latch(&a,v,copy.data(),8));
    EXPECT_CALL(mock,Changed(AECP_CHANGE_FORMAT,6,0)).Times(1);
    EXPECT_CALL(mock,Changed(AECP_CHANGE_LATENCY,6,0)).Times(1);
    auto b=target(6,0,12);std::copy(p.begin(),p.end(),b.begin()+4);
    ask(8,b);ask(8,b);
    EXPECT_TRUE(aecp_value_latch(&a,v,copy.data(),8));EXPECT_EQ(copy,p);
    auto out=ask(15,target(6,0));EXPECT_EQ(get(out,62,4),12345u)<<"unoverridden latency comes from its owner";
    b=target(6,0,84);put(b,4,0x20000000,4);ask(14,b);
    out=ask(15,target(6,0));EXPECT_EQ(get(out,62,4),0u)<<"zero is a real accepted override";
    observations=false;ask(8,target(6,0,12),10);ask(6,Bytes(4),10);
}

TEST_F(Core, RestoreValuesValidateAndRollbackWithoutLiveEvents)
{
    EXPECT_CALL(mock,Changed(_,_,_)).Times(0);
    a.open=false;
    std::vector<std::pair<aecp_value,Bytes>> cases;
    cases.push_back({{AECP_CHANGE_CONFIGURATION,0,0,0},Bytes(2)});
    for(auto [kind,type,off,width]:std::vector<std::array<unsigned,4>>{
        {AECP_CHANGE_FORMAT,5,74,8},{AECP_CHANGE_FORMAT,6,74,8},
        {AECP_CHANGE_RATE,2,136,4},{AECP_CHANGE_CLOCK,36,70,2}}){
        auto &d=desc(type);cases.push_back({{aecp_change(kind),uint16_t(type),0,0},Bytes(d.value+off,d.value+off+width)});
    }
    cases.push_back({{AECP_CHANGE_LATENCY,6,0,0},Bytes{0,0,1,2}});
    cases.push_back({{AECP_CHANGE_NAME,0,0,1},Bytes(64,0)});
    for(auto &[ref,value]:cases){
        EXPECT_EQ(aecp_value_restore(&a,ref,value.data(),value.size()),0u);
        Bytes got(value.size());EXPECT_TRUE(aecp_value_latch(&a,ref,got.data(),got.size()));EXPECT_EQ(got,value);
        EXPECT_EQ(aecp_value_restore(&a,ref,value.data(),value.size()-1),7u);
        EXPECT_FALSE(aecp_value_latch(&a,ref,got.data(),got.size()-1));
    }
    Bytes bad(8,0xff);
    for(auto ref:std::vector<aecp_value>{{AECP_CHANGE_FORMAT,5,0,0},{AECP_CHANGE_RATE,2,0,0},
          {AECP_CHANGE_CLOCK,36,0,0},{AECP_CHANGE_CONFIGURATION,0,0,0},{AECP_CHANGE_LATENCY,6,0,0}}){
        unsigned width=ref.kind==AECP_CHANGE_FORMAT?8:ref.kind==AECP_CHANGE_RATE||ref.kind==AECP_CHANGE_LATENCY?4:2;
        EXPECT_EQ(aecp_value_restore(&a,ref,bad.data(),width),7u);
    }
    EXPECT_TRUE(aecp_restore_defaults(&a));
    for(auto &d:descriptors)EXPECT_EQ(Bytes(d.value,d.value+d.length),Bytes(d.defaults,d.defaults+d.length));
    EXPECT_FALSE(aecp_value_latch(&a,{AECP_CHANGE_FORMAT,5,0,0},bad.data(),8));
    a.in_port=true;EXPECT_FALSE(aecp_restore_defaults(&a));
    EXPECT_EQ(aecp_value_restore(&a,cases[0].first,bad.data(),2),10u);
    a.in_port=false;aecp_open(&a);EXPECT_FALSE(aecp_restore_defaults(&a));
    EXPECT_EQ(aecp_value_restore(&a,cases[0].first,bad.data(),2),10u);
}

TEST_F(Core, RestoreMapWholeSetClipAndDefaults)
{
    EXPECT_CALL(mock,Changed(_,_,_)).Times(0);a.open=false;
    std::array<aecp_mapping,8> defaults;
    for(unsigned i=0;i<8;++i)defaults[i]={0,uint16_t(i),uint16_t(i),0};
    auto &m=maps[0];m.defaults=defaults.data();m.default_count=8;
    ASSERT_TRUE(aecp_restore_defaults(&a));ASSERT_EQ(m.count,8u);
    auto bad=defaults;bad[7].stream=0xff00;
    EXPECT_EQ(aecp_map_restore(&a,&m,bad.data(),8),7u);EXPECT_EQ(m.count,8u);
    bad=defaults;bad[7]={0,6,6,1};EXPECT_EQ(aecp_map_restore(&a,&m,bad.data(),8),7u);
    bad=defaults;bad[7]={0,6,0,0};EXPECT_EQ(aecp_map_restore(&a,&m,bad.data(),8),7u);
    ASSERT_EQ(aecp_map_restore(&a,&m,defaults.data(),4),0u);EXPECT_EQ(m.count,4u);
    EXPECT_EQ(aecp_map_restore(&a,&m,nullptr,0),0u);EXPECT_EQ(m.count,0u);
    ASSERT_TRUE(aecp_restore_defaults(&a));
    // A supported synthetic narrow format isolates restore/map ordering.
    auto &d=desc(5);auto raw=Bytes(d.value,d.value+d.length);
    uint64_t narrow=(get(d.value+74,8)&~(uint64_t(1023)<<22))|(uint64_t(4)<<22);
    put(d.value+get(d.value+82,2),narrow,8);Bytes value(8);put(value,0,narrow,8);
    ASSERT_EQ(aecp_value_restore(&a,{AECP_CHANGE_FORMAT,5,0,0},value.data(),8),0u);
    ASSERT_EQ(m.count,8u)<<"restoring a format does not prematurely judge maps";
    ASSERT_EQ(aecp_restore_settle(&a),0u);ASSERT_EQ(m.count,4u);
    for(unsigned i=0;i<4;++i)EXPECT_EQ(m.rows[i].channel,i);
    EXPECT_EQ(get(d.value+74,8),narrow);
    EXPECT_TRUE(aecp_restore_defaults(&a));EXPECT_EQ(m.count,8u);
    EXPECT_EQ(Bytes(d.value,d.value+d.length),raw);
    aecp_open(&a);EXPECT_EQ(aecp_map_restore(&a,&m,nullptr,0),10u);EXPECT_EQ(aecp_restore_settle(&a),10u);
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
    for(auto [cmd,type,size]:std::vector<std::array<unsigned,3>>{{8,5,12},{20,2,8},{22,36,8},{14,6,84},{24,26,5},{34,5,4}})
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
    // The second advertised entry sets the AAF "up to" bit (IEEE 7.3.3),
    // describing a range. It is not itself a concrete stream format.
    std::copy(d.value+off+8,d.value+off+16,b.begin()+4);ask(8,b,7);
    uint64_t narrow=(get(d.value+74,8)&~(uint64_t(1023)<<22))|(uint64_t(4)<<22);
    put(b,4,narrow,8);ask(8,b);EXPECT_EQ(get(d.value+74,8),narrow);
    ask(22,target(36,0,6),7); // IEEE 7.4.23.1 reserved halfword is mandatory
    auto clock=target(36,0,8);put(clock,4,1,2);ask(22,clock);EXPECT_EQ(get(desc(36).value+70,2),1u);
    auto rate=target(2,0,8);put(rate,4,48000,4);put(desc(2).value+136,44100,4);ask(20,rate);
    for(unsigned type:{5,2,36}){
        auto&row=desc(type);unsigned cmd=type==5?8:type==2?20:22, width=type==5?8:type==2?4:2;
        auto input=target(type,0,std::max(8u,4+width));size_t original=row.length;row.length=4;ask(cmd,input,10);row.length=original;
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

TEST_F(Core, FailedSnapshotRetriesAndUnsupportedEventsAreDiscarded)
{
    register_controller();sent.clear();observations=false;
    aecp_changed(&a,5,0,15);aecp_changed(&a,0,0,15);aecp_changed(&a,36,0,7);
    drain();EXPECT_TRUE(sent.empty());
    EXPECT_EQ(events[&desc(5)-descriptors.data()].pending,9u);
    EXPECT_EQ(events[&desc(0)-descriptors.data()].pending,0u);
    EXPECT_EQ(events[&desc(36)-descriptors.data()].pending,0u);
    observations=true;drain();ASSERT_EQ(sent.size(),2u);
    EXPECT_EQ(get(sent[0].second,36,2),0x800fu);
    EXPECT_EQ(get(sent[1].second,36,2),0x8029u);
    EXPECT_EQ(events[&desc(5)-descriptors.data()].pending,0u);
}

TEST_F(Core, StaticMapsPreventOrphaningFormats)
{
    auto &port=desc(14), &map=desc(10); // Replace an unrelated row with a synthetic AUDIO_MAP.
    map.type=23;map.index=0;map.length=24;std::fill(map.value,map.value+24,0);
    put(map.value+4,8,2);put(map.value+6,2,2);
    put(map.value+8,1,2);put(map.value+10,7,2); // another stream does not constrain stream zero
    put(map.value+16,0,2);put(map.value+18,7,2);
    put(port.value+16,1,2);put(port.value+18,0,2);
    auto body=target(5,0,12);uint64_t old=get(desc(5).value+74,8);
    put(body,4,(old&~(uint64_t(1023)<<22))|(uint64_t(4)<<22),8);
    ask(8,body,7);EXPECT_EQ(get(desc(5).value+74,8),old);
    put(map.value+18,3,2);ask(8,body);
    for(auto damaged:std::vector<std::pair<unsigned,unsigned>>{{4,25},{6,3}}){
        auto oldfield=get(map.value+damaged.first,2);put(map.value+damaged.first,damaged.second,2);
        ask(8,body,7);put(map.value+damaged.first,oldfield,2);
    }
    map.length=7;ask(8,body,7);map.length=24;map.index=1;ask(8,body,7);map.index=0;
    port.length=19;ask(8,body,7);port.length=20;
    map.index=65535;put(port.value+18,65535,2);put(port.value+16,2,2);ask(8,body,7);
}

TEST_F(Core, OutputMappingsHaveOneGlobalOwner)
{
    aecp_mapping other_rows[]={{0,1,0,0},{1,0,1,0}};
    aecp_map other[]={maps[0],maps[1],{15,1,0,8,other_rows,2,2,nullptr,0}};
    a.cfg.maps=other;a.cfg.map_count=3;
    auto b=target(15,0,16);put(b,4,1,2);put(b,10,1,2);put(b,12,1,2);
    ask(44,b,7);EXPECT_EQ(other[1].count,0u)<<"another port already owns this stream channel";
    other[2].configuration=1;ask(44,b);EXPECT_EQ(other[1].count,1u);
    other[2].configuration=0;put(b,10,2,2);put(b,12,2,2);ask(44,b);EXPECT_EQ(other[1].count,2u);
    observations=false;put(b,10,3,2);put(b,12,3,2);ask(44,b,7);
}

TEST_F(Core, SavedValuesRejectWrongFieldsAndDamagedDescriptors)
{
    a.open=false;Bytes bytes(64);
    for(auto v:std::vector<aecp_value>{{AECP_CHANGE_FORMAT,0,0,0},{AECP_CHANGE_FORMAT,9,0,0},
        {AECP_CHANGE_RATE,5,0,0},{AECP_CHANGE_CLOCK,2,0,0},{AECP_CHANGE_LATENCY,5,0,0},
        {AECP_CHANGE_NAME,0,0,2},{AECP_CHANGE_IDENTIFY,26,0,0},{AECP_CHANGE_NAME,5,65535,0}}){
        EXPECT_EQ(aecp_value_restore(&a,v,bytes.data(),bytes.size()),AECP_ENTITY_MISBEHAVING);
        EXPECT_FALSE(aecp_value_latch(&a,v,bytes.data(),bytes.size()));
    }
    desc(5).length=67;
    EXPECT_EQ(aecp_value_restore(&a,{AECP_CHANGE_NAME,5,0,0},bytes.data(),64),AECP_ENTITY_MISBEHAVING);
    desc(5).length=83;
    EXPECT_EQ(aecp_value_restore(&a,{AECP_CHANGE_FORMAT,5,0,0},bytes.data(),8),AECP_ENTITY_MISBEHAVING);
    a.open=true;
    EXPECT_EQ(aecp_value_restore(&a,{AECP_CHANGE_NAME,0,0,0},bytes.data(),64),AECP_ENTITY_MISBEHAVING);
}

TEST_F(Core, MapTopologyFailuresAndEmptyPartitions)
{
    auto b=target(14,0,16);put(b,4,1,2);auto &stream=desc(5),&cluster=desc(20),&port=desc(14);
    auto add=[&]{ask(44,b,7);EXPECT_EQ(maps[0].count,0u);};
    unsigned length=stream.length;stream.length=81;add();stream.length=length;
    length=cluster.length;cluster.length=85;add();cluster.length=length;
    cluster.type=21;add();cluster.type=20;
    auto geometry=get(port.value+12,4);put(port.value+12,2,2);put(port.value+14,65535,2);
    put(b,12,1,2);add();put(b,12,0,2);put(port.value+12,geometry,4);
    a.locked=true;a.lock_owner=CTLR+1;ask(44,b,3);a.locked=false;
    for(unsigned size:{0u,177u}){maps[0].page_channels=size;ask(43,target(14,0,8),10);}
    maps[0].page_channels=8;maps[0].configuration=1;ask(43,target(14,0,8),10);maps[0].configuration=0;
    maps[0].index=1;ask(43,target(14,0,8),10);maps[0].index=0;
    put(port.value+12,0,2);auto page=ask(43,target(14,0,8));
    EXPECT_EQ(get(page,44,2),1u);EXPECT_EQ(get(page,46,2),0u);put(port.value+12,geometry,4);
    // A valid second input partition is selected by cluster geometry, not row order.
    maps[0].page_channels=4;put(b,10,7,2);put(b,12,7,2);ask(44,b);
    page=ask(43,target(14,0,8));EXPECT_EQ(get(page,46,2),0u);
    auto query=target(14,0,8);put(query,4,1,2);page=ask(43,query);EXPECT_EQ(get(page,46,2),1u);
    auto duplicate=b;duplicate.insert(duplicate.end(),b.begin()+8,b.end());put(duplicate,4,2,2);
    ask(44,duplicate);EXPECT_EQ(maps[0].count,1u);
}

TEST_F(Core, OutputPartitionGeometryUsesAllAdvertisedWidths)
{
    auto &s=desc(6),&port=desc(15);auto original=s;
    // Metadata is externally owned; malformed lists cannot create phantom pages.
    Bytes defaults(s.defaults,s.defaults+s.length);s.defaults=defaults.data();
    auto query=target(15,0,8);maps[1].page_channels=1;
    auto page=ask(43,query);EXPECT_EQ(get(page,44,2),8u);
    s.length=85;page=ask(43,query);EXPECT_EQ(get(page,44,2),1u);s.length=original.length;
    auto list=get(defaults.data()+82,4);
    put(defaults.data()+82,65535,2);page=ask(43,query);EXPECT_EQ(get(page,44,2),1u);
    put(defaults.data()+82,list,4);put(defaults.data()+84,65535,2);
    page=ask(43,query);EXPECT_EQ(get(page,44,2),1u);put(defaults.data()+82,list,4);
    auto &cluster=desc(20);cluster.type=21;query=target(14,0,8);
    page=ask(43,query);EXPECT_EQ(get(page,44,2),1u);cluster.type=20;
    cluster.length=85;page=ask(43,query);EXPECT_EQ(get(page,44,2),1u);
    (void)port;s=original;
}

TEST_F(Core, BootMapFaultsCannotPartlyReplaceTheSet)
{
    a.open=false;auto &m=maps[0];auto &input_descriptor=desc(5);aecp_mapping row{0,0,0,0};
    auto restore=[&](unsigned expected){EXPECT_EQ(aecp_map_restore(&a,&m,&row,1),expected);};
    m.index=65535;restore(10);m.index=0;
    desc(14).length=19;restore(10);desc(14).length=20;
    desc(14).configuration=1;m.configuration=1;restore(10);m.configuration=0;desc(14).configuration=0;
    put(desc(14).value+16,1,2);restore(7);put(desc(14).value+16,0,2);
    m.capacity=0;restore(7);m.capacity=64;
    a.in_port=true;restore(10);EXPECT_EQ(aecp_restore_settle(&a),10u);
    aecp_map_refused(&a,&m);EXPECT_EQ(events[&desc(14)-descriptors.data()].overrides,0u);a.in_port=false;
    a.open=true;restore(10);aecp_map_refused(&a,&m);a.open=false;
    m.index=65535;aecp_map_refused(&a,&m);EXPECT_EQ(aecp_restore_settle(&a),10u);m.index=0;
    m.configuration=1;EXPECT_EQ(aecp_restore_settle(&a),0u);m.configuration=0;
    m.defaults=&row;m.default_count=1;ASSERT_TRUE(aecp_restore_defaults(&a));
    aecp_map_refused(&a,&m);desc(5).length=81;EXPECT_EQ(aecp_restore_settle(&a),10u);desc(5).length=154;
    input_descriptor.index=65535;EXPECT_EQ(aecp_restore_settle(&a),10u);input_descriptor.index=0;
    EXPECT_EQ(aecp_restore_settle(&a),0u);EXPECT_EQ(m.count,1u);
    events[&desc(14)-descriptors.data()].overrides=0;desc(5).length=81;
    EXPECT_EQ(aecp_restore_settle(&a),10u);desc(5).length=154;input_descriptor.index=65535;
    EXPECT_EQ(aecp_restore_settle(&a),10u);input_descriptor.index=0;
    aecp_mapping rows[]={{0,0,0,0},{0,1,0,0}};
    EXPECT_EQ(aecp_map_restore(&a,&m,rows,2),7u);EXPECT_EQ(m.count,1u);
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
        aecp_start_done(&a,true,true);aecp_changed(&a,5,0,8);aecp_tx_complete(&a,0,0);return true;});
    aecp_rx(&a,0,p.data(),p.size());drain();EXPECT_EQ(a.reentries,6u);
    EXPECT_EQ(aecp_ready(&a),true);
}

TEST_F(Core, ProbeIdentityAndSequenceMustBothMatch)
{
    register_controller();sent.clear();ms=42345;drain();ASSERT_EQ(sent.size(),1u);
    auto reply=sent[0].second;put(reply,0,MAC,6);put(reply,6,CMAC,6);reply[15]=1;
    auto wrong=reply;put(wrong,18,CTLR+1,8);aecp_rx(&a,0,wrong.data(),wrong.size());
    EXPECT_EQ(a.registry[0][0].probing,1u);
    wrong=reply;put(wrong,34,get(wrong,34,2)+1,2);aecp_rx(&a,0,wrong.data(),wrong.size());
    EXPECT_EQ(a.registry[0][0].probing,1u);EXPECT_EQ(a.ignored,2u);
    aecp_rx(&a,0,reply.data(),reply.size());EXPECT_EQ(a.registry[0][0].probing,0u);
}

TEST_F(Core, CounterTimerArmsOnlyEligibleCompletedSnapshots)
{
    auto &e=events[&desc(5)-descriptors.data()];
    e.pending=8;e.counter_sent=true;e.counter_at=1000;
    EXPECT_CALL(mock,Timer(true,1000)).Times(1);aecp_open(&a);
    testing::Mock::VerifyAndClearExpectations(&mock);
    a.locked=true;a.lock_deadline=500;
    EXPECT_CALL(mock,Timer(true,500)).Times(1);aecp_open(&a);
    testing::Mock::VerifyAndClearExpectations(&mock);
    a.locked=false;e.awaiting_output=true;
    EXPECT_CALL(mock,Timer(false,_)).Times(1);aecp_open(&a);
}

TEST_F(Core, MetadataConfigurationKeysAndRepeatedOverrides)
{
    auto &stream=desc(5);stream.configuration=1;
    auto map=target(14,0,16);put(map,4,1,2);ask(44,map,7);stream.configuration=0;
    maps[0].configuration=1;auto body=target(5,0,12);put(body,4,get(stream.defaults+74,8),8);ask(8,body);
    maps[0].configuration=0;maps[0].count=1;input[0]={1,0,0,0};ask(8,body);
    desc(14).configuration=1;ask(8,body);desc(14).configuration=0;
    auto &other=desc(10);auto saved=other;other.type=0;other.length=4;
    ask(6,Bytes(4));ask(6,Bytes(4));other=saved;
    auto si=target(6,0,84);put(si,4,0x20000000,4);put(si,24,100,4);ask(14,si);
    put(si,24,200,4);ask(14,si);EXPECT_EQ(latency[0],200u);
    auto fmt=target(5,0,12);put(fmt,4,(get(stream.defaults+74,8)&~(uint64_t(1023)<<22))|(uint64_t(4)<<22),8);
    ask(8,fmt);EXPECT_EQ(get(stream.value+74,8),get(fmt,4,8));
    // A row for a future configuration cannot increase the active output partition.
    desc(6).configuration=1;auto page=ask(43,target(15,0,8));EXPECT_EQ(get(page,44,2),1u);
}

TEST_F(Core, MapsCompareEveryCoordinateAndBothDirectionsOnRestore)
{
    a.open=false;
    aecp_mapping rows[]={{0,0,0,0},{0,1,1,0}};
    auto &cluster=desc(20);put(cluster.value+84,2,2);
    ASSERT_EQ(aecp_map_restore(&a,&maps[0],rows,2),0u);
    auto b=target(14,0,16);put(b,4,1,2);put(b,14,1,2);aecp_open(&a);ask(44,b);
    EXPECT_EQ(maps[0].count,3u)<<"a distinct cluster channel is a distinct input key";
    put(b,8,1,2);ask(44,b,7); // CRF has no audio channels
    put(desc(5,1).value+74,get(desc(5).value+74,8),8);
    ask(44,b,7); // a second audio stream cannot claim the same input key
    aecp_stream_info absent{};EXPECT_FALSE(aecp_stream_read(&a,5,65535,&absent));
    a.open=false;maps[1].defaults=rows;maps[1].default_count=2;
    ASSERT_TRUE(aecp_restore_defaults(&a));aecp_map_refused(&a,&maps[1]);
    EXPECT_EQ(aecp_restore_settle(&a),0u);EXPECT_EQ(maps[1].count,2u);
    aecp_mapping duplicate[]={{0,0,0,0},{0,0,0,0}};
    EXPECT_EQ(aecp_map_restore(&a,&maps[1],duplicate,2),0u);EXPECT_EQ(maps[1].count,1u);
    put(desc(6,1).value+74,get(desc(6).value+74,8),8);
    aecp_mapping outputs[]={{0,0,0,0},{1,0,1,0}};
    EXPECT_EQ(aecp_map_restore(&a,&maps[1],outputs,2),0u);EXPECT_EQ(maps[1].count,2u);
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

TEST_F(Mailbox, FullTransmitRingAndCompletionQueueKeepTheirOwedResponse)
{
    mbx_model_tx_pause(&fabric,true);Bytes filler(60);filler[14]=0xfb;
    while(mbx_tx_send(MBX_CH_AECP,0,filler.data(),filler.size())==MBX_STATUS_OK){}
    receive(2);EXPECT_TRUE(adapter.core.response_owed);auto before=fabric.tx_sent;
    mbx_model_tx_pause(&fabric,false);service(100);
    EXPECT_FALSE(adapter.core.response_owed);EXPECT_GT(fabric.tx_sent,before);
    for(unsigned n=0;n<AECP_MBX_COMPLETIONS;++n)
        ASSERT_TRUE(adapter.ports.send(&adapter,0,filler.data(),filler.size(),n));
    EXPECT_FALSE(adapter.ports.send(&adapter,0,filler.data(),filler.size(),100));
    EXPECT_EQ(adapter.completion_count,AECP_MBX_COMPLETIONS);service(100);
    EXPECT_EQ(adapter.completion_count,0u);
    mbx_event e{};e.type=MBX_EV_TYPE_TIMER;e.timer_slot=6;e.timer_tag=adapter.tag;
    adapter.armed=false;loop.sinks[0].fn(loop.sinks[0].ctx,&e);EXPECT_EQ(adapter.stale_expiries,1u);
}
#endif
