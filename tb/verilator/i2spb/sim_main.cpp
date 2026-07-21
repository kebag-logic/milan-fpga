// KL_i2s_playback true-async harness: clk_i ~50 MHz vs clk_audio ~24.576 MHz
// (fractional phase-walk so every alignment is exercised), PDU-burst feed
// profile (6 pairs back-to-back @ 8 kHz), decode the serialized I2S and
// compare sample-exact against the fed ramp. Reproduces/regresses the
// silicon 48-sample corruption (CDC under real burst+async conditions).
#include "VKL_i2s_playback.h"
#include "verilated.h"
#include <cstdio>
#include <vector>
#include <cstdint>

static VKL_i2s_playback* dut;
static long checks=0, fails=0;
static void ck(const char* w, long got, long exp){
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %s got=%ld exp=%ld\n", w, got, exp); }
    else printf("  [ ok ] %s = %ld\n", w, got);
}

int main(int argc, char** argv){
    Verilated::commandArgs(argc, argv);
    dut = new VKL_i2s_playback;
    dut->rst_n = 0; dut->clk_i = 0; dut->clk_audio_i = 0;
    dut->pcm_tvalid_i = 0; dut->pcm_tready_i = 1; dut->pcm_tlast_i = 0;
    dut->wire_chans_i = 2; dut->servo_en_i = 0;

    // ================================================================
    // [W] half-beat walker rates (USER 1-to-1 mapping rule): fill_o is
    // the exact pair count while the boot prefill holds the feeder.
    // C=2: 1 pair/beat; C=8: first-pair-only = 1 per 4 beats; C=3: 2
    // per 3 beats (odd straddle); C=1: 2 pairs/beat via the staging
    // queue (back-to-back beats included). Full reset afterwards.
    // ================================================================
    {
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

    // async clocks: clk_i 10ns period, clk_audio 40.690ns (24.576 MHz) -
    // phase-walk via a picosecond accumulator
    uint64_t t = 0;                     // picoseconds
    uint64_t next_i = 5000, next_a = 20345;
    auto tickmin = [&](){
        if (next_i <= next_a) { t = next_i; dut->clk_i ^= 1; next_i += 10000/2; }
        else                  { t = next_a; dut->clk_audio_i ^= 1; next_a += 40690/2; }
        dut->eval();
    };
    for (int i = 0; i < 64; i++) tickmin();
    dut->rst_n = 1;

    // feed: bursts of 6 pairs (one PDU) every 125 us; payload = ramp
    // (L = idx, R = idx ^ 0xFFFFFF) so any slot mixup is visible
    uint32_t idx = 1;                      // avoid 0 (matches silence)
    uint64_t next_burst_ps = 200000;       // first PDU at 200 ns (sim-fast)
    int      in_burst = 0;
    uint64_t burst_gap_ps = 2000000;       // 2 us between "PDUs" (sim-compressed 125us)

    // I2S decoder on the audio-domain outputs
    int sclk_q=0, lrck_q=1, bit= -1; uint32_t acc=0;
    std::vector<uint32_t> got;

    while (t < 3000000000ull && got.size() < 400) {   // 3 ms sim
        int was_clk_i = dut->clk_i;
        tickmin();
        // feeder on clk_i rising
        if (!was_clk_i && dut->clk_i) {
            if (in_burst == 0 && t >= next_burst_ps) { in_burst = 6; next_burst_ps += burst_gap_ps; }
            if (in_burst > 0 && dut->pcm_tvalid_i == 0) {
                uint32_t l = idx & 0xFFFFFF, r = (idx ^ 0xFFFFFF) & 0xFFFFFF;
                // S32BE lanes: bytes 0..2 = L msb..lsb, byte3=0, 4..6 = R
                uint64_t d = 0;
                d |= (uint64_t)((l >> 16) & 0xFF) << 0;
                d |= (uint64_t)((l >> 8)  & 0xFF) << 8;
                d |= (uint64_t)(l & 0xFF)         << 16;
                d |= (uint64_t)((r >> 16) & 0xFF) << 32;
                d |= (uint64_t)((r >> 8)  & 0xFF) << 40;
                d |= (uint64_t)(r & 0xFF)         << 48;
                dut->pcm_tdata_i = d; dut->pcm_tvalid_i = 1;
                idx++; in_burst--;
            } else {
                dut->pcm_tvalid_i = 0;
            }
        }
        // decoder on audio clk rising
        int sclk = dut->i2s_sclk_o, lrck = dut->i2s_lrck_o;
        if (sclk && !sclk_q) {
            if (lrck_q && !lrck) { bit = 0; acc = 0; }        // LEFT begins
            else if (bit >= 0) {
                bit++;
                // textbook I2S chip: MSB on the SECOND rising edge after the
                // LRCK transition (slots 1..24), exactly like the CS4344
                if (bit >= 1 && bit <= 24) acc = (acc << 1) | (dut->i2s_sdin_o & 1);
                if (bit == 24) { got.push_back(acc); bit = -1; }
            }
            lrck_q = lrck;
        }
        sclk_q = sclk;
    }

    // verdict: after startup, decoded LEFT samples must be CONSECUTIVE ramp
    // values (repeats allowed ONLY when the feed starved - none here: feed
    // 6/2us >> drain 1/20.8us) with NO stuck/garbage values
    // start at the first NONZERO sample: the prefill recenter pads a few
    // zero frames before output begins (count depends on the release level)
    size_t first = 4;
    while (first < got.size() && got[first] == 0) first++;
    int consecutive=0, best=0; uint32_t prev=0; long bad_jumps=0;
    for (size_t i = first; i < got.size(); i++) {
        if (got[i] == prev + 1) { consecutive++; best = consecutive > best ? consecutive : best; }
        else if (i > first) { bad_jumps++; consecutive = 0; }
        prev = got[i];
    }
    printf("decoded %zu samples, longest consecutive run %d, bad jumps %ld\n",
           got.size(), best, bad_jumps);
    for (size_t i = 4; i < 20 && i < got.size(); i++) printf("  s[%zu]=0x%06X\n", i, got[i]);
    ck("[A] enough samples decoded", got.size() >= 100, 1);
    ck("[A] zero bad jumps (no CDC corruption)", bad_jumps == 0, 1);
    printf("i2spb-async: %ld checks, %ld failures\n", checks, fails);
    return fails ? 1 : 0;
}
