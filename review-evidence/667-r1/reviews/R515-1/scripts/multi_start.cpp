// Independent packet-boundary probe: eight talkers, mixed widths and offsets.
#include "VKL_aaf_packetizer.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <cstdio>
#include <map>
#include <vector>

struct Probe {
  VKL_aaf_packetizer d;
  std::array<int,8> width{}, base{}, count{}, seq{};
  std::map<unsigned,std::array<uint32_t,8>> stamps;
  std::vector<uint8_t> frame;
  uint64_t now = 0xfff00000ULL;
  unsigned clocks=0, checks=0, failures=0;
  bool grade=false;
  void ck(bool yes) { ++checks; if (!yes) ++failures; }
  uint32_t word(unsigned p) {
    uint32_t v=0; for (int i=0;i<4;++i) v=(v<<8)|frame.at(p+i); return v;
  }
  void packet() {
    if (!grade) {frame.clear();return;}
    int t=frame.at(29);
    ck(t>=0 && t<8);
    if(t<0 || t>=8) {frame.clear();return;}
    unsigned first=word(42)>>16;
    ck(frame.size()==unsigned(42+24*width[t]));
    ck(frame.at(19)&1);
    ck(stamps.count(first));
    if(stamps.count(first)) ck(word(30)==uint32_t(stamps[first][t]+2000000+t*1000));
    for(int r=0;r<6;++r) for(int c=0;c<width[t];++c)
      ck(word(42+4*(r*width[t]+c))==uint32_t(((first+r)*256+t*16+c)<<8));
    if(count[t]) ck(frame.at(20)==uint8_t(seq[t]+1));
    seq[t]=frame.at(20); ++count[t];frame.clear();
  }
  void tick() {
    d.ptp_ns_i=now; d.m_axis_tready=(clocks%19)>=7;
    d.clk_i=0;d.eval();
    if(d.m_axis_tvalid && d.m_axis_tready) {
      for(int i=0;i<8;++i) if((d.m_axis_tkeep>>i)&1) frame.push_back(d.m_axis_tdata>>(8*i));
      if(d.m_axis_tlast) packet();
    }
    d.clk_i=1;d.eval();now+=20;++clocks;
  }
  void idle(int n) {d.pair_valid_i=0;while(n--) tick();}
  void sample(unsigned n,int phase=-1) {
    for(int k=0;k<(n%3==0?1041:1042);++k) {
      if(k==phase) {d.rst_n=1;d.stream_en_i=255;}
      d.pair_valid_i=0;
      for(int t=0;t<8;++t) {
        if(k==base[t]) stamps[n][t]=uint32_t(now);
        if(k>=base[t] && k<base[t]+width[t]/2) {
          int c=2*(k-base[t]);d.pair_valid_i=1;d.pair_slot_i=k;
          d.pair_l_i=n*256+t*16+c;d.pair_r_i=n*256+t*16+c+1;
        }
      }
      tick();
    }
  }
  int run(int phase,bool mixed,bool reset_start) {
    d.rst_n=0;d.stream_en_i=0;d.tctx_wr_en_i=0;d.tctx_rd_en_i=0;
    d.station_mac_i=0x020000000001ULL;d.dest_mac_i=0x91e0f0000001ULL;
    d.vlan_vid_i=2;d.vlan_pcp_i=3;d.dom_ovr_i=0;d.ts_uncertain_i=0;d.mr_i=0;
    for(int t=0;t<8;++t) d.transit_ns_i[t]=2000000+t*1000;
    idle(4);d.rst_n=1;idle(4);
    int offset=0;
    for(int t=0;t<8;++t) {
      width[t]=mixed ? 2+2*(t%4) : 8;base[t]=offset;offset+=width[t]/2;
      d.tctx_wr_en_i=1;d.tctx_wr_addr_i=t*16;d.tctx_wr_data_i=width[t]<<1;idle(1);
    }
    d.tctx_wr_en_i=0;d.stream_en_i=255;
    for(unsigned n=0;n<13;++n) sample(n);
    if(reset_start) d.rst_n=0;else d.stream_en_i=0;
    idle(8);now+=3800000000ULL;frame.clear();stamps.clear();grade=true;
    sample(13,phase);
    for(unsigned n=14;n<80;++n) sample(n);
    for(int t=0;t<8;++t) ck(count[t]>=10);
    std::printf("multi phase=%d mixed=%d reset=%d checks=%u failures=%u counts=",
                phase,mixed,reset_start,checks,failures);
    for(int n:count) std::printf("%d,",n);std::puts("");
    return failures;
  }
};
int main(int argc,char**argv) {
  Verilated::commandArgs(argc,argv);
  unsigned failures=0;
  for(bool mixed:{false,true}) for(bool reset:{false,true}) {
    if(mixed && reset) continue;
    for(int phase:{0,1,2,3,4,7,8,15,16,19,20,27,28,31,32,1040}) {
      Probe p;failures+=p.run(phase,mixed,reset);
    }
  }
  std::printf("multi-start failures=%u\n",failures);
  return failures?1:0;
}
