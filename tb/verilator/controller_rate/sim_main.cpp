// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// GATING regression for the (fixed) CBS datapath bug
// (docs/findings/CBS_DATAPATH_BUG.md): back-to-back frames that classify to
// different queues used to lose ~1 beat each to the wrong queue. Drives an
// alternating tagged(PCP1)/untagged frame pair through the controller and
// checks per-frame byte integrity at egress; exits non-zero on any
// integrity failure (see README.md).
#include "Vcontroller_rate_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <vector>
#include <random>

namespace {
constexpr unsigned kRngSeed = 12345;      // fixed seed: the pacing must replay
constexpr int kResetEdges = 16;           // clock edges held in reset
constexpr int kMtuBytes = 1514;           // one MTU frame
constexpr long kMaxCycles = 8000000;      // simulation length, in clock cycles
constexpr long kStallCycles = 400000;     // no handshake for this long = deadlock

//! Feeds the 802.1Q traffic controller an alternating tagged/untagged frame
//! mix and audits every egressed frame's length and payload bytes.
class ControllerRateHarness {
 public:
    int run();

 private:
    void configure_classifier_and_shaper();
    void hold_in_reset();
    static std::vector<uint8_t> make_frame(bool tagged, int len);
    void build_interference_mix();
    void push_exp(size_t idx);
    bool pump_until_deadlock_or_end();
    void drive_ingress_beat();
    void advance_ingress_feeder();
    void absorb_egress_beat(uint64_t odata, unsigned okraw, bool olast);
    void audit_egressed_frame();
    void report_deadlock(long c);
    int report_integrity_verdict();

    const milan::tb::Model<Vcontroller_rate_wrap> model;
    Vcontroller_rate_wrap* const dut = model.get();
    std::mt19937 rng{kRngSeed};

    // interference-like mix: ACK-sized + MTU frames, alternating queues
    std::vector<std::pair<std::vector<uint8_t>,int>> mix;   // (frame, expected_len)

    long last_prog = 0;
    uint64_t egress_frames=0;
    uint64_t integrity_fails=0;
    uint64_t total_out_bytes=0;
    std::vector<uint8_t> obuf;
    int beat=0;
    size_t mi=0;
    std::vector<uint8_t>* fp=nullptr;
    int flen = 0;
    int nbeats = 0;
    // expected egress: per-queue FIFO of frame lengths, in input order.
    // PCP1(tagged)->q1, untagged->q0 (identity regen + reset PCP_TC + TC_QUEUE=0xE1).
    std::vector<int> expq0;
    std::vector<int> expq1;
};

void ControllerRateHarness::configure_classifier_and_shaper() {
    dut->is_1g_i = 1; dut->cls_use_pcp_i = 1; dut->cls_default_pcp_i = 0;
    dut->cls_pcp_tc_map_i = 0xFAC688; dut->cls_prio_regen_i = 0xFAC688;
    dut->cls_tc_queue_map_i = 0xE1;                  // TC0->q1, TC1->q0
    for (int q = 0; q < 4; q++) {
        dut->cbs_idle_slope_bps_i[q] = (q == 0) ? 10000000u : 0u;
        dut->cbs_hi_credit_bytes_i[q] = 200;
        dut->cbs_lo_credit_bytes_i[q] = static_cast<uint32_t>(-1522);
    }
    dut->cbs_shaped_i = 0x1; dut->m_tready = 1;
}

void ControllerRateHarness::hold_in_reset() {
    dut->resetn = 0;
    for (int i=0;i<kResetEdges;i++){dut->clk=0;dut->eval();dut->clk=1;dut->eval();}
    dut->resetn = 1;
}

// frame factory: tagged(PCP1)/untagged, arbitrary byte length (min 60 = ACK-like)
std::vector<uint8_t> ControllerRateHarness::make_frame(bool tagged, int len) {
    std::vector<uint8_t> f(len);
    for (int i=0;i<len;i++) f[i]=static_cast<uint8_t>(i>>3);
    for (int i=0;i<6;i++){ f[i]=0x68; f[6+i]=0x02; }
    if (tagged){ f[12]=0x81; f[13]=0x00; f[14]=0x20; f[15]=0x02; f[16]=0x08; f[17]=0x00; }
    else       { f[12]=0x08; f[13]=0x00; }
    return f;
}

void ControllerRateHarness::build_interference_mix() {
    constexpr int sizes[] = {
        60, 1514, 60, 60, 1514, 90, 60, 1514, 66, 1514};
    for (int i = 0; i < 10; i++) {
        auto f = make_frame((i & 1) != 0, sizes[i]);
        mix.push_back({f, sizes[i]});
    }
}

void ControllerRateHarness::push_exp(size_t idx) {
    bool tag = (idx & 1) != 0;             // mix[] alternates untagged/tagged
    if (tag) expq1.push_back(static_cast<int>(mix[idx].second));
    else     expq0.push_back(static_cast<int>(mix[idx].second));
}

//! One ingress beat of the frame currently being fed, plus this cycle's
//! egress-ready duty.
void ControllerRateHarness::drive_ingress_beat() {
    uint64_t d=0;
    int vb=0;
    for (int b=0;b<8;b++){ int idx=beat*8+b; if(idx<flen){ d|=static_cast<uint64_t>((*fp)[idx])<<(8*b); vb++; } }
    dut->s_tdata=d; dut->s_tkeep=(vb==8)?0xFF:((1u<<vb)-1);
    dut->s_tvalid=1; dut->s_tlast=(beat==nbeats-1);
    dut->m_tready=((rng()&7)<2);                 // ~25% duty: 1G wire pacing
}

//! An accepted ingress beat: step within the frame, or start the next one.
void ControllerRateHarness::advance_ingress_feeder() {
    if (dut->s_tlast){
        beat=0; mi=(mi+1)%mix.size();
        fp=&mix[mi].first; flen=static_cast<int>(mix[mi].second); nbeats=(flen+7)/8;
        push_exp(mi);
    } else beat++;
}

//! An accepted egress beat: append its valid lanes, and audit on tlast.
void ControllerRateHarness::absorb_egress_beat(uint64_t odata, unsigned okraw, bool olast) {
    for (int b=0; b<8; b++)
        if (okraw & (1<<b)) obuf.push_back(static_cast<uint8_t>((odata >> (8*b)) & 0xFF));
    if (olast){
        audit_egressed_frame();
    }
}

void ControllerRateHarness::audit_egressed_frame() {
    // content check: valid length + payload bytes k>=18 equal (k>>3)
    bool ok = false;
    for (int sz : {60,66,90,1514}) if (static_cast<int>(obuf.size())==sz) ok=true;
    int badk=-1;
    for (size_t k=18; ok && k<obuf.size(); k++)
        if (obuf[k] != static_cast<uint8_t>(k>>3)) { ok=false; badk=static_cast<int>(k); }
    if (!ok) { integrity_fails++;
        if (integrity_fails<=8)
            printf("[bad] frame %llu len=%zu badk=%d got=%d exp=%d\n",
                   static_cast<unsigned long long>(egress_frames), obuf.size(), badk,
                   badk>=0?obuf[badk]:-1, badk>=0?(badk>>3):-1);
    }
    egress_frames++; total_out_bytes += obuf.size();
    obuf.clear();
}

// deadlock detector with sideband state dump
void ControllerRateHarness::report_deadlock(long c) {
    printf("[controller_rate] DEADLOCK at cycle %ld: egress=%llu frames\n"
           "  cls: tq_wr=%u tq_rd=%u pushed=%u fifo_v=%u tqe=%u\n"
           "  shp: grant=%x hasdata=%x allow=%x hold=%u active=%u\n"
           "  q:   dep0=%u dep1=%u q2s_v=%u q2s_r=%u\n",
           c, static_cast<unsigned long long>(egress_frames),
           static_cast<unsigned>(dut->p_tq_wr), static_cast<unsigned>(dut->p_tq_rd),
           static_cast<unsigned>(dut->p_tq_pushed), static_cast<unsigned>(dut->p_fifo_v),
           static_cast<unsigned>(dut->p_tq_empty),
           static_cast<unsigned>(dut->p_grant), static_cast<unsigned>(dut->p_hasdata),
           static_cast<unsigned>(dut->p_allow), static_cast<unsigned>(dut->p_hold),
           static_cast<unsigned>(dut->p_active),
           static_cast<unsigned>(dut->p_dep0), static_cast<unsigned>(dut->p_dep1),
           static_cast<unsigned>(dut->p_q2s_v2), static_cast<unsigned>(dut->p_q2s_r2));
}

//! Runs the wire until the cycle budget is spent. False = the deadlock
//! detector fired and has already dumped the sideband state.
bool ControllerRateHarness::pump_until_deadlock_or_end() {
    for (long c=0;c<kMaxCycles;c++) {
        drive_ingress_beat();
        // sample handshakes PRE-EDGE (settled comb state = what the posedge commits);
        // post-edge sampling mis-advances the feeder and fabricates beat loss
        dut->clk=0; dut->eval();
        bool in_hs  = dut->s_tvalid && dut->s_tready;
        bool out_hs = dut->m_tvalid && dut->m_tready;
        bool olast  = dut->m_tlast;
        uint64_t odata = dut->m_tdata;
        unsigned okraw = static_cast<unsigned>(dut->m_tkeep);
        dut->clk=1; dut->eval();
        if (in_hs) {
            advance_ingress_feeder();
        }
        if (out_hs) {
            absorb_egress_beat(odata, okraw, olast);
        }
        if (out_hs || in_hs) last_prog = c;
        if (c - last_prog > kStallCycles) {
            report_deadlock(c);
            return false;
        }
    }
    return true;
}

int ControllerRateHarness::report_integrity_verdict() {
    printf("[controller_rate] egress=%llu frames, %llu bytes, integrity_fails=%llu\n",
           static_cast<unsigned long long>(egress_frames),
           static_cast<unsigned long long>(total_out_bytes),
           static_cast<unsigned long long>(integrity_fails));
    // The sweep totals checks by reading a summary line out of this log
    // (scripts/suite_tally.py). Without one this suite contributed a
    // structural ZERO to the headline figure while actually integrity-checking
    // every egressed frame - indistinguishable, from the outside, from a
    // harness that asserts nothing. One egressed frame = one length+payload
    // verdict, which is exactly what integrity_fails counts against.
    printf("controller_rate: %llu checks, %llu failures\n",
           static_cast<unsigned long long>(egress_frames),
           static_cast<unsigned long long>(integrity_fails));
    if (integrity_fails)
        printf("[controller_rate] REPRODUCED the OPEN classifier tdest bug "
               "(docs/findings/CBS_DATAPATH_BUG.md) — %llu frames egressed short.\n",
               static_cast<unsigned long long>(integrity_fails));
    else
        printf("[controller_rate] no integrity failures — bug appears FIXED; "
               "flip this harness to gating (return integrity_fails?1:0).\n");
    return integrity_fails ? 1 : 0;   // gating since the 2026-07-05 classifier fix
}

int ControllerRateHarness::run() {
    configure_classifier_and_shaper();
    hold_in_reset();
    build_interference_mix();
    obuf.reserve(kMtuBytes);     // one MTU frame; clear() below keeps the capacity
    fp=&mix[0].first;
    flen = static_cast<int>(mix[0].second);
    nbeats = (flen+7)/8;
    push_exp(0);
    if (!pump_until_deadlock_or_end()) {
        return 2;
    }
    return report_integrity_verdict();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    ControllerRateHarness harness;
    return harness.run();
}
