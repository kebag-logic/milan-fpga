// tx_ifg_gasket: two back-to-back frames in -> both emerge with >= GAP idle
// cycles between them; no beats lost; passthrough byte-exact.
#include "Vtx_ifg_gasket.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <vector>
// The stimulus: two frames of three beats each, fed back-to-back.
constexpr int kFrames = 2;
constexpr int kBeatsPerFrame = 3;
constexpr int kTotalBeats = kFrames * kBeatsPerFrame;
// The gasket must hold the second frame off by at least this many idle cycles.
constexpr int kMinGapCycles = 500;
// Cycle budget for the whole run.
constexpr int kMaxCycles = 800;
// Larger than any gap the budget above can measure, so the first gap seen wins.
constexpr int kGapUnmeasured = 999999;

namespace {
// The model handle and the tally were file-scope statics; they are the state
// of one run of this harness, so they belong to the object that performs it.
class IfgGasketHarness {
 public:
    int run();

 private:
    void ck(const char* w,long g,long e){checks++; if(g!=e){fails++;printf("  [FAIL] %s got=%ld exp=%ld\n",w,g,e);} else printf("  [ ok ] %s=%ld\n",w,g);}
    void step(){dut->clk_i=0;dut->eval();dut->clk_i=1;dut->eval();}

    Vtx_ifg_gasket* dut = nullptr;
    long checks=0;
    long fails=0;
};

int IfgGasketHarness::run(){
    const milan::tb::Model<Vtx_ifg_gasket> model;
    dut = model.get();
    dut->rst_n=0; dut->s_tvalid=0; dut->m_tready=1; step(); step(); dut->rst_n=1; step();
    // feed 2 frames of 3 beats each, back-to-back (no idle between)
    std::vector<std::pair<uint64_t,int>> in; // (data,last)
    for(int f=0;f<kFrames;f++) for(int b=0;b<kBeatsPerFrame;b++) in.push_back({static_cast<uint64_t>(f*10+b), b==kBeatsPerFrame-1});
    size_t i=0;
    int outbeats=0;
    int frames=0;
    int gap_min=kGapUnmeasured;
    int since_last=0;
    bool seen_last=false;
    std::vector<uint64_t> got;
    for(int cyc=0; cyc<kMaxCycles && (i<in.size()||outbeats<kTotalBeats); cyc++){
        dut->m_tready=1;
        if(i<in.size()){ dut->s_tdata=in[i].first; dut->s_tkeep=0xFF; dut->s_tvalid=1; dut->s_tlast=in[i].second; }
        else dut->s_tvalid=0;
        dut->clk_i=0; dut->eval();
        bool s_acc = dut->s_tvalid && dut->s_tready;
        bool m_acc = dut->m_tvalid && dut->m_tready;
        if(m_acc){ got.push_back(dut->m_tdata); outbeats++; if(seen_last) { if(since_last<gap_min) gap_min=since_last; } if(dut->m_tlast){frames++; seen_last=true; since_last=0;} }
        else if(seen_last && frames==1) since_last++;
        dut->clk_i=1; dut->eval();
        if(s_acc) i++;
    }
    ck("all 6 beats emerged", outbeats, kTotalBeats);
    ck("2 frames", frames, kFrames);
    // byte-exact
    bool eq=got.size()==kTotalBeats;
    for(size_t k=0;k<got.size()&&eq;k++) eq=(got[k]==(k/kBeatsPerFrame)*10+(k%kBeatsPerFrame));
    ck("byte-exact passthrough", eq?1:0, 1);
    ck("gap >= 500 cycles between frames", gap_min>=kMinGapCycles?1:0, 1);
    printf("gap measured=%d\n", gap_min);
    printf("ifg: %ld checks, %ld failures\n", checks, fails);
    return fails?1:0;
}
}  // namespace

int main(int c,char**v){
    Verilated::commandArgs(c,v);
    IfgGasketHarness harness;
    return harness.run();
}
