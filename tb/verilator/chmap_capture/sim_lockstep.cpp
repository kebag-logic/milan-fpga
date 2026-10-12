// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Lockstep leg (#640 M6): KL_chan_map_capture against the pre-change
// reference KL_chan_map_capture_ref (reference/, the module of dev e8454e27
// with only its name changed), both fed the SAME inputs every cycle by
// chmap_lockstep_wrap.
//
//   [LS] every output of the two is identical in every cycle: the injected
//        pairs and their slots, the map readback and flat view, and the
//        four slip counters.
//   [ST] the source table: every channel entry class - I2S and TDM halves,
//        TDM pairs past the bucket, tone, ZERO, the reserved sources, a
//        disabled entry, and LOOP entries naming a pair the build keeps or
//        not - resolves to its own source sample, judged by value.
//   [SK] the commit skid and its beat bank: back-to-back loopback beats on a
//        mono wire (two commits per beat) and on a three-channel wire (a
//        stashed L closing on the next beat, a lone even channel) replay
//        every sample event exactly once, in order, judged by value.
//   [SO] a seeded random soak over every input - map writes and reads,
//        front-end strobes, beats at wire and faster-than-wire spacing,
//        flushes, recentres and late ticks - compared as [LS].
#include "Vchmap_lockstep_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

#ifndef SLOTS_TB
#define SLOTS_TB 4
#endif
#ifndef NLB_TB
#define NLB_TB 1
#endif

namespace {

constexpr int kSlots = SLOTS_TB;
constexpr int kNlb = NLB_TB;
constexpr int kTdmPairs = 4;
constexpr int kGap = 24;
//! one walk: 1 + the pre-walk + every slot's step and gap
constexpr int kWalk = 1 + (kNlb * 4 + 1) + kSlots * (kGap + 2);
constexpr uint32_t kSrcZero = 0;
constexpr uint32_t kSrcI2s = 1;
constexpr uint32_t kSrcTdm = 2;
constexpr uint32_t kSrcRes = 3;
constexpr uint32_t kSrcTone = 4;
constexpr uint32_t kSrcLoop = 5;

uint32_t entry(bool en, int half, uint32_t src, int idxh, int idx) {
    return (en ? 1u << 12 : 0u) | (static_cast<uint32_t>(half) << 11) | (src << 8) |
           (static_cast<uint32_t>(idxh) << 4) | static_cast<uint32_t>(idx);
}

//! a beat of two S32BE samples in wire order (byte 0 = MSB, byte 3 = pad)
uint64_t beat(uint32_t s0, uint32_t s1) {
    auto lane = [](uint32_t v) {
        return static_cast<uint64_t>((v >> 16) & 0xFF) | (static_cast<uint64_t>((v >> 8) & 0xFF) << 8) |
               (static_cast<uint64_t>(v & 0xFF) << 16);
    };
    return lane(s0) | (lane(s1) << 32);
}

struct Rng {
    uint64_t s;
    explicit Rng(uint64_t seed) : s(seed ? seed : 1) {}
    uint64_t next() {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        return s;
    }
    uint32_t below(uint32_t n) { return static_cast<uint32_t>(next() % n); }
    bool chance(uint32_t one_in) { return below(one_in) == 0; }
};

struct Inject {
    int slot;
    uint32_t l;
    uint32_t r;
};

class Lockstep {
 public:
    explicit Lockstep(milan::tb::Checker& c) : c_(c) {}
    void run();

 private:
    milan::tb::Checker& c_;
    milan::tb::Model<Vchmap_lockstep_wrap> dut_;
    uint64_t cycle_ = 0;
    uint64_t ls_bad_ = 0;
    std::string first_bad_;
    std::vector<Inject> injected_;

    void pulses_off();
    void step();
    void compare();
    void cycles(int n) {
        for (int i = 0; i < n; i++) step();
    }
    void reset();
    void map_write(int key, uint32_t e);
    void tick_walk();
    void send_beat(uint64_t data, bool last, int stream);
    void report(const char* phase);

    void st_source_table();
    void sk_replay(int chans, const char* name);
    void soak(uint64_t seed, int n);
};

void Lockstep::pulses_off() {
    dut_->map_wr_en_i = 0;
    dut_->map_rd_en_i = 0;
    dut_->i2s_pair_valid_i = 0;
    dut_->tdm_pair_valid_i = 0;
    dut_->lb_tvalid_i = 0;
    dut_->lb_tlast_i = 0;
    dut_->lb_flush_i = 0;
    dut_->lb_recentre_i = 0;
    dut_->tick_i = 0;
}

void Lockstep::step() {
    dut_->clk_i = 0;
    dut_->eval();
    dut_->clk_i = 1;
    dut_->eval();
    ++cycle_;
    pulses_off();
    dut_->eval();
    compare();
    if (dut_->dut_pair_valid_o)
        injected_.push_back({dut_->dut_pair_slot_o, dut_->dut_pair_l_o, dut_->dut_pair_r_o});
}

void Lockstep::compare() {
    auto bad = [this](const char* what) {
        if (ls_bad_++ == 0) first_bad_ = std::string(what) + " at cycle " + std::to_string(cycle_);
    };
    if (dut_->ref_map_rd_valid_o != dut_->dut_map_rd_valid_o) bad("map_rd_valid_o");
    if (dut_->ref_map_rd_data_o != dut_->dut_map_rd_data_o) bad("map_rd_data_o");
    constexpr int kFlatWords = (2 * kSlots * 13 + 31) / 32;
    for (int w = 0; w < kFlatWords; w++) {
        if constexpr (2 * kSlots * 13 > 64) {
            if (dut_->ref_map_flat_o[w] != dut_->dut_map_flat_o[w]) bad("map_flat_o");
        } else {
            if (dut_->ref_map_flat_o != dut_->dut_map_flat_o) bad("map_flat_o");
        }
    }
    if (dut_->ref_pair_valid_o != dut_->dut_pair_valid_o) bad("pair_valid_o");
    if (dut_->ref_pair_slot_o != dut_->dut_pair_slot_o) bad("pair_slot_o");
    if (dut_->ref_pair_l_o != dut_->dut_pair_l_o) bad("pair_l_o");
    if (dut_->ref_pair_r_o != dut_->dut_pair_r_o) bad("pair_r_o");
    if (dut_->ref_lb_dup_cnt_o != dut_->dut_lb_dup_cnt_o) bad("lb_dup_cnt_o");
    if (dut_->ref_lb_skip_cnt_o != dut_->dut_lb_skip_cnt_o) bad("lb_skip_cnt_o");
    if (dut_->ref_tdm_dup_cnt_o != dut_->dut_tdm_dup_cnt_o) bad("tdm_dup_cnt_o");
    if (dut_->ref_tdm_skip_cnt_o != dut_->dut_tdm_skip_cnt_o) bad("tdm_skip_cnt_o");
}

void Lockstep::report(const char* phase) {
    if (ls_bad_ != 0) std::printf("  first divergence: %s\n", first_bad_.c_str());
    const std::string a = std::string("[LS] ") + phase + ": every output identical to the reference in every cycle";
    c_.dec(a.c_str(), ls_bad_, 0);
    ls_bad_ = 0;
    first_bad_.clear();
}

void Lockstep::reset() {
    dut_->rst_n = 0;
    cycles(3);
    dut_->rst_n = 1;
    cycles(2);
}

void Lockstep::map_write(int key, uint32_t e) {
    dut_->map_wr_en_i = 1;
    dut_->map_wr_addr_i = static_cast<uint8_t>(key);
    dut_->map_wr_data_i = static_cast<uint16_t>(e);
    step();
}

//! one media tick and the whole walk it starts, injected pairs recorded
void Lockstep::tick_walk() {
    injected_.clear();
    dut_->tick_i = 1;
    cycles(kWalk + 8);
}

void Lockstep::send_beat(uint64_t data, bool last, int stream) {
    dut_->lb_tdata_i = data;
    dut_->lb_tvalid_i = 1;
    dut_->lb_tlast_i = last ? 1 : 0;
    dut_->lb_tuser_i = static_cast<uint8_t>(stream);
    step();
}

void Lockstep::st_source_table() {
    std::printf("[ST] the source table resolves every entry class\n");
    reset();
    //! the front ends: one I2S pair, one whole TDM frame, a fixed tone
    dut_->i2s_pair_valid_i = 1;
    dut_->i2s_l_i = 0x111111;
    dut_->i2s_r_i = 0x222222;
    step();
    for (int p = 0; p < kTdmPairs; p++) {
        dut_->tdm_pair_valid_i = 1;
        dut_->tdm_pair_slot_i = static_cast<uint8_t>(p);
        dut_->tdm_l_i = 0x300000u | static_cast<uint32_t>(p << 8) | 0x0Au;
        dut_->tdm_r_i = 0x400000u | static_cast<uint32_t>(p << 8) | 0x0Bu;
        cycles(3);
    }
    dut_->tone_smp_i = 0x777777;
    //! every class, with the sample it must resolve to
    struct Case {
        uint32_t e;
        uint32_t want;
    };
    std::vector<Case> cases = {
        {entry(true, 0, kSrcI2s, 0, 0), 0x111111}, {entry(true, 1, kSrcI2s, 0, 9), 0x222222},
        {entry(true, 0, kSrcTone, 0, 0), 0x777777}, {entry(true, 1, kSrcTone, 3, 3), 0x777777},
        {entry(true, 0, kSrcZero, 0, 0), 0}, {entry(true, 1, kSrcRes, 0, 0), 0},
        {entry(true, 0, 6, 0, 0), 0}, {entry(true, 1, 7, 0, 1), 0},
        {entry(false, 0, kSrcI2s, 0, 0), 0}, {entry(false, 1, kSrcTdm, 0, 1), 0},
        {entry(true, 0, kSrcLoop, 0, 0), 0}, {entry(true, 1, kSrcLoop, kNlb, 0), 0},
        {entry(true, 0, kSrcLoop, 0, 7), 0}, {entry(true, 0, kSrcTdm, 0, 4), 0},
        {entry(true, 1, kSrcTdm, 0, 15), 0},
    };
    for (int p = 0; p < kTdmPairs; p++) {
        cases.push_back({entry(true, 0, kSrcTdm, 0, p), 0x300000u | static_cast<uint32_t>(p << 8) | 0x0Au});
        cases.push_back({entry(true, 1, kSrcTdm, 5, p), 0x400000u | static_cast<uint32_t>(p << 8) | 0x0Bu});
    }
    uint64_t wrong = 0;
    uint64_t seen = 0;
    for (size_t base = 0; base < cases.size(); base += 2 * kSlots) {
        for (int k = 0; k < 2 * kSlots; k++)
            map_write(k, cases[(base + static_cast<size_t>(k)) % cases.size()].e);
        tick_walk();
        for (const Inject& in : injected_) {
            const size_t kl = (base + static_cast<size_t>(2 * in.slot)) % cases.size();
            const size_t kr = (base + static_cast<size_t>(2 * in.slot + 1)) % cases.size();
            wrong += (in.l != cases[kl].want) + (in.r != cases[kr].want);
            seen += 2;
        }
    }
    c_.that("[ST] every walk injected every slot (the case is live)",
            seen >= cases.size() && seen % (2 * kSlots) == 0);
    c_.dec("[ST] every channel entry resolves to its own source sample", wrong, 0);
    report("ST");
}

//! `chans`-channel loopback wire on stream 0, its pairs mapped to the
//! slots in channel order; PDUs of back-to-back beats, one media tick per
//! sample event, so the queue replays each event at one walk
void Lockstep::sk_replay(int chans, const char* name) {
    std::printf("[SK] %s\n", name);
    reset();
    const int pairs = (chans + 1) / 2;
    for (int k = 0; k < 2 * kSlots; k++) {
        const int pair = k / 2;
        map_write(k, pair < pairs ? entry(true, k % 2, kSrcLoop, 0, pair) : entry(true, 0, kSrcZero, 0, 0));
    }
    uint32_t wc = 0;
    for (int s = 0; s < kNlb; s++) wc |= static_cast<uint32_t>(chans) << (4 * s);
    dut_->lb_wire_chans_i = wc;
    //! sample value of event e, channel ch: unique per sample
    auto value = [](int e, int ch) { return 0x100000u | (static_cast<uint32_t>(e) << 4) | static_cast<uint32_t>(ch); };
    constexpr int kEvents = 6;  //! per PDU (class A)
    constexpr int kPdus = 8;
    const uint64_t skip0 = dut_->ref_lb_skip_cnt_o;
    std::vector<Inject> got;
    for (int pdu = 0; pdu < kPdus; pdu++) {
        //! the PDU's samples in wire order, two per beat, back to back
        std::vector<uint32_t> smp;
        for (int e = 0; e < kEvents; e++)
            for (int ch = 0; ch < chans; ch++) smp.push_back(value(pdu * kEvents + e, ch));
        if (smp.size() % 2) smp.push_back(0);
        for (size_t i = 0; i < smp.size(); i += 2) send_beat(beat(smp[i], smp[i + 1]), i + 2 >= smp.size(), 0);
        cycles(4);
        //! the first PDU primes the queue; every later PDU's events pop
        //! one per walk, behind the previous PDU's
        for (int t = 0; t < kEvents; t++) {
            tick_walk();
            for (const Inject& in : injected_) got.push_back(in);
        }
    }
    //! judge the replay: walk w carries event w on every mapped pair
    uint64_t wrong = 0;
    uint64_t walks = 0;
    for (size_t i = 0; i + static_cast<size_t>(kSlots) <= got.size(); i += static_cast<size_t>(kSlots)) {
        const int e = static_cast<int>(walks++);
        for (int p = 0; p < pairs; p++) {
            const Inject& in = got[i + static_cast<size_t>(p)];
            const uint32_t want_l = value(e, 2 * p);
            const uint32_t want_r = (2 * p + 1 < chans) ? value(e, 2 * p + 1) : 0;
            wrong += (in.l != want_l) + (in.r != want_r);
        }
    }
    c_.that("[SK] the replay ran one walk per event (the case is live)", walks == kPdus * kEvents);
    const std::string w = std::string("[SK] ") + name + ": every event replayed once, in order";
    c_.dec(w.c_str(), wrong, 0);
    const std::string k = std::string("[SK] ") + name + ": no event refused at the skid";
    c_.dec(k.c_str(), dut_->ref_lb_skip_cnt_o - skip0, 0);
    report("SK");
}

void Lockstep::soak(uint64_t seed, int n) {
    std::printf("[SO] random soak, seed %llu, %d cycles\n", static_cast<unsigned long long>(seed), n);
    Rng r(seed);
    reset();
    int beats_left = 0;
    int beat_gap = 0;
    int stream = 0;
    uint64_t pairs = 0;
    uint64_t beats = 0;
    uint64_t skips = 0;
    uint64_t flushes = 0;
    uint64_t ticks = 0;
    uint64_t resets = 0;
    for (int i = 0; i < n; i++) {
        if (r.chance(20000)) {
            reset();
            resets++;
            continue;
        }
        if (r.chance(60)) {
            dut_->map_wr_en_i = 1;
            dut_->map_wr_addr_i = static_cast<uint8_t>(r.below(2 * kSlots));
            uint32_t e = r.below(1u << 13);
            if (!r.chance(4)) e = (e & ~0xF0u) | (r.below(kNlb + 1) << 4);
            if (!r.chance(4)) e = (e & ~0xFu) | r.below(5);
            if (r.chance(3)) e = (e & ~0x700u) | (kSrcLoop << 8) | 0x1000u;
            dut_->map_wr_data_i = static_cast<uint16_t>(e);
        }
        if (r.chance(50)) {
            dut_->map_rd_en_i = 1;
            dut_->map_rd_addr_i = static_cast<uint8_t>(r.below(2 * kSlots));
        }
        if (r.chance(35)) {
            dut_->i2s_pair_valid_i = 1;
            dut_->i2s_l_i = r.below(1u << 24);
            dut_->i2s_r_i = r.below(1u << 24);
        }
        if (r.chance(10)) {
            dut_->tdm_pair_valid_i = 1;
            dut_->tdm_pair_slot_i = static_cast<uint8_t>(r.chance(20) ? r.below(16) : r.below(kTdmPairs));
            dut_->tdm_l_i = r.below(1u << 24);
            dut_->tdm_r_i = r.below(1u << 24);
        }
        if (r.chance(2000)) {
            uint32_t wc = 0;
            for (int s = 0; s < kNlb; s++) wc |= r.below(16) << (4 * s);
            dut_->lb_wire_chans_i = wc;
        }
        //! loopback PDUs: beats at wire spacing, sometimes far faster
        if (beats_left == 0 && r.chance(150)) {
            beats_left = 1 + static_cast<int>(r.below(12));
            beat_gap = r.chance(4) ? 1 + static_cast<int>(r.below(2)) : 8 + static_cast<int>(r.below(8));
            stream = static_cast<int>(r.chance(10) ? r.below(16) : r.below(kNlb));
        }
        if (beats_left > 0 && (i % beat_gap) == 0) {
            dut_->lb_tdata_i = r.next();
            dut_->lb_tvalid_i = 1;
            dut_->lb_tuser_i = static_cast<uint8_t>(stream);
            dut_->lb_tlast_i = (--beats_left == 0) ? 1 : 0;
            beats++;
        }
        if (r.chance(3000)) {
            dut_->lb_flush_i = static_cast<uint8_t>(1u << r.below(kNlb));
            flushes++;
        }
        if (r.chance(3000)) dut_->lb_recentre_i = static_cast<uint8_t>(r.below(1u << kNlb));
        if (r.chance(kWalk + 200)) {
            dut_->tick_i = 1;
            dut_->tone_smp_i = r.below(1u << 24);
            ticks++;
        }
        step();
        pairs += dut_->ref_pair_valid_o;
    }
    skips = dut_->ref_lb_skip_cnt_o;
    std::printf("  soak exercised: %llu injected pairs, %llu beats, %llu ticks, %llu flushes, "
                "%llu resets, skip counter %llu\n",
                static_cast<unsigned long long>(pairs), static_cast<unsigned long long>(beats),
                static_cast<unsigned long long>(ticks), static_cast<unsigned long long>(flushes),
                static_cast<unsigned long long>(resets), static_cast<unsigned long long>(skips));
    c_.that("[SO] the soak injected pairs, sent beats, ticked, flushed and reset (live)",
            pairs > 1000 && beats > 1000 && ticks > 100 && flushes > 10 && resets > 2);
    report("SO");
}

void Lockstep::run() {
    dut_->clk_i = 0;
    dut_->lb_wire_chans_i = 0;
    dut_->tone_smp_i = 0;
    pulses_off();
    reset();
    st_source_table();
    sk_replay(1, "mono wire, two commits per beat");
    sk_replay(3, "three-channel wire, stashed and lone channels");
    sk_replay(8, "eight-channel wire, aligned pairs");
    soak(0x640u + kSlots, 400000);
    soak(0x9e3779b97f4a7c15ULL, 400000);
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const std::string label = "chmap_capture lockstep " + std::to_string(kSlots) + " slots";
    milan::tb::Checker c(label.c_str());
    c.echo_passes();
    {
        Lockstep ls(c);
        ls.run();
    }
    return c.report();
}
