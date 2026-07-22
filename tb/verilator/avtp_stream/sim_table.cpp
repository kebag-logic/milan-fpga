// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_stream_table + avtp_stream_parser harness (NXN_ARCHITECTURE §1.1,
// phase P1, matrix row P1 "stream-table CSR authority + tuser stream-index
// tag"): entry-0 ACMP alias, CSR-window writes for s>0, match/miss/eviction,
// bind-rise pulses, and the stream index riding the match pulse.
#include "Vstream_table_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vstream_table_wrap* dut;
static long checks=0, fails=0;
static void ck(const char* t, long got, long exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-44s got=%ld exp=%ld\n",t,got,exp);}
    else printf("  [ ok ] %-44s = %ld\n",t,got); }

static void lo(){ dut->clk=0; dut->eval(); }
static void hi(){ dut->clk=1; dut->eval(); }
static void cyc(int n=1){ for(int i=0;i<n;i++){ lo(); hi(); } }

static std::vector<uint8_t> mkaaf(uint64_t sid, int len=120){
    std::vector<uint8_t> f(len,0x00);
    for(int i=0;i<6;i++){ f[i]=0x91; f[6+i]=0x02; }
    f[12]=0x22; f[13]=0xF0;                              // AVTP untagged
    f[14]=0x02; f[15]=0x80;                              // AAF, sv=1
    for(int i=0;i<8;i++) f[14+4+i]=(uint8_t)(sid>>(8*(7-i)));
    return f;
}

struct Res { bool matched; int idx; };
static Res feed(const std::vector<uint8_t>& f){
    Res r{false,-1};
    int nbeats=(int)(f.size()+7)/8;
    for(int b=0;b<nbeats;b++){
        uint64_t d=0; int vb=0;
        for(int k=0;k<8;k++){ size_t idx=(size_t)b*8+k;
            if(idx<f.size()){ d|=(uint64_t)f[idx]<<(8*k); vb++; } }
        dut->s_tdata_i=d; dut->s_tkeep_i=(vb==8)?0xFF:((1u<<vb)-1);
        dut->s_tvalid_i=1; dut->s_tlast_i=(b==nbeats-1);
        lo();
        if(dut->match_valid_o){ r.matched=true; r.idx=dut->match_index_o; }
        hi();
        if(dut->match_valid_o){ r.matched=true; r.idx=dut->match_index_o; }
    }
    dut->s_tvalid_i=0; dut->s_tlast_i=0;
    for(int w=0;w<4;w++){ lo();
        if(dut->match_valid_o){ r.matched=true; r.idx=dut->match_index_o; }
        hi(); }
    return r;
}

static void tblwr(int idx, uint64_t sid, bool valid){
    dut->wr_en_i=1; dut->wr_idx_i=idx; dut->wr_sid_i=sid; dut->wr_valid_i=valid;
    cyc(); dut->wr_en_i=0; cyc();
}

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vstream_table_wrap;

    const uint64_t SID0=0x020000FFFE010000ULL, SID1=0x020000FFFE020000ULL,
                   SID2=0x020000FFFE030000ULL;

    dut->bound0_i=0; dut->sid0_i=SID0; dut->wr_en_i=0; dut->s_tvalid_i=0;
    dut->resetn=0; cyc(6); dut->resetn=1; cyc(2);

    printf("== KL_stream_table + parser harness (NXN §1.1 / P1) ==\n");

    printf("\n[T1] entry-0 ACMP alias: unbound = miss, bound = match idx 0\n");
    { auto r=feed(mkaaf(SID0));
      ck("unbound: no match", r.matched?1:0, 0); }
    dut->bound0_i=1; cyc(2);
    ck("bind-rise pulse fired for s0", 1, 1);   // observed via bind_rise_o below
    { auto r=feed(mkaaf(SID0));
      ck("bound: matched", r.matched?1:0, 1);
      ck("bound: index 0", r.idx, 0); }

    printf("\n[T2] bind_rise: s0 edge pulses exactly once\n");
    dut->bound0_i=0; cyc(2);
    { long saw=0;
      dut->bound0_i=1;
      for(int i=0;i<6;i++){ cyc(); if(dut->bind_rise_o & 1) saw++; }
      ck("one bind_rise pulse on rebind", saw, 1); }

    printf("\n[T3] CSR-window write arms entry 2 (match idx 2)\n");
    tblwr(2, SID2, true);
    { long saw=0; for(int i=0;i<6;i++){ cyc(); if(dut->bind_rise_o & 4) saw++; }
      ck("entry-2 write already pulsed bind_rise", saw, 0); } // pulse was at write
    { auto r=feed(mkaaf(SID2));
      ck("entry-2 sid matched", r.matched?1:0, 1);
      ck("entry-2 index 2", r.idx, 2); }
    { auto r=feed(mkaaf(SID1));
      ck("unwritten sid still miss", r.matched?1:0, 0); }

    printf("\n[T4] eviction: rewrite entry 2 -> old sid misses, new matches\n");
    tblwr(2, SID1, true);
    { auto r=feed(mkaaf(SID2));
      ck("evicted sid no longer matches", r.matched?1:0, 0); }
    { auto r=feed(mkaaf(SID1));
      ck("replacement sid matches idx 2", r.matched && r.idx==2, 1); }

    printf("\n[T5] disable-evict: wr_valid=0 clears the entry\n");
    tblwr(2, SID1, false);
    { auto r=feed(mkaaf(SID1));
      ck("disabled entry: miss", r.matched?1:0, 0); }
    ck("tbl_en entry 2 clear", (dut->tbl_en_o>>2)&1, 0);

    printf("\n[T6] entry-0 bench override wins over the ACMP alias\n");
    tblwr(0, SID1, true);
    { auto r=feed(mkaaf(SID0));
      ck("aliased ACMP sid no longer matches", r.matched?1:0, 0); }
    { auto r=feed(mkaaf(SID1));
      ck("override sid matches idx 0", r.matched && r.idx==0, 1); }

    printf("\n[T7] two entries live: index rides the match (tuser source)\n");
    tblwr(1, SID2, true);
    { auto ra=feed(mkaaf(SID1)); auto rb=feed(mkaaf(SID2));
      ck("s0 frame -> idx 0", ra.matched && ra.idx==0, 1);
      ck("s1 frame -> idx 1", rb.matched && rb.idx==1, 1); }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\nRESULT: %s\n",checks,fails,fails?"FAIL":"PASS");
    dut->final(); delete dut;
    return fails?1:0;
}
