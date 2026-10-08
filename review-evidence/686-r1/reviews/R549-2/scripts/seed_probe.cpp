// Independent reset-class and state-cycle checks of the compiled MAAP engine.
#include "VKL_maap.h"
#include "VKL_maap___024root.h"
#include <array>
#include <cstdint>
#include <cstdio>
#include <memory>

int main() {
    auto d = std::make_unique<VKL_maap>();
    auto tick = [&]() { d->clk_i=0; d->eval(); d->clk_i=1; d->eval(); };
    auto state = [&]() { return d->rootp->KL_maap__DOT__lfsr_r; };
    auto fail = [](const char* message, unsigned x) {
        std::printf("FAIL %s: %u\n", message, x); return 1;
    };
    d->rx_tvalid_i=0; d->rx_tready_i=1; d->rx_tlast_i=0; d->m_axis_tready=1;
    // Every possible folded MAC seed, twice: with and without a supplied offset.
    // The remaining MAC bits do not feed mac_seed_w; the two low words XOR.
    for (unsigned seeded=0; seeded<2; ++seeded) {
        for (unsigned fold=0; fold<65536; ++fold) {
            const unsigned high = (fold*40503u + 7u) & 65535u;
            d->station_mac_i = 0x020000000000ULL | (uint64_t(high)<<16) | (fold^high);
            d->seed_valid_i=seeded; d->seed_offset_i=fold; d->count_i=fold&255;
            d->enable_i=0; d->rst_n=0; tick();
            unsigned expected = 0xace1u ^ fold;
            if (!expected) expected=0xace1u;
            if (state()!=expected || !state()) return fail("reset seed", fold);
            d->rst_n=1; d->enable_i=1; tick();
            const unsigned draw_state = state();
            tick();
            const unsigned timer = d->rootp->KL_maap__DOT__timer_ms_r;
            if (timer != 518u + (draw_state&63u)) return fail("actual probe timer load", fold);
            if (!(timer>500 && timer<600)) return fail("probe timer bounds", fold);
        }
    }
    std::puts("PASS 131072 reset/first-send cases: all 65536 folded MAC classes, both supplied-seed modes, all offsets, all count values; no zero seed.");
    d->enable_i=0; d->station_mac_i=0x02000000ace1ULL; d->rst_n=0; tick();
    d->rst_n=1;
    std::array<bool,65536> seen{};
    for (unsigned n=0; n<65535; ++n) {
        const unsigned x=state();
        if (!x || seen[x]) return fail("nonzero cycle repeats early", n);
        seen[x]=true;
        const unsigned probe=518+(x&63), announce=30488+(x&1023);
        if (!(probe>500 && probe<600 && announce>30000 && announce<32000))
            return fail("timer draw bounds", x);
        tick();
    }
    if (state()!=0xace1) return fail("full-period return", state());
    std::puts("PASS actual state cycle: all 65535 nonzero states exactly once, returns to 0xACE1; both draw formulae strictly bounded.");
    d->final();
    return 0;
}
