// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once

static std::vector<B> drain(H &h) {
  std::vector<B> result;
  while(!h.q_aecp.empty()){result.push_back(unpad(h.q_aecp.front()));h.q_aecp.pop_front();}
  return result;
}

static void wire_timers(H &h,Firmware &f,unsigned interface) {
  unsigned sequence=0x8000;
  auto ask=[&](unsigned cmd,uint64_t controller,B body=B{}){
    auto request=aecp_frame(OWN_MAC,CTLR_MAC,0,0,EID,controller,sequence++,cmd,body);
    h.feed(request);auto first=unpad(h.wait_any(h.q_aecp,240));h.run_ms(30);
    auto fabric=drain(h);if(!first.empty())fabric.insert(fabric.begin(),first);
    f.sent.clear();fw::aecp_rx(&f.a,interface,request.data(),request.size());f.run();
    record("command",request,fabric,f.sent,interface);
  };
  ask(37,CTLR2_EID);
  h.feed(acmp_frame(CTLR_MAC,8,0,0,CTLR_EID,T1_EID,EID,T1_UID,0,0,0,0x7A01,0,0));
  auto unbind=h.wait_any(h.q_acmp,400);
  if(unbind.empty()||(be(unbind.data()+16,2)>>11)!=0)throw std::runtime_error("timer unbind");
  h.run_ms(1000);h.flush_all();if(!h.q_aecp.empty())throw std::runtime_error("timer setup residue");
  f.bound=false;ask(36,CTLR2_EID,B(4));
  auto timer=[&](unsigned at,unsigned wait,const char *kind){
    auto first=unpad(h.wait_any(h.q_aecp,wait));h.run_ms(1);auto fabric=drain(h);
    if(!first.empty())fabric.insert(fabric.begin(),first);
    f.sent.clear();f.time=at;f.run();record(kind,B{},fabric,f.sent,interface);
  };
  timer(30000,61000,"probe");timer(30250,300,"retry");timer(30500,300,"departure");
  ask(36,CTLR2_EID,B(4));ask(1,CTLR_EID,B(16));
  for(unsigned n=0;n<2;++n){
    h.run_ms(20000);f.time+=20000;ask(2,CTLR2_EID);
  }
  timer(90501,20100,"unlock");
}

static void wire_interfaces(H &h,Firmware &f,unsigned interface) {
#if AECP_WIRE_INTERFACES == 2
  auto ask=[&](unsigned port,unsigned cmd){
    auto body=cmd==36?B(4):B{};
    auto request=aecp_frame(OWN_MAC,CTLR_MAC,0,0,EID,CTLR2_EID,0x9000+port+cmd,cmd,body);
    h.d->rx_if_index_i=port;h.feed(request);
    auto first=unpad(h.wait_any(h.q_aecp,240));h.run_ms(30);auto fabric=drain(h);
    if(!first.empty())fabric.insert(fabric.begin(),first);
    f.sent.clear();fw::aecp_rx(&f.a,port,request.data(),request.size());f.run();
    record("command",request,fabric,f.sent,port);
  };
  ask(interface^1,36);ask(interface,37);
  h.d->gsi_avb_chg_i=1;h.idle(1);h.d->gsi_avb_chg_i=0;
  auto first=unpad(h.wait_any(h.q_aecp,240));h.run_ms(30);auto fabric=drain(h);
  if(!first.empty())fabric.insert(fabric.begin(),first);
  f.sent.clear();f.sent_interfaces.clear();fw::aecp_changed(&f.a,9,0,2);f.run();
  if(f.sent_interfaces!=std::vector<unsigned>{interface^1})throw std::runtime_error("registry interface isolation");
  record("interface",B{},fabric,f.sent,interface^1);
  ask(interface^1,37);ask(interface,36);h.d->rx_if_index_i=interface;
#else
  (void)h;(void)f;(void)interface;
#endif
}
