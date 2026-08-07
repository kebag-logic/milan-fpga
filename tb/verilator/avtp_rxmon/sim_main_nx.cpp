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
//   [IV] Milan v1.2 Table 5.6 OBSERVATION-INTERVAL semantics ("incremented
//        at the end of every observation interval during which ...", <= 1 s)
//        for SEQ_NUM_MISMATCH / MEDIA_RESET / TIMESTAMP_UNCERTAIN /
//        UNSUPPORTED_FORMAT / LATE_TIMESTAMP / EARLY_TIMESTAMP / FRAMES_RX:
//        N events inside ONE interval move the counter by exactly 1 (the
//        per-frame reading is IEEE 1722.1-2021 Table 7-153's, and serving
//        it read 8000x high at class A), one event in EACH of two intervals
//        moves it by 2, and the per-event counters (MEDIA_LOCKED/UNLOCKED,
//        STREAM_INTERRUPTED - "incremented each time") stay per-event.
// Scaled clock: CLK_FREQ_HZ_P=100000 -> 1 ms = 100 cyc, the 100 ms silence
// unlock = 10000 cyc; observation interval IVAL_CYC_P=2000 cyc (20 scaled
// ms, conformant) - well inside the silence timeout, so an interval flush
// never unlocks a stream, exactly like 1 s vs 100 ms at speed.
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

// Milan v1.2 Table 5.6, MEDIA_UNLOCKED: "At any time, the PAAD-AE shall
// ensure that either MEDIA_LOCKED=MEDIA_UNLOCKED (in this case, the input
// stream is not synchronized on the media clock), or
// MEDIA_LOCKED=MEDIA_UNLOCKED+1 (in this case, the input stream is
// synchronized on the media clock)."
//
// Sampled on EVERY clock, but the verdict is on a SUSTAINED breach, not an
// instantaneous one.  The counters live in a BRAM the engine walks serially -
// the bind era-wipe zeroes MEDIA_LOCKED one cycle before MEDIA_UNLOCKED - so
// an every-cycle equality check flags walk transients that no controller can
// observe: GET_COUNTERS is answered from the CSR snapshot (milan_csr
// snap_req), which is what makes the read atomic.  A REAL breach - an unlock
// credited into an era whose counters were just zeroed - is PERMANENT until
// the next bind, so any threshold well above the longest walk separates them.
// Longest walk = bind (6 preserved-field/CFG writes + 10 counter zeroes)
// plus a parked remainder; 128 cycles is generous margin over that.
static const long INV_SETTLE_CYC = 128;
static long inv_run=0, inv_worst=0, inv_bad=0;
static void check_lock_invariant(){
    long ml=dut->cnt_media_locked_o, mu=dut->cnt_media_unlocked_o;
    if(ml==mu || ml==mu+1){ inv_run=0; return; }
    inv_run++;
    if(inv_run>inv_worst) inv_worst=inv_run;
    if(inv_run==INV_SETTLE_CYC){
        if(inv_bad<3) printf("  [FAIL] lock invariant SUSTAINED %ld cyc: "
                             "ML=%ld MU=%ld\n", inv_run, ml, mu);
        inv_bad++;
    }
}

static void sample(){
    check_lock_invariant();
    if(dut->pdu_accept_p_o) acc_idx.push_back(dut->pdu_accept_idx_o);
    if(dut->pcm_tvalid_o && dut->pcm_tready_i){
        for(int l=0;l<8;l++) pcm.push_back((dut->pcm_tdata_o>>(8*l))&0xFF);
        if(dut->pcm_tlast_o){ pcm_last=true; pcm_users.push_back(dut->pcm_tuser_o); }
    }
    if(dut->render_tvalid_o && dut->pcm_tready_i && dut->render_tlast_o)
        rend_users.push_back((int)dut->pcm_tuser_o);
}
static long gcyc=0;        // total clocked cycles (interval-phase tracking)
static long rst_cyc=0;     // gcyc at reset release = interval phase origin
static void lo(){ dut->clk=0; dut->eval(); }
static void hi(){ dut->clk=1; dut->eval(); sample(); gcyc++; }
static void cyc(int n=1){ for(int i=0;i<n;i++){ lo(); hi(); } }

// Milan Table 5.6 observation interval (must match the wrap's IVAL_CYC_P)
static const int IVAL = 2000;
// advance to just AFTER an interval tick, so a following burst of feeds
// lands wholly inside ONE fresh interval (the tick divider free-runs from
// reset release; 40 cycles of margin covers the tick pulse + a drain walk)
static void align_iv(){ cyc((int)(IVAL - (gcyc - rst_cyc) % IVAL) + 40); }
// guarantee at least one interval boundary passed AND its commit walked
static void flush_iv(){ cyc(IVAL + 80); }

// STREAM_INPUT current format: AAF 48 kHz / INT32 / depth 32 / 8 ch
static const uint64_t FMT  = 0x0205022002006000ULL;
static const uint64_t SID0 = 0x020000FFFE010000ULL;
static const uint64_t SID1 = 0x020000FFFE020000ULL;

struct AafCfg {
    uint64_t sid      = SID0;
    uint8_t  subtype  = 0x02;
    uint8_t  seq      = 0;
    bool     tu       = false;
    bool     tv       = true;   // b1 bit 0 (timestamp valid)
    bool     mr       = false;  // b1 bit 3 (media clock restart, 4.4.4.3)
    uint8_t  nsr      = 0x05;
    uint8_t  chans    = 8;
    uint8_t  depth    = 32;
};

static std::vector<uint8_t> mkaaf(const AafCfg& c, int len=120){
    std::vector<uint8_t> f(len,0x00);
    for(int i=0;i<6;i++){ f[i]=0x91; f[6+i]=0x02; }
    f[12]=0x22; f[13]=0xF0; int o=14;
    f[o+0]=c.subtype;
    f[o+1]=(uint8_t)(0x80|(c.mr?0x08:0x00)|(c.tv?0x01:0x00));
    f[o+2]=c.seq; f[o+3]=c.tu?0x01:0x00;
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

// feed the beats and STOP - no drain headroom, so the caller lands its next
// stimulus while the counter walk for this PDU is still in flight
static void feed_nowait(const std::vector<uint8_t>& f){
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

// LCTX CNT word offsets (Table 7-157 order, spec §1.4 w16..w25; the Milan
// 1.3 tv tallies ride the APPENDED columns at w26/w27)
enum { W_ML=16, W_MU=17, W_SI=18, W_SM=19, W_MR=20,
       W_TU=21, W_UF=22, W_LT=23, W_ET=24, W_FRX=25,
       W_TV=26, W_TNV=27 };

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vavtp_rxmon_nx_wrap;

    dut->bound0_i=0; dut->sid0_i=SID0; dut->fmt0_i=FMT;
    dut->tbl_wr_en_i=0; dut->lctx_wr_en_i=0; dut->lctx_rd_en_i=0;
    dut->route_wr_en_i=0; dut->pcm_tready_i=1;
    dut->ptp_now_i=0xA55AC33CUL-1000000; dut->pres_ofs_i=2000000;
    dut->clk_src_i=0; dut->servo_conv_i=0;
    dut->resetn=0; dut->s_tvalid_i=0;
    cyc(6); dut->resetn=1; rst_cyc=gcyc; cyc(4);

    printf("== NxN RX stack harness (N=4, NXN P1/P2/P3 + Table 5.6 IV) ==\n");

    printf("\n[G1] P2 golden: unbound frame counts nothing\n");
    feed(mkaaf({}));
    flush_iv();                 // even across an interval close
    ck("frames_rx 0", dut->cnt_frames_rx_o, 0);
    ck("not locked", dut->media_locked_o, 0);

    printf("\n[G2] P2 golden: bind resets and arms (Milan Table 5.6)\n");
    dut->bound0_i=1; cyc(30);
    ck("counters clear after bind", dut->cnt_frames_rx_o, 0);

    printf("\n[G3] P2 golden: first valid PDU locks, seq seeded\n");
    align_iv();
    { AafCfg c; c.seq=10; feed(mkaaf(c)); }
    ck("MEDIA_LOCKED 1 (event counter: immediate)",
       dut->cnt_media_locked_o, 1);
    ck("locked level", dut->media_locked_o, 1);
    //! Table 5.6: FRAMES_RX commits at the END of the observation interval
    ck("FRAMES_RX still 0 before the interval closes",
       dut->cnt_frames_rx_o, 0);
    flush_iv();
    ck("FRAMES_RX 1 after the interval closes", dut->cnt_frames_rx_o, 1);
    ck("last_ts captured", dut->last_ts_o == 0xA55AC33CUL, 1);
    ck("wire_chans follows the wire", dut->wire_chans_o, 8);

    printf("\n[G4] P2 golden: settle absorbs a step, then mismatch counts\n");
    { AafCfg c; c.seq=11; feed(mkaaf(c)); }
    { AafCfg c; c.seq=50; feed(mkaaf(c)); }
    for(uint8_t s=51; s<=57; s++){ AafCfg c; c.seq=s; feed(mkaaf(c)); }
    flush_iv();                 // a wrongly-raised flag would commit here
    ck("no mismatch through settle", dut->cnt_seq_mismatch_o, 0);
    { AafCfg c; c.seq=59; feed(mkaaf(c)); }       // expected 58 -> lost 1
    ck("STREAM_INTERRUPTED 0 (lost=1)", dut->cnt_stream_interrupted_o, 0);
    flush_iv();
    ck("SEQ_NUM_MISMATCH 1 (interval commit)", dut->cnt_seq_mismatch_o, 1);
    { AafCfg c; c.seq=62; feed(mkaaf(c)); }       // expected 60 -> lost 2
    //! STREAM_INTERRUPTED is "incremented each time" - no tick needed
    ck("STREAM_INTERRUPTED 1 (event, pre-tick)",
       dut->cnt_stream_interrupted_o, 1);
    flush_iv();
    ck("SEQ_NUM_MISMATCH 2 (second interval)", dut->cnt_seq_mismatch_o, 2);

    printf("\n[G5] P2 golden: tu + format compare (counts nothing else)\n");
    { AafCfg c; c.seq=63; c.tu=true; feed(mkaaf(c)); }
    flush_iv();
    ck("TIMESTAMP_UNCERTAIN 1", dut->cnt_ts_uncertain_o, 1);
    long frx=dut->cnt_frames_rx_o;
    align_iv();                 // both rejects inside ONE interval
    { AafCfg c; c.seq=64; c.nsr=0x07; feed(mkaaf(c)); }
    //! depth, not channels: channel count left the family compare with
    //! the Milan BAF Section 4 law (task #24)
    { AafCfg c; c.seq=64; c.depth=24; feed(mkaaf(c)); }
    flush_iv();
    //! two bad-format PDUs in one interval = ONE tick (Milan Table 5.6);
    //! the old per-frame reading counted 2 here
    ck("UNSUPPORTED_FORMAT 1 for a 2-reject interval",
       dut->cnt_unsupported_fmt_o, 1);
    ck("FRAMES_RX unchanged by rejects", dut->cnt_frames_rx_o, frx);
    { AafCfg c; c.seq=64; feed(mkaaf(c)); }
    flush_iv();
    ck("no mismatch across bad-format PDUs", dut->cnt_seq_mismatch_o, 2);

    printf("\n[G6] P2 golden: 100 ms silence unlocks (ms-grid watchdog)\n");
    cyc(12000);
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
    //! era wipe covers PENDING interval flags too: an uncommitted flag from
    //! before the bind edge must not tick a fresh counter after it
    align_iv();
    { AafCfg c; c.seq=210; feed(mkaaf(c)); }      // flag raised, no tick yet
    dut->bound0_i=0; cyc(10); dut->bound0_i=1; cyc(40);
    flush_iv();
    ck("pre-bind pending flag wiped, not committed",
       dut->cnt_frames_rx_o, 0);

    printf("\n[G8] P2 golden: LATE/EARLY/MEDIA_RESET at stream 0\n");
    { AafCfg c; c.seq=0; feed(mkaaf(c)); }        // relock on-time
    dut->ptp_now_i = 0xA55AC33CUL + 1000;
    { AafCfg c; c.seq=1; feed(mkaaf(c)); }
    flush_iv();
    ck("LATE counted", dut->cnt_late_ts_o, 1);
    dut->ptp_now_i = 0xA55AC33CUL - 50000000;
    { AafCfg c; c.seq=2; feed(mkaaf(c)); }
    flush_iv();
    ck("EARLY counted", dut->cnt_early_ts_o, 1);
    dut->ptp_now_i = 0xA55AC33CUL - 1000000;
    //! Milan Table 5.6 MEDIA_RESET = the received mr bit TOGGLED (a wire
    //! event), not a local playback rail
    { AafCfg c; c.seq=3; c.mr=true; feed(mkaaf(c)); }
    flush_iv();
    ck("MEDIA_RESET counted", dut->cnt_media_reset_o, 1);
    //! toggle back, so stream 0's mr LEVEL returns to 0 and the default-mr
    //! frames the rest of this harness feeds are not toggles
    { AafCfg c; c.seq=4; c.mr=false; feed(mkaaf(c)); }
    flush_iv();
    ck("MEDIA_RESET counts the return toggle too", dut->cnt_media_reset_o, 2);

    printf("\n[T1] P1: PCM payload byte-exact with tuser = 0 (stream 0)\n");
    pcm.clear(); pcm_users.clear(); pcm_last=false;
    { AafCfg c; c.seq=5; feed(mkaaf(c)); }
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
    flush_iv();                                   // commit [T1]'s frame first
    long s0_frx = dut->cnt_frames_rx_o;
    align_iv();                                   // s0 noise in ONE interval
    { AafCfg c; c.seq=6; c.tu=true; feed(mkaaf(c)); }       // s0 tu event
    { AafCfg c; c.seq=9; feed(mkaaf(c)); }                  // s0 seq jump
    { AafCfg c; c.seq=10; c.nsr=0x07; feed(mkaaf(c)); }     // s0 bad format
    flush_iv();
    //! coalesced law: 2 format-OK frames count; the bad-format PDU raises
    //! UF instead of FRX (the iv_events fork), so +2 not +3
    ck("s0 events landed (FRX +2 frames, coalesced)",
       dut->cnt_frames_rx_o, s0_frx+2);
    ck("s1 LCTX FRX still 0", lctx_rd(1, W_FRX), 0);
    ck("s1 LCTX SEQ_MM still 0", lctx_rd(1, W_SM), 0);
    ck("s1 LCTX TU still 0", lctx_rd(1, W_TU), 0);
    ck("s1 LCTX UNSUP still 0", lctx_rd(1, W_UF), 0);
    ck("s1 LCTX MEDIA_LOCKED still 0", lctx_rd(1, W_ML), 0);

    printf("\n[I2] P2 isolation: stream-1 PDUs count in s1's LCTX only\n");
    long s0_ml = dut->cnt_media_locked_o;
    long s0_frx2 = dut->cnt_frames_rx_o;
    align_iv();
    { AafCfg c; c.sid=SID1; c.seq=0; feed(mkaaf(c)); }
    { AafCfg c; c.sid=SID1; c.seq=1; c.tu=true; feed(mkaaf(c)); }
    flush_iv();
    ck("s1 LCTX FRX = 2 (2 PDUs, coalesced law)", lctx_rd(1, W_FRX), 2);
    ck("s1 LCTX MEDIA_LOCKED = 1", lctx_rd(1, W_ML), 1);
    ck("s1 LCTX TU = 1", lctx_rd(1, W_TU), 1);
    //! NULL routing discards AFTER the depacketizer - w11 still attributes,
    //! and w11 stays PER-FRAME (a depkt tally, not a Table 5.6 counter)
    ck("s1 LCTX DEPKT pdus = 2 (NULL discards post-depkt)",
       lctx_rd(1, 11) & 0xFFFF, 2);
    ck("s0 legacy FRX untouched", dut->cnt_frames_rx_o, s0_frx2);
    ck("s0 legacy ML untouched", dut->cnt_media_locked_o, s0_ml);
    ck("s1 w8 wire_chans = 8", (lctx_rd(1, 8) >> 14) & 0xFF, 8);

    printf("\n[R1] P3: s1 NULL by default - monitor counts, no PCM copy\n");
    pcm.clear(); pcm_users.clear();
    align_iv();
    { AafCfg c; c.sid=SID1; c.seq=2; feed(mkaaf(c)); }
    flush_iv();
    ck("NULL route: no ring bytes", (long)pcm.size(), 0);
    ck("NULL route: s1 LCTX FRX advanced", lctx_rd(1, W_FRX), 3);

    printf("\n[R2] P3: s1 -> DMA passes tagged, render tap stays s0\n");
    //! route field = FLAGS since the ALSA-design rework: bit0 DMA, bit1
    //! RENDER (s0 reset = 0b11 RENDER|DMA = the P3 RENDER behavior)
    routewr(1, 1 /*DMA flag*/);
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
    routewr(1, 2 /*RENDER flag*/);                // s0 and s1 both RENDER
    ck("lowest-indexed RENDER wins (sel=0)", dut->render_sel_o, 0);
    routewr(0, 1 /*DMA only*/);                   // s0 leaves RENDER
    ck("render_sel moves to 1", dut->render_sel_o, 1);
    rend_users.clear();
    { AafCfg c; c.sid=SID1; c.seq=4; c.chans=2; feed(mkaaf(c)); }
    { AafCfg c; c.seq=6; feed(mkaaf(c)); }        // s0 now DMA-only
    ck("render tap follows s1", rend_users.size()==1 && rend_users[0]==1, 1);
    ck("wire_chans follows the RENDER stream", dut->wire_chans_o, 2);
    routewr(0, 3); routewr(1, 0);                 // restore defaults

    printf("\n[E1] P1 eviction: unbind + retarget s1's table entry\n");
    //! an in-place rewrite keeps en=1 (no not-bound->bound edge, so no
    //! Milan counter reset - [M-5.3.8.10]); evict explicitly first
    tblwr(1, SID1, false); cyc(10);
    tblwr(1, 0x1111222233334444ULL, true); cyc(40);   // bind edge: CNT reset
    lctx_wr(1, 2, (uint32_t)(FMT & 0xFFFFFFFF));
    lctx_wr(1, 3, (uint32_t)(FMT >> 32));
    ck("s1 CNT reset on rebind", lctx_rd(1, W_FRX), 0);
    align_iv();
    { AafCfg c; c.sid=SID1; c.seq=5; feed(mkaaf(c)); }    // old sid: miss
    flush_iv();
    ck("evicted sid does not count", lctx_rd(1, W_FRX), 0);
    align_iv();
    { AafCfg c; c.sid=0x1111222233334444ULL; c.seq=0; feed(mkaaf(c)); }
    flush_iv();
    ck("new sid counts", lctx_rd(1, W_FRX), 1);

    printf("\n[M13] TIMESTAMP_VALID / TIMESTAMP_NOT_VALID (Milan 1.3 5.3.8.10;\n"
           "      1722.1-2021 Table 7-157 per-frame tv tallies, appended\n"
           "      LCTX words 26/27; per-frame BY DEFINITION - the TV+TNV ==\n"
           "      FRAMES_RX identity belongs to 1722.1's per-frame reading\n"
           "      and deliberately breaks against Milan interval FRAMES_RX)\n");
    //! s1 sits freshly rebound from [E1] with ONE tv=1 frame counted
    ck("[M13a] TV follows the [E1] frame", lctx_rd(1, W_TV), 1);
    ck("[M13b] TNV still 0", lctx_rd(1, W_TNV), 0);
    align_iv();
    { AafCfg c; c.sid=0x1111222233334444ULL; c.seq=1; c.tv=false;
      feed(mkaaf(c)); }
    ck("[M13c] tv=0 PDU -> TNV=1 (per-frame: immediate)",
       lctx_rd(1, W_TNV), 1);
    ck("[M13d] TV holds", lctx_rd(1, W_TV), 1);
    { AafCfg c; c.sid=0x1111222233334444ULL; c.seq=2; feed(mkaaf(c)); }
    flush_iv();
    //! 3 accepted frames, 2 observation intervals: the tallies say 3, the
    //! Milan FRAMES_RX says 2 - torture_campaign.tv_plus_tnv_identity()
    //! calls exactly this split "milan-interval" (INFO, not a defect)
    ck("[M13e] TV+TNV = accepted frames (3)",
       lctx_rd(1, W_TV) + lctx_rd(1, W_TNV), 3);
    //! coalesced law (USER 2026-08-05: ATDECC quantity, Milan cadence):
    //! FRAMES_RX == frames, so the 1722.1 identity TV+TNV == FRX holds
    ck("[M13e2] FRAMES_RX equals the tallies (coalesced law)",
       lctx_rd(1, W_FRX), 3);
    { long tvs = lctx_rd(1, W_TV) + lctx_rd(1, W_TNV);
      AafCfg c; c.sid=0x1111222233334444ULL; c.seq=3; c.chans=0;
      feed(mkaaf(c));                          // UF early-return
      ck("[M13f] unsupported-format PDU counts neither tally",
         lctx_rd(1, W_TV) + lctx_rd(1, W_TNV), tvs); }
    tblwr(1, 0x1111222233334444ULL, false); cyc(10);
    tblwr(1, 0x1111222233334444ULL, true);  cyc(40);  // bind edge: era wipe
    ck("[M13g] bind-zero walk clears TV (w26)", lctx_rd(1, W_TV), 0);
    ck("[M13h] bind-zero walk clears TNV (w27)", lctx_rd(1, W_TNV), 0);

    // ---------------------------------------------------------------- //
    // [IV] Milan v1.2 Table 5.6 interval semantics, the bite-proof set: //
    // N events inside ONE observation interval move each of the seven   //
    // interval counters by EXACTLY 1; per-event counters keep counting  //
    // per event; one event per interval across two intervals counts 2.  //
    // Runs on stream 2 (fresh context) so every delta starts at zero.   //
    // ---------------------------------------------------------------- //
    printf("\n[IV] Table 5.6 observation-interval semantics (stream 2)\n");
    static const uint64_t SID2 = 0x020000FFFE030000ULL;
    tblwr(2, SID2, true); cyc(40);                    // bind s2 (CNT zeroed)
    lctx_wr(2, 2, (uint32_t)(FMT & 0xFFFFFFFF));      // s2 FMT_LO
    lctx_wr(2, 3, (uint32_t)(FMT >> 32));             // s2 FMT_HI
    //! lock + drain the 8-PDU settle window so mismatches count
    for(uint8_t s=0; s<9; s++){ AafCfg c; c.sid=SID2; c.seq=s; feed(mkaaf(c)); }
    flush_iv();
    long iv_frx = lctx_rd(2, W_FRX);
    ck("[IV0] settle-drain committed (FRX = 9 frames, coalesced)",
       iv_frx, 9);

    printf("\n[IV1] FRAMES_RX: 6 PDUs, one interval -> +1 (was +6)\n");
    align_iv();
    for(uint8_t s=9; s<15; s++){ AafCfg c; c.sid=SID2; c.seq=s; feed(mkaaf(c)); }
    ck("[IV1a] uncommitted before the tick", lctx_rd(2, W_FRX), iv_frx);
    flush_iv();
    ck("[IV1b] FRAMES_RX += the burst's 6 frames (coalesced)",
       lctx_rd(2, W_FRX), iv_frx+6);

    printf("\n[IV2] SEQ_NUM_MISMATCH vs STREAM_INTERRUPTED: 3 gaps, one\n"
           "      interval -> SM +1 (was +3) while SI +3 (per-event)\n");
    align_iv();
    // expected 15 -> send 17 / 20 / 23: three lost=2 discontinuities
    { AafCfg c; c.sid=SID2; c.seq=17; feed(mkaaf(c)); }
    { AafCfg c; c.sid=SID2; c.seq=20; feed(mkaaf(c)); }
    { AafCfg c; c.sid=SID2; c.seq=23; feed(mkaaf(c)); }
    ck("[IV2a] SI = 3 immediately (Table 5.6: 'each time')",
       lctx_rd(2, W_SI), 3);
    ck("[IV2b] SM uncommitted before the tick", lctx_rd(2, W_SM), 0);
    flush_iv();
    ck("[IV2c] SM +1 for 3 gaps in one interval", lctx_rd(2, W_SM), 1);
    ck("[IV2d] SI still 3 (no interval inflation)", lctx_rd(2, W_SI), 3);

    printf("\n[IV3] TIMESTAMP_UNCERTAIN: 4 tu PDUs, one interval -> +1\n");
    align_iv();
    for(uint8_t s=24; s<28; s++){ AafCfg c; c.sid=SID2; c.seq=s; c.tu=true;
                                  feed(mkaaf(c)); }
    flush_iv();
    ck("[IV3] TU +1 for 4 tu frames", lctx_rd(2, W_TU), 1);

    printf("\n[IV4] UNSUPPORTED_FORMAT: 5 rejects, one interval -> +1\n");
    long iv_frx4 = lctx_rd(2, W_FRX);
    align_iv();
    for(int k=0;k<5;k++){ AafCfg c; c.sid=SID2; c.seq=28; c.nsr=0x07;
                          feed(mkaaf(c)); }
    flush_iv();
    ck("[IV4a] UF +1 for 5 rejects", lctx_rd(2, W_UF), 1);
    ck("[IV4b] rejects never advance FRAMES_RX", lctx_rd(2, W_FRX), iv_frx4);

    printf("\n[IV5] one event per interval, two intervals -> +2 (still a\n"
           "      counter, not a one-shot)\n");
    long iv_tu5 = lctx_rd(2, W_TU);
    { AafCfg c; c.sid=SID2; c.seq=28; c.tu=true; feed(mkaaf(c)); }
    flush_iv();
    { AafCfg c; c.sid=SID2; c.seq=29; c.tu=true; feed(mkaaf(c)); }
    flush_iv();
    ck("[IV5] TU +2 across two intervals", lctx_rd(2, W_TU), iv_tu5+2);

    printf("\n[IV6] MEDIA_RESET: 2 mr toggles, one interval -> +1 (was +2)\n");
    //! s2's mr level is 0 (every PDU fed to it so far defaulted mr=false),
    //! so mr=1 then mr=0 is exactly two toggles inside one interval
    long iv_mr = lctx_rd(2, W_MR);
    align_iv();
    { AafCfg c; c.sid=SID2; c.seq=30; c.mr=true;  feed(mkaaf(c)); }
    { AafCfg c; c.sid=SID2; c.seq=31; c.mr=false; feed(mkaaf(c)); }
    ck("[IV6a] uncommitted before the tick", lctx_rd(2, W_MR), iv_mr);
    flush_iv();
    ck("[IV6b] MEDIA_RESET +1 for 2 toggles in one interval",
       lctx_rd(2, W_MR), iv_mr+1);
    //! and the BITE the other way: a HELD mr is not a toggle at all
    align_iv();
    for(uint8_t s=32; s<38; s++){ AafCfg c; c.sid=SID2; c.seq=s; c.mr=false;
                                  feed(mkaaf(c)); }
    flush_iv();
    ck("[IV6c] 6 HELD-mr frames tick nothing", lctx_rd(2, W_MR), iv_mr+1);

    printf("\n[IV8] LATE_TIMESTAMP / EARLY_TIMESTAMP: the last two Table 5.6\n"
           "      interval counters. Both are 'incremented at the end of every\n"
           "      observation interval during which a Stream Data AVTPDU has\n"
           "      been received with an AVTP timestamp field that was in the\n"
           "      past / too far in the future to process', so a BURST inside\n"
           "      one interval is +1 - the same law as FRX/SM/TU/UF/MR.\n");
    {
        long lt0 = lctx_rd(2, W_LT), et0 = lctx_rd(2, W_ET);
        uint8_t sq = 40;
        // 5 LATE PDUs, ONE interval -> +1
        dut->ptp_now_i = 0xA55AC33CUL + 1000;             // ts already past
        align_iv();
        for(int k=0;k<5;k++){ AafCfg c; c.sid=SID2; c.seq=sq++; feed(mkaaf(c)); }
        ck("[IV8a] LATE uncommitted before the tick", lctx_rd(2, W_LT), lt0);
        flush_iv();
        ck("[IV8b] LATE +1 for a 5-PDU burst", lctx_rd(2, W_LT), lt0+1);
        ck("[IV8c] EARLY untouched by LATE PDUs", lctx_rd(2, W_ET), et0);
        // one LATE in EACH of two intervals -> +2 (still a counter)
        { AafCfg c; c.sid=SID2; c.seq=sq++; feed(mkaaf(c)); } flush_iv();
        { AafCfg c; c.sid=SID2; c.seq=sq++; feed(mkaaf(c)); } flush_iv();
        ck("[IV8d] LATE +2 across two intervals", lctx_rd(2, W_LT), lt0+3);
        // 4 EARLY PDUs, ONE interval -> +1
        dut->ptp_now_i = 0xA55AC33CUL - 50000000;         // far ahead
        align_iv();
        for(int k=0;k<4;k++){ AafCfg c; c.sid=SID2; c.seq=sq++; feed(mkaaf(c)); }
        flush_iv();
        ck("[IV8e] EARLY +1 for a 4-PDU burst", lctx_rd(2, W_ET), et0+1);
        ck("[IV8f] LATE untouched by EARLY PDUs", lctx_rd(2, W_LT), lt0+3);
        dut->ptp_now_i = 0xA55AC33CUL - 1000000;          // back on time
        align_iv();
        for(int k=0;k<4;k++){ AafCfg c; c.sid=SID2; c.seq=sq++; feed(mkaaf(c)); }
        flush_iv();
        ck("[IV8g] on-time PDUs move neither",
           lctx_rd(2, W_LT) + lctx_rd(2, W_ET), lt0+3+et0+1);
    }

    printf("\n[IV9] MEDIA_LOCKED / MEDIA_UNLOCKED are PER-EVENT ('incremented\n"
           "      each time ...'), and Table 5.6's lock invariant holds across\n"
           "      lock / silence-unlock / rebind churn: either ML=MU (not\n"
           "      synchronized) or ML=MU+1 (synchronized).\n");
    {
        static const uint64_t SIDA = 0x020000FFFE050000ULL;
        tblwr(1, SIDA, false); cyc(10);
        tblwr(1, SIDA, true);  cyc(40);            // fresh era on stream 1
        lctx_wr(1, 2, (uint32_t)(FMT & 0xFFFFFFFF));
        lctx_wr(1, 3, (uint32_t)(FMT >> 32));
        ck("[IV9a] bind zeroes both", lctx_rd(1, W_ML) + lctx_rd(1, W_MU), 0);
        uint8_t sq = 0;
        // three lock/unlock laps: each lock is +1 ML, each 100 ms silence +1 MU
        for (int lap = 0; lap < 3; lap++) {
            { AafCfg c; c.sid=SIDA; c.seq=sq++; feed(mkaaf(c)); }
            ck("[IV9b] MEDIA_LOCKED is immediate (per-event)",
               lctx_rd(1, W_ML), lap+1);
            ck("[IV9c] synchronized => ML = MU+1",
               lctx_rd(1, W_ML) == lctx_rd(1, W_MU)+1, 1);
            cyc(12000);                            // > 100 ms scaled: unlock
            ck("[IV9d] MEDIA_UNLOCKED is immediate (per-event)",
               lctx_rd(1, W_MU), lap+1);
            ck("[IV9e] not synchronized => ML = MU",
               lctx_rd(1, W_ML) == lctx_rd(1, W_MU), 1);
        }
        tblwr(1, SIDA, false); cyc(10);
        //! THE ERA BOUNDARY under the task-#25 free-wheel law: clock-source
        //! churn (the gPTP-change shape) must never generate an unlock, so
        //! sweeping clk_src flips and rebind edges across the lock walk's
        //! whole window has to leave the pair invariant legal AND the
        //! stream locked in every phase - the churn is pure noise now.
        uint8_t sq0 = 0;
        long bad_ph = -1;
        for (int ph = 0; ph < 24 && bad_ph < 0; ph++) {
            dut->clk_src_i = 0; dut->servo_conv_i = 0;
            dut->bound0_i = 0; cyc(8);
            dut->bound0_i = 1; cyc(60);                 // fresh era, s0
            { AafCfg c; c.seq=sq0++; feed_nowait(mkaaf(c)); }  // lock, busy
            dut->clk_src_i = 1;             // churn mid-walk: NOT an unlock
            cyc(ph);                        // ... swept across the walk
            dut->bound0_i = 0; cyc(1);      // rebind edge, mid-flight
            dut->bound0_i = 1; cyc(160);
            dut->clk_src_i = 0; cyc(40);
            long ml = dut->cnt_media_locked_o, mu = dut->cnt_media_unlocked_o;
            if (!(ml == mu || ml == mu + 1)) {
                printf("  [FAIL] [IV9f] phase %d left ML=%ld MU=%ld\n",
                       ph, ml, mu);
                bad_ph = ph;
            }
        }
        ck("[IV9f] rebind never strands MU above ML (24 phases)", bad_ph, -1);
        printf("      (worst illegal-pair run seen: %ld cyc, limit %ld)\n",
               inv_worst, INV_SETTLE_CYC);
        ck("[IV9g] the 'at any time' invariant never breached for good",
           inv_bad, 0);
        dut->clk_src_i = 0; dut->servo_conv_i = 0;
        dut->bound0_i = 0; cyc(10); dut->bound0_i = 1; cyc(40);
    }

    printf("\n[IV7] back-to-back PDUs across EVERY interval-drain phase: the\n"
           "      commit verdict must beat each frame's tlast (walker yield;\n"
           "      hostplane ax8x8 lost 1 of 2 b2b ring frames without it)\n");
    {
        // stream 3 (fresh): bind, set FMT, lock + drain settle
        static const uint64_t SID3 = 0x020000FFFE040000ULL;
        tblwr(3, SID3, true); cyc(40);
        lctx_wr(3, 2, (uint32_t)(FMT & 0xFFFFFFFF));
        lctx_wr(3, 3, (uint32_t)(FMT >> 32));
        uint8_t sq = 0;
        for (int k = 0; k < 9; k++){ AafCfg c; c.sid=SID3; c.seq=sq++;
                                     feed(mkaaf(c)); }
        // sweep the b2b pair's start across a whole interval of drain
        // phases; s0 (RENDER, bound) gets fresh MR+TU+LT flags each lap so
        // the tick always has a multi-counter drain to run
        long lost = 0;
        for (int ph = 0; ph < 40; ph++) {
            dut->ptp_now_i = 0xA55AC33CUL + 1000;           // s0 late
            //! alternate s0's mr every lap so MEDIA_RESET joins TU+LATE+FRX
            //! in the drain - the tick always has a multi-counter walk to run
            { AafCfg c; c.seq=(uint8_t)(100+ph); c.tu=true; c.mr=(ph & 1);
              feed(mkaaf(c)); }                       // s0 tu+late+mr flags
            dut->ptp_now_i = 0xA55AC33CUL - 1000000;
            cyc((int)(IVAL - (gcyc - rst_cyc) % IVAL) - 8 + ph); // tick-8+ph
            size_t a0 = acc_idx.size();
            // two frames with ZERO gap on the lane (b2b tlast->tvalid)
            auto f1 = mkaaf([&]{ AafCfg c; c.sid=SID3; c.seq=sq++;
                                 return c; }());
            auto f2 = mkaaf([&]{ AafCfg c; c.sid=SID3; c.seq=sq++;
                                 return c; }());
            std::vector<uint8_t> b2b(f1); b2b.insert(b2b.end(),
                                                     f2.begin(), f2.end());
            int nbeats = (int)(b2b.size()+7)/8;
            for (int b = 0; b < nbeats; b++) {
                uint64_t d = 0; int vb = 0;
                for (int k2 = 0; k2 < 8; k2++){ size_t ix=(size_t)b*8+k2;
                    if (ix < b2b.size()){ d |= (uint64_t)b2b[ix]<<(8*k2); vb++; } }
                dut->s_tdata_i=d; dut->s_tkeep_i=(vb==8)?0xFF:((1u<<vb)-1);
                dut->s_tvalid_i=1;
                dut->s_tlast_i=(b == 14 || b == nbeats-1);  // 120 B = 15 beats
                cyc();
            }
            dut->s_tvalid_i=0; dut->s_tlast_i=0; cyc(60);
            if (acc_idx.size() - a0 != 2) lost++;
        }
        ck("[IV7] no accept verdict missed across 40 drain phases", lost, 0);
    }

    printf("\n======================================================================\n");
    printf("NxN RX stack: %ld checks, %ld failures\nRESULT: %s\n",
           checks, fails, fails?"FAIL":"PASS");
    delete dut;
    return fails ? 1 : 0;
}
