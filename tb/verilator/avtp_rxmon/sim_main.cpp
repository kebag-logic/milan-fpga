// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for KL_avtp_rx_monitor behind avtp_stream_parser —
// the Milan v1.2 STREAM_INPUT counter contract (pipewire stream.c
// handle_aaf_packet + cmd-get-counters.c, byte-extracted):
//   lock on first valid PDU / 8-PDU settle window / SEQ_NUM_MISMATCH with
//   STREAM_INTERRUPTED at lost>=2 / 100 ms silence unlock / per-PDU format
//   compare (UNSUPPORTED_FORMAT counts nothing else) / TIMESTAMP_UNCERTAIN
//   from tu / counter reset on the not-bound->bound edge.
// Clock is scaled: CLK_FREQ_HZ_P=10000 -> the 100 ms unlock = 1000 cycles.
#include "Vavtp_rxmon_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vavtp_rxmon_wrap* dut;
static long checks=0, fails=0;
static void ck(const char* t, long got, long exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-40s got=%ld exp=%ld\n",t,got,exp);}
    else printf("  [ ok ] %-40s = %ld\n",t,got); }

static void lo(){ dut->clk=0; dut->eval(); }
static void hi(){ dut->clk=1; dut->eval(); }
static void cyc(int n=1){ for(int i=0;i<n;i++){ lo(); hi(); } }

// STREAM_INPUT[0] current format: AAF 48 kHz / INT32 / depth 32 / 8 ch / 6 spf
static const uint64_t FMT = 0x0205022002006000ULL;
static const uint64_t SID = 0x020000FFFE010000ULL;

struct AafCfg {
    bool     tagged   = false;
    uint8_t  subtype  = 0x02;   // AAF
    bool     sv       = true;
    bool     tu       = false;
    uint8_t  seq      = 0;
    uint64_t sid      = SID;
    uint8_t  format   = 0x02;   // INT_32BIT
    uint8_t  nsr      = 0x05;   // 48 kHz
    uint8_t  chans    = 8;
    uint8_t  depth    = 32;
    uint8_t  sp       = 0;      // NORMAL
};

// build an Ethernet + AVTP AAF PDU with explicit format-specific fields
static std::vector<uint8_t> mkaaf(const AafCfg& c, int len=120){
    std::vector<uint8_t> f(len,0x00);
    for(int i=0;i<6;i++){ f[i]=0x91; f[6+i]=0x02; }
    int o;
    if(c.tagged){ f[12]=0x81; f[13]=0x00; f[14]=0x20; f[15]=0x02;
                  f[16]=0x22; f[17]=0xF0; o=18; }
    else        { f[12]=0x22; f[13]=0xF0; o=14; }
    f[o+0]=c.subtype;
    f[o+1]=(c.sv?0x80:0x00)|0x01;                       // sv, tv=1
    f[o+2]=c.seq;
    f[o+3]=c.tu?0x01:0x00;
    for(int i=0;i<8;i++) f[o+4+i]=(uint8_t)(c.sid>>(8*(7-i)));
    // avtp_timestamp arbitrary (0)
    f[o+16]=c.format;
    f[o+17]=(uint8_t)(c.nsr<<4);
    f[o+18]=c.chans;
    f[o+19]=c.depth;
    f[o+20]=0x00; f[o+21]=0x40;                         // data_len (unchecked)
    f[o+22]=(uint8_t)(c.sp<<4);
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
    dut->s_tvalid_i=0; dut->s_tlast_i=0; cyc(2);
}

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vavtp_rxmon_wrap;

    dut->cfg_sid_i=SID; dut->bound_i=0; dut->fmt_i=FMT;
    dut->resetn=0; dut->s_tvalid_i=0;
    cyc(6);
    dut->resetn=1; cyc(2);

    printf("== KL_avtp_rx_monitor harness (scaled clk: 100 ms = 1000 cyc) ==\n");

    printf("\n[1] unbound: matched-sid frame counts nothing\n");
    feed(mkaaf({}));
    ck("frames_rx 0", dut->cnt_frames_rx_o, 0);
    ck("not locked", dut->media_locked_o, 0);

    printf("\n[2] bind resets and arms (Milan Table 5.6)\n");
    dut->bound_i=1; cyc(2);
    ck("counters clear after bind", dut->cnt_frames_rx_o, 0);

    printf("\n[3] first valid PDU locks (seq seeded, settle armed)\n");
    { AafCfg c; c.seq=10; feed(mkaaf(c)); }
    ck("MEDIA_LOCKED 1", dut->cnt_media_locked_o, 1);
    ck("locked level", dut->media_locked_o, 1);
    ck("FRAMES_RX 1", dut->cnt_frames_rx_o, 1);

    printf("\n[4] settle window: a sequence step is absorbed, not counted\n");
    { AafCfg c; c.seq=11; feed(mkaaf(c)); }
    { AafCfg c; c.seq=50; feed(mkaaf(c)); }   // step inside settle -> re-seed
    { AafCfg c; c.seq=51; feed(mkaaf(c)); }
    ck("SEQ_NUM_MISMATCH 0 in settle", dut->cnt_seq_mismatch_o, 0);
    ck("FRAMES_RX 4", dut->cnt_frames_rx_o, 4);

    printf("\n[5] drain the settle window (8 post-lock PDUs)\n");
    for(uint8_t s=52; s<=56; s++){ AafCfg c; c.seq=s; feed(mkaaf(c)); }
    ck("still no mismatch", dut->cnt_seq_mismatch_o, 0);

    printf("\n[6] single loss: mismatch, NOT interrupted (lost=1)\n");
    { AafCfg c; c.seq=58; feed(mkaaf(c)); }   // expected 57 -> lost 1
    ck("SEQ_NUM_MISMATCH 1", dut->cnt_seq_mismatch_o, 1);
    ck("STREAM_INTERRUPTED 0", dut->cnt_stream_interrupted_o, 0);

    printf("\n[7] double loss: mismatch AND interrupted (lost=2)\n");
    { AafCfg c; c.seq=61; feed(mkaaf(c)); }   // expected 59 -> lost 2
    ck("SEQ_NUM_MISMATCH 2", dut->cnt_seq_mismatch_o, 2);
    ck("STREAM_INTERRUPTED 1", dut->cnt_stream_interrupted_o, 1);

    printf("\n[8] duplicate: lost=255 counts as interruption (reference math)\n");
    { AafCfg c; c.seq=61; feed(mkaaf(c)); }
    ck("SEQ_NUM_MISMATCH 3", dut->cnt_seq_mismatch_o, 3);
    ck("STREAM_INTERRUPTED 2", dut->cnt_stream_interrupted_o, 2);

    printf("\n[9] tu bit counts TIMESTAMP_UNCERTAIN\n");
    { AafCfg c; c.seq=62; c.tu=true; feed(mkaaf(c)); }
    ck("TIMESTAMP_UNCERTAIN 1", dut->cnt_ts_uncertain_o, 1);

    printf("\n[10] format mismatch counts UNSUPPORTED_FORMAT and nothing else\n");
    long frx = dut->cnt_frames_rx_o;
    { AafCfg c; c.seq=63; c.nsr=0x07; feed(mkaaf(c)); }       // 96 kHz PDU
    { AafCfg c; c.seq=63; c.depth=24; feed(mkaaf(c)); }       // wrong depth
    { AafCfg c; c.seq=63; c.chans=2;  feed(mkaaf(c)); }       // wrong channels
    { AafCfg c; c.seq=63; c.sp=1;     feed(mkaaf(c)); }       // sparse
    { AafCfg c; c.seq=63; c.subtype=0x04; feed(mkaaf(c)); }   // CRF on our sid
    ck("UNSUPPORTED_FORMAT 5", dut->cnt_unsupported_fmt_o, 5);
    ck("FRAMES_RX unchanged", dut->cnt_frames_rx_o, frx);
    { AafCfg c; c.seq=63; feed(mkaaf(c)); }   // good frame, seq continues
    ck("no mismatch across bad-format PDUs", dut->cnt_seq_mismatch_o, 3);

    printf("\n[11] VLAN-tagged PDU parses identically\n");
    { AafCfg c; c.seq=64; c.tagged=true; feed(mkaaf(c)); }
    ck("FRAMES_RX +2", dut->cnt_frames_rx_o, frx+2);
    ck("still locked", dut->media_locked_o, 1);

    printf("\n[12] 100 ms silence unlocks (MEDIA_UNLOCKED)\n");
    cyc(1100);
    ck("MEDIA_UNLOCKED 1", dut->cnt_media_unlocked_o, 1);
    ck("unlocked level", dut->media_locked_o, 0);

    printf("\n[13] relock: MEDIA_LOCKED again, settle re-armed\n");
    { AafCfg c; c.seq=200; feed(mkaaf(c)); }
    ck("MEDIA_LOCKED 2", dut->cnt_media_locked_o, 2);
    { AafCfg c; c.seq=90; feed(mkaaf(c)); }   // step right after relock
    ck("post-relock step absorbed", dut->cnt_seq_mismatch_o, 3);

    printf("\n[14] unbind -> rebind resets everything\n");
    dut->bound_i=0; cyc(4);
    ck("unbind does NOT reset", dut->cnt_media_locked_o, 2);
    dut->bound_i=1; cyc(4);
    ck("rebind resets MEDIA_LOCKED", dut->cnt_media_locked_o, 0);
    ck("rebind resets FRAMES_RX", dut->cnt_frames_rx_o, 0);
    ck("rebind resets mismatch", dut->cnt_seq_mismatch_o, 0);
    ck("rebind drops lock", dut->media_locked_o, 0);

    printf("\n[15] wrong stream_id never reaches the monitor\n");
    { AafCfg c; c.seq=0; c.sid=0x1111222233334444ULL; feed(mkaaf(c)); }
    ck("foreign sid: frames_rx 0", dut->cnt_frames_rx_o, 0);

    printf("\n======================================================================\n");
    printf("KL_avtp_rx_monitor: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
