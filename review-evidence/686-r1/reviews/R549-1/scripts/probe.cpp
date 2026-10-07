#include "VKL_maap.h"
#include "verilated.h"
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <set>
#include <vector>

struct Frame { std::vector<unsigned char> bytes; long start = 0; };
struct Harness {
  VKL_maap d;
  long now = 0;
  Frame current;
  std::vector<Frame> frames;
  explicit Harness(uint64_t mac = 0x020000000001ULL, unsigned seed = 0x4000) {
    d.clk_i=0; d.rst_n=0; d.station_mac_i=mac; d.count_i=8;
    d.seed_valid_i=1; d.seed_offset_i=seed; d.enable_i=0;
    d.rx_tvalid_i=0; d.rx_tready_i=1; d.rx_tlast_i=0;
    d.rx_tkeep_i=0xff; d.rx_tdata_i=0; d.m_axis_tready=1;
    step(6); d.rst_n=1; step(3);
  }
  void step(unsigned n=1) {
    while(n--) {
      d.clk_i=0; d.eval();
      if(d.m_axis_tvalid && d.m_axis_tready) {
        if(current.bytes.empty()) current.start=now;
        for(unsigned j=0;j<8;j++) if(d.m_axis_tkeep&(1u<<j))
          current.bytes.push_back(d.m_axis_tdata>>(8*j));
        if(d.m_axis_tlast) {frames.push_back(current); current=Frame{};}
      }
      d.clk_i=1; d.eval(); now++;
    }
  }
  bool until(unsigned n, unsigned budget=340000) {
    while(frames.size()<n && budget--) step();
    return frames.size()>=n;
  }
  void begin() {d.enable_i=1; step(3);}
  void acquire() {begin(); until(5);}
  void input(unsigned type, uint64_t src, unsigned start, unsigned count,
             unsigned length=60, unsigned final_keep=0x0f) {
    unsigned char f[64]={};
    uint64_t dst=0x91e0f000ff00ULL;
    for(unsigned j=0;j<6;j++) {f[j]=dst>>(40-8*j);f[6+j]=src>>(40-8*j);}
    f[12]=0x22;f[13]=0xf0;f[14]=0xfe;f[15]=type;f[16]=8;f[17]=16;
    unsigned pos=type==2?34:26;
    f[pos]=0x91;f[pos+1]=0xe0;f[pos+2]=0xf0;
    f[pos+4]=start>>8;f[pos+5]=start;f[pos+6]=count>>8;f[pos+7]=count;
    for(unsigned at=0;at<length;at+=8) {
      uint64_t w=0;for(unsigned j=0;j<8;j++) w|=uint64_t(f[at+j])<<(8*j);
      d.rx_tdata_i=w;d.rx_tvalid_i=1;d.rx_tlast_i=at+8>=length;
      d.rx_tkeep_i=d.rx_tlast_i?final_keep:0xff;step();
    }
    d.rx_tvalid_i=0;d.rx_tlast_i=0;step(20);
  }
};

int main(int argc,char**argv) {
  Verilated::commandArgs(argc,argv);
  unsigned pass=0,fail=0;
  auto ck=[&](const char* name,bool ok) {
    std::printf("[%s] %s\n",ok?"PASS":"FAIL",name);ok?++pass:++fail;
  };
  // Independent half-open range oracle, including 17-bit end sums.
  unsigned cases=0,bad=0;
  for(unsigned state=1;state<=2;state++) for(unsigned type=1;type<=3;type++)
    for(unsigned relation=0;relation<3;relation++)
      for(auto range:std::vector<std::pair<unsigned,unsigned>>{
          {0x3ff8,8},{0x3ff9,8},{0x4000,1},{0x4007,1},{0x4008,8},
          {0x4002,0},{0x3000,0xdfff},{0xfffe,0xffff}}) {
        Harness h;if(state==1)h.begin();else h.acquire();
        const uint64_t src=relation==0?0x66778899aa00ULL:
                           relation==1?0x020000000001ULL:0x66778899aabbULL;
        const bool overlap=range.second && range.first<0x4008 &&
                           0x4000<range.first+range.second;
        // The two explicitly deferred compare_MAC cells retain their declared behavior.
        const bool restart=overlap && !(state==2 && (type==1 || (type==3 && relation==2)));
        const bool defend=overlap && state==2 && type==1;
        h.input(type,src,range.first,range.second);
        bool ok=(h.d.conflicts_o==unsigned(restart)) && (h.d.defends_o==unsigned(defend));
        if(!ok)std::printf("matrix mismatch state=%u type=%u relation=%u start=%u count=%u\n",state,type,relation,range.first,range.second);
        cases++;bad+=!ok;
      }
  std::printf("range/state matrix cases=%u mismatches=%u\n",cases,bad);
  ck("shared overlap and rAnnounce row",bad==0);
  for(uint64_t mac:{0x020000000001ULL,0x02000000ace1ULL}) {
    Harness h(mac);h.acquire();h.until(29,8500000);
    std::set<long> draws;bool bounds=h.frames.size()==29;
    for(unsigned i=5;i<h.frames.size();i++) {
      long dt=h.frames[i].start-h.frames[i-1].start;
      // Exclude the initial partial millisecond from the diversity test.
      if(i>5)draws.insert(dt);
      bounds &= dt>300000 && dt<320000;
    }
    std::printf("mac=%012llx announce_samples=%zu distinct_intervals=%zu",(unsigned long long)mac,h.frames.size()-5,draws.size());
    for(long dt:draws)std::printf(" %ld",dt);
    std::puts("");
    ck("announce strict bounds",bounds);
    ck(mac==0x020000000001ULL?"normal MAC randomized announce":"zero-state MAC randomized announce",draws.size()>1);
  }
  {
    Harness h;h.acquire();h.d.m_axis_tready=0;
    h.input(1,0x66778899aabbULL,0x4000,1);
    h.d.m_axis_tready=1;h.step(4);h.d.m_axis_tready=0;h.d.clk_i=0;h.d.eval();
    const auto data=h.d.m_axis_tdata;const auto valid=h.d.m_axis_tvalid;
    h.d.count_i=9;h.step();h.d.clk_i=0;h.d.eval();
    std::printf("stalled requested_count beat before=%016llx after=%016llx valid=%u\n",(unsigned long long)data,(unsigned long long)h.d.m_axis_tdata,valid);
    ck("every per-frame field remains latched under stall",valid && data==h.d.m_axis_tdata);
    h.d.rst_n=0;h.step();ck("reset while stalled clears allocation and TX",!h.d.addr_valid_o && !h.d.m_axis_tvalid && h.d.state_o==0);
  }
  {
    Harness h(0x020000000001ULL,0xfeff);h.acquire();
    std::printf("seeded offset=%04x count=%u valid=%u\n",h.d.offset_o,h.d.count_i,h.d.addr_valid_o);
    ck("documented pool containment includes seed",!h.d.addr_valid_o || h.d.offset_o+h.d.count_i<=0xfe00);
  }
  std::printf("independent probes: pass=%u fail=%u\n",pass,fail);
  return fail?1:0;
}
