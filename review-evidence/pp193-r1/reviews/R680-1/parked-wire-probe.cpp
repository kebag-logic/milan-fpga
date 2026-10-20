// SPDX-License-Identifier: CERN-OHL-W-2.0
// Issue #193/#188: test a reoccupied parked value through the complete SRP datapath.
#define main original_suite_main
#include "sim_main.cpp"
#undef main

int main(int argc,char** argv) {
  Verilated::commandArgs(argc,argv);
  const milan::tb::Model<Vsrp_top_wrap> model;
  auto* d=model.get(); H h(d);
  constexpr uint64_t sid=0x1122334455660001ULL, da=0x91E0F0112233ULL;
  int fails=0;
  for(int old=0;old<2;++old) {
    const int fresh=1-old;
    h.reset();d->link_up_i=1;h.run_ms(700);
    h.op(OP_DECL_LS,old,sid,da,2,0,0,DECL_READY);
    Msg adv{1,25,false,{Vec{false,1,fv_talker(sid,da,2,256,1,3,1,500),{EV_JOININ},{}}}};
    h.feed(mrpdu_body(true,{adv}),true);
    h.run_ms(1500);h.sync();
    if(h.ls_decl(old)!=DECL_READY) return 2;
    auto from=h.archive.size();
    h.op(OP_WDRW_LS,old);
    h.op(OP_DECL_LS,old,sid+1,da+1,2,0,0,DECL_READY);
    h.op(OP_DECL_LS,fresh,sid,da,2,0,0,DECL_READY);
    h.feed(mrpdu_body(true,{adv}),true);h.idle(10);
    if(h.ls_decl(fresh)!=DECL_READY || h.tk_reg(fresh)!=1) return 3;
    h.run_ms(250);
    int count=0,leaves=0;bool in=true;
    printf("old_sink=%d current_sink=%d declared=%d\n",old,fresh,h.ls_decl(fresh));
    for(size_t j=from;j<h.archive.size();++j) {
      auto pf=parse_frame(h.archive[j]);if(!pf.ok || !pf.msrp) continue;
      bool relevant=false;
      for(const auto& v:pf.vecs) {
        if(v.type!=3)continue;
        for(int k=0;k<v.nov;++k) {
          if(fv_u64(v.fv,0,8)+k!=sid)continue;
          relevant=true;++count;
          if(v.ev[k]==EV_LV){++leaves;in=false;}
          if(v.ev[k]==EV_NEW || v.ev[k]==EV_JOININ || v.ev[k]==EV_JOINMT) in=true;
          printf("  wire event=%d fourpacked=%d peer_IN=%d\n",v.ev[k],v.fp[k],in);
        }
      }
      if(relevant)dump("wire",h.archive[j]);
    }
    bool pass=count==1 && leaves==0 && in;
    printf("%s: one Listener value and no withdrawal while declared: values=%d Lv=%d peer_IN=%d\n",
           pass?"PASS":"FAIL",count,leaves,in);
    fails+=!pass;
  }
  printf("2 checks: %d PASS, %d FAIL\n",2-fails,fails);
  return fails?1:0;
}
