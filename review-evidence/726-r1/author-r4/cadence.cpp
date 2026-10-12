// Isolated unchanged notification RTL probe; the response engine is modeled.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <tuple>
#include <vector>
#include "VKL_aecp_notify.h"
#include "verilated.h"
#ifndef STREAMS
#define STREAMS 2
#endif
struct Send { uint64_t cycle; unsigned type, index, recipient; };
int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  VKL_aecp_notify d;
  uint64_t cycle=0;
  constexpr uint64_t cpm=50000; // 50 MHz, the shipping Milan clock.
  auto tick=[&]() { d.now_ms_i=cycle/cpm; d.clk_i=0; d.eval(); d.clk_i=1; d.eval(); ++cycle; };
  d.rst_n=0; d.prng_draw_busy_i=1; d.ca_ready_i=1; d.uns_done_i=0;
  for (int i=0;i<4;++i) tick();
  d.rst_n=1;
  for (int i=0;i<4;++i) tick();
  for (unsigned r=0;r<2;++r) {
    d.rgy_req_i=1; d.rgy_op_i=0; d.rgy_state_i=0; d.rgy_tl_i=0;
    d.rgy_eid_i=0x1111000000000001ULL+r;
    d.rgy_mac_i=0x020000000001ULL+r;
    unsigned guard=0;
    for (;;) { d.clk_i=0; d.eval(); if(!d.rgy_wait_o) break; tick(); if(++guard>100) return 2; }
    if(d.rgy_data_o) return 3;
    tick(); d.rgy_req_i=0; for(int i=0;i<4;++i) tick();
  }
  if(d.dbg_reg_cnt_o!=2) return 4;
  constexpr unsigned descriptors=2*STREAMS+2;
  std::vector<Send> sends;
  bool held=false;
  uint64_t release=0;
  const uint64_t begin=cycle, end=begin+2200*cpm;
  for (;cycle<end;) {
    // Give every descriptor a continuously changing source, so missing upstream
    // pulses cannot explain any scheduler gap in this probe.
    const unsigned desc=cycle%descriptors;
    d.ev_ctr_i=1;
    d.ev_ctr_type_i=desc<STREAMS?5:desc<2*STREAMS?6:desc==2*STREAMS?9:36;
    d.ev_ctr_index_i=desc<2*STREAMS?desc%STREAMS:0;
    d.now_ms_i=cycle/cpm; d.clk_i=0; d.eval();
    d.uns_done_i=0;
    if(d.uns_valid_o) {
      const unsigned r=unsigned(d.uns_mac_o-0x020000000001ULL);
      if(d.uns_kind_o!=6 || r>1) return 5;
      // One legal, bounded 2 ms wait at the response-engine completion seam.
      // Every other notification completes immediately when presented.
      if(!held && r==1) { held=true; release=cycle+2*cpm; }
      if(cycle>=release) {
        sends.push_back({cycle,unsigned(d.uns_desc_type_o),unsigned(d.uns_desc_index_o),r});
        d.uns_done_i=1;
      }
    }
    tick();
  }
  std::map<std::tuple<unsigned,unsigned,unsigned>,std::vector<uint64_t>> rows;
  for(const auto&s:sends) rows[{s.type,s.index,s.recipient}].push_back(s.cycle);
  unsigned late=0, early=0;
  std::puts("type,index,recipient,sends_0_1s,sends_1_2s,sends_2_2p2s,min_gap_ms,max_gap_ms,first_send_ms");
  for(const auto &[key,v]:rows) {
    auto [type,index,recipient]=key;
    uint64_t lo=UINT64_MAX,hi=0; std::array<unsigned,3> counts{};
    for(size_t i=0;i<v.size();++i) {
      ++counts[std::min<uint64_t>(2,(v[i]-begin)/(1000*cpm))];
      if(i) {const uint64_t gap=v[i]-v[i-1]; lo=std::min(lo,gap); hi=std::max(hi,gap);}
    }
    if(hi>1000*cpm) ++late;
    if(lo<1000*cpm) ++early;
    std::printf("%04x,%u,%u,%u,%u,%u,%.5f,%.5f,%.5f\n",type,index,recipient,counts[0],counts[1],counts[2],double(lo)/cpm,double(hi)/cpm,double(v.front()-begin)/cpm);
  }
  std::printf("rows=%zu expected=%u late_rows=%u early_rows=%u model_clock_hz=50000000 modeled_initial_wait_ms=2\n",rows.size(),2*descriptors,late,early);
  if(rows.size()!=2*descriptors || !late) return 6;
  std::puts("PROBE_COMPLETE: maximum one-second cadence fails in unchanged scheduler; this is not a wire acceptance test.");
  return 0;
}
