#include "VKL_aaf_rx_depacketizer.h"
#include "verilated.h"
#include <array>
#include <vector>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
using Bytes=std::vector<uint8_t>;
VKL_aaf_rx_depacketizer d;
std::array<std::vector<Bytes>,8> actual,expected;
Bytes partial;
uint64_t cycle=0,stampcycle=0,helddata=0;
unsigned helduser=0,heldlast=0,headers=0,checks=0;
bool held=false;
uint32_t randomstate=918273;
void ck(bool yes,const char* msg){++checks;if(!yes){printf("FAIL cycle=%llu %s\n",(unsigned long long)cycle,msg);exit(1);}}
void tick(bool ready=true){
 d.clk_i=0;d.m_axis_tready=ready;d.eval();
 if(d.rst_n && held){ck(d.m_axis_tvalid && d.m_axis_tdata==helddata && d.m_axis_tuser==helduser && d.m_axis_tlast==heldlast,"held beat stable");}
 held=d.rst_n && d.m_axis_tvalid && !ready;helddata=d.m_axis_tdata;helduser=d.m_axis_tuser;heldlast=d.m_axis_tlast;
 if(d.rst_n && d.hdr_p_o){++headers;stampcycle=cycle;ck(d.hdr_tv_o && d.hdr_ts_o==0x12345678,"timestamp per replay");}
 if(d.rst_n && d.m_axis_tvalid && ready){
  ck(cycle-stampcycle>=16,"timestamp lead");ck(d.m_axis_tuser<8,"valid input tag");
  for(unsigned k=0;k<8;++k)partial.push_back(d.m_axis_tdata>>(8*k));
  if(d.m_axis_tlast){actual[d.m_axis_tuser].push_back(partial);partial.clear();}
 }
 d.clk_i=1;d.eval();++cycle;
}
bool ready(){randomstate^=randomstate<<13;randomstate^=randomstate>>17;randomstate^=randomstate<<5;return (randomstate&7)>2;}
void reset(){d.rst_n=0;d.s_tvalid_i=0;d.pdu_enq_p_i=0;d.pdu_done_p_i=0;held=false;for(int k=0;k<4;++k)tick();d.rst_n=1;tick();partial.clear();}
void send(unsigned bytes,bool vlan,unsigned mask,unsigned serial,bool record=true){
 unsigned o=vlan?18:14;Bytes f(o+24+bytes,0),payload(bytes);
 f[12]=vlan?0x81:0x22;f[13]=vlan?0:0xf0;if(vlan){f[16]=0x22;f[17]=0xf0;}
 f[o]=2;f[o+1]=0x81;f[o+12]=0x12;f[o+13]=0x34;f[o+14]=0x56;f[o+15]=0x78;
 f[o+20]=bytes>>8;f[o+21]=bytes;
 for(unsigned k=0;k<bytes;++k)f[o+24+k]=payload[k]=(k*17+serial*31)&255;
 payload.resize((bytes+7)/8*8);
 if(record)for(unsigned s=0;s<8;++s)if(mask>>s&1)expected[s].push_back(payload);
 unsigned beats=(f.size()+7)/8;
 for(unsigned b=0;b<beats;++b){
  uint64_t data=0;unsigned n=0;for(unsigned k=0;k<8 && b*8+k<f.size();++k){data|=uint64_t(f[b*8+k])<<(8*k);++n;}
  d.s_tvalid_i=1;d.s_tready_i=1;d.s_tlast_i=b+1==beats;d.s_tdata_i=data;d.s_tkeep_i=(1u<<n)-1;
  d.pdu_enq_p_i=b==8;d.pdu_done_p_i=b==10;d.pdu_done_mask_i=mask;tick(ready());
 }
 d.s_tvalid_i=0;d.s_tlast_i=0;d.pdu_enq_p_i=0;d.pdu_done_p_i=0;
}
int main(int argc,char**argv){
 Verilated::commandArgs(argc,argv);reset();
 unsigned serial=0,total=0;
 for(bool vlan:{false,true})for(unsigned size:{64u,72u,192u,384u,768u,1984u})for(unsigned mask:{0u,1u,2u,0x81u,0x55u,0xffu}){
  printf("case size=%u vlan=%u mask=%02x\n",size,vlan,mask);
  send(size,vlan,mask,serial++);for(unsigned s=0;s<8;++s)total+=(mask>>s)&1;
  for(unsigned k=0;k<size*18+2000;++k)tick(ready());
  for(unsigned s=0;s<8;++s)ck(actual[s]==expected[s],"exact ordered payload per input");
 }
 ck(headers==total,"one timestamp header per delivered copy");ck(d.drops_o==0,"drained legal frames do not overflow");
 send(192,false,255,serial++,false);for(unsigned k=0;k<20;++k)tick(false);reset();
 for(unsigned k=0;k<200;++k)tick();ck(!d.m_axis_tvalid,"reset clears pending replay");
 for(auto&v:actual)v.clear();for(auto&v:expected)v.clear();
 send(192,true,0x81,serial++);for(unsigned k=0;k<3000;++k)tick(ready());
 for(unsigned s=0;s<8;++s)ck(actual[s]==expected[s],"post-reset isolation and recovery");
 printf("PASS independent depacketizer probe: %u checks; 72 cases, both tag forms, masks, stalls, long frames, timestamp lead, reset\n",checks);
}
