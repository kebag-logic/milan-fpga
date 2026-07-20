// KL_pcm_lpf v2 (serial MAC): 2nd-order Butterworth LPF (fc 20 kHz @ 48 kHz).
// Feeds 6-beat back-to-back bursts (the real AAF PDU pattern) and collects
// outputs from m_tvalid. Checks: exact-unity DC, 1 kHz ~unity, 22 kHz
// attenuation per the quantized response, burst 1:1 accounting, inactive
// mode emits nothing, L/R independence.
#include "VKL_pcm_lpf.h"
#include "verilated.h"
#include <cstdio>
#include <cmath>
#include <vector>
static VKL_pcm_lpf* dut;
static long checks=0, fails=0;
static std::vector<int32_t> outl, outr;
static void ck(const char* w,int ok){checks++; if(!ok){fails++;printf("  [FAIL] %s\n",w);} else printf("  [ ok ] %s\n",w);}
static void step(){
    dut->clk_i=0;dut->eval();
    dut->clk_i=1;dut->eval();
    if(dut->m_tvalid){
        uint64_t d=dut->m_tdata;
        uint32_t L=((d>>0)&0xFF)<<24 | ((d>>8)&0xFF)<<16 | ((d>>16)&0xFF)<<8;
        uint32_t R=((d>>32)&0xFF)<<24 | ((d>>40)&0xFF)<<16 | ((d>>48)&0xFF)<<8;
        outl.push_back(((int32_t)L)>>8); outr.push_back(((int32_t)R)>>8);
    }
}
static uint64_t pack(int32_t l,int32_t r){
    uint32_t L=((uint32_t)l)<<8, R=((uint32_t)r)<<8; uint64_t b=0;
    b|=(uint64_t)((L>>24)&0xFF)<<0;  b|=(uint64_t)((L>>16)&0xFF)<<8;
    b|=(uint64_t)((L>>8)&0xFF)<<16;
    b|=(uint64_t)((R>>24)&0xFF)<<32; b|=(uint64_t)((R>>16)&0xFF)<<40;
    b|=(uint64_t)((R>>8)&0xFF)<<48;
    return b;
}
// send a 6-frame burst back-to-back, then idle (like one AAF PDU)
static void burst(const int32_t* l,const int32_t* r){
    for(int i=0;i<6;i++){
        dut->s_tdata=pack(l[i],r[i]); dut->s_tvalid=1; dut->s_tready=1;
        step();
    }
    dut->s_tvalid=0;
    for(int i=0;i<100;i++) step();   // drain (6 pairs x 12 cycles << 100)
}
int main(int c,char**v){
    Verilated::commandArgs(c,v); dut=new VKL_pcm_lpf;
    dut->rst_n=0; dut->enable_i=1; dut->chans_i=2; dut->s_tvalid=0; dut->s_tready=1;
    step(); step(); dut->rst_n=1; step();
    // DC convergence -> exact unity
    int32_t dcl[6],dcr[6]; for(int i=0;i<6;i++){dcl[i]=1000000;dcr[i]=-1000000;}
    for(int k=0;k<80;k++) burst(dcl,dcr);
    ck("burst accounting 1:1", (long)outl.size()==480);
    ck("DC gain exactly 1.0 (L)", !outl.empty() && outl.back()==1000000);
    ck("DC gain exactly 1.0 (R, negative)", !outr.empty() && outr.back()==-1000000);
    // 1 kHz ~unity
    outl.clear(); outr.clear();
    double amp=4e6; int n=0;
    for(int k=0;k<80;k++){int32_t l[6],r[6];
        for(int i=0;i<6;i++){l[i]=(int32_t)(amp*sin(2*M_PI*1000.0*n/48000.0));r[i]=0;n++;}
        burst(l,r);}
    double mx=0; for(size_t i=200;i<outl.size();i++) if(fabs((double)outl[i])>mx) mx=fabs((double)outl[i]);
    ck("1 kHz passband ~unity (0.99..1.01)", mx>0.99*amp && mx<1.01*amp);
    // 22 kHz attenuated (quantized |H| = 0.234)
    outl.clear(); outr.clear(); n=0;
    for(int k=0;k<80;k++){int32_t l[6],r[6];
        for(int i=0;i<6;i++){l[i]=(int32_t)(amp*sin(2*M_PI*22000.0*n/48000.0));r[i]=0;n++;}
        burst(l,r);}
    mx=0; for(size_t i=200;i<outl.size();i++) if(fabs((double)outl[i])>mx) mx=fabs((double)outl[i]);
    ck("22 kHz attenuated (0.15..0.35)", mx<0.35*amp && mx>0.15*amp);
    // R stayed silent through the L sweeps
    double mr=0; for(int32_t s:outr) if(fabs((double)s)>mr) mr=fabs((double)s);
    ck("R silent while L active", mr<64);
    // inactive (8ch) -> no outputs, primes only
    outl.clear(); outr.clear();
    dut->chans_i=8; step();
    int32_t z[6]={9,9,9,9,9,9}; burst(z,z);
    ck("inactive mode emits nothing", outl.empty());
    dut->chans_i=2; step();
    printf("pcmlpf: %ld checks, %ld failures\n",checks,fails);
    return fails?1:0;
}
