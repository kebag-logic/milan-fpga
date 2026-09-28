// SPDX-License-Identifier: CERN-OHL-W-2.0
// Focused reproductions using the unmodified upstream SRP engine and BFM.
#define main upstream_suite_main_unused
#include "srp_top/sim_main.cpp"
#undef main
#include <stdexcept>
#include <string>
#include <algorithm>

static constexpr uint64_t SID = (OWN_MAC << 16) | 1;
static constexpr uint64_t DA = 0x91e0f0006818ULL;
static void need(bool ok, const char* why) {
  if (!ok) throw std::runtime_error(why);
}
static void listener(H& h, int ev, bool la=false) {
  h.feed(mrpdu_body(true, {Msg{3,8,true,
    {Vec{la,1,fv_sid(SID),{ev},{DECL_READY}}}}}), true);
}
static void start(H& h) {
  h.reset(); h.d->link_up_i=1; h.idle(10);
  auto r=h.op(OP_DECL_TK,1,SID,DA,2,217,1);
  need(r.got && r.status==ST_OK,"declaration service failed");
  h.run_ms(500);
}
static int reg(H& h) { return (h.d->probe_reg_o >> 2)&3; }
static void until(H& h, uint32_t ms) {
  while(h.d->now_ms_o < ms) h.cycle();
}
static bool frame_la(const std::vector<uint8_t>& f) {
  auto p=parse_frame(f);
  if(!p.ok || !p.msrp) return false;
  for(auto& v:p.vecs) if(v.type==3 && v.la) return true;
  return false;
}
static bool ta(const std::vector<uint8_t>& f) {
  return frame_has(f,true,1,SID,EV_NEW) || frame_has(f,true,1,SID,EV_JOININ)
    || frame_has(f,true,1,SID,EV_JOINMT);
}
static void first_bind(H& h) {
  h.reset();h.d->link_up_i=1;h.run_ms(1000);
  need(std::none_of(h.archive.begin(),h.archive.end(),ta),"unrequested talker advertised");
  unsigned t=h.d->now_ms_o;
  auto r=h.op(OP_DECL_TK,1,SID,DA,2,217,1);
  need(r.got && r.status==0,"first declaration failed");
  auto f=h.wait_frame(true,250,ta);
  need(!f.empty(),"first advertisement waited for LeaveAll");
  unsigned adv=h.d->now_ms_o;
  listener(h,EV_NEW);
  need(h.active(1),"Ready did not activate the source");
  printf("FIRST_BIND prompt peer: declare=%u first_TA=%u Ready_done=%u ACTIVE=1; no LeaveAll required\n",t,adv,h.d->now_ms_o);

  // Replaying delayed peer availability cannot establish why the peer delayed.
  h.reset();h.d->link_up_i=1;h.run_ms(1000);
  t=h.d->now_ms_o;
  h.op(OP_DECL_TK,1,SID,DA,2,217,1);
  until(h,t+6080);
  need(!h.active(1),"unexpected active before delayed peer");
  unsigned count=0;for(auto& a:h.archive) count+=ta(a);
  need(count>=5,"periodic advertisements did not persist");
  h.feed(mrpdu_body(true,{la_only(1,25,false),la_only(2,34,false),
                         la_only(3,8,true),la_only(4,4,false)}),true);
  until(h,t+6888);
  need(!h.active(1),"LeaveAll alone activated stream");
  listener(h,EV_NEW);need(h.active(1),"late Ready did not activate");
  printf("FIRST_BIND prescribed peer delay: %u TA frames before +6080 ms LeaveAll; inactive until injected +6888 ms Ready, then ACTIVE=1\n",count);

  // SRP service boundary long hold. ACMP's 15-second policy is not modeled here.
  h.op(OP_WDRW_TK,1);h.run_ms(20000);
  need(!h.active(1),"withdrawn source active during long hold");
  t=h.d->now_ms_o;h.q_msrp.clear();
  h.op(OP_DECL_TK,1,SID,DA,2,217,1);
  f=h.wait_frame(true,250,ta);need(!f.empty(),"long-hold declaration delayed");
  listener(h,EV_NEW);need(h.active(1),"long-hold Ready not activated");
  printf("LONG_HOLD service boundary: 20000 ms withdrawn; re-declare to Ready/ACTIVE %u ms\n",h.d->now_ms_o-t);
}
static void normal_leave(H& h) {
  start(h);listener(h,EV_NEW);need(reg(h)==1 && h.active(1),"setup not IN");
  unsigned t=h.d->now_ms_o;listener(h,EV_LV);
  need(reg(h)==0 && !h.active(1),"IN + Leave did not stop");
  h.run_ms(2000);need(!h.active(1),"source restarted without Ready");
  listener(h,EV_NEW);need(h.active(1),"normal restart failed");
  printf("NORMAL Leave: IN->MT, ACTIVE=0 by decoded PDU; restart after 2000 ms hold, start=%u\n",t);
}
static void own_leaveall_race(H& h, bool renew) {
  start(h);listener(h,EV_NEW);
  unsigned deadline=h.d->probe_la_deadline_o;
  need(deadline>h.d->now_ms_o+500,"own LeaveAll deadline invalid");
  until(h,deadline-100);
  listener(h,EV_JOINMT);need(reg(h)==1,"refresh before own LeaveAll failed");
  size_t base=h.archive.size();
  unsigned guard=500*MS_CYC;
  while(reg(h)!=2 && guard--)h.cycle();
  need(reg(h)==2,"own LeaveAll did not enter LV");
  unsigned entered=h.d->now_ms_o;
  need(std::none_of(h.archive.begin()+base,h.archive.end(),frame_la),"LeaveAll already serialized");
  // Lv is received after the timer event but before the next join-time drain.
  listener(h,EV_LV);
  unsigned leave=h.d->now_ms_o;
  need(reg(h)==2 && h.active(1),"expected LV/ACTIVE after Leave in window");
  unsigned first_wire=0,stop=0;bool dipped=false;
  for(int i=0;i<2000*MS_CYC;i++) {
    h.cycle();dipped |= !h.active(1);
    if(!first_wire && std::any_of(h.archive.begin()+base,h.archive.end(),frame_la))
      first_wire=h.d->now_ms_o;
  }
  need(!dipped && first_wire>leave,"two-second non-stop reproduction failed");
  printf("OWN_LA race: timer/LV=%u ms Lv_decoded=%u ms wire_LA=%u ms; ACTIVE stayed 1 throughout 2000 ms\n",entered,leave,first_wire);
  if(renew) {
    listener(h,EV_NEW);need(reg(h)==1 && h.active(1),"renewal did not cancel leaving");
    for(int i=0;i<4000*MS_CYC;i++){h.cycle();need(h.active(1),"old expiry revoked renewed registration");}
    printf("OWN_LA quick re-declare: IN again, no ACTIVE falling edge, old LeaveTime canceled\n");
  } else {
    guard=4000*MS_CYC;
    while(h.active(1) && guard--)h.cycle();
    stop=h.d->now_ms_o;
    need(!h.active(1) && reg(h)==0,"no-renewal LeaveTime failed to expire");
    need(stop>=entered+4999 && stop<=entered+5005,"unexpected LeaveTime duration");
    printf("OWN_LA no renewal: ACTIVE finally falls at %u ms (%u ms after LV entry)\n",stop,stop-entered);
  }
}
static void received_la(H& h) {
  start(h);listener(h,EV_NEW);
  h.feed(mrpdu_body(true,{la_only(3,8,true)}),true);
  need(reg(h)==2 && h.active(1),"received LeaveAll did not preserve reservation in LV");
  listener(h,EV_LV);need(reg(h)==2 && h.active(1),"LV rLv behavior differs");
  h.run_ms(2000);need(h.active(1),"LV dropped early");
  listener(h,EV_JOINMT);need(reg(h)==1 && h.active(1),"LA recovery failed");
  printf("RECEIVED_LA control: LV + rLv keeps ACTIVE; JoinMt restores IN before expiry\n");
  h.feed(mrpdu_body(true,{la_only(1,25,false)}),true);
  need(reg(h)==1,"Talker-type LeaveAll aged Listener registrar");
  printf("TYPE_SCOPE control: Talker Advertise LeaveAll leaves Listener IN\n");
}
static void phase_sweep(H& h, bool deferred) {
  for(int offset : {-50,-1,1,40,80,120,199}) {
    start(h);listener(h,EV_NEW);
    unsigned deadline=h.d->probe_la_deadline_o;
    until(h,deadline+offset);
    int before=reg(h);listener(h,EV_LV);bool after=h.active(1);
    // Relative to this deterministic draw, the next join is about +105 ms.
    // Only the early negative control expects the counterfactual to differ.
    if(offset<0)need(!after,"Leave before timer did not stop");
    if(offset>0 && offset<100)need(after!=deferred,"timer-before-transmit window mismatch");
    printf("PHASE offset=%+d ms from own deadline=%u: reg_before_Lv=%d ACTIVE_after=%d variant=%s\n",
      offset,deadline,before,after,deferred?"defer registrar to join":"baseline");
  }
}
int main(int argc,char** argv) {
  Verilated::commandArgs(argc,argv);
  try {
    Vsrp_top_wrap d; H h(&d);
    bool deferred=argc>1 && std::string(argv[1])=="deferred";
    first_bind(h);normal_leave(h);
    if(!deferred){own_leaveall_race(h,true);own_leaveall_race(h,false);}
    received_la(h);phase_sweep(h,deferred);
    need(h.malformed==0,"malformed injected PDU");
    printf("PASS: focused reproductions and controls; ACTIVE is SRP licence, no AVTP framer instantiated\n");
    return 0;
  } catch(const std::exception& e){printf("FAIL: %s\n",e.what());return 1;}
}
