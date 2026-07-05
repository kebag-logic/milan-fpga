// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for avtp_stream_parser: feeds hand-built AVTP AAF /
// CVF / control / non-AVTP frames (untagged and VLAN-tagged) and checks the
// extracted stream_id, presentation timestamp, subtype, tv, and the
// programmable stream_id match (index + counters).
#include "Vavtp_stream_parser.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vavtp_stream_parser* dut;
static long checks=0, fails=0;
static void ck(const char* t, long got, long exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-34s got=%ld exp=%ld\n",t,got,exp);} }
static void ckx(const char* t, uint64_t got, uint64_t exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-34s got=%llx exp=%llx\n",t,
        (unsigned long long)got,(unsigned long long)exp);} }

static void lo(){ dut->clk=0; dut->eval(); }
static void hi(){ dut->clk=1; dut->eval(); }

// build an Ethernet+AVTP frame. tagged adds a C-VLAN. subtype/sv/tv/sid/ts set
// the AVTP header. len pads to `len` bytes.
static std::vector<uint8_t> mkavtp(bool tagged,uint8_t subtype,bool sv,bool tv,
                                   uint64_t sid,uint32_t ts,int len){
    std::vector<uint8_t> f(len,0x00);
    for(int i=0;i<6;i++){ f[i]=0x91; f[6+i]=0x02; }        // dst/src MAC
    int o;
    if(tagged){ f[12]=0x81; f[13]=0x00; f[14]=0x20; f[15]=0x02;   // C-VLAN
                f[16]=0x22; f[17]=0xF0; o=18; }
    else      { f[12]=0x22; f[13]=0xF0; o=14; }
    f[o+0]=subtype;
    f[o+1]=(sv?0x80:0x00)|0x10|(tv?0x01:0x00);             // sv,version=1,tv
    f[o+2]=0x00; f[o+3]=0x00;
    for(int i=0;i<8;i++) f[o+4+i]=(uint8_t)(sid>>(8*(7-i)));// stream_id MS first
    for(int i=0;i<4;i++) f[o+12+i]=(uint8_t)(ts>>(8*(3-i)));// avtp_timestamp
    // payload bytes are arbitrary (already 0)
    return f;
}

struct Res { bool matched; int idx; uint64_t sid; uint32_t ts; int sub; bool tv; };

// drive one frame; capture the (single) match/parse pulse observed
static Res feed(const std::vector<uint8_t>& f){
    Res r{false,0,0,0,-1,false};
    int nbeats=(f.size()+7)/8;
    for(int b=0;b<nbeats;b++){
        uint64_t d=0; int vb=0;
        for(int k=0;k<8;k++){ size_t idx=b*8+k; if(idx<f.size()){ d|=(uint64_t)f[idx]<<(8*k); vb++; } }
        dut->s_tdata_i=d; dut->s_tkeep_i=(vb==8)?0xFF:((1u<<vb)-1);
        dut->s_tvalid_i=1; dut->s_tready_i=1; dut->s_tlast_i=(b==nbeats-1);
        lo();
        // capture the parse pulse (avtp_frames increments) and match pulse
        static uint32_t prev_af=0;
        bool parsed = (dut->avtp_frames_o != prev_af);
        if(parsed){ r.sid=dut->stream_id_o; r.ts=dut->avtp_ts_o; r.sub=dut->subtype_o; r.tv=dut->ts_valid_o; }
        if(dut->match_valid_o){ r.matched=true; r.idx=dut->match_index_o; }
        prev_af=dut->avtp_frames_o;
        hi();
    }
    dut->s_tvalid_i=0; dut->s_tlast_i=0; lo(); hi();
    return r;
}

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vavtp_stream_parser;

    // program the match table: entry 3 = 0xAABBCCDD00112233, entry 5 = 0x1122...
    const uint64_t SID_A=0xAABBCCDD00112233ULL, SID_B=0x1122334455667788ULL;
    // packed [64*8] input = 16 x 32-bit words; entry e -> words {2e:lo, 2e+1:hi}
    for(int w=0;w<16;w++) dut->cfg_stream_id_i[w]=0;
    auto setentry=[&](int e,uint64_t v){ dut->cfg_stream_id_i[2*e]=(uint32_t)v;
                                          dut->cfg_stream_id_i[2*e+1]=(uint32_t)(v>>32); };
    setentry(3,SID_A);
    setentry(5,SID_B);
    dut->cfg_stream_en_i=(1<<3)|(1<<5);

    dut->resetn=0; dut->s_tvalid_i=0;
    for(int i=0;i<6;i++){ lo(); hi(); }
    dut->resetn=1;

    printf("== avtp_stream_parser harness ==\n");

    // 1. untagged AAF (subtype 0x02), matches entry 3
    { auto r=feed(mkavtp(false,0x02,true,true,SID_A,0x12345678,200));
      ckx("untagged AAF stream_id",r.sid,SID_A);
      ck ("untagged AAF ts",r.ts,0x12345678);
      ck ("untagged AAF subtype",r.sub,0x02);
      ck ("untagged AAF tv",r.tv,1);
      ck ("untagged AAF matched",r.matched,1);
      ck ("untagged AAF match idx",r.idx,3); }

    // 2. VLAN-tagged CVF (0x03), matches entry 5
    { auto r=feed(mkavtp(true,0x03,true,false,SID_B,0xCAFEBABE,300));
      ckx("vlan CVF stream_id",r.sid,SID_B);
      ck ("vlan CVF ts",r.ts,0xCAFEBABE);
      ck ("vlan CVF subtype",r.sub,0x03);
      ck ("vlan CVF tv",r.tv,0);
      ck ("vlan CVF matched",r.matched,1);
      ck ("vlan CVF match idx",r.idx,5); }

    // 3. AAF with an UNKNOWN stream_id -> parsed but not matched
    { auto r=feed(mkavtp(false,0x02,true,true,0xDEADBEEF0BADF00DULL,0x1,200));
      ck ("unknown sid parsed",r.sub,0x02);
      ck ("unknown sid NOT matched",r.matched,0); }

    // 4. control subtype (AECP 0xFB) -> not a stream, no parse/match
    { auto r=feed(mkavtp(false,0xFB,true,true,SID_A,0x1,200));
      ck ("control subtype no match",r.matched,0);
      ck ("control subtype not parsed",r.sub,-1); }

    // 5. sv=0 stream frame -> ignored
    { auto r=feed(mkavtp(false,0x02,false,true,SID_A,0x1,200));
      ck ("sv=0 not matched",r.matched,0); }

    // 6. non-AVTP (EtherType 0x0800 IPv4) -> nothing
    { std::vector<uint8_t> ip(200,0); for(int i=0;i<6;i++){ip[i]=0x91;ip[6+i]=0x02;}
      ip[12]=0x08; ip[13]=0x00;
      auto r=feed(ip);
      ck ("ipv4 no match",r.matched,0);
      ck ("ipv4 not parsed",r.sub,-1); }

    // 7. counters: 3 AVTP stream frames w/ sv=1 (tests 1,2,3,5? no sv=0 excluded);
    //    matched = 2 (tests 1,2). tests 1,2,3 = 3 parses; test 5 sv=0 excluded.
    ck ("avtp_frames counter",dut->avtp_frames_o,3);
    ck ("matched_frames counter",dut->matched_frames_o,2);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\nRESULT: %s\n",checks,fails,fails?"FAIL":"PASS");
    dut->final(); delete dut;
    return fails?1:0;
}
