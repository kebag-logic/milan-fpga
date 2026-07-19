// tx_ifg_gasket: two back-to-back frames in -> both emerge with >= GAP idle
// cycles between them; no beats lost; passthrough byte-exact.
#include "Vtx_ifg_gasket.h"
#include "verilated.h"
#include <cstdio>
#include <vector>
static Vtx_ifg_gasket* dut;
static long checks=0, fails=0;
static void ck(const char* w,long g,long e){checks++; if(g!=e){fails++;printf("  [FAIL] %s got=%ld exp=%ld\n",w,g,e);} else printf("  [ ok ] %s=%ld\n",w,g);}
static void step(){dut->clk_i=0;dut->eval();dut->clk_i=1;dut->eval();}
int main(int c,char**v){
    Verilated::commandArgs(c,v); dut=new Vtx_ifg_gasket;
    dut->rst_n=0; dut->s_tvalid=0; dut->m_tready=1; step(); step(); dut->rst_n=1; step();
    // feed 2 frames of 3 beats each, back-to-back (no idle between)
    std::vector<std::pair<uint64_t,int>> in; // (data,last)
    for(int f=0;f<2;f++) for(int b=0;b<3;b++) in.push_back({(uint64_t)(f*10+b), b==2});
    size_t i=0; int outbeats=0, frames=0, gap_min=999999, since_last=0; bool seen_last=false;
    std::vector<uint64_t> got;
    for(int cyc=0; cyc<800 && (i<in.size()||outbeats<6); cyc++){
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
    ck("all 6 beats emerged", outbeats, 6);
    ck("2 frames", frames, 2);
    // byte-exact
    bool eq=got.size()==6; for(size_t k=0;k<got.size()&&eq;k++) eq=(got[k]==(k/3)*10+(k%3));
    ck("byte-exact passthrough", eq?1:0, 1);
    ck("gap >= 500 cycles between frames", gap_min>=500?1:0, 1);
    printf("gap measured=%d\n", gap_min);
    printf("ifg: %ld checks, %ld failures\n", checks, fails);
    return fails?1:0;
}
