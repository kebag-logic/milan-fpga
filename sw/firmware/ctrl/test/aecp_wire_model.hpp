// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once
#include <cstdint>
static uint64_t scenario_word(uint8_t, uint16_t, uint16_t, uint8_t, uint8_t);
static bool scenario_format(uint16_t, uint16_t, uint64_t);
#define main reference_suite_main
#include "reference.cpp"
#undef main
#include <array>
namespace fw {
extern "C" {
#include "aecp.h"
#include "aecp_image.h"
#include "aecp_entity_gen.h"
}
}
using B = std::vector<uint8_t>;
static uint64_t be(const uint8_t *p, unsigned n) { uint64_t v=0;while(n--)v=(v<<8)|*p++;return v; }
static const uint8_t *image_row(unsigned type,unsigned index) {
  const auto *b=fw::aecp_entity_image;
  unsigned at=be(b+12,4);
  unsigned first=0;
  for(unsigned n=0;n<be(b+8,2);++n,at+=16){
    unsigned count=be(b+at+4,2);
    if(be(b+at+2,2)!=type)continue;
    if(index<first+count)return b+be(b+at+8,4)+(index-first)*be(b+at+14,2);
    first+=count;
  }
  throw std::runtime_error("scenario descriptor absent");
}
static uint64_t scenario_word(uint8_t kind,uint16_t ty,uint16_t ix,uint8_t sel,uint8_t ord) {
  if(kind==0){
    if(sel==0)return ty==5?0x80000000:0xf2000000;
    if(sel==1)return be(image_row(ty,ix)+74,8);
    if(sel==2&&ty==6)return 0x0102030405060708ull;
    if(sel==3)return 12345;
    if(sel==4&&ty==6)return 0x91e0f00001010000ull;
    if(sel==6&&ty==6)return uint64_t(2)<<48;
    return 0;
  }
  if(kind==1){
    if(sel==0)return GM0;
    if(sel==1)return (uint64_t(0x1234)<<32)|(uint64_t(7)<<16)|1;
    if(sel==8&&ord==0)return 0x06030002;
  }
  if(kind==2){if(sel==0)return 1;if(sel==8&&ord==0)return GM0;}
  return 0;
}
static bool scenario_format(uint16_t type,uint16_t index,uint64_t proposed) {
  uint64_t declared=be(image_row(type,index)+74,8);
  if((declared>>56)!=2)return proposed==declared;
  const uint64_t mask=(uint64_t(1023)<<22)|(uint64_t(1)<<52);
  unsigned channels=(proposed>>22)&1023;
  bool allowed=channels==1||channels==2||channels==4||channels==6||channels==8;
  return !(proposed&(uint64_t(1)<<52))&&(proposed&~mask)==(declared&~mask)&&
    (type==5?allowed:channels==((declared>>22)&1023));
}
struct Firmware {
  H &physical;
  fw::aecp a{};
  std::array<fw::aecp_descriptor,AECP_ENTITY_DESCRIPTORS> descriptors{};
  std::array<uint8_t,AECP_ENTITY_VALUE_BYTES> values{};
  std::array<fw::aecp_event,AECP_ENTITY_DESCRIPTORS> events{};
  uint32_t latency[AECP_ENTITY_OUTPUTS]{};
  fw::aecp_mapping input[64]{};
  fw::aecp_mapping output[64]{};
  fw::aecp_map maps[2]={{14,0,0,8,input,0,64,nullptr,0},{15,0,0,176,output,0,64,nullptr,0}};
  fw::aecp_model model{};
  fw::aecp_ports ports{};
  fw::aecp_config cfg{};
  std::vector<B> sent;
  std::vector<unsigned> sent_interfaces;
  std::vector<uint32_t> completions;
  uint32_t time=0;
  bool started=false;
  bool bound=false;
  bool changed=false;
  explicit Firmware(H &h):physical(h) {
    if(!fw::aecp_image_load(&model,fw::aecp_entity_image,sizeof fw::aecp_entity_image,AECP_ENTITY_CRC,
        descriptors.data(),descriptors.size(),values.data(),values.size()))throw std::runtime_error("image");
    ports.ctx=this;
    ports.available_index=[](void*,unsigned){return 0u;};
    ports.send=[](void*p,unsigned interface,const uint8_t*b,size_t n,uint32_t c){auto&s=*static_cast<Firmware*>(p);
      s.sent.emplace_back(b,b+n);s.sent_interfaces.push_back(interface);s.completions.push_back(c);return true;};
    ports.now_ms=[](void*p){return static_cast<Firmware*>(p)->time;};
    ports.random=[](void*){return 0u;};ports.timer=[](void*,bool,uint32_t){};
    ports.stream=[](void*p,unsigned,uint16_t t,uint16_t,fw::aecp_stream_info*v){
      *v={};v->flags=t==5?0x80000000:0xf2000000;v->latency=12345;
      if(t==6){v->stream_id=0x0102030405060708ull;v->dest_mac=0x91e0f0000101ull;v->vlan=2;}
      auto &s=*static_cast<Firmware*>(p);v->running=s.started;v->bound=s.bound;
      if(s.bound){v->probing_status=2;v->acmp_status=7;}
      if(t==5&&s.bound&&!s.started)v->flags|=8u;return true;};
    ports.avb=[](void*,unsigned,uint16_t,fw::aecp_avb_info*v){*v={GM0,0x1234,0,7,3,2};return true;};
    ports.path=[](void*,unsigned,uint16_t,uint64_t*v,size_t,size_t*n){*n=1;v[0]=GM0;return true;};
    ports.counters=[](void*p,unsigned,uint16_t t,uint16_t i,fw::aecp_counters*v){
      const auto &h=static_cast<Firmware*>(p)->physical;v->valid=h.ctr_mask(t,i);
      for(unsigned k=0;k<32;++k)v->value[k]=h.ctr_value(t,i,k);return true;};
    ports.changed=[](void*,fw::aecp_change,uint16_t,uint16_t){};
    ports.start=[](void*p,uint16_t,bool v){auto &s=*static_cast<Firmware*>(p);s.changed=s.bound&&s.started!=v;if(s.bound)s.started=v;};
    ports.format=[](void*,uint16_t t,uint16_t i,uint64_t v){return scenario_format(t,i,v);};
    cfg={EID,{OWN_MAC,OWN_MAC},AECP_WIRE_INTERFACES,&model,maps,2,events.data(),latency};
    if(!fw::aecp_init(&a,&cfg,&ports))throw std::runtime_error("init");
    fw::aecp_open(&a);
  }
  void run(){for(unsigned k=0;k<128;++k){
    bool busy=fw::aecp_poll(&a);
    if(a.start_pending){
      fw::aecp_start_done(&a,true,changed);
      if(changed)fw::aecp_changed(&a,5,0,1);
    }
    for(auto c:completions)fw::aecp_tx_complete(&a,c,time);
    completions.clear();if(!busy)break;
  }}
};
static B target(unsigned type,unsigned index=0,unsigned bytes=4){B b(bytes);putbe(b.data(),type,2);putbe(b.data()+2,index,2);return b;}
static B unpad(B b){if(b.size()>=26)b.resize(26+(be(b.data()+16,2)&0x7ff));return b;}
