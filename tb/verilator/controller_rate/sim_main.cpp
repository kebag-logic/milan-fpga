// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Reproduces the OPEN CBS datapath bug (docs/CBS_DATAPATH_BUG.md): back-to-back
// frames that classify to different queues lose ~1 beat each to the wrong queue.
// Drives an alternating tagged(PCP1)/untagged frame pair through the controller
// and checks per-frame byte integrity at egress. PRINTS the diagnosis and
// EXITS 0 — a documented reproduction, not a gating test, until the classifier
// tdest handoff is reworked.
#include "Vcontroller_rate_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <vector>
#include <random>

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    auto* dut = new Vcontroller_rate_wrap;
    std::mt19937 rng(12345);

    dut->is_1g_i = 1; dut->cls_use_pcp_i = 1; dut->cls_default_pcp_i = 0;
    dut->cls_pcp_tc_map_i = 0xFAC688; dut->cls_prio_regen_i = 0xFAC688;
    dut->cls_tc_queue_map_i = 0xE1;                  // TC0->q1, TC1->q0
    for (int q = 0; q < 4; q++) {
        dut->cbs_idle_slope_i[q] = (q == 0) ? 10000000u : 0u;
        dut->cbs_hi_credit_i[q] = 200; dut->cbs_lo_credit_i[q] = (uint32_t)-1522;
    }
    dut->cbs_shaped_i = 0x1; dut->m_tready = 1;

    dut->resetn = 0; for (int i=0;i<16;i++){dut->clk=0;dut->eval();dut->clk=1;dut->eval();}
    dut->resetn = 1;

    std::vector<uint8_t> ft(1514), fu(1514);
    for (int i=0;i<1514;i++){ ft[i]=fu[i]=(uint8_t)(i>>3); }
    for (int i=0;i<6;i++){ ft[i]=fu[i]=0x68; ft[6+i]=fu[6+i]=0x02; }
    ft[12]=0x81; ft[13]=0x00; ft[14]=0x20; ft[15]=0x02; ft[16]=0x08; ft[17]=0x00; // PCP1
    fu[12]=0x08; fu[13]=0x00;                                                     // untagged
    const int nbeats = (1514+7)/8;

    uint64_t egress_frames=0, cur=0, integrity_fails=0;
    int beat=0; bool tagged=true; std::vector<uint8_t>* fp=&ft;
    for (long c=0;c<6000000;c++) {
        uint64_t d=0; int vb=0;
        for (int b=0;b<8;b++){ int idx=beat*8+b; if(idx<1514){ d|=(uint64_t)(*fp)[idx]<<(8*b); vb++; } }
        dut->s_tdata=d; dut->s_tkeep=(vb==8)?0xFF:((1u<<vb)-1);
        dut->s_tvalid=1; dut->s_tlast=(beat==nbeats-1);
        dut->m_tready=((rng()&7)<2);                 // ~25% duty: 1G wire pacing
        // sample handshakes PRE-EDGE (settled comb state = what the posedge commits);
        // post-edge sampling mis-advances the feeder and fabricates beat loss
        dut->clk=0; dut->eval();
        bool in_hs  = dut->s_tvalid && dut->s_tready;
        bool out_hs = dut->m_tvalid && dut->m_tready;
        int  okeep  = __builtin_popcount(dut->m_tkeep);
        bool olast  = dut->m_tlast;
        dut->clk=1; dut->eval();
        if (in_hs) {
            if (dut->s_tlast){ beat=0; tagged=!tagged; fp=tagged?&ft:&fu; } else beat++;
        }
        if (out_hs) {
            cur += okeep;
            if (olast){ egress_frames++; if(cur!=1514) integrity_fails++; cur=0; }
        }
    }
    printf("[controller_rate] egress=%llu frames, integrity_fails=%llu\n",
           (unsigned long long)egress_frames, (unsigned long long)integrity_fails);
    if (integrity_fails)
        printf("[controller_rate] REPRODUCED the OPEN classifier tdest bug "
               "(docs/CBS_DATAPATH_BUG.md) — %llu frames egressed short.\n",
               (unsigned long long)integrity_fails);
    else
        printf("[controller_rate] no integrity failures — bug appears FIXED; "
               "flip this harness to gating (return integrity_fails?1:0).\n");
    return integrity_fails ? 1 : 0;   // gating since the 2026-07-05 classifier fix
}
