// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for KL_maap - IEEE 1722 Annex B vs the module-avb
// maap.c reference contract: 3 probes @500ms+jitter -> announce @3-5s
// (address valid only announced); RX PROBE conflict: probing->re-address,
// announced->DEFEND with the overlap; RX DEFEND/ANNOUNCE with conflicting
// CONFLICT fields -> re-address (reference quirk: the REQUEST fields of a
// received ANNOUNCE are NOT checked - byte-faithful to maap.c).
// Scaled clock: CLK_FREQ_HZ_P=10000 -> 1 ms = 10 cycles.
#include "VKL_maap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#if VM_COVERAGE
#include "verilated_cov.h"
#endif
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>

// wait_tx budgets, in scaled cycles (CLK_FREQ_HZ_P=10000 -> 1 ms = 10 cycles)
constexpr int kProbeBudgetCyc    = 9000;    // probe interval 500-627 ms
constexpr int kAnnounceBudgetCyc = 55000;   // first announce 3000-5047 ms
constexpr int kDefendBudgetCyc   = 200;     // a DEFEND answers the PROBE at once
// cycles allowed for an injected PDU to be parsed and acted on
constexpr int kSettleCyc = 50;
// highest offset the RTL can claim: POOL_SIZE_C (0xFE00) - count_i (8)
constexpr uint16_t kMaxOffset = 0xFDF8;

namespace {

//! The KL_maap harness: the model, the tally and the TX capture state are its
//! members, so nothing this suite mutates lives at file scope (I.2).
class MaapHarness {
 public:
    int run();

 private:
    void ck(const char* t, long got, long exp){
        checks++; if(got!=exp){ fails++; printf("  [FAIL] %-44s got=%ld exp=%ld\n",t,got,exp);}
        else printf("  [ ok ] %-44s = %ld\n",t,got); }

    void cyc(int n=1){
        for(int i=0;i<n;i++){
            dut->clk_i=0; dut->eval();
            dut->clk_i=1; dut->eval();
            if(dut->m_axis_tvalid && dut->m_axis_tready){
                int nb = (dut->m_axis_tkeep==0xFF)?8:4;
                for(int l=0;l<nb;l++) txf.push_back((dut->m_axis_tdata>>(8*l))&0xFF);
                if(dut->m_axis_tlast) tx_done=true;
            }
        }
    }

    // run until a full TX frame is captured or budget expires; returns frame.
    // txf is NOT cleared on entry: a frame may already be in flight (e.g. a
    // DEFEND that starts during inject()) and must not be truncated.
    std::vector<uint8_t> wait_tx(int budget){
        for(int i=0;i<budget && !tx_done;i++) cyc();
        auto f=txf; txf.clear(); tx_done=false;
        return f;
    }

    // inject a MAAP PDU on the RX tap (untagged, 60B padded); maap_version
    // defaults to the reference's 1 (byte 16 = version<<3 | len[10:8])
    void inject(uint8_t msg, uint16_t req_off, uint16_t req_cnt,
                uint16_t conf_off, uint16_t conf_cnt, bool conf_pool=true,
                uint8_t maap_ver=1){
        uint8_t f[64]; memset(f,0,sizeof f);
        const uint8_t dst[6]={0x91,0xE0,0xF0,
                              0x00,0xFF,0x00};
        const uint8_t src[6]={0x66,0x77,0x88,
                              0x99,0xAA,0xBB};
        memcpy(f,dst,6); memcpy(f+6,src,6);
        f[12]=0x22; f[13]=0xF0; f[14]=0xFE; f[15]=msg;
        f[16]=static_cast<uint8_t>((maap_ver&0x1F)<<3); f[17]=0x1C;
        f[26]=0x91; f[27]=0xE0; f[28]=0xF0; f[29]=0x00;
        f[30]=req_off>>8; f[31]=req_off;
        f[32]=req_cnt>>8; f[33]=req_cnt;
        if(conf_pool){ f[34]=0x91; f[35]=0xE0; f[36]=0xF0; f[37]=0x00; }
        f[38]=conf_off>>8; f[39]=conf_off;
        f[40]=conf_cnt>>8; f[41]=conf_cnt;
        for(int b=0;b<8;b++){
            uint64_t v=0;
            for(int j=0;j<8;j++) v|=static_cast<uint64_t>(f[b*8+j])<<(8*j);
            dut->rx_tdata_i=v; dut->rx_tkeep_i=(b==7)?0x0F:0xFF;
            dut->rx_tvalid_i=1; dut->rx_tready_i=1; dut->rx_tlast_i=(b==7);
            cyc();
        }
        dut->rx_tvalid_i=0; dut->rx_tlast_i=0; cyc(3);
    }

    void bring_up_idle();
    void check_reset_idle();
    uint16_t claim_offset_through_three_probes();
    void check_first_announce_frame(uint16_t off0);
    void defend_the_overlap_against_a_probe(uint16_t off0);
    void ignore_announce_covering_our_request(uint16_t off0);
    void readdress_on_conflicting_defend(uint16_t off0);
    void readdress_silently_while_probing();
    void ignore_disjoint_and_non_pool_pdus();
    void honour_conflicts_from_any_maap_version();
    void disable_then_claim_the_seed();

    const milan::tb::Model<VKL_maap> model;
    VKL_maap* dut = model.get();
    long checks=0;
    long fails=0;

    std::vector<uint8_t> txf;      // collected TX frame (wire bytes)
    bool tx_done=false;
};

void MaapHarness::bring_up_idle(){
    constexpr uint64_t MAC=0x020000000001ULL;   // 02:00:00:00:00:01
    dut->station_mac_i=MAC;
    dut->enable_i=0; dut->count_i=8;
    dut->seed_offset_i=0; dut->seed_valid_i=0;
    dut->m_axis_tready=1; dut->rx_tvalid_i=0;
    dut->rst_n=0; cyc(6); dut->rst_n=1; cyc(3);

    printf("== KL_maap harness (10 kHz scaled: 1 ms = 10 cyc) ==\n");
}

void MaapHarness::check_reset_idle(){
    printf("\n[1] reset/idle\n");
    ck("state IDLE", dut->state_o, 0);
    ck("addr not valid", dut->addr_valid_o, 0);
}

uint16_t MaapHarness::claim_offset_through_three_probes(){
    printf("\n[2] enable -> PROBE, three golden probes, then ANNOUNCE\n");
    dut->enable_i=1; cyc(3);
    ck("state PROBE", dut->state_o, 1);
    uint16_t off0 = dut->offset_o;
    ck("offset inside pool", off0 <= kMaxOffset, 1);
    for(int p=0;p<3;p++){
        auto f=wait_tx(kProbeBudgetCyc);          // 500-627ms = 5000-6270 cyc
        char nm[64]; snprintf(nm,sizeof nm,"probe %d emitted (60B)",p+1);
        ck(nm, static_cast<long>(f.size()), 60);
        if(f.size()==60){
            ck("dst 91:E0:F0:00:FF:00", memcmp(f.data(),
               (const uint8_t[]){0x91,0xE0,0xF0,0x00,0xFF,0x00},6)==0, 1);
            ck("src station mac", f[6]==0x02&&f[11]==0x01, 1);
            ck("ethertype/subtype", f[12]==0x22&&f[13]==0xF0&&f[14]==0xFE, 1);
            ck("msg PROBE", f[15]&0x0F, 1);
            ck("version/len bytes", f[16]==0x08&&f[17]==0x1C, 1);
            ck("request_start pool+off",
               f[26]==0x91&&f[27]==0xE0&&f[28]==0xF0&&f[29]==0x00&&
               f[30]==(off0>>8)&&f[31]==(off0&0xFF), 1);
            ck("request_count 8", (f[32]<<8)|f[33], 8);
            ck("conflict fields zero",
               f[34]|f[35]|f[36]|f[37]|f[38]|f[39]|f[40]|f[41], 0);
        }
    }
    ck("state ANNOUNCE after 3 probes", dut->state_o, 2);
    ck("addr valid", dut->addr_valid_o, 1);
    ck("addr = pool base + offset",
       static_cast<long>((dut->addr_o>>16)&0xFFFFFFFF)==0x91E0F000UL &&
       (dut->addr_o&0xFFFF)==off0, 1);
    return off0;
}

void MaapHarness::check_first_announce_frame(uint16_t off0){
    printf("\n[3] first ANNOUNCE frame (msg 3, same request fields)\n");
    { auto f=wait_tx(kAnnounceBudgetCyc);           // 3000-5047ms
      ck("announce emitted", static_cast<long>(f.size()), 60);
      if(f.size()==60){
          ck("msg ANNOUNCE", f[15]&0x0F, 3);
          ck("announce offset unchanged", f[30]==(off0>>8)&&f[31]==(off0&0xFF), 1);
      } }
}

void MaapHarness::defend_the_overlap_against_a_probe(uint16_t off0){
    printf("\n[4] announced + conflicting PROBE -> DEFEND with the overlap\n");
    inject(1, off0+4, 8, 0, 0);        // overlaps [off0+4, off0+12)
    { auto f=wait_tx(kDefendBudgetCyc);
      ck("DEFEND emitted promptly", static_cast<long>(f.size()), 60);
      if(f.size()==60){
          ck("msg DEFEND", f[15]&0x0F, 2);
          uint16_t cs=(f[38]<<8)|f[39];
          uint16_t cc=(f[40]<<8)|f[41];
          ck("conflict start = overlap start", cs, off0+4);
          ck("conflict count = overlap size", cc, 4);
      } }
    ck("still ANNOUNCE", dut->state_o, 2);
    ck("defends counted", dut->defends_o, 1);   // 4b makes it 2 later

    printf("\n[4b] DEFEND overlap branch 2: prober's range starts below ours\n");
    inject(1, off0-4, 8, 0, 0);        // our_start inside [off0-4, off0+4]
    { auto f=wait_tx(kDefendBudgetCyc);
      ck("DEFEND emitted (branch 2)", static_cast<long>(f.size()), 60);
      if(f.size()==60){
          uint16_t cs=(f[38]<<8)|f[39];
          uint16_t cc=(f[40]<<8)|f[41];
          ck("conflict start = our start", cs, off0);
          ck("conflict count = overlap", cc, 4);
      } }

    printf("\n[4c] unknown message type ignored\n");
    inject(5, off0, 8, off0, 8);
    cyc(kSettleCyc);
    ck("unknown msg: still ANNOUNCE", dut->state_o, 2);
}

void MaapHarness::ignore_announce_covering_our_request(uint16_t off0){
    printf("\n[5] reference quirk: ANNOUNCE with covering REQUEST is ignored\n");
    inject(3, off0, 8, 0, 0);
    cyc(kSettleCyc);
    ck("no re-address (state ANNOUNCE)", dut->state_o, 2);
    ck("offset unchanged", dut->offset_o, off0);
}

void MaapHarness::readdress_on_conflicting_defend(uint16_t off0){
    printf("\n[6] DEFEND with conflicting CONFLICT fields -> re-address\n");
    inject(2, 0, 0, off0, 8);
    cyc(kSettleCyc);
    ck("back to PROBE", dut->state_o, 1);
    ck("addr dropped", dut->addr_valid_o, 0);
    ck("offset changed", dut->offset_o != off0, 1);
    ck("conflicts counted", dut->conflicts_o, 1);
}

void MaapHarness::readdress_silently_while_probing(){
    printf("\n[7] probing + conflicting PROBE -> silent re-address\n");
    uint16_t off1 = dut->offset_o;
    inject(1, off1, 8, 0, 0);
    cyc(kSettleCyc);
    ck("still PROBE", dut->state_o, 1);
    ck("offset changed again", dut->offset_o != off1, 1);
    ck("conflicts = 2", dut->conflicts_o, 2);
}

void MaapHarness::ignore_disjoint_and_non_pool_pdus(){
    printf("\n[8] non-conflicting + non-pool PDUs ignored\n");
    uint16_t off2 = dut->offset_o;
    inject(1, static_cast<uint16_t>(off2+1000), 8, 0, 0);        // disjoint range
    inject(2, 0, 0, off2, 8, /*conf_pool=*/false);    // wrong pool prefix
    cyc(kSettleCyc);
    ck("offset stable", dut->offset_o, off2);
    ck("conflicts still 2", dut->conflicts_o, 2);
}

void MaapHarness::honour_conflicts_from_any_maap_version(){
    printf("\n[8b] maap_version handling (traceability MAAP-6, IEEE 1722-2016\n"
           "     B.2.3.2: a future-version PDU must STILL count as a conflict\n"
           "     for its ranges; lower/equal versions processed normally)\n");
    {
        // higher version (7): conflicting ANNOUNCE must still re-address —
        // the RX parse is deliberately version-agnostic (ethertype/subtype/
        // msg_type only), so newer talkers keep defending their ranges
        uint16_t offv = dut->offset_o;
        inject(3, 0, 0, offv, 8, /*conf_pool=*/true, /*maap_ver=*/7);
        cyc(kSettleCyc);
        ck("ver7: conflict honored (re-address)", dut->offset_o != offv, 1);
        ck("ver7: conflicts = 3", dut->conflicts_o, 3);
        // version 0 (lower than ours): conflicting DEFEND processed the same
        uint16_t offw = dut->offset_o;
        inject(2, 0, 0, offw, 8, /*conf_pool=*/true, /*maap_ver=*/0);
        cyc(kSettleCyc);
        ck("ver0: conflict honored (re-address)", dut->offset_o != offw, 1);
        ck("ver0: conflicts = 4", dut->conflicts_o, 4);
        // higher version with a DISJOINT range stays ignored (no false
        // conflict from the version bits landing in the wrong cone)
        uint16_t offx = dut->offset_o;
        inject(3, 0, 0, static_cast<uint16_t>(offx+2000), 8, true, 7);
        cyc(kSettleCyc);
        ck("ver7 disjoint: ignored", dut->offset_o, offx);
        ck("ver7 disjoint: conflicts still 4", dut->conflicts_o, 4);
    }
}

void MaapHarness::disable_then_claim_the_seed(){
    printf("\n[9] disable -> IDLE; seeded re-enable claims the seed\n");
    dut->enable_i=0; cyc(5);
    ck("IDLE on disable", dut->state_o, 0);
    dut->seed_offset_i=0x1234; dut->seed_valid_i=1;
    dut->enable_i=1; cyc(3);
    ck("seeded offset", dut->offset_o, 0x1234);
    ck("PROBE with seed", dut->state_o, 1);
}

int MaapHarness::run(){
    bring_up_idle();
    check_reset_idle();
    const uint16_t off0 = claim_offset_through_three_probes();
    check_first_announce_frame(off0);
    defend_the_overlap_against_a_probe(off0);
    ignore_announce_covering_our_request(off0);
    readdress_on_conflicting_defend(off0);
    readdress_silently_while_probing();
    ignore_disjoint_and_non_pool_pdus();
    honour_conflicts_from_any_maap_version();
    disable_then_claim_the_seed();

    printf("\n======================================================================\n");
    printf("KL_maap: %ld checks, %ld failures\n", checks, fails);
#if VM_COVERAGE
    Verilated::threadContextp()->coveragep()->write("coverage.dat");
#endif
    return fails ? 1 : 0;
}

}  // namespace

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    MaapHarness harness;
    return harness.run();
}
