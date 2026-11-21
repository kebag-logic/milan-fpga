#include "VKL_aaf_rx_depacketizer.h"
#include "verilated.h"
#include <cstdio>
#include <vector>
VKL_aaf_rx_depacketizer d;
unsigned beatsout=0,ends=0;
void tick(){d.clk_i=0;d.eval();if(d.m_axis_tvalid){++beatsout;if(d.m_axis_tlast)++ends;}d.clk_i=1;d.eval();}
int main(int argc,char**argv){
 Verilated::commandArgs(argc,argv);
 for(unsigned size:{64u,65u}){
  d.rst_n=0;d.s_tvalid_i=0;d.s_tready_i=1;d.m_axis_tready=1;
#ifdef BASE
  d.pdu_accept_p_i=0;d.pdu_accept_idx_i=0;
#else
  d.pdu_enq_p_i=0;d.pdu_done_p_i=0;d.pdu_done_mask_i=1;
#endif
  for(int k=0;k<4;++k)tick();d.rst_n=1;beatsout=0;ends=0;
  std::vector<unsigned char> f(size+38);f[12]=0x22;f[13]=0xf0;f[14]=2;f[15]=0x81;f[35]=size;
  for(unsigned k=0;k<size;++k)f[38+k]=k;
  unsigned beats=(f.size()+7)/8;
  for(unsigned b=0;b<beats;++b){
   d.s_tdata_i=0;unsigned n=0;for(unsigned k=0;k<8&&b*8+k<f.size();++k){d.s_tdata_i|=uint64_t(f[b*8+k])<<(k*8);++n;}
   d.s_tvalid_i=1;d.s_tkeep_i=(1u<<n)-1;d.s_tlast_i=b+1==beats;
#ifdef BASE
   d.pdu_accept_p_i=b==8;
#else
   d.pdu_enq_p_i=b==8;d.pdu_done_p_i=b==10;
#endif
   tick();
  }
  d.s_tvalid_i=0;d.s_tlast_i=0;
#ifdef BASE
  d.pdu_accept_p_i=0;
#else
  d.pdu_enq_p_i=0;d.pdu_done_p_i=0;
#endif
  for(int k=0;k<200;++k)tick();
  printf("payload=%u output_beats=%u output_last=%u expected_beats=%u expected_last=1\n",size,beatsout,ends,(size+7)/8);
 }
}
