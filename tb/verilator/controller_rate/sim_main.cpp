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

    // frame factory: tagged(PCP1)/untagged, arbitrary byte length (min 60 = ACK-like)
    auto mkframe = [](bool tagged, int len){
        std::vector<uint8_t> f(len);
        for (int i=0;i<len;i++) f[i]=(uint8_t)(i>>3);
        for (int i=0;i<6;i++){ f[i]=0x68; f[6+i]=0x02; }
        if (tagged){ f[12]=0x81; f[13]=0x00; f[14]=0x20; f[15]=0x02; f[16]=0x08; f[17]=0x00; }
        else       { f[12]=0x08; f[13]=0x00; }
        return f;
    };
    // interference-like mix: ACK-sized + MTU frames, alternating queues
    std::vector<std::pair<std::vector<uint8_t>,int>> mix;   // (frame, expected_len)
    const int sizes[] = {60, 1514, 60, 60, 1514, 90, 60, 1514, 66, 1514};
    for (int i = 0; i < 10; i++) {
        auto f = mkframe((i & 1) != 0, sizes[i]);
        mix.push_back({f, sizes[i]});
    }

    long last_prog = 0;
    uint64_t egress_frames=0, cur=0, integrity_fails=0, total_out_bytes=0;
    std::vector<uint8_t> obuf;
    int beat=0; size_t mi=0;
    std::vector<uint8_t>* fp=&mix[0].first;
    int flen = (int)mix[0].second;
    int nbeats = (flen+7)/8;
    // expected egress: per-queue FIFO of frame lengths, in input order.
    // PCP1(tagged)->q1, untagged->q0 (identity regen + reset PCP_TC + TC_QUEUE=0xE1).
    std::vector<int> expq0, expq1;
    auto push_exp = [&](size_t idx){
        bool tag = (idx & 1) != 0;             // mix[] alternates untagged/tagged
        if (tag) expq1.push_back((int)mix[idx].second);
        else     expq0.push_back((int)mix[idx].second);
    };
    push_exp(0);
    size_t xq0=0, xq1=0;
    for (long c=0;c<8000000;c++) {
        uint64_t d=0; int vb=0;
        for (int b=0;b<8;b++){ int idx=beat*8+b; if(idx<flen){ d|=(uint64_t)(*fp)[idx]<<(8*b); vb++; } }
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
        int  odest  = (int)dut->m_tdest;
        uint64_t odata = dut->m_tdata;
        unsigned okraw = (unsigned)dut->m_tkeep;
        dut->clk=1; dut->eval();
        if (in_hs) {
            if (dut->s_tlast){
                beat=0; mi=(mi+1)%mix.size();
                fp=&mix[mi].first; flen=(int)mix[mi].second; nbeats=(flen+7)/8;
                push_exp(mi);
            } else beat++;
        }
        if (out_hs) {
            for (int b=0; b<8; b++)
                if (okraw & (1<<b)) obuf.push_back((uint8_t)((odata >> (8*b)) & 0xFF));
            cur += okeep;
            if (olast){
                // content check: valid length + payload bytes k>=18 equal (k>>3)
                bool ok = false;
                for (int sz : {60,66,90,1514}) if ((int)obuf.size()==sz) ok=true;
                int badk=-1;
                for (size_t k=18; ok && k<obuf.size(); k++)
                    if (obuf[k] != (uint8_t)(k>>3)) { ok=false; badk=(int)k; }
                if (!ok) { integrity_fails++;
                    if (integrity_fails<=8)
                        printf("[bad] frame %llu len=%zu badk=%d got=%d exp=%d\n",
                               (unsigned long long)egress_frames, obuf.size(), badk,
                               badk>=0?obuf[badk]:-1, badk>=0?(badk>>3):-1);
                }
                egress_frames++; total_out_bytes += obuf.size();
                obuf.clear(); cur=0;
            }
        }
        // deadlock detector with sideband state dump
        if (out_hs || in_hs) last_prog = c;
        if (c - last_prog > 400000) {
            printf("[controller_rate] DEADLOCK at cycle %ld: egress=%llu frames\n"
                   "  cls: tq_wr=%u tq_rd=%u pushed=%u fifo_v=%u tqe=%u\n"
                   "  shp: grant=%x hasdata=%x allow=%x hold=%u active=%u\n"
                   "  q:   dep0=%u dep1=%u q2s_v=%u q2s_r=%u\n",
                   c, (unsigned long long)egress_frames,
                   (unsigned)dut->p_tq_wr, (unsigned)dut->p_tq_rd,
                   (unsigned)dut->p_tq_pushed, (unsigned)dut->p_fifo_v,
                   (unsigned)dut->p_tq_empty,
                   (unsigned)dut->p_grant, (unsigned)dut->p_hasdata,
                   (unsigned)dut->p_allow, (unsigned)dut->p_hold,
                   (unsigned)dut->p_active,
                   (unsigned)dut->p_dep0, (unsigned)dut->p_dep1,
                   (unsigned)dut->p_q2s_v2, (unsigned)dut->p_q2s_r2);
            return 2;
        }
    }
    printf("[controller_rate] egress=%llu frames, %llu bytes, integrity_fails=%llu\n",
           (unsigned long long)egress_frames, (unsigned long long)total_out_bytes,
           (unsigned long long)integrity_fails);
    if (integrity_fails)
        printf("[controller_rate] REPRODUCED the OPEN classifier tdest bug "
               "(docs/CBS_DATAPATH_BUG.md) — %llu frames egressed short.\n",
               (unsigned long long)integrity_fails);
    else
        printf("[controller_rate] no integrity failures — bug appears FIXED; "
               "flip this harness to gating (return integrity_fails?1:0).\n");
    return integrity_fails ? 1 : 0;   // gating since the 2026-07-05 classifier fix
}
