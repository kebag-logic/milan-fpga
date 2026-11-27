// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_status_leds (#1018): each LED through each state of its input, the LD0
// activity blink and its hold, and the low PWM duty. 100 kHz clock, so a
// millisecond is 100 clocks; the blink is 40 ms off then at least 60 ms on.

#include "VKL_status_leds.h"
#include "verilated.h"

#include <array>
#include <cstdio>
#include <memory>

static int &checks() { static int n = 0; return n; }
static int &fails() { static int n = 0; return n; }
#define CHECK(c, ...) do { ++checks(); if (!(c)) { std::printf("FAIL %s:%d: ", __FILE__, __LINE__); \
    std::printf(__VA_ARGS__); std::printf("\n"); ++fails(); } } while (0)

struct Leds {
    std::unique_ptr<VKL_status_leds> model = std::make_unique<VKL_status_leds>();
    VKL_status_leds *d = model.get();
    std::array<unsigned, 4> on_cnt{};
    unsigned tot = 0;

    void cyc(int n = 1)
    {
        for (int i = 0; i < n; ++i) {
            d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval();
            for (int k = 0; k < 4; ++k) on_cnt[k] += (d->led_o >> k) & 1;
            ++tot;
        }
    }
    void clear() { on_cnt.fill(0); tot = 0; }
    int st(int k) const { return (d->state_o >> k) & 1; }

    // over whole PWM periods: an on LED is lit 16/256 of the time, an off one never
    void duty(const char *what, unsigned mask)
    {
        clear(); cyc(256 * 8);
        for (int k = 0; k < 4; ++k) {
            unsigned want = ((mask >> k) & 1) ? 16 * 8 : 0;
            CHECK(on_cnt[k] == want, "%s: LD%d lit %u of %u clocks, expected %u", what, k, on_cnt[k], tot, want);
        }
    }
    ~Leds() { d->final(); }
};

int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    Leds bench;
    VKL_status_leds *d = bench.d;
    auto cyc = [&](int n = 1) { bench.cyc(n); };
    auto clear = [&] { bench.clear(); };
    auto st = [&](int k) { return bench.st(k); };
    auto duty = [&](const char *what, unsigned mask) { bench.duty(what, mask); };
    d->rst_ni = 0; d->link_up_i = 0; d->act_i = 0; d->usb_ok_i = 0; d->stream_i = 0; d->clock_i = 0;
    cyc(4); d->rst_ni = 1; cyc(4);

    // each input through each state, alone
    duty("all off", 0x0);
    d->link_up_i = 1; cyc(2); CHECK(d->state_o == 0x1, "LD0 alone on link (%x)", d->state_o); duty("link", 0x1);
    d->link_up_i = 0; d->usb_ok_i = 1; cyc(2); CHECK(d->state_o == 0x2, "LD1 alone (%x)", d->state_o); duty("usb", 0x2);
    d->usb_ok_i = 0; d->stream_i = 1; d->clock_i = 0; cyc(2); CHECK(d->state_o == 0x4, "LD2 alone (%x)", d->state_o); duty("stream", 0x4);
    d->stream_i = 0; d->clock_i = 1; cyc(2); CHECK(d->state_o == 0x8, "LD3 alone (%x)", d->state_o); duty("clock", 0x8);
    d->stream_i = 1; d->clock_i = 1; d->usb_ok_i = 1; d->link_up_i = 1; cyc(2); CHECK(d->state_o == 0xF, "all on"); duty("all on", 0xF);
    d->stream_i = 0; d->clock_i = 0; d->usb_ok_i = 0;

    // LD0: one frame blinks it off, for 40 ms (4000 clocks, +-1 ms of tick phase)
    cyc(1000);
    d->act_i = 1; cyc(1); d->act_i = 0;
    int off = 0; while (!st(0) && off < 20000) { cyc(1); ++off; }
    CHECK(off >= 3900 && off <= 4100, "one frame: LD0 off for %d clocks, expected 40 ms", off);
    // the hold: a frame right after the blink does not blink it again for 60 ms
    d->act_i = 1; cyc(1); d->act_i = 0; cyc(10);
    CHECK(st(0), "a frame inside the 60 ms hold does not blink");
    cyc(6100);
    d->act_i = 1; cyc(1); d->act_i = 0; cyc(10);
    CHECK(!st(0), "after the hold the next frame blinks");
    cyc(5000);

    // steady traffic: LD0 flickers 40 off / 60 on, never dark
    clear(); int lit = 0, n = 100000;
    d->act_i = 1;
    for (int i = 0; i < n; ++i) { cyc(1); lit += st(0); }
    d->act_i = 0;
    CHECK(lit > n * 55 / 100 && lit < n * 65 / 100, "steady traffic: LD0 on %d of %d clocks, expected 60 %%", lit, n);
    // link down: no blink, LD0 off whatever the traffic
    cyc(12000);
    d->link_up_i = 0; cyc(2);
    d->act_i = 1; cyc(500); d->act_i = 0;
    CHECK(!st(0), "link down: LD0 off");
    d->link_up_i = 1; cyc(2);
    CHECK(st(0), "link back: LD0 on at once, no stale blink");

    std::printf("%d checks: %d PASS, %d FAIL\n", checks(), checks() - fails(), fails());
    return fails() ? 1 : 0;
}
