// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// NxN lane-A RX stack harness (docs/NXN_ARCHITECTURE.md):
//   [G]  P2 matrix row: N=1-shape golden regression - the ctx engine's
//        stream-0 legacy view reproduces the flat KL_avtp_rx_monitor
//        contract (lock/settle/mismatch/interrupt/silence/format/bind).
//   [I]  P2 matrix row: per-stream counter isolation - stream-0 events
//        never leak into stream 1's LCTX CNT region and vice versa.
//   [T]  P1 matrix row: tuser stream-index tag parser->FIFO->PCM output.
//   [R]  P3 matrix row: PCM routing policy - RENDER-lowest-wins, NULL
//        discard (monitor still counts), DMA passes tagged, render tap
//        follows the configured stream.
// Scaled clock: CLK_FREQ_HZ_P=10000 -> 1 ms = 10 cyc, 100 ms = 1000 cyc.
#include "Vavtp_rxmon_nx_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vavtp_rxmon_nx_wrap* dut;
static long checks=0, fails=0;
static void ck(const char* t, long got, long exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-46s got=%ld exp=%ld\n",t,got,exp);}
    else printf("  [ ok ] %-46s = %ld\n",t,got); }

static std::vector<uint8_t> pcm;         // ring-output payload bytes
static std::vector<int>     pcm_users;   // tuser per ring PDU (at tlast)
static std::vector<int>     rend_users;  // render-tap PDUs (tuser at tlast)
static std::vector<int>     acc_idx;     // accept-pulse indices
static bool pcm_last=false;

static void sample(){
    if(dut->pdu_accept_p_o) acc_idx.push_back(dut->pdu_accept_idx_o);
    if(dut->pcm_tvalid_o && dut->pcm_tready_i){
        for(int l=0;l<8;l++) pcm.push_back((dut->pcm_tdata_o>>(8*l))&0xFF);
        if(dut->pcm_tlast_o){ pcm_last=true; pcm_users.push_back(dut->pcm_tuser_o); }
    }
    if(dut->render_tvalid_o && dut->pcm_tready_i && dut->render_tlast_o)
        rend_users.push_back((int)dut->pcm_tuser_o);
}
static void lo(){ dut->clk=0; dut->eval(); }
static void hi(){ dut->clk=1; dut->eval(); sample(); }
static void cyc(int n=1){ for(int i=0;i<n;i++){ lo(); hi(); } }

// STREAM_INPUT current format: AAF 48 kHz / INT32 / depth 32 / 8 ch
static const uint64_t FMT  = 0x0205022002006000ULL;
static const uint64_t SID0 = 0x020000FFFE010000ULL;
static const uint64_t SID1 = 0x020000FFFE020000ULL;

struct AafCfg {
    uint64_t sid      = SID0;
    uint8_t  subtype  = 0x02;
    uint8_t  seq      = 0;
    bool     tu       = false;
    uint8_t  nsr      = 0x05;
    uint8_t  chans    = 8;
    uint8_t  depth    = 32;
};

static std::vector<uint8_t> mkaaf(const AafCfg& c, int len=120){
    std::vector<uint8_t> f(len,0x00);
    for(int i=0;i<6;i++){ f[i]=0x91; f[6+i]=0x02; }
    f[12]=0x22; f[13]=0xF0; int o=14;
    f[o+0]=c.subtype; f[o+1]=0x81; f[o+2]=c.seq; f[o+3]=c.tu?0x01:0x00;
    for(int i=0;i<8;i++) f[o+4+i]=(uint8_t)(c.sid>>(8*(7-i)));
    f[o+12]=0xA5; f[o+13]=0x5A; f[o+14]=0xC3; f[o+15]=0x3C;
    f[o+16]=0x02;                       // format INT32
    f[o+17]=(uint8_t)(c.nsr<<4);
    f[o+18]=c.chans; f[o+19]=c.depth;
    f[o+20]=0x00; f[o+21]=0x40;         // data_len = 64
    f[o+22]=0x00;
    for(int i=0;i<64;i++) f[o+24+i]=(uint8_t)(0x30+i);
    return f;
}

static void feed(const std::vector<uint8_t>& f){
    int nbeats=(int)(f.size()+7)/8;
    for(int b=0;b<nbeats;b++){
        uint64_t d=0; int vb=0;
        for(int k=0;k<8;k++){ size_t idx=(size_t)b*8+k;
            if(idx<f.size()){ d|=(uint64_t)f[idx]<<(8*k); vb++; } }
        dut->s_tdata_i=d; dut->s_tkeep_i=(vb==8)?0xFF:((1u<<vb)-1);
        dut->s_tvalid_i=1; dut->s_tlast_i=(b==nbeats-1);
        cyc();
    }
    dut->s_tvalid_i=0; dut->s_tlast_i=0;
    cyc(40);                            // walk + FIFO drain headroom
}

static void tblwr(int idx, uint64_t sid, bool valid){
    dut->tbl_wr_en_i=1; dut->tbl_wr_idx_i=idx;
    dut->tbl_wr_sid_i=sid; dut->tbl_wr_valid_i=valid;
    cyc(); dut->tbl_wr_en_i=0; cyc(2);
}

static void routewr(int idx, int val){
    dut->route_wr_en_i=1; dut->route_wr_idx_i=idx; dut->route_wr_val_i=val;
    cyc(); dut->route_wr_en_i=0; cyc();
}

static uint32_t lctx_rd(int s, int w){
    dut->lctx_rd_en_i=1; dut->lctx_rd_addr_i=(uint8_t)((s<<5)|w);
    for(int i=0;i<64;i++){ cyc();
        if(dut->lctx_rd_valid_o){ dut->lctx_rd_en_i=0; uint32_t v=dut->lctx_rd_data_o; cyc(); return v; } }
    dut->lctx_rd_en_i=0; printf("  [FAIL] lctx_rd timeout s%d w%d\n",s,w); fails++; checks++;
    return 0xDEADBEEF;
}

static void lctx_wr(int s, int w, uint32_t v){
    dut->lctx_wr_en_i=1; dut->lctx_wr_addr_i=(uint8_t)((s<<5)|w);
    dut->lctx_wr_data_i=v;
    for(int i=0;i<64;i++){ lo(); bool rdy=dut->lctx_wr_rdy_o; hi(); sample();
        if(rdy){ dut->lctx_wr_en_i=0; cyc(); return; } }
    dut->lctx_wr_en_i=0; printf("  [FAIL] lctx_wr timeout s%d w%d\n",s,w); fails++; checks++;
}

// LCTX CNT word offsets (Table 7-157 order, spec §1.4 w16..w25)
enum { W_ML=16, W_MU=17, W_SI=18, W_SM=19, W_MR=20,
       W_TU=21, W_UF=22, W_LT=23, W_ET=24, W_FRX=25 };

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vavtp_rxmon_nx_wrap;

    dut->bound0_i=0; dut->sid0_i=SID0; dut->fmt0_i=FMT;
    dut->tbl_wr_en_i=0; dut->lctx_wr_en_i=0; dut->lctx_rd_en_i=0;
    dut->route_wr_en_i=0; dut->pcm_tready_i=1;
    dut->ptp_now_i=0xA55AC33CUL-1000000; dut->pres_ofs_i=2000000;
    dut->media_reset_p_i=0; dut->clk_src_i=0; dut->servo_conv_i=0;
    dut->resetn=0; dut->s_tvalid_i=0;
    cyc(6); dut->resetn=1; cyc(4);

    printf("== NxN RX stack harness (N=4, NXN P1/P2/P3) ==\n");

    printf("\n[G1] P2 golden: unbound frame counts nothing\n");
    feed(mkaaf({}));
    ck("frames_rx 0", dut->cnt_frames_rx_o, 0);
    ck("not locked", dut->media_locked_o, 0);

    printf("\n[G2] P2 golden: bind resets and arms (Milan Table 5.6)\n");
    dut->bound0_i=1; cyc(30);
    ck("counters clear after bind", dut->cnt_frames_rx_o, 0);

    printf("\n[G3] P2 golden: first valid PDU locks, seq seeded\n");
    { AafCfg c; c.seq=10; feed(mkaaf(c)); }
    ck("MEDIA_LOCKED 1", dut->cnt_media_locked_o, 1);
    ck("locked level", dut->media_locked_o, 1);
    ck("FRAMES_RX 1", dut->cnt_frames_rx_o, 1);
    ck("last_ts captured", dut->last_ts_o == 0xA55AC33CUL, 1);
    ck("wire_chans follows the wire", dut->wire_chans_o, 8);

    printf("\n[G4] P2 golden: settle absorbs a step, then mismatch counts\n");
    { AafCfg c; c.seq=11; feed(mkaaf(c)); }
    { AafCfg c; c.seq=50; feed(mkaaf(c)); }
    for(uint8_t s=51; s<=57; s++){ AafCfg c; c.seq=s; feed(mkaaf(c)); }
    ck("no mismatch through settle", dut->cnt_seq_mismatch_o, 0);
    { AafCfg c; c.seq=59; feed(mkaaf(c)); }       // expected 58 -> lost 1
    ck("SEQ_NUM_MISMATCH 1", dut->cnt_seq_mismatch_o, 1);
    ck("STREAM_INTERRUPTED 0 (lost=1)", dut->cnt_stream_interrupted_o, 0);
    { AafCfg c; c.seq=62; feed(mkaaf(c)); }       // expected 60 -> lost 2
    ck("SEQ_NUM_MISMATCH 2", dut->cnt_seq_mismatch_o, 2);
    ck("STREAM_INTERRUPTED 1 (lost=2)", dut->cnt_stream_interrupted_o, 1);

    printf("\n[G5] P2 golden: tu + format compare (counts nothing else)\n");
    { AafCfg c; c.seq=63; c.tu=true; feed(mkaaf(c)); }
    ck("TIMESTAMP_UNCERTAIN 1", dut->cnt_ts_uncertain_o, 1);
    long frx=dut->cnt_frames_rx_o;
    { AafCfg c; c.seq=64; c.nsr=0x07; feed(mkaaf(c)); }
    { AafCfg c; c.seq=64; c.chans=9; feed(mkaaf(c)); }
    ck("UNSUPPORTED_FORMAT 2", dut->cnt_unsupported_fmt_o, 2);
    ck("FRAMES_RX unchanged", dut->cnt_frames_rx_o, frx);
    { AafCfg c; c.seq=64; feed(mkaaf(c)); }
    ck("no mismatch across bad-format PDUs", dut->cnt_seq_mismatch_o, 2);

    printf("\n[G6] P2 golden: 100 ms silence unlocks (ms-grid watchdog)\n");
    cyc(1200);
    ck("MEDIA_UNLOCKED 1", dut->cnt_media_unlocked_o, 1);
    ck("unlocked level", dut->media_locked_o, 0);
    { AafCfg c; c.seq=200; feed(mkaaf(c)); }
    ck("relock: MEDIA_LOCKED 2", dut->cnt_media_locked_o, 2);

    printf("\n[G7] P2 golden: unbind keeps, rebind resets\n");
    dut->bound0_i=0; cyc(10);
    ck("unbind does NOT reset", dut->cnt_media_locked_o, 2);
    dut->bound0_i=1; cyc(40);
    ck("rebind resets MEDIA_LOCKED", dut->cnt_media_locked_o, 0);
    ck("rebind resets FRAMES_RX", dut->cnt_frames_rx_o, 0);
    ck("rebind drops lock", dut->media_locked_o, 0);

    printf("\n[G8] P2 golden: LATE/EARLY/MEDIA_RESET at stream 0\n");
    { AafCfg c; c.seq=0; feed(mkaaf(c)); }        // relock on-time
    dut->ptp_now_i = 0xA55AC33CUL + 1000;
    { AafCfg c; c.seq=1; feed(mkaaf(c)); }
    ck("LATE counted", dut->cnt_late_ts_o, 1);
    dut->ptp_now_i = 0xA55AC33CUL - 50000000;
    { AafCfg c; c.seq=2; feed(mkaaf(c)); }
    ck("EARLY counted", dut->cnt_early_ts_o, 1);
    dut->ptp_now_i = 0xA55AC33CUL - 1000000;
    dut->media_reset_p_i=1; cyc(); dut->media_reset_p_i=0; cyc(30);
    ck("MEDIA_RESET counted", dut->cnt_media_reset_o, 1);

    printf("\n[T1] P1: PCM payload byte-exact with tuser = 0 (stream 0)\n");
    pcm.clear(); pcm_users.clear(); pcm_last=false;
    { AafCfg c; c.seq=3; feed(mkaaf(c)); }
    ck("PCM 64 bytes", (long)pcm.size(), 64);
    ck("PCM tlast", pcm_last?1:0, 1);
    { bool ok=pcm.size()>=64;
      for(int i=0;i<64&&ok;i++) if(pcm[i]!=(uint8_t)(0x30+i)) ok=false;
      ck("PCM payload byte-exact", ok?1:0, 1); }
    ck("PCM tuser = 0", pcm_users.size()==1 ? pcm_users[0] : -1, 0);
    ck("accept idx = 0", acc_idx.empty() ? -1 : acc_idx.back(), 0);

    printf("\n[I1] P2 isolation: arm stream 1 (table + LCTX FMT), s0 noise\n");
    tblwr(1, SID1, true); cyc(40);                // bind s1 (LCTX s1 zeroed)
    lctx_wr(1, 2, (uint32_t)(FMT & 0xFFFFFFFF));  // s1 FMT_LO
    lctx_wr(1, 3, (uint32_t)(FMT >> 32));         // s1 FMT_HI
    long s0_frx = dut->cnt_frames_rx_o;
    { AafCfg c; c.seq=4; c.tu=true; feed(mkaaf(c)); }       // s0 tu event
    { AafCfg c; c.seq=9; feed(mkaaf(c)); }                  // s0 seq jump
    { AafCfg c; c.seq=10; c.nsr=0x07; feed(mkaaf(c)); }     // s0 bad format
    ck("s0 events landed (FRX +2)", dut->cnt_frames_rx_o, s0_frx+2);
    ck("s1 LCTX FRX still 0", lctx_rd(1, W_FRX), 0);
    ck("s1 LCTX SEQ_MM still 0", lctx_rd(1, W_SM), 0);
    ck("s1 LCTX TU still 0", lctx_rd(1, W_TU), 0);
    ck("s1 LCTX UNSUP still 0", lctx_rd(1, W_UF), 0);
    ck("s1 LCTX MEDIA_LOCKED still 0", lctx_rd(1, W_ML), 0);

    printf("\n[I2] P2 isolation: stream-1 PDUs count in s1's LCTX only\n");
    long s0_ml = dut->cnt_media_locked_o;
    long s0_frx2 = dut->cnt_frames_rx_o;
    { AafCfg c; c.sid=SID1; c.seq=0; feed(mkaaf(c)); }
    { AafCfg c; c.sid=SID1; c.seq=1; c.tu=true; feed(mkaaf(c)); }
    ck("s1 LCTX FRX = 2", lctx_rd(1, W_FRX), 2);
    ck("s1 LCTX MEDIA_LOCKED = 1", lctx_rd(1, W_ML), 1);
    ck("s1 LCTX TU = 1", lctx_rd(1, W_TU), 1);
    //! NULL routing discards AFTER the depacketizer - w11 still attributes
    ck("s1 LCTX DEPKT pdus = 2 (NULL discards post-depkt)",
       lctx_rd(1, 11) & 0xFFFF, 2);
    ck("s0 legacy FRX untouched", dut->cnt_frames_rx_o, s0_frx2);
    ck("s0 legacy ML untouched", dut->cnt_media_locked_o, s0_ml);
    ck("s1 w8 wire_chans = 8", (lctx_rd(1, 8) >> 14) & 0xFF, 8);

    printf("\n[R1] P3: s1 NULL by default - monitor counts, no PCM copy\n");
    pcm.clear(); pcm_users.clear();
    { AafCfg c; c.sid=SID1; c.seq=2; feed(mkaaf(c)); }
    ck("NULL route: no ring bytes", (long)pcm.size(), 0);
    ck("NULL route: s1 LCTX FRX advanced", lctx_rd(1, W_FRX), 3);

    printf("\n[R2] P3: s1 -> DMA passes tagged, render tap stays s0\n");
    routewr(1, 2 /*DMA*/);
    pcm.clear(); pcm_users.clear(); rend_users.clear();
    { AafCfg c; c.sid=SID1; c.seq=3; feed(mkaaf(c)); }
    { AafCfg c; c.seq=5; feed(mkaaf(c)); }        // s0 (RENDER default)
    ck("two ring PDUs", (long)pcm_users.size(), 2);
    ck("first ring PDU tuser = 1", pcm_users.size()>0 ? pcm_users[0] : -1, 1);
    ck("second ring PDU tuser = 0", pcm_users.size()>1 ? pcm_users[1] : -1, 0);
    ck("render tap saw only s0", (long)rend_users.size(), 1);
    ck("render tap PDU was s0", rend_users.size()==1 ? rend_users[0] : -1, 0);
    ck("s1 DEPKT pdus accumulated (2 NULL + 1 NULL + 1 DMA)",
       lctx_rd(1, 11) & 0xFFFF, 4);

    printf("\n[R3] P3: RENDER-lowest-wins + render switch\n");
    routewr(1, 1 /*RENDER*/);                     // s0 and s1 both RENDER
    ck("lowest-indexed RENDER wins (sel=0)", dut->render_sel_o, 0);
    routewr(0, 2 /*DMA*/);                        // s0 leaves RENDER
    ck("render_sel moves to 1", dut->render_sel_o, 1);
    rend_users.clear();
    { AafCfg c; c.sid=SID1; c.seq=4; c.chans=2; feed(mkaaf(c)); }
    { AafCfg c; c.seq=6; feed(mkaaf(c)); }        // s0 now DMA
    ck("render tap follows s1", rend_users.size()==1 && rend_users[0]==1, 1);
    ck("wire_chans follows the RENDER stream", dut->wire_chans_o, 2);
    routewr(0, 1); routewr(1, 0);                 // restore defaults

    printf("\n[E1] P1 eviction: unbind + retarget s1's table entry\n");
    //! an in-place rewrite keeps en=1 (no not-bound->bound edge, so no
    //! Milan counter reset - [M-5.3.8.10]); evict explicitly first
    tblwr(1, SID1, false); cyc(10);
    tblwr(1, 0x1111222233334444ULL, true); cyc(40);   // bind edge: CNT reset
    lctx_wr(1, 2, (uint32_t)(FMT & 0xFFFFFFFF));
    lctx_wr(1, 3, (uint32_t)(FMT >> 32));
    ck("s1 CNT reset on rebind", lctx_rd(1, W_FRX), 0);
    { AafCfg c; c.sid=SID1; c.seq=5; feed(mkaaf(c)); }    // old sid: miss
    ck("evicted sid does not count", lctx_rd(1, W_FRX), 0);
    { AafCfg c; c.sid=0x1111222233334444ULL; c.seq=0; feed(mkaaf(c)); }
    ck("new sid counts", lctx_rd(1, W_FRX), 1);

    printf("\n======================================================================\n");
    printf("NxN RX stack: %ld checks, %ld failures\nRESULT: %s\n",
           checks, fails, fails?"FAIL":"PASS");
    delete dut;
    return fails ? 1 : 0;
}
