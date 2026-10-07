// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for KL_maap against IEEE 1722-2016 Annex B (#686).
// The standard is the oracle: every check names the clause it grades, and
// mutants.py plants one defect per #686 item and requires its named check to
// fail. Item 1 is B.2.1 (DEFEND destination, control_data_length 16), item 2
// B.3.3 Table B.8 and B.3.4 (strict, random probe and announce intervals,
// for a station MAC that folds the LFSR seed to zero as well), item 3
// B.3.2 Table B.7 notes b and d (ANNOUNCE conflict detection), item 4 Table
// B.7 ReserveAddress!/probetimer!/probeCount! (four PROBEs, the first at
// once). A DEFEND's requested_* fields are not graded: their B.3.6.6 echo is
// a recorded deviation outside #686 (docs/design/MAAP_FABRIC.md).
// Scaled clock: CLK_FREQ_HZ_P=10000 -> 1 ms = 10 cycles.
#include "VKL_maap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#if VM_COVERAGE
#include "verilated_cov.h"
#endif
#include <algorithm>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <set>
#include <vector>

constexpr long kCycPerMs = 10;
// B.3.4.2 and B.3.4.1 open intervals, in scaled cycles
constexpr long kProbeMinCyc = 500 * kCycPerMs;
constexpr long kProbeMaxCyc = 600 * kCycPerMs;
constexpr long kAnnounceMinCyc = 30000 * kCycPerMs;
constexpr long kAnnounceMaxCyc = 32000 * kCycPerMs;
// wait budgets, well past each bound: an interval that breaks its bound is
// then measured and graded by the bound check, not lost to a timeout
constexpr long kProbeBudgetCyc = 2 * kProbeMaxCyc;
constexpr long kAnnounceBudgetCyc = kAnnounceMaxCyc + 10000 * kCycPerMs;
constexpr long kDefendBudgetCyc = 200;
// "at once": event to first accepted beat. Begin! is 3 cycles (enable ->
// PROBE state -> send -> beat), probeCount! 2 after the PROBE's last beat.
constexpr long kAtOnceCyc = 4;
// cycles allowed for an injected PDU to be parsed and acted on
constexpr int kSettleCyc = 50;
// highest offset the RTL can claim: POOL_SIZE_C (0xFE00) - count_i (8)
constexpr uint16_t kMaxOffset = 0xFDF8;
constexpr uint16_t kCount = 8;
constexpr uint64_t kMaapDst = 0x91E0F000FF00ULL;     // Table B.10
constexpr uint64_t kStationMac = 0x020000000001ULL;  // reversed: 01:..:02
// compare_MAC operands (B.3.6.4 compares octet-reversed MACs). kPeerAbove
// reverses to BB:AA:99:88:77:66, above this station, so compare_MAC is TRUE
// and this station keeps its range. kPeerBelow reverses to 00:AA:..:66,
// below it, so this station yields. Unreversed, both are above the station,
// which is what lets a reversal defect show.
constexpr uint64_t kPeerAbove = 0x66778899AABBULL;
constexpr uint64_t kPeerBelow = 0x66778899AA00ULL;
// a station MAC whose two low 16-bit halves XOR to 0xACE1, which folds the
// LFSR's MAC seed to zero (the LFSR's fixed point)
constexpr uint64_t kZeroSeedMac = 0x02000000ACE1ULL;
// timing campaign size: walks restarted by disable/enable
constexpr int kTimingWalks = 150;
constexpr int kAnnounceSamples = 24;
// zero-seed MAC: walks for its probe draws, ANNOUNCEs after the first
constexpr int kZeroSeedWalks = 3;
constexpr int kZeroSeedAnnounces = 4;
// a walk stops counting PROBEs here (a defect could send them forever)
constexpr int kProbeLimit = 8;

namespace {

//! One captured TX frame: wire bytes and the cycles of its first and last
//! accepted beats.
struct Frame {
    std::vector<uint8_t> b;
    long start = 0;
    long end = 0;
    uint64_t at(int pos, int n) const {
        uint64_t v = 0;
        for (int k = 0; k < n; k++) v = (v << 8) | b[pos + k];
        return v;
    }
};

//! What one ReserveAddress! walk put on the wire.
struct Walk {
    int probes = 0;          // PROBEs before the first other frame
    bool announced = false;  // four PROBEs, then an ANNOUNCE at once
    long first = -1;         // event to first PROBE beat, cycles
    long announce = -1;      // the ANNOUNCE's first beat
};

//! The KL_maap harness: the model, the tally and the TX capture state are its
//! members, so nothing this suite mutates lives at file scope (I.2).
class MaapHarness {
 public:
    int run();

 private:
    void ck(const char* t, long got, long exp){
        checks++; if(got!=exp){ fails++; printf("  [FAIL] %-44s got=%ld exp=%ld\n",t,got,exp);}
        else printf("  [ ok ] %-44s = %ld\n",t,got); }

    // One clock. A beat counts as accepted when tvalid and tready are both
    // high as the edge arrives, so tready may be changed between calls.
    void cyc(int n=1){
        for(int i=0;i<n;i++){
            dut->clk_i=0; dut->eval();
            if(dut->m_axis_tvalid && dut->m_axis_tready){
                if(cur.b.empty()) cur.start=now;
                int nb = (dut->m_axis_tkeep==0xFF)?8:4;
                for(int l=0;l<nb;l++) cur.b.push_back((dut->m_axis_tdata>>(8*l))&0xFF);
                if(dut->m_axis_tlast){ cur.end=now; frames.push_back(cur); cur=Frame{}; }
            }
            dut->clk_i=1; dut->eval(); now++;
        }
    }

    // The next frame not yet consumed, waiting up to budget cycles for it.
    bool next(Frame& f, long budget){
        for(long i=0;i<budget && frames.size()<=seen;i++) cyc();
        if(frames.size()<=seen) return false;
        f=frames[seen++];
        return true;
    }

    // inject a MAAP PDU on the RX tap (untagged, 60B padded); maap_version
    // defaults to 1 (byte 16 = version<<3 | cdl[10:8], cdl 16 per B.2.1)
    void inject(uint8_t msg, uint64_t src, uint16_t req_off, uint16_t req_cnt,
                uint16_t conf_off, uint16_t conf_cnt, bool conf_pool=true,
                uint8_t maap_ver=1, bool req_pool=true){
        uint8_t f[64]; memset(f,0,sizeof f);
        for(int k=0;k<6;k++){ f[k]=kMaapDst>>(40-8*k); f[6+k]=src>>(40-8*k); }
        f[12]=0x22; f[13]=0xF0; f[14]=0xFE; f[15]=msg;
        f[16]=static_cast<uint8_t>((maap_ver&0x1F)<<3); f[17]=16;
        if(req_pool){ f[26]=0x91; f[27]=0xE0; f[28]=0xF0; f[29]=0x00; }
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
        rx_end=now;
        dut->rx_tvalid_i=0; dut->rx_tlast_i=0; cyc(3);
    }

    // Figure B.1 frame as B.3.6.5 (PROBE) and B.3.6.7 (ANNOUNCE) build it
    static std::vector<uint8_t> golden(uint8_t msg, uint16_t off){
        std::vector<uint8_t> g(60,0);
        for(int k=0;k<6;k++){ g[k]=kMaapDst>>(40-8*k); g[6+k]=kStationMac>>(40-8*k); }
        g[12]=0x22; g[13]=0xF0; g[14]=0xFE; g[15]=msg;
        g[16]=0x08; g[17]=16;              // maap_version 1, cdl 16 (B.2.1)
        g[26]=0x91; g[27]=0xE0; g[28]=0xF0; g[29]=0x00;
        g[30]=off>>8; g[31]=off&0xFF; g[33]=kCount;
        return g;
    }

    bool frame_is(const Frame& f, uint8_t msg){
        return f.b.size()==60 && (f.b[15]&0x0F)==msg;
    }
    void check_defend(const Frame& f, const char* tag, uint64_t prober,
                      uint16_t cs, uint16_t cc);
    Walk walk(const char* tag, long event, uint16_t off, bool grade);
    void check_walk(const char* tag, const Walk& w);

    void bring_up_idle();
    void check_reset_idle();
    uint16_t acquire_four_probes_then_announce();
    void announce_intervals_and_destination();
    void defend_to_the_prober(uint16_t off0);
    void announce_conflict_detection(uint16_t off0);
    void frame_on_the_wire_keeps_its_range();
    void defend_and_probe_reception();
    void ignore_disjoint_and_non_pool_pdus();
    void honour_conflicts_from_any_maap_version();
    void probe_interval_campaign();
    void disable_then_claim_the_seed();
    std::vector<long> frame_starts(size_t n);
    void zero_seed_mac_draws_random_timers();

    const milan::tb::Model<VKL_maap> model;
    VKL_maap* dut = model.get();
    long checks=0;
    long fails=0;

    long now=0;                    // posedges since construction
    long rx_end=0;                 // cycle of the last injected beat
    long last_announce=0;          // first beat of the latest ANNOUNCE
    std::vector<Frame> frames;     // completed TX frames
    size_t seen=0;                 // frames consumed by next()
    Frame cur;                     // frame being collected
    std::vector<long> probe_iv;    // every observed PROBE interval, cycles
    std::vector<long> announce_iv; // every observed ANNOUNCE interval, cycles
};

void MaapHarness::bring_up_idle(){
    dut->station_mac_i=kStationMac;
    dut->enable_i=0; dut->count_i=kCount;
    dut->seed_offset_i=0; dut->seed_valid_i=0;
    dut->m_axis_tready=1; dut->rx_tvalid_i=0;
    dut->rst_n=0; cyc(6); dut->rst_n=1; cyc(3);

    printf("== KL_maap harness, IEEE 1722-2016 Annex B (10 kHz scaled: 1 ms = 10 cyc) ==\n");
}

void MaapHarness::check_reset_idle(){
    printf("\n[1] reset/idle\n");
    ck("state IDLE", dut->state_o, 0);
    ck("addr not valid", dut->addr_valid_o, 0);
    cyc(kSettleCyc);
    ck("no frame while disabled", static_cast<long>(frames.size()), 0);
}

// One ReserveAddress! walk from `event` (the Begin! or Restart! cycle): the
// first PROBE at once, three retransmissions at the probe timer, then the
// first ANNOUNCE at once. Every PROBE interval is sampled; grade=true also
// grades each frame (the timing campaign passes false and judges in bulk).
Walk MaapHarness::walk(const char* tag, long event, uint16_t off, bool grade){
    char nm[96];
    Walk w;
    long prev=-1;
    Frame f;
    while(w.probes<kProbeLimit && next(f, kProbeBudgetCyc) && frame_is(f,1)){
        if(w.probes==0) w.first=f.start-event;
        if(grade){
            snprintf(nm,sizeof nm,"%s PROBE %d = golden (B.2/B.3.6.5)",tag,w.probes+1);
            ck(nm, f.b==golden(1,off), 1);
            snprintf(nm,sizeof nm,"B.2.1 cdl 16 (%s PROBE %d)",tag,w.probes+1);
            ck(nm, f.at(16,2)&0x7FF, 16);
            snprintf(nm,sizeof nm,"B.2.1 PROBE DA multicast (%s %d)",tag,w.probes+1);
            ck(nm, f.at(0,6)==kMaapDst, 1);
        }
        if(prev>=0) probe_iv.push_back(f.start-prev);
        prev=f.start;
        w.probes++;
        if(grade && w.probes==3)
            ck("address not valid before the fourth PROBE", dut->addr_valid_o, 0);
    }
    // f is the ANNOUNCE only if it was read after the fourth PROBE
    w.announced = w.probes==4 && frame_is(f,3) && seen>=2 &&
                  f.start-frames[seen-2].end<=kAtOnceCyc;
    if(w.announced) w.announce=f.start;
    if(grade && w.announced){
        snprintf(nm,sizeof nm,"%s ANNOUNCE = golden (B.2/B.3.6.7)",tag);
        ck(nm, f.b==golden(3,off), 1);
        snprintf(nm,sizeof nm,"%s: address valid in ANNOUNCE",tag);
        ck(nm, dut->addr_valid_o, 1);
    }
    return w;
}

void MaapHarness::check_walk(const char* tag, const Walk& w){
    char nm[96];
    snprintf(nm,sizeof nm,"T.B7 %s: first PROBE at once",tag);
    ck(nm, w.first>=0 && w.first<=kAtOnceCyc, 1);
    snprintf(nm,sizeof nm,"T.B7 %s: four PROBEs before ANNOUNCE",tag);
    ck(nm, w.probes, 4);
    snprintf(nm,sizeof nm,"T.B7 probeCount!: ANNOUNCE at once (%s)",tag);
    ck(nm, w.announced, 1);
}

uint16_t MaapHarness::acquire_four_probes_then_announce(){
    printf("\n[2] Begin!: four golden PROBEs, the first at once, then ANNOUNCE at once\n");
    dut->enable_i=1;
    const long begin=now;
    cyc(1);
    ck("state PROBE", dut->state_o, 1);
    const uint16_t off0 = dut->offset_o;
    ck("offset inside pool", off0 <= kMaxOffset, 1);
    // [4] and [5] probe ranges up to 8 below and 1000 above it
    ck("offset leaves room for the range cases", off0>=8 && off0<=kMaxOffset-1000, 1);
    const Walk w=walk("Begin!", begin, off0, true);
    check_walk("Begin!", w);
    ck("state ANNOUNCE after four PROBEs", dut->state_o, 2);
    ck("addr = pool base + offset",
       static_cast<long>((dut->addr_o>>16)&0xFFFFFFFF)==0x91E0F000UL &&
       (dut->addr_o&0xFFFF)==off0, 1);
    for(long iv: probe_iv){
        ck("B.3.4.2 probe T > 500 ms", iv>kProbeMinCyc, 1);
        ck("B.3.4.2 probe T < 600 ms", iv<kProbeMaxCyc, 1);
    }
    last_announce=w.announce;
    return off0;
}

void MaapHarness::announce_intervals_and_destination(){
    printf("\n[3] B.3.4.1: ANNOUNCE every 30 s < T < 32 s, randomized, multicast\n");
    Frame f;
    for(int k=0;k<kAnnounceSamples;k++){
        if(!next(f, kAnnounceBudgetCyc) || !frame_is(f,3)){
            ck("ANNOUNCE repeats at the announce timer", 0, 1);
            return;
        }
        announce_iv.push_back(f.start-last_announce);
        last_announce=f.start;
    }
    const auto mm=std::minmax_element(announce_iv.begin(), announce_iv.end());
    printf("  [i]    %zu ANNOUNCE intervals: %ld..%ld cycles\n",
           announce_iv.size(), *mm.first, *mm.second);
    ck("B.3.4.1 announce T > 30 s", *mm.first>kAnnounceMinCyc, 1);
    ck("B.3.4.1 announce T < 32 s", *mm.second<kAnnounceMaxCyc, 1);
    std::set<long> distinct(announce_iv.begin(), announce_iv.end());
    ck("B.3.4.1 announce T randomized", distinct.size()>=3, 1);
    ck("B.2.1 ANNOUNCE DA multicast", f.at(0,6)==kMaapDst, 1);
    ck("B.2.1 cdl 16 (ANNOUNCE)", f.at(16,2)&0x7FF, 16);
}

void MaapHarness::check_defend(const Frame& f, const char* tag, uint64_t prober,
                               uint16_t cs, uint16_t cc){
    char nm[96];
    snprintf(nm,sizeof nm,"%s: DEFEND emitted promptly",tag);
    ck(nm, frame_is(f,2), 1);
    if(!frame_is(f,2)) return;
    snprintf(nm,sizeof nm,"B.2.1 DEFEND DA = PROBE source (%s)",tag);
    ck(nm, f.at(0,6)==prober, 1);
    snprintf(nm,sizeof nm,"B.2.1 cdl 16 (DEFEND %s)",tag);
    ck(nm, f.at(16,2)&0x7FF, 16);
    snprintf(nm,sizeof nm,"%s: SA, ethertype, subtype",tag);
    ck(nm, f.at(6,6)==kStationMac && f.at(12,3)==0x22F0FE, 1);
    snprintf(nm,sizeof nm,"B.2.7 conflict_start = overlap (%s)",tag);
    ck(nm, f.at(34,6), static_cast<long>(0x91E0F0000000ULL|cs));
    snprintf(nm,sizeof nm,"B.2.8 conflict_count = overlap (%s)",tag);
    ck(nm, f.at(40,2), cc);
}

void MaapHarness::defend_to_the_prober(uint16_t off0){
    printf("\n[4] announced + conflicting PROBE -> DEFEND to the prober (B.2.1)\n");
    Frame f;
    inject(1, kPeerAbove, off0+4, 8, 0, 0);       // overlaps [off0+4, off0+8)
    next(f, kDefendBudgetCyc);
    check_defend(f, "above", kPeerAbove, off0+4, 4);
    ck("still ANNOUNCE", dut->state_o, 2);
    ck("defends counted", dut->defends_o, 1);

    printf("\n[4b] the prober's range starts below ours, another prober\n");
    inject(1, kPeerBelow, off0-4, 8, 0, 0);       // overlaps [off0, off0+4)
    next(f, kDefendBudgetCyc);
    check_defend(f, "below", kPeerBelow, off0, 4);

    printf("\n[4c] DEFEND held by backpressure; a later PDU must not redirect it\n");
    constexpr uint64_t kProber = 0x0A0B0C0D0E0FULL;
    dut->m_axis_tready=0;
    inject(1, kProber, off0, 1, 0, 0);            // one-address overlap
    inject(1, 0x111111111111ULL, off0+1000, 8, 0, 0);   // disjoint: no action
    cyc(kSettleCyc);
    dut->m_axis_tready=1;
    next(f, kDefendBudgetCyc);
    ck("B.2.1 DEFEND DA latched at send", frame_is(f,2) && f.at(0,6)==kProber, 1);
    ck("B.2.7 one-address overlap start", f.at(38,2), off0);
    ck("B.2.8 one-address overlap count", f.at(40,2), 1);
    ck("defends = 3", dut->defends_o, 3);

    printf("\n[4d] note b applies to PROBE: adjacent and empty ranges get no DEFEND\n");
    const size_t before=frames.size();
    inject(1, kPeerBelow, off0+kCount, 8, 0, 0);  // adjacent above
    inject(1, kPeerBelow, off0-8, 8, 0, 0);       // adjacent below
    inject(1, kPeerBelow, off0+2, 0, 0, 0);       // empty, inside ours
    cyc(kSettleCyc);
    ck("note b: no DEFEND for non-conflicting PROBEs", static_cast<long>(frames.size()-before), 0);
    ck("defends still 3", dut->defends_o, 3);

    printf("\n[4e] unknown message type ignored (B.2.2)\n");
    inject(5, kPeerBelow, off0, 8, off0, 8);
    cyc(kSettleCyc);
    ck("unknown msg: still ANNOUNCE", dut->state_o, 2);

    printf("\n[4f] the ANNOUNCE after the DEFENDs is multicast again\n");
    ck("B.2.1 ANNOUNCE DA multicast after DEFEND",
       next(f, kAnnounceBudgetCyc) && frame_is(f,3) && f.at(0,6)==kMaapDst, 1);
}

void MaapHarness::announce_conflict_detection(uint16_t off0){
    printf("\n[5] ANNOUNCE conflict detection (B.3.2, Table B.7 notes b and d)\n");
    const long c0=dut->conflicts_o;
    inject(3, kPeerAbove, off0, 8, 0, 0);
    cyc(kSettleCyc);
    ck("T.B7 note d: lower MAC keeps range", dut->offset_o==off0 && dut->state_o==2, 1);
    inject(3, kPeerBelow, off0+1000, 8, off0, 8);
    cyc(kSettleCyc);
    ck("B.2.7 ANNOUNCE conflict_* is not its range", dut->offset_o==off0 && dut->state_o==2, 1);
    inject(3, kPeerBelow, off0+kCount, 8, 0, 0);
    cyc(kSettleCyc);
    ck("note b adjacent above: no conflict", dut->offset_o==off0 && dut->state_o==2, 1);
    inject(3, kPeerBelow, off0-8, 8, 0, 0);
    cyc(kSettleCyc);
    ck("note b adjacent below: no conflict", dut->offset_o==off0 && dut->state_o==2, 1);
    inject(3, kPeerBelow, off0+2, 0, 0, 0);
    cyc(kSettleCyc);
    ck("note b empty range: no conflict", dut->offset_o==off0 && dut->state_o==2, 1);
    ck("no re-address so far", dut->conflicts_o, c0);

    printf("\n[5b] one shared address, peer below: rAnnounce!/DEFEND re-addresses\n");
    inject(3, kPeerBelow, off0+kCount-1, 1, 0, 0);
    const long restart=rx_end;
    ck("T.B7 rAnnounce!/DEFEND: re-address", dut->state_o, 1);
    ck("addr dropped", dut->addr_valid_o, 0);
    const uint16_t off1=dut->offset_o;
    ck("offset changed", off1!=off0, 1);
    ck("conflicts counted", dut->conflicts_o, c0+1);
    Frame f;
    ck("T.B7 Restart!: first PROBE at once",
       next(f, kProbeBudgetCyc) && frame_is(f,1) && f.start-restart<=kAtOnceCyc, 1);
    ck("Restart! PROBE carries the new range", f.b==golden(1,off1), 1);

    printf("\n[5c] ANNOUNCE while probing: rAnnounce!/PROBE yields without compare_MAC\n");
    inject(3, kPeerAbove, off1, 8, 0, 0);
    const long restart2=rx_end;
    const uint16_t off2=dut->offset_o;
    ck("T.B7 rAnnounce!/PROBE: no compare_MAC", off2!=off1 && dut->conflicts_o==c0+2, 1);
    seen=frames.size();                 // keep the walk below to the new range
    check_walk("Restart!", walk("Restart!", restart2, off2, true));
}

void MaapHarness::frame_on_the_wire_keeps_its_range(){
    printf("\n[6] a Restart! while an ANNOUNCE waits on the wire leaves it intact\n");
    const uint16_t off=dut->offset_o;
    dut->m_axis_tready=0;
    for(long i=0;i<kAnnounceBudgetCyc && !dut->m_axis_tvalid;i++) cyc();
    ck("ANNOUNCE requested under backpressure", dut->m_axis_tvalid, 1);
    inject(2, kPeerBelow, 0, 0, off, 8);          // conflicting DEFEND
    ck("DEFEND re-addresses (state PROBE)", dut->state_o, 1);
    const uint16_t fresh=dut->offset_o;
    dut->m_axis_tready=1;
    Frame f;
    next(f, kDefendBudgetCyc);
    ck("frame on the wire keeps its offset", frame_is(f,3) && f.at(30,2)==off, 1);
    ck("then the new range's PROBE",
       next(f, kDefendBudgetCyc) && frame_is(f,1) && f.at(30,2)==fresh, 1);
}

void MaapHarness::defend_and_probe_reception(){
    printf("\n[7] DEFEND judged on conflict_*; PROBE while probing re-addresses silently\n");
    const long c0=dut->conflicts_o;
    uint16_t off=dut->offset_o;
    inject(2, kPeerAbove, off+1000, 8, off, 8);
    cyc(kSettleCyc);
    ck("DEFEND with conflicting conflict_*: re-address", dut->offset_o!=off, 1);
    ck("conflicts +1", dut->conflicts_o, c0+1);
    off=dut->offset_o;
    inject(2, kPeerAbove, off, 8, off+1000, 8);
    cyc(kSettleCyc);
    ck("DEFEND judged on conflict_* only", dut->offset_o, off);
    const long defends=dut->defends_o;
    inject(1, kPeerAbove, off, 8, 0, 0);
    cyc(kSettleCyc);
    ck("probing + PROBE: still PROBE", dut->state_o, 1);
    ck("probing + PROBE: offset changed", dut->offset_o!=off, 1);
    ck("probing + PROBE: no DEFEND", dut->defends_o, defends);
    ck("conflicts +2", dut->conflicts_o, c0+2);
}

void MaapHarness::ignore_disjoint_and_non_pool_pdus(){
    printf("\n[8] non-conflicting + non-pool PDUs ignored\n");
    const long c0=dut->conflicts_o;
    uint16_t off2 = dut->offset_o;
    inject(1, kPeerBelow, static_cast<uint16_t>(off2+1000), 8, 0, 0);    // disjoint
    inject(2, kPeerBelow, 0, 0, off2, 8, /*conf_pool=*/false);           // conflict prefix
    inject(3, kPeerBelow, off2, 8, 0, 0, true, 1, /*req_pool=*/false);  // requested prefix
    cyc(kSettleCyc);
    ck("offset stable", dut->offset_o, off2);
    ck("conflicts unchanged", dut->conflicts_o, c0);
}

void MaapHarness::honour_conflicts_from_any_maap_version(){
    printf("\n[8b] maap_version handling (IEEE 1722-2016 B.2.3.2: a future-version\n"
           "     PDU must STILL count as a conflict for its ranges; lower/equal\n"
           "     versions processed normally)\n");
    const long c0=dut->conflicts_o;
    // higher version (7): conflicting ANNOUNCE must still re-address - the
    // RX parse is deliberately version-agnostic (ethertype/subtype/msg_type)
    uint16_t offv = dut->offset_o;
    inject(3, kPeerBelow, offv, 8, 0, 0, true, 7);
    cyc(kSettleCyc);
    ck("ver7: conflict honored (re-address)", dut->offset_o != offv, 1);
    ck("ver7: conflicts +1", dut->conflicts_o, c0+1);
    // version 0 (lower than ours): conflicting DEFEND processed the same
    uint16_t offw = dut->offset_o;
    inject(2, kPeerBelow, 0, 0, offw, 8, true, 0);
    cyc(kSettleCyc);
    ck("ver0: conflict honored (re-address)", dut->offset_o != offw, 1);
    ck("ver0: conflicts +2", dut->conflicts_o, c0+2);
    // higher version with a DISJOINT range stays ignored
    uint16_t offx = dut->offset_o;
    inject(3, kPeerBelow, static_cast<uint16_t>(offx+2000), 8, 0, 0, true, 7);
    cyc(kSettleCyc);
    ck("ver7 disjoint: ignored", dut->offset_o, offx);
    ck("ver7 disjoint: conflicts still +2", dut->conflicts_o, c0+2);
}

void MaapHarness::probe_interval_campaign(){
    printf("\n[9] B.3.4.2 over %d walks: every PROBE interval strictly inside\n"
           "    500..600 ms, and the draw reaches both ends of 518..581 ms\n", kTimingWalks);
    long worst_first=0;
    int short_walks=0;
    for(int k=0;k<kTimingWalks;k++){
        dut->enable_i=0; cyc(5 + k%7);   // vary the millisecond tick phase
        while(dut->m_axis_tvalid) cyc(); // let a frame already sent finish
        seen=frames.size();
        dut->enable_i=1;
        const long begin=now;
        cyc(1);
        const Walk w=walk("campaign", begin, dut->offset_o, false);
        worst_first=std::max(worst_first, w.first<0 ? kProbeBudgetCyc : w.first);
        if(!w.announced) short_walks++;
    }
    ck("campaign: every walk four PROBEs + ANNOUNCE", short_walks, 0);
    ck("campaign: T.B7 Begin!: first PROBE at once", worst_first<=kAtOnceCyc, 1);
    const auto mm=std::minmax_element(probe_iv.begin(), probe_iv.end());
    printf("  [i]    %zu PROBE intervals: %ld..%ld cycles\n", probe_iv.size(), *mm.first, *mm.second);
    ck("B.3.4.2 probe T > 500 ms (campaign)", *mm.first>kProbeMinCyc, 1);
    ck("B.3.4.2 probe T < 600 ms (campaign)", *mm.second<kProbeMaxCyc, 1);
    ck("probe draw reaches its low end", *mm.first<=520*kCycPerMs, 1);
    ck("probe draw reaches its high end", *mm.second>=580*kCycPerMs, 1);
}

void MaapHarness::disable_then_claim_the_seed(){
    printf("\n[10] disable -> IDLE; seeded re-enable claims the seed at once\n");
    dut->enable_i=0; cyc(5);
    ck("IDLE on disable", dut->state_o, 0);
    ck("addr dropped on disable", dut->addr_valid_o, 0);
    cyc(kSettleCyc);
    seen=frames.size();
    dut->seed_offset_i=0x1234; dut->seed_valid_i=1;
    dut->enable_i=1;
    const long begin=now;
    cyc(3);
    ck("seeded offset", dut->offset_o, 0x1234);
    ck("PROBE with seed", dut->state_o, 1);
    Frame f;
    ck("T.B7 note a: seeded PROBE at once",
       next(f, kProbeBudgetCyc) && f.start-begin<=kAtOnceCyc && f.b==golden(1,0x1234), 1);
}

// The first beats of the next n frames, or fewer if one does not come.
std::vector<long> MaapHarness::frame_starts(size_t n){
    std::vector<long> starts;
    Frame f;
    while(starts.size()<n && next(f, kAnnounceBudgetCyc)){
        if(!frame_is(f, starts.size()<4 ? 1 : 3)) break;   // four PROBEs, then ANNOUNCEs
        starts.push_back(f.start);
    }
    return starts;
}

// B.3.4 wants a random T. Only timer-to-timer intervals are compared: a send
// the timer starts is one cycle after a millisecond tick, so that interval
// is exactly the draw. The at-once sends (the first PROBE, the first
// ANNOUNCE) start at another tick phase, so counting them would let a draw
// frozen at one value pass as random through the phase alone.
void MaapHarness::zero_seed_mac_draws_random_timers(){
    printf("\n[11] B.3.4: a station MAC that folds the LFSR seed to zero\n"
           "     (02:00:00:00:AC:E1) still draws random probe and announce intervals\n");
    dut->enable_i=0; cyc(5);
    while(dut->m_axis_tvalid) cyc();
    dut->station_mac_i=kZeroSeedMac; dut->seed_valid_i=0;
    dut->rst_n=0; cyc(6); dut->rst_n=1; cyc(3);
    cur=Frame{};
    std::vector<long> piv;
    std::vector<long> aiv;
    bool shape=true;
    for(int k=0;k<kZeroSeedWalks;k++){
        const bool last = k==kZeroSeedWalks-1;
        dut->enable_i=0; cyc(5 + k);
        while(dut->m_axis_tvalid) cyc();
        seen=frames.size();
        dut->enable_i=1;
        const size_t want = last ? 5+kZeroSeedAnnounces : 5;
        const std::vector<long> s=frame_starts(want);
        shape = shape && s.size()==want;
        if(s.size()!=want) break;
        piv.push_back(s[2]-s[1]);                  // PROBE 2 -> 3
        piv.push_back(s[3]-s[2]);                  // PROBE 3 -> 4
        for(size_t i=6;i<s.size();i++) aiv.push_back(s[i]-s[i-1]);   // ANNOUNCE 1 -> 2 on
    }
    ck("zero-seed MAC: four PROBEs, then ANNOUNCEs", shape, 1);
    const std::set<long> pd(piv.begin(), piv.end());
    const std::set<long> ad(aiv.begin(), aiv.end());
    printf("  [i]    %zu timer PROBE intervals, %zu distinct; %zu timer ANNOUNCE intervals, %zu distinct\n",
           piv.size(), pd.size(), aiv.size(), ad.size());
    ck("B.3.4.2 probe T in bounds (zero-seed MAC)",
       !pd.empty() && *pd.begin()>kProbeMinCyc && *pd.rbegin()<kProbeMaxCyc, 1);
    ck("B.3.4.2 probe T randomized (zero-seed MAC)", pd.size()>1, 1);
    ck("B.3.4.1 announce T in bounds (zero-seed MAC)",
       !ad.empty() && *ad.begin()>kAnnounceMinCyc && *ad.rbegin()<kAnnounceMaxCyc, 1);
    ck("B.3.4.1 announce T randomized (zero-seed MAC)", ad.size()>1, 1);
}

int MaapHarness::run(){
    bring_up_idle();
    check_reset_idle();
    const uint16_t off0 = acquire_four_probes_then_announce();
    announce_intervals_and_destination();
    defend_to_the_prober(off0);
    announce_conflict_detection(off0);
    frame_on_the_wire_keeps_its_range();
    defend_and_probe_reception();
    ignore_disjoint_and_non_pool_pdus();
    honour_conflicts_from_any_maap_version();
    probe_interval_campaign();
    disable_then_claim_the_seed();
    zero_seed_mac_draws_random_timers();

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
