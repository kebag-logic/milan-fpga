// KL_pcm_lpf v2 (serial MAC): 2nd-order Butterworth LPF (fc 20 kHz @ 48 kHz).
// Feeds 6-beat back-to-back bursts (the real AAF PDU pattern) and collects
// outputs from m_tvalid. Checks: exact-unity DC, 1 kHz ~unity, 22 kHz
// attenuation per the quantized response, burst 1:1 accounting, inactive
// mode emits nothing, L/R independence.
#include "../../common/verilator_harness.hpp"
#include "VKL_pcm_lpf.h"
#include "verilated.h"
#include <array>
#include <cstdio>
#include <cmath>
#include <vector>
// One AAF PDU's worth of frames, sent back-to-back.
constexpr int kBurstFrames = 6;
// Idle cycles after a burst: 6 pairs x 12 cycles << 100.
constexpr int kDrainCycles = 100;
constexpr double kSampleRateHz = 48000.0;
// Outputs skipped before a sweep's peak is measured: the filter's startup transient.
constexpr size_t kSettleSamples = 200;

namespace {

//! One burst's worth of samples for one channel.
using Burst = std::array<int32_t, kBurstFrames>;

//! Drives the filter and owns everything the drive and the checks share.
class PcmLpfHarness {
 public:
    int run();

 private:
    void ck(const char* w,int ok);
    void step();
    static uint64_t pack(int32_t l,int32_t r);
    void burst(const Burst& l,const Burst& r);

    VKL_pcm_lpf* dut = nullptr;
    long checks = 0;
    long fails = 0;
    std::vector<int32_t> outl;
    std::vector<int32_t> outr;
};

void PcmLpfHarness::ck(const char* w,int ok){checks++; if(!ok){fails++;printf("  [FAIL] %s\n",w);} else printf("  [ ok ] %s\n",w);}

void PcmLpfHarness::step(){
    dut->clk_i=0;dut->eval();
    dut->clk_i=1;dut->eval();
    if(dut->m_tvalid){
        uint64_t d=dut->m_tdata;
        uint32_t L=((d>>0)&0xFF)<<24 | ((d>>8)&0xFF)<<16 | ((d>>16)&0xFF)<<8;
        uint32_t R=((d>>32)&0xFF)<<24 | ((d>>40)&0xFF)<<16 | ((d>>48)&0xFF)<<8;
        outl.push_back(static_cast<int32_t>(L)>>8);
        outr.push_back(static_cast<int32_t>(R)>>8);
    }
}

uint64_t PcmLpfHarness::pack(int32_t l,int32_t r){
    uint32_t L=static_cast<uint32_t>(l)<<8;
    uint32_t R=static_cast<uint32_t>(r)<<8;
    uint64_t b=0;
    b|=static_cast<uint64_t>((L>>24)&0xFF)<<0;  b|=static_cast<uint64_t>((L>>16)&0xFF)<<8;
    b|=static_cast<uint64_t>((L>>8)&0xFF)<<16;
    b|=static_cast<uint64_t>((R>>24)&0xFF)<<32; b|=static_cast<uint64_t>((R>>16)&0xFF)<<40;
    b|=static_cast<uint64_t>((R>>8)&0xFF)<<48;
    return b;
}

// send a 6-frame burst back-to-back, then idle (like one AAF PDU)
void PcmLpfHarness::burst(const Burst& l,const Burst& r){
    for(int i=0;i<kBurstFrames;i++){
        dut->s_tdata=pack(l[i],r[i]); dut->s_tvalid=1; dut->s_tready=1;
        step();
    }
    dut->s_tvalid=0;
    for(int i=0;i<kDrainCycles;i++) step();   // drain (6 pairs x 12 cycles << 100)
}

int PcmLpfHarness::run(){
    const milan::tb::Model<VKL_pcm_lpf> model;
    dut = model.get();
    dut->rst_n=0; dut->enable_i=1; dut->chans_i=2; dut->s_tvalid=0; dut->s_tready=1;
    step(); step(); dut->rst_n=1; step();
    // DC convergence -> exact unity
    Burst dcl;
    Burst dcr;
    for(int i=0;i<kBurstFrames;i++){dcl[i]=1000000;dcr[i]=-1000000;}
    for(int k=0;k<80;k++) burst(dcl,dcr);
    ck("burst accounting 1:1", static_cast<long>(outl.size())==480);
    ck("DC gain exactly 1.0 (L)", !outl.empty() && outl.back()==1000000);
    ck("DC gain exactly 1.0 (R, negative)", !outr.empty() && outr.back()==-1000000);
    // 1 kHz ~unity
    outl.clear(); outr.clear();
    double amp=4e6;
    int n=0;
    for(int k=0;k<80;k++){
        Burst l;
        Burst r;
        for(int i=0;i<kBurstFrames;i++){l[i]=static_cast<int32_t>(amp*sin(2*M_PI*1000.0*n/kSampleRateHz));r[i]=0;n++;}
        burst(l,r);}
    double mx=0;
    for(size_t i=kSettleSamples;i<outl.size();i++) if(fabs(static_cast<double>(outl[i]))>mx) mx=fabs(static_cast<double>(outl[i]));
    ck("1 kHz passband ~unity (0.99..1.01)", mx>0.99*amp && mx<1.01*amp);
    // 22 kHz attenuated (quantized |H| = 0.234)
    outl.clear(); outr.clear(); n=0;
    for(int k=0;k<80;k++){
        Burst l;
        Burst r;
        for(int i=0;i<kBurstFrames;i++){l[i]=static_cast<int32_t>(amp*sin(2*M_PI*22000.0*n/kSampleRateHz));r[i]=0;n++;}
        burst(l,r);}
    mx=0;
    for(size_t i=kSettleSamples;i<outl.size();i++) if(fabs(static_cast<double>(outl[i]))>mx) mx=fabs(static_cast<double>(outl[i]));
    ck("22 kHz attenuated (0.15..0.35)", mx<0.35*amp && mx>0.15*amp);
    // R stayed silent through the L sweeps
    double mr=0;
    for(int32_t s:outr) if(fabs(static_cast<double>(s))>mr) mr=fabs(static_cast<double>(s));
    ck("R silent while L active", mr<64);
    // inactive (8ch) -> no outputs, primes only
    outl.clear(); outr.clear();
    dut->chans_i=8; step();
    const Burst z = {9,9,9,9,9,9};
    burst(z,z);
    ck("inactive mode emits nothing", outl.empty());
    dut->chans_i=2; step();
    // [LK] burst-FIFO count-leak regression (silicon wedge class,
    // 2026-07-21): sustained back-to-back beats force full+pop and
    // bypass+pop coincidences; the old per-branch bookkeeping leaked
    // phantom entries until the engine read permanently-full and
    // m_tvalid stopped forever. Accounting must stay exact: every
    // accepted pair eventually emits, and the engine keeps running.
    outl.clear(); outr.clear();
    for(int k=0;k<4;k++){
        for(int i=0;i<24;i++){                 // 24 back-to-back beats
            dut->s_tdata=pack(500000+i,-500000-i);
            dut->s_tvalid=1; dut->s_tready=1; step();
        }
        dut->s_tvalid=0;
        // mid-stream active toggle: pop-during-bypass coincidences
        dut->chans_i=8; for(int i=0;i<7;i++) step();
        dut->chans_i=2; for(int i=0;i<400;i++) step();
    }
    ck("[LK] engine alive after burst storms", !outl.empty());
    outl.clear();
    const Burst probe = {111111,222222,333333,444444,555555,666666};
    burst(probe,probe);
    ck("[LK] steady 1:1 accounting after storms", static_cast<long>(outl.size())==kBurstFrames);

    printf("pcmlpf: %ld checks, %ld failures\n",checks,fails);
    return fails?1:0;
}

}  // namespace

int main(int c,char**v){
    Verilated::commandArgs(c,v);
    PcmLpfHarness harness;
    return harness.run();
}
