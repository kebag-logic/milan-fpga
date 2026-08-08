// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// NxN talker lane harness (docs/NXN_ARCHITECTURE.md):
//   [GB] P4 matrix row "golden-frame check: N=1 emits today's exact wire
//        bytes" - flat aaf_talker_i2s vs KL_aaf_capture_i2s +
//        KL_aaf_packetizer(N=1) on the same I2S stimulus, frames compared
//        BYTE-EXACT (header + seq + ts + payload).
//   [I2T] P4/§2.3: two-talker interleave (N=2, direct pair injection) -
//        per-stream seq chains, per-stream ts capture, per-stream
//        DMAC/uid from TCTX, payload isolation, round-robin epochs.
#include "Vaaf_nx_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vaaf_nx_wrap* dut;
static long checks=0, fails=0;
static void ck(const char* t, long got, long exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-46s got=%ld exp=%ld\n",t,got,exp);}
    else printf("  [ ok ] %-46s = %ld\n",t,got); }

using Frame = std::vector<uint8_t>;
static std::vector<Frame> gfr, dfr, p2fr;   // collected frames per port
static Frame gcur, dcur, p2cur;

static void sample(){
    if(dut->g_tvalid_o && dut->g_tready_i){
        for(int i=0;i<8;i++) if((dut->g_tkeep_o>>i)&1)
            gcur.push_back((dut->g_tdata_o>>(8*i))&0xFF);
        if(dut->g_tlast_o){ gfr.push_back(gcur); gcur.clear(); }
    }
    if(dut->d_tvalid_o && dut->d_tready_i){
        for(int i=0;i<8;i++) if((dut->d_tkeep_o>>i)&1)
            dcur.push_back((dut->d_tdata_o>>(8*i))&0xFF);
        if(dut->d_tlast_o){ dfr.push_back(dcur); dcur.clear(); }
    }
    if(dut->p2_tvalid_o && dut->p2_tready_i){
        for(int i=0;i<8;i++) if((dut->p2_tkeep_o>>i)&1)
            p2cur.push_back((dut->p2_tdata_o>>(8*i))&0xFF);
        if(dut->p2_tlast_o){ p2fr.push_back(p2cur); p2cur.clear(); }
    }
}
// [TSL] live-PHC mode: when nonzero, ptp_ns_i advances by this many ns per
// clk cycle - a free-running PHC ramp instead of the static per-epoch pokes
// the earlier sections use. 0 keeps their byte-exact behaviour untouched.
static uint64_t g_ptp_rate = 0;
static void step(){
    dut->clk=0; dut->clk_audio=0; dut->eval();
    dut->clk=1; dut->clk_audio=1; dut->eval();
    sample();
    if (g_ptp_rate) dut->ptp_ns_i += g_ptp_rate;
}
static void cyc(int n=1){ for(int i=0;i<n;i++) step(); }

static unsigned long be(const Frame& b,int o,int n){
    unsigned long v=0; for(int i=0;i<n;i++) v=(v<<8)|b[o+i]; return v; }

static void p2_tctx_wr(int t,int w,uint32_t v){
    dut->p2_tctx_wr_en_i=1; dut->p2_tctx_wr_addr_i=(uint8_t)((t<<4)|w);
    dut->p2_tctx_wr_data_i=v;
    for(int i=0;i<32;i++){ dut->clk=0; dut->clk_audio=0; dut->eval();
        bool rdy=dut->p2_tctx_wr_rdy_o;
        dut->clk=1; dut->clk_audio=1; dut->eval(); sample();
        if(rdy){ dut->p2_tctx_wr_en_i=0; cyc(); return; } }
    dut->p2_tctx_wr_en_i=0; printf("  [FAIL] tctx_wr timeout\n"); fails++; checks++;
}
static uint32_t p2_tctx_rd(int t,int w){
    dut->p2_tctx_rd_en_i=1; dut->p2_tctx_rd_addr_i=(uint8_t)((t<<4)|w);
    for(int i=0;i<64;i++){ cyc();
        if(dut->p2_tctx_rd_valid_o){ dut->p2_tctx_rd_en_i=0; uint32_t v=dut->p2_tctx_rd_data_o; cyc(); return v; } }
    dut->p2_tctx_rd_en_i=0; printf("  [FAIL] tctx_rd timeout\n"); fails++; checks++;
    return 0xDEADBEEF;
}

// inject one L/R pair into the N=2 packetizer
static void pair(int slot, uint32_t l, uint32_t r, int gap=24){
    dut->p2_pair_slot_i=slot; dut->p2_pair_l_i=l&0xFFFFFF; dut->p2_pair_r_i=r&0xFFFFFF;
    dut->p2_pair_valid_i=1; cyc(); dut->p2_pair_valid_i=0; cyc(gap);
}

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vaaf_nx_wrap;

    dut->rst_n=0; dut->enable_i=0; dut->i2s_sdout_i=1;
    dut->g_tready_i=1; dut->d_tready_i=1; dut->p2_tready_i=1;
    dut->dest_mac_i=0x91E0F000FE01ULL; dut->station_mac_i=0x020000000002ULL;
    dut->vlan_vid_i=2; dut->ptp_ns_i=0x11223344; dut->transit_ns_i=2000000;
    dut->p2_pair_valid_i=0; dut->p2_en_i=0;
    dut->p2_tctx_wr_en_i=0; dut->p2_tctx_rd_en_i=0;
    dut->ts_uncertain_i=0;
    cyc(8); dut->rst_n=1; dut->enable_i=1;

    printf("== NxN talker lane harness (NXN P4) ==\n");

    printf("\n[GB] golden byte-compare: flat talker vs capture+packetizer\n");
    // run until both sides produced 4 frames (SDOUT=1 -> 0xFFFFFF samples)
    for(long c=0; c<800000 && (gfr.size()<4 || dfr.size()<4); c++) step();
    ck("golden produced 4 frames", gfr.size()>=4, 1);
    ck("DUT produced 4 frames", dfr.size()>=4, 1);
    long nf = (long)((gfr.size()<dfr.size()? gfr.size():dfr.size()));
    if(nf>4) nf=4;
    long all_eq=1, len_ok=1;
    for(long f=0; f<nf; f++){
        if(gfr[f].size()!=90 || dfr[f].size()!=90) len_ok=0;
        if(gfr[f]!=dfr[f]){ all_eq=0;
            printf("    frame %ld differs (g%zu vs d%zu bytes)\n",
                   f, gfr[f].size(), dfr[f].size());
            for(size_t i=0;i<gfr[f].size() && i<dfr[f].size(); i++)
                if(gfr[f][i]!=dfr[f][i])
                    printf("      byte %zu: gold=%02x dut=%02x\n",
                           i, gfr[f][i], dfr[f][i]);
        }
    }
    ck("frame length 90 on both sides", len_ok, 1);
    ck("4 frames BYTE-EXACT gold vs shared packetizer", all_eq, 1);
    long tu0_ok=1;
    for(long f=0; f<nf; f++) if(dfr[f][21]!=0x00) tu0_ok=0;
    ck("synchronised clock: tu=0 on every frame", tu0_ok, 1);
    ck("DUT seq chain 0..3", nf==4 && dfr[0][20]==0 && dfr[1][20]==1 &&
                            dfr[2][20]==2 && dfr[3][20]==3, 1);
    ck("DUT ts = ptp+transit", nf>0 ? (long)be(dfr[0],30,4)
                                    : -1, (long)(0x11223344UL+2000000UL));
    cyc(50);                            // let the last TCTX writeback land
    ck("frames_sent_o alias tracks", dut->d_frames_o >= 4, 1);

    // [GBU] the same byte-compare with the clock declared UNCERTAIN. Two
    // things must hold at once: the flat golden talker and the shared
    // packetizer must AGREE (the N=1 axiom now covers the tu bit), and the
    // only byte that may move is 21 bit 0 - not tv, not the length, not the
    // cadence (Milan v1.2 5.3.7.3 forbids stopping the Stream Output).
    printf("\n[GBU] golden byte-compare with tu asserted\n");
    size_t g0=gfr.size(), d0=dfr.size();
    dut->ts_uncertain_i=1;
    for(long c=0; c<800000 && (gfr.size()<g0+3 || dfr.size()<d0+3); c++) step();
    ck("tu=1: golden still streams", gfr.size()>=g0+3, 1);
    ck("tu=1: DUT still streams",    dfr.size()>=d0+3, 1);
    long u_eq=1, u_tu=1, u_len=1, u_tv=1;
    for(size_t f=g0+1; f<g0+3 && f<gfr.size() && f<dfr.size(); f++){
        if(gfr[f]!=dfr[f]) u_eq=0;
        if(dfr[f].size()!=90) u_len=0;
        if(dfr[f][21]!=0x01) u_tu=0;
        if(dfr[f][19]!=0x81) u_tv=0;
    }
    ck("tu=1: gold and packetizer still BYTE-EXACT", u_eq, 1);
    ck("tu=1: frames still 90 bytes", u_len, 1);
    ck("tu=1: byte 21 bit 0 set on the wire", u_tu, 1);
    ck("tu=1: tv untouched (1722-2016 7.5)", u_tv, 1);
    dut->ts_uncertain_i=0;

    printf("\n[I2T] two-talker interleave (N=2, direct pair injection)\n");
    // t1 CFG via the TCTX window: DMAC base+1, uid=1, vid=2
    p2_tctx_wr(1, 1, 0xF000FE02u);          // DMAC_LO (wire bytes 2..5)
    p2_tctx_wr(1, 2, (1u<<16) | 0x91E0u);   // {UID=1, DMAC_HI}
    p2_tctx_wr(1, 0, (2u<<5) | (2u<<1) | 1u); // CTRL {en, chans=2, vid=2}
    dut->p2_en_i=3; cyc(4);
    p2fr.clear();

    // interleave pairs: 6 pairs per stream, alternating (shared cadence)
    for(int i=0;i<6;i++){
        pair(0, 0x100000+i, 0x200000+i);
        pair(1, 0x300000+i, 0x400000+i);
    }
    cyc(400);
    ck("two frames emitted", (long)p2fr.size(), 2);
    if(p2fr.size()==2){
        // identify per-stream frames by uid (stream_id low 16 bits)
        int i0 = (be(p2fr[0],22,8)&0xFFFF)==0 ? 0 : 1;
        int i1 = 1-i0;
        ck("both streams present (uid 0 + uid 1)",
           ((be(p2fr[i0],22,8)&0xFFFF)==0) && ((be(p2fr[i1],22,8)&0xFFFF)==1), 1);
        ck("t0 DMAC = CSR alias", be(p2fr[i0],0,6)==0x91E0F000FE01UL, 1);
        ck("t1 DMAC = TCTX (base+1)", be(p2fr[i1],0,6)==0x91E0F000FE02UL, 1);
        ck("t0 seq 0", p2fr[i0][20], 0);
        ck("t1 seq 0", p2fr[i1][20], 0);
        ck("t0 payload = its own samples",
           be(p2fr[i0],42,3)==0x100000UL && be(p2fr[i0],46,3)==0x200000UL, 1);
        ck("t1 payload = its own samples",
           be(p2fr[i1],42,3)==0x300000UL && be(p2fr[i1],46,3)==0x400000UL, 1);
        ck("both ts = ptp+transit", be(p2fr[i0],30,4)==0x11223344UL+2000000UL &&
                                    be(p2fr[i1],30,4)==0x11223344UL+2000000UL, 1);
    } else { for(int k=0;k<8;k++) ck("frame content (skipped: count wrong)",0,1); }

    printf("\n[I2T2] second epoch: per-stream seq/ts independence\n");
    dut->ptp_ns_i=0x22334455;               // ts moves for the next epoch
    p2fr.clear();
    for(int i=0;i<6;i++){
        pair(1, 0x500000+i, 0x600000+i);    // t1 first this time
        pair(0, 0x700000+i, 0x800000+i);
    }
    cyc(400);
    ck("two more frames", (long)p2fr.size(), 2);
    if(p2fr.size()==2){
        int i0 = (be(p2fr[0],22,8)&0xFFFF)==0 ? 0 : 1;
        int i1 = 1-i0;
        ck("t0 seq advanced to 1", p2fr[i0][20], 1);
        ck("t1 seq advanced to 1", p2fr[i1][20], 1);
        ck("epoch-2 ts latched fresh",
           be(p2fr[i0],30,4)==0x22334455UL+2000000UL &&
           be(p2fr[i1],30,4)==0x22334455UL+2000000UL, 1);
        ck("t1 epoch-2 payload", be(p2fr[i1],42,3)==0x500000UL, 1);
        ck("t0 epoch-2 payload", be(p2fr[i0],42,3)==0x700000UL, 1);
    } else { for(int k=0;k<5;k++) ck("epoch-2 content (skipped)",0,1); }

    printf("\n[I2T3] TCTX records: seq/frames per stream via the window\n");
    ck("t0 TCTX SEQ = 2", p2_tctx_rd(0,3), 2);
    ck("t1 TCTX SEQ = 2", p2_tctx_rd(1,3), 2);
    ck("t0 TCTX FRAMES = 2", p2_tctx_rd(0,5), 2);
    ck("t1 TCTX FRAMES = 2", p2_tctx_rd(1,5), 2);

    printf("\n[I2T4] per-stream gate: disabling t1 stops only t1\n");
    dut->p2_en_i=1; cyc(4);
    p2fr.clear();
    for(int i=0;i<6;i++){
        pair(0, 0x110000+i, 0x120000+i);
        pair(1, 0x130000+i, 0x140000+i);    // dropped (t1 disabled)
    }
    cyc(400);
    ck("only t0 emitted", (long)p2fr.size(), 1);
    if(p2fr.size()==1)
        ck("the emitted frame is t0's", (long)(be(p2fr[0],22,8)&0xFFFF), 0);
    else ck("t0 frame check (skipped)",0,1);

    // ================================================================== //
    // [TSL] avtp_timestamp LAW: per-epoch PHC LATCH, never an adder.      //
    //                                                                     //
    // Wire find (t532 silicon, 2026-08-09): the talker's avtp_timestamp   //
    // advanced EXACTLY 123750 ns per 6-sample PDU, min == max over 40000  //
    // PDUs, where Milan's 48 kHz owes 125000 ns - the 99-for-100 grid     //
    // (123750 = 6 x 2062.5 x 10 ns, and 2062.5 = 99 MHz/48000: a divider  //
    // fed 99e6 while the fabric clocks 100 MHz). The RTL law that makes   //
    // such a wrong grid IMPOSSIBLE to hide is: the timestamp is LATCHED   //
    // from the live PHC at each epoch's first pair (tsw_val_r <=          //
    // ptp_ns_i + transit), so consecutive-PDU deltas equal the REAL PHC   //
    // elapsed between epochs - 125000 ns at a true 48 kHz pacing - and    //
    // they TRACK the PHC rate. A synthesized ts += CONST cannot pass      //
    // both phases below; no suite asserted the absolute delta before      //
    // this leg (that is the desk gap that let t532 ship).                 //
    // ================================================================== //
    printf("\n[TSL] avtp_timestamp = per-epoch PHC latch (125000 ns law)\n");
    {
        // t0 only, clean slate; live PHC ramp at 10 ns per cycle = the
        // 100 MHz shipping grid
        dut->p2_en_i = 1; cyc(4);
        dut->ptp_ns_i = 0x01000000; g_ptp_rate = 10;
        p2fr.clear();
        // pace one pair per media tick, Bresenham 2083/2083/2084 = EXACTLY
        // 100e6/48000 average - 6 pairs per epoch, 12500 cycles per epoch
        long acc = 0;
        auto paced_pair = [&](int i, uint32_t l, uint32_t r) {
            dut->p2_pair_slot_i=0; dut->p2_pair_l_i=l&0xFFFFFF; dut->p2_pair_r_i=r&0xFFFFFF;
            dut->p2_pair_valid_i=1; cyc(); dut->p2_pair_valid_i=0;
            int period = ((i % 3) == 2) ? 2084 : 2083;
            cyc(period - 1);
            acc += period;
        };
        for (int s = 0; s < 6*6; s++)        // 6 epochs x 6 samples
            paced_pair(s, 0x600000 + s, 0x700000 + s);
        cyc(600);                            // drain the last emission
        ck("TSL: 6 paced epochs emitted 6 PDUs", (long)p2fr.size(), 6);
        long d_ok = 1, d_not_t532 = 1;
        for (size_t f = 1; f < p2fr.size(); f++) {
            long d = (long)((uint32_t)(be(p2fr[f],30,4) - be(p2fr[f-1],30,4)));
            if (d != 125000) d_ok = 0;
            if (d == 123750) d_not_t532 = 0;
            if (d != 125000)
                printf("         delta %zu = %ld ns (owed 125000)\n", f, d);
        }
        ck("TSL: EVERY consecutive-PDU delta = 125000 ns", d_ok, 1);
        ck("TSL: and never the t532 99-for-100 constant 123750", d_not_t532, 1);

        // ---- phase 2: warp the PHC rate x2 - the deltas MUST follow ------
        // (a latch tracks the clock it samples; a ts += CONST adder keeps
        // its constant and reddens exactly this check)
        g_ptp_rate = 20;
        p2fr.clear();
        for (int s = 0; s < 4*6; s++)
            paced_pair(s, 0x610000 + s, 0x710000 + s);
        cyc(600);
        ck("TSL warp: 4 epochs emitted 4 PDUs", (long)p2fr.size(), 4);
        long w_ok = 1;
        for (size_t f = 1; f < p2fr.size(); f++) {
            long d = (long)((uint32_t)(be(p2fr[f],30,4) - be(p2fr[f-1],30,4)));
            if (d != 250000) w_ok = 0;
            if (d != 250000)
                printf("         warp delta %zu = %ld ns (owed 250000)\n", f, d);
        }
        ck("TSL warp: deltas doubled with the PHC (latch, not adder)", w_ok, 1);
        g_ptp_rate = 0;                      // restore the static-poke mode
    }

    printf("\n======================================================================\n");
    printf("NxN talker lane: %ld checks, %ld failures\nRESULT: %s\n",
           checks, fails, fails?"FAIL":"PASS");
    delete dut;
    return fails ? 1 : 0;
}
