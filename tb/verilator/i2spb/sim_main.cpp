// KL_i2s_playback true-async harness: clk_i ~50 MHz vs clk_audio ~24.576 MHz
// (fractional phase-walk so every alignment is exercised), PDU-burst feed
// profile (6 pairs back-to-back @ 8 kHz), decode the serialized I2S and
// compare sample-exact against the fed ramp. Reproduces/regresses the
// silicon 48-sample corruption (CDC under real burst+async conditions).
#include "VKL_i2s_playback.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <vector>
#include <cstdint>

// clk_i 10 ns period, clk_audio 40.690 ns (24.576 MHz), in picoseconds
constexpr uint64_t kSysPeriodPs = 10000;
constexpr uint64_t kSysHalfPeriodPs = kSysPeriodPs / 2;
constexpr uint64_t kAudioPeriodPs = 40690;
constexpr uint64_t kAudioHalfPeriodPs = kAudioPeriodPs / 2;
constexpr uint64_t kSimEndPs = 3000000000ull;   // 3 ms sim
constexpr size_t   kMaxSamples = 400;           // decoder capture cap
constexpr size_t   kMinSamples = 100;           // [A] "enough samples" floor
constexpr int      kSampleBits = 24;            // I2S slots 1..24
constexpr uint32_t kSampleMask = 0xFFFFFF;      // 24-bit sample mask

namespace {

class I2sPlaybackHarness {
 public:
    int run();

 private:
    void ck(const char* w, long got, long exp);

    void walk_half_beat_rates();
    void release_reset_on_walking_clocks();
    void feed_bursts_and_decode_i2s();
    void report_ramp_continuity();
    void clear_and_rearm_rails();

    // async clocks: clk_i 10ns period, clk_audio 40.690ns (24.576 MHz) -
    // phase-walk via a picosecond accumulator
    void tickmin();

    VKL_i2s_playback* dut = nullptr;
    long checks = 0;
    long fails = 0;

    uint64_t t = 0;                     // picoseconds
    uint64_t next_i = kSysHalfPeriodPs;
    uint64_t next_a = kAudioHalfPeriodPs;

    std::vector<uint32_t> got;
};

void I2sPlaybackHarness::ck(const char* w, long got, long exp){
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %s got=%ld exp=%ld\n", w, got, exp); }
    else printf("  [ ok ] %s = %ld\n", w, got);
}

void I2sPlaybackHarness::tickmin(){
    if (next_i <= next_a) { t = next_i; dut->clk_i ^= 1; next_i += kSysHalfPeriodPs; }
    else                  { t = next_a; dut->clk_audio_i ^= 1; next_a += kAudioHalfPeriodPs; }
    dut->eval();
}

// ================================================================
// [W] half-beat walker rates (USER 1-to-1 mapping rule): fill_o is
// the exact pair count while the boot prefill holds the feeder.
// C=2: 1 pair/beat; C=8: first-pair-only = 1 per 4 beats; C=3: 2
// per 3 beats (odd straddle); C=1: 2 pairs/beat via the staging
// queue (back-to-back beats included). Full reset afterwards.
// ================================================================
void I2sPlaybackHarness::walk_half_beat_rates(){
    auto sysstep = [&](){ dut->clk_i = 1; dut->eval();
                          dut->clk_i = 0; dut->eval(); };
    for (int i = 0; i < 8; i++) sysstep();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) sysstep();
    auto beat = [&](int last, int gap){
        dut->pcm_tdata_i = 0x0011223300445566ull;
        dut->pcm_tvalid_i = 1; dut->pcm_tlast_i = last;
        sysstep();
        dut->pcm_tvalid_i = 0; dut->pcm_tlast_i = 0;
        for (int g = 0; g < gap; g++) sysstep();
    };
    long f0 = dut->fill_o;

    dut->wire_chans_i = 2;
    for (int b = 0; b < 6; b++) beat(b == 5, 1);
    for (int i = 0; i < 6; i++) sysstep();
    ck("[W] C=2 pairs (1/beat)", dut->fill_o - f0, 6); f0 = dut->fill_o;

    dut->wire_chans_i = 8;
    for (int b = 0; b < 8; b++) beat(b == 7, 1);
    for (int i = 0; i < 6; i++) sysstep();
    ck("[W] C=8 first-pair only", dut->fill_o - f0, 2); f0 = dut->fill_o;

    dut->wire_chans_i = 3;
    for (int b = 0; b < 3; b++) beat(b == 2, 1);
    for (int i = 0; i < 6; i++) sysstep();
    ck("[W] C=3 odd straddle", dut->fill_o - f0, 2); f0 = dut->fill_o;

    dut->wire_chans_i = 1;
    for (int b = 0; b < 3; b++) beat(b == 2, 0);   // back-to-back
    for (int i = 0; i < 8; i++) sysstep();
    ck("[W] C=1 mono 2/beat (staging)", dut->fill_o - f0, 6);

    ck("[W] prefill still holding feeder", dut->underruns_o, 0);
    // full reset: scenario [A] starts from a clean FIFO
    dut->rst_n = 0;
    for (int i = 0; i < 8; i++) sysstep();
    dut->wire_chans_i = 2;
}

void I2sPlaybackHarness::release_reset_on_walking_clocks(){
    for (int i = 0; i < 64; i++) tickmin();
    dut->rst_n = 1;
}

// feed: bursts of 6 pairs (one PDU) every 125 us; payload = ramp
// (L = idx, R = idx ^ 0xFFFFFF) so any slot mixup is visible
void I2sPlaybackHarness::feed_bursts_and_decode_i2s(){
    uint32_t idx = 1;                      // avoid 0 (matches silence)
    uint64_t next_burst_ps = 200000;       // first PDU at 200 ns (sim-fast)
    int      in_burst = 0;
    uint64_t burst_gap_ps = 2000000;       // 2 us between "PDUs" (sim-compressed 125us)

    // I2S decoder on the audio-domain outputs
    int sclk_q = 0;
    int lrck_q = 1;
    int bit = -1;
    uint32_t acc = 0;

    while (t < kSimEndPs && got.size() < kMaxSamples) {   // 3 ms sim
        int was_clk_i = dut->clk_i;
        tickmin();
        // feeder on clk_i rising
        if (!was_clk_i && dut->clk_i) {
            if (in_burst == 0 && t >= next_burst_ps) { in_burst = 6; next_burst_ps += burst_gap_ps; }
            if (in_burst > 0 && dut->pcm_tvalid_i == 0) {
                uint32_t l = idx & kSampleMask;
                uint32_t r = (idx ^ kSampleMask) & kSampleMask;
                // S32BE lanes: bytes 0..2 = L msb..lsb, byte3=0, 4..6 = R
                uint64_t d = 0;
                d |= static_cast<uint64_t>((l >> 16) & 0xFF) << 0;
                d |= static_cast<uint64_t>((l >> 8)  & 0xFF) << 8;
                d |= static_cast<uint64_t>(l & 0xFF)         << 16;
                d |= static_cast<uint64_t>((r >> 16) & 0xFF) << 32;
                d |= static_cast<uint64_t>((r >> 8)  & 0xFF) << 40;
                d |= static_cast<uint64_t>(r & 0xFF)         << 48;
                dut->pcm_tdata_i = d; dut->pcm_tvalid_i = 1;
                idx++; in_burst--;
            } else {
                dut->pcm_tvalid_i = 0;
            }
        }
        // decoder on audio clk rising
        int sclk = dut->i2s_sclk_o;
        int lrck = dut->i2s_lrck_o;
        if (sclk && !sclk_q) {
            if (lrck_q && !lrck) { bit = 0; acc = 0; }        // LEFT begins
            else if (bit >= 0) {
                bit++;
                // textbook I2S chip: MSB on the SECOND rising edge after the
                // LRCK transition (slots 1..24), exactly like the CS4344
                if (bit >= 1 && bit <= kSampleBits) acc = (acc << 1) | (dut->i2s_sdin_o & 1);
                if (bit == kSampleBits) { got.push_back(acc); bit = -1; }
            }
            lrck_q = lrck;
        }
        sclk_q = sclk;
    }
}

// verdict: after startup, decoded LEFT samples must be CONSECUTIVE ramp
// values (repeats allowed ONLY when the feed starved - none here: feed
// 6/2us >> drain 1/20.8us) with NO stuck/garbage values
void I2sPlaybackHarness::report_ramp_continuity(){
    // start at the first NONZERO sample: the prefill recenter pads a few
    // zero frames before output begins (count depends on the release level)
    size_t first = 4;
    while (first < got.size() && got[first] == 0) first++;
    int consecutive = 0;
    int best = 0;
    uint32_t prev = 0;
    long bad_jumps = 0;
    for (size_t i = first; i < got.size(); i++) {
        if (got[i] == prev + 1) { consecutive++; best = consecutive > best ? consecutive : best; }
        else if (i > first) { bad_jumps++; consecutive = 0; }
        prev = got[i];
    }
    printf("decoded %zu samples, longest consecutive run %d, bad jumps %ld\n",
           got.size(), best, bad_jumps);
    for (size_t i = 4; i < 20 && i < got.size(); i++) printf("  s[%zu]=0x%06X\n", i, got[i]);
    ck("[A] enough samples decoded", got.size() >= kMinSamples, 1);
    ck("[A] zero bad jumps (no CDC corruption)", bad_jumps == 0, 1);
}

// ================================================================
// [C] rail-counter W1C (gaps 5b): the saturating rails were stuck
// forever once hit; an I2SPB_STAT write now restarts them per half
// (clr_over_i direct in clk_i, clr_under_i via cdc_pulse to audio).
// ================================================================
void I2sPlaybackHarness::clear_and_rearm_rails(){
    auto wait_posedge_i = [&](){
        for (;;) { int w = dut->clk_i; tickmin(); if (!w && dut->clk_i) return; }
    };
    auto run_us = [&](uint64_t us){
        uint64_t te = t + us * 1000000ull; while (t < te) tickmin();
    };
    dut->pcm_tvalid_i = 0;

    // both rails are nonzero after [A]: the boot prefill starved the
    // audio side (underruns), the 3 ms overfeed hit FIFO-full (overruns)
    long u0 = dut->underruns_o;
    long v0 = dut->overruns_o;
    ck("[C] underrun rail armed", u0 > 0, 1);
    ck("[C] overrun rail armed",  v0 > 0, 1);

    // W1C the OVERRUN half only (feed stopped -> no new drops)
    wait_posedge_i();
    dut->clr_over_i = 1; wait_posedge_i(); dut->clr_over_i = 0;
    run_us(5);
    ck("[C] overruns cleared", dut->overruns_o, 0);
    ck("[C] underruns untouched by over-clear", dut->underruns_o, u0);

    // W1C the UNDERRUN half (crosses into the audio domain; the CDC
    // FIFO is stocked so no new underrun accrues during the check)
    wait_posedge_i();
    dut->clr_under_i = 1; wait_posedge_i(); dut->clr_under_i = 0;
    run_us(5);
    ck("[C] underruns cleared", dut->underruns_o, 0);

    // re-arm: the cleared overrun rail counts again (FIFO still full,
    // a continuous feed drops immediately) - no stuck-at-zero either
    dut->pcm_tdata_i = 0x0011223300445566ull;
    dut->pcm_tvalid_i = 1;
    for (int b = 0; b < 64; b++) wait_posedge_i();
    dut->pcm_tvalid_i = 0;
    run_us(2);
    ck("[C] overrun rail re-armed", dut->overruns_o > 0, 1);
}

int I2sPlaybackHarness::run(){
    const milan::tb::Model<VKL_i2s_playback> model;
    dut = model.get();
    dut->rst_n = 0; dut->clk_i = 0; dut->clk_audio_i = 0;
    dut->pcm_tvalid_i = 0; dut->pcm_tready_i = 1; dut->pcm_tlast_i = 0;
    dut->wire_chans_i = 2; dut->servo_en_i = 0;
    dut->clr_under_i = 0; dut->clr_over_i = 0;

    walk_half_beat_rates();
    release_reset_on_walking_clocks();
    feed_bursts_and_decode_i2s();
    report_ramp_continuity();
    clear_and_rearm_rails();

    printf("i2spb-async: %ld checks, %ld failures\n", checks, fails);
    return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv){
    Verilated::commandArgs(argc, argv);
    I2sPlaybackHarness harness;
    return harness.run();
}
