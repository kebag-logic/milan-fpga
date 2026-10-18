#include "VKL_srp_domain.h"
#include <cstdio>
#include <vector>
#include <utility>
VKL_srp_domain d;
std::vector<std::pair<int,unsigned>> events;
void tick(){d.clk_i=0;d.eval();if(d.dom_ev_valid_o&&d.dom_ev_ready_i)events.emplace_back(d.dom_ev_event_o,d.dom_ev_value_o);d.clk_i=1;d.eval();}
void run(int n){while(n--)tick();}
void reset(){d.rst_n=0;d.link_up_i=0;d.rxdom_valid_i=0;d.rxdom_lv_i=0;d.rxdom_class_id_i=6;d.rxdom_prio_i=3;d.rxdom_vid_i=2;d.rxdom_nov_i=1;d.periodic_tick_i=0;d.leaveall_tick_i=0;d.tx_tick_i=0;d.dom_ev_ready_i=1;run(3);d.rst_n=1;tick();d.link_up_i=1;run(4);events.clear();}
void rx(bool lv){d.rxdom_valid_i=!lv;d.rxdom_lv_i=lv;tick();d.rxdom_valid_i=0;d.rxdom_lv_i=0;}
void periodic(){d.periodic_tick_i=1;tick();d.periodic_tick_i=0;run(4);}
int fails=0;
void check(bool ok,const char*label){printf("%s %s\n",ok?"PASS":"FAIL",label);fails+=!ok;}
int main(int argc, char**){
 bool contract=argc>1;
 reset();periodic();check(events.size()==1&&events[0].first==3,"no peer -> JoinMt");
 reset();rx(false);periodic();check(events.size()==1&&events[0].first==1,"matching peer -> JoinIn");
 events.clear();rx(true);periodic();check(events.size()==1&&events[0].first==3,"rLv -> next periodic JoinMt");
 reset();rx(false);d.dom_ev_ready_i=0;periodic();check(d.dom_ev_valid_o&&d.dom_ev_event_o==1,"queued JoinIn before withdrawal");rx(true);run(4);printf("OBS queued event after rLv while not accepted: event=%d valid=%d\n",d.dom_ev_event_o,d.dom_ev_valid_o);d.dom_ev_ready_i=1;run(4);if(contract)check(events.size()==1&&events[0].first==3,"DOC293/309: rejoin accepted after Lv is JoinMt");periodic();check(events.size()==2&&events[0].first==1&&events[1].first==3,"queued old JoinIn then fresh JoinMt");
 reset();rx(false);d.periodic_tick_i=1;tick();d.periodic_tick_i=0;rx(true);run(4);printf("OBS withdrawal at enqueue: accepted-event=%d\n",events.empty()?-1:events[0].first);events.clear();periodic();check(events.size()==1&&events[0].first==3,"fresh rejoin after enqueue collision is JoinMt");
 reset();d.dom_ev_ready_i=0;periodic();rx(false);run(4);printf("OBS queued event after registration while not accepted: event=%d valid=%d\n",d.dom_ev_event_o,d.dom_ev_valid_o);d.dom_ev_ready_i=1;run(4);if(contract)check(events.size()==1&&events[0].first==1,"DOC293: rejoin samples registrar at acceptance");periodic();check(events.size()==2&&events[0].first==3&&events[1].first==1,"queued old JoinMt then fresh JoinIn");
 printf("%d FAIL\n",fails);return fails?1:0;
}
