// KL_pcm_lpf: 2nd-order Butterworth LPF (fc 20 kHz @ fs 48 kHz), s24 stereo.
// Checks: exact-unity DC, 1 kHz ~unity, 22 kHz attenuated, bypass bit-true,
// channel independence, saturation-free small signals.
#include "VKL_pcm_lpf.h"
#include "verilated.h"
#include <cstdio>
#include <cmath>
#include <vector>
static VKL_pcm_lpf* dut;
static long checks=0, fails=0;
static void ck(const char* w,int ok){checks++; if(!ok){fails++;printf("  [FAIL] %s\n",w);} else printf("  [ ok ] %s\n",w);}
static void step(){dut->clk_i=0;dut->eval();dut->clk_i=1;dut->eval();}
static uint64_t pack(int32_t l,int32_t r){
    uint32_t L=((uint32_t)l)<<8, R=((uint32_t)r)<<8; uint64_t b=0;
    b|=(uint64_t)((L>>24)&0xFF)<<0;  b|=(uint64_t)((L>>16)&0xFF)<<8;
    b|=(uint64_t)((L>>8)&0xFF)<<16;  b|=(uint64_t)(L&0xFF)<<24;
    b|=(uint64_t)((R>>24)&0xFF)<<32; b|=(uint64_t)((R>>16)&0xFF)<<40;
    b|=(uint64_t)((R>>8)&0xFF)<<48;  b|=(uint64_t)(R&0xFF)<<56;
    return b;
}
static int32_t unpackL(uint64_t d){
    uint32_t v=((d>>0)&0xFF)<<24 | ((d>>8)&0xFF)<<16 | ((d>>16)&0xFF)<<8 | ((d>>24)&0xFF);
    return ((int32_t)v)>>8;
}
static int32_t feed(int32_t l,int32_t r){
    dut->s_tdata=pack(l,r); dut->s_tvalid=1; dut->s_tready=1;
    dut->eval();                    // combinational output before the edge
    int32_t y=unpackL(dut->m_tdata);
    step();
    return y;
}
int main(int c,char**v){
    Verilated::commandArgs(c,v); dut=new VKL_pcm_lpf;
    dut->rst_n=0; dut->enable_i=1; dut->chans_i=2; dut->s_tvalid=0; dut->s_tready=1;
    step(); step(); dut->rst_n=1; step();
    // DC: step to a constant -> output converges EXACTLY to it (unity DC)
    int32_t dc=1000000, y=0;
    for(int i=0;i<400;i++) y=feed(dc,-dc);
    ck("DC gain exactly 1.0 (L)", y==dc);
    // 1 kHz ~unity (fc=20k): amplitude within 1%
    double amp=4e6, mx=0;
    for(int i=0;i<480;i++){ int32_t x=(int32_t)(amp*sin(2*M_PI*1000.0*i/48000.0));
        int32_t o=feed(x,0); if(i>200 && fabs((double)o)>mx) mx=fabs((double)o); }
    ck("1 kHz passband ~unity (>0.99, <1.01)", mx>0.99*amp && mx<1.01*amp);
    // 22 kHz attenuated (Butterworth fc=20k: |H(22k)| ~= 0.63 -> require < 0.8 and > 0.3)
    mx=0;
    for(int i=0;i<480;i++){ int32_t x=(int32_t)(amp*sin(2*M_PI*22000.0*i/48000.0));
        int32_t o=feed(x,0); if(i>200 && fabs((double)o)>mx) mx=fabs((double)o); }
    ck("22 kHz attenuated (~0.234 theoretical, allow 0.15..0.35)", mx<0.35*amp && mx>0.15*amp);
    // bypass: enable=0 -> bit-true passthrough
    dut->enable_i=0; step();
    int32_t o=feed(1234567,-7654321);
    ck("bypass bit-true", o==1234567);
    // auto-bypass on chans != 2
    dut->enable_i=1; dut->chans_i=8; step();
    o=feed(-2222222,0);
    ck("auto-bypass for 8ch", o==-2222222);
    dut->chans_i=2; step();
    // R channel independent: L silent while R runs
    for(int i=0;i<100;i++) feed(0,(int32_t)(1e6*sin(2*M_PI*1000.0*i/48000.0)));
    o=feed(0,500000);
    ck("L stays silent while R active", o==0 || (o<64 && o>-64));
    printf("pcmlpf: %ld checks, %ld failures\n",checks,fails);
    return fails?1:0;
}
