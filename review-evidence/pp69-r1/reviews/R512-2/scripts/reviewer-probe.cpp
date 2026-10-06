// Reviewer-owned port-face checks; no hierarchical state modification.
#include <cstdio>
#include <cstdint>
#include <set>
#include <vector>
#include "VKL_aecp_notify.h"
#include "verilated.h"
VKL_aecp_notify d;
int failures=0, checks=0;
void check(bool ok,const char* name){++checks;printf("%s: %s\n",ok?"PASS":"FAIL",name);if(!ok)++failures;}
void tick(){d.clk_i=0;d.eval();d.clk_i=1;d.eval();}
void idle(unsigned n){while(n--)tick();}
void low(){d.clk_i=0;d.eval();}
uint64_t eid(unsigned n){return 0xabc0000000000000ULL+n;}
uint64_t mac(unsigned n){return 0x020000000000ULL+n;}
uint64_t op(unsigned code,unsigned n,unsigned port,bool tl=false){
 d.rgy_state_i=0;d.rgy_op_i=code;d.rgy_eid_i=eid(n);d.rgy_mac_i=mac(n);d.rgy_tl_i=tl;
#ifdef HEAD_SEAM
 d.rgy_port_i=port;
#else
 (void)port;
#endif
 d.rgy_req_i=1;uint64_t result=~0ULL;
 for(unsigned i=0;i<160;++i){low();if(!d.rgy_wait_o){result=d.rgy_data_o;break;}tick();}
 tick();d.rgy_req_i=0;idle(3);return result;
}
void expire(unsigned slot,unsigned owner){d.tmr_exp_valid_i=1;d.tmr_exp_slot_i=slot;d.tmr_exp_owner_i=owner;tick();d.tmr_exp_valid_i=0;}
int main(int argc,char**argv){
 Verilated::commandArgs(argc,argv);d.prng_draw_busy_i=1;d.now_ms_i=1000;d.rst_n=0;idle(4);d.rst_n=1;idle(4);
#ifdef DEPTH16
 bool good=true;
 for(unsigned port=0;port<2;++port){for(unsigned i=0;i<16;++i){auto r=op(0,port*32+i+1,port,true);printf("REG port=%u controller=%u result=%llu count=%u\n",port,i,(unsigned long long)r,d.dbg_reg_cnt_o);good &=r==0;}
  auto r=op(0,100+port,port,true);printf("OVERFLOW port=%u result=%llu\n",port,(unsigned long long)r);good &=r==1;}
 check(good&&d.dbg_reg_cnt_o==32,"D16 capacity is 16 per interface; each seventeenth is refused");
 d.ev_cmd_class_i=7;d.ev_cmd_type_i=2;d.ev_cmd_index_i=0;d.ev_cmd_excl_eid_i=eid(999);d.ev_cmd_i=1;tick();d.ev_cmd_i=0;
 std::set<uint64_t> recipients;unsigned jobs=0;bool seq=true;
 for(unsigned c=0;c<4000;++c){low();if(d.uns_valid_o){recipients.insert(d.uns_mac_o);++jobs;seq &=d.uns_seq_o==0;d.uns_done_i=1;tick();d.uns_done_i=0;}else tick();}
 check(jobs==32&&recipients.size()==32&&seq,"D16 fanout reaches all 32 distinct registrations at initial sequence zero");
 good=op(1,33,1)==0&&d.dbg_reg_cnt_o==31;
 good &=op(0,101,0)==1&&d.dbg_reg_cnt_o==31;
 good &=op(0,101,1)==0&&d.dbg_reg_cnt_o==32;
 check(good,"D16 freeing a port-1 row allows port 1 only to refill");
#else
 check(op(0,1,0,true)==0&&op(0,2,0)==0&&d.dbg_reg_cnt_o==2,"C1 setup two controllers");
 d.prng_draw_busy_i=0;
 for(unsigned c=0;c<30;++c){low();bool req=d.prng_draw_req_o;tick();d.prng_draw_valid_i=req;d.prng_draw_ms_i=30000;}
 d.prng_draw_valid_i=0;d.prng_draw_busy_i=1;idle(3);
 d.ca_ready_i=0;expire(27,0xd0);idle(3);expire(28,0xd1);idle(3);d.ca_ready_i=1;
 unsigned probes=0;for(unsigned c=0;c<20;++c){low();if(d.ca_valid_o)probes|=1u<<d.ca_owner_o;tick();}
 check(probes==3,"C1 both probes issued");
 expire(25,0xa0);unsigned cancels=0;bool collision=false;
 for(unsigned c=0;c<16;++c){low();if(!collision&&d.ca_cancel_valid_o&&d.ca_cancel_owner_o==0){d.rx_cmd_eid_i=eid(2);d.rx_cmd_mac_i=mac(2);d.rx_cmd_valid_i=1;collision=true;low();}
  if(d.ca_cancel_valid_o)cancels|=1u<<d.ca_cancel_owner_o;tick();d.rx_cmd_valid_i=0;}
 printf("C1 collision=%u cancel_mask=%u remaining=%u\n",collision,cancels,d.dbg_reg_cnt_o);
 check(collision&&cancels==1&&d.dbg_reg_cnt_o==1,"C1 known baseline gap: drain cancel wins, command cancel absent");
 d.ca_fail_valid_i=1;d.ca_fail_owner_i=1;tick();d.ca_fail_valid_i=0;
 for(unsigned c=0;c<80;++c){low();d.uns_done_i=d.uns_valid_o;tick();}d.uns_done_i=0;
 printf("C1 after_orphan_failure remaining=%u\n",d.dbg_reg_cnt_o);
 check(d.dbg_reg_cnt_o==0,"C1 known baseline gap: orphan failure removes remaining row");
#endif
 printf("reviewer probe: %d checks, %d failures\n",checks,failures);return failures?1:0;
}
