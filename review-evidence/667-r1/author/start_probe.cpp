// SPDX-License-Identifier: CERN-OHL-W-2.0
// Startup at the shipping 1x1 eight-channel packetizer boundary.
#include "VKL_aaf_packetizer.h"
#include "verilator_harness.hpp"
#include <array>
#include <cstdint>
#include <cstdio>
#include <vector>

using Frame = std::vector<uint8_t>;
class Probe {
 public:
  milan::tb::Model<VKL_aaf_packetizer> model;
  VKL_aaf_packetizer* d = model.get();
  std::vector<Frame> frames;
  Frame frame;
  uint64_t now = 0;
  void tick() {
    d->ptp_ns_i = now;
    d->clk_i = 0; d->eval();
    if (d->m_axis_tvalid && d->m_axis_tready) {
      for (int b=0;b<8;++b) if ((d->m_axis_tkeep >> b)&1)
        frame.push_back(d->m_axis_tdata >> (8*b));
      if (d->m_axis_tlast) {frames.push_back(frame); frame.clear();}
    }
    d->clk_i = 1; d->eval();
    now += 20;
  }
  void cycles(int n) {while(n--) tick();}
  void sample(unsigned n, int enable_at=-100) {
    // The capture-map walk emits four channel pairs on consecutive ticks.
    // 1041,1042,1042 cycles reproduce a 48 kHz media grid at 50 MHz.
    for (int k=0;k<((n%3)==0 ? 1041:1042);++k) {
      if (k==enable_at) d->stream_en_i=1;
      d->pair_valid_i=k<4;
      d->pair_slot_i=k<4 ? k:0;
      d->pair_l_i=(n<<4)+(k*2);
      d->pair_r_i=(n<<4)+(k*2)+1;
      tick();
    }
    d->pair_valid_i=0;
  }
  void reset(uint64_t base) {
    now=base;
    d->rst_n=0; d->stream_en_i=0; d->pair_valid_i=0;
    d->m_axis_tready=1;
    d->dest_mac_i=0x91e0f0000001ULL; d->station_mac_i=0x020000000001ULL;
    d->vlan_vid_i=2; d->vlan_pcp_i=3; d->dom_ovr_i=0;
    d->transit_ns_i=2000000; d->ts_uncertain_i=0; d->mr_i=0;
    d->tctx_wr_en_i=0; d->tctx_rd_en_i=0;
    cycles(4); d->rst_n=1; cycles(4);
  }
  static uint32_t word(const Frame& f,unsigned p) {
    return (uint32_t(f[p])<<24)|(uint32_t(f[p+1])<<16)|(uint32_t(f[p+2])<<8)|f[p+3];
  }
};
int main(int argc,char** argv) {
  Verilated::commandArgs(argc,argv);
  int fail=0;
  for (uint64_t base: {uint64_t(1000000000),uint64_t(0xffe00000)}) {
    for (int phase: {0,1,2,3,4,5,1040}) {
      Probe p; p.reset(base);
      p.d->stream_en_i=1;
      for(unsigned n=0;n<13;++n) p.sample(n);
      p.d->stream_en_i=0; p.cycles(8);
      // A stopped stream sees a later PHC on restart. No timestamp is
      // written while disabled; eliding idle cycles preserves that state.
      p.now+=3800000000ULL;
      p.frames.clear(); p.frame.clear();
      p.sample(13,phase);
      for(unsigned n=14;n<80 && p.frames.size()<10;++n) p.sample(n);
      bool ok=p.frames.size()>=10;
      uint32_t prev=0;
      for(unsigned k=0;k<p.frames.size() && k<10;++k) {
        const auto& f=p.frames[k];
        if(f.size()!=234) {ok=false; continue;}
        uint32_t ts=Probe::word(f,30);
        int64_t step= k ? int64_t(int32_t(ts-prev)):0;
        printf("PDU base=%llu phase=%d n=%u seq=%u tv=%u ts=%08x step=%lld\n",
               (unsigned long long)base,phase,k+1,f[20],f[19]&1,ts,(long long)step);
        if(k && step!=125000) ok=false;
        if(!(f[19]&1)) ok=false;
        prev=ts;
      }
      printf("START base=%llu phase=%d frames=%zu %s\n",
             (unsigned long long)base,phase,p.frames.size(),ok?"PASS":"FAIL");
      fail+=!ok;
    }
  }
  printf("STARTUP failures=%d\n",fail);
  return fail?1:0;
}
