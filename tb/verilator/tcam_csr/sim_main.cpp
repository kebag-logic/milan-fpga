#include "Vtcam_csr_wrap.h"
#include "verilated.h"
#include <cstdio>
static Vtcam_csr_wrap* dut;
static void step(){ dut->clk_i=0; dut->eval(); dut->clk_i=1; dut->eval(); }
static void wr(uint32_t a, uint32_t d){ dut->wr_addr_i=a; dut->wr_data_i=d; dut->wr_p_i=1; step(); dut->wr_p_i=0; step(); }
int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vtcam_csr_wrap;
    dut->rst_n=0; dut->s_tvalid=0; dut->m_tready=1; step(); step();
    dut->rst_n=1; step();
    wr(0x708,0x000091E0); wr(0x704,0xF0000000);
    wr(0x710,0x0000FFFF); wr(0x70C,0xFF000000);
    wr(0x714,1); wr(0x718,0x00010100);
    // frame 1: dmac 91:E0:F0:00:77:77 (little lane) -> expect DROP
    // frame 2: dmac 00:11:22:33:44:55 -> expect PASS
    uint64_t d1=0; uint8_t m1[8]={0x91,0xE0,0xF0,0x00,0x77,0x77,0x08,0x00};
    uint64_t d2=0; uint8_t m2[8]={0x00,0x11,0x22,0x33,0x44,0x55,0x08,0x00};
    for(int i=0;i<8;i++){ d1|=(uint64_t)m1[i]<<(8*i); d2|=(uint64_t)m2[i]<<(8*i); }
    int out1=0,out2=0;
    for(int f=0; f<2; f++){
        uint64_t d = f? d2 : d1;
        for(int b=0;b<4;b++){
            dut->s_tdata = b? 0 : d; dut->s_tkeep=0xFF;
            dut->s_tvalid=1; dut->s_tlast=(b==3);
            // sample the cut-through outputs BEFORE the clock edge: the
            // filter is combinational per beat, and sampling after the edge
            // shows the NEXT-cycle view - on the tlast beat that view is the
            // runt-SOF guard (rx_mac_filter 2026-07-19) rejecting a phantom
            // 1-beat frame, not this beat's verdict
            dut->eval();
            printf("    f%d b%d: s_tvalid=%d s_tready=%d m_tvalid=%d dropped=%d\n",
                   f,b,dut->s_tvalid,dut->s_tready,dut->m_tvalid,dut->dropped_o);
            if(dut->m_tvalid && dut->m_tready){ if(f) out2++; else out1++; }
            step();
        }
        dut->s_tvalid=0; dut->s_tlast=0; step(); step();
    }
    printf("filtered-frame beats out=%d (exp 0), other=%d (exp 4)\n",out1,out2);
    return (out1==0 && out2==4)?0:1;
}
