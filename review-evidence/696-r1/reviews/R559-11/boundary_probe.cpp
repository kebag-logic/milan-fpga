// Independent boundary and handshake probes for the frozen #696 contract.
#include "VKL_maap.h"
#include "verilator_harness.hpp"
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <vector>
using Bytes=std::vector<uint8_t>;
int checks=0, failures=0;
void check(bool ok,const char* name) { ++checks; if(!ok) { ++failures; std::printf("FAIL %s\n",name); } }
struct Bench {
  const milan::tb::Model<VKL_maap> model;
  VKL_maap* d=model.get();
  std::vector<Bytes> frames; Bytes current;
  void tick() {
    d->clk_i=0; d->eval();
    if(d->m_axis_tvalid && d->m_axis_tready) {
      for(unsigned i=0;i<8;++i) if((d->m_axis_tkeep>>i)&1) current.push_back(d->m_axis_tdata>>(8*i));
      if(d->m_axis_tlast) { frames.push_back(current); current.clear(); }
    }
    d->clk_i=1; d->eval();
  }
  void cycles(unsigned n) { while(n--) tick(); }
  void reset() {
    d->rst_n=0; d->enable_i=0; d->port_operational_i=1;
    d->station_mac_i=0x020000000010ULL; d->realtime_ns_i=29;
    d->count_i=8; d->seed_valid_i=1; d->seed_offset_i=0x100;
    d->m_axis_tready=1; d->rx_tvalid_i=0; d->rx_tready_i=1; d->rx_tlast_i=0;
    cycles(4); frames.clear();current.clear(); d->rst_n=1; cycles(2);
  }
  void begin(bool announce) {
    d->enable_i=1;
    for(unsigned i=0;i<20000 && frames.size()<(announce?5u:1u);++i) tick();
    check(frames.size()==(announce?5u:1u),"setup full walk");
    frames.clear();
  }
  static uint64_t field(const Bytes& b,unsigned start,unsigned n) {
    if(b.size()<start+n) return UINT64_MAX;
    uint64_t result=0; for(unsigned i=0;i<n;++i) result=(result<<8)|b[start+i]; return result;
  }
  static void put(Bytes& b,unsigned start,unsigned n,uint64_t value) {
    for(unsigned i=0;i<n;++i) b[start+n-i-1]=value>>(8*i);
  }
  void inject(unsigned type,unsigned length,int missing=-1,unsigned requested=0xfe,unsigned count=0x102) {
    Bytes b(64,0); put(b,0,6,0x91e0f000ff00ULL);put(b,6,6,0x020000000001ULL);
    put(b,12,2,0x22f0);b[14]=0xfe;b[15]=type;b[16]=8;b[17]=16;
    put(b,26,6,0x91e0f0000000ULL|requested);put(b,32,2,count);
    put(b,34,6,0x91e0f0000100ULL);put(b,40,2,8);
    for(unsigned off=0;off<length;off+=8) {
      uint64_t data=0;for(unsigned i=0;i<8;++i)data|=uint64_t(b[off+i])<<(8*i);
      unsigned keep=(1u<<std::min(8u,length-off))-1;
      if(missing>=int(off)&&missing<int(off+8))keep&=~(1u<<(missing-off));
      d->rx_tdata_i=data;d->rx_tkeep_i=keep;d->rx_tvalid_i=1;d->rx_tlast_i=off+8>=length;
      d->rx_tready_i=0;cycles(2); // unaccepted beats must not advance parsing
      d->rx_tready_i=1;tick();d->rx_tvalid_i=0;cycles(2); // valid gaps too
    }
    d->rx_tlast_i=0;cycles(3);
  }
};
int main(int argc,char**argv) {
  Verilated::commandArgs(argc,argv);
  // Every truncation and missing-byte position, each event/state; a later valid
  // 42-byte frame must still work. Reinitialize so timer phase cannot hide RX effects.
  for(bool announced:{false,true})for(unsigned type:{1u,2u,3u}) {
    for(int defect=0;defect<83;++defect) {
      Bench b;b.reset();b.begin(announced);
      b.inject(type,defect<41?unsigned(defect+1):60u,defect<41?-1:defect-41);
      check(b.d->state_o==(announced?2:1)&&b.d->offset_o==0x100&&b.d->conflicts_o==0&&b.d->defends_o==0,"incomplete frame leaves allocation untouched");
      b.inject(type,42);
      if(announced && type==1) {
        b.cycles(30);check(b.frames.size()==1&&Bench::field(b.frames[0],26,6)==0x91e0f00000feULL&&Bench::field(b.frames[0],32,2)==0x102,"42-byte PROBE accepted after malformed input and echoed");
      } else check(b.d->state_o==1&&b.d->conflicts_o==1,"42-byte conflicting event accepted after malformed input");
    }
  }
  // Echo and overlap are independent expressions, including wide requested counts.
  for(unsigned start:{0u,0xffu,0x100u,0x107u})for(unsigned count:{1u,8u,255u,256u,65535u}) {
    if(start+count<=0x100)continue;
    Bench b;b.reset();b.begin(true);b.inject(1,42,-1,start,count);b.cycles(30);
    unsigned overlap=std::min(start+count,0x108u)-std::max(start,0x100u);
    check(b.frames.size()==1,"overlap produces exactly one response");
    if(b.frames.empty())continue;
    check(Bench::field(b.frames[0],26,6)==(0x91e0f0000000ULL|start)&&Bench::field(b.frames[0],32,2)==count,"DEFEND echoes complete requested range");
    check(Bench::field(b.frames[0],38,2)==std::max(start,0x100u)&&Bench::field(b.frames[0],40,2)==overlap,"DEFEND computes half-open intersection");
  }
  std::printf("independent boundary probes: %d checks, %d failures\n",checks,failures);
  return failures?1:0;
}
