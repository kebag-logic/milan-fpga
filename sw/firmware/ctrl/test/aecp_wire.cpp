// SPDX-License-Identifier: CERN-OHL-W-2.0
// Byte observations from unchanged processor RTL and the portable firmware.
#include "aecp_wire_model.hpp"

static void hex(const B &bytes) {
  std::printf("\"");for(auto value:bytes)std::printf("%02x",value);std::printf("\"");
}
static void frames(const std::vector<B> &values) {
  std::printf("[");bool first=true;
  for(const auto &value:values){if(!first)std::printf(",");first=false;hex(value);}
  std::printf("]");
}
static void record(const char *kind,const B &request,const std::vector<B> &fabric,const std::vector<B> &core,unsigned interface) {
  std::printf("WIRE {\"kind\":\"%s\",\"interface\":%u,\"request\":",kind,interface);hex(request);
  std::printf(",\"fabric\":");frames(fabric);std::printf(",\"core\":");frames(core);std::printf("}\n");
}
#include "aecp_wire_timers.hpp"

int main(int argc,char **argv) {
  Verilated::commandArgs(argc,argv);
  unsigned interface=argc>1?unsigned(std::stoul(argv[1])):0;
  if(interface>=AECP_WIRE_INTERFACES)return 2;
  milan::tb::Model<Vpp_top_wrap> dut;
  H h(dut.get());h.dram.assign(fw::aecp_entity_image,fw::aecp_entity_image+sizeof fw::aecp_entity_image);
  h.reset();h.d->identify_index_i=0;h.amap_edit_mode=true;
  if(!h.boot_to_aecp())return 2;
  h.d->link_up_i=1;h.d->entity_enable_i=1;h.idle(1000);h.flush_all();
  Firmware f(h);unsigned seq=1;
  auto collect=[&](){
    h.run_ms(30);std::vector<B> frames;
    while(!h.q_aecp.empty()){frames.push_back(unpad(h.q_aecp.front()));h.q_aecp.pop_front();}
    return frames;
  };
  auto ask=[&](unsigned cmd,B b=B{},unsigned msg=0,uint64_t controller=CTLR_EID){
    auto request=aecp_frame(OWN_MAC,CTLR_MAC,msg,0,EID,controller,seq++,cmd,b);
    h.flush_all();
#if AECP_WIRE_INTERFACES == 2
    h.d->rx_if_index_i=interface;
#endif
    h.feed(request);
    auto first=unpad(h.wait_any(h.q_aecp,240));auto fabric=collect();
    if(!first.empty())fabric.insert(fabric.begin(),first);
    f.sent.clear();f.sent_interfaces.clear();fw::aecp_rx(&f.a,interface,request.data(),request.size());f.run();
    for(size_t k=0;k<f.sent.size();++k)if(!(f.sent[k][36]&0x80)&&f.sent_interfaces[k]!=interface)
      throw std::runtime_error("wrong response interface");
    record("command",request,fabric,f.sent,interface);
  };
  for(const auto&d:f.descriptors){auto b=B(8);putbe(b.data()+4,d.type,2);putbe(b.data()+6,d.index,2);ask(4,b);}
  for(unsigned type:{0u,1u})for(unsigned config:{1u,65535u}){
    auto b=B(8);putbe(b.data(),config,2);putbe(b.data()+4,type,2);ask(4,b);
  }
  ask(36,B(4),0,CTLR2_EID);ask(0,B(16));ask(1,B(16));auto lock=B(16);lock[3]=1;ask(1,lock);ask(2);ask(7);ask(6,B(4));
  for(auto [cmd,type,offset,width]:std::vector<std::array<unsigned,4>>{{8,5,74,8},{8,6,74,8},{20,2,136,4},{22,36,70,2}}){
    ask(cmd+1,target(type));auto b=target(type,0,std::max(8u,4+width));std::copy(image_row(type,0)+offset,image_row(type,0)+offset+width,b.begin()+4);ask(cmd,b);
  }
  auto name=target(0,0,72);std::fill(name.begin()+8,name.end(),0x4a);ask(16,name);ask(17,target(0,0,8));
  ask(15,target(5));ask(15,target(6));auto si=target(6,0,84);putbe(si.data()+4,0x20000000,4);putbe(si.data()+24,67890,4);ask(14,si);
  auto control=target(26,0,5);control[4]=255;ask(24,control);ask(25,target(26));
  ask(34,target(5));ask(35,target(5));ask(39,target(9));ask(40,B(4));
  for(unsigned t:{5,6,9,36})ask(41,target(t));
  for(unsigned t:{14,15}){ask(43,target(t,0,8));auto b=target(t,0,16);b[5]=1;b[11]=1;b[13]=1;ask(44,b);ask(43,target(t,0,8));ask(45,b);}
  B gdi(12);gdi[1]=4;gdi[7]=9;gdi[9]=5;ask(75,gdi);
  ask(36,B(4));ask(37);ask(38,target(26));ask(0x3fff,B{1,2,3});
  B mvu={0xc5,0x0a,0xc1,0,0,0,0,0};ask(0x001b,mvu,6);mvu[5]=2;ask(0x001b,mvu,6);
  mvu[5]=1;mvu.resize(16);mvu[15]=1;ask(0x001b,mvu,6);
  ask(36,B(4),0,CTLR2_EID);
  ask(1,B(16));ask(1,lock);
  name[8]=0x4b;ask(16,name);
  auto narrow=target(5,0,12);auto fmt=be(image_row(5,0)+74,8);putbe(narrow.data()+4,(fmt&~(uint64_t(1023)<<22))|(uint64_t(4)<<22),8);ask(8,narrow);
  putbe(si.data()+24,123456,4);ask(14,si);
  auto cs=target(36,0,8);cs[5]=1;ask(22,cs);
  auto rate=target(2,0,8);putbe(rate.data()+4,96000,4);ask(20,rate);
  control[4]=0;ask(24,control);ask(34,target(5));ask(35,target(5));
  auto rows=target(14,0,16);rows[5]=1;rows[11]=1;rows[13]=1;ask(44,rows);ask(45,rows);
  ask(37,B{},0,CTLR2_EID);
  h.feed(acmp_frame(CTLR_MAC,6,0,0,CTLR_EID,T1_EID,EID,T1_UID,0,0,0,0x7A00,0,0));
  auto bind=h.wait_any(h.q_acmp,400);
  if(bind.empty() || (be(bind.data()+16,2)>>11)!=0)return 3;
  h.run_ms(1000);h.flush_all();h.gsi_fold_sw=true;f.bound=true;f.started=true;
  if((h.d->acmp_bound_o&1)==0 || (h.d->aecp_strm_started_o&1)==0)return 4;
  if(!h.q_aecp.empty())return 5;
  ask(36,B(4),0,CTLR2_EID);
  ask(35,target(5));ask(15,target(5));ask(34,target(5));ask(15,target(5));
  auto event=[&](unsigned type,unsigned bits){
    h.flush_all();f.sent.clear();fw::aecp_changed(&f.a,type,0,bits);f.run();
    h.d->ctr_change_desc_type_i=type;h.d->ctr_change_desc_index_i=0;
    h.d->ctr_change_i=(bits&8)!=0;h.d->gsi_avb_chg_i=(bits&2)!=0;h.d->gsi_asp_chg_i=(bits&4)!=0;
    h.idle(1);h.d->ctr_change_i=0;h.d->gsi_avb_chg_i=0;h.d->gsi_asp_chg_i=0;
    auto first=unpad(h.wait_any(h.q_aecp,240));auto fabric=collect();
    if(!first.empty())fabric.insert(fabric.begin(),first);
    auto metadata=target(type,0,8);putbe(metadata.data()+4,bits,4);
    record("event",metadata,fabric,f.sent,interface);
  };
  event(9,2);event(9,4);for(unsigned type:{5,6,9,36})event(type,8);
  wire_interfaces(h,f,interface);
  wire_timers(h,f,interface);
  return 0;
}
