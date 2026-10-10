// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for KL_maap against IEEE 1722-2016 Annex B (#686).
// The standard is the oracle: every check names the clause it grades, and
// mutants.py plants one defect per #686 item and requires its named check to
// fail. Item 1 is B.2.1 (DEFEND destination, control_data_length 16), item 2
// B.3.3 Table B.8 and B.3.4 (strict, random probe and announce intervals,
// for a station MAC whose MAC-plus-clock seed is zero as well), item 3
// B.3.2 Table B.7 notes b and d (ANNOUNCE conflict detection), item 4 Table
// B.7 ReserveAddress!/probetimer!/probeCount! (four PROBEs, the first at
// once). #696 also grades the DEFEND requested-range echo (B.3.6.6) and the
// first Begin! claims of equally timed stations (B.3.4 NOTE, B.3.6.1): on
// the wire for sampled pairs, and for every seed through first-draw maps
// learned from the RTL.
// Scaled clock: CLK_FREQ_HZ_P=10000 -> 1 ms = 10 cycles.
#include "VKL_maap.h"
#include "VKL_maap___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#if VM_COVERAGE
#include "verilated_cov.h"
#endif
#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
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
// Its first Begin! offset at clock 0 leaves room for the range fixtures.
constexpr uint64_t kStationMac = 0x020000001001ULL;  // reversed: 01:10:..:02
// compare_MAC operands (B.3.6.4 compares octet-reversed MACs). kPeerAbove
// reverses to BB:AA:99:88:77:66, above this station, so compare_MAC is TRUE
// and this station keeps its range. kPeerBelow reverses to 00:AA:..:66,
// below it, so this station yields. Unreversed, both are above the station,
// which is what lets a reversal defect show.
constexpr uint64_t kPeerAbove = 0x66778899AABBULL;
constexpr uint64_t kPeerBelow = 0x66778899AA00ULL;
// A unicast MAC whose low 32 bits sum with clock zero to the fixed point.
constexpr uint64_t kZeroSeedMac = 0x020000000000ULL;
// The unicast prefix of the first-claim stations; their low 32 bits carry the seed.
constexpr uint64_t kMacBase = 0x020000000000ULL;
// first-draw linearity samples, and the tries to find an unambiguous pair
constexpr int kLinearitySamples = 256;
constexpr int kColumnTries = 64;
// timing campaign size: walks restarted by disable/enable
constexpr int kTimingWalks = 150;
constexpr int kAnnounceSamples = 24;
// zero-seed MAC: walks for its probe draws, ANNOUNCEs after the first
constexpr int kZeroSeedWalks = 3;
constexpr int kZeroSeedAnnounces = 4;
// a walk stops counting PROBEs here (a defect could send them forever)
constexpr int kProbeLimit = 8;
// A link outage longer than a whole walk (the at-once PROBE, three probe
// intervals under 600 ms, the at-once ANNOUNCE), so a walk restarted at
// the loss would end before the return
constexpr long kOutageCyc = 4 * kProbeMaxCyc;

namespace {

//! One captured TX frame: wire bytes and the cycles of its first and last
//! accepted beats.
struct Frame {
    std::vector<uint8_t> b;
    long start = 0;
    long end = 0;
    uint64_t at(int pos, int n) const {
        // A missing or short frame is a failed comparison, never an invalid read.
        if (pos < 0 || n < 0 || static_cast<size_t>(pos + n) > b.size())
            return UINT64_MAX;
        uint64_t v = 0;
        for (int k = 0; k < n; k++) v = (v << 8) | b[pos + k];
        return v;
    }
};

//! What one station claimed at its first Begin!.
struct FirstClaim {
    long start = -1;     // the first PROBE's requested_start, -1 if none
    long interval = -1;  // first PROBE to second PROBE, cycles, -1 if unmeasured
};

//! Two equally timed stations: a MAC and a clock each.
struct StationPair {
    uint64_t mac_a;
    uint64_t mac_b;
    uint32_t clock_a;
    uint32_t clock_b;
};

//! A first-draw value and a seed the RTL maps onto it.
struct SeedImage {
    uint32_t value = 0;
    uint32_t seed = 0;
};
//! Row-echelon basis of a learned map's image: entry b has top bit b.
using ImageBasis = std::array<SeedImage, 32>;
//! A learned GF(2)-linear map of the seed: column k is the image of bit k.
using SeedMap = std::array<uint32_t, 32>;

//! Learn a linear map of the seed from the RTL: column k is the XOR of two
//! observations whose seeds differ in bit k only. `observe` returns -1 where
//! it cannot tell the value; a zero seed (the fallback) is never observed.
template <typename Observe>
bool learn_seed_map(SeedMap& map, uint32_t sample, Observe observe) {
    for (unsigned k=0;k<map.size();++k) {
        bool found=false;
        for (int t=0;t<kColumnTries && !found;++t) {
            sample=sample*1664525u+1013904223u;
            const uint32_t other=sample^(uint32_t{1}<<k);
            if (!sample || !other) continue;
            const long a=observe(sample);
            const long b=observe(other);
            if (a<0 || b<0) continue;
            map[k]=static_cast<uint32_t>(a^b);
            found=true;
        }
        if (!found) return false;
    }
    return true;
}

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
        if(frames.size()<=seen){ f=Frame{}; return false; }
        f=frames[seen++];
        return true;
    }

    // inject a MAAP PDU on the RX tap (untagged, 60B padded); maap_version
    // defaults to 1 (byte 16 = version<<3 | cdl[10:8], cdl 16 per B.2.1)
    void inject(uint8_t msg, uint64_t src, uint16_t req_off, uint16_t req_cnt,
                uint16_t conf_off, uint16_t conf_cnt, bool conf_pool=true,
                uint8_t maap_ver=1, bool req_pool=true, unsigned length=60,
                int missing_byte=-1, bool deliver=true){
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
        const int beats=static_cast<int>((length+7)/8);
        for(int b=0;b<beats;b++){
            uint64_t v=0;
            for(int j=0;j<8;j++) v|=static_cast<uint64_t>(f[b*8+j])<<(8*j);
            const unsigned bytes=std::min(8u, length-static_cast<unsigned>(b)*8);
            unsigned keep=(1u<<bytes)-1;
            if (missing_byte>=b*8 && missing_byte<(b+1)*8)
                keep &= ~(1u<<(missing_byte-b*8));
            dut->rx_tdata_i=v; dut->rx_tkeep_i=keep;
            dut->rx_tvalid_i=deliver; dut->rx_tready_i=1; dut->rx_tlast_i=(b==beats-1);
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
    void probe_mid_frame_is_defended();
    void frame_on_the_wire_keeps_its_range();
    void defend_and_probe_reception();
    void ignore_disjoint_and_non_pool_pdus();
    void honour_conflicts_from_any_maap_version();
    void probe_interval_campaign();
    void disable_then_claim_the_seed();
    std::vector<long> frame_starts(size_t n);
    void zero_seed_mac_draws_random_timers();
    void compare_mac_remaining_cells();
    void pending_response_cancelled();
    void port_return_reprobes();
    void port_loss_is_no_event();
    void supplied_seed_bounds();
    void truncated_pdus_have_no_effect();
    void generator_period_and_seed();
    FirstClaim first_claim(uint64_t mac, uint32_t clock, bool interval);
    bool claims_disjoint(const std::vector<StationPair>& pairs);
    bool claims_differ(const std::vector<StationPair>& pairs);
    bool intervals_differ(const std::vector<StationPair>& pairs);
    void first_claims_of_equally_timed_stations();
    uint16_t seeded_first_offset(uint32_t seed, uint8_t count);
    long seeded_first_probe_draw(uint32_t seed);
    static bool insert_image(ImageBasis& basis, SeedImage image, uint32_t& kernel);
    static int image_rank(const SeedMap& map, unsigned first, unsigned last);
    void first_draws_for_every_seed();
    using GeneratorMap = std::array<uint32_t, 32>;
    static uint32_t apply_generator_map(const GeneratorMap& map, uint32_t state);
    static uint32_t jump_generator(GeneratorMap map, uint32_t state, uint64_t steps);
    uint32_t generator_step(uint32_t state);

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
    dut->realtime_ns_i=0;
    dut->enable_i=0; dut->count_i=kCount; dut->port_operational_i=1;
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
    ck("M2 B.3.6.6 requested start echoes PROBE", f.at(26,6),
       static_cast<long>(0x91E0F0000000ULL | (off0+4)));
    ck("still ANNOUNCE", dut->state_o, 2);
    ck("defends counted", dut->defends_o, 1);

    printf("\n[4b] the prober's range starts below ours, another prober\n");
    inject(1, kPeerBelow, off0-4, 8, 0, 0);       // overlaps [off0, off0+4)
    next(f, kDefendBudgetCyc);
    check_defend(f, "below", kPeerBelow, off0, 4);
    // The only fixture whose PROBE starts below ours: the echo and the
    // overlap start differ here, and anywhere else they coincide.
    ck("M2 B.3.6.6 requested start echoes a PROBE starting below ours", f.at(26,6),
       static_cast<long>(0x91E0F0000000ULL | static_cast<uint16_t>(off0-4)));

    printf("\n[4c] DEFEND held by backpressure; a later PDU must not redirect it\n");
    constexpr uint64_t kProber = 0x0A0B0C0D0E0FULL;
    dut->m_axis_tready=0;
    inject(1, kProber, off0+7, 0x1234, 0, 0);     // one-address overlap
    inject(1, 0x111111111111ULL, off0+1000, 8, 0, 0);   // disjoint: no action
    cyc(kSettleCyc);
    dut->m_axis_tready=1;
    next(f, kDefendBudgetCyc);
    ck("B.2.1 DEFEND DA latched at send", frame_is(f,2) && f.at(0,6)==kProber, 1);
    ck("B.2.7 one-address overlap start", f.at(38,2), off0+7);
    ck("M2 B.3.6.6 requested count echoes all 16 bits", f.at(32,2), 0x1234);
    ck("M2 requested start held under backpressure", f.at(30,2), off0+7);
    ck("B.2.8 one-address overlap count", f.at(40,2), 1);
    ck("defends = 3", dut->defends_o, 3);

    // The response buffer is occupied throughout a stalled DEFEND.
    // A further conflicting PROBE must not rewrite that frame.
    for (int accepted : {0,2,4,7}) {
        dut->m_axis_tready=0;
        inject(1, kProber, off0+1, 0x1234, 0, 0);
        cyc(kSettleCyc);
        dut->m_axis_tready=1; cyc(accepted); dut->m_axis_tready=0;
        inject(1, kPeerAbove, off0+3, 0x2345, 0, 0);
        cyc(kSettleCyc);
        dut->m_axis_tready=1;
        next(f, kDefendBudgetCyc);
        ck("M6 occupied response buffer preserves active DEFEND",
           frame_is(f,2) && f.at(0,6)==kProber && f.at(30,2)==off0+1
           && f.at(32,2)==0x1234 && f.at(38,2)==off0+1 && f.at(40,2)==7,1);
    }
    const long after_busy=dut->defends_o;


    printf("\n[4d] note b applies to PROBE: adjacent and empty ranges get no DEFEND\n");
    const size_t before=frames.size();
    inject(1, kPeerBelow, off0+kCount, 8, 0, 0);  // adjacent above
    inject(1, kPeerBelow, off0-8, 8, 0, 0);       // adjacent below
    inject(1, kPeerBelow, off0+2, 0, 0, 0);       // empty, inside ours
    cyc(kSettleCyc);
    ck("note b: no DEFEND for non-conflicting PROBEs", static_cast<long>(frames.size()-before), 0);
    ck("non-conflicting PROBEs leave defends unchanged", dut->defends_o, after_busy);

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

void MaapHarness::probe_mid_frame_is_defended(){
    printf("\n[6a] a conflicting PROBE parsed while an ANNOUNCE is part-way out on the\n"
           "     wire leaves that frame byte-identical and gets a deferred DEFEND\n");
    for (int accepted : {0,2,7}) {
    const uint16_t off=dut->offset_o;
    const long defends=dut->defends_o;
    const long c0=dut->conflicts_o;
    dut->m_axis_tready=0;
    for(long i=0;i<kAnnounceBudgetCyc && !dut->m_axis_tvalid;i++) cyc();
    ck("ANNOUNCE requested under backpressure", dut->m_axis_tvalid, 1);
    dut->m_axis_tready=1; cyc(accepted); dut->m_axis_tready=0;   // two beats out, then stall
    const size_t before=frames.size();
    inject(1, kPeerAbove, off+2, 0x1234, 0, 0);   // conflicting PROBE, mid-frame
    inject(1, kPeerBelow, off+3, 8, 0, 0);       // occupied response keeps first PROBE
    cyc(kSettleCyc);
    dut->m_axis_tready=1;
    Frame f;
    next(f, kDefendBudgetCyc);
    ck("PROBE mid-frame: frame on the wire byte-identical", frame_is(f,3) && f.b==golden(3,off), 1);
    const bool defended=next(f,kDefendBudgetCyc) && frame_is(f,2);
    ck("M6 busy PROBE gets DEFEND after wire is free",defended,1);
    ck("M6 pending response preserves prober and requested range",
       defended && f.at(0,6)==kPeerAbove && f.at(30,2)==off+2
       && f.at(32,2)==0x1234 && f.at(38,2)==off+2 && f.at(40,2)==6,1);
    cyc(kSettleCyc);
    ck("M6 pending response sent exactly once",static_cast<long>(frames.size()-before),2);
    ck("PROBE mid-frame: deferred DEFEND counted",dut->defends_o,defends+1);
    ck("PROBE mid-frame: range kept",
       dut->state_o==2 && dut->offset_o==off && dut->conflicts_o==c0, 1);
    }
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
    inject(1, kPeerBelow, off, 8, 0, 0);
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
    // note b holds for this station's own block too: count_i 0 claims nothing
    dut->count_i=0;
    inject(1, kPeerBelow, static_cast<uint16_t>(off2>=4 ? off2-4 : 0), 8, 0, 0);  // straddles off2
    cyc(kSettleCyc);
    dut->count_i=kCount;
    ck("note b: this station's empty range never conflicts",
       dut->offset_o==off2 && dut->conflicts_o==c0, 1);
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
    ck("campaign: observed PROBE intervals", !probe_iv.empty(), 1);
    if(probe_iv.empty()) return;
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
    printf("\n[11] B.3.4: a station MAC whose seed with clock 0 is zero\n"
           "     (02:00:00:00:00:00) still draws random probe and announce intervals\n");
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

void MaapHarness::compare_mac_remaining_cells(){
    dut->station_mac_i=kStationMac;
    for (unsigned state : {1u, 2u}) {
        bool keeps=true;
        bool yields=true;
        for (auto peer : {kPeerAbove,kPeerBelow,kStationMac}) {
            dut->enable_i=0; cyc(20); seen=frames.size();
            dut->seed_valid_i=1; dut->seed_offset_i=0x100;
            dut->enable_i=1;
            Frame frame;
            const unsigned nframes=state==1 ? 1 : 5;
            for (unsigned n=0;n<nframes;++n)
                keeps &= next(frame,kProbeBudgetCyc);
            const unsigned conflicts=dut->conflicts_o;
            inject(state==1 ? 1 : 2,peer,0x100,8,0x100,8);
            cyc(kSettleCyc);
            if (peer==kPeerAbove)
                keeps &= dut->state_o==state && dut->offset_o==0x100
                         && dut->conflicts_o==conflicts;
            else
                yields &= dut->state_o==1 && dut->conflicts_o==conflicts+1;
        }
        ck(state==1 ? "M1 rProbe/PROBE lower MAC keeps range"
                    : "M1 rDefend/DEFEND lower MAC keeps range", keeps,1);
        ck(state==1 ? "M1 rProbe/PROBE higher or equal MAC yields"
                    : "M1 rDefend/DEFEND higher or equal MAC yields", yields,1);
    }
    dut->seed_valid_i=0;
}

void MaapHarness::pending_response_cancelled(){
    bool cancelled=true;
    for (unsigned action=0;action<4;++action) {
        dut->enable_i=0; dut->rst_n=0; dut->m_axis_tready=1;
        dut->port_operational_i=1; cyc(6);
        dut->station_mac_i=kStationMac; dut->count_i=kCount;
        dut->seed_valid_i=1; dut->seed_offset_i=0x100;
        dut->rst_n=1; cyc(3); dut->enable_i=1;
        frames.clear(); cur=Frame{}; seen=0;
        Frame frame;
        for (unsigned n=0;n<5;++n) cancelled &= next(frame,kProbeBudgetCyc);
        dut->m_axis_tready=0;
        for (long n=0;n<kAnnounceBudgetCyc && !dut->m_axis_tvalid;++n) cyc();
        inject(1,kPeerAbove,0x102,8,0,0);
        if (action==0) { dut->enable_i=0; cyc(2); dut->enable_i=1; }
        if (action==1) { dut->port_operational_i=0; cyc(2); dut->port_operational_i=1; }
        if (action==2) inject(3,kPeerBelow,0x100,8,0,0);
        if (action==3) { dut->rst_n=0; cyc(2); dut->rst_n=1; }
        frames.clear(); seen=0; dut->m_axis_tready=1;
        cyc(20000); // Includes a full new four-PROBE walk and deferred sends.
        cancelled &= dut->state_o==2 && dut->defends_o==0;
        for (const auto& emitted : frames) cancelled &= !frame_is(emitted,2);
    }
    ck("M6 pending response cancelled with allocation",cancelled,1);
    dut->seed_valid_i=0;
}

void MaapHarness::port_return_reprobes(){
    for (unsigned state : {1u,2u}) {
        dut->enable_i=0; dut->port_operational_i=1; cyc(20);
        seen=frames.size(); dut->enable_i=1;
        Frame frame;
        const unsigned nframes=state==1 ? 1 : 5;
        bool valid=true;
        for (unsigned n=0;n<nframes;++n) valid &= next(frame,kProbeBudgetCyc);
        const unsigned conflicts=dut->conflicts_o;
        dut->port_operational_i=0; cyc(8);
        const long event=now;
        dut->port_operational_i=1; cyc();
        valid &= dut->state_o==1 && !dut->addr_valid_o;
        seen=frames.size();
        const Walk restarted=walk("PortOperational",event,dut->offset_o,false);
        valid &= restarted.probes==4 && restarted.announced && restarted.first<=kAtOnceCyc;
        valid &= dut->conflicts_o==conflicts;
        ck(state==1 ? "M5 B.3.5.9 link return restarts PROBE"
                    : "M5 B.3.5.9 link return revokes and reprobes",valid,1);
        cyc(kSettleCyc);
        ck("M5 stable operational level does not restart",dut->state_o,2);
    }
}

// B.3.5.9 makes entering the operational state the event; Table B.3 names
// none for leaving it, so the walk in progress carries on through an
// outage. The outage outlasts a whole walk: a restart taken at the loss
// would finish before the return, so only a restart at the return passes.
void MaapHarness::port_loss_is_no_event(){
    bool held=true;
    for (unsigned state : {1u,2u}) {
        dut->enable_i=0; dut->port_operational_i=1; cyc(20);
        seen=frames.size(); dut->enable_i=1;
        Frame frame;
        const unsigned nframes=state==1 ? 1 : 5;
        for (unsigned n=0;n<nframes;++n) held &= next(frame,kProbeBudgetCyc);
        const uint16_t off=dut->offset_o;
        const unsigned conflicts=dut->conflicts_o;
        const size_t before=frames.size();
        dut->port_operational_i=0;
        const long loss=now;
        cyc(kOutageCyc);
        // Only the rest of the walk in progress, on its own range: three
        // timer PROBEs and the ANNOUNCE from PROBE, nothing from ANNOUNCE.
        int probes=0;
        int announces=0;
        for (size_t n=before;n<frames.size();++n) {
            probes += frame_is(frames[n],1);
            announces += frame_is(frames[n],3);
            held &= frames[n].start-loss>kAtOnceCyc && frames[n].at(30,2)==off;
        }
        held &= probes==(state==1 ? 3 : 0) && announces==(state==1 ? 1 : 0);
        held &= frames.size()-before==static_cast<size_t>(probes+announces);
        held &= dut->state_o==2 && dut->offset_o==off && dut->conflicts_o==conflicts;
        const long event=now;
        dut->port_operational_i=1; cyc();
        held &= dut->state_o==1 && !dut->addr_valid_o;
        seen=frames.size();
        const Walk restarted=walk("PortOperational",event,dut->offset_o,false);
        held &= restarted.probes==4 && restarted.announced
                && restarted.first>=0 && restarted.first<=kAtOnceCyc;
        held &= dut->conflicts_o==conflicts;
    }
    ck("M5 B.3.5.9 link loss is no event; return reprobes",held,1);
}

void MaapHarness::supplied_seed_bounds(){
    bool valid_kept=true;
    bool invalid_refused=true;
    for (unsigned count : {1u, 8u, 255u}) {
        dut->count_i=count;
        const unsigned limit=0xfe00-count;
        for (unsigned seed : {0u, limit, limit+1, 0xfe00u, 0xff00u, 0xffffu}) {
            dut->enable_i=0; cyc(20);
            seen=frames.size();
            dut->seed_valid_i=1; dut->seed_offset_i=seed;
            dut->enable_i=1; cyc(20);
            const unsigned got=dut->offset_o;
            if (seed<=limit) valid_kept &= got==seed;
            else invalid_refused &= got<=limit && got!=seed;
        }
    }
    ck("M7 Table B.9 valid supplied boundary retained", valid_kept, 1);
    ck("M7 Table B.9 invalid supplied range refused", invalid_refused, 1);
    dut->count_i=kCount; dut->seed_valid_i=0;
}

void MaapHarness::truncated_pdus_have_no_effect(){
    // Compare an idle RX tap with identical cycles carrying malformed PDUs.
    // Equal complete output frames and deadlines prove timer/TX noninterference.
    for (unsigned state : {1u, 2u}) {
        std::vector<Frame> reference;
        long origin=0;
        bool no_effect=true;
        for (bool deliver : {false, true}) {
            dut->enable_i=0; dut->rst_n=0; cyc(6);
            dut->station_mac_i=kStationMac;
            dut->count_i=kCount; dut->seed_valid_i=1; dut->seed_offset_i=0x100;
            dut->rst_n=1; cyc(3); dut->enable_i=1;
            frames.clear(); cur=Frame{}; seen=0;
            Frame f;
            const unsigned initial_frames=state==1 ? 1 : 5;
            for (unsigned n=0;n<initial_frames;++n)
                no_effect &= next(f,kProbeBudgetCyc);
            origin=now;
            frames.clear(); seen=0;
            for (unsigned type : {1u, 2u, 3u}) {
                for (unsigned length=1;length<42;++length)
                    inject(type,kPeerBelow,0x100,8,0x100,8,true,1,true,
                           length,-1,deliver);
                // Full frame length cannot hide a missing required byte.
                for (int missing=0;missing<42;++missing)
                    inject(type,kPeerBelow,0x100,8,0x100,8,true,1,true,
                           60,missing,deliver);
            }
            no_effect &= dut->state_o==state && dut->offset_o==0x100;
            no_effect &= dut->conflicts_o==0 && dut->defends_o==0;
            // Observe the next timer event, without injecting a receive event.
            seen=frames.size();
            no_effect &= next(f,state==1 ? kProbeBudgetCyc : kAnnounceBudgetCyc);
            for (auto& frame : frames) { frame.start-=origin; frame.end-=origin; }
            if (!deliver) reference=frames;
            else {
                no_effect &= frames.size()==reference.size();
                for (size_t n=0;n<std::min(frames.size(),reference.size());++n)
                    no_effect &= frames[n].b==reference[n].b
                        && frames[n].start==reference[n].start
                        && frames[n].end==reference[n].end;
            }
        }
        ck(state==1 ? "M8 B.2 truncated PROBE-state input has no effect"
                    : "M8 B.2 truncated DEFEND-state input has no effect", no_effect,1);
    }
}

// Learn one-step transitions by clocking the RTL, then check the order of
// its linear map. For N = 2^32 - 1, N's prime factors are 3, 5, 17, 257,
// and 65537. Returning after N steps and after none of N/q proves that the
// seed-1 orbit has exactly N states, covering every nonzero 32-bit state.
uint32_t MaapHarness::apply_generator_map(const GeneratorMap& map, uint32_t state) {
    uint32_t result=0;
    for (unsigned bit=0;bit<map.size();++bit)
        if (state & (uint32_t{1}<<bit)) result ^= map[bit];
    return result;
}

uint32_t MaapHarness::jump_generator(GeneratorMap map, uint32_t state, uint64_t steps) {
    while (steps) {
        if (steps & 1) state=apply_generator_map(map,state);
        GeneratorMap squared{};
        for (unsigned bit=0;bit<map.size();++bit)
            squared[bit]=apply_generator_map(map,map[bit]);
        map=squared;
        steps >>= 1;
    }
    return state;
}

uint32_t MaapHarness::generator_step(uint32_t state) {
    dut->rootp->KL_maap__DOT__lfsr_r=state;
    cyc();
    return dut->rootp->KL_maap__DOT__lfsr_r;
}

void MaapHarness::generator_period_and_seed() {
    bring_up_idle();
    GeneratorMap map{};
    for (unsigned bit=0;bit<map.size();++bit)
        map[bit]=generator_step(uint32_t{1}<<bit);
    bool linear=true;
    for (uint32_t state : {0u,1u,0x12345678u,UINT32_MAX,0x80000001u})
        linear &= generator_step(state)==apply_generator_map(map,state);
    uint32_t sample=0x9e3779b9u;
    for (unsigned i=0;i<128;++i) {
        sample=sample*1664525u+1013904223u;
        linear &= generator_step(sample)==apply_generator_map(map,sample);
    }
    bool maximal=linear && jump_generator(map,1,UINT32_MAX)==1;
    for (uint32_t factor : {3u,5u,17u,257u,65537u})
        maximal &= jump_generator(map,1,UINT32_MAX/factor)!=1;
    ck("M3 B.3.6.1 generator period is 2^32-1",maximal,1);

    struct SeedCase { uint64_t mac; uint32_t clock; };
    const std::array<SeedCase,5> seeds{{
        {0x020000000000ULL,0},
        {kStationMac,17},
        {0x020012345678ULL,0x01020304u},
        {0x0200ffffffffULL,1},
        {0x020000000000ULL,0xffff1234u},
    }};
    bool seeded=true;
    bool continuous=true;
    for (const auto& test : seeds) {
        bring_up_idle();
        dut->station_mac_i=test.mac;
        dut->realtime_ns_i=test.clock;
        dut->enable_i=1;
        cyc();
        uint32_t observed=dut->rootp->KL_maap__DOT__lfsr_r;
        const uint32_t expected=static_cast<uint32_t>(test.mac+test.clock);
        seeded &= expected ? observed==expected : observed!=0;
        // First enable is the seeding boundary. A later Release!/Begin!
        // continues the generator even if the MAC and clock have changed.
        dut->station_mac_i=test.mac ^ 0x000100000001ULL;
        dut->realtime_ns_i=test.clock+32;
        dut->enable_i=0;
        cyc();
        continuous &= dut->rootp->KL_maap__DOT__lfsr_r==apply_generator_map(map,observed);
        observed=dut->rootp->KL_maap__DOT__lfsr_r;
        dut->enable_i=1;
        cyc();
        continuous &= dut->rootp->KL_maap__DOT__lfsr_r==apply_generator_map(map,observed);
    }
    ck("M3 B.3.6.1 first enable seeds MAC plus clock",seeded,1);
    ck("M3 Release/Begin retains the generator sequence",continuous,1);
}

// One station from reset. Every station resets, samples its MAC and clock
// and enables on the same cycles, so only the MAC and the clock separate
// equally timed stations (B.3.4 NOTE).
FirstClaim MaapHarness::first_claim(uint64_t mac, uint32_t clock, bool interval){
    dut->enable_i=0; dut->rst_n=0; cyc(6);
    dut->station_mac_i=mac; dut->realtime_ns_i=clock;
    dut->count_i=kCount; dut->seed_valid_i=0; dut->port_operational_i=1;
    dut->m_axis_tready=1; dut->rx_tvalid_i=0;
    dut->rst_n=1; cyc(3);
    frames.clear(); cur=Frame{}; seen=0;
    dut->enable_i=1;
    FirstClaim claim;
    Frame probe;
    if(!next(probe,kProbeBudgetCyc) || !frame_is(probe,1)) return claim;
    claim.start=static_cast<long>(probe.at(30,2));
    Frame retransmission;
    if(interval && next(retransmission,kProbeBudgetCyc) && frame_is(retransmission,1))
        claim.interval=retransmission.start-probe.start;
    return claim;
}

// Table B.7 note b: two blocks of kCount addresses conflict when they share one.
bool MaapHarness::claims_disjoint(const std::vector<StationPair>& pairs){
    bool disjoint=true;
    for(const auto& p : pairs){
        const FirstClaim a=first_claim(p.mac_a,p.clock_a,false);
        const FirstClaim b=first_claim(p.mac_b,p.clock_b,false);
        const bool apart=a.start>=0 && b.start>=0
                         && (a.start>=b.start+kCount || b.start>=a.start+kCount);
        if(!apart)
            printf("  [i]    %012llx clock %08x -> 0x%04lx; %012llx clock %08x -> 0x%04lx\n",
                   static_cast<unsigned long long>(p.mac_a),p.clock_a,a.start,
                   static_cast<unsigned long long>(p.mac_b),p.clock_b,b.start);
        disjoint &= apart;
    }
    return disjoint;
}

bool MaapHarness::claims_differ(const std::vector<StationPair>& pairs){
    bool differ=true;
    for(const auto& p : pairs){
        const FirstClaim a=first_claim(p.mac_a,p.clock_a,false);
        const FirstClaim b=first_claim(p.mac_b,p.clock_b,false);
        differ &= a.start>=0 && b.start>=0 && a.start!=b.start;
    }
    return differ;
}

bool MaapHarness::intervals_differ(const std::vector<StationPair>& pairs){
    bool differ=true;
    for(const auto& p : pairs){
        const FirstClaim a=first_claim(p.mac_a,p.clock_a,true);
        const FirstClaim b=first_claim(p.mac_b,p.clock_b,true);
        differ &= a.interval>=0 && b.interval>=0 && a.interval!=b.interval;
    }
    return differ;
}

// #696 M4 (B.3.4 NOTE, B.3.6.1): the station MAC and the real-time clock must
// separate the first claims of equally timed stations. For every carry run
// i..j of the seed, one pair of seeds 2^i apart whose sum flips exactly bits
// i..j; each pair has its own common clock, and the MACs carry the rest of
// the seeds. i = 0 gives adjacent MACs, 16 <= i <= 31 MACs that differ only
// in bits 16..31. These sample the criterion of #696 comment 6102832618;
// section [13] establishes it for every seed. The fixed pairs are R558-6's
// and two clock pairs: they pin those pairs at these fold constants, and
// pairs that are not a power of two apart carry no separation guarantee.
void MaapHarness::first_claims_of_equally_timed_stations(){
    printf("\n[12] #696 M4: first Begin! claims of equally timed stations (B.3.4 NOTE, B.3.6.1)\n");
    const std::vector<StationPair> fixed{{0x020000000001ULL,0x020000000002ULL,0,0},
                                   {0x020000000001ULL,0x020000010001ULL,0,0},
                                   {0x0200000a1234ULL,0x0200005b1234ULL,7,7},
                                   {0x020011001234ULL,0x020022001234ULL,0,0}};
    std::vector<StationPair> adjacent;
    std::vector<StationPair> high;
    std::vector<StationPair> low;
    std::vector<StationPair> timers;
    uint32_t sample=0x2545f491u;
    for(unsigned i=0;i<32;++i)
        for(unsigned j=i;j<32;++j){
            sample=sample*1664525u+1013904223u;
            const uint32_t ones=static_cast<uint32_t>((uint64_t{1}<<j)-(uint64_t{1}<<i));
            const uint32_t seed=(sample|ones)&~(uint32_t{1}<<j);
            const uint32_t clock=sample*2654435761u;
            const StationPair p{kMacBase|static_cast<uint32_t>(seed-clock),
                                kMacBase|static_cast<uint32_t>(seed-clock+(uint32_t{1}<<i)),
                                clock,clock};
            (i==0 ? adjacent : i>=16 ? high : low).push_back(p);
            if(i==0 || (i>=16 && j==i)) timers.push_back(p);
        }
    std::vector<StationPair> clocks;
    for(unsigned k=0;k<32;++k){
        sample=sample*1664525u+1013904223u;
        clocks.push_back({kStationMac,kStationMac,sample,sample+(uint32_t{1}<<k)});
    }
    const std::vector<StationPair> fixed_clocks{{kStationMac,kStationMac,0,17},
                                                {kStationMac,kStationMac,0x01020304u,0xffff1234u}};
    printf("  [i]    2^i apart: %zu adjacent, %zu with i 16..31, %zu with i 1..15, %zu clock,"
           " %zu interval pairs; fixed: %zu MAC, %zu clock pairs\n",
           adjacent.size(),high.size(),low.size(),clocks.size(),timers.size(),
           fixed.size(),fixed_clocks.size());
    ck("M4 B.3.6.1 adjacent MACs claim disjoint first blocks",claims_disjoint(adjacent),1);
    ck("M4 B.3.6.1 MACs 2^i apart (16 <= i <= 31) claim disjoint first blocks",
       claims_disjoint(high),1);
    ck("M4 B.3.6.1 MACs 2^i apart (1 <= i <= 15) claim disjoint first blocks",
       claims_disjoint(low),1);
    ck("M4 B.3.6.1 R558-6's fixed MAC pairs claim disjoint first blocks",claims_disjoint(fixed),1);
    ck("M3 B.3.6.1 clocks 2^k apart claim different first offsets",claims_differ(clocks),1);
    ck("M3 B.3.6.1 fixed clock pairs claim different first offsets",claims_differ(fixed_clocks),1);
    ck("M4 B.3.4 MACs 2^i apart draw different first probe intervals",intervals_differ(timers),1);
    ck("M4 B.3.4 R558-6's fixed MAC pairs draw different first probe intervals",
       intervals_differ(fixed),1);
}

// One station's first Begin! from reset, as the RTL draws it: the seed is
// the MAC's low word at clock 0, and enable follows reset by one cycle. The
// claim is made at that edge; with tready low nothing reaches the wire.
uint16_t MaapHarness::seeded_first_offset(uint32_t seed, uint8_t count){
    dut->enable_i=0; dut->rst_n=0; dut->m_axis_tready=0; cyc();
    dut->station_mac_i=kMacBase|seed; dut->realtime_ns_i=0;
    dut->count_i=count; dut->seed_valid_i=0; dut->port_operational_i=1;
    dut->rst_n=1; dut->enable_i=1; cyc();
    return dut->offset_o;
}

// The same station's first probe draw: the probe timer its first PROBE loads
// on the next cycle, less the RTL's own PROBE_MIN_MS_C.
long MaapHarness::seeded_first_probe_draw(uint32_t seed){
    seeded_first_offset(seed, kCount);
    cyc();
    return static_cast<long>(dut->rootp->KL_maap__DOT__timer_ms_r)
           - static_cast<long>(VKL_maap___024root::KL_maap__DOT__PROBE_MIN_MS_C);
}

// Reduce `image` against the basis. A new pivot extends the image; a value
// that reduces to zero leaves its seed in the map's kernel.
bool MaapHarness::insert_image(ImageBasis& basis, SeedImage image, uint32_t& kernel){
    for (int bit=31;bit>=0;--bit) {
        if (!((image.value>>bit)&1)) continue;
        if (!basis[bit].value) { basis[bit]=image; return true; }
        image.value^=basis[bit].value;
        image.seed^=basis[bit].seed;
    }
    kernel=image.seed;
    return false;
}

int MaapHarness::image_rank(const SeedMap& map, unsigned first, unsigned last){
    ImageBasis basis{};
    uint32_t kernel=0;
    int rank=0;
    for (unsigned k=first;k<=last;++k) rank+=insert_image(basis,{map[k],uint32_t{1}<<k},kernel);
    return rank;
}

// #696 M4: the criterion of comment 6102832618 for every seed, not a sample.
// The first offset word and the first probe draw are GF(2)-linear in the seed
// (one generator step, then parity folds), so the suite learns both maps from
// the RTL's own first Begin! and checks them on fresh seeds. Seeds s and
// s + 2^i differ by one carry run i..j, so their words differ by that run's
// image whatever s is: every run meets every word of the image, and each
// word's claim for counts 1..8 is the offset the RTL claims for it. No fold
// row, generator tap or pool bound is restated here.
void MaapHarness::first_draws_for_every_seed(){
    printf("\n[13] #696 M4: first draws for every seed, learned from the RTL (B.3.4, B.3.6.1)\n");
    // With count 0 the clip never acts, and the pool fold puts every word
    // above the pool below this bound, so an offset at or above it is the word.
    constexpr long kUnfolded=0x10000L-VKL_maap___024root::KL_maap__DOT__POOL_SIZE_C;
    SeedMap offset_map{};
    SeedMap probe_map{};
    bool linear=learn_seed_map(offset_map,0x7f4a7c15u,[this](uint32_t seed){
        const long offset=seeded_first_offset(seed,0);
        return offset>=kUnfolded ? offset : -1L; });
    linear&=learn_seed_map(probe_map,0x2b992ddfu,[this](uint32_t seed){
        return seeded_first_probe_draw(seed); });

    // Every word of the offset image, each steered by a seed the RTL maps onto
    // it. Adding a kernel seed keeps every steered seed nonzero.
    ImageBasis basis{};
    uint32_t kernel=0;
    for (unsigned k=0;k<offset_map.size();++k) {
        uint32_t dependent=0;
        if (!insert_image(basis,{offset_map[k],uint32_t{1}<<k},dependent) && !kernel)
            kernel=dependent;
    }
    std::vector<SeedImage> pivots;
    for (const auto& entry : basis) if (entry.value) pivots.push_back(entry);
    linear&=kernel!=0;
    // claims[count-1][word]: the offset the RTL claims, -1 outside the image
    std::vector<std::vector<int32_t>> claims(kCount, std::vector<int32_t>(1u<<16,-1));
    for (uint32_t m=0;linear && m<(uint32_t{1}<<pivots.size());++m) {
        SeedImage word{0,kernel};
        for (unsigned p=0;p<pivots.size();++p)
            if ((m>>p)&1) { word.value^=pivots[p].value; word.seed^=pivots[p].seed; }
        for (unsigned count=1;count<=kCount;++count)
            claims[count-1][word.value]=seeded_first_offset(word.seed,static_cast<uint8_t>(count));
    }
    uint32_t sample=0x6c8e9cf5u;
    for (int n=0;linear && n<kLinearitySamples;++n) {
        sample=sample*1664525u+1013904223u;
        if (!sample) continue;
        const unsigned count=1+static_cast<unsigned>(n)%kCount;
        linear&=seeded_first_offset(sample,static_cast<uint8_t>(count))
                ==claims[count-1][apply_generator_map(offset_map,sample)];
        linear&=seeded_first_probe_draw(sample)
                ==static_cast<long>(apply_generator_map(probe_map,sample));
    }
    dut->m_axis_tready=1;
    ck("M4 first-draw maps learned from the RTL are linear in the seed",linear,1);

    bool disjoint=linear;
    bool probes_differ=linear;
    long spare=1L<<16;
    for (unsigned i=0;linear && i<32;++i)
        for (unsigned j=i;j<32;++j) {
            const uint32_t run=static_cast<uint32_t>((uint64_t{1}<<(j+1))-(uint64_t{1}<<i));
            const uint32_t delta=apply_generator_map(offset_map,run);
            if (!apply_generator_map(probe_map,run)) {
                if (probes_differ) printf("  [i]    carry run %u..%u: equal first probe draws\n",i,j);
                probes_differ=false;
            }
            for (unsigned count=1;count<=kCount;++count) {
                const auto& claim=claims[count-1];
                for (uint32_t w=0;w<claim.size();++w) {
                    if (claim[w]<0) continue;
                    // delta lies in the image, so claim[w^delta] is known
                    const long other=claim[w^delta];
                    const long gap=other<0 ? -1 : std::labs(claim[w]-other);
                    if (gap<static_cast<long>(count) && disjoint)
                        printf("  [i]    carry run %u..%u, count %u: words 0x%04x / 0x%04x"
                               " claim 0x%04x / 0x%04lx\n",i,j,count,w,w^delta,
                               static_cast<unsigned>(claim[w]),static_cast<unsigned long>(other));
                    disjoint&=gap>=static_cast<long>(count);
                    spare=std::min(spare,gap-static_cast<long>(count));
                }
            }
        }
    SeedMap both{};
    for (unsigned k=0;k<both.size();++k) both[k]=offset_map[k]|(probe_map[k]<<16);
    if (linear)
        printf("  [i]    offset image %zu bits, probe image %d bits; %zu words x %d counts claimed;"
               " 528 carry runs; least spare addresses %ld\n",
               pivots.size(),image_rank(probe_map,0,31),size_t{1}<<pivots.size(),kCount,spare);
    else
        printf("  [i]    the maps are not linear, so no claim below is established\n");
    ck("M4 B.3.6.1 every seed pair 2^i apart claims disjoint first blocks of 1..8",disjoint,1);
    ck("M4 B.3.4 every seed pair 2^i apart draws different first probe intervals",probes_differ,1);
    ck("M4 B.3.6.1 seed bits 16..31 map one-to-one onto the first offset word",
       linear && image_rank(offset_map,16,31)==16,1);
    ck("M4 B.3.6.1 first offset word and first probe draw are independent",
       linear && image_rank(both,0,31)==22,1);
}

int MaapHarness::run(){
    bring_up_idle();
    check_reset_idle();
    const uint16_t off0 = acquire_four_probes_then_announce();
    announce_intervals_and_destination();
    defend_to_the_prober(off0);
    announce_conflict_detection(off0);
    probe_mid_frame_is_defended();
    frame_on_the_wire_keeps_its_range();
    defend_and_probe_reception();
    ignore_disjoint_and_non_pool_pdus();
    honour_conflicts_from_any_maap_version();
    probe_interval_campaign();
    disable_then_claim_the_seed();
    zero_seed_mac_draws_random_timers();
    compare_mac_remaining_cells();
    pending_response_cancelled();
    port_return_reprobes();
    port_loss_is_no_event();
    supplied_seed_bounds();
    truncated_pdus_have_no_effect();
    generator_period_and_seed();
    first_claims_of_equally_timed_stations();
    first_draws_for_every_seed();

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
