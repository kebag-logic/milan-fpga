// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_stream_table + avtp_stream_parser harness (docs/overview/ARCHITECTURE.md,
// matrix row P1 "stream-table CSR authority + tuser stream-index
// tag"): entry-0 ACMP alias, CSR-window writes for s>0, match/miss/eviction,
// bind-rise pulses, and the stream index riding the match pulse.
#include "Vstream_table_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <cstdint>
#include <vector>

// Frame layout and bus geometry the stimulus builder and feed() work in.
constexpr int kBitsPerByte      = 8;    // shift distance per octet
constexpr int kMacBytes         = 6;    // dst/src MAC, 6 octets each
constexpr int kStreamIdBytes    = 8;    // AVTP stream_id field
constexpr int kBusBytes         = 8;    // s_tdata_i is 64 bits = 8 lanes
constexpr uint8_t kKeepAll      = 0xFF; // s_tkeep_i with every lane valid
constexpr int kResetCycles      = 6;    // clocks held with resetn low
constexpr int kDrainCycles      = 4;    // idle clocks after tlast, to catch a late match
constexpr int kPulseWatchCycles = 6;    // clocks watched for a bind_rise pulse

namespace {

struct Res { bool matched; int idx; };

//! The stream-table harness: the model, the tally and the stimulus buffer are
//! its members, so nothing this suite mutates lives at file scope (I.2).
class StreamTableHarness {
 public:
    int run();

 private:
    void ck(const char* t, long got, long exp){
        checks++; if(got!=exp){ fails++; printf("  [FAIL] %-44s got=%ld exp=%ld\n",t,got,exp);}
        else printf("  [ ok ] %-44s = %ld\n",t,got); }

    void lo(){ dut->clk=0; dut->eval(); }
    void hi(){ dut->clk=1; dut->eval(); }
    void cyc(int n=1){ for(int i=0;i<n;i++){ lo(); hi(); } }

    const std::vector<uint8_t>& build_aaf(std::vector<uint8_t>& out,
                                                 uint64_t sid, int len=120){
        out.assign(len,0x00);           // assign KEEPS the capacity
        std::vector<uint8_t>& f = out;
        for(int i=0;i<kMacBytes;i++){ f[i]=0x91; f[kMacBytes+i]=0x02; }
        f[12]=0x22; f[13]=0xF0;                              // AVTP untagged
        f[14]=0x02; f[15]=0x80;                              // AAF, sv=1
        for(int i=0;i<kStreamIdBytes;i++)
            f[14+4+i]=static_cast<uint8_t>(sid>>(kBitsPerByte*(kStreamIdBytes-1-i)));
        return out;
    }

    Res feed(const std::vector<uint8_t>& f){
        Res r{false,-1};
        int nbeats=static_cast<int>(f.size()+kBusBytes-1)/kBusBytes;
        for(int b=0;b<nbeats;b++){
            uint64_t d=0; int vb=0;
            for(int k=0;k<kBusBytes;k++){ size_t idx=static_cast<size_t>(b)*kBusBytes+k;
                if(idx<f.size()){ d|=static_cast<uint64_t>(f[idx])<<(kBitsPerByte*k); vb++; } }
            dut->s_tdata_i=d; dut->s_tkeep_i=(vb==kBusBytes)?kKeepAll:((1u<<vb)-1);
            dut->s_tvalid_i=1; dut->s_tlast_i=(b==nbeats-1);
            lo();
            if(dut->match_valid_o){ r.matched=true; r.idx=dut->match_index_o; }
            hi();
            if(dut->match_valid_o){ r.matched=true; r.idx=dut->match_index_o; }
        }
        dut->s_tvalid_i=0; dut->s_tlast_i=0;
        for(int w=0;w<kDrainCycles;w++){ lo();
            if(dut->match_valid_o){ r.matched=true; r.idx=dut->match_index_o; }
            hi(); }
        return r;
    }

    void tblwr(int idx, uint64_t sid, bool valid){
        dut->wr_en_i=1; dut->wr_idx_i=idx; dut->wr_sid_i=sid; dut->wr_valid_i=valid;
        cyc(); dut->wr_en_i=0; cyc();
    }

    const milan::tb::Model<Vstream_table_wrap> model;
    Vstream_table_wrap* dut = model.get();
    long checks=0;
    long fails=0;
    //! One reusable frame buffer for the whole run: build_aaf() fills it through a
    //! reference and assign() keeps the capacity, so the stimulus frames cost ONE
    //! allocation between them instead of one each.
    std::vector<uint8_t> stim;
};

int StreamTableHarness::run(){
    constexpr uint64_t SID0=0x020000FFFE010000ULL;
    constexpr uint64_t SID1=0x020000FFFE020000ULL;
    constexpr uint64_t SID2=0x020000FFFE030000ULL;

    dut->bound0_i=0; dut->sid0_i=SID0; dut->wr_en_i=0; dut->s_tvalid_i=0;
    dut->resetn=0; cyc(kResetCycles); dut->resetn=1; cyc(2);

    printf("== KL_stream_table + parser harness (NXN §1.1 / P1) ==\n");

    printf("\n[T1] entry-0 ACMP alias: unbound = miss, bound = match idx 0\n");
    { auto r=feed(build_aaf(stim, SID0));
      ck("unbound: no match", r.matched?1:0, 0); }
    dut->bound0_i=1; cyc(2);
    ck("bind-rise pulse fired for s0", 1, 1);   // observed via bind_rise_o below
    { auto r=feed(build_aaf(stim, SID0));
      ck("bound: matched", r.matched?1:0, 1);
      ck("bound: index 0", r.idx, 0); }

    printf("\n[T2] bind_rise: s0 edge pulses exactly once\n");
    dut->bound0_i=0; cyc(2);
    { long saw=0;
      dut->bound0_i=1;
      for(int i=0;i<kPulseWatchCycles;i++){ cyc(); if(dut->bind_rise_o & 1) saw++; }
      ck("one bind_rise pulse on rebind", saw, 1); }

    printf("\n[T3] CSR-window write arms entry 2 (match idx 2)\n");
    tblwr(2, SID2, true);
    { long saw=0;
      for(int i=0;i<kPulseWatchCycles;i++){ cyc(); if(dut->bind_rise_o & 4) saw++; }
      ck("entry-2 write already pulsed bind_rise", saw, 0); } // pulse was at write
    { auto r=feed(build_aaf(stim, SID2));
      ck("entry-2 sid matched", r.matched?1:0, 1);
      ck("entry-2 index 2", r.idx, 2); }
    { auto r=feed(build_aaf(stim, SID1));
      ck("unwritten sid still miss", r.matched?1:0, 0); }

    printf("\n[T4] eviction: rewrite entry 2 -> old sid misses, new matches\n");
    tblwr(2, SID1, true);
    { auto r=feed(build_aaf(stim, SID2));
      ck("evicted sid no longer matches", r.matched?1:0, 0); }
    { auto r=feed(build_aaf(stim, SID1));
      ck("replacement sid matches idx 2", r.matched && r.idx==2, 1); }

    printf("\n[T5] disable-evict: wr_valid=0 clears the entry\n");
    tblwr(2, SID1, false);
    { auto r=feed(build_aaf(stim, SID1));
      ck("disabled entry: miss", r.matched?1:0, 0); }
    ck("tbl_en entry 2 clear", (dut->tbl_en_o>>2)&1, 0);

    printf("\n[T6] entry-0 bench override wins over the ACMP alias\n");
    tblwr(0, SID1, true);
    { auto r=feed(build_aaf(stim, SID0));
      ck("aliased ACMP sid no longer matches", r.matched?1:0, 0); }
    { auto r=feed(build_aaf(stim, SID1));
      ck("override sid matches idx 0", r.matched && r.idx==0, 1); }

    printf("\n[T7] two entries live: index rides the match (tuser source)\n");
    tblwr(1, SID2, true);
    { auto ra=feed(build_aaf(stim, SID1)); auto rb=feed(build_aaf(stim, SID2));
      ck("s0 frame -> idx 0", ra.matched && ra.idx==0, 1);
      ck("s1 frame -> idx 1", rb.matched && rb.idx==1, 1); }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\nRESULT: %s\n",checks,fails,fails?"FAIL":"PASS");
    return fails?1:0;
}

}  // namespace

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    StreamTableHarness harness;
    return harness.run();
}
